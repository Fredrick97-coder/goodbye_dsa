"""
Exercises: Intervals & Matrix Patterns

Part 1 (1-11):  intervals -- merging, sweeping, intersecting
Part 2 (12-24): matrix -- spiral, rotate, islands, BFS, search
"""

from typing import List, Tuple, Optional

print("=" * 70)
print("EXERCISES: Intervals & Matrix Patterns")
print("=" * 70)
print("""
THE TWO RULES TO INTERNALISE

  INTERVALS: sort first -- by START to merge, by END to maximise a COUNT.
             Derive overlap by negating non-overlap: a2 < b1 or b2 < a1.

  MATRIX:    write rows/cols/DIRS_4/in_bounds at the top, every time.
             Never write [[0]*c]*r -- use a comprehension.
""")

# ============================================================
#                    PART 1: INTERVALS
# ============================================================
print("\n[EASY -- INTERVALS]")
print("-" * 70)

print("\n1. DO TWO INTERVALS OVERLAP?")
print("Input: Two intervals (start, end)")
print("Output: True if they overlap")
print("Example: (1,3) and (2,4) -> True; (1,2) and (3,4) -> False")
def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    # TODO: Do NOT try to enumerate the overlap cases -- there are four and
    # you will miss one. Write the NON-overlap condition (a[1] < b[0] or
    # b[1] < a[0]) and negate it.
    # Decide whether touching endpoints count, and write a comment saying
    # which you chose. Half-open is usually right for time.
    pass

print("\n2. MERGE INTERVALS")
print("Input: A list of intervals, unsorted, possibly overlapping")
print("Output: The minimal list of non-overlapping intervals")
print("Example: [(1,3),(2,6),(8,10)] -> [[1,6],[8,10]]")
def merge(intervals: List[Tuple[int, int]]) -> List[List[int]]:
    # TODO: Sort by START. Walk through; if the current interval starts at
    # or before the last merged interval's end, EXTEND that end.
    # Use max(last_end, end) -- NOT plain assignment. Otherwise [1,10]
    # followed by [2,3] loses the 10. That bug only shows up on NESTED
    # intervals, so it survives casual testing.
    pass

print("\n3. INSERT INTERVAL")
print("Input: A sorted, already-merged list, and one new interval")
print("Output: The list with the new interval merged in")
print("Example: [[1,3],[6,9]] + [2,5] -> [[1,5],[6,9]]")
def insert(intervals: List[List[int]], new: List[int]) -> List[List[int]]:
    # TODO: Three explicit phases, not one loop with flags:
    #   1. copy everything that ends strictly before new starts
    #   2. absorb everything that overlaps (min the starts, max the ends)
    #   3. copy the rest
    # O(n) with no sort, since the input is already ordered.
    pass

print("\n4. CAN A PERSON ATTEND ALL MEETINGS?")
print("Input: Meeting intervals")
print("Output: True if none overlap")
print("Example: [(0,30),(5,10)] -> False")
def can_attend_all(intervals: List[Tuple[int, int]]) -> bool:
    # TODO: Sort by start, then check each interval against only its
    # IMMEDIATE predecessor. After sorting, that is sufficient -- you do
    # not need the O(n^2) pairwise check. Be able to explain why.
    pass

print("\n5. MINIMUM MEETING ROOMS")
print("Input: Meeting intervals")
print("Output: The fewest rooms needed")
print("Example: [(0,30),(5,10),(15,20)] -> 2")
def min_meeting_rooms(intervals: List[Tuple[int, int]]) -> int:
    # TODO: Solve it TWICE.
    #   (a) sweep line: +1 at each start, -1 at each end, sort, track the
    #       running max. Note that (t,-1) sorts before (t,+1), which gives
    #       half-open semantics for free.
    #   (b) heap of end times (Topic 19).
    # Then say which you prefer and why. The sweep line generalises to
    # "when was the peak" and "how long was it busy"; the heap does not.
    pass


print("\n\n[MEDIUM -- INTERVALS]")
print("-" * 70)

print("\n6. NON-OVERLAPPING INTERVALS (FEWEST REMOVALS)")
print("Input: A list of intervals")
print("Output: The minimum number to remove so none overlap")
print("Example: [(1,2),(2,3),(3,4),(1,3)] -> 1")
def erase_overlap_intervals(intervals: List[Tuple[int, int]]) -> int:
    # TODO: Sort by END, not start. Greedily keep any interval starting at
    # or after the last kept end; the answer is len - kept.
    # Sorting by START here is a REAL bug that fails on ~11% of random
    # inputs -- [(1,100),(2,3),(4,5)] picks [1,100] and blocks everything.
    # Verify against a brute-force subset search on small inputs.
    pass

print("\n7. INTERVAL LIST INTERSECTIONS")
print("Input: Two sorted, internally-disjoint interval lists")
print("Output: All intersections")
print("Example: [[0,2],[5,10]] & [[1,5],[8,12]] -> [[1,2],[5,5],[8,10]]")
def interval_intersection(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    # TODO: Two pointers. The intersection of a[i] and b[j] is
    # [max(starts), min(ends)] -- keep it if lo <= hi.
    # Then advance whichever interval ENDS FIRST: it cannot intersect
    # anything further along in the other list.
    # O(n + m), no sorting needed.
    pass

print("\n8. EMPLOYEE FREE TIME")
print("Input: A list of schedules, each a sorted list of busy intervals")
print("Output: The intervals when EVERYONE is free")
print("Example: the gaps in the union of all busy time")
def employee_free_time(schedules: List[List[List[int]]]) -> List[List[int]]:
    # TODO: Flatten everything, merge (problem 2), then return the GAPS
    # between consecutive merged intervals. The free time is the
    # complement of the union.
    # A heap-based k-way merge (Topic 19) also works if the input is huge
    # and you want to stream it.
    pass

print("\n9. MEETING ROOMS III -- WHICH ROOM, AND WHEN")
print("Input: Meeting intervals")
print("Output: A room assignment per meeting, using the fewest rooms")
print("Example: counting rooms is not enough -- you must assign them")
def assign_rooms(intervals: List[Tuple[int, int]]) -> List[int]:
    # TODO: Sort by start. Keep a min-heap of (end_time, room_id) for busy
    # rooms and a min-heap of free room ids. Release everything that has
    # ended, then take the lowest-numbered free room (or open a new one).
    # Counting is a sweep line; ASSIGNING needs the heap. Know the
    # difference -- interviewers escalate from one to the other.
    pass

print("\n10. CAR POOLING / CAPACITY CHECK")
print("Input: Trips (passengers, start, end) and a vehicle capacity")
print("Output: True if capacity is never exceeded")
print("Example: a weighted sweep line")
def car_pooling(trips: List[Tuple[int, int, int]], capacity: int) -> bool:
    # TODO: Sweep line where the delta is the PASSENGER COUNT, not 1.
    # Same three lines as problem 5 with a different weight -- that is the
    # sign you have understood the pattern rather than memorised it.
    pass

print("\n11. MINIMUM NUMBER OF ARROWS TO BURST BALLOONS")
print("Input: Balloon intervals")
print("Output: The fewest points that stab every interval")
print("Example: [[10,16],[2,8],[1,6],[7,12]] -> 2")
def find_min_arrows(points: List[List[int]]) -> int:
    # TODO: Sort by END and shoot at each end point greedily. This is the
    # same exchange argument as problem 6 and as activity selection in
    # Topic 15 -- three problems, one greedy proof. Recognising that is
    # worth more than three memorised solutions.
    pass


# ============================================================
#                   PART 2: MATRIX PATTERNS
# ============================================================
print("\n\n[EASY -- MATRIX]")
print("-" * 70)

print("\n12. TRANSPOSE A MATRIX")
print("Input: A square matrix")
print("Output: The transpose, in place")
print("Example: swap only where c > r")
def transpose(matrix: List[List[int]]) -> None:
    # TODO: Swap matrix[r][c] with matrix[c][r] for c in range(r+1, n).
    # Using range(n) swaps every pair TWICE and returns the original --
    # a bug that looks like it works because the code reads correctly.
    pass

print("\n13. ROTATE A MATRIX 90 DEGREES IN PLACE")
print("Input: A square matrix")
print("Output: Rotated clockwise, O(1) extra space")
print("Example: transpose, then reverse each row")
def rotate(matrix: List[List[int]]) -> None:
    # TODO: transpose (problem 12), then reverse each row.
    # Verify by building a reference matrix with
    #   new[r][c] = old[n-1-c][r]
    # and by checking that four rotations return the original.
    # Bonus: counter-clockwise and 180 degrees.
    pass

print("\n14. SPIRAL ORDER TRAVERSAL")
print("Input: Any m x n matrix")
print("Output: Elements in spiral order")
print("Example: [[1,2,3],[4,5,6],[7,8,9]] -> [1,2,3,6,9,8,7,4,5]")
def spiral_order(matrix: List[List[int]]) -> List[int]:
    # TODO: Four boundaries (top, bottom, left, right) shrinking inward.
    # The two GUARDS are mandatory: check `top <= bottom` before the
    # right-to-left pass and `left <= right` before the bottom-to-top pass.
    # Without them a single remaining row is emitted TWICE.
    # Test 1x1, 1xN, and Nx1 -- that is exactly where it breaks.
    pass

print("\n15. GENERATE A SPIRAL MATRIX")
print("Input: n")
print("Output: An n x n matrix filled 1..n^2 in spiral order")
print("Example: the inverse of problem 14, same boundary logic")
def generate_spiral(n: int) -> List[List[int]]:
    # TODO: Same four shrinking bounds, writing instead of reading.
    # Remember: [[0]*n for _ in range(n)], never [[0]*n]*n.
    pass

print("\n16. SET MATRIX ZEROES")
print("Input: A matrix")
print("Output: Every row and column containing a 0 becomes all zeroes")
print("Example: do it in O(1) extra space")
def set_zeroes(matrix: List[List[int]]) -> None:
    # TODO: First record whether row 0 and column 0 themselves contain a
    # zero. Then use row 0 and column 0 as MARKER storage for the interior.
    # Apply the interior FIRST, then overwrite row 0 / column 0 last --
    # they are still holding your markers until then.
    # Verify against an O(R+C)-space reference using two index sets.
    pass

print("\n17. DIAGONAL TRAVERSE")
print("Input: A matrix")
print("Output: Elements in diagonal (zigzag) order")
print("Example: cells on one diagonal all share the same r + c")
def diagonal_order(matrix: List[List[int]]) -> List[int]:
    # TODO: Group cells by r + c (there are R + C - 1 diagonals), then
    # reverse alternate groups for the zigzag.
    # The r+c invariant is the same fact that makes N-Queens diagonal
    # checks O(1) in Topic 20.
    pass


print("\n\n[MEDIUM -- MATRIX]")
print("-" * 70)

print("\n18. NUMBER OF ISLANDS")
print("Input: A grid of '1' (land) and '0' (water)")
print("Output: The count of connected land components")
print("Example: 4-directional connectivity")
def num_islands(grid: List[List[str]]) -> int:
    # TODO: Implement THREE ways and cross-check them:
    #   (a) recursive DFS, sinking each island by overwriting with '0'
    #   (b) iterative DFS with an explicit stack
    #   (c) Union-Find (Topic 14)
    # Then measure (a) on a 600x600 all-land grid and watch it hit
    # RecursionError. (b) is the production answer. Bring this up
    # unprompted in an interview.
    pass

print("\n19. FLOOD FILL")
print("Input: An image grid, a start cell, and a new colour")
print("Output: The 4-connected region recoloured")
print("Example: guard against the new colour equalling the old one")
def flood_fill(image: List[List[int]], sr: int, sc: int, colour: int) -> List[List[int]]:
    # TODO: Same traversal as islands. The trap: if colour == the starting
    # colour, a naive recursion never terminates because the "visited"
    # marker is indistinguishable from unvisited. Guard it explicitly.
    pass

print("\n20. ROTTING ORANGES (MULTI-SOURCE BFS)")
print("Input: A grid of 0 (empty), 1 (fresh), 2 (rotten)")
print("Output: Minutes until nothing fresh remains, or -1")
print("Example: rot spreads from ALL rotten cells simultaneously")
def oranges_rotting(grid: List[List[int]]) -> int:
    # TODO: Seed the queue with EVERY rotten cell before starting. Then
    # process level by level with `for _ in range(len(queue))` -- snapshot
    # the length, because the queue grows while you iterate.
    # Count fresh oranges upfront so you can return -1 when some are
    # unreachable. Running BFS per source would be O(sources * R * C).
    pass

print("\n21. 01 MATRIX / NEAREST ZERO")
print("Input: A binary matrix")
print("Output: For each cell, its distance to the nearest 0")
print("Example: multi-source BFS seeded from every zero")
def update_matrix(mat: List[List[int]]) -> List[List[int]]:
    # TODO: Seed from all zeros at once -- BFS then computes every
    # distance in ONE sweep, O(R*C).
    # The naive alternative (BFS from each 1) is O((R*C)^2). Reversing
    # the direction of the search is the entire trick.
    pass

print("\n22. SEARCH A 2D MATRIX (STAIRCASE)")
print("Input: A matrix sorted along both rows and columns, and a target")
print("Output: True if present")
print("Example: O(R + C), not O(R * C) and not O(log)")
def search_matrix(matrix: List[List[int]], target: int) -> bool:
    # TODO: Start at the TOP-RIGHT. If the value is too big, drop the
    # column; if too small, drop the row. Each step eliminates a whole
    # row or column.
    # Bottom-left works identically. Top-left does NOT: both moves
    # increase, so a mismatch gives you no information. Be ready to say
    # why the corner matters.
    pass


print("\n\n[HARD / CHALLENGE]")
print("-" * 70)

print("\n23. WORD SEARCH IN A GRID (BACKTRACKING + MATRIX)")
print("Input: A character grid and a word")
print("Output: True if the word can be traced through adjacent cells")
print("Example: combines Topic 20 with this topic's grid setup")
def exist(board: List[List[str]], word: str) -> bool:
    # TODO: DFS from every cell, marking the current cell and RESTORING it
    # on the way out (Topic 20's choose/explore/undo). Forgetting the
    # restore corrupts the board for later start positions -- a silent
    # wrong answer, not a crash.
    pass

print("\n24. SURROUNDED REGIONS")
print("Input: A board of 'X' and 'O'")
print("Output: Flip every 'O' region NOT touching the border to 'X'")
print("Example: invert the problem -- mark what SURVIVES")
def solve_surrounded(board: List[List[str]]) -> None:
    # TODO: Do not try to detect enclosure directly. Instead flood-fill
    # from the BORDER 'O's, marking them safe, then flip everything still
    # unmarked. Inverting the question is the insight.
    pass

print("\n25. SPIRAL MATRIX III / WALK OFF THE GRID")
print("Input: Grid dimensions and a start cell")
print("Output: All cells in spiral order, where the spiral may leave the grid")
print("Example: step lengths grow 1,1,2,2,3,3,... regardless of bounds")
def spiral_walk(rows: int, cols: int, r0: int, c0: int) -> List[List[int]]:
    # TODO: The shrinking-boundary trick does NOT work here, because the
    # spiral wanders outside. Walk with growing step lengths
    # (1,1,2,2,3,3,...) and simply skip out-of-bounds cells, stopping once
    # you have collected rows*cols of them.
    # A good reminder that "spiral" is not one algorithm.
    pass

print("\n26. MAXIMAL SQUARE (MATRIX + DP)")
print("Input: A binary matrix")
print("Output: The area of the largest all-1 square")
print("Example: dp[r][c] = 1 + min(up, left, up-left) when grid[r][c] == 1")
def maximal_square(matrix: List[List[str]]) -> int:
    # TODO: This is Topic 12's DP on a grid. The recurrence is the whole
    # problem: a square of side k ending at (r,c) requires squares of side
    # k-1 ending above, left, and up-left.
    # Note that backtracking would be exponential here. Recognising that
    # a grid question is really a DP question is the skill being tested.
    pass

print("\n27. SPARSE MATRIX MULTIPLICATION")
print("Input: Two matrices, mostly zeros")
print("Output: Their product, skipping the zeros")
print("Example: the practical version of a textbook triple loop")
def sparse_multiply(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    # TODO: The naive triple loop is O(m*n*p) regardless of sparsity.
    # Instead index the non-zero entries of each matrix and iterate only
    # over those. Measure both on a 1%-dense matrix and report the
    # speedup -- this is the difference between textbook and production.
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
PART 1: INTERVALS

1. The One Rule:
   SORT FIRST. The only real decision is the key:

     by START  -> merging, inserting, overlap detection, concurrency
     by END    -> maximising the COUNT of non-overlapping intervals

   Choosing wrong gives you code that looks right and fails on ~11% of
   random inputs. Measured, not guessed.

2. Overlap, Derived Not Memorised:
     no overlap  <=>  a[1] < b[0] or b[1] < a[0]
     overlap     <=>  a[0] <= b[1] and b[0] <= a[1]

   Always write the negation first. And DECIDE the endpoint semantics:
     closed    [1,2] and [2,3] DO overlap      -> use <=
     half-open [1,2) and [2,3) do NOT overlap  -> use <
   Half-open is usually intended for time. State your assumption aloud.

3. Merge Intervals:
   Sort by start; if start <= last_end, extend with MAX(last_end, end).
   Plain assignment loses nested intervals ([1,10] then [2,3]) and only
   fails on nested input, so it survives casual testing.

4. Insert Interval -- three phases, O(n), no sort:
   before / absorb-overlaps / after. Structure it as three loops, not one
   loop with flags.

5. The Sweep Line -- the most general interval tool:
   Convert to events, sort, sweep a running counter.

     +1 at each start, -1 at each end
     (t,-1) sorts before (t,+1)  ->  half-open semantics for free

   It answers what a heap cannot:
     peak concurrency      max of the counter
     WHEN the peak hit     the time at that max
     total covered length  sum of gaps where counter > 0
     covered by >= k       gaps where counter >= k

   Flip the tie order and you are off by one -- but only on inputs that
   actually have ties, which is why it slips through tests.

6. Weighted sweep line: make the delta a passenger count, a bandwidth, a
   cost. Same three lines. That substitution is the test of whether you
   understood the pattern.

7. Intersection of two sorted lists -- two pointers, O(n+m):
   [max(starts), min(ends)] if non-empty, then advance whichever ENDS
   FIRST. It cannot intersect anything further along.

8. Counting vs Assigning:
   "how many rooms"   -> sweep line
   "WHICH room each"  -> heap of (end_time, room_id)
   Interviewers escalate from the first to the second.

Interval Complexity:

Problem                        Sort by      Time         Space
────────────────────────────────────────────────────────────────
Merge intervals                start        O(n log n)   O(n)
Insert interval                pre-sorted   O(n)         O(n)
Max concurrency / min rooms    events       O(n log n)   O(n)
Max non-overlapping COUNT      END          O(n log n)   O(1)
Fewest removals                END          O(n log n)   O(1)
Min arrows to burst            END          O(n log n)   O(1)
Two-list intersection          pre-sorted   O(n + m)     O(n)
Employee free time             events       O(n log n)   O(n)


PART 2: MATRIX PATTERNS

9. The Setup, Every Time:
     rows, cols = len(grid), len(grid[0]) if grid else 0
     DIRS_4 = [(-1,0),(1,0),(0,-1),(0,1)]
     DIRS_8 = DIRS_4 + [(-1,-1),(-1,1),(1,-1),(1,1)]
     def in_bounds(r, c): return 0 <= r < rows and 0 <= c < cols

   A named in_bounds eliminates a whole bug class. Guard grid[0] -- the
   empty grid is a standard hidden test.

10. THE TRAP: [[0]*cols]*rows makes `rows` references to ONE list.
    Mutating [0][0] changes every row. Always use a comprehension:
      [[0]*cols for _ in range(rows)]
    This catches everyone exactly once.

11. Spiral: four boundaries shrinking inward, with TWO mandatory guards
    (`top <= bottom` and `left <= right`) before the reverse passes.
    Without them, a single remaining row is emitted twice. Test 1x1,
    1xN, Nx1.

12. Rotate in place = TRANSPOSE then REVERSE EACH ROW. O(1) space.
    The transpose inner loop must be range(r+1, n). Using range(n) swaps
    every pair twice and silently returns the original.
      clockwise         transpose, reverse rows
      counter-clockwise transpose, reverse columns
      180 degrees       reverse rows, reverse each row

13. Islands = DFS/BFS on an implicit graph. Mutate the grid to mark
    visited (free O(1) space) or keep a visited set if you may not touch
    the input.

    RECURSION DEPTH IS REAL: a 600x600 all-land grid needs up to 360,000
    frames against Python's 1,000 limit. Iterative DFS with an explicit
    stack is the production answer. Say so before you are asked.

14. Multi-Source BFS -- seed EVERY source before sweeping:
      rotting oranges, nearest zero, fire spread, water levels
    Reversing the search direction (from all zeros outward, instead of
    from each one inward) turns O((R*C)^2) into O(R*C).

    `for _ in range(len(queue))` processes exactly one LEVEL, which is
    how BFS measures time or distance. Snapshot the length -- the queue
    grows while you iterate it.

15. Set Matrix Zeroes in O(1): use row 0 and column 0 as marker storage.
    Apply the interior FIRST, then overwrite the markers. Reversing that
    order destroys the marks you still need.

16. Staircase Search -- O(R + C) on a doubly-sorted matrix:
    Start TOP-RIGHT. Too big -> drop the column. Too small -> drop the row.
    Bottom-left is equivalent. Top-left and bottom-right do NOT work:
    both available moves change the value in the same direction, so a
    mismatch tells you nothing.

Matrix Complexity:

Pattern                Time        Space         Key idea
──────────────────────────────────────────────────────────────────────
Spiral traversal       O(R*C)      O(1) extra    4 bounds + 2 guards
Spiral generate        O(R*C)      O(R*C) out    same bounds, writing
Transpose              O(R*C)      O(1)          c > r only
Rotate in place        O(R*C)      O(1)          transpose + reverse
Number of islands      O(R*C)      O(R*C) stack  mutate to mark
Flood fill             O(R*C)      O(R*C) stack  guard same-colour
Multi-source BFS       O(R*C)      O(R*C) queue  seed ALL sources
Nearest zero (01)      O(R*C)      O(R*C)        reverse the direction
Set matrix zeroes      O(R*C)      O(1)          first row/col markers
Staircase search       O(R + C)    O(1)          start top-right
Diagonal traverse      O(R*C)      O(1) extra    r + c is constant
Maximal square (DP)    O(R*C)      O(C)          1 + min(3 neighbours)


Cross-Topic Connections:

  Topic 15 Greedy      sort-by-end is activity selection, min arrows, and
                       fewest removals -- ONE exchange argument, three
                       problems
  Topic 19 Heaps       min rooms via a heap; ASSIGNING rooms needs one
  Topic 11 Graphs      islands is connected components on an implicit graph
  Topic 14 Union-Find  a third correct way to count islands
  Topic 20 Backtracking word search = grid setup + choose/explore/undo
  Topic 12 DP          maximal square is grid DP, not search
  Topic 16 Bits        N-Queens diagonals use the same r+c / r-c invariant
                       as diagonal traversal

Common Pitfalls:

1. Wrong sort key (start vs end). Fails ~11% of random inputs.
2. merged[-1][1] = end instead of max(...). Breaks on nested intervals.
3. Ambiguous endpoint semantics -- decide and state it.
4. Sweep-line tie order flipped. Off by one, on ties only.
5. Not handling the empty interval list.
6. Missing the two spiral guards.
7. Transposing with range(n) instead of range(r+1, n).
8. [[0]*c]*r aliasing.
9. Not guarding grid[0] on an empty grid.
10. Recursion depth on large grids.
11. Forgetting to snapshot len(queue) in level-order BFS.
12. Writing the first row/column too early in set-matrix-zeroes.
13. Starting a staircase search at the top-left.
14. Not restoring a mutated cell in grid backtracking.

Interview Tips:

1. ASK about endpoint semantics before writing interval code. It reads as
   care, and it is a real ambiguity.
2. Say which sort key you chose AND WHY. That is the actual test.
3. Offer the sweep line when a question mentions concurrency, coverage, or
   "at any point in time" -- and mention that it generalises where the
   heap solution does not.
4. For grids, state O(R*C) and note that each cell is visited once.
5. Raise the recursion-depth risk on large grids yourself.
6. Name the O(1)-space tricks (transpose+reverse, first-row markers).
   They separate a passing answer from a strong one.
7. When you see "sorted rows AND columns", say "staircase from the
   top-right" and explain why the corner matters.

Learning Progression:

1. Basic: overlap predicate, merge, insert, transpose, spiral
2. Intermediate: sweep line, sort-key choice, islands, multi-source BFS
3. Advanced: room assignment, employee free time, O(1)-space zeroes,
   staircase search
4. Expert: spiral-off-grid, sparse multiplication, and recognising when a
   grid problem is really DP

Next: implement each stub, then run project.py to see these patterns
running a calendar, an image editor, a game-of-life engine, and a
seat-booking system.
""")
