import math
from .prList import prList

def ExpectedFPR(g: prList, h: prList, t: list[float], f: list[float], n: int) -> float:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-key density of each segmenet
        t (list[float]): threshold boundaries of each region
        f (list[float]): FPRs of each region
        n (int): the number of keys
    Returns:
        float: expectedFPR
    """

    N = g.N
    k = len(t) - 1

    expectedFPR = 0
    for i in range(1, k+1):
        neg_pr = h.acc_range(t[i-1], t[i])
        expectedFPR += neg_pr * f[i]

    return expectedFPR


