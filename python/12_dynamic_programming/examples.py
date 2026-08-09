"""
Examples: Dynamic Programming Techniques

Demonstrate memoization, tabulation, and classic DP problems.
"""

from typing import Dict, List
import time

print("=" * 70)
print("DYNAMIC PROGRAMMING - TECHNIQUES & PATTERNS")
print("=" * 70)

# ==================== (1) Fibonacci - Memoization ====================
print("\n[1] Fibonacci: Memoization (Top-Down)")
print("-" * 70)

def fib_recursive(n):
    """Naive recursion - exponential time"""
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

def fib_memo(n, memo=None):
    """Memoization - cache results"""
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# Compare performance
n = 35
print(f"Fibonacci({n}):\n")

start = time.time()
naive = fib_recursive(n)
naive_time = (time.time() - start) * 1000

start = time.time()
memoized = fib_memo(n)
memo_time = (time.time() - start) * 1000

print(f"  Naive recursion:    {naive_time:>8.2f}ms")
print(f"  Memoization:        {memo_time:>8.2f}ms (speedup: {naive_time/memo_time:.0f}x)")
print(f"  Result:             {memoized}")
print("→ Memoization trades memory for speed")

# ==================== (2) Fibonacci - Tabulation ====================
print("\n[2] Fibonacci: Tabulation (Bottom-Up)")
print("-" * 70)

def fib_tab(n):
    """Tabulation - iterative DP"""
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

result = fib_tab(35)
print(f"Fibonacci(35) via tabulation: {result}")
print("→ Time: O(n), Space: O(n)")
print("→ No recursion overhead, clean iterative approach")

# ==================== (3) Coin Change ====================
print("\n[3] Coin Change: Minimum Coins")
print("-" * 70)

def coin_change(coins: List[int], amount: int) -> int:
    """Find minimum coins to make amount"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

coins = [1, 2, 5]
amount = 11
result = coin_change(coins, amount)

print(f"Coins: {coins}, Amount: {amount}")
print(f"Minimum coins: {result} (5+5+1)")
print("→ Time: O(amount × coins), Space: O(amount)")
print("→ Greedy (always pick largest) fails on some coin sets!")

# ==================== (4) Longest Common Subsequence ====================
print("\n[4] Longest Common Subsequence (LCS)")
print("-" * 70)

def lcs(s1: str, s2: str) -> int:
    """Find length of longest common subsequence"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]

def lcs_string(s1: str, s2: str) -> str:
    """Reconstruct actual LCS string"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(result))

s1, s2 = "ABCDGH", "AEDFHR"
length = lcs(s1, s2)
actual = lcs_string(s1, s2)

print(f"String 1: {s1}")
print(f"String 2: {s2}")
print(f"LCS length: {length}")
print(f"LCS string: {actual}")
print("→ Time: O(m×n), Space: O(m×n)")
print("→ Classic string comparison problem")

# ==================== (5) Edit Distance ====================
print("\n[5] Edit Distance (Levenshtein)")
print("-" * 70)

def edit_distance(s1: str, s2: str) -> int:
    """Minimum operations to transform s1 to s2"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )

    return dp[m][n]

s1, s2 = "kitten", "sitting"
dist = edit_distance(s1, s2)

print(f"Transform '{s1}' to '{s2}'")
print(f"Edit distance: {dist}")
print("Operations: kitten→sitten→sittin→sitting (3 edits)")
print("→ Time: O(m×n), Space: O(m×n)")
print("→ Used in spell checkers, DNA alignment")

# ==================== (6) 0/1 Knapsack ====================
print("\n[6] 0/1 Knapsack Problem")
print("-" * 70)

def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """Maximum value with weight constraint"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item
            dp[i][w] = dp[i - 1][w]

            # Take item if fits
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )

    return dp[n][capacity]

weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 8
result = knapsack(weights, values, capacity)

print(f"Items (weight, value): {list(zip(weights, values))}")
print(f"Capacity: {capacity}")
print(f"Maximum value: {result}")
print("→ Time: O(n×W), Space: O(n×W)")
print("→ Classic optimization problem")

# ==================== (7) House Robber ====================
print("\n[7] House Robber (Max Non-Adjacent Sum)")
print("-" * 70)

def rob(houses: List[int]) -> int:
    """Rob houses, can't rob adjacent"""
    if not houses:
        return 0

    dp = [0] * len(houses)
    dp[0] = houses[0]

    if len(houses) > 1:
        dp[1] = max(houses[0], houses[1])

    for i in range(2, len(houses)):
        dp[i] = max(
            dp[i - 1],                    # Skip house i
            dp[i - 2] + houses[i]         # Rob house i
        )

    return dp[-1]

houses = [1, 3, 1, 3, 100]
result = rob(houses)

print(f"House values: {houses}")
print(f"Maximum loot: {result} (house[1]=3 + house[4]=100)")
print("→ Time: O(n), Space: O(n) [or O(1) with rolling variables]")
print("→ Greedy fails: taking max isn't always optimal")

# ==================== (8) Climbing Stairs ====================
print("\n[8] Climbing Stairs (Number of Ways)")
print("-" * 70)

def climb_stairs(n: int) -> int:
    """Number of ways to climb n stairs (1 or 2 steps per move)"""
    if n <= 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2

    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

n = 5
result = climb_stairs(n)

print(f"Stairs: {n}")
print(f"Ways to climb: {result}")
print("  1+1+1+1+1, 2+1+1+1, 1+2+1+1, 1+1+2+1, 1+1+1+2, 2+2+1, 2+1+2, 1+2+2")
print("→ Time: O(n), Space: O(n)")
print("→ This is just Fibonacci!")

# ==================== (9) Grid Paths ====================
print("\n[9] Unique Paths in Grid")
print("-" * 70)

def unique_paths(m: int, n: int) -> int:
    """Paths from top-left to bottom-right (right/down only)"""
    dp = [[1] * n for _ in range(m)]

    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp[m - 1][n - 1]

m, n = 3, 3
result = unique_paths(m, n)

print(f"Grid: {m}×{n}")
print(f"Unique paths: {result}")
print(f"Grid visualization:")
grid = [[str(unique_paths(i + 1, j + 1)) for j in range(n)] for i in range(m)]
for row in grid:
    print("  " + " ".join(row))
print("→ Time: O(m×n), Space: O(m×n)")
print("→ Common interview problem")

# ==================== (10) Space Optimization ====================
print("\n[10] Space Optimization: Rolling Array")
print("-" * 70)

def unique_paths_optimized(m: int, n: int) -> int:
    """Same problem with O(n) space instead of O(m×n)"""
    prev = [1] * n

    for i in range(1, m):
        curr = [1] * n
        for j in range(1, n):
            curr[j] = curr[j - 1] + prev[j]
        prev = curr

    return prev[n - 1]

m, n = 5, 5
result = unique_paths_optimized(m, n)

print(f"Grid: {m}×{n}")
print(f"Unique paths: {result}")
print("→ Time: O(m×n), Space: O(n) [reduced from O(m×n)]")
print("→ Many 2D DP problems can be space-optimized this way")

# ==================== (11) Decision DP ====================
print("\n[11] Partition Equal Subset Sum")
print("-" * 70)

def can_partition(nums: List[int]) -> bool:
    """Can split array into two equal-sum subsets?"""
    total = sum(nums)

    if total % 2 != 0:
        return False

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]

    return dp[target]

nums = [1, 5, 11, 5]
result = can_partition(nums)

print(f"Array: {nums}, Sum: {sum(nums)}")
print(f"Can partition: {result}")
print("Partition: [11] and [5, 5, 1]")
print("→ Time: O(n×sum), Space: O(sum)")
print("→ Iterate backwards to avoid using same element twice")

# ==================== (12) Memoization Decorator ====================
print("\n[12] Memoization with Decorator")
print("-" * 70)

def memoize(func):
    """Decorator to add memoization to any function"""
    cache = {}

    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]

    return wrapper

@memoize
def fib_decorated(n):
    """Fibonacci with automatic memoization"""
    if n <= 1:
        return n
    return fib_decorated(n - 1) + fib_decorated(n - 2)

result = fib_decorated(35)
print(f"Fibonacci(35) with decorator: {result}")
print("→ Clean way to add memoization to recursive functions")
print("→ Production-ready with functools.lru_cache")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("DYNAMIC PROGRAMMING SUMMARY")
print("=" * 70)

print("""
Key DP Concepts:

1. Memoization (Top-Down):
   - Recursive solution with caching
   - Pros: Intuitive, lazy evaluation
   - Cons: Recursion overhead

2. Tabulation (Bottom-Up):
   - Iterative solution with table
   - Pros: No recursion, cache-friendly
   - Cons: Must compute all states

3. State Definition:
   - What changes? Index by that
   - Example: dp[i] = answer for first i items

4. Base Cases:
   - When do we know answer without recursion?
   - Examples: dp[0], dp[1]

5. Transition:
   - How to build solution from smaller problems?
   - Usually involves choice: include/exclude, min/max

6. Space Optimization:
   - Many 2D problems → O(n) with rolling arrays
   - Example: previous row + current row

Classic Problems:

✓ Fibonacci:           O(n) time, O(n) space
✓ Coin Change:        O(amount×coins) time
✓ LCS:                O(m×n) time
✓ Edit Distance:      O(m×n) time
✓ Knapsack:           O(n×W) time
✓ House Robber:       O(n) time
✓ Grid Paths:         O(m×n) time, reducible to O(n)

When to Use DP:
✓ Optimal substructure exists
✓ Overlapping subproblems
✓ State space manageable
✓ Need exact optimal solution

Next: Solve DP exercises and build real applications!
""")

print("=" * 70)
print("Examples Complete!")
print("=" * 70)
