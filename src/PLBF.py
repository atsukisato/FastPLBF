import math
from utils.ThresMaxDivDP import ThresMaxDivDP
from utils.OptimalFPR import OptimalFPR
from utils.SpaceUsed import SpaceUsed
from utils.prList import prList

class PLBF:

    def __init__(self, g: list[float], h: list[float], F: float, N: int, k: int, n: int):
        """

        Args:
            g (list[float]): key density of each segmenet (0-index)
            h (list[float]): non-keye density of each segmenet (0-index)
            F (float): target overall fpr
            N (int): number of segments
            k (int): number of regions
            n (int); number of keys
        """

        assert(len(g) == N)
        assert(len(h) == N)

        self.g = prList(g)
        self.h = prList(g)
        self.F = F
        self.N = N
        self.k = k

        ### find t_best, f_best
        minSpaceUsed = -math.inf
        t_best = None
        f_best = None
        for j in range(k, N+1):
            t = ThresMaxDivDP(self.g, self.h, j, k)
            f = OptimalFPR(self.g, self.h, t, F, k)
            if minSpaceUsed < SpaceUsed(self.g, self.h, t, f, n):
                minSpaceUsed = SpaceUsed(self.g, self.h, t, f, n)
                t_best = t
                f_best = f

        self.t = t_best
        self.f = f_best

    def insert(self, key):
        pass

    def contains(self, x):
        pass


if __name__ == "__main__":
    g = [0.1, 0.2, 0.3, 0.4]
    h = [0.4, 0.3, 0.2, 0.1]
    F = 0.01
    N = 4
    k = 2
    n = 100

    plbf = PLBF(g, h, F, N, k, n)
    
    print("t:", plbf.t)
    print("f:", plbf.f)


