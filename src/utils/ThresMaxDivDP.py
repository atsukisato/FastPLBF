from utils.prList import prList
from utils.calc_DPKL import calc_DPKL

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

    DPKL, DPPre = calc_DPKL(g, h, k)

    # DPPre[j-1][k-1]から逆にたどっていく
    reversed_t = [1.0]

    now = j-1
    reversed_t.append(g.segmenet_thre_list[now])
    for i in reversed(range(1, k)):
        now = DPPre[now][i]
        reversed_t.append(g.segmenet_thre_list[now])
    
    t = list(reversed(reversed_t))

    assert(len(t) == k+1)
    return t
