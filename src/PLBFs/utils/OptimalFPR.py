from .prList import prList
from .const import EPS


def OptimalFPR(g: prList, h: prList, t: list[float], F: float, k: int) -> list[float]:
    """Compute the optimal FPR of each region in O(k log k) time.

    Args:
        g (prList): key density of each segment
        h (prList): non-key density of each segment
        t (list[float]): threshold boundaries of each region
        F (float): target overall fpr
        k (int): number of regions

    Returns:
        list[float]: FPRs of each region (1-index)
    """

    pos_pr_list = [g.acc_range(t[i-1], t[i]) for i in range(1, k+1)]
    neg_pr_list = [h.acc_range(t[i-1], t[i]) for i in range(1, k+1)]

    assert(abs(sum(pos_pr_list) - 1) < EPS)
    assert(abs(sum(neg_pr_list) - 1) < EPS)

    order = [i for i in range(k) if neg_pr_list[i] != 0]
    order.sort(key=lambda i: pos_pr_list[i] / neg_pr_list[i], reverse=True)
    L = len(order)

    suf_pos = [0.0] * (L + 1)
    suf_neg = [0.0] * (L + 1)
    for j in range(L - 1, -1, -1):
        suf_pos[j] = suf_pos[j+1] + pos_pr_list[order[j]]
        suf_neg[j] = suf_neg[j+1] + neg_pr_list[order[j]]

    m = 0
    invalid_neg_pr_sum = 0.0
    while True:
        valid_pos_pr_sum = suf_pos[m]
        valid_neg_pr_sum = suf_neg[m]

        if valid_pos_pr_sum == 0:
            opt_fpr_list = [1.0 for _ in range(k)]
            for i in order[m:]:
                opt_fpr_list[i] = 0.0
            opt_fpr_list.insert(0, None)
            return opt_fpr_list

        normed_F = (F - invalid_neg_pr_sum) / (1 - invalid_neg_pr_sum)

        top = order[m]
        top_fpr = normed_F * (pos_pr_list[top] / valid_pos_pr_sum) / (neg_pr_list[top] / valid_neg_pr_sum)
        if top_fpr > 1:
            invalid_neg_pr_sum += neg_pr_list[top]
            m += 1
            continue
        break

    opt_fpr_list = [1 for _ in range(k)]
    for i in order[m:]:
        opt_fpr_list[i] = normed_F * (pos_pr_list[i] / valid_pos_pr_sum) / (neg_pr_list[i] / valid_neg_pr_sum)

    opt_fpr_list.insert(0, None)

    assert(len(opt_fpr_list) == k+1)
    return opt_fpr_list
