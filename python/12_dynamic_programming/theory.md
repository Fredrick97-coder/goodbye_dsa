# Dynamic Programming - Optimization Fundamentals

Master the art of breaking problems into overlapping subproblems and building solutions efficiently.

---

## 1. What is Dynamic Programming?

**Dynamic Programming (DP)** is an optimization technique for solving problems with:
- **Optimal substructure**: Optimal solution uses optimal solutions to subproblems
- **Overlapping subproblems**: Same subproblems solved multiple times

### DP transforms exponential time to polynomial time by caching results.

```
Without DP (Fibonacci):
fib(5) calls fib(3) twice, fib(2) three times → O(2^n)

With DP:
Calculate once, store, reuse → O(n)
```

---

## 2. Two Approaches to DP

### Approach 1: Memoization (Top-Down)
Recursive solution with caching.

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]
```

**Pros**:
- ✓ Natural recursive thinking
- ✓ Only computes needed subproblems
- ✓ Easy to understand

**Cons**:
- ✗ Recursion overhead
- ✗ Stack depth issues on large n

### Approach 2: Tabulation (Bottom-Up)
Iterative solution with DP table.

```python
def fib_tab(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

**Pros**:
- ✓ No recursion overhead
- ✓ Predictable performance
- ✓ Easy to optimize space

**Cons**:
- ✗ Must compute all states
- ✗ Less intuitive

---

## 3. DP Problem Structure

### Step 1: Define State
What do we need to track? Often indexed by size/position.

```
Fibonacci: dp[n] = fib(n)
Coin Change: dp[amount] = min coins
Grid Path: dp[i][j] = paths to (i,j)
```

### Step 2: Base Cases
When do we know the answer without recursion?

```
Fibonacci: dp[0]=0, dp[1]=1
Coin Change: dp[0]=0 (no coins needed)
Grid Path: dp[0][*]=1, dp[*][0]=1 (one path)
```

### Step 3: Transition
How do we build solution from smaller problems?

```
Fibonacci: dp[n] = dp[n-1] + dp[n-2]
Coin Change: dp[amount] = min(dp[amount-coin] + 1)
Grid Path: dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

---

## 4. Common DP Patterns

### Pattern 1: 1D DP (Linear)
```python
# dp[i] depends on dp[0..i-1]
# Example: max sum subarray, climb stairs

dp = [0] * (n + 1)
for i in range(1, n + 1):
    dp[i] = f(dp[i-1], dp[i-2], ...)
```

### Pattern 2: 2D DP (Grid/Strings)
```python
# dp[i][j] depends on neighbors
# Example: longest common subsequence, edit distance

dp = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        dp[i][j] = f(dp[i-1][j], dp[i][j-1], ...)
```

### Pattern 3: 0/1 Decisions
```python
# Choose to include or exclude
# Example: knapsack, partition equal subset

for i in range(1, n + 1):
    # Include item i
    include = dp[i-1] + value[i]
    # Exclude item i
    exclude = dp[i-1]
    dp[i] = max(include, exclude)
```

---

## 5. Classic DP Problems

### Problem 1: Fibonacci Number
Find nth Fibonacci number.

```python
# Recursive with memoization
def fib(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

# Time: O(n), Space: O(n)
```

### Problem 2: Coin Change
Minimum coins to make amount.

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# Time: O(amount * n), Space: O(amount)
```

### Problem 3: Longest Common Subsequence
Longest sequence appearing in both strings.

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

# Time: O(m*n), Space: O(m*n)
```

### Problem 4: 0/1 Knapsack
Maximum value with weight constraint.

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item
            dp[i][w] = dp[i-1][w]
            
            # Take item if fits
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]

# Time: O(n*W), Space: O(n*W)
```

### Problem 5: Edit Distance
Minimum operations to transform s1 to s2.

```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # Delete
                    dp[i][j-1],      # Insert
                    dp[i-1][j-1]     # Replace
                )
    
    return dp[m][n]

# Time: O(m*n), Space: O(m*n)
```

---

## 6. DP Complexity Analysis

| Problem | State Size | Transitions | Time | Space |
|---------|-----------|-------------|------|-------|
| Fibonacci | O(n) | 2 | O(n) | O(n) |
| Coin Change | O(amount) | coins | O(amount*n) | O(amount) |
| LCS | O(m*n) | 2 | O(m*n) | O(m*n) |
| Knapsack | O(n*W) | 2 | O(n*W) | O(n*W) |
| Edit Distance | O(m*n) | 3 | O(m*n) | O(m*n) |

**Key insight**: Time = States × Transitions per state

---

## 7. Space Optimization

Many DP solutions can optimize space by keeping only previous row/column.

```python
# Full 2D: O(m*n) space
# Optimized: O(n) space for LCS

def lcs_optimized(s1, s2):
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev, curr = curr, prev
    
    return prev[n]
```

---

## 8. When to Use DP

### Use DP when:
- ✓ Problem has optimal substructure
- ✓ Overlapping subproblems exist
- ✓ Constraint is not too large
- ✓ Need exact optimal solution

### Don't use DP when:
- ✗ Subproblems don't overlap
- ✗ State space is exponential (e.g., 2^n states)
- ✗ Problem requires approximate solution
- ✗ State transitions are complex

---

## 9. DP vs Greedy

| Aspect | DP | Greedy |
|--------|----|----|
| Optimal | Always | Sometimes |
| Speed | Slower | Faster |
| Memory | More | Less |
| Proof needed | Often easy | Often hard |

Greedy fails on many problems (e.g., coin change with arbitrary coins).

---

## 10. Advanced DP Concepts

### Digit DP
Count numbers with special property (e.g., palindromes up to N).

### Tree DP
Process trees bottom-up (e.g., max path in tree).

### Bitmask DP
Use bitmask as state (e.g., traveling salesman).

### Convex Hull Trick
Optimize linear DP to O(n) instead of O(n²).

---

## 11. Key Takeaways

✅ **DP**: Break into subproblems and cache  
✅ **Memoization**: Top-down, recursive approach  
✅ **Tabulation**: Bottom-up, iterative approach  
✅ **State**: Define what changes, index by problem size  
✅ **Base cases**: Know answers without recursion  
✅ **Transition**: How to build from smaller problems  
✅ **Optimize**: Often can reduce space with rolling arrays  

**Best for**: Optimization, counting, path problems  
**Interview favorite**: Because it's learnable and powerful

Next: Practice classic DP problems and build real solutions!
