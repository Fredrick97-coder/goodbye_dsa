# Intervals & Matrix Patterns - Two Families You Will Be Asked About

Master interval merging, sweep lines, and the grid-traversal patterns:
spiral, rotate-in-place, islands, and multi-source BFS.

---

# PART 1: INTERVALS

## 1. The One Rule That Solves Most Interval Problems

> **Sort first. By start time, or by end time — and knowing which is the
> whole problem.**

| Sort by | Use for |
|---------|---------|
| **start** | merging, inserting, finding overlaps, counting concurrency |
| **end** | maximising the *count* of non-overlapping intervals (greedy) |

That's the fork. Get it right and the rest is bookkeeping; get it wrong and
you'll write a correct-looking loop that returns wrong answers on the third
test case.

Sorting by end time for interval *scheduling* was Topic 15 (Greedy). Here we
cover the other side: merging, overlap detection, and sweep lines.

---

## 2. Overlap Detection

Two intervals `[a1, a2]` and `[b1, b2]` overlap when:

```python
def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]
```

Reason about the *negation* instead — it's easier to get right. They **don't**
overlap only when one finishes entirely before the other starts:

```
No overlap:   a2 < b1   OR   b2 < a1

  a: [----]
  b:         [----]        a2 < b1

  a:         [----]
  b: [----]                b2 < a1
```

Negate that and you get the condition above. Whenever you doubt an interval
comparison, write the non-overlap case and negate it.

**Touching endpoints**: is `[1,2]` and `[2,3]` an overlap? It depends on the
problem. Half-open intervals `[start, end)` — a meeting ending at 2:00 and
one starting at 2:00 don't conflict — use `<`. Closed intervals use `<=`.
**Ask, or state your assumption.** This is the single most common source of
off-by-one bugs in interval problems.

---

## 3. Merge Intervals

```python
def merge(intervals):
    """O(n log n) for the sort, O(n) for the pass."""
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])          # by START
    merged = [list(intervals[0])]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:              # overlaps the last merged
            merged[-1][1] = max(merged[-1][1], end)   # extend
        else:
            merged.append([start, end])         # disjoint: start a new one
    return merged
```

The `max` matters: `[1,10]` followed by `[2,3]` must stay `[1,10]`. Writing
`merged[-1][1] = end` is a real bug that passes on non-nested input.

```
Input:  [1,3] [2,6] [8,10] [15,18]
Sorted: [1,3] [2,6] [8,10] [15,18]

[1,3]              -> merged: [[1,3]]
[2,6]   2 <= 3     -> extend: [[1,6]]
[8,10]  8 > 6      -> append: [[1,6],[8,10]]
[15,18] 15 > 10    -> append: [[1,6],[8,10],[15,18]]
```

**Time**: O(n log n), dominated by the sort. **Space**: O(n) for the output.

---

## 4. Insert Interval

Inserting into an already-sorted, already-merged list — O(n), no sort needed.

```python
def insert(intervals, new):
    result = []
    i, n = 0, len(intervals)

    # 1. Everything strictly before `new`
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # 2. Absorb everything that overlaps
    start, end = new
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])

    # 3. Everything strictly after
    result.extend(intervals[i:])
    return result
```

Three phases: before, overlapping, after. Structuring it this way is far more
reliable than trying to handle it in one loop with flags.

---

## 5. The Sweep Line

The most powerful interval technique. **Convert intervals into events, sort
the events, sweep through them keeping a running count.**

```python
def max_concurrent(intervals):
    """Peak number of simultaneously active intervals. O(n log n)"""
    events = []
    for start, end in intervals:
        events.append((start, 1))       # +1 when something starts
        events.append((end, -1))        # -1 when something ends
    events.sort()

    current = peak = 0
    for _, delta in events:
        current += delta
        peak = max(peak, current)
    return peak
```

**Critical detail — tie ordering.** When one interval ends exactly as another
begins, which event fires first?

- `(time, -1)` sorts before `(time, +1)` because -1 < 1, so **ends are
  processed first**. That treats intervals as half-open `[start, end)`: a
  meeting ending at 2:00 frees the room for one starting at 2:00.
- If your problem treats endpoints as overlapping (closed intervals), encode
  starts as `(time, 0)` and ends as `(time, 1)`, or sort with an explicit key.

Getting this backwards produces answers that are off by exactly one in
tie cases — and passes every test that doesn't have a tie.

### Why Sweep Line Beats the Heap Here

Topic 19 solved "minimum meeting rooms" with a heap of end times. Sweep line
solves it with a sort and a counter — simpler, and it generalises:

| Question | Sweep line answer |
|----------|-------------------|
| Peak concurrency | max of the running counter |
| When does the peak occur | the time at which max was hit |
| Total covered length | sum of gaps where counter > 0 |
| Points covered by ≥ k intervals | times where counter ≥ k |

The heap answers only the first. Sweep line is the more general tool.

---

## 6. Common Interval Problems

```python
def erase_overlap_intervals(intervals):
    """Fewest removals to make the rest non-overlapping. Sort by END."""
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])          # by END -- greedy
    kept, last_end = 1, intervals[0][1]
    for start, end in intervals[1:]:
        if start >= last_end:
            kept += 1
            last_end = end
    return len(intervals) - kept


def interval_intersection(a, b):
    """Intersect two sorted, disjoint lists. O(n + m), two pointers."""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            result.append([lo, hi])
        # Advance whichever ends first -- it cannot intersect anything else
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result
```

The intersection pattern is worth memorising: `max` of starts, `min` of ends,
and advance the one that ends first.

### Complexity Summary — Intervals

| Problem | Sort by | Time | Space |
|---------|---------|------|-------|
| Merge intervals | start | O(n log n) | O(n) |
| Insert interval | (pre-sorted) | **O(n)** | O(n) |
| Max concurrency | events | O(n log n) | O(n) |
| Min rooms needed | events or heap | O(n log n) | O(n) |
| Erase overlaps (fewest removals) | **end** | O(n log n) | O(1) |
| Max non-overlapping count | **end** | O(n log n) | O(1) |
| Two-list intersection | (pre-sorted) | O(n + m) | O(n) |
| Employee free time | events | O(n log n) | O(n) |

---

# PART 2: MATRIX PATTERNS

## 7. The Setup Every Grid Problem Needs

```python
rows, cols = len(grid), len(grid[0]) if grid else 0

DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]              # up down left right
DIRS_8 = DIRS_4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]   # plus diagonals

def in_bounds(r, c):
    return 0 <= r < rows and 0 <= c < cols
```

Writing `in_bounds` as a helper rather than inlining four comparisons
eliminates a whole class of bugs. Always guard `grid[0]` — an empty grid is a
standard hidden test case.

---

## 8. Spiral Traversal

Four moving boundaries, shrinking inward.

```python
def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):        # left -> right along top
            result.append(matrix[top][c])
        top += 1

        for r in range(top, bottom + 1):        # top -> bottom along right
            result.append(matrix[r][right])
        right -= 1

        if top <= bottom:                       # GUARD: single row left?
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1

        if left <= right:                       # GUARD: single column left?
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1
    return result
```

**The two guards are not optional.** Without them, a single remaining row
gets traversed twice — once left-to-right, once right-to-left. Test on
`1×n`, `n×1`, and `1×1` matrices; those are exactly where naive versions
break.

---

## 9. Rotate a Matrix In Place

**The trick**: transpose, then reverse each row. That's a 90° clockwise
rotation, and it needs O(1) extra space.

```python
def rotate(matrix):
    n = len(matrix)

    # 1. Transpose (reflect across the main diagonal)
    for r in range(n):
        for c in range(r + 1, n):               # c > r, or you undo your work
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]

    # 2. Reverse each row
    for row in matrix:
        row.reverse()
```

```
1 2 3      transpose      1 4 7    reverse rows     7 4 1
4 5 6      --------->     2 5 8    ------------>    8 5 2
7 8 9                     3 6 9                     9 6 3
```

The `range(r + 1, n)` is essential: iterating the full row swaps every pair
twice, returning the original matrix. A classic self-inflicted bug.

**Variants**: counter-clockwise = transpose then reverse *columns* (or
reverse rows then transpose). 180° = reverse rows and reverse each row.

---

## 10. Islands (Connected Components on a Grid)

This is just DFS/BFS from Topic 11, with the grid as an implicit graph.

```python
def num_islands(grid):
    """O(rows * cols) -- every cell visited at most once."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def sink(r, c):
        """Flood-fill this island so it is never counted again."""
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        grid[r][c] = "0"                        # mark visited IN PLACE
        for dr, dc in DIRS_4:
            sink(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
```

**Mutating the grid** is the standard space optimisation — no separate
`visited` set. If you may not modify the input, copy it or keep a `visited`
set and say so.

**Recursion depth**: a 1000×1000 grid of all land recurses up to 1,000,000
deep and will crash Python. Use an explicit stack (iterative DFS) or BFS for
large grids. Interviewers do ask about this.

### Multi-Source BFS

When something spreads from *many* starting points simultaneously — rotting
oranges, fire, water levels — seed the BFS queue with **all** sources at once.

```python
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))            # ALL sources seeded
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):             # process one full level
            r, c = queue.popleft()
            for dr, dc in DIRS_4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1

    return minutes if fresh == 0 else -1
```

The `for _ in range(len(queue))` is the level-by-level trick — it's how BFS
measures *time* or *distance* rather than just reachability. Snapshot the
length before the loop; the queue grows while you iterate it.

---

## 11. Other Matrix Patterns

### Set Matrix Zeroes (O(1) space)

Use the first row and column as your own marker storage:

```python
def set_zeroes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))

    # Mark in the first row/col
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    # Apply the marks
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    # Handle the first row/col last -- they were the markers
    if first_row_zero:
        for c in range(cols):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0
```

Order matters: apply the interior first, then the marker row/column. Doing
the first row early destroys the marks you still need.

### Search a Sorted Matrix — Staircase Search

If rows and columns are both sorted, start at the **top-right** corner:

```python
def search_matrix(matrix, target):
    """O(rows + cols) -- not O(log) but far better than O(rows * cols)."""
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        if matrix[r][c] == target:
            return True
        if matrix[r][c] > target:
            c -= 1                              # too big: drop this column
        else:
            r += 1                              # too small: drop this row
    return False
```

The top-right corner is special: moving left strictly decreases, moving down
strictly increases. Each step eliminates an entire row or column. Bottom-left
works identically; top-left and bottom-right do **not** (both moves go the
same direction, so you can't decide).

---

## 12. Complexity Summary — Matrix

| Pattern | Time | Space | Note |
|---------|------|-------|------|
| Spiral traversal | O(R·C) | O(1) extra | four shrinking bounds |
| Rotate in place | O(R·C) | **O(1)** | transpose + reverse rows |
| Transpose | O(R·C) | O(1) if square | `c > r` only |
| Number of islands | O(R·C) | O(R·C) worst stack | mutate to mark |
| Multi-source BFS | O(R·C) | O(R·C) queue | seed all sources |
| Set matrix zeroes | O(R·C) | **O(1)** | first row/col as markers |
| Staircase search | **O(R + C)** | O(1) | start top-right |
| Spiral generate | O(R·C) | O(R·C) output | same bounds logic |
| Diagonal traverse | O(R·C) | O(1) extra | `r + c` is constant |
| Flood fill | O(R·C) | O(R·C) stack | same as islands |

---

## 13. Common Pitfalls

**Intervals**

1. **Sorting by the wrong key.** Merging needs start; maximising the count of
   non-overlapping intervals needs end. Wrong choice → plausible wrong answers.
2. **`merged[-1][1] = end` instead of `max(...)`.** Breaks on nested
   intervals like `[1,10]` then `[2,3]`.
3. **Ambiguous endpoint semantics.** Decide whether `[1,2]` and `[2,3]`
   overlap, and say so. Half-open is usually intended for time.
4. **Sweep-line tie order.** `(t, -1)` before `(t, +1)` gives half-open
   behaviour. Flip it and you're off by one on ties only.
5. **Not handling the empty list.** `intervals[0]` on `[]` raises.
6. **Mutating the caller's list via `sort()`** when they didn't expect it.

**Matrix**

7. **Missing the two spiral guards.** Single remaining row/column gets
   double-traversed.
8. **Transposing with the full row range** instead of `c > r`, which undoes
   every swap.
9. **Not guarding `grid[0]`** on an empty grid.
10. **`[[0] * cols] * rows`** — every row is the *same list object*. Use a
    comprehension: `[[0] * cols for _ in range(rows)]`. This bites everyone
    once.
11. **Recursion depth on large grids.** 1000×1000 all-land island DFS
    crashes. Go iterative.
12. **Forgetting to snapshot `len(queue)`** in level-order BFS.
13. **Setting the first row/column too early** in set-matrix-zeroes.
14. **Starting a staircase search at the wrong corner.** Top-left doesn't work.

---

## 14. Key Takeaways

**Intervals**

✅ **Sort first** — by **start** to merge, by **end** to maximise the count
✅ **Non-overlap is `a2 < b1 or b2 < a1`** — negate it rather than guessing
✅ **Merge extends with `max(...)`**, never plain assignment
✅ **Insert is three phases**: before, absorb, after — and O(n), no sort
✅ **Sweep line** = events + sort + running counter; more general than a heap
✅ **Tie order encodes endpoint semantics** — `(t,-1)` before `(t,+1)` is half-open
✅ **Intersection** = `max` of starts, `min` of ends, advance the earlier end

**Matrix**

✅ **Write `in_bounds` and `DIRS_4` once**, at the top
✅ **Spiral needs two guards** for the single-row and single-column cases
✅ **Rotate = transpose + reverse rows**, O(1) space, `c > r` in the transpose
✅ **Islands = DFS/BFS on an implicit graph**; mutate the grid to mark visited
✅ **Multi-source BFS**: seed every source before starting the sweep
✅ **`for _ in range(len(queue))`** turns BFS into a distance/time measurement
✅ **Staircase search from the top-right** gives O(R + C) on a sorted matrix
✅ **`[[0]*c]*r` is a trap** — use a comprehension
✅ **Watch recursion depth** on large grids; iterate instead

**Interview Focus**:
- Ask about endpoint semantics before writing interval code. It signals care.
- Say which sort key you're using *and why* — that's the actual test.
- Offer sweep line when a question asks about concurrency or coverage; it
  generalises where the heap solution doesn't.
- For grids, state O(R·C) and note that every cell is visited once.
- Mention the recursion-depth risk on large grids before being asked.
- Name the O(1)-space tricks (transpose+reverse, first-row markers) — they're
  the difference between a passing and a strong answer.

Next: implement merge and sweep line, then the five grid patterns — and
verify every one against a brute-force reference!
