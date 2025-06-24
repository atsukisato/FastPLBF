import math
from typing import Tuple
from .prList import prList
from .const import INF
from .matrix_problem_on_monotone_matrix import matrix_problem_on_monotone_matrix



def fast_calc_DPKL(g: prList, h: prList, k: int) -> Tuple[list[list[float]], list[list[int]]]:
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
    for j in range(1, k + 1):
        
        def func_A(p: int, i: int) -> float:
            """
            func_A(p, i) 
            = A_{pi}

            = { -INF                        (i = p+1, p+2, ..., N-1)
              { DPKL[i-1][j-1] + dkl(i, p)  (i = 1, ..., p)

            Args:
                p (int): \in {1 ... N}
                i (int): \in {1 ... N}

            Returns:
                float: A_{pi}
            """
            
            if i >= p+1:
                return -INF
            
            Pos = g.acc_range_idx(i, p)
            Neg = h.acc_range_idx(i, p)

            if Neg == 0:
                return -INF
            if Pos == 0:
                return DPKL[i-1][j-1] + 0

            return DPKL[i-1][j-1] + Pos * math.log(Pos / Neg)

        max_args = matrix_problem_on_monotone_matrix(func_A, N, N)

        for n in range(1, N + 1):
            pre = max_args[n]
            DPKL[n][j] = func_A(n, pre)
            DPPre[n][j] = pre-1

    return DPKL, DPPre

