"""
Exercises: Dynamic Programming

Practice memoization, tabulation, and classic DP patterns.
"""

from typing import List

print("=" * 70)
print("EXERCISES: Dynamic Programming")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. FIBONACCI NUMBER")
print("Input: n")
print("Output: nth Fibonacci number")
def fib(n: int) -> int:
    # TODO: Implement using memoization or tabulation
    pass

print("\n2. CLIMBING STAIRS")
print("Input: n (stairs)")
print("Output: Number of ways to climb (1 or 2 steps at a time)")
def climb_stairs(n: int) -> int:
    # TODO: Implement DP solution
    pass

print("\n3. HOUSE ROBBER")
print("Input: nums (house values)")
print("Output: Maximum value without robbing adjacent houses")
def rob(nums: List[int]) -> int:
    # TODO: Implement with DP
    pass

print("\n4. UNIQUE PATHS")
print("Input: m, n (grid dimensions)")
print("Output: Number of unique paths from top-left to bottom-right")
def unique_paths(m: int, n: int) -> int:
    # TODO: Implement 2D DP solution
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n5. COIN CHANGE")
print("Input: coins list, amount")
print("Output: Minimum number of coins to make amount")
def coin_change(coins: List[int], amount: int) -> int:
    # TODO: Implement DP solution
    pass

print("\n6. LONGEST COMMON SUBSEQUENCE")
print("Input: s1, s2 (strings)")
print("Output: Length of longest common subsequence")
def lcs_length(s1: str, s2: str) -> int:
    # TODO: Implement 2D DP solution
    pass

print("\n7. EDIT DISTANCE")
print("Input: s1, s2 (strings)")
print("Output: Minimum edits to transform s1 to s2")
def edit_distance(s1: str, s2: str) -> int:
    # TODO: Implement with insert/delete/replace operations
    pass

print("\n8. PARTITION EQUAL SUBSET SUM")
print("Input: nums list")
print("Output: Can split into two equal-sum subsets?")
def can_partition(nums: List[int]) -> bool:
    # TODO: Implement subset sum DP
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n9. 0/1 KNAPSACK")
print("Input: weights, values, capacity")
print("Output: Maximum value without exceeding capacity")
def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    # TODO: Implement classic knapsack DP
    pass

print("\n10. LONGEST INCREASING SUBSEQUENCE")
print("Input: nums list")
print("Output: Length of longest increasing subsequence")
def lis_length(nums: List[int]) -> int:
    # TODO: Implement O(n log n) or O(n²) solution
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n11. WORD BREAK")
print("Input: s (string), word_dict (list of valid words)")
print("Output: Can s be segmented into valid words?")
def word_break(s: str, word_dict: List[str]) -> bool:
    # TODO: Implement DP with set for O(n²) solution
    pass

print("\n12. COIN CHANGE II")
print("Input: coins list, amount")
print("Output: Number of ways to make amount with coins")
def change(coins: List[int], amount: int) -> int:
    # TODO: Implement combinations DP (order doesn't matter)
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
DP Problem Categories:

Linear DP (1D):
- Fibonacci: dp[i] depends on dp[i-1], dp[i-2]
- Climbing stairs: count ways
- House robber: max value non-adjacent
- Coin change: min/count coins

2D DP (Grid/String):
- Unique paths: count paths in grid
- LCS: longest common subsequence
- Edit distance: minimum operations
- Knapsack: max value with constraint

Subset/Partition DP:
- Partition equal sum: can split into equal parts?
- Subset sum: target sum exists?
- Combinations: count ways to select items

State Definition Strategy:
1. dp[i] = answer for first i items/positions
2. dp[i][j] = answer for i items and j capacity/length
3. dp[i][j][k] = answer with 3 dimensions (rare)

Base Cases:
- dp[0] usually means "nothing selected"
- Often 0 or 1 depending on problem
- Sometimes multiple base cases needed

Transition Patterns:
- Include/exclude: max/min of both choices
- Min/max operation: for optimization
- Counting: sum all possibilities
- Boolean: AND/OR of conditions

Common Mistakes:
- Forgetting base cases → wrong answers
- Wrong iteration order → dependencies not met
- Not initializing → garbage values
- Off-by-one errors → boundary issues
- Not handling impossible cases → wrong type

Optimization Techniques:
1. Space optimization: O(n²) → O(n) with rolling arrays
2. Time optimization: O(n²) → O(n log n) with binary search
3. Memoization: automatic caching with @lru_cache
4. Modulo: for large numbers (counting problems)

Practice Tips:
1. Identify state: what changes between subproblems?
2. Find base case: when don't we need recursion?
3. Write recurrence: how to build from smaller problems?
4. Implement: either memoization or tabulation
5. Optimize: space/time if needed
6. Test: edge cases, large inputs, impossible cases

Common Pitfalls:
- Greedy doesn't work for many DP problems
- Must iterate in correct order (dependencies)
- Forgetting to mark impossible states
- Confusing combinations vs permutations
- Integer overflow on large answers

Next: Complete project with real DP applications!
""")
