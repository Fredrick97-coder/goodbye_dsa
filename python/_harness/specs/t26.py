"""Specs for Rosetta module 26 -- Sequences."""

from ..spec import spec


def _ref_fibonacci(n):
    out, a, b = [], 0, 1
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out


def _ref_equilibrium(numbers):
    total = sum(numbers)
    left = 0
    out = []
    for i, value in enumerate(numbers):
        if left == total - left - value:
            out.append(i)
        left += value
    return out


def _ref_longest_increasing(numbers):
    """O(n^2) on purpose: the obvious reading, against which a clever one is checked."""
    if not numbers:
        return 0
    best = [1] * len(numbers)
    for i in range(len(numbers)):
        for j in range(i):
            if numbers[j] < numbers[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best)


def _ref_spiral(n):
    if n <= 0:
        return []
    grid = [[None] * n for _ in range(n)]
    row = col = 0
    dr, dc = 0, 1
    for value in range(n * n):
        grid[row][col] = value
        nr, nc = row + dr, col + dc
        if not (0 <= nr < n and 0 <= nc < n) or grid[nr][nc] is not None:
            dr, dc = dc, -dr          # turn clockwise
            nr, nc = row + dr, col + dc
        row, col = nr, nc
    return grid


def _ref_zigzag(n):
    if n <= 0:
        return []
    cells = sorted(((r, c) for r in range(n) for c in range(n)),
                   key=lambda rc: (rc[0] + rc[1],
                                   rc[1] if (rc[0] + rc[1]) % 2 == 0 else -rc[1]))
    grid = [[0] * n for _ in range(n)]
    for value, (r, c) in enumerate(cells):
        grid[r][c] = value
    return grid


SPECS = [
    spec(1, "fibonacci", ref=_ref_fibonacci, gen=lambda r: (r.randint(0, 40),),
         cases=[((0,), []), ((1,), [0]), ((2,), [0, 1]),
                ((8,), [0, 1, 1, 2, 3, 5, 8, 13])],
         note="starts 0, 1; n is a COUNT, not the index of the last value"),

    spec(2, "equilibrium_indices", ref=_ref_equilibrium,
         gen=lambda r: ([r.randint(-9, 9) for _ in range(r.randint(0, 12))],),
         cases=[(([-7, 1, 5, 2, -4, 3, 0],), [3, 6]),
                (([],), []),
                (([0],), [0]),
                (([2, 4, 6],), [])],
         note="the element at the index counts towards neither side"),

    spec(3, "longest_increasing", ref=_ref_longest_increasing,
         gen=lambda r: ([r.randint(0, 20) for _ in range(r.randint(0, 14))],),
         cases=[(([3, 2, 6, 4, 5, 1],), 3), (([],), 0), (([7],), 1),
                (([5, 5, 5],), 1), (([1, 2, 3, 4],), 4)],
         note="strictly increasing, so equal values do not extend it"),

    spec(4, "spiral_matrix", ref=_ref_spiral, gen=lambda r: (r.randint(0, 7),),
         cases=[((1,), [[0]]),
                ((3,), [[0, 1, 2], [7, 8, 3], [6, 5, 4]]),
                ((0,), [])],
         note="clockwise inward from the top-left, numbering from 0"),

    spec(5, "zigzag_matrix", ref=_ref_zigzag, gen=lambda r: (r.randint(0, 7),),
         cases=[((1,), [[0]]),
                ((3,), [[0, 1, 5], [2, 4, 6], [3, 7, 8]]),
                ((0,), [])],
         note="numbered along the anti-diagonals, alternating direction"),
]
