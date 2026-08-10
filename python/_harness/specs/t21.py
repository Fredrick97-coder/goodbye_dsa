"""Specs for Topic 21 -- Intervals & Matrix Patterns.

Interval semantics here are HALF-OPEN, matching the topic's theory file:
[1,2] and [2,3] do not overlap. Where a problem is ambiguous the spec says so.
"""

import itertools
from collections import deque

from ..spec import lists_to_tuples, spec

DIRS4 = ((-1, 0), (1, 0), (0, -1), (0, 1))

# ------------------------------------------------------------- references


def _ref_overlaps(a, b):
    """Half-open: touching endpoints do NOT overlap."""
    return a[0] < b[1] and b[0] < a[1]


def _ref_merge(intervals):
    """Independent: fuse any overlapping pair until stable. No sorting sweep."""
    items = [list(x) for x in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i], items[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    items[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    items.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(items)


def _ref_insert(intervals, new):
    return _ref_merge([tuple(x) for x in intervals] + [tuple(new)])


def _ref_can_attend(intervals):
    iv = sorted(intervals)
    return all(iv[i][1] <= iv[i + 1][0] for i in range(len(iv) - 1))


def _ref_min_rooms(intervals):
    if not intervals:
        return 0
    lo = min(s for s, _ in intervals)
    hi = max(e for _, e in intervals)
    return max((sum(1 for s, e in intervals if s <= t < e)
                for t in range(lo, hi + 1)), default=0)


def _ref_erase_overlap(intervals):
    """len - (max non-overlapping subset), by brute force."""
    n = len(intervals)
    for r in range(n, 0, -1):
        for combo in itertools.combinations(intervals, r):
            srt = sorted(combo)
            if all(srt[i][1] <= srt[i + 1][0] for i in range(len(srt) - 1)):
                return n - r
    return n


def _ref_intersection(a, b):
    """Pairwise intersect. a and b are each internally disjoint."""
    out = []
    for s1, e1 in a:
        for s2, e2 in b:
            lo, hi = max(s1, s2), min(e1, e2)
            if lo <= hi:
                out.append([lo, hi])
    return sorted(out)


def _ref_car_pooling(trips, capacity):
    if not trips:
        return True
    hi = max(e for _, _, e in trips)
    for t in range(hi + 1):
        if sum(p for p, s, e in trips if s <= t < e) > capacity:
            return False
    return True


def _ref_min_arrows(points):
    """Max non-overlapping-by-a-point cover == greedy on end coordinate."""
    if not points:
        return 0
    pts = sorted(points, key=lambda x: x[1])
    shots = 1
    last = pts[0][1]
    for s, e in pts[1:]:
        if s > last:
            shots += 1
            last = e
    return shots


# The four references below MUTATE their argument, because the exercise
# functions are declared as in-place (-> None). The harness reads args[0]
# after the call, so a reference that returned a new matrix instead would
# look unimplemented -- which is exactly what the self-consistency check
# reported before this was fixed.

def _ref_transpose(m):
    n = len(m)
    fresh = [[m[c][r] for c in range(n)] for r in range(n)]
    m[:] = fresh
    return None


def _ref_rotate(m):
    fresh = [list(row) for row in zip(*m[::-1])]
    m[:] = fresh
    return None


def _ref_spiral(matrix):
    """Simulated walk with a visited grid -- unlike the boundary method."""
    if not matrix or not matrix[0]:
        return []
    R, C = len(matrix), len(matrix[0])
    seen = [[False] * C for _ in range(R)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    out = []
    r = c = di = 0
    for _ in range(R * C):
        out.append(matrix[r][c])
        seen[r][c] = True
        nr, nc = r + dirs[di][0], c + dirs[di][1]
        if not (0 <= nr < R and 0 <= nc < C and not seen[nr][nc]):
            di = (di + 1) % 4
            nr, nc = r + dirs[di][0], c + dirs[di][1]
        r, c = nr, nc
    return out


def _ref_generate_spiral(n):
    m = [[0] * n for _ in range(n)]
    for i, (r, c) in enumerate(_spiral_coords(n, n), 1):
        m[r][c] = i
    return m


def _spiral_coords(R, C):
    seen = [[False] * C for _ in range(R)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r = c = di = 0
    for _ in range(R * C):
        yield (r, c)
        seen[r][c] = True
        nr, nc = r + dirs[di][0], c + dirs[di][1]
        if not (0 <= nr < R and 0 <= nc < C and not seen[nr][nc]):
            di = (di + 1) % 4
            nr, nc = r + dirs[di][0], c + dirs[di][1]
        r, c = nr, nc


def _ref_set_zeroes(matrix):
    R, C = len(matrix), len(matrix[0])
    zr = {r for r in range(R) for c in range(C) if matrix[r][c] == 0}
    zc = {c for r in range(R) for c in range(C) if matrix[r][c] == 0}
    fresh = [[0 if r in zr or c in zc else matrix[r][c] for c in range(C)]
             for r in range(R)]
    matrix[:] = fresh
    return None


def _ref_diagonal(matrix):
    if not matrix or not matrix[0]:
        return []
    R, C = len(matrix), len(matrix[0])
    groups = {}
    for r in range(R):
        for c in range(C):
            groups.setdefault(r + c, []).append(matrix[r][c])
    out = []
    for k in sorted(groups):
        out.extend(groups[k] if k % 2 else groups[k][::-1])
    return out


def _ref_num_islands(grid):
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    seen = set()
    count = 0
    for r0 in range(R):
        for c0 in range(C):
            if grid[r0][c0] != "1" or (r0, c0) in seen:
                continue
            count += 1
            stack = [(r0, c0)]
            seen.add((r0, c0))
            while stack:
                r, c = stack.pop()
                for dr, dc in DIRS4:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < R and 0 <= nc < C
                            and grid[nr][nc] == "1" and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
    return count


def _ref_flood_fill(image, sr, sc, colour):
    R, C = len(image), len(image[0])
    old = image[sr][sc]
    out = [row[:] for row in image]
    if old == colour:
        return out
    stack = [(sr, sc)]
    out[sr][sc] = colour
    while stack:
        r, c = stack.pop()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and out[nr][nc] == old:
                out[nr][nc] = colour
                stack.append((nr, nc))
    return out


def _ref_oranges(grid):
    g = [row[:] for row in grid]
    R, C = len(g), len(g[0])
    minutes = 0
    while True:
        to_rot = [(r + dr, c + dc) for r in range(R) for c in range(C)
                  if g[r][c] == 2
                  for dr, dc in DIRS4
                  if 0 <= r + dr < R and 0 <= c + dc < C
                  and g[r + dr][c + dc] == 1]
        if not to_rot:
            break
        for r, c in to_rot:
            g[r][c] = 2
        minutes += 1
    return -1 if any(v == 1 for row in g for v in row) else minutes


def _ref_update_matrix(mat):
    R, C = len(mat), len(mat[0])
    dist = [[-1] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if mat[r][c] == 0:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist


def _ref_search_matrix(matrix, target):
    return any(target in row for row in matrix)


def _ref_maximal_square(matrix):
    if not matrix or not matrix[0]:
        return 0
    R, C = len(matrix), len(matrix[0])
    best = 0
    for r in range(R):
        for c in range(C):
            k = 1
            while (r + k <= R and c + k <= C
                   and all(matrix[i][j] == "1"
                           for i in range(r, r + k) for j in range(c, c + k))):
                best = max(best, k)
                k += 1
    return best * best


def _ref_sparse_multiply(a, b):
    n, m, p = len(a), len(b), len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(m)) for j in range(p)]
            for i in range(n)]


def _ref_solve_surrounded(board):
    if not board or not board[0]:
        return [row[:] for row in board]
    R, C = len(board), len(board[0])
    safe = set()
    stack = [(r, c) for r in range(R) for c in range(C)
             if (r in (0, R - 1) or c in (0, C - 1)) and board[r][c] == "O"]
    safe.update(stack)
    while stack:
        r, c = stack.pop()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if (0 <= nr < R and 0 <= nc < C
                    and board[nr][nc] == "O" and (nr, nc) not in safe):
                safe.add((nr, nc))
                stack.append((nr, nc))
    fresh = [["O" if (r, c) in safe else "X" if board[r][c] == "O"
              else board[r][c] for c in range(C)] for r in range(R)]
    board[:] = fresh
    return None


# ------------------------------------------------------------- generators


def g_two_intervals(rng):
    a0 = rng.randint(0, 10)
    b0 = rng.randint(0, 10)
    return ((a0, a0 + rng.randint(0, 5)), (b0, b0 + rng.randint(0, 5)))


def g_intervals(rng, nmax=8):
    iv = []
    for _ in range(rng.randint(0, nmax)):
        a = rng.randint(0, 20)
        iv.append((a, a + rng.randint(0, 8)))
    return (iv,)


def g_small_intervals(rng):
    return g_intervals(rng, 6)


def g_disjoint_sorted(rng):
    iv = []
    a = rng.randint(0, 3)
    for _ in range(rng.randint(0, 5)):
        iv.append([a, a + rng.randint(0, 3)])
        a += rng.randint(4, 7)
    return iv


def g_insert(rng):
    base = _ref_merge([tuple(x) for x in g_disjoint_sorted(rng)])
    s = rng.randint(0, 30)
    return (base, [s, s + rng.randint(0, 10)])


def g_two_lists(rng):
    return (g_disjoint_sorted(rng), g_disjoint_sorted(rng))


def g_square(rng, lo=0, hi=99):
    n = rng.randint(1, 6)
    return ([[rng.randint(lo, hi) for _ in range(n)] for _ in range(n)],)


def g_matrix(rng, lo=0, hi=99):
    R, C = rng.randint(1, 6), rng.randint(1, 6)
    return ([[rng.randint(lo, hi) for _ in range(C)] for _ in range(R)],)


def g_matrix_with_zeros(rng):
    R, C = rng.randint(1, 5), rng.randint(1, 5)
    return ([[rng.choice([0, 1, 1, 2, 3]) for _ in range(C)]
             for _ in range(R)],)


def g_grid01(rng):
    R, C = rng.randint(1, 6), rng.randint(1, 6)
    return ([[rng.choice("01") for _ in range(C)] for _ in range(R)],)


def g_orchard(rng):
    R, C = rng.randint(1, 5), rng.randint(1, 5)
    return ([[rng.choice([0, 1, 1, 2]) for _ in range(C)] for _ in range(R)],)


def g_binary_matrix(rng):
    R, C = rng.randint(1, 6), rng.randint(1, 6)
    m = [[rng.choice([0, 1]) for _ in range(C)] for _ in range(R)]
    if all(v == 1 for row in m for v in row):
        m[0][0] = 0
    return (m,)


def g_sorted_matrix(rng):
    R, C = rng.randint(1, 5), rng.randint(1, 5)
    vals = sorted(rng.sample(range(0, 200), R * C))
    m = [vals[i * C:(i + 1) * C] for i in range(R)]
    return (m, rng.randint(0, 200))


def g_flood(rng):
    R, C = rng.randint(1, 5), rng.randint(1, 5)
    img = [[rng.randint(0, 2) for _ in range(C)] for _ in range(R)]
    return (img, rng.randrange(R), rng.randrange(C), rng.randint(0, 3))


def g_char_grid(rng, alphabet="XO", lo=1, hi=5):
    """
    Rectangular grid of characters.

    NOTE the shape must be decided BEFORE the comprehension. Writing
    `[[... for _ in range(rng.randint(1,5))] for _ in range(rng.randint(1,5))]`
    re-evaluates the inner randint per row and yields a RAGGED grid, which
    then throws IndexError inside otherwise-correct solutions.
    """
    R, C = rng.randint(lo, hi), rng.randint(lo, hi)
    return ([[rng.choice(alphabet) for _ in range(C)] for _ in range(R)],)


SPECS = [
    # --- intervals -------------------------------------------------------
    spec(1, "overlaps", ref=_ref_overlaps, gen=g_two_intervals, cases=[
        (((1, 3), (2, 4)), True),
        (((1, 2), (3, 4)), False),
        (((1, 2), (2, 3)), False),      # half-open
        (((1, 5), (2, 3)), True),
    ], note="half-open: [1,2) and [2,3) do NOT overlap"),
    spec(2, "merge", ref=_ref_merge, gen=g_intervals,
         norm=lists_to_tuples, cases=[
        (([(1, 3), (2, 6), (8, 10), (15, 18)],), [[1, 6], [8, 10], [15, 18]]),
        (([(1, 10), (2, 3)],), [[1, 10]]),      # nested -- needs max()
        (([],), []),
    ]),
    spec(3, "insert", ref=_ref_insert, gen=g_insert,
         norm=lists_to_tuples, cases=[
        (([[1, 3], [6, 9]], [2, 5]), [[1, 5], [6, 9]]),
        (([[1, 3], [6, 9]], [0, 0]), [[0, 0], [1, 3], [6, 9]]),
        (([], [4, 8]), [[4, 8]]),
    ]),
    spec(4, "can_attend_all", ref=_ref_can_attend, gen=g_intervals, cases=[
        (([(0, 30), (5, 10)],), False),
        (([(7, 10), (2, 4)],), True),
        (([],), True),
    ]),
    spec(5, "min_meeting_rooms", ref=_ref_min_rooms, gen=g_intervals, cases=[
        (([(0, 30), (5, 10), (15, 20)],), 2),
        (([],), 0),
    ]),
    spec(6, "erase_overlap_intervals", ref=_ref_erase_overlap,
         gen=g_small_intervals, cases=[
        (([(1, 2), (2, 3), (3, 4), (1, 3)],), 1),
        (([(1, 2)],), 0),
    ]),
    spec(7, "interval_intersection", ref=_ref_intersection, gen=g_two_lists,
         norm=lists_to_tuples, cases=[
        (([[0, 2], [5, 10], [13, 23], [24, 25]],
          [[1, 5], [8, 12], [15, 24], [25, 26]]),
         [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]),
    ]),
    spec(10, "car_pooling", ref=_ref_car_pooling,
         gen=lambda r: ([(r.randint(1, 4), (lambda s: s)(r.randint(0, 8)),
                          r.randint(9, 16)) for _ in range(r.randint(0, 5))],
                        r.randint(1, 10)),
         cases=[(([(2, 1, 5), (3, 3, 7)], 4), False),
                (([(2, 1, 5), (3, 3, 7)], 5), True)]),
    spec(11, "find_min_arrows", ref=_ref_min_arrows, gen=g_small_intervals,
         cases=[
        (([[10, 16], [2, 8], [1, 6], [7, 12]],), 2),
        (([[1, 2], [3, 4], [5, 6], [7, 8]],), 4),
        (([],), 0),
    ]),

    # --- matrix ----------------------------------------------------------
    spec(12, "transpose", inplace=True, ref=_ref_transpose, gen=g_square,
         cases=[(([[1, 2], [3, 4]],), [[1, 3], [2, 4]])]),
    spec(13, "rotate", inplace=True, ref=_ref_rotate, gen=g_square, cases=[
        (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],),
         [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
        (([[1]],), [[1]]),
    ]),
    spec(14, "spiral_order", ref=_ref_spiral, gen=g_matrix, cases=[
        (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 2, 3, 6, 9, 8, 7, 4, 5]),
        (([[1, 2, 3, 4]],), [1, 2, 3, 4]),          # 1xN guard
        (([[1], [2], [3]],), [1, 2, 3]),            # Nx1 guard
        (([],), []),
    ]),
    spec(15, "generate_spiral", ref=_ref_generate_spiral,
         gen=lambda r: (r.randint(1, 6),), norm=lists_to_tuples,
         cases=[((3,), [[1, 2, 3], [8, 9, 4], [7, 6, 5]])]),
    spec(16, "set_zeroes", inplace=True, ref=_ref_set_zeroes,
         gen=g_matrix_with_zeros, norm=lists_to_tuples, cases=[
        (([[1, 1, 1], [1, 0, 1], [1, 1, 1]],),
         [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
    ]),
    spec(17, "diagonal_order", ref=_ref_diagonal, gen=g_matrix, cases=[
        (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 2, 4, 7, 5, 3, 6, 8, 9]),
    ]),
    spec(18, "num_islands", ref=_ref_num_islands, gen=g_grid01, cases=[
        (([list("11000"), list("11000"), list("00100"), list("00011")],), 3),
        (([],), 0),
    ]),
    spec(19, "flood_fill", ref=_ref_flood_fill, gen=g_flood,
         norm=lists_to_tuples, cases=[
        (([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2),
         [[2, 2, 2], [2, 2, 0], [2, 0, 1]]),
        (([[0, 0], [0, 0]], 0, 0, 0), [[0, 0], [0, 0]]),   # same-colour guard
    ]),
    spec(20, "oranges_rotting", ref=_ref_oranges, gen=g_orchard, cases=[
        (([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4),
        (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1),
        (([[0, 2]],), 0),
    ]),
    spec(21, "update_matrix", ref=_ref_update_matrix, gen=g_binary_matrix,
         norm=lists_to_tuples, cases=[
        (([[0, 0, 0], [0, 1, 0], [1, 1, 1]],),
         [[0, 0, 0], [0, 1, 0], [1, 2, 1]]),
    ]),
    spec(22, "search_matrix", ref=_ref_search_matrix, gen=g_sorted_matrix,
         cases=[
        (([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16]], 5), True),
        (([[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16]], 13), False),
    ]),
    spec(24, "solve_surrounded", inplace=True, ref=_ref_solve_surrounded,
         gen=lambda r: g_char_grid(r, "XO"),
         norm=lists_to_tuples, cases=[
        (([list("XXXX"), list("XOOX"), list("XXOX"), list("XOXX")],),
         [list("XXXX"), list("XXXX"), list("XXXX"), list("XOXX")]),
    ]),
    spec(26, "maximal_square", ref=_ref_maximal_square,
         gen=lambda r: g_char_grid(r, "01", 1, 6),
         cases=[
        (([list("10100"), list("10111"), list("11111"), list("10010")],), 4),
        (([list("0")],), 0),
    ]),
    spec(27, "sparse_multiply", ref=_ref_sparse_multiply,
         gen=lambda r: (lambda n, m, p: (
             [[r.choice([0, 0, 0, 1, 2]) for _ in range(m)] for _ in range(n)],
             [[r.choice([0, 0, 0, 1, 3]) for _ in range(p)] for _ in range(m)]
         ))(r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)),
         norm=lists_to_tuples,
         cases=[(([[1, 0, 0], [-1, 0, 3]], [[7, 0, 0], [0, 0, 0], [0, 0, 1]]),
                 [[7, 0, 0], [-7, 0, 3]])]),
]
