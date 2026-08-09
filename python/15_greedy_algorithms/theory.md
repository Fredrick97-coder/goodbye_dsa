# Greedy Algorithms - Optimization by Local Choice

Master the greedy approach: make locally optimal choices hoping to find global optimum.

---

## 1. What is a Greedy Algorithm?

**Greedy**: Make the locally optimal choice at each step, hoping it leads to global optimum.

### Characteristics:
- **Greedy choice property**: Local optimum leads to global optimum
- **Optimal substructure**: Optimal solution contains optimal subsolutions
- **No backtracking**: Once a choice is made, it's never reconsidered

### Greedy ≠ Always Optimal:
- Works for some problems (Dijkstra, MST, Activity Selection)
- Fails for others (0/1 Knapsack, Coin Change with arbitrary coins)
- Requires proof of correctness

---

## 2. Activity Selection Problem

**Problem**: Select maximum number of non-overlapping activities.

```python
def activity_selection(activities):
    """Sort by end time, greedily select"""
    # activities: list of (start, end) tuples
    
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_end = activities[0][1]
    
    for start, end in activities[1:]:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    
    return selected
```

**Algorithm**: Sort by end time, always pick earliest finishing activity that doesn't conflict.

**Proof**: Greedy choice (earliest finish) leaves maximum room for future activities.

**Time**: O(n log n), **Space**: O(n)

---

## 3. Huffman Coding

**Problem**: Build optimal prefix-free code with minimum average length.

```python
import heapq

class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_coding(text):
    """Build Huffman tree, generate codes"""
    # Count frequencies
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    # Build min-heap of nodes
    heap = [Node(f, c) for c, f in freq.items()]
    heapq.heapify(heap)
    
    # Build tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, parent)
    
    # Generate codes
    root = heap[0]
    codes = {}
    
    def traverse(node, code=""):
        if node.char:
            codes[node.char] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    
    traverse(root)
    return codes
```

**Algorithm**: Build tree bottom-up by repeatedly combining two smallest frequency nodes.

**Why greedy works**: Merging smallest frequencies minimizes total cost (depth × frequency sum).

**Time**: O(n log n), **Space**: O(n)

---

## 4. Fractional Knapsack

**Problem**: Maximize value with weight constraint. Items can be split.

```python
def fractional_knapsack(items, capacity):
    """items: list of (weight, value) tuples"""
    
    # Sort by value-to-weight ratio (descending)
    items.sort(key=lambda x: x[1]/x[0], reverse=True)
    
    total_value = 0
    total_weight = 0
    
    for weight, value in items:
        if total_weight + weight <= capacity:
            # Take whole item
            total_weight += weight
            total_value += value
        else:
            # Take fraction
            remaining = capacity - total_weight
            fraction = remaining / weight
            total_value += value * fraction
            break
    
    return total_value
```

**Algorithm**: Sort by value-to-weight ratio, greedily take items.

**Why optimal**: At each step, take maximum value per unit weight remaining.

**Time**: O(n log n), **Space**: O(1)

---

## 5. Job Sequencing with Deadlines

**Problem**: Schedule jobs with deadlines to maximize profit.

```python
def job_sequencing(jobs):
    """jobs: list of (id, deadline, profit) tuples"""
    
    # Sort by profit (descending)
    jobs.sort(key=lambda x: x[2], reverse=True)
    
    max_deadline = max(job[1] for job in jobs)
    schedule = [None] * max_deadline
    
    total_profit = 0
    
    for job_id, deadline, profit in jobs:
        # Try to schedule at latest possible slot before deadline
        for slot in range(deadline - 1, -1, -1):
            if schedule[slot] is None:
                schedule[slot] = job_id
                total_profit += profit
                break
    
    return total_profit, schedule
```

**Algorithm**: Sort by profit (descending), greedily assign to latest available slot.

**Why greedy works**: High-profit jobs shouldn't be blocked by lower-profit jobs.

**Time**: O(n²), **Space**: O(n)

---

## 6. Interval Scheduling Maximization

**Problem**: Select maximum non-overlapping intervals.

```python
def interval_schedule(intervals):
    """Similar to activity selection"""
    
    # Sort by end time
    intervals.sort(key=lambda x: x[1])
    
    selected = [intervals[0]]
    last_end = intervals[0][1]
    
    for start, end in intervals[1:]:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    
    return selected
```

**Proof**: By always choosing interval with earliest finish time, we maximize remaining time for future intervals.

---

## 7. Greedy vs Dynamic Programming

| Problem | Greedy | DP | Result |
|---------|--------|----|----|
| Activity Selection | ✓ Optimal | Works too | Same |
| Fractional Knapsack | ✓ Optimal | Works too | Same |
| 0/1 Knapsack | ✗ Fails | ✓ Optimal | DP correct |
| Coin Change (fixed coins) | ✗ Fails | ✓ Optimal | DP correct |
| Huffman Coding | ✓ Optimal | N/A | Greedy correct |
| Job Sequencing | ✓ Optimal | Works too | Same |

### Key Difference:
- **Greedy**: Commit to choice immediately (may miss better solutions)
- **DP**: Explore all choices (guaranteed optimal)

---

## 8. Greedy Algorithms in Known Contexts

### Already Greedy (Covered Earlier):
- **Dijkstra**: Always pick unvisited vertex with minimum distance
- **Prim's MST**: Always pick minimum edge expanding tree
- **Kruskal's MST**: Always pick minimum edge not creating cycle
- **Huffman**: Always merge two minimum frequency nodes

### Greedy Elements:
- **Topological Sort** (Kahn's): Pick vertices with in-degree 0
- **Interval Scheduling**: Pick earliest finishing activity
- **Activity Selection**: Same as interval scheduling

---

## 9. When to Use Greedy

### Good Indicators:
1. Problem has **optimal substructure** (optimal solution from optimal subsolutions)
2. Problem has **greedy choice property** (local optimal = global optimal)
3. No need to explore all possibilities
4. Simple, fast algorithm exists

### Red Flags:
1. Problem explicitly requires "maximum number of choices"
2. Items have interdependencies
3. Order matters significantly
4. Backtracking needed

### Proof Strategy:
1. **Exchange argument**: Show greedy choice can replace any choice without worsening solution
2. **Induction**: Prove greedy choice leads to optimal solution
3. **Counterexample**: If exists, greedy fails

---

## 10. Common Greedy Problems

| Problem | Greedy Strategy | Time | Proof |
|---------|-----------------|------|-------|
| Activity Selection | Earliest finish | O(n log n) | Exchange |
| Fractional Knapsack | Value/weight ratio | O(n log n) | Obvious |
| Interval Scheduling | Earliest finish | O(n log n) | Exchange |
| Job Sequencing | Highest profit first | O(n²) | Priority |
| Huffman Coding | Merge smallest freq | O(n log n) | Optimality |
| MST (Kruskal) | Minimum edge | O(E log E) | Cut |
| MST (Prim) | Minimum edge from tree | O(E log V) | Cut |
| Dijkstra | Minimum distance | O((V+E) log V) | Induction |

---

## 11. Greedy Failures

### Example 1: Coin Change
```
Coins: [1, 3, 4], Amount: 6
Greedy: 4 + 1 + 1 = 3 coins (WRONG)
Optimal: 3 + 3 = 2 coins (DP)
```

### Example 2: 0/1 Knapsack
```
Items: [(1, 100), (50, 30), (50, 31)]
Capacity: 50
Greedy (by value): 100 (total 1 weight, 100 value) (WRONG)
Optimal: 30 + 31 = 61 value (DP)
```

### Example 3: Minimum Spanning Tree (Wrong Order)
```
Greedy by smallest edge: May create cycle, waste edge
Correct: Use union-find to avoid cycles
```

---

## 12. Key Takeaways

✅ **Greedy**: Local optimization, fast, not always optimal  
✅ **Activity Selection**: Sort by end time, locally optimal = globally optimal  
✅ **Huffman Coding**: Optimal prefix code via bottom-up merging  
✅ **Fractional Knapsack**: Optimal with value/weight ratio  
✅ **Proof needed**: Always verify greedy works for problem  
✅ **Exchange argument**: Show greedy choice doesn't worsen solution  
✅ **When it works**: Massive speedup over DP  

**Interview Focus**:
- Prove greedy correctness
- Know when greedy fails
- Distinguish from DP
- Optimize with priority queue

Next: Implement greedy algorithms and recognize when they apply!
