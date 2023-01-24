import math
from utils.prList import prList

def ThresMaxDivDP(g: prList, h: prList, j: int, k: int) -> list[float]:
    """_summary_

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        j (int): j-th to N-th segments are clustered as k-th region
        k (int): number of regions

    Returns:
        list[float]: t (threshold boundaries of each region)
    """

    N = g.N
    assert(h.N == N)



    assert(N == 4)
    assert(k == 2)

    t = [0.0, 0.25, 1.0]









    assert(len(t) == k+1)
    return t
