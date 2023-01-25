import math
from typing import Tuple
from utils.prList import prList
from utils.const import INF


def calc_DPKL(g: prList, h: prList, k: int) -> Tuple[list[list[float]], list[list[int]]]:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        k (int): number of regions

    Returns:
        Tuple[list[list[float]], list[list[int]]]: DPKL, DPPre
    """

    N = g.N

    DPKL = [[-INF for _ in range(k + 1)] for _ in range(N + 1)]
    DPPre = [[None for _ in range(k + 1)] for _ in range(N + 1)]
    DPKL[0][0] = 0
    for n in range(1, N + 1):
        for j in range(1, k + 1):
            for i in range(1, n + 1):
                # i-th to n-th segments are clustered into j-th region

                Pos = g.acc_range_idx(i, n)
                Neg = h.acc_range_idx(i, n)
                
                if Neg == 0:
                    continue
                if Pos == 0:
                    tmp_sum = DPKL[i-1][j-1] + 0
                else:
                    tmp_sum = DPKL[i-1][j-1] + Pos * math.log(Pos / Neg)

                if DPKL[n][j] < tmp_sum:
                    DPKL[n][j] = tmp_sum
                    DPPre[n][j] = i-1

    return DPKL, DPPre

