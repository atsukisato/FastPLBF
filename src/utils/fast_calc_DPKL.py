import math
from typing import Tuple
from utils.prList import prList
from utils.const import INF


def fast_calc_DPKL(g: prList, h: prList, k: int) -> Tuple[list[list[float]], list[list[int]]]:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        k (int): number of regions

    Returns:
        Tuple[list[list[float]], list[list[int]]]: DPKL, DPPre
    """

    assert(isinstance(g, prList))
    assert(isinstance(h, prList))
    assert(isinstance(k, int))
    N = g.N
    assert(h.N == N)

    DPKL = [[-INF for _ in range(k + 1)] for _ in range(N + 1)]
    DPPre = [[None for _ in range(k + 1)] for _ in range(N + 1)]
    DPKL[0][0] = 0
    for j in range(1, k + 1):
        

        for n in range(1, N + 1):
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
            
    # for j in range(K + 1):
    #     row = ""
    #     for n in range(N + 1):
    #         if DPPre[n][j][0] is None:
    #             row += "  _"
    #         else:
    #             if DPPre[n][j][0] < 10:
    #                 row += f"  {DPPre[n][j][0]}"
    #             else:
    #                 row += f" {DPPre[n][j][0]}"
    #     print(row)
    
    # for j in range(K + 1):
    #     row = []
    #     for n in range(N + 1):
    #         row.append(DPKL[n][j])
    #     print(dekoboko_str(row))

    return DPKL, DPPre

