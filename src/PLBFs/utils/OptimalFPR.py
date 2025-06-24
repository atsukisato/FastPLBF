from .prList import prList
from .const import EPS

def OptimalFPR(g: prList, h: prList, t: list[float], F: float, k: int) -> list[float]:
    """_summary_

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        t (list[float]): threshold boundaries of each region
        F (float): target overall fpr
        k (int): number of regions

    Returns:
        list[float]: FPRs of each region (1-index)
    """


    N = g.N

    pos_pr_list = [g.acc_range(t[i-1], t[i]) for i in range(1, k+1)]
    neg_pr_list = [h.acc_range(t[i-1], t[i]) for i in range(1, k+1)]

    assert(abs(sum(pos_pr_list) - 1) < EPS)
    assert(abs(sum(neg_pr_list) - 1) < EPS)

    valid_list = [True for i in range(k)]

    for i in range(k):
        if neg_pr_list[i] == 0:
            valid_list[i] = False

    while True:
        valid_pos_pr_sum = 0
        valid_neg_pr_sum = 0
        invalid_pos_pr_sum = 0
        invalid_neg_pr_sum = 0
        for val, pos_pr, neg_pr in zip(valid_list, pos_pr_list, neg_pr_list):
            if val:
                valid_pos_pr_sum += pos_pr
                valid_neg_pr_sum += neg_pr
            else:
                invalid_pos_pr_sum += pos_pr
                invalid_neg_pr_sum += neg_pr
        normed_F = (F - invalid_neg_pr_sum) / (1 - invalid_neg_pr_sum)

        if valid_pos_pr_sum == 0:
            # The F is too large that the Bloom filter does not need to be used.
            opt_fpr_list = []
            for i in range(k):
                if valid_list[i]:
                    opt_fpr_list.append(0.0)
                else:
                    opt_fpr_list.append(1.0)
            # f to 1-index
            opt_fpr_list.insert(0, None)

            return opt_fpr_list

        normed_pos_pr_list = [0 for i in range(k)]
        normed_neg_pr_list = [0 for i in range(k)]
        for idx, (pos_pr, neg_pr) in enumerate(zip(pos_pr_list, neg_pr_list)):
            if valid_list[idx]:
                normed_pos_pr_list[idx] = pos_pr / valid_pos_pr_sum
                normed_neg_pr_list[idx] = neg_pr / valid_neg_pr_sum

        opt_fpr_list = [0 for i in range(k)]
        for idx, (n_pos_pr, n_neg_pr) in enumerate(zip(normed_pos_pr_list, normed_neg_pr_list)):
            if not valid_list[idx]:
                opt_fpr_list[idx] = 1
            else:
                opt_fpr_list[idx] = normed_F * n_pos_pr / n_neg_pr

        ok = True
        for idx, opt_fpr in enumerate(opt_fpr_list):
            if opt_fpr > 1:
                ok = False
                valid_list[idx] = False
        if ok:
            break

    # f to 1-index
    opt_fpr_list.insert(0, None)

    assert(len(opt_fpr_list) == k+1)
    return opt_fpr_list

