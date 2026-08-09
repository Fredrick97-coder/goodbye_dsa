"""
Examples: Greedy Algorithms

Demonstrate activity selection, Huffman coding, job sequencing, and more.
"""

import heapq
from typing import List, Tuple, Dict

print("=" * 70)
print("GREEDY ALGORITHMS")
print("=" * 70)

# ==================== (1) Activity Selection ====================
print("\n[1] Activity Selection (Maximum Non-Overlapping Activities)")
print("-" * 70)

def activity_selection(activities: List[Tuple]) -> List[Tuple]:
    """Select maximum non-overlapping activities"""
    # activities: list of (start, end) tuples
    activities.sort(key=lambda x: x[1])  # Sort by end time

    selected = [activities[0]]
    last_end = activities[0][1]

    for start, end in activities[1:]:
        if start >= last_end:
            selected.append((start, end))
            last_end = end

    return selected

activities = [(1, 3), (2, 5), (4, 6), (6, 7), (5, 8), (8, 9)]
selected = activity_selection(activities)

print("Activities (start, end):")
for act in activities:
    print(f"  {act}")

print(f"\nMaximum non-overlapping selection:")
for i, act in enumerate(selected, 1):
    print(f"  {i}. {act}")

print("→ Time: O(n log n), Space: O(n)")
print("→ Greedy choice (earliest finish) is optimal")

# ==================== (2) Huffman Coding ====================
print("\n[2] Huffman Coding (Optimal Prefix Codes)")
print("-" * 70)

class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def huffman_coding(text: str) -> Dict[str, str]:
    """Build Huffman tree and generate codes"""
    # Count character frequencies
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1

    # Special case: single character
    if len(freq) == 1:
        return {list(freq.keys())[0]: "0"}

    # Build min-heap
    heap = [Node(f, c) for c, f in freq.items()]
    heapq.heapify(heap)

    # Build Huffman tree
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
            if node.left:
                traverse(node.left, code + "0")
            if node.right:
                traverse(node.right, code + "1")

    traverse(root)
    return codes

text = "mississippi"
codes = huffman_coding(text)

print(f"Text: '{text}'")
print("\nCharacter frequencies:")
freq = {}
for char in text:
    freq[char] = freq.get(char, 0) + 1
for char, count in sorted(freq.items()):
    print(f"  {char}: {count}")

print("\nHuffman codes:")
for char, code in sorted(codes.items()):
    print(f"  {char}: {code}")

# Calculate compression
original_bits = len(text) * 8
encoded_bits = sum(freq[char] * len(codes[char]) for char in freq)
print(f"\nCompression: {original_bits} → {encoded_bits} bits ({encoded_bits/original_bits*100:.1f}%)")

print("→ Time: O(n log n), Space: O(n)")
print("→ Optimal prefix code with minimum average length")

# ==================== (3) Fractional Knapsack ====================
print("\n[3] Fractional Knapsack (Items Can Be Split)")
print("-" * 70)

def fractional_knapsack(items: List[Tuple], capacity: float) -> Tuple[float, List]:
    """Maximize value with weight constraint (items can be split)"""
    # items: list of (weight, value) tuples
    # Sort by value-to-weight ratio (descending)
    items_with_ratio = [(w, v, v / w) for w, v in items]
    items_with_ratio.sort(key=lambda x: x[2], reverse=True)

    total_value = 0
    total_weight = 0
    selected = []

    for weight, value, ratio in items_with_ratio:
        if total_weight + weight <= capacity:
            # Take whole item
            total_weight += weight
            total_value += value
            selected.append((weight, value, 1.0))
        else:
            # Take fraction
            remaining = capacity - total_weight
            if remaining > 0:
                fraction = remaining / weight
                total_value += value * fraction
                selected.append((weight, value, fraction))
            break

    return total_value, selected

items = [(10, 60), (20, 100), (30, 120)]
capacity = 50
max_value, selection = fractional_knapsack(items, capacity)

print("Items (weight, value):")
for w, v in items:
    print(f"  {(w, v)}: ratio = {v/w:.2f}")

print(f"\nCapacity: {capacity}")
print("Selection:")
for w, v, frac in selection:
    print(f"  Item (w={w}, v={v}): take {frac*100:.0f}% (value = {v*frac:.1f})")

print(f"\nTotal value: {max_value:.1f}")
print("→ Time: O(n log n), Space: O(n)")
print("→ Optimal greedy: take items by value/weight ratio")

# ==================== (4) Job Sequencing with Deadlines ====================
print("\n[4] Job Sequencing with Deadlines (Maximize Profit)")
print("-" * 70)

def job_sequencing(jobs: List[Tuple]) -> Tuple[int, List]:
    """Schedule jobs to maximize profit"""
    # jobs: list of (id, deadline, profit) tuples
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

jobs = [("J1", 2, 100), ("J2", 1, 50), ("J3", 3, 30), ("J4", 2, 40)]
max_profit, schedule = job_sequencing(jobs)

print("Jobs (id, deadline, profit):")
for job in jobs:
    print(f"  {job}")

print(f"\nOptimal schedule:")
for slot, job in enumerate(schedule, 1):
    print(f"  Slot {slot}: {job}")

print(f"Maximum profit: {max_profit}")
print("→ Time: O(n²), Space: O(n)")
print("→ Schedule high-profit jobs first")

# ==================== (5) Interval Scheduling ====================
print("\n[5] Interval Scheduling (Weighted - Maximize Value)")
print("-" * 70)

def weighted_interval_schedule(intervals: List[Tuple]) -> Tuple[int, List]:
    """Select non-overlapping intervals to maximize total weight"""
    # intervals: list of (start, end, weight) tuples
    # Note: This is actually DP, but shown for comparison
    intervals.sort(key=lambda x: x[1])

    n = len(intervals)
    dp = [0] * (n + 1)
    selected = [[]] * (n + 1)

    for i in range(1, n + 1):
        start, end, weight = intervals[i - 1]

        # Find last non-overlapping interval
        last = -1
        for j in range(i - 2, -1, -1):
            if intervals[j][1] <= start:
                last = j
                break

        # Include or exclude current interval
        include = weight + (dp[last + 1] if last >= 0 else 0)
        exclude = dp[i - 1]

        if include > exclude:
            dp[i] = include
            selected[i] = selected[last + 1] + [intervals[i - 1]]
        else:
            dp[i] = exclude
            selected[i] = selected[i - 1]

    return dp[n], selected[n]

intervals = [(1, 2, 50), (2, 3, 10), (1, 3, 40), (2, 5, 70), (4, 6, 60)]
max_weight, schedule = weighted_interval_schedule(intervals)

print("Intervals (start, end, weight):")
for interval in intervals:
    print(f"  {interval}")

print(f"\nOptimal non-overlapping selection:")
for interval in schedule:
    print(f"  {interval}")

print(f"Maximum weight: {max_weight}")
print("→ Time: O(n²), Space: O(n)")
print("→ Optimal requires DP, not pure greedy")

# ==================== (6) Greedy vs DP Comparison ====================
print("\n[6] Greedy vs DP: When Each Works")
print("-" * 70)

print("Greedy fails on Coin Change with arbitrary coins:")
coins = [1, 3, 4]
amount = 6

greedy_count = 0
remaining = amount
greedy_coins = []
for coin in sorted(coins, reverse=True):
    while remaining >= coin:
        greedy_coins.append(coin)
        remaining -= coin
        greedy_count += 1

print(f"  Coins: {coins}, Amount: {amount}")
print(f"  Greedy: {greedy_coins} = {greedy_count} coins (SUBOPTIMAL)")
print(f"  Optimal: [3, 3] = 2 coins (DP solution)")

print("\nGreedy works on Activity Selection:")
activities = [(1, 3), (2, 4), (4, 6), (6, 7)]
selected = activity_selection(activities)
print(f"  Activities: {activities}")
print(f"  Greedy (earliest finish): {selected}")
print(f"  Result: OPTIMAL ✓")

print("→ Not all problems have greedy solutions")
print("→ Always verify greedy correctness")

# ==================== (7) Greedy Algorithms Summary ====================
print("\n[7] Greedy Algorithm Properties")
print("-" * 70)

algorithms = {
    "Activity Selection": ("✓", "Earliest finish", "O(n log n)"),
    "Fractional Knapsack": ("✓", "Value/weight ratio", "O(n log n)"),
    "Huffman Coding": ("✓", "Min frequency merge", "O(n log n)"),
    "Job Sequencing": ("✓", "Max profit first", "O(n²)"),
    "Dijkstra": ("✓", "Min distance", "O((V+E) log V)"),
    "Prim's MST": ("✓", "Min edge", "O(E log V)"),
    "Kruskal's MST": ("✓", "Min edge + union", "O(E log E)"),
    "0/1 Knapsack": ("✗", "Fails", "Need DP"),
    "Coin Change": ("✗", "Fails on arbitrary", "Need DP"),
}

print(f"{'Algorithm':<25} {'Works':<8} {'Strategy':<25} {'Time':<15}")
print("-" * 73)

for algo, (works, strategy, time) in algorithms.items():
    print(f"{algo:<25} {works:<8} {strategy:<25} {time:<15}")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
