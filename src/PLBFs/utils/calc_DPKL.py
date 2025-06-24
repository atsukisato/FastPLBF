import math
from typing import Tuple
from .prList import prList
from .const import INF


def calc_DPKL(g: prList, h: prList, k: int, j: int = None) -> Tuple[list[list[float]], list[list[int]]]:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        k (int): number of regions
        j (int): 1-th to j-th segments are clustered

    Returns:
        Tuple[list[list[float]], list[list[int]]]: DPKL, DPPre
    """

    N = g.N
    if j is None:
        j = N

    DPKL = [[-INF for _ in range(k + 1)] for _ in range(j + 1)]
    DPPre = [[None for _ in range(k + 1)] for _ in range(j + 1)]
    DPKL[0][0] = 0
    for n in range(1, j + 1):
        for q in range(1, k + 1):
            for i in range(1, n + 1):
                # i-th to n-th segments are clustered into q-th region

                Pos = g.acc_range_idx(i, n)
                Neg = h.acc_range_idx(i, n)
                
                if Neg == 0:
                    continue
                if Pos == 0:
                    tmp_sum = DPKL[i-1][q-1] + 0
                else:
                    tmp_sum = DPKL[i-1][q-1] + Pos * math.log(Pos / Neg)

                if DPKL[n][q] < tmp_sum:
                    DPKL[n][q] = tmp_sum
                    DPPre[n][q] = i-1

    return DPKL, DPPre

