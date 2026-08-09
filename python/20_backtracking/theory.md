# Backtracking - Systematic Search with Undo

Master the one template behind permutations, subsets, combinations,
N-Queens, Sudoku, and word search — plus the pruning that makes it viable.

---

## 1. What Backtracking Is

Backtracking is **DFS over a tree of partial solutions**, with one addition:
when a branch fails, you *undo* your last choice and try the next one.

```
Build a solution incrementally.
At each step:
  1. CHOOSE   -- make one candidate choice
  2. EXPLORE  -- recurse to build on it
  3. UNDO     -- retract the choice, so the next candidate starts clean
```

That third step is the entire difference between backtracking and plain
recursion. It's why the same `path` list can be reused across billions of
branches instead of copied at every node.

### The Universal Template

Every problem in this topic is this shape:

```python
def backtrack(state, path, results):
    if is_complete(state, path):
        results.append(path[:])        # COPY -- path keeps mutating
        return

    for choice in candidates(state, path):
        if not is_valid(choice, path):
            continue                   # PRUNE -- never explore this branch

        path.append(choice)            # 1. CHOOSE
        backtrack(state, path, results)  # 2. EXPLORE
        path.pop()                     # 3. UNDO
```

Learn this once. Then every "generate all X" problem becomes a question of
filling in four blanks: `is_complete`, `candidates`, `is_valid`, and what
you append to `results`.

**The `path[:]` copy is mandatory.** Appending `path` itself stores a
reference to a list that will be mutated to empty by the time you return.
This is the single most common backtracking bug.

---

## 2. The Decision Tree

Backtracking explores a tree where each level is one decision.

```
Subsets of [1, 2, 3] -- at each element, "include it or not":

                        []
                  /            \
            include 1        skip 1
              [1]               []
            /     \           /     \
        [1,2]     [1]      [2]      []
        /   \     /  \     /  \    /  \
   [1,2,3][1,2][1,3][1]  [2,3][2] [3] []

8 leaves = 2^3 subsets
```

```
Permutations of [1, 2, 3] -- "which unused element comes next":

                       []
              /         |         \
            [1]        [2]        [3]
           /   \      /   \      /   \
       [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
         |     |     |     |     |     |
      [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]

6 leaves = 3! permutations
```

Notice the shapes differ: subsets branch **twice** at every level (in/out),
permutations branch over **remaining candidates**. Recognising which tree
your problem induces tells you what `candidates()` returns.

---

## 3. Subsets (The Power Set)

Two formulations, both worth knowing.

### Include/Exclude

```python
def subsets(nums):
    """2^n subsets. O(n · 2^n) time (output-bound), O(n) recursion depth."""
    results = []

    def backtrack(i, path):
        if i == len(nums):
            results.append(path[:])
            return
        # Branch 1: exclude nums[i]
        backtrack(i + 1, path)
        # Branch 2: include nums[i]
        path.append(nums[i])
        backtrack(i + 1, path)
        path.pop()

    backtrack(0, [])
    return results
```

### Loop-and-Recurse (generalises better)

```python
def subsets(nums):
    results = []

    def backtrack(start, path):
        results.append(path[:])        # EVERY node is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)     # i+1: never reuse an element
            path.pop()

    backtrack(0, [])
    return results
```

The second form is the one to internalise — it extends directly to
combinations, combination sum, and palindrome partitioning by changing only
the base case and the recursion index.

**Complexity**: O(n · 2ⁿ) — there are 2ⁿ subsets and copying each costs
O(n). You cannot beat this; the *output* is that large.

---

## 4. Permutations

```python
def permutations(nums):
    """n! permutations. O(n · n!) time."""
    results = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            results.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True             # CHOOSE
            path.append(nums[i])
            backtrack(path)            # EXPLORE
            path.pop()                 # UNDO
            used[i] = False            # UNDO
    backtrack([])
    return results
```

### The Swap Variant (O(1) extra space)

```python
def permutations_swap(nums):
    results = []

    def backtrack(start):
        if start == len(nums):
            results.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]   # CHOOSE
            backtrack(start + 1)                          # EXPLORE
            nums[start], nums[i] = nums[i], nums[start]   # UNDO
    backtrack(0)
    return results
```

No `used` array — the array prefix *is* the state. Elegant, but it produces
permutations in a different order and is harder to adapt for duplicates.

---

## 5. Handling Duplicates

This is where most people get stuck. The rule:

> **Sort first, then skip a candidate if it equals the previous one *and*
> the previous one wasn't used at this level.**

### Subsets With Duplicates

```python
def subsets_with_dup(nums):
    nums.sort()                        # MANDATORY -- groups equal values
    results = []

    def backtrack(start, path):
        results.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue               # skip duplicates AT THIS LEVEL
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return results
```

`i > start` is the crucial guard. It means "this isn't the first candidate
I'm trying at this level, and it repeats the previous one — so the subtree
it would generate is identical to one I already explored."

### Permutations With Duplicates

```python
def permute_unique(nums):
    nums.sort()
    results = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            results.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip a duplicate whose identical predecessor is unused,
            # which means we are at the same tree level
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
    backtrack([])
    return results
```

The `not used[i-1]` condition is subtle and worth reasoning through slowly:
if the predecessor *is* used, we're deeper in the tree along a branch that
legitimately uses both copies. If it *isn't* used, we're choosing between
two identical options at the same level — pick only the first.

---

## 6. Combinations and Combination Sum

```python
def combine(n, k):
    """All k-length combinations from 1..n. C(n, k) results."""
    results = []

    def backtrack(start, path):
        if len(path) == k:
            results.append(path[:])
            return
        # PRUNE: not enough numbers left to reach length k
        remaining_needed = k - len(path)
        for i in range(start, n - remaining_needed + 2):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    backtrack(1, [])
    return results
```

That loop bound is a real pruning win: if you need 3 more numbers and only 2
remain, don't even start.

### Combination Sum (unlimited reuse)

```python
def combination_sum(candidates, target):
    candidates.sort()                  # enables the break below
    results = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                  # PRUNE: sorted, so all later are worse
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])   # i, not i+1: reuse
            path.pop()
    backtrack(0, [], target)
    return results
```

Two details: `backtrack(i, ...)` allows reusing the same candidate, and
`break` (not `continue`) works because sorting means everything after is
also too large.

---

## 7. Pruning: What Makes Backtracking Practical

Raw backtracking on N-Queens with n=8 would check 8⁸ ≈ 16.7 million board
states. With pruning it checks about 15,000. **Pruning is not an
optimisation — it's what makes the technique work at all.**

Three kinds:

### Constraint Propagation (reject early)
Check validity *before* recursing, not at the leaf. Rejecting a bad choice
at depth 2 kills an entire subtree.

### Bound Pruning (branch and bound)
If the best possible completion of this partial solution is worse than a
solution you already have, stop.

### Symmetry Breaking
If two branches produce mirror-image solutions, explore only one. For
N-Queens, restricting the first queen to the left half of row 0 nearly
halves the work.

```python
# BAD: validate at the leaf. Explores the whole tree.
def bad(path):
    if len(path) == n:
        if is_valid_board(path):
            results.append(path[:])
        return
    for c in range(n):
        path.append(c)
        bad(path)
        path.pop()

# GOOD: validate before recursing. Cuts subtrees immediately.
def good(path):
    if len(path) == n:
        results.append(path[:])
        return
    for c in range(n):
        if not conflicts(path, c):     # <-- the entire difference
            path.append(c)
            good(path)
            path.pop()
```

---

## 8. N-Queens

Place n queens on an n×n board so none attack each other.

**Key modelling choice**: one queen per row, so a solution is just a list
where `path[r] = c`. That eliminates row conflicts by construction.

```python
def solve_n_queens(n):
    results = []
    cols = set()          # occupied columns
    diag1 = set()         # r - c  (constant along "\" diagonals)
    diag2 = set()         # r + c  (constant along "/" diagonals)

    def backtrack(row, path):
        if row == n:
            results.append(path[:])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue                       # PRUNE in O(1)
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            path.append(col)

            backtrack(row + 1, path)

            path.pop()
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)
    backtrack(0, [])
    return results
```

The three sets are the trick: conflict checking becomes O(1) instead of
O(row). `r - c` is constant along one diagonal direction, `r + c` along the
other — worth drawing on paper once to convince yourself.

**Solution counts**: n=4 → 2, n=6 → 4, n=8 → 92, n=10 → 724, n=12 → 14,200.
Growth is brutal, which is why pruning matters.

---

## 9. Grid Backtracking: Word Search

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def backtrack(r, c, i):
        if i == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[i]:
            return False

        board[r][c] = "#"              # CHOOSE: mark visited in place
        found = (backtrack(r + 1, c, i + 1) or backtrack(r - 1, c, i + 1) or
                 backtrack(r, c + 1, i + 1) or backtrack(r, c - 1, i + 1))
        board[r][c] = word[i]          # UNDO: restore
        return found

    return any(backtrack(r, c, 0) for r in range(rows) for c in range(cols))
```

Mutating the board in place and restoring it is the classic space
optimisation — no separate `visited` set, O(1) extra space beyond recursion.
Just don't forget the restore, or you'll corrupt the input for later
starting positions.

---

## 10. Sudoku Solver

```python
def solve_sudoku(board):
    def is_valid(r, c, ch):
        for i in range(9):
            if board[r][i] == ch or board[i][c] == ch:
                return False
            # 3x3 box containing (r, c)
            br, bc = 3 * (r // 3) + i // 3, 3 * (c // 3) + i % 3
            if board[br][bc] == ch:
                return False
        return True

    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for ch in "123456789":
                        if is_valid(r, c, ch):
                            board[r][c] = ch          # CHOOSE
                            if backtrack():           # EXPLORE
                                return True
                            board[r][c] = "."         # UNDO
                    return False       # no digit works -> this branch is dead
        return True                    # no empty cells -> solved

    backtrack()
```

Note the `return False` after the digit loop: if no digit fits an empty
cell, the *caller's* choice was wrong, so fail upward. That's backtracking
propagating a failure.

**Optimisation worth mentioning**: choose the empty cell with the *fewest*
legal candidates next (minimum remaining values heuristic). It reduces
branching factor dramatically on hard puzzles.

---

## 11. Complexity

Backtracking complexities are usually **output-bound** — you can't beat the
size of what you're generating.

| Problem | Count of results | Time | Space (excl. output) |
|---------|------------------|------|----------------------|
| Subsets | 2ⁿ | O(n · 2ⁿ) | O(n) |
| Permutations | n! | O(n · n!) | O(n) |
| Combinations C(n,k) | C(n,k) | O(k · C(n,k)) | O(k) |
| Combination sum | varies | exponential | O(target) |
| N-Queens | ~O(n!) upper bound | much less with pruning | O(n) |
| Sudoku | 1 | exponential worst case | O(1) |
| Word search | — | O(rows · cols · 4^L) | O(L) |
| Palindrome partitioning | up to 2ⁿ⁻¹ | O(n · 2ⁿ) | O(n) |

**Space is O(depth)** for the recursion stack plus the path — usually O(n),
which is modest. The output dominates memory.

### Why "exponential" isn't automatically disqualifying

For n ≤ 20, 2ⁿ ≈ 1 million — instant. n! explodes faster: 10! = 3.6M,
12! = 479M, 13! = 6.2 billion. Know roughly where the cliff is:

| n | 2ⁿ | n! |
|---|-----|-----|
| 10 | 1,024 | 3,628,800 |
| 15 | 32,768 | 1.3 × 10¹² |
| 20 | 1,048,576 | 2.4 × 10¹⁸ |
| 25 | 33,554,432 | 1.6 × 10²⁵ |

Subsets stay feasible to n≈25. Permutations die around n≈11.

---

## 12. Backtracking vs Dynamic Programming

Both explore a decision space. The difference:

| | Backtracking | DP (Topic 12) |
|---|---|---|
| Goal | enumerate **all** solutions | find the **optimal** value |
| Overlapping subproblems | doesn't exploit them | memoises them |
| Output | list of solutions | one number/answer |
| Complexity | exponential | usually polynomial |
| When | you need the actual arrangements | you need a count or best value |

**The tell**: if the question asks "how many ways" or "what's the maximum",
reach for DP. If it asks "list all the ways" or "find one valid
arrangement", reach for backtracking.

Some problems admit both: Combination Sum enumerated with backtracking, but
"count the combinations" is DP. Word Break has a DP formulation for
feasibility and a backtracking one to list all sentences.

---

## 13. Common Pitfalls

1. **Appending `path` instead of `path[:]`.** You store a reference; by
   return time it's empty. The number-one bug, by a wide margin.
2. **Forgetting to undo.** State leaks into sibling branches and the results
   are silently wrong — not a crash, which makes it worse.
3. **Undoing incompletely.** N-Queens needs all three sets restored; miss
   one and you get too few solutions.
4. **Validating at the leaf instead of before recursing.** Turns a pruned
   search into brute force. Correct but unusably slow.
5. **Wrong recursion index.** `i` reuses the current element, `i + 1` moves
   past it, `start` vs `i` changes whether order matters. Getting this wrong
   turns combinations into permutations or causes infinite recursion.
6. **Not sorting before duplicate handling.** The `nums[i] == nums[i-1]`
   skip only works on sorted input.
7. **`i > 0` instead of `i > start`** in the subsets-with-duplicates guard —
   this over-prunes and drops valid results.
8. **Mutating the input without restoring it** in grid problems, corrupting
   later iterations.
9. **Ignoring recursion depth.** Python's default limit is 1000. Deep
   backtracking on large inputs hits `RecursionError`.
10. **Using backtracking when DP is the answer.** If you only need a count
    or an optimum, enumerating everything is exponentially wasteful.

---

## 14. Key Takeaways

✅ **Backtracking = DFS + undo.** Choose, explore, un-choose.
✅ **One template** covers subsets, permutations, combinations, N-Queens, Sudoku
✅ **`path[:]` when recording** — appending `path` stores a reference that empties
✅ **Pruning is not optional** — it's the difference between 16.7M and 15K states
✅ **Validate before recursing**, never at the leaf
✅ **Sort first for duplicates**, then skip `nums[i] == nums[i-1]` at the same level
✅ **`i` reuses, `i + 1` advances** — the recursion index encodes the problem
✅ **Complexity is output-bound**: 2ⁿ subsets, n! permutations, unavoidable
✅ **Space is O(depth)**, usually O(n) — cheap; the output is what's large
✅ **"List all" → backtracking. "How many / what's best" → DP.**

**Interview Focus**:
- Write the template first, out loud, before filling in problem specifics.
  It signals you have a system rather than a memorised answer.
- State the complexity as output-bound and say why it can't be beaten.
- Point out your pruning explicitly — interviewers are watching for whether
  you validate early or at the leaf.
- For duplicates, explain the `i > start` guard rather than just writing it.
- Mention the DP alternative when the question only asks for a count.
- Draw the decision tree for n=3. Every one of these problems becomes
  obvious once the tree is on the whiteboard.

Next: implement the template once, then watch it solve eight different
problems with only the four blanks changed!
