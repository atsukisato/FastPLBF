from collections.abc import Callable


def smawk(f: Callable[[int, int], float], n: int, m: int) -> list[int]:
    """

    Args:
        f (Callable[[int, int], float]): returns B_{ij} (B is a totally monotone / Monge matrix) ({1 ... n} x {1 ... m} -> float).
        n (int): B is a n * m matrix
        m (int): B is a n * m matrix

    Returns:
        list[int]: a[i] = J(i) (i.e., a[i] is the smallest j that B_{i,j} equals the maximum value of the i-th row of B).
    """

    a = [None for _ in range(n + 1)]

    def reduce(rows: list[int], cols: list[int]) -> list[int]:
        # Discard columns that cannot be the (leftmost) row maximum, reducing |cols| to at most |rows|
        stack: list[int] = []
        for c in cols:
            while stack:
                r = rows[len(stack) - 1]
                if f(r, stack[-1]) < f(r, c):
                    stack.pop()
                else:
                    break
            if len(stack) < len(rows):
                stack.append(c)
        return stack

    def solve(rows: list[int], cols: list[int]) -> None:
        if not rows:
            return
        cols = reduce(rows, cols)
        # Recursively solve odd-indexed rows (0-indexed)
        solve(rows[1::2], cols)
        # Even-indexed rows: scan only between the answers of the neighboring rows
        pos = {c: idx for idx, c in enumerate(cols)}
        k = 0
        for i in range(0, len(rows), 2):
            r = rows[i]
            end = pos[a[rows[i + 1]]] if i + 1 < len(rows) else len(cols) - 1
            best = cols[k]
            best_val = f(r, best)
            for t in range(k + 1, end + 1):
                v = f(r, cols[t])
                if v > best_val:
                    best_val = v
                    best = cols[t]
            a[r] = best
            k = end

    solve(list(range(1, n + 1)), list(range(1, m + 1)))
    return a
