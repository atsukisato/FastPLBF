from utils.ThresMaxDivDP import fastMaxDivDP, ThresMaxDiv
from utils.OptimalFPR_M import OptimalFPR_M
from utils.SpaceUsed import SpaceUsed
from utils.ExpectedFPR import ExpectedFPR
from utils.const import INF
from PLBF_M import PLBF_M

import time
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

class FastPLBFpp_M(PLBF_M):
    def __init__(self, pos_keys: list, pos_scores: list[float], neg_scores: list[float], M: float, N: int, k: int):
        """
        Args:
            pos_keys (list): keys
            pos_scores (list[float]): scores of keys
            neg_scores (list[float]): scores of non-keys
            M (float): the target memory usage for backup Bloom filters
            N (int): number of segments
            k (int): number of regions
        """

        # assert 
        assert(isinstance(pos_keys, list))
        assert(isinstance(pos_scores, list))
        assert(len(pos_keys) == len(pos_scores))
        assert(isinstance(neg_scores, list))
        assert(isinstance(M, float))
        assert(0 < M)
        assert(isinstance(N, int))
        assert(isinstance(k, int))

        for score in pos_scores:
            assert(0 <= score <= 1)
        for score in neg_scores:
            assert(0 <= score <= 1)

        
        self.M = M
        self.N = N
        self.k = k
        self.n = len(pos_keys)


        segment_thre_list, g, h = self.divide_into_segments(pos_scores, neg_scores)
        self.find_best_t_and_f(segment_thre_list, g, h)
        self.insert_keys(pos_keys, pos_scores)

    def find_best_t_and_f(self, segment_thre_list, g, h):
        minExpectedFPR = INF
        t_best = None
        f_best = None

        DPKL, DPPre = fastMaxDivDP(g, h, self.N, self.k)
        for j in range(self.k, self.N+1):
            t = ThresMaxDiv(DPPre, j, self.k, segment_thre_list)
            if t is None:
                continue
            f = OptimalFPR_M(g, h, t, self.M, self.k, self.n)
            if minExpectedFPR > ExpectedFPR(g, h, t, f, self.n):
                minExpectedFPR = ExpectedFPR(g, h, t, f, self.n)
                t_best = t
                f_best = f

        self.t = t_best
        self.f = f_best
        self.memory_usage_of_backup_bf = SpaceUsed(g, h, t, f, self.n)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', action="store", dest="data_path", type=str, required=True,
                        help="path of the dataset")
    parser.add_argument('--N', action="store", dest="N", type=int, required=True,
                        help="N: the number of segments")
    parser.add_argument('--k', action="store", dest="k", type=int, required=True,
                        help="k: the number of regions")
    parser.add_argument('--M', action="store", dest="M", type=float, required=True,
                        help="M: the target memory usage for backup Bloom filters")

    results = parser.parse_args()

    DATA_PATH = results.data_path
    N = results.N
    k = results.k
    M = results.M

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

    construct_start = time.time()
    plbf = FastPLBFpp_M(pos_keys, pos_scores, train_neg_scores, M, N, k)
    construct_end = time.time()

    # assert : no false negative
    for key, score in zip(pos_keys, pos_scores):
        assert(plbf.contains(key, score))
    
    # test
    fp_cnt = 0
    for key, score in zip(test_neg_keys, test_neg_scores):
        if plbf.contains(key, score):
            fp_cnt += 1
    
    print(f"Construction Time: {construct_end - construct_start}")
    print(f"Memory Usage of Backup BF: {plbf.memory_usage_of_backup_bf}")
    print(f"False Positive Rate: {fp_cnt / len(test_neg_keys)} [{fp_cnt} / {len(test_neg_keys)}]")


