from .prList import prList
from .const import EPS
import math


def OptimalFPR_M(g: prList, h: prList, t: list[float], M: float, k: int, n: int) -> list[float]:
    """Compute the optimal FPR of each region in O(k log k) time.

    Args:
        g (prList): key density of each segment
        h (prList): non-key density of each segment
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

    order = [i for i in range(k) if neg_pr_list[i] != 0]
    order.sort(key=lambda i: pos_pr_list[i] / neg_pr_list[i], reverse=True)
    L = len(order)

    G_sum = sum(pos_pr_list[i] for i in range(k) if neg_pr_list[i] == 0)

    suf_K = [0.0] * (L + 1)
    for j in range(L - 1, -1, -1):
        i = order[j]
        term = 0.0
        if pos_pr_list[i] != 0:
            term = pos_pr_list[i] * math.log2(pos_pr_list[i] / neg_pr_list[i])
        suf_K[j] = suf_K[j+1] + term

    m = 0
    beta = None
    while m < L:
        K_sum = suf_K[m]
        beta = (M + c * n * K_sum) / (c * n * (1 - G_sum))
        top = order[m]
        if math.pow(2, -beta) * pos_pr_list[top] / neg_pr_list[top] > 1:
            G_sum += pos_pr_list[top]
            m += 1
            continue
        break

    opt_fpr_list = [1 for _ in range(k)]
    for i in order[m:]:
        opt_fpr_list[i] = math.pow(2, -beta) * pos_pr_list[i] / neg_pr_list[i]

    opt_fpr_list.insert(0, None)

    assert(len(opt_fpr_list) == k+1)
    return opt_fpr_list
