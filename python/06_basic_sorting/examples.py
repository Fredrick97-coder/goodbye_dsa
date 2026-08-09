"""
Examples: Basic Sorting Algorithms

Demonstrates Bubble Sort, Selection Sort, and Insertion Sort with analysis.
"""

from typing import List, Tuple
import time

print("=" * 60)
print("BASIC SORTING ALGORITHMS - EXAMPLES")
print("=" * 60)

# ==================== (1) Bubble Sort ====================
print("\n[1] Bubble Sort - Simple but Inefficient")
print("-" * 40)

def bubble_sort(arr: List[int]) -> List[int]:
    """Bubble sort: compare adjacent and swap if needed"""
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  # Early exit if sorted

    return arr

arr = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {arr}")
sorted_arr = bubble_sort(arr)
print(f"Sorted:   {sorted_arr}")
print("→ Time: O(n²), Space: O(1), Stable: Yes")

# ==================== (2) Selection Sort ====================
print("\n[2] Selection Sort - Find Minimum Each Pass")
print("-" * 40)

def selection_sort(arr: List[int]) -> List[int]:
    """Selection sort: find min and place at beginning"""
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

arr = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {arr}")
sorted_arr = selection_sort(arr)
print(f"Sorted:   {sorted_arr}")
print("→ Time: O(n²), Space: O(1), Stable: No")

# ==================== (3) Insertion Sort ====================
print("\n[3] Insertion Sort - Build Sorted Array")
print("-" * 40)

def insertion_sort(arr: List[int]) -> List[int]:
    """Insertion sort: insert each element in correct position"""
    arr = arr.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

arr = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {arr}")
sorted_arr = insertion_sort(arr)
print(f"Sorted:   {sorted_arr}")
print("→ Time: O(n²) avg, O(n) best, Space: O(1), Stable: Yes")

# ==================== (4) Comparison on Different Data ====================
print("\n[4] Performance on Different Data Types")
print("-" * 40)

test_cases = [
    ([5, 2, 8, 1, 9], "Random"),
    ([1, 2, 3, 4, 5], "Already sorted"),
    ([5, 4, 3, 2, 1], "Reverse sorted"),
    ([3, 1, 3, 1, 3], "Duplicates"),
]

for arr, description in test_cases:
    result = insertion_sort(arr)
    print(f"{description:20} {arr} → {result}")

# ==================== (5) Counting Comparisons ====================
print("\n[5] Count Comparisons - Analyze Algorithm")
print("-" * 40)

def bubble_sort_with_count(arr: List[int]) -> Tuple[List[int], int]:
    """Bubble sort with comparison counter"""
    arr = arr.copy()
    comparisons = 0
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

    return arr, comparisons

arr = [5, 2, 8, 1, 9]
sorted_arr, comps = bubble_sort_with_count(arr)
print(f"Array: {arr}")
print(f"Comparisons: {comps}")
print(f"Expected: ~n²/2 = {len(arr) * (len(arr) - 1) // 2}")
print("→ O(n²) confirmed through counting")

# ==================== (6) Counting Swaps ====================
print("\n[6] Count Swaps - Measure Data Movement")
print("-" * 40)

def bubble_sort_swap_count(arr: List[int]) -> Tuple[List[int], int]:
    """Bubble sort with swap counter"""
    arr = arr.copy()
    swaps = 0
    n = len(arr)

    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    return arr, swaps

test_arrays = [
    ([1, 2, 3, 4, 5], "Already sorted"),
    ([5, 4, 3, 2, 1], "Reverse sorted"),
    ([3, 1, 4, 1, 5], "Random"),
]

print("Comparing swap counts:")
for arr, desc in test_arrays:
    _, swaps = bubble_sort_swap_count(arr)
    print(f"  {desc:20} → {swaps:2} swaps")

print("→ Swaps vary: 0 (sorted) to n²/2 (reverse)")

# ==================== (7) Stability Check ====================
print("\n[7] Stability - Maintain Order of Equal Elements")
print("-" * 40)

def bubble_sort_objects(arr: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
    """Bubble sort on tuples (first element)"""
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j][0] > arr[j + 1][0]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

data = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]
sorted_data = bubble_sort_objects(data)

print(f"Original: {data}")
print(f"Sorted:   {sorted_data}")
print("Note: (1,'b') before (1,'d') and (2,'a') before (2,'c')")
print("→ Bubble sort is STABLE (maintains order of equals)")

# ==================== (8) Insertion Sort on Nearly Sorted ====================
print("\n[8] Insertion Sort - Best on Nearly Sorted Data")
print("-" * 40)

def insertion_sort_with_count(arr: List[int]) -> Tuple[List[int], int]:
    """Insertion sort with comparison count"""
    arr = arr.copy()
    comparisons = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr, comparisons

# Compare on different datasets
datasets = [
    (list(range(1, 11)), "Already sorted"),
    ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], "Reverse sorted"),
    ([1, 2, 3, 4, 5, 6, 7, 10, 8, 9], "Nearly sorted"),
]

print("Insertion sort comparison counts:")
for arr, desc in datasets:
    _, comps = insertion_sort_with_count(arr)
    print(f"  {desc:20} → {comps:2} comparisons")

print("→ Nearly sorted: very few comparisons!")

# ==================== (9) Space Complexity ====================
print("\n[9] Space Complexity - In-Place Sorting")
print("-" * 40)

def verify_inplace(arr: List[int], sorted_arr: List[int]) -> bool:
    """Verify if original array was modified in-place"""
    return arr is sorted_arr

arr1 = [5, 2, 8, 1, 9]
result1 = bubble_sort(arr1)

print(f"Original array (before): {arr1}")
print(f"Returned array:           {result1}")
print(f"In-place? {arr1 is result1}")
print("→ All basic sorts: O(1) extra space")

# ==================== (10) Python Sorting Performance ====================
print("\n[10] Python's Built-In Sort (Always Use This!)")
print("-" * 40)

arr = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {arr}")

# Method 1: sorted() - returns new list
sorted_arr = sorted(arr)
print(f"sorted(): {sorted_arr}")

# Method 2: .sort() - modifies in place
arr_copy = arr.copy()
arr_copy.sort()
print(f".sort():  {arr_copy}")

print("→ Python uses Timsort: O(n log n) time, O(n) space")
print("→ Hybrid of merge sort + insertion sort")
print("→ Optimized for real-world data")

# ==================== (11) Timing Comparison ====================
print("\n[11] Timing Comparison on Larger Array")
print("-" * 40)

def benchmark_sort(sort_func, arr, name):
    """Measure sorting time"""
    start = time.time()
    sort_func(arr.copy())
    elapsed = (time.time() - start) * 1000
    return elapsed

# Test on array of 1000 elements
arr = list(range(1000, 0, -1))  # Worst case: reverse sorted

print("Sorting 1000 elements (reverse sorted):")
bubble_time = benchmark_sort(bubble_sort, arr, "Bubble")
selection_time = benchmark_sort(selection_sort, arr, "Selection")
insertion_time = benchmark_sort(insertion_sort, arr, "Insertion")

print(f"  Bubble Sort:    {bubble_time:.2f} ms")
print(f"  Selection Sort: {selection_time:.2f} ms")
print(f"  Insertion Sort: {insertion_time:.2f} ms")

# Compare to built-in
builtin_start = time.time()
sorted(arr)
builtin_time = (time.time() - builtin_start) * 1000

print(f"  Built-in sort:  {builtin_time:.2f} ms")
print(f"\n  Built-in is ~{bubble_time/builtin_time:.0f}x faster!")

# ==================== (12) Complexity Summary ====================
print("\n[12] Sorting Algorithm Complexity Summary")
print("-" * 40)

algorithms = {
    "Bubble Sort": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "Selection Sort": {"best": "O(n²)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "Insertion Sort": {"best": "O(n)", "avg": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
}

print(f"{'Algorithm':<18} {'Best':<8} {'Average':<8} {'Worst':<8} {'Space':<8}")
print("-" * 50)
for name, complexity in algorithms.items():
    print(f"{name:<18} {complexity['best']:<8} {complexity['avg']:<8} "
          f"{complexity['worst']:<8} {complexity['space']:<8}")

print("\n" + "=" * 60)
print("Next: Solve exercises and build comparison project!")
print("=" * 60)
