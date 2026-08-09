"""
Examples: Backtracking

One template, eight problems. Plus the pruning that makes it viable
and the DP comparison that tells you when NOT to use it.
"""

import itertools
import sys
import time
from typing import List, Tuple, Set, Optional

print("=" * 70)
print("BACKTRACKING")
print("=" * 70)

# ==================== (1) The Template ====================
print("\n[1] The Universal Template: Choose, Explore, Undo")
print("-" * 70)

print("""  def backtrack(state, path, results):
      if is_complete(path):
          results.append(path[:])      # COPY -- path keeps mutating
          return

      for choice in candidates(state, path):
          if not is_valid(choice, path):
              continue                 # PRUNE

          path.append(choice)          # 1. CHOOSE
          backtrack(state, path, results)   # 2. EXPLORE
          path.pop()                   # 3. UNDO
""")

print("  Every problem below fills in the same four blanks:")
print("    is_complete  -- when is a path a finished solution?")
print("    candidates   -- what can I try next?")
print("    is_valid     -- which candidates are legal here?")
print("    what to record")

# The path[:] bug, demonstrated
print("\n  THE #1 BUG -- appending `path` instead of `path[:]`:")

def subsets_buggy(nums: List[int]) -> List[List[int]]:
    results = []
    def bt(start, path):
        results.append(path)           # BUG: stores a reference
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return results

def subsets_correct(nums: List[int]) -> List[List[int]]:
    results = []
    def bt(start, path):
        results.append(path[:])        # correct: stores a snapshot
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return results

print(f"    buggy  : {subsets_buggy([1, 2, 3])}")
print(f"    correct: {subsets_correct([1, 2, 3])}")
print("    -> The buggy version returns 8 references to ONE list, which the")
print("       undo steps have emptied by the time you look at it.")

# ==================== (2) Subsets ====================
print("\n[2] Subsets (The Power Set) -- 2^n Results")
print("-" * 70)

def subsets_include_exclude(nums: List[int]) -> List[List[int]]:
    """Branch twice at each element: in or out."""
    results = []
    def bt(i, path):
        if i == len(nums):
            results.append(path[:])
            return
        bt(i + 1, path)                # exclude nums[i]
        path.append(nums[i])           # include nums[i]
        bt(i + 1, path)
        path.pop()
    bt(0, [])
    return results


def subsets_loop(nums: List[int]) -> List[List[int]]:
    """Loop-and-recurse. Generalises to combinations and partitioning."""
    results = []
    def bt(start, path):
        results.append(path[:])        # EVERY node is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1, path)            # i+1: never reuse an element
            path.pop()
    bt(0, [])
    return results


nums = [1, 2, 3]
r1 = subsets_include_exclude(nums)
r2 = subsets_loop(nums)
print(f"  subsets({nums}):")
print(f"    include/exclude: {r1}")
print(f"    loop-and-recurse: {r2}")
print(f"    same set of subsets: {sorted(map(sorted, r1)) == sorted(map(sorted, r2))}")
print(f"    count: {len(r2)} = 2^{len(nums)}")

print("\n  The decision tree (include/exclude at each level):")
print("""                        []
                  /            \\
            include 1        skip 1
              [1]               []
            /     \\           /     \\
        [1,2]     [1]      [2]      []
        /   \\     /  \\     /  \\    /  \\
   [1,2,3][1,2][1,3][1]  [2,3][2] [3]  []
""")

print(f"  {'n':>4} {'2^n subsets':>13} {'time':>10}")
print("  " + "-" * 30)
for n in [4, 8, 16, 20]:
    arr = list(range(n))
    start = time.perf_counter()
    res = subsets_loop(arr)
    ms = (time.perf_counter() - start) * 1000
    assert len(res) == 2 ** n
    print(f"  {n:>4} {len(res):>13,} {ms:>8.1f}ms")
print("\n  -> O(n * 2^n) and unavoidable: the OUTPUT is that large.")

# ==================== (3) Permutations ====================
print("\n[3] Permutations -- n! Results")
print("-" * 70)

def permutations_used(nums: List[int]) -> List[List[int]]:
    """Track which elements are consumed with a `used` array."""
    results = []
    used = [False] * len(nums)
    def bt(path):
        if len(path) == len(nums):
            results.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True             # CHOOSE
            path.append(nums[i])
            bt(path)                   # EXPLORE
            path.pop()                 # UNDO
            used[i] = False            # UNDO
    bt([])
    return results


def permutations_swap(nums: List[int]) -> List[List[int]]:
    """Swap-in-place. No `used` array -- the prefix IS the state."""
    results = []
    arr = list(nums)
    def bt(start):
        if start == len(arr):
            results.append(arr[:])
            return
        for i in range(start, len(arr)):
            arr[start], arr[i] = arr[i], arr[start]     # CHOOSE
            bt(start + 1)                               # EXPLORE
            arr[start], arr[i] = arr[i], arr[start]     # UNDO
    bt(0)
    return results


nums = [1, 2, 3]
p1 = permutations_used(nums)
p2 = permutations_swap(nums)
print(f"  permutations({nums}):")
print(f"    used-array: {p1}")
print(f"    swap      : {p2}")
print(f"    same set  : {sorted(p1) == sorted(p2)}   (different ORDER, same results)")
print(f"    verify vs itertools: "
      f"{sorted(p1) == sorted(list(map(list, itertools.permutations(nums))))}")

print("\n  The decision tree (which unused element comes next):")
print("""                       []
              /         |         \\
            [1]        [2]        [3]
           /   \\      /   \\      /   \\
       [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
         |     |     |     |     |     |
      [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]
""")
print("  -> Subsets branch TWICE per level; permutations branch over the")
print("     REMAINING candidates. Recognising the tree tells you what")
print("     candidates() should return.")

print(f"\n  {'n':>4} {'n! perms':>14} {'time':>10}   the cliff")
print("  " + "-" * 46)
for n in [4, 6, 8, 9, 10]:
    arr = list(range(n))
    start = time.perf_counter()
    res = permutations_used(arr)
    ms = (time.perf_counter() - start) * 1000
    import math
    assert len(res) == math.factorial(n)
    note = "<- getting painful" if n >= 9 else ""
    print(f"  {n:>4} {len(res):>14,} {ms:>8.1f}ms   {note}")
print("\n  -> Subsets stay feasible to n~25. Permutations die around n~11.")
print("     11! = 39,916,800 and 13! = 6.2 billion. Know where the cliff is.")

# ==================== (4) Handling Duplicates ====================
print("\n[4] Handling Duplicates -- the `i > start` Guard")
print("-" * 70)

def subsets_with_dup(nums: List[int]) -> List[List[int]]:
    """Sort, then skip a repeat that is not the first candidate at this level."""
    nums = sorted(nums)               # MANDATORY -- groups equal values
    results = []
    def bt(start, path):
        results.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue              # duplicate AT THIS LEVEL
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return results


def subsets_with_dup_wrong(nums: List[int]) -> List[List[int]]:
    """The over-pruning bug: `i > 0` instead of `i > start`."""
    nums = sorted(nums)
    results = []
    def bt(start, path):
        results.append(path[:])
        for i in range(start, len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:      # BUG
                continue
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return results


dup = [1, 2, 2]
correct = subsets_with_dup(dup)
wrong = subsets_with_dup_wrong(dup)
brute = sorted(set(tuple(sorted(c)) for r in range(len(dup) + 1)
                   for c in itertools.combinations(dup, r)))

print(f"  subsets_with_dup({dup}):")
print(f"    correct (i > start): {correct}   ({len(correct)} results)")
print(f"    buggy   (i > 0)    : {wrong}   ({len(wrong)} results)")
print(f"    brute-force truth  : {[list(t) for t in brute]}   ({len(brute)} results)")
print(f"    correct matches truth: "
      f"{sorted(map(tuple, correct)) == sorted(brute)}")
print(f"    buggy   matches truth: "
      f"{sorted(map(tuple, wrong)) == sorted(brute)}   <- DROPS [2,2]")
print("\n  -> `i > start` means 'not the first candidate at THIS level'.")
print("     `i > 0` also blocks the legitimate second 2 when it follows the")
print("     first one down the tree, so [2,2] never gets generated.")

def permute_unique(nums: List[int]) -> List[List[int]]:
    """The `not used[i-1]` condition is what detects 'same tree level'."""
    nums = sorted(nums)
    results = []
    used = [False] * len(nums)
    def bt(path):
        if len(path) == len(nums):
            results.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            bt(path)
            path.pop()
            used[i] = False
    bt([])
    return results


d2 = [1, 1, 2]
uniq = permute_unique(d2)
truth = sorted(set(itertools.permutations(d2)))
print(f"\n  permute_unique({d2}): {uniq}")
print(f"    count: {len(uniq)}  (3!/2! = 3)")
print(f"    matches itertools set: {sorted(map(tuple, uniq)) == truth}")
print("\n  -> If nums[i-1] IS used, we are deeper in a branch that")
print("     legitimately uses both copies -> allow it.")
print("     If it is NOT used, we are choosing between two identical")
print("     options at the same level -> take only the first.")

# ==================== (5) Combinations ====================
print("\n[5] Combinations and Combination Sum")
print("-" * 70)

def combine(n: int, k: int) -> List[List[int]]:
    """C(n, k) combinations, with a real pruning bound."""
    results = []
    def bt(start, path):
        if len(path) == k:
            results.append(path[:])
            return
        need = k - len(path)
        # PRUNE: stop when too few numbers remain to reach length k
        for i in range(start, n - need + 2):
            path.append(i)
            bt(i + 1, path)
            path.pop()
    bt(1, [])
    return results


def combine_no_prune(n: int, k: int) -> Tuple[List[List[int]], int]:
    """Same result, no pruning bound. Counts nodes visited."""
    results = []
    nodes = 0
    def bt(start, path):
        nonlocal nodes
        nodes += 1
        if len(path) == k:
            results.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            bt(i + 1, path)
            path.pop()
    bt(1, [])
    return results, nodes


def combine_prune_counted(n: int, k: int) -> Tuple[List[List[int]], int]:
    results = []
    nodes = 0
    def bt(start, path):
        nonlocal nodes
        nodes += 1
        if len(path) == k:
            results.append(path[:])
            return
        need = k - len(path)
        for i in range(start, n - need + 2):
            path.append(i)
            bt(i + 1, path)
            path.pop()
    bt(1, [])
    return results, nodes


print(f"  combine(4, 2) = {combine(4, 2)}")
print(f"  count = {len(combine(4, 2))} = C(4,2) = 6")

print(f"\n  Effect of the pruning bound:")
print(f"  {'n, k':>10} {'results':>9} {'nodes (no prune)':>18} {'nodes (pruned)':>16} {'saved':>8}")
print("  " + "-" * 66)
for n, k in [(10, 3), (16, 4), (20, 5)]:
    r_np, nodes_np = combine_no_prune(n, k)
    r_p, nodes_p = combine_prune_counted(n, k)
    assert r_np == r_p
    print(f"  {f'{n}, {k}':>10} {len(r_p):>9,} {nodes_np:>18,} {nodes_p:>16,} "
          f"{(1 - nodes_p / nodes_np) * 100:>7.0f}%")
print("\n  -> Same results, but the saving is only ~5-6%. Be honest about this:")
print("     for combinations the loop bound is a MINOR win, because most of")
print("     the tree already leads to valid output. There is little to prune")
print("     when almost every branch succeeds.")
print("  -> Pruning pays off when most branches FAIL. Compare N-Queens below,")
print("     where validity is rare and pruning cuts 99.99% of the tree.")


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """Unlimited reuse. `break` works because the input is sorted."""
    candidates = sorted(candidates)
    results = []
    def bt(start, path, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                 # PRUNE: sorted -> all later are worse
            path.append(candidates[i])
            bt(i, path, remaining - candidates[i])   # i, not i+1 -> reuse
            path.pop()
    bt(0, [], target)
    return results


def combination_sum2(candidates: List[int], target: int) -> List[List[int]]:
    """Each element used at most once, duplicates in the input."""
    candidates = sorted(candidates)
    results = []
    def bt(start, path, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue              # duplicate at this level
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            bt(i + 1, path, remaining - candidates[i])   # i+1 -> no reuse
            path.pop()
    bt(0, [], target)
    return results


print(f"\n  combination_sum([2,3,6,7], 7)  = {combination_sum([2,3,6,7], 7)}")
print(f"    (2 reused: 2+2+3 = 7)")
print(f"  combination_sum2([10,1,2,7,6,1,5], 8) =")
for c in combination_sum2([10, 1, 2, 7, 6, 1, 5], 8):
    print(f"    {c}  sum = {sum(c)}")
print("\n  -> The ONLY differences: `i` vs `i+1`, and the duplicate guard.")

# ==================== (6) N-Queens ====================
print("\n[6] N-Queens -- Where Pruning Decides Everything")
print("-" * 70)

def solve_n_queens(n: int) -> Tuple[List[List[int]], int]:
    """One queen per row. Three sets make conflict checks O(1)."""
    results = []
    cols: Set[int] = set()
    diag1: Set[int] = set()          # r - c constant along "\"
    diag2: Set[int] = set()          # r + c constant along "/"
    nodes = 0

    def bt(row, path):
        nonlocal nodes
        nodes += 1
        if row == n:
            results.append(path[:])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue                              # PRUNE in O(1)
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            path.append(col)
            bt(row + 1, path)
            path.pop()
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)
    bt(0, [])
    return results, nodes


def solve_n_queens_brute(n: int) -> Tuple[List[List[int]], int]:
    """Validate only at the leaf. Correct, but explores the whole tree."""
    results = []
    nodes = 0

    def valid(path):
        for i in range(len(path)):
            for j in range(i + 1, len(path)):
                if path[i] == path[j] or abs(path[i] - path[j]) == j - i:
                    return False
        return True

    def bt(row, path):
        nonlocal nodes
        nodes += 1
        if row == n:
            if valid(path):
                results.append(path[:])
            return
        for col in range(n):
            path.append(col)
            bt(row + 1, path)
            path.pop()
    bt(0, [])
    return results, nodes


def draw_board(solution: List[int]) -> List[str]:
    n = len(solution)
    return ["".join("Q" if solution[r] == c else "." for c in range(n))
            for r in range(n)]


sols, nodes = solve_n_queens(4)
print(f"  n=4: {len(sols)} solutions, {nodes} nodes explored")
for i, s in enumerate(sols, 1):
    print(f"\n    Solution {i}: {s}")
    for line in draw_board(s):
        print(f"      {line}")

print(f"\n  Pruned vs brute force (validate early vs validate at the leaf):")
print(f"  {'n':>4} {'solutions':>11} {'nodes (pruned)':>16} {'nodes (brute)':>15} {'reduction':>11}")
print("  " + "-" * 62)
for n in [4, 5, 6, 7, 8]:
    sp, np_ = solve_n_queens(n)
    sb, nb = solve_n_queens_brute(n)
    assert sorted(sp) == sorted(sb), f"mismatch at n={n}"
    print(f"  {n:>4} {len(sp):>11} {np_:>16,} {nb:>15,} "
          f"{nb / np_:>10.0f}x")

print("\n  -> Identical solutions, but brute force explores orders of")
print("     magnitude more nodes. At n=8 that is the difference between")
print("     a usable algorithm and an unusable one.")
print("  -> PRUNING IS NOT AN OPTIMISATION. It is what makes backtracking work.")

print(f"\n  Solution counts (growth is brutal):")
print(f"  {'n':>4} {'solutions':>11} {'time':>10}")
print("  " + "-" * 28)
for n in [4, 6, 8, 9, 10]:
    start = time.perf_counter()
    s, _ = solve_n_queens(n)
    ms = (time.perf_counter() - start) * 1000
    print(f"  {n:>4} {len(s):>11,} {ms:>8.1f}ms")

# ==================== (7) Grid Backtracking ====================
print("\n[7] Grid Backtracking -- Word Search")
print("-" * 70)

def exist(board: List[List[str]], word: str) -> bool:
    """Mutate the board to mark visited, then restore. O(1) extra space."""
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])

    def bt(r, c, i):
        if i == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[i]:
            return False

        saved = board[r][c]
        board[r][c] = "#"                          # CHOOSE (mark visited)
        found = (bt(r + 1, c, i + 1) or bt(r - 1, c, i + 1) or
                 bt(r, c + 1, i + 1) or bt(r, c - 1, i + 1))
        board[r][c] = saved                        # UNDO (restore)
        return found

    return any(bt(r, c, 0) for r in range(rows) for c in range(cols))


grid = [list("ABCE"), list("SFCS"), list("ADEE")]
print("  Board:")
for row in grid:
    print(f"    {' '.join(row)}")

print(f"\n  {'word':<10} {'found':>7}")
print("  " + "-" * 20)
for w in ["ABCCED", "SEE", "ABCB", "ASADEESCFB"]:
    before = [r[:] for r in grid]
    found = exist(grid, w)
    restored = grid == before
    print(f"  {w:<10} {str(found):>7}   board restored: {restored}")

print("\n  -> Marking cells in place and restoring them avoids a separate")
print("     visited set. Forget the restore and later start positions see")
print("     a corrupted board -- a silent wrong answer, not a crash.")

# ==================== (8) Sudoku ====================
print("\n[8] Sudoku Solver")
print("-" * 70)

def solve_sudoku(board: List[List[str]]) -> Tuple[bool, int]:
    """Returns (solved, nodes explored)."""
    nodes = 0

    def is_valid(r, c, ch):
        for i in range(9):
            if board[r][i] == ch or board[i][c] == ch:
                return False
            br, bc = 3 * (r // 3) + i // 3, 3 * (c // 3) + i % 3
            if board[br][bc] == ch:
                return False
        return True

    def bt():
        nonlocal nodes
        nodes += 1
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for ch in "123456789":
                        if is_valid(r, c, ch):
                            board[r][c] = ch          # CHOOSE
                            if bt():                  # EXPLORE
                                return True
                            board[r][c] = "."         # UNDO
                    return False    # no digit fits -> caller's choice was wrong
        return True                 # no empty cells -> solved
    solved = bt()
    return solved, nodes


puzzle_str = [
    "53..7....", "6..195...", ".98....6.",
    "8...6...3", "4..8.3..1", "7...2...6",
    ".6....28.", "...419..5", "....8..79",
]
puzzle = [list(row) for row in puzzle_str]

def print_sudoku(b, indent="    "):
    for i, row in enumerate(b):
        if i % 3 == 0 and i:
            print(f"{indent}------+-------+------")
        cells = []
        for j, ch in enumerate(row):
            if j % 3 == 0 and j:
                cells.append("|")
            cells.append(ch)
        print(f"{indent}{' '.join(cells)}")

print("  Puzzle:")
print_sudoku(puzzle)

start = time.perf_counter()
solved, nodes = solve_sudoku(puzzle)
ms = (time.perf_counter() - start) * 1000

print(f"\n  Solved: {solved} in {ms:.1f}ms, {nodes:,} nodes explored")
print_sudoku(puzzle)

# Verify the solution
def valid_sudoku(b) -> bool:
    for i in range(9):
        if sorted(b[i]) != list("123456789"):
            return False
        if sorted(b[r][i] for r in range(9)) != list("123456789"):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box = [b[br + i][bc + j] for i in range(3) for j in range(3)]
            if sorted(box) != list("123456789"):
                return False
    return True

print(f"\n  All rows, columns, and boxes contain 1-9 exactly once: "
      f"{valid_sudoku(puzzle)}")
print("\n  -> The `return False` after the digit loop is backtracking")
print("     propagating failure upward: if no digit fits this cell, the")
print("     CALLER made a wrong choice.")
print("  -> Optimisation worth naming: fill the cell with the FEWEST legal")
print("     candidates next (minimum remaining values). It shrinks the")
print("     branching factor dramatically on hard puzzles.")

# ==================== (9) More Applications of the Same Template ====================
print("\n[9] The Same Template, Five More Problems")
print("-" * 70)

def generate_parenthesis(n: int) -> List[str]:
    """Valid combinations of n pairs. Prune on the open/close counts."""
    results = []
    def bt(path, open_count, close_count):
        if len(path) == 2 * n:
            results.append("".join(path))
            return
        if open_count < n:                     # can still open
            path.append("(")
            bt(path, open_count + 1, close_count)
            path.pop()
        if close_count < open_count:           # can only close what is open
            path.append(")")
            bt(path, open_count, close_count + 1)
            path.pop()
    bt([], 0, 0)
    return results


def letter_combinations(digits: str) -> List[str]:
    """Phone keypad. Branching factor varies per level."""
    if not digits:
        return []
    keypad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
              "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    results = []
    def bt(i, path):
        if i == len(digits):
            results.append("".join(path))
            return
        for ch in keypad[digits[i]]:
            path.append(ch)
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return results


def partition_palindromes(s: str) -> List[List[str]]:
    """Every partition into palindromic substrings."""
    results = []
    def is_pal(sub):
        return sub == sub[::-1]
    def bt(start, path):
        if start == len(s):
            results.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if is_pal(piece):                  # PRUNE: only palindromic cuts
                path.append(piece)
                bt(end, path)
                path.pop()
    bt(0, [])
    return results


def restore_ip_addresses(s: str) -> List[str]:
    """Split into 4 valid octets. Heavy pruning on segment validity."""
    results = []
    def valid(seg):
        if not seg or len(seg) > 3:
            return False
        if seg[0] == "0" and len(seg) > 1:     # no leading zeros
            return False
        return int(seg) <= 255
    def bt(start, path):
        if len(path) == 4:
            if start == len(s):
                results.append(".".join(path))
            return
        for end in range(start + 1, min(start + 4, len(s) + 1)):
            seg = s[start:end]
            if valid(seg):
                path.append(seg)
                bt(end, path)
                path.pop()
    bt(0, [])
    return results


def word_break_all(s: str, word_dict: List[str]) -> List[str]:
    """Every sentence formable from the dictionary."""
    words = set(word_dict)
    results = []
    def bt(start, path):
        if start == len(s):
            results.append(" ".join(path))
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece in words:
                path.append(piece)
                bt(end, path)
                path.pop()
    bt(0, [])
    return results


print(f"  generate_parenthesis(3):")
print(f"    {generate_parenthesis(3)}")
print(f"    count = {len(generate_parenthesis(3))} (Catalan number C_3 = 5)")

print(f"\n  letter_combinations('23'):")
print(f"    {letter_combinations('23')}")

print(f"\n  partition_palindromes('aab'):")
for p in partition_palindromes("aab"):
    print(f"    {p}")

print(f"\n  restore_ip_addresses('25525511135'):")
for ip in restore_ip_addresses("25525511135"):
    print(f"    {ip}")

print(f"\n  word_break_all('catsanddog', ['cat','cats','and','sand','dog']):")
for sent in word_break_all("catsanddog", ["cat", "cats", "and", "sand", "dog"]):
    print(f"    {sent}")

print("\n  -> Five different problems. Same three lines: choose, explore, undo.")
print("     Only is_complete, candidates, and is_valid changed.")

# ==================== (10) Backtracking vs DP ====================
print("\n[10] Backtracking vs DP -- Knowing Which to Reach For")
print("-" * 70)

def count_paths_backtrack(m: int, n: int) -> int:
    """Enumerate every path in an m x n grid. Exponential."""
    count = 0
    def bt(r, c):
        nonlocal count
        if r == m - 1 and c == n - 1:
            count += 1
            return
        if r < m - 1:
            bt(r + 1, c)
        if c < n - 1:
            bt(r, c + 1)
    bt(0, 0)
    return count


def count_paths_dp(m: int, n: int) -> int:
    """Count them. Polynomial."""
    row = [1] * n
    for _ in range(m - 1):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]


print("  Same question -- 'how many paths through an m x n grid?'")
print(f"\n  {'grid':>8} {'paths':>12} {'backtrack':>12} {'DP':>10} {'speedup':>10}")
print("  " + "-" * 56)
for m, n in [(4, 4), (8, 8), (10, 10), (12, 12)]:
    start = time.perf_counter()
    c1 = count_paths_backtrack(m, n)
    t1 = (time.perf_counter() - start) * 1000
    start = time.perf_counter()
    c2 = count_paths_dp(m, n)
    t2 = (time.perf_counter() - start) * 1000
    assert c1 == c2
    print(f"  {f'{m}x{n}':>8} {c1:>12,} {t1:>10.1f}ms {t2:>8.3f}ms "
          f"{t1 / max(t2, 0.0001):>9.0f}x")

print("\n  -> Backtracking VISITS every path; DP COUNTS them without walking.")
print("     If the question asks 'how many' or 'what is the best', use DP.")
print("     If it asks 'list them all' or 'find one valid arrangement',")
print("     use backtracking -- DP cannot produce the arrangements.")

print("\n  The tell:")
print(f"    {'Question phrasing':<38} {'Tool'}")
print("    " + "-" * 52)
for q, tool in [
    ("'list all subsets/permutations'", "backtracking"),
    ("'how many ways'", "DP"),
    ("'find ONE valid board'", "backtracking"),
    ("'maximum/minimum value'", "DP"),
    ("'all sentences from this string'", "backtracking"),
    ("'can it be segmented at all'", "DP"),
]:
    print(f"    {q:<38} {tool}")

# ==================== (11) Recursion Depth ====================
print("\n[11] The Practical Limit: Recursion Depth")
print("-" * 70)

print(f"  Python's default recursion limit: {sys.getrecursionlimit():,}")
print("  Backtracking depth is usually O(n), so this bites when n is large.\n")

def deep_subset_count(n: int) -> Optional[int]:
    """Depth-n recursion. Returns None if it blows the stack."""
    count = 0
    def bt(i):
        nonlocal count
        if i == n:
            count += 1
            return
        bt(i + 1)
    try:
        bt(0)
        return count
    except RecursionError:
        return None

for n in [500, 990, 1500]:
    result = deep_subset_count(n)
    status = f"ok (depth {n})" if result else "RecursionError"
    print(f"    depth {n:>5}: {status}")

print("\n  Fixes, in order of preference:")
print("    1. Reduce the depth (better formulation, stronger pruning)")
print("    2. Convert to an explicit stack (iterative DFS)")
print("    3. sys.setrecursionlimit(N) -- a blunt instrument; you can still")
print("       hit a real C-stack segfault well before Python's limit")

# ==================== (12) Verification Suite ====================
print("\n[12] Verification Against Brute Force / itertools")
print("-" * 70)

import math
checks = {}

# subsets
fails = 0
for n in range(0, 9):
    arr = list(range(n))
    got = sorted(map(tuple, subsets_loop(arr)))
    want = sorted(tuple(c) for r in range(n + 1)
                  for c in itertools.combinations(arr, r))
    if got != want or len(got) != 2 ** n:
        fails += 1
checks["subsets vs itertools"] = fails

# both subset formulations agree
fails = 0
for n in range(0, 9):
    arr = list(range(n))
    a = sorted(map(tuple, map(sorted, subsets_loop(arr))))
    b = sorted(map(tuple, map(sorted, subsets_include_exclude(arr))))
    if a != b:
        fails += 1
checks["subsets: both formulations"] = fails

# permutations
fails = 0
for n in range(0, 7):
    arr = list(range(n))
    got = sorted(map(tuple, permutations_used(arr)))
    want = sorted(itertools.permutations(arr))
    if got != want or len(got) != math.factorial(n):
        fails += 1
checks["permutations vs itertools"] = fails

# permutation swap variant
fails = 0
for n in range(0, 7):
    arr = list(range(n))
    if sorted(map(tuple, permutations_swap(arr))) != sorted(itertools.permutations(arr)):
        fails += 1
checks["permutations: swap variant"] = fails

# subsets with duplicates
fails = 0
import random
random.seed(1)
for _ in range(200):
    arr = [random.randint(1, 4) for _ in range(random.randint(0, 7))]
    got = sorted(map(tuple, subsets_with_dup(arr)))
    want = sorted(set(tuple(sorted(c)) for r in range(len(arr) + 1)
                      for c in itertools.combinations(sorted(arr), r)))
    if got != want:
        fails += 1
checks["subsets_with_dup"] = fails

# permutations with duplicates
fails = 0
for _ in range(200):
    arr = [random.randint(1, 3) for _ in range(random.randint(0, 6))]
    got = sorted(map(tuple, permute_unique(arr)))
    want = sorted(set(itertools.permutations(sorted(arr))))
    if got != want:
        fails += 1
checks["permute_unique"] = fails

# combinations
fails = 0
for n in range(1, 9):
    for k in range(1, n + 1):
        got = sorted(map(tuple, combine(n, k)))
        want = sorted(itertools.combinations(range(1, n + 1), k))
        if got != want or len(got) != math.comb(n, k):
            fails += 1
checks["combine vs itertools"] = fails

# combination sum
fails = 0
for _ in range(150):
    cands = sorted(set(random.randint(2, 9) for _ in range(random.randint(1, 5))))
    target = random.randint(1, 16)
    got = sorted(map(tuple, map(sorted, combination_sum(cands, target))))
    # brute force with replacement, up to target // min(cands) items
    want = set()
    maxlen = target // min(cands) if cands else 0
    for r in range(1, maxlen + 1):
        for combo in itertools.combinations_with_replacement(cands, r):
            if sum(combo) == target:
                want.add(tuple(sorted(combo)))
    if got != sorted(want):
        fails += 1
checks["combination_sum"] = fails

# n-queens: pruned == brute force
fails = 0
for n in range(1, 8):
    a, _ = solve_n_queens(n)
    b, _ = solve_n_queens_brute(n)
    if sorted(a) != sorted(b):
        fails += 1
checks["n_queens: pruned vs brute"] = fails

# known n-queens counts
known = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}
fails = sum(1 for n, cnt in known.items() if len(solve_n_queens(n)[0]) != cnt)
checks["n_queens: known counts"] = fails

# generate_parenthesis == Catalan numbers
def catalan(n):
    return math.comb(2 * n, n) // (n + 1)
fails = sum(1 for n in range(0, 9)
            if len(generate_parenthesis(n)) != catalan(n))
checks["parenthesis == Catalan"] = fails

# word search against brute force on tiny grids
fails = 0
for _ in range(200):
    R, C = random.randint(1, 3), random.randint(1, 3)
    g = [[random.choice("ab") for _ in range(C)] for _ in range(R)]
    w = "".join(random.choice("ab") for _ in range(random.randint(1, 4)))
    got = exist([r[:] for r in g], w)

    # brute force: try every simple path
    def brute(r, c, i, vis):
        if i == len(w):
            return True
        if not (0 <= r < R and 0 <= c < C) or (r, c) in vis or g[r][c] != w[i]:
            return False
        vis.add((r, c))
        # The i == len(w) base case above already handles completion, so
        # no special-casing of the final character is needed here.
        ok = any(brute(r + dr, c + dc, i + 1, vis)
                 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        vis.discard((r, c))
        return ok
    want = any(brute(r, c, 0, set()) for r in range(R) for c in range(C))
    if got != want:
        fails += 1
checks["word search vs brute"] = fails

# palindrome partitioning
fails = 0
for _ in range(150):
    s = "".join(random.choice("ab") for _ in range(random.randint(1, 8)))
    got = partition_palindromes(s)
    # every part must be a palindrome and concatenate back to s
    for part in got:
        if "".join(part) != s or any(p != p[::-1] for p in part):
            fails += 1
            break
    # count check: number of ways == product over palindromic cut DP
    n = len(s)
    ways = [0] * (n + 1)
    ways[0] = 1
    for end in range(1, n + 1):
        for start in range(end):
            piece = s[start:end]
            if piece == piece[::-1]:
                ways[end] += ways[start]
    if len(got) != ways[n]:
        fails += 1
checks["palindrome partitioning"] = fails

print(f"  {'Check':<34} {'Failures':>10}  Verdict")
print("  " + "-" * 56)
for name, f in checks.items():
    print(f"  {name:<34} {f:>10}  {'PASS' if f == 0 else 'FAIL'}")

print("\n-> Every generator cross-checked against itertools or a")
print("   brute-force reference. N-Queens also matched published counts.")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
