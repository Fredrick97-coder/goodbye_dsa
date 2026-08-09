"""
Examples: Introduction to DSA

Demonstrates Big-O notation, time complexity analysis, and basic algorithm patterns.
"""

import time
from typing import List

print("=" * 60)
print("INTRODUCTION TO DATA STRUCTURES AND ALGORITHMS")
print("=" * 60)

# ==================== (1) O(1) - Constant Time ====================
print("\n[1] O(1) - Constant Time")
print("-" * 40)

def get_first_element(arr: List[int]) -> int:
    """Access first element - always 1 operation regardless of array size"""
    return arr[0]

arr = [10, 20, 30, 40, 50]
print(f"Array: {arr}")
print(f"First element: {get_first_element(arr)}")
print("→ Time: O(1) - Always 1 operation, regardless of size")

# ==================== (2) O(n) - Linear Time ====================
print("\n[2] O(n) - Linear Time")
print("-" * 40)

def find_sum(arr: List[int]) -> int:
    """Sum all elements - loops n times"""
    total = 0
    for num in arr:
        total += num
    return total

arr = [1, 2, 3, 4, 5]
print(f"Array: {arr}")
print(f"Sum: {find_sum(arr)}")
print("→ Time: O(n) - Loops through all n elements once")

# ==================== (3) O(n) - Linear Search ====================
print("\n[3] O(n) - Linear Search")
print("-" * 40)

def linear_search(arr: List[int], target: int) -> int:
    """Find target in unsorted array"""
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1

arr = [5, 2, 8, 1, 9]
target = 8
result = linear_search(arr, target)
print(f"Array: {arr}, Target: {target}")
print(f"Index found: {result}")
print("→ Time: O(n) - Worst case: iterate through all elements")

# ==================== (4) O(log n) - Binary Search ====================
print("\n[4] O(log n) - Binary Search")
print("-" * 40)

def binary_search(arr: List[int], target: int) -> int:
    """Find target in sorted array using binary search"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        print(f"  Checking mid={mid} (value={arr[mid]})", end="")

        if arr[mid] == target:
            print(" ✓ FOUND!")
            return mid
        elif arr[mid] < target:
            print(" → Search right")
            left = mid + 1
        else:
            print(" → Search left")
            right = mid - 1

    return -1

arr = [1, 3, 5, 7, 9, 11, 13, 15]
target = 7
print(f"Array (sorted): {arr}, Target: {target}")
result = binary_search(arr, target)
print(f"Result: {result}")
print("→ Time: O(log n) - Eliminates half of remaining elements each iteration")

# ==================== (5) O(n²) - Nested Loops ====================
print("\n[5] O(n²) - Nested Loops (Quadratic)")
print("-" * 40)

def find_pairs_with_sum(arr: List[int], target: int):
    """Find all pairs that sum to target"""
    pairs = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                pairs.append((arr[i], arr[j]))
    return pairs

arr = [1, 5, 7, -1, 5]
target = 6
print(f"Array: {arr}, Target sum: {target}")
result = find_pairs_with_sum(arr, target)
print(f"Pairs: {result}")
print("→ Time: O(n²) - Nested loops iterate through all pairs")

# ==================== (6) O(n²) - Bubble Sort ====================
print("\n[6] O(n²) - Bubble Sort")
print("-" * 40)

def bubble_sort(arr: List[int]) -> List[int]:
    """Sort array using bubble sort"""
    n = len(arr)
    arr_copy = arr.copy()

    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        if not swapped:
            break

    return arr_copy

arr = [64, 34, 25, 12, 22, 11, 90]
print(f"Original: {arr}")
sorted_arr = bubble_sort(arr)
print(f"Sorted: {sorted_arr}")
print("→ Time: O(n²) - Double nested loops")

# ==================== (7) Space Complexity Examples ====================
print("\n[7] Space Complexity - O(1) vs O(n)")
print("-" * 40)

def has_duplicates_space_efficient(arr: List[int]) -> bool:
    """Check duplicates with O(n) extra space"""
    seen = set()  # Extra O(n) space
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False

def has_duplicates_time_efficient(arr: List[int]) -> bool:
    """Check duplicates with O(1) extra space (but O(n²) time)"""
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False

arr = [1, 2, 3, 2, 4]
print(f"Array: {arr}")
print(f"Has duplicates (O(n) space): {has_duplicates_space_efficient(arr)}")
print(f"Has duplicates (O(1) space): {has_duplicates_time_efficient(arr)}")
print("→ Trade-off: Use more space for faster time, or less space for slower time")

# ==================== (8) Best, Average, Worst Case ====================
print("\n[8] Best, Average, Worst Case Analysis")
print("-" * 40)

def linear_search_verbose(arr: List[int], target: int) -> int:
    """Linear search with case analysis"""
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1

arr = [1, 2, 3, 4, 5]

# Best case: target at beginning
result = linear_search_verbose(arr, 1)
print(f"Best case - Target 1 at index {result}: O(1)")

# Average case: target in middle
result = linear_search_verbose(arr, 3)
print(f"Average case - Target 3 at index {result}: O(n)")

# Worst case: target not found
result = linear_search_verbose(arr, 10)
print(f"Worst case - Target 10 not found (index {result}): O(n)")

# ==================== (9) Comparing Algorithms ====================
print("\n[9] Comparing Algorithm Efficiency")
print("-" * 40)

def time_algorithm(func, arr, target=None):
    """Measure execution time of algorithm"""
    start = time.time()
    if target:
        func(arr, target)
    else:
        func(arr)
    end = time.time()
    return (end - start) * 1000  # Convert to milliseconds

arr_small = list(range(100))
arr_medium = list(range(1000))
arr_large = list(range(5000))

print("Time to find sum in arrays of different sizes:")
print(f"n=100:   {time_algorithm(find_sum, arr_small):.4f} ms")
print(f"n=1000:  {time_algorithm(find_sum, arr_medium):.4f} ms")
print(f"n=5000:  {time_algorithm(find_sum, arr_large):.4f} ms")
print("→ Linear: Time roughly proportional to input size")

# ==================== (10) When to Use Which ====================
print("\n[10] Algorithm Selection Guide")
print("-" * 40)

guide = {
    "O(1)": "Constant lookup, set operations → Use always!",
    "O(log n)": "Binary search → Very efficient, seek when possible",
    "O(n)": "Linear scan → Acceptable for most problems",
    "O(n log n)": "Efficient sorting → Close to optimal for comparison sorts",
    "O(n²)": "Nested loops → OK for n<10,000; risky for larger",
    "O(2ⁿ)": "Exponential → Only for very small n (n<20)",
}

for complexity, description in guide.items():
    print(f"{complexity:12} → {description}")

print("\n" + "=" * 60)
print("Next: Learn specific data structures and algorithms!")
print("=" * 60)
