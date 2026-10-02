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

    raise NotImplementedError("SMAWK is not implemented yet")
