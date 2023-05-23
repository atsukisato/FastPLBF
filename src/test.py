from PLBFs.PLBF import PLBF
from PLBFs.FastPLBF import FastPLBF
from PLBFs.FastPLBFpp import FastPLBFpp

import random
import time
import math


def create_ieal_g_h(N):
    g_h_dif = [random.random() for _ in range(N)]
    g_h_list = [g_h_dif[0]]
    for i in range(1, N):
        g_h_list.append(g_h_list[i-1] + g_h_dif[i])

    unnormed_h = [random.random() for _ in range(N)]
    sum_unnormed_h = sum(unnormed_h)
    h = [uh / sum_unnormed_h for uh in unnormed_h]

    unnormed_g = [h * g_h for h, g_h in zip(h, g_h_list)]
    sum_unnormed_g = sum(unnormed_g)
    g= [ug / sum_unnormed_g for ug in unnormed_g]

    return g, h

def create_not_ieal_g_h(N):
    unnormed_h = [random.random() for _ in range(N)]
    sum_unnormed_h = sum(unnormed_h)
    h = [uh / sum_unnormed_h for uh in unnormed_h]

    unnormed_g = [random.random() for _ in range(N)]
    sum_unnormed_g = sum(unnormed_g)
    g = [ug / sum_unnormed_g for ug in unnormed_g]

    return g, h

def make_scores_list(pr_list, N, n):
    assert(len(pr_list) == N)
    scores_list = []
    for region_idx, pr in enumerate(pr_list):
        num = math.floor(pr * n + 0.5)
        for _ in range(num):
            score = (region_idx + random.random()) / N
            scores_list.append(score)
    return scores_list

def test(test_times = 1, N = 1000, F = 0.001, k = 5, pos_num = 50000, train_neg_num = 50000, test_neg_num = 50000, ideal = True):

    for seed in range(test_times):
        random.seed(seed)
        if ideal :
            g, h = create_ieal_g_h(N)
        else:
            g, h = create_not_ieal_g_h(N)
        
        pos_scores = make_scores_list(g, N, pos_num)
        train_neg_scores = make_scores_list(h, N, train_neg_num)
        test_neg_scores  = make_scores_list(h, N, test_neg_num)

        pos_keys = [f"key_{i}" for i in range(len(pos_scores))]
        test_neg_keys = [f"nonkey_{i}" for i in range(len(test_neg_scores))]

        time1 = time.time()
        plbf        = PLBF(pos_keys, pos_scores, train_neg_scores, F, N, k)
        time2 = time.time()
        fastPlbf    = FastPLBF(pos_keys, pos_scores, train_neg_scores, F, N, k)
        time3 = time.time()
        fastPlbfpp  = FastPLBFpp(pos_keys, pos_scores, train_neg_scores, F, N, k)
        time4 = time.time()

        if ideal :
            assert(plbf.memory_usage_of_backup_bf == fastPlbf.memory_usage_of_backup_bf and fastPlbf.memory_usage_of_backup_bf == fastPlbfpp.memory_usage_of_backup_bf)
        else:
            assert(plbf.memory_usage_of_backup_bf == fastPlbf.memory_usage_of_backup_bf and fastPlbf.memory_usage_of_backup_bf <= fastPlbfpp.memory_usage_of_backup_bf)

        # assert : no false negative
        for p in [plbf, fastPlbf, fastPlbfpp]:
            for key, score in zip(pos_keys, pos_scores):
                assert(p.contains(key, score))
        
        # test
        fp_cnts = []
        for p in [plbf, fastPlbf, fastPlbfpp]:
            fp_cnt = 0
            for key, score in zip(test_neg_keys, test_neg_scores):
                if p.contains(key, score):
                    fp_cnt += 1
            fp_cnts.append(fp_cnt)
        
        if ideal:
            assert(fp_cnts[0] == fp_cnts[1] and fp_cnts[1] == fp_cnts[2])

        print(f"OK (Construction Time[s] : PLBF {time2 - time1}, FastPLBF {time3 - time2}, FastPLBF++ {time4 - time3}")
    

if __name__ == "__main__":
    test(test_times = 10, ideal = True)
    test(test_times = 10, ideal = False)
