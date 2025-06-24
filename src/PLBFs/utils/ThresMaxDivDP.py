from typing import Tuple
from .prList import prList
from .calc_DPKL import calc_DPKL
from .fast_calc_DPKL import fast_calc_DPKL
from .const import INF


def ThresMaxDivDP(g: prList, h: prList, j: int, k: int) -> list[float]:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        j (int): j-th to N-th segments are clustered as k-th region
        k (int): number of regions

    Returns:
        list[float]: t (threshold boundaries of each region)
    """

    assert(isinstance(g, prList))
    assert(isinstance(h, prList))
    assert(isinstance(j, int))
    assert(isinstance(k, int))
    N = g.N
    assert(h.N == N)


    DPKL, DPPre = calc_DPKL(g, h, k, j)

    #  tracing the transitions backward from DPPre[j-1][k-1]
    if DPPre[j-1][k-1] is None:
        return None

    reversed_t = [1.0]

    now = j-1
    reversed_t.append(g.thre_list[now])
    for i in reversed(range(1, k)):
        now = DPPre[now][i]
        reversed_t.append(g.thre_list[now])
    
    t = list(reversed(reversed_t))

    assert(len(t) == k+1)
    return t






def MaxDivDP(g: prList, h: prList, N: int, k: int) -> Tuple[list[list[float]], list[list[int]]]:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        N (int): number of segments
        k (int): number of regions

    Returns:
        Tuple[list[list[float]], list[list[int]]]: DPKL, DPPre
    """

    assert(isinstance(g, prList))
    assert(isinstance(h, prList))
    assert(isinstance(N, int))
    assert(isinstance(k, int))
    N = g.N
    assert(h.N == N)

    DPKL, DPPre = calc_DPKL(g, h, k)
    return DPKL, DPPre

def ThresMaxDiv(DPPre: list[list[int]], j: int, k: int, thre_list: list[float]):
    """

    Args:
        DPPre (list[list[int]]): DPPre
        j (int): j-th to N-th segments are clustered as k-th region
        k (int): number of regions
    """

    assert(isinstance(DPPre, list))
    assert(isinstance(j, int))
    assert(isinstance(k, int))
    
    # tracing the transitions backward from DPPre[j-1][k-1]
    if DPPre[j-1][k-1] is None:
        return None

    reversed_t = [1.0]

    now = j-1
    reversed_t.append(thre_list[now])
    for i in reversed(range(1, k)):
        now = DPPre[now][i]
        if now is None:
            return None
        reversed_t.append(thre_list[now])
    
    t = list(reversed(reversed_t))

    assert(len(t) == k+1)
    return t

def fastMaxDivDP(g: prList, h: prList, N: int, k: int) -> Tuple[list[list[float]], list[list[int]]]:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        N (int): number of segments
        k (int): number of regions

    Returns:
        Tuple[list[list[float]], list[list[int]]]: DPKL, DPPre
    """

    N = g.N

    DPKL, DPPre = fast_calc_DPKL(g, h, k)
    return DPKL, DPPre
