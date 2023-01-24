import math
from utils.prList import prList

def OptimalFPR(g: prList, h: prList, t: list[float], F: float, k: int) -> list[float]:
    """_summary_

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        t (list[float]): threshold boundaries of each region
        F (float): target overall fpr
        k (int): number of regions

    Returns:
        list[float]: FPRs of each region
    """

    N = g.N
    assert(h.N == N)
    assert(len(t) == k+1)

    assert(N == 4)
    assert(k == 2)
    
    f = [None, 0.50, 1]











    assert(len(f) == k+1)
    return f

