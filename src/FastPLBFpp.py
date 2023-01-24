from utils.ThresMaxDivDP import fastMaxDivDP, ThresMaxDiv
from utils.OptimalFPR import OptimalFPR
from utils.SpaceUsed import SpaceUsed
from utils.prList import prList
from utils.const import INF

class FastPLBFpp:

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
        assert(0 < F < 1)
        assert(isinstance(N, int))
        assert(isinstance(k, int))
        assert(isinstance(n, int))


        self.g = prList(g)
        self.h = prList(h)
        self.segmenet_thre_list = (self.g).segmenet_thre_list

        self.F = F
        self.N = N
        self.k = k

        ### find t_best, f_best
        minSpaceUsed = INF
        t_best = None
        f_best = None

        DPKL, DPPre = fastMaxDivDP(self.g, self.h, N, k)
        for j in range(k, N+1):
            t = ThresMaxDiv(DPPre, j, k, self.segmenet_thre_list)
            f = OptimalFPR(self.g, self.h, t, F, k)

            print("t:", t)
            print("f:", f)
            print("S:", SpaceUsed(self.g, self.h, t, f, n))

            if minSpaceUsed > SpaceUsed(self.g, self.h, t, f, n):
                minSpaceUsed = SpaceUsed(self.g, self.h, t, f, n)
                t_best = t
                f_best = f

        self.t = t_best
        self.f = f_best
        self.memory_backup_bf = minSpaceUsed

    def insert(self, key, score):
        pass

    def contains(self, x):
        pass


if __name__ == "__main__":
    print("Fast PLBF++ ------------------")


    
    g = [0.1, 0.1, 0.1, 0.2, 0.2, 0.3]
    h = [0.3, 0.2, 0.2, 0.15, 0.1, 0.05]
    F = 0.01
    N = 6
    k = 3
    n = 100

    fast_plbf = FastPLBFpp(g, h, F, N, k, n)

    print("t:", fast_plbf.t)
    print("f:", fast_plbf.f)
    print("S_:", fast_plbf.memory_backup_bf)

