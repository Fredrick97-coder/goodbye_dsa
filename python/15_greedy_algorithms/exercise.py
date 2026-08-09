"""
Exercises: Greedy Algorithms

Practice activity selection, Huffman coding, job scheduling, and more.
"""

from typing import List, Tuple

print("=" * 70)
print("EXERCISES: Greedy Algorithms")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. ACTIVITY SELECTION")
print("Input: List of activities (start, end) tuples")
print("Output: Maximum non-overlapping activities")
def activity_selection(activities: List[Tuple]) -> List[Tuple]:
    # TODO: Sort by end time, greedily select non-overlapping
    pass

print("\n2. FRACTIONAL KNAPSACK")
print("Input: Items (weight, value), capacity")
print("Output: Maximum value (items can be split)")
def fractional_knapsack(items: List[Tuple], capacity: float) -> float:
    # TODO: Sort by value/weight ratio, greedily take items
    pass

print("\n3. HUFFMAN CODING")
print("Input: Text string")
print("Output: Huffman codes dictionary")
def huffman_coding(text: str) -> dict:
    # TODO: Build Huffman tree via min-heap merging
    pass

print("\n4. MINIMUM NUMBER OF COINS")
print("Input: Coins (standard: 1,5,10,25), amount")
print("Output: Minimum coins needed")
def min_coins_standard(amount: int) -> int:
    # TODO: Greedy works for standard US coins
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n5. JOB SEQUENCING WITH DEADLINES")
print("Input: Jobs (id, deadline, profit)")
print("Output: Maximum profit schedule")
def job_sequencing(jobs: List[Tuple]) -> int:
    # TODO: Sort by profit, schedule at latest available slot
    pass

print("\n6. GREEDY INTERVAL SCHEDULING")
print("Input: Intervals (start, end)")
print("Output: Maximum non-overlapping intervals")
def interval_schedule(intervals: List[Tuple]) -> List[Tuple]:
    # TODO: Sort by end time (same as activity selection)
    pass

print("\n7. MAXIMUM PRODUCT SUBARRAY (GREEDY ELEMENTS)")
print("Input: Array of integers")
print("Output: Maximum product of contiguous subarray")
def max_product(nums: List[int]) -> int:
    # TODO: Track pos/neg products, greedy update
    pass

print("\n8. ASSIGN COOKIES TO CHILDREN")
print("Input: Children (desired sizes), Cookies (sizes)")
print("Output: Maximum children satisfied")
def assign_cookies(children: List[int], cookies: List[int]) -> int:
    # TODO: Sort both, greedily match smallest to smallest
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n9. MEETING ROOMS (MINIMUM ROOMS)")
print("Input: Meetings (start, end)")
print("Output: Minimum number of rooms needed")
def min_meeting_rooms(meetings: List[Tuple]) -> int:
    # TODO: Greedy with event-based approach
    pass

print("\n10. CONTAINER WITH MOST WATER (GREEDY ELEMENTS)")
print("Input: Array of heights")
print("Output: Maximum area between two lines")
def max_area(heights: List[int]) -> int:
    # TODO: Two-pointer greedy approach
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n11. GAS STATION (GREEDY CIRCULAR)")
print("Input: Gas at each station, cost to next station")
print("Output: Starting station index (-1 if impossible)")
def gas_station(gas: List[int], cost: List[int]) -> int:
    # TODO: Greedy with tracking balance
    pass

print("\n12. OPTIMAL REARRANGE (GREEDY + DP HYBRID)")
print("Input: String, number of operations")
print("Output: Lexicographically smallest string")
def optimal_rearrange(s: str, k: int) -> str:
    # TODO: Greedy character selection with constraints
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Greedy Algorithm Properties:

1. Greedy Choice Property:
   - Local optimal choice leads to global optimum
   - Make choice immediately without reconsidering
   - Example: Activity selection (earliest finish)

2. Optimal Substructure:
   - Optimal solution contains optimal subsolutions
   - Required for both greedy and DP
   - Example: MST problems

3. When Greedy Works:
   ✓ Activity Selection (earliest finish)
   ✓ Fractional Knapsack (value/weight ratio)
   ✓ Huffman Coding (min frequency merge)
   ✓ Dijkstra (min distance)
   ✓ MST (Kruskal, Prim)
   ✓ Job Sequencing (max profit first)

4. When Greedy Fails:
   ✗ 0/1 Knapsack (indivisible items)
   ✗ Coin Change (arbitrary coin sets)
   ✗ Some graph problems
   ✗ Weighted interval scheduling (complex)

Problem-Solving Strategy:

1. Identify greedy choice:
   - What locally optimal choice to make?
   - Does it work? Try examples.

2. Prove correctness:
   - Exchange argument: Show choice doesn't worsen solution
   - Induction: Prove inductively optimal
   - Counterexample: If exists, greedy fails

3. Implement efficiently:
   - Sorting: O(n log n)
   - Priority queue: O(n log n)
   - Union-find: O(α(n))

4. Compare with DP:
   - Greedy: Fast if works, doesn't guarantee optimal
   - DP: Slow but guaranteed optimal
   - Hybrid: Use greedy + DP elements

Common Patterns:

1. Sorting-Based:
   - Activity selection: sort by end time
   - Job sequencing: sort by profit
   - Interval scheduling: sort by start/end

2. Priority Queue-Based:
   - Huffman coding: min-heap
   - Dijkstra: min-heap (distance)
   - Prim's MST: min-heap (edge weight)

3. Two-Pointer Based:
   - Assign cookies: sort both, match
   - Container with water: expand/contract

4. Simulation-Based:
   - Gas station: track balance, try start
   - Meeting rooms: event-based tracking

Interview Tips:

1. Recognize greedy problems:
   - "Maximum/minimum number of..."
   - "Select items subject to constraint..."
   - "Optimal ordering..."

2. Don't assume greedy:
   - Test with examples
   - Look for counterexamples
   - Some problems need DP

3. Prove correctness:
   - Show greedy choice is optimal
   - Use exchange or induction argument
   - Discuss complexity

4. Implement carefully:
   - Handle edge cases (empty, single)
   - Use correct data structures
   - Optimize sorting/heap operations

Algorithm Classification:

Definitely Greedy:
✓ Activity Selection
✓ Huffman Coding
✓ Fractional Knapsack
✓ MST (Kruskal, Prim)
✓ Dijkstra (single-source shortest)

Conditional (Usually DP):
? 0/1 Knapsack → DP
? Coin Change → DP
? Weighted Interval → DP
? Longest Increasing → DP

Mixed (Greedy + Structure):
+ Gas Station (greedy simulation)
+ Meeting Rooms (greedy + counting)
+ Two-Sum variations (greedy pairs)

Complexity Reference:

Problem                 Best Approach   Time        Space
────────────────────────────────────────────────────────
Activity Selection      Greedy          O(n log n)  O(n)
Fractional Knapsack     Greedy          O(n log n)  O(n)
Huffman Coding          Greedy          O(n log n)  O(n)
Job Sequencing          Greedy          O(n²)       O(n)
0/1 Knapsack            DP              O(nW)       O(W)
Coin Change             DP              O(nC)       O(n)
MST                     Greedy (K/P)    O(E log E)  O(V)
Dijkstra                Greedy          O((V+E)logV) O(V)

Learning Progression:

1. Basic: Activity selection, fractional knapsack
2. Intermediate: Huffman, job sequencing
3. Advanced: MST, Dijkstra
4. Expert: Prove greedy vs find counterexamples

Next: Practice recognizing and proving greedy algorithms!
""")
