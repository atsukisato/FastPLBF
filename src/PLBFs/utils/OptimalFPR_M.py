from .prList import prList
from .const import EPS
import math

def calc_K_sum(pos_pr_list: list[float], neg_pr_list: list[float], valid_list: list[bool]) -> float:
    K_sum = 0
    for pos_pr, neg_pr, valid in zip(pos_pr_list, neg_pr_list, valid_list):
        if not valid:
            continue
        if pos_pr == 0:
            continue
        K_sum += pos_pr * math.log2(pos_pr / neg_pr)
    return K_sum

def calc_G_sum(pos_pr_list: list[float], neg_pr_list: list[float], valid_list: list[bool]) -> float:
    G_sum = 0
    for pos_pr, neg_pr, valid in zip(pos_pr_list, neg_pr_list, valid_list):
        if valid:
            continue
        G_sum += pos_pr
    return G_sum

def some_f_i_is_greater_than_1(f: list[float]) -> bool:
    for f_i in f:
        if f_i > 1:
            return True
    return False

def OptimalFPR_M(g: prList, h: prList, t: list[float], M: float, k: int, n: int) -> list[float]:
    """_summary_

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        t (list[float]): threshold boundaries of each region
        M (float): the target memory usage for backup Bloom filters
        k (int): number of regions
        n (int): number of keys

    Returns:
        list[float]: FPRs of each region (1-index)
    """

    c = math.log2(math.e)

    pos_pr_list = [g.acc_range(t[i-1], t[i]) for i in range(1, k+1)]
    neg_pr_list = [h.acc_range(t[i-1], t[i]) for i in range(1, k+1)]

    assert(abs(sum(pos_pr_list) - 1) < EPS)
    assert(abs(sum(neg_pr_list) - 1) < EPS)

    valid_list = [True for i in range(k)]

    for i in range(k):
        if neg_pr_list[i] == 0:
            valid_list[i] = False

    G_sum = calc_G_sum(pos_pr_list, neg_pr_list, valid_list)
    K_sum = calc_K_sum(pos_pr_list, neg_pr_list, valid_list)

    beta = (M + c * n * K_sum) / (c * n * (1 - G_sum))

    opt_fpr_list = [0 for i in range(k)]
    for i in range(k):
        if not valid_list[i]:
            opt_fpr_list[i] = 1
        else:
            opt_fpr_list[i] = math.pow(2, -beta) * pos_pr_list[i] / neg_pr_list[i]

    while some_f_i_is_greater_than_1(opt_fpr_list):
        for i in range(k):
            if opt_fpr_list[i] > 1:
                valid_list[i] = False
                opt_fpr_list[i] = 1

        G_sum = calc_G_sum(pos_pr_list, neg_pr_list, valid_list)
        K_sum = calc_K_sum(pos_pr_list, neg_pr_list, valid_list)

        beta = (M + c * n * K_sum) / (c * n * (1 - G_sum))

        for i in range(k):
            if not valid_list[i]:
                opt_fpr_list[i] = 1
            else:
                opt_fpr_list[i] = math.pow(2, -beta) * pos_pr_list[i] / neg_pr_list[i]


    # f to 1-index
    opt_fpr_list.insert(0, None)

    assert(len(opt_fpr_list) == k+1)
    return opt_fpr_list

