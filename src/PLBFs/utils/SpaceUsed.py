import math
from .prList import prList

def SpaceUsed(g: prList, h: prList, t: list[float], f: list[float], n: int) -> float:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        t (list[float]): threshold boundaries of each region
        f (list[float]): FPRs of each region
        n (int): the number of keys
    Returns:
        float: spaceUsed
    """

    N = g.N
    k = len(t) - 1

    spaceUsed = 0
    for i in range(1, k+1):
        pos_pr = g.acc_range(t[i-1], t[i])
        pos_num = pos_pr * n
        if pos_num == 0:
            continue
        fpr = f[i]
        hash_num = math.log(fpr) / math.log(0.5)
        m = hash_num * pos_num / math.log(2)
        spaceUsed += m

    return spaceUsed


