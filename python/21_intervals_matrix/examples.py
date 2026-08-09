"""
Examples: Intervals & Matrix Patterns

Part 1: overlap detection, merging, inserting, sweep lines.
Part 2: spiral, rotate in place, islands, multi-source BFS, staircase search.

Every algorithm is cross-checked against a brute-force reference.
"""

import random
import time
from collections import deque
from typing import List, Tuple

print("=" * 70)
print("INTERVALS & MATRIX PATTERNS")
print("=" * 70)

# ============================================================
#                      PART 1: INTERVALS
# ============================================================
print("\n" + "=" * 70)
print("PART 1: INTERVALS")
print("=" * 70)

# ==================== (1) Overlap Detection ====================
print("\n[1] Overlap Detection -- Reason About the NEGATION")
print("-" * 70)

def overlaps_closed(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    """Closed intervals: touching endpoints DO overlap."""
    return a[0] <= b[1] and b[0] <= a[1]

def overlaps_half_open(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    """Half-open [start, end): touching endpoints do NOT overlap."""
    return a[0] < b[1] and b[0] < a[1]

print("  The condition is easier to derive by negating the NON-overlap case:")
print("    no overlap  <=>  a2 < b1  OR  b2 < a1")
print("    overlap     <=>  a1 <= b2 AND b1 <= a2\n")

pairs = [((1, 3), (2, 4)), ((1, 5), (2, 3)), ((1, 2), (3, 4)),
         ((1, 2), (2, 3)), ((5, 6), (1, 2))]
print(f"  {'a':<10} {'b':<10} {'closed':>8} {'half-open':>11}  situation")
print("  " + "-" * 56)
for a, b in pairs:
    c = overlaps_closed(a, b)
    h = overlaps_half_open(a, b)
    if a[1] == b[0] or b[1] == a[0]:
        note = "TOUCHING -- semantics decide"
    elif c:
        note = "genuine overlap"
    else:
        note = "disjoint"
    print(f"  {str(a):<10} {str(b):<10} {str(c):>8} {str(h):>11}  {note}")

print("\n  -> Always ASK (or state) whether endpoints count as overlapping.")
print("     Half-open is usually right for time: a meeting ending at 2:00")
print("     does not conflict with one starting at 2:00.")

# ==================== (2) Merge Intervals ====================
print("\n[2] Merge Intervals -- Sort by START")
print("-" * 70)

def merge(intervals: List[Tuple[int, int]]) -> List[List[int]]:
    """O(n log n). The max() is what makes nested intervals work."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])      # by START
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)      # EXTEND
        else:
            merged.append([start, end])
    return merged


def merge_buggy(intervals: List[Tuple[int, int]]) -> List[List[int]]:
    """The classic bug: assignment instead of max()."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda x: x[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = end                          # BUG
        else:
            merged.append([start, end])
    return merged


def merge_brute(intervals: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Reference: repeatedly fuse ANY two overlapping intervals until stable.
    O(n^3) and deliberately unlike the sweep above -- no sorting, no
    single pass. It shares only the `overlaps_closed` predicate.

    NOTE: an earlier version of this reference expanded each interval into
    a set of integer points and regrouped consecutive runs. That was WRONG:
    it fused [1,2] with [3,4] because the integers 2 and 3 are adjacent,
    even though the intervals do not overlap. It reported 710 false
    "failures" against a correct merge(). Adjacency is not overlap.
    """
    items = [list(x) for x in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i], items[j]
                if a[0] <= b[1] and b[0] <= a[1]:        # genuine overlap
                    items[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    items.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(items)


data = [(1, 3), (2, 6), (8, 10), (15, 18)]
print(f"  Input : {data}")
print(f"  Sorted: {sorted(data, key=lambda x: x[0])}")
print(f"\n  Trace:")
ordered = sorted(data, key=lambda x: x[0])
acc = [list(ordered[0])]
print(f"    {str(tuple(ordered[0])):<10} -> start   {acc}")
for s, e in ordered[1:]:
    if s <= acc[-1][1]:
        acc[-1][1] = max(acc[-1][1], e)
        print(f"    {str((s, e)):<10} -> {s} <= prev end, EXTEND  {acc}")
    else:
        acc.append([s, e])
        print(f"    {str((s, e)):<10} -> disjoint, APPEND      {acc}")

print(f"\n  merge(...)   = {merge(data)}")

nested = [(1, 10), (2, 3), (4, 5)]
print(f"\n  The nested-interval bug:")
print(f"    input        = {nested}")
print(f"    correct(max) = {merge(nested)}")
print(f"    buggy(assign)= {merge_buggy(nested)}   <- WRONG, lost the 10")

print("\n  Verifying merge() against a brute-force point-set reference:")
random.seed(1)
fails = 0
for _ in range(3000):
    iv = []
    for _ in range(random.randint(0, 8)):
        a = random.randint(0, 20)
        iv.append((a, a + random.randint(0, 6)))
    if merge(iv) != merge_brute(iv):
        fails += 1
print(f"    3,000 random inputs, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

buggy_fails = sum(
    1 for _ in range(500)
    if (lambda iv: merge_buggy(iv) != merge_brute(iv))(
        [(a, a + random.randint(0, 6))
         for a in (random.randint(0, 20) for _ in range(random.randint(0, 8)))])
)
print(f"    The buggy version fails {buggy_fails} of 500 -- it only breaks")
print(f"    when one interval NESTS inside another, so it passes casual tests.")

# ==================== (3) Insert Interval ====================
print("\n[3] Insert Interval -- Three Phases, O(n), No Sort")
print("-" * 70)

def insert(intervals: List[List[int]], new: List[int]) -> List[List[int]]:
    """Input is already sorted and merged. O(n)."""
    result: List[List[int]] = []
    i, n = 0, len(intervals)

    while i < n and intervals[i][1] < new[0]:        # 1. strictly before
        result.append(list(intervals[i]))
        i += 1

    start, end = new                                 # 2. absorb overlaps
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])

    result.extend(list(x) for x in intervals[i:])    # 3. strictly after
    return result


base = [[1, 3], [6, 9]]
print(f"  base = {base}")
for new in ([2, 5], [4, 5], [0, 0], [10, 12], [0, 20]):
    print(f"    insert(base, {str(new):<8}) = {insert(base, new)}")

print("\n  Verifying insert() against merge(base + [new]):")
fails = 0
for _ in range(3000):
    iv = []
    a = random.randint(0, 5)
    for _ in range(random.randint(0, 6)):
        iv.append((a, a + random.randint(0, 3)))
        a += random.randint(4, 8)                    # keep them disjoint
    iv_merged = merge(iv)
    s = random.randint(0, 40)
    new = [s, s + random.randint(0, 10)]
    if insert(iv_merged, new) != merge([tuple(x) for x in iv_merged] + [tuple(new)]):
        fails += 1
print(f"    3,000 random inputs, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

# ==================== (4) Sweep Line ====================
print("\n[4] The Sweep Line -- Events, Sort, Running Counter")
print("-" * 70)

def max_concurrent(intervals: List[Tuple[int, int]]) -> int:
    """Peak simultaneous intervals. Half-open: ends fire before starts."""
    events: List[Tuple[int, int]] = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()                        # (t,-1) sorts before (t,+1)
    cur = peak = 0
    for _, delta in events:
        cur += delta
        peak = max(peak, cur)
    return peak


def max_concurrent_closed(intervals: List[Tuple[int, int]]) -> int:
    """Closed intervals: touching endpoints DO overlap, so starts fire first."""
    events: List[Tuple[int, int, int]] = []
    for s, e in intervals:
        events.append((s, 0, 1))        # 0 sorts before 1 -> starts first
        events.append((e, 1, -1))
    events.sort()
    cur = peak = 0
    for _, _, delta in events:
        cur += delta
        peak = max(peak, cur)
    return peak


def max_concurrent_brute(intervals: List[Tuple[int, int]]) -> int:
    """Reference: check every integer time point, half-open."""
    if not intervals:
        return 0
    lo = min(s for s, _ in intervals)
    hi = max(e for _, e in intervals)
    best = 0
    for t in range(lo, hi + 1):
        best = max(best, sum(1 for s, e in intervals if s <= t < e))
    return best


meetings = [(0, 30), (5, 10), (15, 20), (25, 35), (30, 40)]
print(f"  Meetings: {meetings}")
print(f"\n  Event list (sorted):")
evs = sorted([(s, 1) for s, _ in meetings] + [(e, -1) for _, e in meetings])
cur = peak = 0
for t, d in evs:
    cur += d
    peak = max(peak, cur)
    kind = "start" if d == 1 else "end  "
    bar = "#" * cur
    print(f"    t={t:>3}  {kind}  active={cur}  {bar}")
print(f"\n  Peak concurrency (rooms needed): {peak}")

print(f"\n  Half-open vs closed semantics on touching intervals:")
touch = [(1, 2), (2, 3), (3, 4)]
print(f"    intervals    : {touch}")
print(f"    half-open    : {max_concurrent(touch)}  (a chain, 1 room)")
print(f"    closed       : {max_concurrent_closed(touch)}  (endpoints collide)")
print(f"    -> The ONLY difference is the tie order in the sort. Flip it and")
print(f"       you are off by one, but only on inputs that have ties.")

print("\n  Verifying sweep line against a brute-force time scan:")
fails = 0
for _ in range(2000):
    iv = []
    for _ in range(random.randint(0, 10)):
        a = random.randint(0, 15)
        iv.append((a, a + random.randint(1, 8)))
    if max_concurrent(iv) != max_concurrent_brute(iv):
        fails += 1
print(f"    2,000 random inputs, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

# What sweep line gives you that a heap does not
print("\n  What the sweep line answers that a heap cannot:")

def sweep_report(intervals: List[Tuple[int, int]]) -> dict:
    events: List[Tuple[int, int]] = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()

    cur = peak = 0
    peak_time = None
    covered = 0
    prev_t = None
    at_least_2 = 0

    for t, d in events:
        if prev_t is not None and cur > 0:
            covered += t - prev_t
            if cur >= 2:
                at_least_2 += t - prev_t
        cur += d
        if cur > peak:
            peak, peak_time = cur, t
        prev_t = t

    return {"peak": peak, "peak_at": peak_time,
            "total_covered": covered, "covered_by_2plus": at_least_2}


rep = sweep_report(meetings)
print(f"    peak concurrency      : {rep['peak']}")
print(f"    first reached at t    : {rep['peak_at']}")
print(f"    total time covered    : {rep['total_covered']}")
print(f"    time covered by >= 2  : {rep['covered_by_2plus']}")

# verify covered length by brute force
def covered_brute(intervals):
    pts = set()
    for s, e in intervals:
        pts.update(range(s, e))
    return len(pts)
print(f"    covered (brute force) : {covered_brute(meetings)}   "
      f"match: {rep['total_covered'] == covered_brute(meetings)}")
print("    -> Topic 19's heap answers only 'how many rooms'. The sweep line")
print("       answers when, how long, and how deep -- from the same events.")

# ==================== (5) The Sort-Key Fork ====================
print("\n[5] The Sort-Key Fork: START vs END")
print("-" * 70)

def max_non_overlapping(intervals: List[Tuple[int, int]]) -> int:
    """Maximum COUNT of non-overlapping intervals. Sort by END (greedy)."""
    if not intervals:
        return 0
    ordered = sorted(intervals, key=lambda x: x[1])      # by END
    count, last_end = 1, ordered[0][1]
    for s, e in ordered[1:]:
        if s >= last_end:
            count += 1
            last_end = e
    return count


def max_non_overlapping_by_start(intervals: List[Tuple[int, int]]) -> int:
    """The SAME greedy but sorted by START -- demonstrably wrong."""
    if not intervals:
        return 0
    ordered = sorted(intervals, key=lambda x: x[0])
    count, last_end = 1, ordered[0][1]
    for s, e in ordered[1:]:
        if s >= last_end:
            count += 1
            last_end = e
    return count


def max_non_overlapping_brute(intervals: List[Tuple[int, int]]) -> int:
    """Reference: try every subset, largest first (small inputs only)."""
    import itertools
    for r in range(len(intervals), 0, -1):
        for combo in itertools.combinations(intervals, r):
            srt = sorted(combo, key=lambda x: x[0])
            if all(srt[i][1] <= srt[i + 1][0] for i in range(len(srt) - 1)):
                return r
    return 0


counter = [(1, 100), (2, 3), (4, 5), (6, 7)]
print(f"  intervals = {counter}")
print(f"    sort by END   -> {max_non_overlapping(counter)}  (correct)")
print(f"    sort by START -> {max_non_overlapping_by_start(counter)}  (WRONG)")
print(f"    brute force   -> {max_non_overlapping_brute(counter)}")
print("    -> Sorting by start picks the greedy [1,100] first and blocks")
print("       everything else. Sorting by end frees the most room.")

print("\n  Verifying the end-sort greedy against brute force:")
fails_end = fails_start = 0
for _ in range(1500):
    iv = []
    for _ in range(random.randint(1, 7)):
        a = random.randint(0, 12)
        iv.append((a, a + random.randint(1, 6)))
    truth = max_non_overlapping_brute(iv)
    if max_non_overlapping(iv) != truth:
        fails_end += 1
    if max_non_overlapping_by_start(iv) != truth:
        fails_start += 1
print(f"    sort-by-END   mismatches: {fails_end:>4}  "
      f"({'PASS' if not fails_end else 'FAIL'})")
print(f"    sort-by-START mismatches: {fails_start:>4}  "
      f"(fails on {fails_start / 1500 * 100:.0f}% of random inputs)")

# ==================== (6) Interval Intersection ====================
print("\n[6] Intersecting Two Sorted Lists -- Two Pointers, O(n + m)")
print("-" * 70)

def interval_intersection(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """max of starts, min of ends, advance whichever ends first."""
    out: List[List[int]] = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return out


A = [[0, 2], [5, 10], [13, 23], [24, 25]]
B = [[1, 5], [8, 12], [15, 24], [25, 26]]
print(f"  A = {A}")
print(f"  B = {B}")
print(f"  intersection = {interval_intersection(A, B)}")

print("\n  Verifying against a brute-force point-set intersection:")
def intersect_brute(a, b):
    """
    Reference: intersect EVERY pair (a_i, b_j) directly. Because a and b
    are each internally disjoint, the resulting pieces are already
    disjoint and need no merging.

    Same lesson as merge_brute: the earlier point-set version fused
    adjacent-but-disjoint results like [5,5] and [6,6] into [5,6].
    """
    out = []
    for s1, e1 in a:
        for s2, e2 in b:
            lo, hi = max(s1, s2), min(e1, e2)
            if lo <= hi:
                out.append([lo, hi])
    return sorted(out)

fails = 0
for _ in range(2000):
    def gen():
        iv = []
        a = random.randint(0, 3)
        for _ in range(random.randint(0, 5)):
            iv.append([a, a + random.randint(0, 3)])
            a += random.randint(4, 7)
        return iv
    x, y = gen(), gen()
    if interval_intersection(x, y) != intersect_brute(x, y):
        fails += 1
print(f"    2,000 random pairs, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

# ============================================================
#                    PART 2: MATRIX PATTERNS
# ============================================================
print("\n\n" + "=" * 70)
print("PART 2: MATRIX PATTERNS")
print("=" * 70)

DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS_8 = DIRS_4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]

# ==================== (7) The [[0]*c]*r Trap ====================
print("\n[7] The Grid Setup -- and the Trap Everyone Hits Once")
print("-" * 70)

bad = [[0] * 3] * 3
good = [[0] * 3 for _ in range(3)]
bad[0][0] = 9
good[0][0] = 9
print(f"  bad  = [[0]*3]*3        -> after bad[0][0]=9 : {bad}")
print(f"  good = [[0]*3 for _ ..] -> after good[0][0]=9: {good}")
print(f"  bad[0] is bad[1]: {bad[0] is bad[1]}   <- the SAME list object")
print("  -> [[0]*c]*r makes r references to ONE row. Always use a")
print("     comprehension. This bites everyone exactly once.")

print("\n  The setup worth writing at the top of every grid problem:")
print("""    rows, cols = len(grid), len(grid[0]) if grid else 0
    DIRS_4 = [(-1,0),(1,0),(0,-1),(0,1)]
    def in_bounds(r, c): return 0 <= r < rows and 0 <= c < cols""")

# ==================== (8) Spiral Traversal ====================
print("\n[8] Spiral Traversal -- The Two Guards Are Not Optional")
print("-" * 70)

def spiral_order(matrix: List[List[int]]) -> List[int]:
    if not matrix or not matrix[0]:
        return []
    out: List[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:                     # GUARD: single row remaining?
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:                     # GUARD: single column remaining?
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1
    return out


def spiral_order_no_guards(matrix: List[List[int]]) -> List[int]:
    """Same code, guards removed -- double-traverses the last row/column."""
    if not matrix or not matrix[0]:
        return []
    out: List[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            out.append(matrix[r][right])
        right -= 1
        for c in range(right, left - 1, -1):
            out.append(matrix[bottom][c])
        bottom -= 1
        for r in range(bottom, top - 1, -1):
            out.append(matrix[r][left])
        left += 1
    return out


m3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("  3x3 matrix:")
for row in m3:
    print(f"    {row}")
print(f"  spiral: {spiral_order(m3)}")

print("\n  Where the guards matter -- degenerate shapes:")
shapes = {
    "1x1": [[1]],
    "1x4": [[1, 2, 3, 4]],
    "4x1": [[1], [2], [3], [4]],
    "3x2": [[1, 2], [3, 4], [5, 6]],
    "2x3": [[1, 2, 3], [4, 5, 6]],
}
print(f"  {'shape':<6} {'with guards':<26} {'without guards':<26} {'ok':>4}")
print("  " + "-" * 66)
for name, m in shapes.items():
    a = spiral_order([r[:] for r in m])
    b = spiral_order_no_guards([r[:] for r in m])
    total = sum(len(r) for r in m)
    ok = "yes" if len(a) == total and sorted(a) == sorted(
        v for r in m for v in r) else "NO"
    flag = "" if a == b else "  <- differ"
    print(f"  {name:<6} {str(a):<26} {str(b):<26} {ok:>4}{flag}")

print("\n  -> Without the guards, 1x4 and 4x1 emit DUPLICATE elements.")
print("     Those are exactly the hidden test cases.")

print("\n  Verifying spiral against a simulated direction-walk reference:")

def spiral_brute(matrix):
    """Reference: walk with a visited set, turning when blocked."""
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

fails = 0
for _ in range(500):
    R, C = random.randint(1, 6), random.randint(1, 6)
    m = [[random.randint(0, 99) for _ in range(C)] for _ in range(R)]
    if spiral_order(m) != spiral_brute(m):
        fails += 1
print(f"    500 random shapes, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

# ==================== (9) Rotate In Place ====================
print("\n[9] Rotate 90 Degrees In Place -- Transpose + Reverse Rows")
print("-" * 70)

def rotate(matrix: List[List[int]]) -> None:
    """Clockwise, O(1) extra space."""
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):                 # c > r ONLY
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()


def rotate_buggy(matrix: List[List[int]]) -> None:
    """Full-row transpose: swaps every pair twice, undoing itself."""
    n = len(matrix)
    for r in range(n):
        for c in range(n):                        # BUG: should be r+1
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()


def rotate_reference(matrix: List[List[int]]) -> List[List[int]]:
    """Reference: build a new matrix. new[c][n-1-r] = old[r][c]"""
    n = len(matrix)
    return [[matrix[n - 1 - c][r] for c in range(n)] for r in range(n)]


m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("  original:")
for row in m:
    print(f"    {row}")

step = [r[:] for r in m]
n = len(step)
for r in range(n):
    for c in range(r + 1, n):
        step[r][c], step[c][r] = step[c][r], step[r][c]
print("  after transpose (reflect across the main diagonal):")
for row in step:
    print(f"    {row}")

for row in step:
    row.reverse()
print("  after reversing each row  =  90 degrees clockwise:")
for row in step:
    print(f"    {row}")

buggy = [r[:] for r in m]
rotate_buggy(buggy)
print(f"\n  The c-range bug (range(n) instead of range(r+1, n)):")
print(f"    result: {buggy}")
print(f"    -> Transposing twice returns the original, so this is just")
print(f"       'reverse each row'. Correct-looking code, wrong answer.")

print("\n  Verifying rotate() against a fresh-matrix reference:")
fails = 0
for _ in range(2000):
    k = random.randint(1, 7)
    m = [[random.randint(0, 99) for _ in range(k)] for _ in range(k)]
    want = rotate_reference(m)
    got = [r[:] for r in m]
    rotate(got)
    if got != want:
        fails += 1
print(f"    2,000 random square matrices, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

print("\n  Four rotations return the original:")
m = [[random.randint(0, 9) for _ in range(4)] for _ in range(4)]
orig = [r[:] for r in m]
for _ in range(4):
    rotate(m)
print(f"    identity after 4 rotations: {m == orig}")

# ==================== (10) Islands ====================
print("\n[10] Islands -- DFS/BFS on an Implicit Graph")
print("-" * 70)

def num_islands_dfs(grid: List[List[str]]) -> int:
    """Recursive DFS, mutating the grid to mark visited. O(R*C)"""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    count = 0

    def sink(r, c):
        if not (0 <= r < R and 0 <= c < C) or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        for dr, dc in DIRS_4:
            sink(r + dr, c + dc)

    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count


def num_islands_iterative(grid: List[List[str]]) -> int:
    """Explicit stack -- no recursion limit. Use this on large grids."""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    count = 0
    for r0 in range(R):
        for c0 in range(C):
            if grid[r0][c0] != "1":
                continue
            count += 1
            stack = [(r0, c0)]
            grid[r0][c0] = "0"
            while stack:
                r, c = stack.pop()
                for dr, dc in DIRS_4:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"
                        stack.append((nr, nc))
    return count


def num_islands_union_find(grid: List[List[str]]) -> int:
    """Union-Find from Topic 14 -- a third correct approach."""
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            return True
        return False

    land = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1":
                parent[(r, c)] = (r, c)
                land += 1
    comps = land
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1":
                for dr, dc in ((1, 0), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "1":
                        if union((r, c), (nr, nc)):
                            comps -= 1
    return comps


island_map = [
    list("11000"),
    list("11000"),
    list("00100"),
    list("00011"),
]
print("  Grid:")
for row in island_map:
    print(f"    {''.join(row)}")

a = num_islands_dfs([r[:] for r in island_map])
b = num_islands_iterative([r[:] for r in island_map])
c = num_islands_union_find([r[:] for r in island_map])
print(f"\n  DFS        : {a}")
print(f"  Iterative  : {b}")
print(f"  Union-Find : {c}")
print(f"  All agree  : {a == b == c}")

print("\n  Cross-verifying three implementations on random grids:")
fails = 0
for _ in range(1500):
    R, C = random.randint(1, 7), random.randint(1, 7)
    g = [[random.choice("011") for _ in range(C)] for _ in range(R)]
    g = [[("1" if ch == "1" else "0") for ch in row] for row in g]
    x = num_islands_dfs([r[:] for r in g])
    y = num_islands_iterative([r[:] for r in g])
    z = num_islands_union_find([r[:] for r in g])
    if not (x == y == z):
        fails += 1
print(f"    1,500 random grids, disagreements: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

# The recursion depth problem
print("\n  The recursion-depth problem on large grids:")
import sys
BIG = 600
solid = [["1"] * BIG for _ in range(BIG)]
print(f"    A {BIG}x{BIG} all-land grid needs up to {BIG*BIG:,} recursion frames.")
print(f"    Python's limit is {sys.getrecursionlimit():,}.")
try:
    num_islands_dfs([r[:] for r in solid])
    print("    Recursive DFS : completed (grid happened to stay shallow)")
except RecursionError:
    print("    Recursive DFS : RecursionError  <- crashes")
start = time.perf_counter()
res = num_islands_iterative([r[:] for r in solid])
it_ms = (time.perf_counter() - start) * 1000
print(f"    Iterative DFS : {res} island, {it_ms:.0f}ms, no depth limit")
print("    -> Mention this before the interviewer does. Iterative is the")
print("       production answer for large grids.")

# ==================== (11) Multi-Source BFS ====================
print("\n[11] Multi-Source BFS -- Seed EVERY Source First")
print("-" * 70)

def oranges_rotting(grid: List[List[int]]) -> int:
    """Minutes until no fresh orange remains, or -1. O(R*C)"""
    R, C = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                queue.append((r, c))          # ALL sources at once
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):           # snapshot: one full LEVEL
            r, c = queue.popleft()
            for dr, dc in DIRS_4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1


def oranges_rotting_brute(grid: List[List[int]]) -> int:
    """Reference: simulate minute by minute over the whole grid."""
    g = [r[:] for r in grid]
    R, C = len(g), len(g[0])
    minutes = 0
    while True:
        to_rot = []
        for r in range(R):
            for c in range(C):
                if g[r][c] == 2:
                    for dr, dc in DIRS_4:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < R and 0 <= nc < C and g[nr][nc] == 1:
                            to_rot.append((nr, nc))
        if not to_rot:
            break
        for r, c in to_rot:
            g[r][c] = 2
        minutes += 1
    return -1 if any(v == 1 for row in g for v in row) else minutes


orchard = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
print("  Grid (2=rotten, 1=fresh, 0=empty):")
for row in orchard:
    print(f"    {row}")

work = [r[:] for r in orchard]
R, C = len(work), len(work[0])
q = deque((r, c) for r in range(R) for c in range(C) if work[r][c] == 2)
fresh = sum(1 for r in range(R) for c in range(C) if work[r][c] == 1)
minute = 0
print(f"\n  Minute {minute}: {fresh} fresh")
while q and fresh:
    for _ in range(len(q)):
        r, c = q.popleft()
        for dr, dc in DIRS_4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and work[nr][nc] == 1:
                work[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc))
    minute += 1
    print(f"  Minute {minute}: {fresh} fresh   {work}")

print(f"\n  Answer: {oranges_rotting([r[:] for r in orchard])} minutes")

print("\n  Verifying multi-source BFS against a minute-by-minute simulation:")
fails = 0
for _ in range(2000):
    R, C = random.randint(1, 6), random.randint(1, 6)
    g = [[random.choice([0, 1, 1, 2]) for _ in range(C)] for _ in range(R)]
    if oranges_rotting([r[:] for r in g]) != oranges_rotting_brute(g):
        fails += 1
print(f"    2,000 random orchards, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")

print("\n  Why seeding ALL sources matters:")
two_src = [[2, 1, 1, 1, 2]]
print(f"    {two_src[0]}  ->  {oranges_rotting([r[:] for r in two_src])} minutes")
print(f"    Rot spreads inward from BOTH ends simultaneously.")
one_src = [[2, 1, 1, 1, 0]]
print(f"    {one_src[0]}  ->  {oranges_rotting([r[:] for r in one_src])} minutes")
print(f"    One source has to travel the whole way.")
print("    -> Running BFS from each source separately and taking the min")
print("       would be O(sources * R * C). Seeding them all is O(R * C).")

# ==================== (12) Staircase Search ====================
print("\n[12] Staircase Search -- O(R + C) from the Top-Right")
print("-" * 70)

def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """Rows and columns both sorted ascending. Start top-RIGHT."""
    if not matrix or not matrix[0]:
        return False
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        if matrix[r][c] == target:
            return True
        if matrix[r][c] > target:
            c -= 1                       # too big -> eliminate this column
        else:
            r += 1                       # too small -> eliminate this row
    return False


sorted_m = [
    [1, 4, 7, 11, 15],
    [2, 5, 8, 12, 19],
    [3, 6, 9, 16, 22],
    [10, 13, 14, 17, 24],
    [18, 21, 23, 26, 30],
]
print("  Matrix (rows and columns both sorted):")
for row in sorted_m:
    print(f"    {row}")

print(f"\n  Search path for target 14 (starting top-right at 15):")
r, c = 0, len(sorted_m[0]) - 1
steps = 0
while r < len(sorted_m) and c >= 0:
    v = sorted_m[r][c]
    steps += 1
    if v == 14:
        print(f"    ({r},{c}) = {v}  FOUND in {steps} steps")
        break
    if v > 14:
        print(f"    ({r},{c}) = {v:>2}  > 14, drop column {c}")
        c -= 1
    else:
        print(f"    ({r},{c}) = {v:>2}  < 14, drop row {r}")
        r += 1

print(f"\n  {'target':>7} {'found':>7}  {'expected':>9}")
print("  " + "-" * 28)
all_present = {v for row in sorted_m for v in row}
for t in [5, 14, 20, 30, 1, 31]:
    got = search_matrix(sorted_m, t)
    print(f"  {t:>7} {str(got):>7}  {str(t in all_present):>9}")

print("\n  Verifying against a full scan, and why the corner matters:")
fails = 0
for _ in range(1500):
    R, C = random.randint(1, 6), random.randint(1, 6)
    # Build a matrix sorted along both axes
    vals = sorted(random.sample(range(0, 200), R * C))
    m = [vals[i * C:(i + 1) * C] for i in range(R)]
    # column sort is implied by the row-major fill of a sorted list
    t = random.randint(0, 200)
    if search_matrix(m, t) != any(t in row for row in m):
        fails += 1
print(f"    1,500 random sorted matrices, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")
print("\n  Why top-right (or bottom-left) and never top-left:")
print("    top-right : left DEcreases, down INcreases -> a real decision")
print("    top-left  : right increases, down increases -> both the same")
print("                direction, so a mismatch tells you nothing")
print(f"    Steps taken: at most R + C = {len(sorted_m) + len(sorted_m[0])}, "
      f"not R * C = {len(sorted_m) * len(sorted_m[0])}")

# ==================== (13) Set Matrix Zeroes ====================
print("\n[13] Set Matrix Zeroes in O(1) Space")
print("-" * 70)

def set_zeroes(matrix: List[List[int]]) -> None:
    """Use the first row and column as marker storage."""
    R, C = len(matrix), len(matrix[0])
    first_row = any(matrix[0][c] == 0 for c in range(C))
    first_col = any(matrix[r][0] == 0 for r in range(R))

    for r in range(1, R):
        for c in range(1, C):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    for r in range(1, R):                    # interior FIRST
        for c in range(1, C):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    if first_row:                            # markers LAST
        for c in range(C):
            matrix[0][c] = 0
    if first_col:
        for r in range(R):
            matrix[r][0] = 0


def set_zeroes_reference(matrix: List[List[int]]) -> List[List[int]]:
    """Reference using O(R + C) extra space."""
    R, C = len(matrix), len(matrix[0])
    zr = {r for r in range(R) for c in range(C) if matrix[r][c] == 0}
    zc = {c for r in range(R) for c in range(C) if matrix[r][c] == 0}
    return [[0 if r in zr or c in zc else matrix[r][c] for c in range(C)]
            for r in range(R)]


mz = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
print("  Before:")
for row in mz:
    print(f"    {row}")
work = [r[:] for r in mz]
set_zeroes(work)
print("  After:")
for row in work:
    print(f"    {row}")

print("\n  Verifying the O(1)-space version against an O(R+C)-space reference:")
fails = 0
for _ in range(2000):
    R, C = random.randint(1, 6), random.randint(1, 6)
    m = [[random.choice([0, 1, 1, 1, 2, 3]) for _ in range(C)]
         for _ in range(R)]
    want = set_zeroes_reference(m)
    got = [r[:] for r in m]
    set_zeroes(got)
    if got != want:
        fails += 1
print(f"    2,000 random matrices, mismatches: {fails}  "
      f"({'PASS' if not fails else 'FAIL'})")
print("\n  -> Order matters: apply the interior BEFORE overwriting the first")
print("     row/column, because those cells are still holding your markers.")

# ==================== (14) Summary Table ====================
print("\n[14] Pattern Summary")
print("-" * 70)

print("  INTERVALS")
print(f"  {'Problem':<32} {'Sort by':<12} {'Time':<14} {'Space'}")
print("  " + "-" * 70)
for prob, key, t, s in [
    ("Merge intervals", "start", "O(n log n)", "O(n)"),
    ("Insert interval", "pre-sorted", "O(n)", "O(n)"),
    ("Max concurrency / min rooms", "events", "O(n log n)", "O(n)"),
    ("Max non-overlapping COUNT", "END", "O(n log n)", "O(1)"),
    ("Fewest removals", "END", "O(n log n)", "O(1)"),
    ("Two-list intersection", "pre-sorted", "O(n + m)", "O(n)"),
]:
    print(f"  {prob:<32} {key:<12} {t:<14} {s}")

print("\n  MATRIX")
print(f"  {'Pattern':<32} {'Time':<14} {'Space':<14} {'Key idea'}")
print("  " + "-" * 78)
for prob, t, s, idea in [
    ("Spiral traversal", "O(R*C)", "O(1) extra", "4 shrinking bounds + 2 guards"),
    ("Rotate in place", "O(R*C)", "O(1)", "transpose then reverse rows"),
    ("Number of islands", "O(R*C)", "O(R*C) stack", "mutate grid to mark"),
    ("Multi-source BFS", "O(R*C)", "O(R*C) queue", "seed ALL sources"),
    ("Set matrix zeroes", "O(R*C)", "O(1)", "first row/col as markers"),
    ("Staircase search", "O(R + C)", "O(1)", "start top-right"),
]:
    print(f"  {prob:<32} {t:<14} {s:<14} {idea}")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
