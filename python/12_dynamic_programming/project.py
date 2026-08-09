"""
Project: Dynamic Programming Applications in the Real World

Build practical systems using DP:
1. Text Editor (Edit Distance)
2. Price Optimizer (Knapsack Variation)
3. Recommendation Engine (LCS)
4. Route Planner (Shortest Path DP)
"""

from typing import List, Dict, Tuple
import time
from collections import defaultdict

print("=" * 70)
print("PROJECT: Dynamic Programming Applications")
print("=" * 70)

# ==================== PART 1: Text Editor (Edit Distance) ====================
print("\n[PART 1] Text Editor - Spell Correction")
print("-" * 70)

class SpellChecker:
    """Spell correction using edit distance"""

    def __init__(self):
        self.dictionary = {
            "apple", "application", "apply",
            "hello", "help", "world",
            "python", "programming", "program",
            "algorithm", "analyze", "analysis"
        }

    def edit_distance(self, s1: str, s2: str) -> int:
        """Calculate minimum edits (insert/delete/replace)"""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

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

    def suggest_corrections(self, word: str, max_distance: int = 2) -> List[str]:
        """Find dictionary words within edit distance"""
        suggestions = []

        for dict_word in self.dictionary:
            dist = self.edit_distance(word.lower(), dict_word.lower())
            if dist <= max_distance:
                suggestions.append((dict_word, dist))

        return sorted(suggestions, key=lambda x: x[1])

# Test spell checker
print("Spell Correction Demo:\n")
checker = SpellChecker()

misspellings = ["appl", "helllo", "programm"]

for word in misspellings:
    suggestions = checker.suggest_corrections(word)
    print(f"'{word}' → ", end="")
    if suggestions:
        print(f"Did you mean: {[s[0] for s in suggestions[:3]]}")
    else:
        print("No suggestions found")

print("→ Time: O(n × m²) for n dictionary words, m word length")
print("→ Used in Google search, IDEs, spell checkers")

# ==================== PART 2: Price Optimizer (Knapsack) ====================
print("\n[PART 2] Price Optimizer - Constrained Budget")
print("-" * 70)

class PriceOptimizer:
    """Maximize value within budget constraint"""

    def __init__(self):
        # (name, price, value_score)
        self.items = [
            ("Premium",     100, 95),
            ("Standard",    60,  70),
            ("Basic",       40,  50),
            ("Trial",       20,  30),
            ("Enterprise",  200, 150),
            ("Starter",     30,  25),
        ]

    def select_items(self, budget: int) -> Tuple[List[str], int, int]:
        """Select items to maximize value within budget"""
        n = len(self.items)
        prices = [item[1] for item in self.items]
        values = [item[2] for item in self.items]

        # DP table
        dp = [[0] * (budget + 1) for _ in range(n + 1)]

        # Fill table
        for i in range(1, n + 1):
            for b in range(budget + 1):
                # Don't take item
                dp[i][b] = dp[i - 1][b]

                # Take item if fits
                if prices[i - 1] <= b:
                    dp[i][b] = max(
                        dp[i][b],
                        dp[i - 1][b - prices[i - 1]] + values[i - 1]
                    )

        # Reconstruct items
        selected = []
        i, b = n, budget
        while i > 0 and b > 0:
            if dp[i][b] != dp[i - 1][b]:
                selected.append(self.items[i - 1][0])
                b -= prices[i - 1]
            i -= 1

        total_value = dp[n][budget]
        total_price = sum(
            item[1] for item in self.items
            if item[0] in selected
        )

        return selected, total_value, total_price

# Test price optimizer
print("Budget Optimization Demo:\n")
optimizer = PriceOptimizer()

budgets = [100, 150, 250]

for budget in budgets:
    items, value, price = optimizer.select_items(budget)
    print(f"Budget: ${budget}")
    print(f"  Selected: {items}")
    print(f"  Cost: ${price}, Value: {value}")

print("→ Time: O(n × budget), Space: O(n × budget)")
print("→ Real applications: portfolio selection, resource allocation")

# ==================== PART 3: Recommendation Engine (LCS) ====================
print("\n[PART 3] Recommendation Engine - Content Similarity")
print("-" * 70)

class RecommendationEngine:
    """Find similar content using LCS"""

    def __init__(self):
        # User watch history (simplified as character sequence)
        self.users = {
            "alice": "actioncomedydrama",
            "bob": "actiondramacomedy",
            "charlie": "comedydramaaction",
            "diana": "horroractiondrama",
        }

    def lcs_length(self, s1: str, s2: str) -> int:
        """Find longest common subsequence"""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    def similarity(self, user1: str, user2: str) -> float:
        """Calculate similarity between users (0-1)"""
        history1 = self.users.get(user1, "")
        history2 = self.users.get(user2, "")

        if not history1 or not history2:
            return 0.0

        lcs = self.lcs_length(history1, history2)
        max_len = max(len(history1), len(history2))

        return lcs / max_len if max_len > 0 else 0.0

    def find_similar_users(self, user: str) -> List[Tuple[str, float]]:
        """Find users with similar taste"""
        if user not in self.users:
            return []

        similarities = []

        for other_user in self.users:
            if other_user != user:
                sim = self.similarity(user, other_user)
                similarities.append((other_user, sim))

        return sorted(similarities, key=lambda x: x[1], reverse=True)

# Test recommendation engine
print("Content Recommendation Demo:\n")
engine = RecommendationEngine()

for user in ["alice", "bob", "diana"]:
    similar = engine.find_similar_users(user)
    print(f"{user.capitalize()}'s similar users:")
    for other, score in similar[:2]:
        print(f"  {other}: {score:.2%} similar")

print("→ Time: O(m × n) for each comparison")
print("→ Real applications: collaborative filtering, user clustering")

# ==================== PART 4: Route Planner (Grid DP) ====================
print("\n[PART 4] Route Planner - Shortest Safe Path")
print("-" * 70)

class RoutePlanner:
    """Find safest/shortest path in grid"""

    def __init__(self, grid: List[List[int]]):
        """Grid: 0=safe, 1=hazard"""
        self.grid = grid
        self.m = len(grid)
        self.n = len(grid[0]) if grid else 0

    def min_risk_path(self) -> Tuple[int, List[Tuple[int, int]]]:
        """Minimum risk path from top-left to bottom-right"""
        if not self.grid or self.m == 0 or self.n == 0:
            return float('inf'), []

        # dp[i][j] = min risk to reach (i,j)
        dp = [[float('inf')] * self.n for _ in range(self.m)]
        parent = [[None] * self.n for _ in range(self.m)]

        dp[0][0] = self.grid[0][0]

        # Fill first row
        for j in range(1, self.n):
            dp[0][j] = dp[0][j - 1] + self.grid[0][j]
            parent[0][j] = (0, j - 1)

        # Fill first column
        for i in range(1, self.m):
            dp[i][0] = dp[i - 1][0] + self.grid[i][0]
            parent[i][0] = (i - 1, 0)

        # Fill rest of table
        for i in range(1, self.m):
            for j in range(1, self.n):
                risk_from_up = dp[i - 1][j]
                risk_from_left = dp[i][j - 1]

                if risk_from_up <= risk_from_left:
                    dp[i][j] = risk_from_up + self.grid[i][j]
                    parent[i][j] = (i - 1, j)
                else:
                    dp[i][j] = risk_from_left + self.grid[i][j]
                    parent[i][j] = (i, j - 1)

        # Reconstruct path
        path = []
        curr = (self.m - 1, self.n - 1)

        while curr is not None:
            path.append(curr)
            if parent[curr[0]][curr[1]] is None:
                break
            curr = parent[curr[0]][curr[1]]

        return dp[self.m - 1][self.n - 1], list(reversed(path))

# Test route planner
print("Route Planning Demo:\n")

grid = [
    [1, 3, 1, 5],
    [2, 2, 4, 1],
    [5, 0, 2, 3],
    [0, 6, 1, 2]
]

planner = RoutePlanner(grid)
risk, path = planner.min_risk_path()

print("Grid (risk values):")
for row in grid:
    print(f"  {row}")

print(f"\nMinimum risk path: {risk}")
print(f"Route: {path}")
print("→ Time: O(m × n), Space: O(m × n)")
print("→ Real applications: GPS navigation, resource planning")

# ==================== PART 5: Performance Analysis ====================
print("\n[PART 5] DP Performance Comparison")
print("-" * 70)

def benchmark_approaches(n: int):
    """Compare memoization vs tabulation"""

    # Memoization
    memo_cache = {}

    def fib_memo(x):
        if x in memo_cache:
            return memo_cache[x]
        if x <= 1:
            return x
        result = fib_memo(x - 1) + fib_memo(x - 2)
        memo_cache[x] = result
        return result

    # Tabulation
    def fib_tab(x):
        if x <= 1:
            return x
        dp = [0] * (x + 1)
        dp[1] = 1
        for i in range(2, x + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[x]

    # Measure memoization
    memo_cache.clear()
    start = time.time()
    memo_result = fib_memo(n)
    memo_time = (time.time() - start) * 1000

    # Measure tabulation
    start = time.time()
    tab_result = fib_tab(n)
    tab_time = (time.time() - start) * 1000

    return memo_time, tab_time

print("Performance Comparison (Fibonacci):\n")
print(f"{'n':<6} {'Memoization':<15} {'Tabulation':<15} {'Speedup':<10}")
print("-" * 46)

for n in [20, 25, 30]:
    memo_t, tab_t = benchmark_approaches(n)
    speedup = memo_t / tab_t if tab_t > 0 else 1
    print(f"{n:<6} {memo_t:>8.3f}ms {'':<2} {tab_t:>8.3f}ms {'':<2} {speedup:>6.2f}x")

print("\n→ Tabulation is faster due to no recursion overhead")
print("→ Both have same time complexity O(n)")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World DP Applications:

1. Text Editor (Edit Distance)
   - Spell checking and correction
   - DNA sequence alignment
   - Plagiarism detection
   - Time: O(m × n), Space: O(m × n)

2. Price Optimizer (0/1 Knapsack)
   - Budget allocation
   - Portfolio selection
   - Resource scheduling
   - Time: O(n × W), Space: O(n × W)

3. Recommendation Engine (LCS)
   - User similarity matching
   - Playlist recommendations
   - Content similarity
   - Time: O(m × n), Space: O(m × n)

4. Route Planner (Grid DP)
   - Navigation systems
   - Cost minimization
   - Risk assessment paths
   - Time: O(m × n), Space: O(m × n)

Key Insights:

✓ DP transforms exponential to polynomial time
✓ Memoization: top-down, recursive, intuitive
✓ Tabulation: bottom-up, iterative, efficient
✓ Both have same time complexity
✓ Space can often be optimized O(n²) → O(n)
✓ Many real problems use DP variants

Common Real-World Patterns:

Linear DP:
- Fibonacci, climbing, house robber
- Optimal value with sequential decisions
- Example: stock trading

Grid DP:
- Shortest path, unique paths
- Optimal value in 2D space
- Example: robot path planning

String DP:
- LCS, edit distance, word break
- String transformation problems
- Example: spell checking

Knapsack DP:
- Resource allocation, budget constraints
- Weight/value optimization
- Example: shopping with budget

Counting DP:
- Number of ways to do something
- Combinations, permutations
- Example: coin change ways

Algorithm Complexity Reference:

Problem              Time        Space   Use Case
─────────────────────────────────────────────
Fibonacci           O(n)        O(n)    Basic pattern
Coin Change         O(n*C)      O(n)    Min coins
LCS                 O(m*n)      O(m*n)  String matching
Edit Distance       O(m*n)      O(m*n)  Spell check
Knapsack            O(n*W)      O(n*W)  Budget allocation
House Robber        O(n)        O(1)    Max value non-adjacent
Unique Paths        O(m*n)      O(n)    Grid navigation

When to Consider DP:
✓ Optimal substructure exists
✓ Overlapping subproblems
✓ State space < 10^8 (memory constraint)
✓ Need exact optimal solution

Next: Master advanced DP patterns and tackle interview problems!
""")

print("=" * 70)
print("🎉 Topic 12 Complete! Dynamic Programming Mastered!")
print("=" * 70)
print("\n✅ ADVANCED LEVEL STARTING...")
print("   6 more topics to complete (Topics 13-18)")
print("   Ready for Topic 13: Advanced Sorting\n")
