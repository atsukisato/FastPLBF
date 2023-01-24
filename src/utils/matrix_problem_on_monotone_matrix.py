import math
from typing import Tuple
from collections.abc import Callable
from utils.prList import prList
from utils.const import INF

def matrix_problem_on_monotone_matrix(f: Callable[[int, int], float], n: int, m: int) -> list[int]:
    
    """

    Args:
        f (Callable[[int, int], float]): returns B_{ij} (B is a monotone matrix) ({0 ... n-1} x {0 ... m-1} -> float).
        n (int): B is a n * m matrix
        m (int): B is a n * m matrix

    Returns:
        list[int]: a[i] = J(i) (i.e., a[i] is the smallest j that B_{i,j} equals the maximum value of the i-th row of B).
    """
    
    """_summary_

    Returns:
        _type_: _description_
    """

    assert(isinstance(f, Callable[[int, int], float]))
    a = [None for i in range(n)]

    def CalcJ(i, jl, jr):
        max = - INF
        argmax = None
        for j in range(jl, jr+1):
            if f(i, j) > max:
                max = f(i, j)
                argmax = j
        return argmax

    def RecSolveMP(il, ir, jl, jr):
        if il > ir:
            return
        i = math.floor((il + ir) / 2)
        j = CalcJ(i, jl, jr)
        a[i] = j
        RecSolveMP(il, i-1, jl, j)
        RecSolveMP(i+1, ir, j, jr)
    
    RecSolveMP(0, n-1, 0, m-1)
    return a
    
