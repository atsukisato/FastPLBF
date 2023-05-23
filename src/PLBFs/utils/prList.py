import math
from utils.const import EPS
import bisect

class prList:

    def __init__(self, scores: list[float], thre_list: list[float]):
        """

        Args:
            scores (list[float]): a list of scores
            thre_list (list[float]): thresholds for divide scores into segment

        """

        assert(thre_list[0] == 0)
        assert(thre_list[-1] == 1)

        self.thre_list = thre_list
        self.N = len(thre_list) - 1

        cnt_list = [0 for _ in range(self.N + 1)]
        for score in scores:
            assert(0 <= score <= 1)

            segment_idx = bisect.bisect_left(thre_list, score)
            if segment_idx == 0:
                assert(score == 0)
                segment_idx = 1

            assert(1 <= segment_idx <= self.N)

            cnt_list[segment_idx] += 1
        
        total_cnt = len(scores)

        self.pr = [0.0 for i in range(self.N+1)]
        self.accPr = [0.0 for i in range(self.N+1)]
        for i in range(1, self.N + 1):
            self.pr[i] = cnt_list[i] / total_cnt
            self.accPr[i] = self.accPr[i - 1] + self.pr[i]
    
        assert(abs(self.accPr[self.N] - 1.0) < EPS), self.accPr[self.N]

    def get_th_idx(self, score: float) -> int:
        """
        0 --> 0
        1/N --> 1
        2/N --> 2
        ...
        N/N --> N

        Args:
            score (float): score

        Returns:
            int: idx
        """

        idx = math.floor(score * self.N + 0.5)
        assert(abs(idx - score * self.N) < 1e-9)

        return idx


    def acc(self, score: float) -> float:
        """

        Args:
            score (float): \in [0, 1]
        Returns:
            float: accumulated probability in [0, score]
        """

        idx = self.get_th_idx(score)

        return self.accPr[idx]

        
    def acc_range(self, score_l: float, score_r: float) -> float:
        """

        Args:
            score_l (float): \in [0, 1]
            score_r (float): \in [0, 1]

        Returns:
            float: accumulated probability in [score_l, score_r]
        """

        idx_l = self.get_th_idx(score_l)
        idx_r = self.get_th_idx(score_r)

        return self.accPr[idx_r] - self.accPr[idx_l]
    
    def acc_idx(self, idx: int) -> float:
        """

        Args:
            idx (int): idx \in {1 ... N}

        Returns:
            float: sum of self.pr[1...idx]
        """
        
        assert(1 <= idx <= self.N)

        return self.accPr[idx]

    def acc_range_idx(self, idx_l: int, idx_r: int) -> float:
        """

        Args:
            idx_l (int): idx \in {1 ... N}
            idx_l (int): idx \in {1 ... N}

        Returns:
            float: sum of self.pr[idx_l...idx_r]
        """

        assert(1 <= idx_l <= self.N)
        assert(1 <= idx_r <= self.N)
        
        return self.accPr[idx_r] - self.accPr[idx_l - 1]

