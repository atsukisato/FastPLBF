from PLBF import PLBF
from FastPLBF import FastPLBF
from FastPLBFpp import FastPLBFpp
from utils.const import EPS

import random
import time



def create_ieal_g_h(N = 1000):
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

def create_not_ieal_g_h(N = 1000):
    g_h_dif = [(random.random() - 0.5) for _ in range(N)]
    g_h_list = [max(EPS, g_h_dif[0])]
    for i in range(1, N):
        g_h_list.append(max(EPS, g_h_list[i-1] + g_h_dif[i]))

    unnormed_h = [random.random() for _ in range(N)]
    sum_unnormed_h = sum(unnormed_h)
    h = [uh / sum_unnormed_h for uh in unnormed_h]

    unnormed_g = [h * g_h for h, g_h in zip(h, g_h_list)]
    sum_unnormed_g = sum(unnormed_g)
    g= [ug / sum_unnormed_g for ug in unnormed_g]

    return g, h

def test(test_times = 1, N = 1000, F = 0.001, k = 5, n = 1000000):

    for seed in range(test_times):
        print("---")
        random.seed(seed)
        g, h = create_ieal_g_h(N)

        p1 = PLBF(g, h, F, N, k, n)
        p2 = FastPLBF(g, h, F, N, k, n)
        p3 = FastPLBFpp(g, h, F, N, k, n)

        if (p1.memory_backup_bf != p2.memory_backup_bf) or (p2.memory_backup_bf != p3.memory_backup_bf):
            print(f"NOT EQUAL RESUKT(seed: {seed}): PLBF: {p1.memory_backup_bf}, FastPLBF: {p2.memory_backup_bf}, FastPLBF++: {p3.memory_backup_bf}")


def test2(test_times = 1, N = 1000, F = 0.001, k = 5, n = 1000000):

    for seed in range(test_times):
        print("---")
        random.seed(seed)
        g, h = create_not_ieal_g_h(N)
            
        p1 = PLBF(g, h, F, N, k, n)
        p2 = FastPLBF(g, h, F, N, k, n)
        p3 = FastPLBFpp(g, h, F, N, k, n)

        if p1.memory_backup_bf != p2.memory_backup_bf :
            print(f"NOT EQUAL RESUKT(seed: {seed}): PLBF: {p1.memory_backup_bf}, FastPLBF: {p2.memory_backup_bf}, FastPLBF++: {p3.memory_backup_bf}")
        elif p1.memory_backup_bf > p3.memory_backup_bf:
            print(f"Fast PLBF++'s memory is smaller than PLBF(seed: {seed}): PLBF: {p1.memory_backup_bf}, FastPLBF: {p2.memory_backup_bf}, FastPLBF++: {p3.memory_backup_bf}")
        


if __name__ == "__main__":
    test(test_times = 100)
    test2(test_times = 100)

