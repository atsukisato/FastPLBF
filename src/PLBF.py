from utils.ThresMaxDivDP import ThresMaxDivDP
from utils.OptimalFPR import OptimalFPR
from utils.SpaceUsed import SpaceUsed
from utils.prList import prList
from utils.const import INF, EPS

import bisect
from bloom_filter import BloomFilter
import pandas as pd
from sklearn.model_selection import train_test_split

import argparse

class PLBF:
    def __init__(self, pos_keys: list, pos_scores: list[float], neg_scores: list[float], F: float, N: int, k: int):
        """
        Args:
            pos_keys (list): keys
            pos_scores (list[float]): scores of keys
            neg_scores (list[float]): scores of non-keys
            F (float): target overall fpr
            N (int): number of segments
            k (int): number of regions
        """

        self.assert_and_init_parameters(pos_keys, pos_scores, neg_scores, F, N, k)
        segment_thre_list, g, h = self.divide_into_segments(pos_scores, neg_scores)
        self.find_best_t_and_f(segment_thre_list, g, h)
        self.insert_keys(pos_keys, pos_scores)

    def assert_and_init_parameters(self, pos_keys: list, pos_scores: list[float], neg_scores: list[float], F: float, N: int, k: int):
        # assert 
        assert(isinstance(pos_keys, list))
        assert(isinstance(pos_scores, list))
        assert(len(pos_keys) == len(pos_scores))
        assert(isinstance(neg_scores, list))
        assert(isinstance(F, float))
        assert(0 < F < 1)
        assert(isinstance(N, int))
        assert(isinstance(k, int))

        for score in pos_scores:
            assert(0 <= score <= 1)
        for score in neg_scores:
            assert(0 <= score <= 1)

        # init
        self.F = F
        self.N = N
        self.k = k
        self.n = len(pos_keys)

    def divide_into_segments(self, pos_scores: list[float], neg_scores: list[float]):
        segment_thre_list = [i / self.N for i in range(self.N + 1)]
        g = prList(pos_scores, segment_thre_list)
        h = prList(neg_scores, segment_thre_list)
        return segment_thre_list, g, h

    def find_best_t_and_f(self, segment_thre_list, g, h):
        minSpaceUsed = INF
        t_best = None
        f_best = None

        for j in range(self.k, self.N+1):
            t = ThresMaxDivDP(g, h, j, self.k)
            if t is None:
                continue
            f = OptimalFPR(g, h, t, self.F, self.k)
            if minSpaceUsed > SpaceUsed(g, h, t, f, self.n):
                minSpaceUsed = SpaceUsed(g, h, t, f, self.n)
                t_best = t
                f_best = f

        self.t = t_best
        self.f = f_best
        self.memory_usage_of_backup_bf = minSpaceUsed

    def insert_keys(self, pos_keys: list, pos_scores: list[float]):
        pos_cnt_list = [0 for _ in range(self.k + 1)]
        for score in pos_scores:
            region_idx = self.get_region_idx(score)
            pos_cnt_list[region_idx] += 1
        

        self.backup_bloom_filters = [None for _ in range(self.k + 1)]
        for i in range(1, self.k + 1):
            if 0 < self.f[i] < 1:
                self.backup_bloom_filters[i] = BloomFilter(max_elements = pos_cnt_list[i], error_rate = self.f[i])
            elif self.f[i] == 0:
                assert(pos_cnt_list[i] == 0)
                self.backup_bloom_filters[i] = BloomFilter(max_elements = 1, error_rate = 1 - EPS)
        
        for key, score in zip(pos_keys, pos_scores):
            region_idx = self.get_region_idx(score)
            if self.backup_bloom_filters[region_idx] is not None:
                self.backup_bloom_filters[region_idx].add(key)

    def get_region_idx(self, score):
        region_idx = bisect.bisect_left(self.t, score)
        if region_idx == 0:
            region_idx = 1
        return region_idx

    def contains(self, key, score):
        assert(0 <= score <= 1)
        region_idx = self.get_region_idx(score)
        if self.backup_bloom_filters[region_idx] is None:
            return True
        
        return (key in self.backup_bloom_filters[region_idx])



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', action="store", dest="data_path", type=str, required=True,
                        help="path of the dataset")
    parser.add_argument('--N', action="store", dest="N", type=int, required=True,
                        help="N: the number of segments")
    parser.add_argument('--k', action="store", dest="k", type=int, required=True,
                        help="k: the number of regions")
    parser.add_argument('--F', action="store", dest="F", type=float, required=True,
                        help="F: the target overall fpr")

    results = parser.parse_args()

    DATA_PATH = results.data_path
    N = results.N
    k = results.k
    F = results.F

    data = pd.read_csv(DATA_PATH)
    negative_sample = data.loc[(data['label'] != 1)]
    positive_sample = data.loc[(data['label'] == 1)]
    train_negative, test_negative = train_test_split(negative_sample, test_size = 0.7, random_state = 0)
    

    pos_keys            = list(positive_sample['key'])
    pos_scores          = list(positive_sample['score'])
    train_neg_keys      = list(train_negative['key'])
    train_neg_scores    = list(train_negative['score'])
    test_neg_keys       = list(test_negative['key'])
    test_neg_scores     = list(test_negative['score'])


    plbf = PLBF(pos_keys, pos_scores, train_neg_scores, F, N, k)
    
    print("t:", plbf.t)
    print("f:", plbf.f)
    print("S_:", plbf.memory_usage_of_backup_bf)


    # assert
    for key, score in zip(pos_keys, pos_scores):
        assert(plbf.contains(key, score))
    
    # test
    fp_cnt = 0
    for key, score in zip(test_neg_keys, test_neg_scores):
        if plbf.contains(key, score):
            fp_cnt += 1
    
    print(f"False Positive Rate: {fp_cnt / len(test_neg_keys)} [{fp_cnt} / {len(test_neg_keys)}]")
