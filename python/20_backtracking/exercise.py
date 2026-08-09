"""
Exercises: Backtracking

One template, twenty-two problems. Fill in the four blanks each time:
is_complete, candidates, is_valid, and what you record.
"""

from typing import List, Tuple, Set, Optional

print("=" * 70)
print("EXERCISES: Backtracking")
print("=" * 70)
print("""
THE TEMPLATE -- write this from memory before you start:

    def backtrack(state, path, results):
        if is_complete(path):
            results.append(path[:])          # COPY, not the reference
            return
        for choice in candidates(state, path):
            if not is_valid(choice, path):
                continue                     # PRUNE
            path.append(choice)              # 1. CHOOSE
            backtrack(state, path, results)  # 2. EXPLORE
            path.pop()                       # 3. UNDO
""")

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. SUBSETS (THE POWER SET)")
print("Input: A list of distinct integers")
print("Output: All 2^n subsets")
print("Example: [1,2,3] -> [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]")
def subsets(nums: List[int]) -> List[List[int]]:
    # TODO: Loop-and-recurse form. Record path[:] at EVERY node -- every
    # partial path is itself a valid subset. Recurse with i + 1 so no
    # element is reused.
    # Write it the include/exclude way too, then compare. The loop form
    # generalises to combinations; the include/exclude form does not.
    pass

print("\n2. PERMUTATIONS")
print("Input: A list of distinct integers")
print("Output: All n! orderings")
print("Example: [1,2,3] -> 6 permutations")
def permutations(nums: List[int]) -> List[List[int]]:
    # TODO: Keep a `used` array. Record only when len(path) == len(nums).
    # Remember to undo BOTH the path append and the used flag -- forgetting
    # one leaks state into sibling branches and silently returns wrong
    # results (no crash, which is worse).
    pass

print("\n3. COMBINATIONS")
print("Input: n and k")
print("Output: All k-length combinations drawn from 1..n")
print("Example: n=4, k=2 -> [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]")
def combine(n: int, k: int) -> List[List[int]]:
    # TODO: Base case is len(path) == k. Add the pruning bound: if you
    # still need `need` more numbers, stop the loop at n - need + 2.
    # Measure the node count with and without it -- for combinations the
    # saving is modest (~5%), because most branches succeed anyway.
    pass

print("\n4. GENERATE PARENTHESES")
print("Input: n pairs of parentheses")
print("Output: All valid combinations")
print("Example: n=3 -> ['((()))','(()())','(())()','()(())','()()()']")
def generate_parenthesis(n: int) -> List[str]:
    # TODO: No is_valid check needed -- prune structurally instead.
    # You may open while open_count < n, and may close only while
    # close_count < open_count. That makes every generated string valid
    # by construction. The count should equal the nth Catalan number.
    pass

print("\n5. LETTER COMBINATIONS OF A PHONE NUMBER")
print("Input: A digit string like '23'")
print("Output: Every letter combination")
print("Example: '23' -> ['ad','ae','af','bd','be','bf','cd','ce','cf']")
def letter_combinations(digits: str) -> List[str]:
    # TODO: One level per digit; the branching factor varies (3 or 4).
    # Guard the empty input -- it should return [], not ['']
    pass

print("\n6. BINARY WATCH / BINARY STRINGS OF LENGTH n")
print("Input: n")
print("Output: Every binary string of length n")
print("Example: n=2 -> ['00','01','10','11']")
def binary_strings(n: int) -> List[str]:
    # TODO: The simplest possible backtracking: two candidates per level.
    # Use this one to check your template is right before moving on.
    pass


# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n7. SUBSETS WITH DUPLICATES")
print("Input: A list that may contain repeats")
print("Output: All UNIQUE subsets")
print("Example: [1,2,2] -> [[],[1],[1,2],[1,2,2],[2],[2,2]]")
def subsets_with_dup(nums: List[int]) -> List[List[int]]:
    # TODO: SORT FIRST -- the duplicate skip only works on sorted input.
    # Then skip when `i > start and nums[i] == nums[i-1]`.
    # It must be `i > start`, NOT `i > 0`. `i > 0` over-prunes and drops
    # [2,2] entirely. Verify against a set-of-sorted-tuples brute force.
    pass

print("\n8. PERMUTATIONS WITH DUPLICATES")
print("Input: A list that may contain repeats")
print("Output: All UNIQUE permutations")
print("Example: [1,1,2] -> [[1,1,2],[1,2,1],[2,1,1]]")
def permute_unique(nums: List[int]) -> List[List[int]]:
    # TODO: Sort, then skip when
    #   nums[i] == nums[i-1] and not used[i-1]
    # Reason it through slowly: if the predecessor IS used we are deeper
    # in a branch legitimately consuming both copies. If it is NOT used
    # we are choosing between identical options at the same level, so
    # only the first should proceed.
    pass

print("\n9. COMBINATION SUM (UNLIMITED REUSE)")
print("Input: Distinct candidates and a target")
print("Output: All combinations summing to target; elements may repeat")
print("Example: [2,3,6,7], 7 -> [[2,2,3],[7]]")
def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    # TODO: Sort, then recurse with `i` (not i + 1) to allow reuse.
    # Because the input is sorted you can `break` -- not `continue` --
    # once candidates[i] > remaining. Every later candidate is also too big.
    pass

print("\n10. COMBINATION SUM II (EACH ELEMENT ONCE, INPUT HAS DUPLICATES)")
print("Input: Candidates with repeats, and a target")
print("Output: Unique combinations, each element used at most once")
print("Example: [10,1,2,7,6,1,5], 8 -> [[1,1,6],[1,2,5],[1,7],[2,6]]")
def combination_sum2(candidates: List[int], target: int) -> List[List[int]]:
    # TODO: Combine the two ideas: recurse with i + 1 (no reuse) AND
    # apply the `i > start` duplicate skip. Note how little changes
    # between problems 9 and 10 -- that is the template working.
    pass

print("\n11. PALINDROME PARTITIONING")
print("Input: A string")
print("Output: Every partition into palindromic substrings")
print("Example: 'aab' -> [['a','a','b'],['aa','b']]")
def partition_palindromes(s: str) -> List[List[str]]:
    # TODO: Candidates are the prefixes s[start:end]. Only recurse when
    # the prefix is a palindrome -- that IS the pruning.
    # Optimisation to mention: precompute an is_palindrome DP table so
    # each check is O(1) instead of O(n).
    pass

print("\n12. RESTORE IP ADDRESSES")
print("Input: A digit string")
print("Output: Every valid IP address formable by inserting three dots")
print("Example: '25525511135' -> ['255.255.11.135','255.255.111.35']")
def restore_ip_addresses(s: str) -> List[str]:
    # TODO: Exactly 4 segments, each 1-3 digits, value <= 255, and no
    # leading zeros (so '01' is invalid but '0' is fine). Prune hard: the
    # segment length cap alone kills most of the tree.
    pass

print("\n13. WORD SEARCH")
print("Input: A character grid and a word")
print("Output: True if the word can be traced through adjacent cells")
print("Example: cells may not be reused within one path")
def exist(board: List[List[str]], word: str) -> bool:
    # TODO: DFS from every cell. Mark the current cell (e.g. set it to '#')
    # before recursing and RESTORE it afterwards -- that gives you the
    # visited set for free at O(1) extra space.
    # Forgetting the restore corrupts the board for later start positions,
    # producing a silent wrong answer.
    pass

print("\n14. SUBSET SUM / TARGET SUM PARTITION")
print("Input: A list and a target")
print("Output: True if some subset sums to target; also return one witness")
print("Example: [3,34,4,12,5,2], 9 -> True, [4,5]")
def subset_sum(nums: List[int], target: int) -> Tuple[bool, Optional[List[int]]]:
    # TODO: Backtracking finds the actual SUBSET. Note that if you only
    # need the boolean, DP is O(n * target) and far better -- state that
    # trade-off explicitly. Backtracking earns its place by producing the
    # witness.
    pass


# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n15. N-QUEENS")
print("Input: n")
print("Output: All valid placements of n non-attacking queens")
print("Example: n=4 -> 2 solutions; n=8 -> 92")
def solve_n_queens(n: int) -> List[List[int]]:
    # TODO: Model one queen PER ROW, so a solution is a list where
    # path[r] = c. That removes row conflicts by construction.
    # Track three sets for O(1) conflict checks:
    #   cols, diag1 = r - c, diag2 = r + c
    # Draw a board and confirm r-c and r+c are constant along the two
    # diagonal directions before you trust it.
    # Undo ALL THREE sets. Missing one gives too few solutions.
    # Verify against the known counts: 1,0,0,2,10,4,40,92,352
    pass

print("\n16. N-QUEENS II (COUNT ONLY) WITH SYMMETRY BREAKING")
print("Input: n")
print("Output: The NUMBER of solutions")
print("Example: exploit mirror symmetry to nearly halve the work")
def total_n_queens(n: int) -> int:
    # TODO: First do the naive count. Then break symmetry: restrict the
    # first queen to the left half of row 0 and double the tally (handling
    # the centre column separately when n is odd).
    # Measure the node count both ways and report the reduction.
    pass

print("\n17. SUDOKU SOLVER")
print("Input: A 9x9 grid with '.' for blanks")
print("Output: The grid solved in place")
print("Example: return False upward when no digit fits a cell")
def solve_sudoku(board: List[List[str]]) -> bool:
    # TODO: Find an empty cell, try '1'..'9', recurse, undo on failure.
    # The `return False` after the digit loop is the important line: it
    # tells the CALLER its choice was wrong.
    # Then add the minimum-remaining-values heuristic -- always fill the
    # empty cell with the FEWEST legal candidates next. Compare node
    # counts on a hard puzzle; the difference is large.
    pass

print("\n18. WORD SEARCH II (MANY WORDS AT ONCE)")
print("Input: A grid and a list of words")
print("Output: Every word present in the grid")
print("Example: running problem 13 per word is wasteful")
def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    # TODO: Build a TRIE of the words (Topic 18), then DFS the grid ONCE,
    # walking the trie in lockstep. Prune the instant the current prefix
    # leaves the trie.
    # This is the payoff for having done Topic 18: k separate searches
    # become one traversal.
    pass

print("\n19. WORD BREAK II (ALL SENTENCES)")
print("Input: A string and a dictionary")
print("Output: Every sentence formable by inserting spaces")
print("Example: 'catsanddog' -> ['cat sand dog','cats and dog']")
def word_break_all(s: str, word_dict: List[str]) -> List[str]:
    # TODO: Straight backtracking works but can blow up on adversarial
    # input like 'aaaa...a' with dictionary ['a','aa','aaa'].
    # Fix: MEMOISE on the start index, caching the list of suffix
    # sentences. That is backtracking plus DP, and it is the intended
    # solution. Test the pathological case to see why.
    pass

print("\n20. EXPRESSION ADD OPERATORS")
print("Input: A digit string and a target")
print("Output: Every way to insert +, -, * to reach the target")
print("Example: '123', 6 -> ['1*2*3','1+2+3']")
def add_operators(num: str, target: int) -> List[str]:
    # TODO: The hard part is MULTIPLICATION PRECEDENCE. Carry both the
    # running total and the LAST TERM; to apply '*', subtract the last
    # term and re-add it multiplied.
    # Also reject operands with leading zeros ('05'), and remember the
    # first number takes no operator.
    pass


# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n21. KNIGHT'S TOUR")
print("Input: Board size n")
print("Output: A path visiting every square exactly once")
print("Example: naive backtracking is hopeless past n=6")
def knights_tour(n: int) -> Optional[List[Tuple[int, int]]]:
    # TODO: Plain backtracking works for n=5 and dies for n=8.
    # Then add WARNSDORFF'S HEURISTIC: always move to the square with the
    # fewest onward moves. That turns an intractable search into a nearly
    # straight-line walk.
    # Implement both and compare node counts. This is the clearest
    # demonstration in the whole topic that heuristics beat raw search.
    pass

print("\n22. GRAPH COLOURING (m-COLOURABILITY)")
print("Input: An adjacency matrix and m colours")
print("Output: A valid colouring, or None")
print("Example: the classic NP-complete decision problem")
def graph_colouring(graph: List[List[int]], m: int) -> Optional[List[int]]:
    # TODO: Colour vertices one at a time; a colour is legal if no
    # neighbour already has it. Order vertices by DESCENDING DEGREE for a
    # large practical speedup -- constrain the hardest vertices first.
    pass

print("\n23. CRYPTARITHMETIC PUZZLE")
print("Input: Words and a result word, e.g. SEND + MORE = MONEY")
print("Output: A digit assignment making the arithmetic true")
print("Example: distinct digits per letter, no leading zeros")
def solve_cryptarithm(words: List[str], result: str) -> Optional[dict]:
    # TODO: Assign digits to the distinct letters. Naive assignment then
    # checking is 10^k; instead prune COLUMN BY COLUMN from the least
    # significant digit, verifying the partial sum and carry as you go.
    # That is constraint propagation, and it is the difference between
    # seconds and hours.
    pass

print("\n24. GENERATE ALL VALID BST SHAPES")
print("Input: n")
print("Output: Every structurally unique BST holding 1..n")
print("Example: n=3 -> 5 trees (the Catalan numbers again)")
def generate_trees(n: int):
    # TODO: For each root value, recursively generate all left subtrees
    # from the smaller values and all right subtrees from the larger ones,
    # then take the cross product.
    # The count is the nth Catalan number -- the same sequence as
    # generate_parenthesis, which is not a coincidence. Explain why.
    pass

print("\n25. SUBSET SUM WITH BRANCH AND BOUND")
print("Input: Weights, values, and a capacity (0/1 knapsack)")
print("Output: The optimal value, found by pruning rather than DP")
print("Example: compare node counts against the Topic 12 DP solution")
def knapsack_branch_and_bound(weights: List[int], values: List[int],
                              capacity: int) -> int:
    # TODO: Sort by value/weight ratio descending. At each node compute an
    # upper BOUND on what this branch could still achieve (the fractional
    # knapsack relaxation from Topic 15). If the bound is no better than
    # the best solution found so far, PRUNE the whole subtree.
    # This is branch and bound: the third kind of pruning from the theory
    # file. Compare against the O(n*W) DP and state when each wins.
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Backtracking Cheat Sheet:

1. What It Is:
   DFS over a tree of partial solutions, with an UNDO step.

     CHOOSE  -> make a candidate choice
     EXPLORE -> recurse
     UNDO    -> retract it, so the next candidate starts clean

   The undo is the whole difference from plain recursion. It is why one
   `path` list can serve billions of branches instead of being copied.

2. The Template (write it from memory):

     def backtrack(state, path, results):
         if is_complete(path):
             results.append(path[:])          # COPY
             return
         for choice in candidates(state, path):
             if not is_valid(choice, path):
                 continue                     # PRUNE
             path.append(choice)              # CHOOSE
             backtrack(state, path, results)  # EXPLORE
             path.pop()                       # UNDO

   Every problem here fills four blanks: is_complete, candidates,
   is_valid, and what gets recorded.

3. THE #1 BUG -- results.append(path) instead of path[:]:
   You store a REFERENCE to a list that the undo steps will empty. You
   get N copies of []. It is not a crash, so it slips through.

4. Recognise the Tree Shape:
   Subsets      branch TWICE per level (include / exclude), 2^n leaves
   Permutations branch over REMAINING candidates, n! leaves
   Combinations branch forward only from `start`, C(n,k) leaves

   Drawing the tree for n=3 makes every one of these obvious. Do it on
   the whiteboard before writing code.

5. The Recursion Index Encodes the Problem:
     backtrack(i, ...)      element may be REUSED     (combination sum)
     backtrack(i + 1, ...)  element consumed, move on (combinations)
     loop from `start`      order does NOT matter     (subsets)
     loop from 0 + `used`   order DOES matter         (permutations)

   Getting this wrong silently turns combinations into permutations, or
   causes infinite recursion.

6. Duplicates -- SORT FIRST, then skip at the same level:

   Subsets/combinations:
     if i > start and nums[i] == nums[i-1]: continue

   Permutations:
     if nums[i] == nums[i-1] and not used[i-1]: continue

   It must be `i > start`, not `i > 0`. `i > 0` over-prunes and drops
   valid results like [2,2]. The `not used[i-1]` test is how you detect
   "same tree level" rather than "deeper in a branch using both copies".

7. Pruning -- Three Kinds:
   CONSTRAINT PROPAGATION  check validity BEFORE recursing, not at the
                           leaf. Killing a branch at depth 2 removes a
                           whole subtree.
   BOUND PRUNING           if the best possible completion cannot beat
                           the incumbent, stop (branch and bound).
   SYMMETRY BREAKING       explore one of each mirror-image pair.

   HOW MUCH pruning buys you depends on how often branches FAIL:
     Combinations  ~5% saved   -- almost every branch succeeds anyway
     N-Queens      ~9,000x at n=8 -- validity is rare, so most of the
                                  tree is dead weight

   Do not claim pruning always transforms the problem. It transforms the
   problems where most branches are invalid.

8. Complexity Is Output-Bound:

   Problem                  Results     Time          Space (excl. output)
   ──────────────────────────────────────────────────────────────────────
   Subsets                  2^n         O(n * 2^n)    O(n)
   Permutations             n!          O(n * n!)     O(n)
   Combinations             C(n,k)      O(k * C(n,k)) O(k)
   Palindrome partitioning  <= 2^(n-1)  O(n * 2^n)    O(n)
   N-Queens                 varies      << n! pruned  O(n)
   Sudoku                   1           exponential   O(1)
   Word search              -           O(R*C*4^L)    O(L)

   You cannot beat these -- the OUTPUT is that large. Space is only
   O(depth), which is cheap; the results list dominates memory.

   Where the cliffs are:
     n=20  2^n = 1,048,576        n! = 2.4e18
     n=25  2^n = 33,554,432       n! = 1.6e25
   Subsets stay feasible to n~25. Permutations die around n~11.

9. Backtracking vs DP:

                        Backtracking          DP
   ────────────────────────────────────────────────────────────
   Goal                 enumerate ALL         optimal VALUE
   Overlapping subprobs ignores them          memoises them
   Output               list of solutions     one number
   Complexity           exponential           usually polynomial

   THE TELL:
     "list all ..."          -> backtracking
     "how many ways"         -> DP
     "find one valid X"      -> backtracking
     "maximum / minimum"     -> DP

   Measured example: counting paths in a 12x12 grid took ~140ms by
   backtracking and ~0.01ms by DP. Backtracking WALKS every path; DP
   COUNTS them. But DP cannot hand you the paths themselves.

   Hybrid: Word Break II needs backtracking for the sentences AND
   memoisation on the start index to survive adversarial input.

10. Practical Limits:
    Python's recursion limit is 1000 by default and backtracking depth is
    usually O(n). Fixes, in order:
      1. reduce depth / prune harder
      2. convert to an explicit stack
      3. sys.setrecursionlimit -- blunt, and you can still segfault the
         C stack before hitting the Python limit

Common Pitfalls:

1. results.append(path) instead of path[:]. The number-one bug.
2. Forgetting to undo -- state leaks into siblings, silently wrong.
3. Undoing incompletely (N-Queens has THREE sets to restore).
4. Validating at the leaf instead of before recursing. Correct but
   unusably slow.
5. Wrong recursion index: i vs i+1 vs start.
6. Not sorting before duplicate handling.
7. `i > 0` instead of `i > start` -- over-prunes.
8. Mutating a grid without restoring it.
9. Ignoring recursion depth on large inputs.
10. Using backtracking when the question only wants a count or an
    optimum. That is DP's job.

Problem Recognition Guide:

"all subsets / power set"              -> subsets template
"all permutations / orderings"         -> permutations + used array
"all combinations of size k"           -> combinations + loop bound
"combinations summing to target"       -> combination sum (i vs i+1)
"unique results, input has repeats"    -> sort + level-skip guard
"place N things without conflict"      -> N-Queens (sets for O(1) checks)
"fill a grid subject to rules"         -> Sudoku (MRV heuristic)
"trace a word through a grid"          -> word search (mark and restore)
"find all words in a grid"             -> trie + one DFS (Topic 18)
"split a string all valid ways"        -> partitioning (+ memo if needed)
"how many ways / best value"           -> DP, NOT backtracking

Interview Tips:

1. Write the template FIRST, out loud, before problem specifics. It
   shows you have a system rather than a memorised answer.
2. Draw the decision tree for n=3. Everything becomes obvious, and it
   makes your reasoning visible to the interviewer.
3. State the complexity as output-bound and say why it cannot be beaten.
4. Point at your pruning explicitly. Interviewers watch for whether you
   validate early or at the leaf.
5. For duplicates, EXPLAIN the `i > start` guard rather than just typing
   it. Anyone can memorise the line; explaining it is the signal.
6. Say when DP would be better. Volunteering that you know the wrong
   tool is a strong signal.
7. Mention the recursion-depth limit for large inputs.

Learning Progression:

1. Basic: the template, subsets, permutations, combinations
2. Intermediate: duplicates, combination sum, partitioning, grid search
3. Advanced: N-Queens with O(1) conflict sets, Sudoku with MRV,
   word search with a trie, memoised word break
4. Expert: branch and bound, Warnsdorff's heuristic, cryptarithmetic
   constraint propagation -- where heuristics beat raw search outright

Next: implement each stub, then run project.py to see backtracking
solving a scheduler, a puzzle generator, a config validator, and a
regex engine.
""")
