"""
Project: Algorithm Complexity Analyzer

Build a tool that:
1. Runs different sorting algorithms
2. Measures their execution time
3. Analyzes and compares their complexity
4. Visualizes results

This project reinforces understanding of:
- Time complexity
- Space complexity
- Trade-offs between algorithms
- Practical performance measurement
"""

import time
from typing import List, Callable, Tuple
import random

print("=" * 70)
print("PROJECT: Algorithm Complexity Analyzer")
print("=" * 70)

# ==================== PART 1: Implement Sorting Algorithms ====================
print("\n[PART 1] Implement Different Sorting Algorithms")
print("-" * 70)

def bubble_sort(arr: List[int]) -> List[int]:
    """
    Bubble Sort
    Time: O(n²) - Best: O(n)
    Space: O(1)
    Idea: Compare adjacent elements and swap if needed
    """
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

    return arr

def selection_sort(arr: List[int]) -> List[int]:
    """
    Selection Sort
    Time: O(n²)
    Space: O(1)
    Idea: Find minimum and place at beginning
    """
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

def insertion_sort(arr: List[int]) -> List[int]:
    """
    Insertion Sort
    Time: O(n²) - Best: O(n)
    Space: O(1)
    Idea: Insert each element into sorted portion
    """
    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr

def merge_sort(arr: List[int]) -> List[int]:
    """
    Merge Sort
    Time: O(n log n)
    Space: O(n)
    Idea: Divide, conquer, merge
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """Helper function for merge sort"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr: List[int]) -> List[int]:
    """
    Quick Sort
    Time: O(n log n) - Worst: O(n²)
    Space: O(log n) recursion
    Idea: Partition and recursively sort
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

# Verify all sorts work correctly
print("\n✓ Testing all sorting algorithms...")
test_arr = [64, 34, 25, 12, 22, 11, 90]
expected = sorted(test_arr)

algorithms = [
    ("Bubble Sort", bubble_sort),
    ("Selection Sort", selection_sort),
    ("Insertion Sort", insertion_sort),
    ("Merge Sort", merge_sort),
    ("Quick Sort", quick_sort),
]

for name, func in algorithms:
    result = func(test_arr)
    assert result == expected, f"{name} failed!"
    print(f"  ✓ {name}: {test_arr} → {result}")

# ==================== PART 2: Benchmark Algorithms ====================
print("\n[PART 2] Benchmark Algorithms on Different Input Sizes")
print("-" * 70)

def benchmark_algorithm(
    func: Callable,
    arr: List[int],
    name: str
) -> Tuple[float, bool]:
    """
    Run algorithm and measure execution time
    Returns: (time_in_ms, is_correct)
    """
    start_time = time.time()

    try:
        result = func(arr)
        end_time = time.time()
        elapsed = (end_time - start_time) * 1000  # Convert to milliseconds

        is_correct = result == sorted(arr)
        return elapsed, is_correct
    except Exception as e:
        return float('inf'), False

# Test on different array sizes
test_sizes = [100, 500, 1000, 2000]
results = {name: [] for name, _ in algorithms}

print("\nBenchmarking results (time in milliseconds):")
print(f"{'Size':<10} " + " | ".join(f"{name:<20}" for name, _ in algorithms))
print("-" * 120)

for size in test_sizes:
    # Generate random array
    test_array = [random.randint(1, 1000) for _ in range(size)]

    row = f"{size:<10}"

    for algo_name, func in algorithms:
        elapsed_ms, is_correct = benchmark_algorithm(func, test_array, algo_name)

        # Format time display
        if elapsed_ms == float('inf'):
            time_str = "ERROR"
        elif elapsed_ms < 0.01:
            time_str = "<0.01"
        else:
            time_str = f"{elapsed_ms:.2f}"

        row += f" | {time_str:<20}"
        results[algo_name].append((size, elapsed_ms))

    print(row)

# ==================== PART 3: Analyze Complexity ====================
print("\n[PART 3] Complexity Analysis")
print("-" * 70)

complexity_info = {
    "Bubble Sort": "O(n²) → Slow for large inputs",
    "Selection Sort": "O(n²) → Similar to bubble sort",
    "Insertion Sort": "O(n²) → But O(n) for nearly sorted",
    "Merge Sort": "O(n log n) → Consistent, uses more space",
    "Quick Sort": "O(n log n) avg → Worst case O(n²), but usually fast",
}

print("\nAlgorithm Complexity Comparison:")
for algo_name, complexity in complexity_info.items():
    print(f"  • {algo_name:<20} → {complexity}")

# ==================== PART 4: Compare Growth Rates ====================
print("\n[PART 4] Why O(n log n) beats O(n²)")
print("-" * 70)

print("\nFor n = 1000:")
print(f"  O(n²)    operations: {1000 * 1000:>10,} (Bubble, Selection, Insertion)")
print(f"  O(n log n) operations: {1000 * 10:>10,} (Merge Sort, Quick Sort)")
print(f"  Difference: {1000*1000 / (1000*10):.0f}x faster!")

print("\nFor n = 10,000:")
print(f"  O(n²)    operations: {10000 * 10000:>10,} (Quadratic sorts)")
print(f"  O(n log n) operations: {10000 * 13:>10,} (Linearithmic sorts)")
print(f"  Difference: {10000*10000 / (10000*13):.0f}x faster!")

print("\nFor n = 100,000:")
print(f"  O(n²)    operations: {100000 * 100000:>10,} (Not practical)")
print(f"  O(n log n) operations: {100000 * 17:>10,} (Still manageable)")

# ==================== PART 5: Best Practices ====================
print("\n[PART 5] When to Use Which Algorithm")
print("-" * 70)

recommendations = {
    "Bubble Sort": "Teaching/learning only. Never use in production.",
    "Selection Sort": "Teaching/learning only. Never use in production.",
    "Insertion Sort": "Small arrays (n < 50) or nearly sorted data.",
    "Merge Sort": "Need guaranteed O(n log n). Want stable sort.",
    "Quick Sort": "Most practical. Average case is very fast.",
    "Built-in sort()": "Always use Python's sorted() in production!",
}

print("\nRecommendations:")
for algo, rec in recommendations.items():
    print(f"  • {algo:<20} → {rec}")

# ==================== PART 6: Space Complexity Analysis ====================
print("\n[PART 6] Space Complexity Comparison")
print("-" * 70)

space_info = {
    "Bubble Sort": "O(1) - Sorts in place",
    "Selection Sort": "O(1) - Sorts in place",
    "Insertion Sort": "O(1) - Sorts in place",
    "Merge Sort": "O(n) - Needs extra array",
    "Quick Sort": "O(log n) - Recursion stack",
}

print("\nSpace Complexity:")
for algo, space in space_info.items():
    print(f"  • {algo:<20} → {space}")

# ==================== PART 7: Trade-offs ====================
print("\n[PART 7] Time vs Space Trade-offs")
print("-" * 70)

print("""
Bubble/Selection/Insertion Sort:
  ✓ O(1) space (very memory efficient)
  ✗ O(n²) time (slow for large inputs)
  → Use when memory is critical, n is small

Merge Sort:
  ✓ O(n log n) time (fast and consistent)
  ✗ O(n) space (uses extra memory)
  → Use when you want guaranteed performance

Quick Sort:
  ✓ O(n log n) avg time (very fast in practice)
  ✓ O(log n) space (recursive stack is small)
  ✗ O(n²) worst case (rare with good pivot)
  → Use for most practical applications
""")

# ==================== PART 8: Summary ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Key Learnings:

1. Different algorithms have different performance characteristics
   - O(n²) gets slow very quickly as n grows
   - O(n log n) scales much better
   - O(1) and O(log n) are nearly instant even for huge inputs

2. Big-O notation helps predict scalability
   - Analyze without actual measurements
   - Design better algorithms
   - Avoid inefficient solutions

3. Constants matter in practice
   - O(n log n) might be slower than O(n) with small n
   - But for large n, O(n log n) always wins

4. Real-world usage:
   - Never write custom sort in production
   - Understand complexity to choose the right tool
   - Know when to optimize and when to leave it alone

Next Steps:
1. Run this project with different input sizes
2. Modify array sizes and observe time differences
3. Try sorting random vs sorted vs reverse-sorted arrays
4. Compare with Python's built-in sort() using timeit module
5. Move to Topic 02: Arrays & Lists
""")

# ==================== BONUS: Test on Different Data ====================
print("\n[BONUS] Testing on Different Types of Data")
print("-" * 70)

# Sorted array (best case for insertion sort)
print("\n1. Nearly Sorted Array (best case for insertion sort):")
sorted_arr = list(range(100)) + [50]  # Almost sorted
t, _ = benchmark_algorithm(insertion_sort, sorted_arr, "Insertion Sort")
print(f"   Insertion Sort on nearly sorted: {t:.3f}ms")

# Reverse sorted (worst case for bubble sort)
print("\n2. Reverse Sorted Array (worst case for bubble sort):")
reverse_arr = list(range(100, 0, -1))
t, _ = benchmark_algorithm(bubble_sort, reverse_arr, "Bubble Sort")
print(f"   Bubble Sort on reverse sorted: {t:.3f}ms")

print("\n" + "=" * 70)
print("Project Complete! Move to Topic 02 for practical array operations.")
print("=" * 70)
