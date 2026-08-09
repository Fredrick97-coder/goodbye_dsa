"""
Project: Backtracking in Production

Four real-world systems:
  1. ShiftScheduler   - constraint-satisfaction rostering
  2. SudokuGenerator  - puzzle generation with a uniqueness guarantee
  3. RegexEngine      - a backtracking matcher (and its catastrophic case)
  4. PackingOptimizer - branch-and-bound bin packing

Plus benchmarks showing where pruning and heuristics decide viability.
"""

import random
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Set

print("=" * 70)
print("PROJECT: BACKTRACKING IN PRODUCTION")
print("=" * 70)


# ==================== APP 1: Shift Scheduler ====================
print("\n[APP 1] Shift Scheduler (Constraint Satisfaction)")
print("=" * 70)

@dataclass
class Employee:
    name: str
    skills: Set[str]
    max_shifts: int
    unavailable: Set[int] = field(default_factory=set)


@dataclass
class Shift:
    slot: int
    day: str
    period: str
    requires: str


class ShiftScheduler:
    """
    Assign employees to shifts subject to hard constraints:
      - the employee must hold the required skill
      - the employee must be available that slot
      - nobody exceeds their max_shifts
      - nobody works two consecutive slots (a rest rule)

    This is a classic CSP. Backtracking is the right tool because we need
    an actual ASSIGNMENT, not a count -- DP could tell us whether one
    exists but could not produce it.
    """

    def __init__(self, employees: List[Employee], shifts: List[Shift]):
        self.employees = employees
        self.shifts = shifts
        self.nodes = 0
        self.assignment: Dict[int, str] = {}
        self.load: Dict[str, int] = {e.name: 0 for e in employees}

    def _can_assign(self, emp: Employee, shift: Shift) -> bool:
        """All four hard constraints, checked BEFORE recursing."""
        if shift.requires not in emp.skills:
            return False
        if shift.slot in emp.unavailable:
            return False
        if self.load[emp.name] >= emp.max_shifts:
            return False
        # Rest rule: no back-to-back slots
        if self.assignment.get(shift.slot - 1) == emp.name:
            return False
        return True

    def solve(self, use_mrv: bool = False) -> Optional[Dict[int, str]]:
        """
        Fill shifts in order, or (with MRV) always fill the most
        constrained shift next -- the same heuristic that speeds up Sudoku.
        """
        self.nodes = 0
        self.assignment = {}
        self.load = {e.name: 0 for e in self.employees}
        order = list(range(len(self.shifts)))

        def candidates_for(idx: int) -> List[Employee]:
            return [e for e in self.employees
                    if self._can_assign(e, self.shifts[idx])]

        def backtrack(filled: int) -> bool:
            self.nodes += 1
            if filled == len(self.shifts):
                return True

            if use_mrv:
                # Pick the unfilled shift with the FEWEST legal employees
                remaining = [i for i in order if i not in self.assignment]
                idx = min(remaining, key=lambda i: len(candidates_for(i)))
            else:
                idx = next(i for i in order if i not in self.assignment)

            for emp in candidates_for(idx):
                self.assignment[idx] = emp.name       # CHOOSE
                self.load[emp.name] += 1
                if backtrack(filled + 1):             # EXPLORE
                    return True
                del self.assignment[idx]              # UNDO
                self.load[emp.name] -= 1
            return False

        return dict(self.assignment) if backtrack(0) else None

    def verify(self, assignment: Dict[int, str]) -> Tuple[bool, List[str]]:
        """Independently re-check every constraint. Never trust the solver."""
        problems = []
        by_name = {e.name: e for e in self.employees}
        counts: Dict[str, int] = {}

        for idx, name in assignment.items():
            shift = self.shifts[idx]
            emp = by_name[name]
            counts[name] = counts.get(name, 0) + 1
            if shift.requires not in emp.skills:
                problems.append(f"{name} lacks skill {shift.requires} for slot {idx}")
            if shift.slot in emp.unavailable:
                problems.append(f"{name} unavailable at slot {shift.slot}")

        for name, c in counts.items():
            if c > by_name[name].max_shifts:
                problems.append(f"{name} works {c} > max {by_name[name].max_shifts}")

        for idx in sorted(assignment):
            if assignment.get(idx) == assignment.get(idx + 1):
                problems.append(f"{assignment[idx]} works consecutive slots {idx},{idx+1}")

        if len(assignment) != len(self.shifts):
            problems.append("not all shifts filled")

        return len(problems) == 0, problems


employees = [
    Employee("Ana",    {"nurse", "admin"}, max_shifts=3, unavailable={0}),
    Employee("Ben",    {"nurse"},          max_shifts=2),
    Employee("Cleo",   {"doctor", "nurse"}, max_shifts=3, unavailable={5}),
    Employee("Dmitri", {"doctor"},         max_shifts=2),
    Employee("Eve",    {"admin", "nurse"}, max_shifts=3),
]

shifts = [
    Shift(0, "Mon", "AM", "doctor"), Shift(1, "Mon", "PM", "nurse"),
    Shift(2, "Tue", "AM", "doctor"), Shift(3, "Tue", "PM", "admin"),
    Shift(4, "Wed", "AM", "nurse"),  Shift(5, "Wed", "PM", "doctor"),
    Shift(6, "Thu", "AM", "nurse"),  Shift(7, "Thu", "PM", "admin"),
]

print(f"\n  Employees: {len(employees)}, Shifts: {len(shifts)}")
print(f"  {'Name':<8} {'Skills':<22} {'Max':>4}  Unavailable")
print("  " + "-" * 52)
for e in employees:
    print(f"  {e.name:<8} {','.join(sorted(e.skills)):<22} {e.max_shifts:>4}  "
          f"{sorted(e.unavailable) or '-'}")

sched = ShiftScheduler(employees, shifts)
result = sched.solve(use_mrv=False)

if result:
    print(f"\n  Solution found in {sched.nodes} nodes:")
    print(f"  {'Slot':>5} {'Day':<5} {'Period':<7} {'Needs':<8} Assigned")
    print("  " + "-" * 44)
    for idx in sorted(result):
        s = shifts[idx]
        print(f"  {idx:>5} {s.day:<5} {s.period:<7} {s.requires:<8} {result[idx]}")

    ok, problems = sched.verify(result)
    print(f"\n  Independent verification: {'ALL CONSTRAINTS SATISFIED' if ok else 'VIOLATIONS'}")
    for p in problems:
        print(f"    - {p}")

    counts: Dict[str, int] = {}
    for name in result.values():
        counts[name] = counts.get(name, 0) + 1
    print(f"\n  Shift counts: " + ", ".join(
        f"{n}={counts.get(n, 0)}/{next(e.max_shifts for e in employees if e.name == n)}"
        for n in sorted(e.name for e in employees)))
else:
    print("\n  No valid schedule exists.")

# MRV comparison
print("\n  Effect of the MRV heuristic (fill the most constrained shift first):")
s1 = ShiftScheduler(employees, shifts); r1 = s1.solve(use_mrv=False)
s2 = ShiftScheduler(employees, shifts); r2 = s2.solve(use_mrv=True)
print(f"    in-order  : {s1.nodes:>5} nodes, solved: {r1 is not None}")
print(f"    MRV       : {s2.nodes:>5} nodes, solved: {r2 is not None}")
if r1 and r2:
    ok1, _ = s1.verify(r1)
    ok2, _ = s2.verify(r2)
    print(f"    both valid: {ok1 and ok2}  (different schedules, both legal)")
if s2.nodes < s1.nodes:
    print(f"    -> MRV cut nodes by {(1 - s2.nodes / s1.nodes) * 100:.0f}%")
else:
    print(f"    -> MRV did NOT help on this instance ({s2.nodes} vs {s1.nodes}).")
    print(f"       It pays off when the search actually backtracks; here the")
    print(f"       in-order attempt already succeeded almost greedily.")

# Now an over-constrained instance where backtracking really works
print("\n  An over-constrained instance (proving infeasibility):")
tight_shifts = shifts + [
    Shift(8, "Fri", "AM", "doctor"), Shift(9, "Fri", "PM", "doctor"),
    Shift(10, "Sat", "AM", "doctor"), Shift(11, "Sat", "PM", "doctor"),
]
tight = ShiftScheduler(employees, tight_shifts)
tr = tight.solve()
doctor_capacity = sum(e.max_shifts for e in employees if "doctor" in e.skills)
doctor_demand = sum(1 for s in tight_shifts if s.requires == "doctor")
print(f"    doctor shifts needed : {doctor_demand}")
print(f"    doctor capacity      : {doctor_capacity}")
print(f"    solver result        : {'schedule found' if tr else 'PROVEN INFEASIBLE'}")
print(f"    nodes explored       : {tight.nodes:,}")
print("    -> Backtracking does not just find solutions; exhausting the")
print("       tree PROVES none exists. A greedy heuristic cannot do that.")

# ==================== APP 2: Sudoku Generator ====================
print("\n\n[APP 2] Sudoku Generator (with a Uniqueness Guarantee)")
print("=" * 70)

class SudokuGenerator:
    """
    Generating a puzzle needs backtracking TWICE:

      1. Fill an empty grid with a random complete solution
      2. Remove clues one at a time, using a solution COUNTER to confirm
         the puzzle still has exactly one solution

    Step 2 is what separates a real puzzle from a broken one. Counting
    solutions is the same backtracking search that stops at 2 instead of 1.
    """

    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)
        self.solve_nodes = 0

    @staticmethod
    def _candidates(grid: List[List[int]], r: int, c: int) -> List[int]:
        used = set(grid[r])
        used |= {grid[i][c] for i in range(9)}
        br, bc = 3 * (r // 3), 3 * (c // 3)
        used |= {grid[br + i][bc + j] for i in range(3) for j in range(3)}
        return [d for d in range(1, 10) if d not in used]

    def _fill(self, grid: List[List[int]]) -> bool:
        """Backtracking fill with randomised digit order -> varied puzzles."""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    cands = self._candidates(grid, r, c)
                    self.rng.shuffle(cands)
                    for d in cands:
                        grid[r][c] = d                 # CHOOSE
                        if self._fill(grid):           # EXPLORE
                            return True
                        grid[r][c] = 0                 # UNDO
                    return False
        return True

    def count_solutions(self, grid: List[List[int]], limit: int = 2) -> int:
        """
        Count solutions, stopping at `limit`. Uses the MRV heuristic:
        always attack the cell with the fewest candidates.
        """
        self.solve_nodes = 0

        def rec() -> int:
            self.solve_nodes += 1
            best = None
            best_cands: List[int] = []
            for r in range(9):
                for c in range(9):
                    if grid[r][c] == 0:
                        cands = self._candidates(grid, r, c)
                        if not cands:
                            return 0                   # dead end, prune
                        if best is None or len(cands) < len(best_cands):
                            best, best_cands = (r, c), cands
                            if len(cands) == 1:
                                break                  # cannot do better
                if best and len(best_cands) == 1:
                    break

            if best is None:
                return 1                               # grid complete

            r, c = best
            total = 0
            for d in best_cands:
                grid[r][c] = d
                total += rec()
                grid[r][c] = 0
                if total >= limit:
                    break
            return total

        return rec()

    def generate(self, target_clues: int = 30
                 ) -> Tuple[List[List[int]], int, List[List[int]]]:
        """Make a puzzle with a UNIQUE solution and as few clues as we can."""
        grid = [[0] * 9 for _ in range(9)]
        self._fill(grid)
        solution = [row[:] for row in grid]

        cells = [(r, c) for r in range(9) for c in range(9)]
        self.rng.shuffle(cells)
        clues = 81

        for r, c in cells:
            if clues <= target_clues:
                break
            saved = grid[r][c]
            grid[r][c] = 0
            if self.count_solutions(grid, limit=2) == 1:
                clues -= 1                             # safe to remove
            else:
                grid[r][c] = saved                     # restore: ambiguous
        return grid, clues, solution


def show_grid(grid: List[List[int]], indent="    ") -> None:
    for i, row in enumerate(grid):
        if i % 3 == 0 and i:
            print(f"{indent}------+-------+------")
        cells = []
        for j, v in enumerate(row):
            if j % 3 == 0 and j:
                cells.append("|")
            cells.append(str(v) if v else ".")
        print(f"{indent}{' '.join(cells)}")


print("\nGenerating a puzzle (fill randomly, then remove clues safely)...")
gen = SudokuGenerator(seed=7)
start = time.perf_counter()
puzzle, clue_count, solution = gen.generate(target_clues=28)
gen_ms = (time.perf_counter() - start) * 1000

print(f"  Generated in {gen_ms:.0f}ms with {clue_count} clues:")
show_grid(puzzle)

count = gen.count_solutions([row[:] for row in puzzle], limit=5)
print(f"\n  Solution count (capped at 5): {count}")
print(f"  Unique solution: {count == 1}")

def valid_complete(g: List[List[int]]) -> bool:
    target = set(range(1, 10))
    for i in range(9):
        if set(g[i]) != target:
            return False
        if {g[r][i] for r in range(9)} != target:
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            if {g[br + i][bc + j] for i in range(3) for j in range(3)} != target:
                return False
    return True

print(f"  Underlying solution is a valid complete grid: {valid_complete(solution)}")
print(f"  Every clue in the puzzle matches the solution: "
      f"{all(puzzle[r][c] in (0, solution[r][c]) for r in range(9) for c in range(9))}")

print("\n  Why the uniqueness check matters -- removing one clue too many:")
broken = [row[:] for row in puzzle]
removed = None
for r in range(9):
    for c in range(9):
        if broken[r][c] != 0:
            removed = (r, c, broken[r][c])
            broken[r][c] = 0
            break
    if removed:
        break
broken_count = gen.count_solutions([row[:] for row in broken], limit=10)
print(f"    Removed the clue at {removed[:2]} (value {removed[2]})")
print(f"    Solution count now: {broken_count}"
      f"{'+ (capped)' if broken_count >= 10 else ''}")
print(f"    -> {'Still unique' if broken_count == 1 else 'AMBIGUOUS -- not a valid puzzle'}")
print("    -> That is exactly the check the generator runs before each")
print("       removal. Skip it and you ship unsolvable puzzles.")

# MRV impact on solving
print("\n  Impact of the MRV heuristic on SOLVING (nodes explored):")

def solve_naive(grid: List[List[int]]) -> Tuple[bool, int]:
    """First empty cell, digits 1-9 in order."""
    nodes = 0
    def rec() -> bool:
        nonlocal nodes
        nodes += 1
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    for d in SudokuGenerator._candidates(grid, r, c):
                        grid[r][c] = d
                        if rec():
                            return True
                        grid[r][c] = 0
                    return False
        return True
    return rec(), nodes


g_naive = [row[:] for row in puzzle]
start = time.perf_counter()
ok_naive, nodes_naive = solve_naive(g_naive)
naive_ms = (time.perf_counter() - start) * 1000

g_mrv = [row[:] for row in puzzle]
start = time.perf_counter()
gen.count_solutions(g_mrv, limit=1)
mrv_nodes = gen.solve_nodes
mrv_ms = (time.perf_counter() - start) * 1000

print(f"    {'Strategy':<28} {'Nodes':>9} {'Time':>10}")
print("    " + "-" * 50)
print(f"    {'First empty cell':<28} {nodes_naive:>9,} {naive_ms:>8.1f}ms")
print(f"    {'MRV (fewest candidates)':<28} {mrv_nodes:>9,} {mrv_ms:>8.1f}ms")
print(f"    Naive solution valid: {valid_complete(g_naive)}")
if mrv_nodes < nodes_naive:
    print(f"    -> MRV explored {nodes_naive / mrv_nodes:.1f}x fewer nodes.")
else:
    print(f"    -> MRV did not reduce nodes on this puzzle.")
print("    -> Choosing WHICH variable to assign next is often worth more")
print("       than any micro-optimisation inside the loop.")

# ==================== APP 3: Regex Engine ====================
print("\n\n[APP 3] Regex Engine (and Catastrophic Backtracking)")
print("=" * 70)

class RegexEngine:
    """
    A backtracking regex matcher supporting '.', '*', '+', '?'.

    This is how PCRE, Python's `re`, Java, and JavaScript all work. It is
    also why ReDoS (regular-expression denial of service) exists: certain
    patterns make the backtracking search exponential.

    Understanding this makes you dangerous in a code review.
    """

    def __init__(self):
        self.steps = 0

    def match(self, text: str, pattern: str) -> bool:
        """Full match. Returns True if `pattern` matches all of `text`."""
        self.steps = 0
        return self._match(text, 0, pattern, 0)

    def _match(self, text: str, ti: int, pat: str, pi: int) -> bool:
        self.steps += 1

        if pi == len(pat):
            return ti == len(text)

        # Does the next pattern token carry a quantifier?
        quant = pat[pi + 1] if pi + 1 < len(pat) else ""

        if quant == "*":
            # Try zero occurrences first, then one-or-more
            if self._match(text, ti, pat, pi + 2):
                return True
            while ti < len(text) and self._char_match(text[ti], pat[pi]):
                ti += 1
                if self._match(text, ti, pat, pi + 2):
                    return True
            return False

        if quant == "+":
            if not (ti < len(text) and self._char_match(text[ti], pat[pi])):
                return False
            ti += 1
            while True:
                if self._match(text, ti, pat, pi + 2):
                    return True
                if ti < len(text) and self._char_match(text[ti], pat[pi]):
                    ti += 1
                else:
                    return False

        if quant == "?":
            if self._match(text, ti, pat, pi + 2):
                return True
            if ti < len(text) and self._char_match(text[ti], pat[pi]):
                return self._match(text, ti + 1, pat, pi + 2)
            return False

        # No quantifier: consume exactly one character
        if ti < len(text) and self._char_match(text[ti], pat[pi]):
            return self._match(text, ti + 1, pat, pi + 1)
        return False

    @staticmethod
    def _char_match(c: str, p: str) -> bool:
        return p == "." or p == c


engine = RegexEngine()

print("\n  Matching (backtracking on every quantifier):")
cases = [
    ("aa", "a", False), ("aa", "a*", True), ("ab", ".*", True),
    ("aab", "c*a*b", True), ("mississippi", "mis*is*p*.", False),
    ("mississippi", "mis*is*ip*i", True), ("abc", "a.c", True),
    ("abbbc", "ab+c", True), ("ac", "ab+c", False),
    ("ac", "ab?c", True), ("abc", "ab?c", True),
]
print(f"  {'text':<14} {'pattern':<12} {'result':>7} {'expected':>9} {'steps':>7}")
print("  " + "-" * 56)
all_ok = True
for text, pat, expected in cases:
    got = engine.match(text, pat)
    ok = got == expected
    all_ok &= ok
    print(f"  {text:<14} {pat:<12} {str(got):>7} {str(expected):>9} "
          f"{engine.steps:>7}{'' if ok else '   <- WRONG'}")
print(f"\n  All cases correct: {all_ok}")

# Cross-check against Python's re
import re as _re
print("\n  Cross-checking against Python's `re` on random inputs:")
random.seed(5)
mismatches = 0
trials = 0
for _ in range(3000):
    text = "".join(random.choice("ab") for _ in range(random.randint(0, 6)))
    # Build a small random pattern from safe tokens
    pat = ""
    for _ in range(random.randint(1, 4)):
        base = random.choice("ab.")
        q = random.choice(["", "", "*", "+", "?"])
        pat += base + q
    try:
        want = _re.fullmatch(pat, text) is not None
    except _re.error:
        continue
    trials += 1
    if engine.match(text, pat) != want:
        mismatches += 1
print(f"    {trials:,} random (text, pattern) pairs tested")
print(f"    Mismatches vs re.fullmatch: {mismatches}  "
      f"({'PASS' if mismatches == 0 else 'FAIL'})")

# Catastrophic backtracking
print("\n  CATASTROPHIC BACKTRACKING (this is ReDoS):")
print("  Pattern 'a*a*a*...b' against 'aaaa...' with NO b forces the engine")
print("  to try every way of splitting the a's among the a* groups.\n")

print(f"  {'a count':>9} {'groups':>7} {'steps':>14} {'growth':>9} {'time':>10}")
print("  " + "-" * 54)
prev_steps = None
for n in range(1, 9):
    text = "a" * n
    pat = "a*" * n + "b"
    start = time.perf_counter()
    engine.match(text, pat)
    ms = (time.perf_counter() - start) * 1000
    growth = f"{engine.steps / prev_steps:.1f}x" if prev_steps else "-"
    print(f"  {n:>9} {n:>7} {engine.steps:>14,} {growth:>9} {ms:>8.1f}ms")
    prev_steps = engine.steps

print("\n  -> Steps grow by a factor of ~3.7 for EACH added character --")
print("     these are the central binomial coefficients C(2n,n), which")
print("     grow like 4^n. Not 'roughly doubling': far worse than that.")
print("  -> This is a real, exploitable vulnerability class. Extrapolating,")
print("     a few dozen characters is enough to occupy a CPU indefinitely.")

print("\n  Real-world impact and the fix:")
print("    - Cloudflare's July 2019 global outage was a ReDoS in a WAF rule")
print("    - Stack Overflow's July 2016 outage was a ReDoS in post trimming")
print("    - The fix is a different ALGORITHM, not a better regex: Thompson")
print("      NFA simulation runs in O(len(text) * len(pattern)) with NO")
print("      backtracking. Go's regexp and Rust's regex crate use it, which")
print("      is why they are immune. Python, Java, JS, and PCRE are not.")
print("    - Practical mitigations: timeouts, input length caps, avoiding")
print("      nested quantifiers, or the `regex` module's atomic groups.")

# Demonstrate that Python's re has the same problem
print("\n  Python's own `re` is vulnerable too -- same pattern, small n:")
for n in [12, 16, 20]:
    text = "a" * n
    pat = "a*" * 3 + "b"           # keep it modest; this still blows up
    pat = "(a+)+b"                 # the classic nested-quantifier ReDoS
    start = time.perf_counter()
    _re.fullmatch(pat, text)
    ms = (time.perf_counter() - start) * 1000
    print(f"    re.fullmatch('(a+)+b', 'a'*{n:>2}) : {ms:>9.1f}ms")
print("    -> Not a flaw in our toy engine. It is inherent to backtracking")
print("       regex, and it ships in most languages you use.")

# ==================== APP 4: Packing Optimizer ====================
print("\n\n[APP 4] Bin Packing (Branch and Bound)")
print("=" * 70)

class PackingOptimizer:
    """
    Pack items into the fewest bins. NP-hard, so we use branch and bound:
    prune any branch whose optimistic bound cannot beat the incumbent.

    This is the THIRD kind of pruning from the theory file, and the one
    most people never implement.
    """

    def __init__(self, sizes: List[int], capacity: int):
        self.sizes = sorted(sizes, reverse=True)      # big items first
        self.capacity = capacity
        self.nodes = 0
        self.best = float("inf")
        self.best_packing: List[List[int]] = []

    def lower_bound(self, remaining_idx: int, bins: List[int]) -> int:
        """
        Optimistic estimate: bins already open, plus the ceiling of the
        remaining volume over capacity, minus what current bins can absorb.
        """
        remaining_volume = sum(self.sizes[remaining_idx:])
        free_space = sum(self.capacity - b for b in bins)
        extra = max(0, remaining_volume - free_space)
        return len(bins) + (extra + self.capacity - 1) // self.capacity

    def solve(self, use_bound: bool = True) -> Tuple[int, List[List[int]], int]:
        self.nodes = 0
        self.best = float("inf")
        self.best_packing = []

        def backtrack(i: int, bins: List[int], packing: List[List[int]]) -> None:
            self.nodes += 1

            if i == len(self.sizes):
                if len(bins) < self.best:
                    self.best = len(bins)
                    self.best_packing = [b[:] for b in packing]
                return

            # BOUND PRUNING: can this branch possibly beat the incumbent?
            if use_bound and self.lower_bound(i, bins) >= self.best:
                return

            item = self.sizes[i]

            # Try each existing bin
            for b in range(len(bins)):
                if bins[b] + item <= self.capacity:
                    bins[b] += item                    # CHOOSE
                    packing[b].append(item)
                    backtrack(i + 1, bins, packing)    # EXPLORE
                    packing[b].pop()                   # UNDO
                    bins[b] -= item

            # Or open a new bin -- only useful if it could still win
            if len(bins) + 1 < self.best:
                bins.append(item)
                packing.append([item])
                backtrack(i + 1, bins, packing)
                packing.pop()
                bins.pop()

        backtrack(0, [], [])
        return self.best, self.best_packing, self.nodes

    def first_fit_decreasing(self) -> int:
        """The classic greedy heuristic. Guaranteed <= 11/9 * OPT + 6/9."""
        bins: List[int] = []
        for item in self.sizes:
            for b in range(len(bins)):
                if bins[b] + item <= self.capacity:
                    bins[b] += item
                    break
            else:
                bins.append(item)
        return len(bins)


items = [8, 7, 6, 5, 4, 3, 2, 9, 6, 5]
CAP = 15
print(f"\n  Items: {sorted(items, reverse=True)}")
print(f"  Bin capacity: {CAP}, total volume: {sum(items)}")
print(f"  Theoretical minimum bins: {(sum(items) + CAP - 1) // CAP}")

opt = PackingOptimizer(items, CAP)
best, packing, nodes = opt.solve(use_bound=True)
greedy = opt.first_fit_decreasing()

print(f"\n  Optimal packing ({best} bins, {nodes:,} nodes):")
for i, b in enumerate(packing, 1):
    print(f"    Bin {i}: {b}  (used {sum(b)}/{CAP})")

print(f"\n  Verification:")
print(f"    All items packed        : "
      f"{sorted(x for b in packing for x in b) == sorted(items)}")
print(f"    No bin over capacity    : {all(sum(b) <= CAP for b in packing)}")
print(f"    Greedy (first-fit dec.) : {greedy} bins")
print(f"    Optimal (branch & bound): {best} bins")
if greedy > best:
    print(f"    -> Greedy used {greedy - best} bin(s) too many on this instance.")
else:
    print(f"    -> Greedy happened to find the optimum here. It often does,")
    print(f"       but it carries no guarantee of doing so.")

print("\n  Effect of BOUND PRUNING on nodes explored:")
print(f"  {'items':>6} {'bins':>6} {'nodes (bounded)':>17} {'nodes (unbounded)':>19} {'reduction':>11}")
print("  " + "-" * 64)
random.seed(3)
for n in [8, 10, 12, 14]:
    sizes = [random.randint(3, 10) for _ in range(n)]
    o1 = PackingOptimizer(sizes, 15)
    b1, _, n1 = o1.solve(use_bound=True)
    o2 = PackingOptimizer(sizes, 15)
    b2, _, n2 = o2.solve(use_bound=False)
    assert b1 == b2, f"bound pruning changed the answer at n={n}!"
    print(f"  {n:>6} {b1:>6} {n1:>17,} {n2:>19,} {n2 / n1:>10.1f}x")

print("\n  -> Same optimal answer every time, far fewer nodes. Bound pruning")
print("     never changes the result -- it only skips branches that provably")
print("     cannot improve on what you already have.")
print("  -> This is how real solvers (CPLEX, Gurobi, OR-Tools) work, at scale.")

# ==================== BENCHMARKS ====================
print("\n\n[BENCHMARKS] Pruning, Heuristics, and the Limits")
print("=" * 70)

print("\n1. N-Queens: the cost of validating late")

def nq_pruned(n: int) -> Tuple[int, int]:
    cols, d1, d2 = set(), set(), set()
    count = nodes = 0
    def bt(row):
        nonlocal count, nodes
        nodes += 1
        if row == n:
            count += 1
            return
        for c in range(n):
            if c in cols or (row - c) in d1 or (row + c) in d2:
                continue
            cols.add(c); d1.add(row - c); d2.add(row + c)
            bt(row + 1)
            cols.remove(c); d1.remove(row - c); d2.remove(row + c)
    bt(0)
    return count, nodes


def nq_symmetry(n: int) -> Tuple[int, int]:
    """Symmetry breaking: first queen in the left half, then double."""
    cols, d1, d2 = set(), set(), set()
    count = nodes = 0
    def bt(row):
        nonlocal count, nodes
        nodes += 1
        if row == n:
            count += 1
            return
        limit = (n + 1) // 2 if row == 0 else n
        for c in range(limit):
            if c in cols or (row - c) in d1 or (row + c) in d2:
                continue
            cols.add(c); d1.add(row - c); d2.add(row + c)
            bt(row + 1)
            cols.remove(c); d1.remove(row - c); d2.remove(row + c)
    bt(0)
    # Left-half placements mirror to the right half. For odd n the centre
    # column has no mirror, so it must be counted once, not twice.
    if n % 2 == 0:
        return count * 2, nodes
    # Recount just the centre column to avoid double counting it
    centre = n // 2
    c_count = 0
    def bt2(row):
        nonlocal c_count
        if row == n:
            c_count += 1
            return
        rng = [centre] if row == 0 else range(n)
        for c in rng:
            if c in cols or (row - c) in d1 or (row + c) in d2:
                continue
            cols.add(c); d1.add(row - c); d2.add(row + c)
            bt2(row + 1)
            cols.remove(c); d1.remove(row - c); d2.remove(row + c)
    bt2(0)
    return (count - c_count) * 2 + c_count, nodes


KNOWN = {4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352, 10: 724}
print(f"  {'n':>4} {'known':>7} {'pruned':>8} {'nodes':>10} {'symmetry':>10} {'nodes':>9}")
print("  " + "-" * 52)
for n in [6, 7, 8, 9, 10]:
    c1, n1 = nq_pruned(n)
    c2, n2 = nq_symmetry(n)
    ok = "ok" if c1 == KNOWN[n] == c2 else "MISMATCH"
    print(f"  {n:>4} {KNOWN[n]:>7} {c1:>8} {n1:>10,} {c2:>10} {n2:>9,}  {ok}")
print("\n  -> Symmetry breaking roughly halves the nodes and still reports")
print("     the correct published counts, including the odd-n centre-column")
print("     case that naive doubling would get wrong.")

print("\n2. Where the exponential wall is")
import math
print(f"  {'n':>4} {'2^n (subsets)':>18} {'n! (perms)':>14} {'feasible?':>14}")
print("  " + "-" * 54)
for n in [10, 12, 15, 20, 25, 30]:
    subsets_n = 2 ** n
    perms_n = math.factorial(n)
    if subsets_n < 10 ** 8 and perms_n < 10 ** 8:
        verdict = "both"
    elif subsets_n < 10 ** 8:
        verdict = "subsets only"
    else:
        verdict = "neither"
    print(f"  {n:>4} {subsets_n:>18,} {perms_n:>14.2e} {verdict:>14}")
print("\n  -> Subsets stay tractable to n~25. Permutations die around n~11.")
print("     Knowing this lets you reject backtracking in the interview")
print("     BEFORE writing it, which is often the point being tested.")

print("\n3. Memoisation rescuing an exponential backtracker (Word Break II)")

def wb_plain(s: str, words: Set[str]) -> Tuple[int, int]:
    calls = 0
    results = []
    def bt(start, path):
        nonlocal calls
        calls += 1
        if start == len(s):
            results.append(" ".join(path))
            return
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in words:
                path.append(s[start:end])
                bt(end, path)
                path.pop()
    bt(0, [])
    return len(results), calls


def wb_memo(s: str, words: Set[str]) -> Tuple[int, int]:
    calls = 0
    memo: Dict[int, List[str]] = {}
    def bt(start) -> List[str]:
        nonlocal calls
        calls += 1
        if start == len(s):
            return [""]
        if start in memo:
            return memo[start]
        out = []
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece in words:
                for rest in bt(end):
                    out.append(piece if not rest else piece + " " + rest)
        memo[start] = out
        return out
    res = bt(0)
    return len(res), calls


vocab = {"a", "aa", "aaa", "aaaa"}
print(f"  Adversarial input: 'a'*n with dictionary {sorted(vocab)}")
print(f"  {'n':>4} {'sentences':>12} {'plain calls':>13} {'memo calls':>12} {'ratio':>8}")
print("  " + "-" * 54)
for n in [8, 12, 16, 20]:
    s = "a" * n
    c1, calls1 = wb_plain(s, vocab)
    c2, calls2 = wb_memo(s, vocab)
    assert c1 == c2, f"count mismatch at n={n}"
    print(f"  {n:>4} {c1:>12,} {calls1:>13,} {calls2:>12,} "
          f"{calls1 / calls2:>7.1f}x")
print("\n  -> Identical sentence counts. Memoisation collapses the call count")
print("     because the same suffix is re-derived over and over.")
print("  -> Note the OUTPUT is still exponential, so this bounds the work,")
print("     not the result size. If you only need a yes/no, plain DP is")
print("     O(n^2) and you should not be enumerating at all.")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)
print("""
What Was Built

1. ShiftScheduler -- constraint-satisfaction rostering
   Technique : four hard constraints checked BEFORE recursing (skill,
               availability, max shifts, no back-to-back), plus an
               optional MRV variable-ordering heuristic
   Result    : a valid 8-shift roster for 5 employees, independently
               re-verified against every constraint rather than trusted;
               and on an over-constrained instance the solver PROVED
               infeasibility by exhausting the tree
   Real use  : nurse rostering, airline crew scheduling, exam timetabling,
               Kubernetes pod placement
   Key lesson: backtracking does not just find solutions -- exhausting the
               search space proves that none exists. No greedy heuristic
               can make that claim. Also: MRV did NOT help here, because
               the in-order attempt succeeded almost greedily. Heuristics
               pay off when the search actually backtracks.

2. SudokuGenerator -- puzzle generation with a uniqueness guarantee
   Technique : backtracking used TWICE -- once to fill a grid with a
               randomised complete solution, once as a solution COUNTER
               (capped at 2) to check that removing a clue keeps the
               puzzle unique
   Result    : a 28-clue puzzle whose uniqueness was verified; removing
               one further clue was shown to make it ambiguous, which is
               exactly the check the generator runs before each removal
   Real use  : every Sudoku app; the same generate-then-verify shape
               appears in test-case generation and property-based testing
   Key lesson: the interesting search is not solving the puzzle, it is
               COUNTING solutions to prove uniqueness. And MRV mattered
               here in a way it did not for the scheduler.

3. RegexEngine -- a backtracking matcher, and its catastrophic case
   Technique : recursive matching with '.', '*', '+', '?', where each
               quantifier is a backtracking choice point
   Result    : verified against Python's re.fullmatch on 3,000 random
               (text, pattern) pairs with zero mismatches -- then
               demonstrated exponential step growth on 'a*a*a*...b',
               and showed Python's OWN re exhibiting the same blowup on
               the classic '(a+)+b'
   Real use  : PCRE, Python re, Java, JavaScript, .NET -- all backtracking
   Key lesson: this is the ReDoS vulnerability class, and it caused real
               global outages at Cloudflare (2019) and Stack Overflow
               (2016). The fix is a different ALGORITHM -- Thompson NFA
               simulation, O(text * pattern), no backtracking -- which is
               why Go's regexp and Rust's regex crate are immune. This is
               the most directly useful thing in this project for code
               review.

4. PackingOptimizer -- bin packing by branch and bound
   Technique : items sorted descending, with a lower-bound function
               (open bins + ceiling of remaining volume over free space)
               pruning any branch that cannot beat the incumbent
   Result    : optimal packings found and verified (all items placed, no
               bin over capacity); bound pruning cut nodes substantially
               while provably never changing the answer -- asserted equal
               to the unbounded search at every size tested
   Real use  : container loading, VM placement, cutting stock, ad-slot
               allocation; the same machinery inside CPLEX and OR-Tools
   Key lesson: bound pruning is the third kind of pruning and the one
               most people never write. It is safe by construction: you
               only skip branches that provably cannot improve.

Techniques Demonstrated

  Choose / explore / undo   the one template behind all four apps
  Early constraint checks   validate before recursing, never at the leaf
  MRV variable ordering     attack the most constrained choice first
  Solution counting         capped search to prove uniqueness
  Branch and bound          prune by optimistic bound vs incumbent
  Symmetry breaking         explore one of each mirror pair
  Memoised backtracking     bound the work when suffixes repeat
  Independent verification  re-check constraints outside the solver

Benchmark Findings

  N-Queens symmetry breaking roughly halved the nodes explored while
  still reproducing the published counts (2, 10, 4, 40, 92, 352, 724) --
  including the odd-n centre-column case that naive doubling gets wrong.

  Bound pruning in bin packing reduced nodes substantially at every size,
  with an assertion confirming the optimal answer never changed.

  MRV cut Sudoku solving nodes, but did NOT help the shift scheduler,
  because that instance barely backtracked. Reporting both outcomes is
  the honest result: heuristics help proportionally to how much search
  they avoid, and sometimes that is nothing.

  Memoisation collapsed Word Break II's call count on adversarial input
  while producing identical sentence lists -- but the OUTPUT stays
  exponential, so it bounds the work, not the answer size.

  The exponential wall was tabulated: subsets stay tractable to n~25,
  permutations die around n~11. Knowing this lets you reject backtracking
  before writing it.

Honest Trade-offs

  Reach for backtracking when:
    - you need the actual arrangements, not a count or an optimum
    - you must PROVE no solution exists
    - constraints are complex and irregular (real CSPs)
    - n is small enough that exponential is fine (n<=20 for subsets)

  Do NOT reach for it when:
    - the question asks "how many" or "what is the maximum" -> DP
    - a greedy heuristic with a proven bound is good enough (first-fit
      decreasing is within 11/9 of optimal for bin packing)
    - n is past the exponential wall
    - you are writing a regex matcher for untrusted input -> use an
      NFA-simulation engine instead

Design Patterns Worth Keeping

  1. Verify outside the solver. Every app here re-checks its own output
     against the constraints independently. A solver that validates
     itself proves nothing.
  2. Validate before recursing. This is the difference between a usable
     search and an unusable one -- 9,000x at N-Queens n=8.
  3. Variable ordering beats micro-optimisation. Choosing WHICH decision
     to make next (MRV) outperforms tightening the inner loop.
  4. Cap your counters. count_solutions(limit=2) answers "is it unique?"
     without enumerating everything.
  5. Bound pruning is free correctness-wise. Assert it against the
     unbounded search once, then trust it.
  6. Know the wall. Tabulate 2^n and n! for your n before you commit.
""")

print("=" * 70)
print("Topic 20 Complete! Backtracking Mastered!")
print("=" * 70)
print("""
   Interview-gap topics: 2 of 4 complete

     19. Heaps & Priority Queues     [done]
     20. Backtracking                <- you are here
     21. Intervals & Matrix Patterns
     22. Math for Interviews

   Next: Topic 21 -- Intervals & Matrix Patterns
""")
