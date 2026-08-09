"""
Examples: Arrays and Lists

Demonstrates array/list operations, complexity analysis, and common patterns.
"""

from typing import List

print("=" * 60)
print("ARRAYS AND LISTS - PRACTICAL EXAMPLES")
print("=" * 60)

# ==================== (1) Basic List Operations ====================
print("\n[1] Basic List Operations and Complexity")
print("-" * 40)

# Create list
arr = [10, 20, 30, 40, 50]
print(f"Original list: {arr}")

# Access (O(1))
print(f"First element [0]: {arr[0]}")
print(f"Last element [-1]: {arr[-1]}")
print(f"Element at index 2: {arr[2]}")

# Append to end (O(1) amortized)
arr.append(60)
print(f"After append(60): {arr}")

# Insert at beginning (O(n))
arr.insert(0, 5)
print(f"After insert(0, 5): {arr}")

# Remove last (O(1))
arr.pop()
print(f"After pop(): {arr}")

# Remove at specific index (O(n))
arr.pop(0)
print(f"After pop(0): {arr}")

# ==================== (2) Slicing ====================
print("\n[2] Slicing (Creates New List)")
print("-" * 40)

arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"Original: {arr}")

print(f"arr[2:5]    = {arr[2:5]}        (index 2,3,4)")
print(f"arr[:4]     = {arr[:4]}        (first 4)")
print(f"arr[6:]     = {arr[6:]}        (from index 6)")
print(f"arr[::2]    = {arr[::2]}      (every 2nd)")
print(f"arr[::-1]   = {arr[::-1]}  (reversed)")

# ==================== (3) List Comprehensions ====================
print("\n[3] List Comprehensions (Fast & Clean)")
print("-" * 40)

# Simple comprehension
squares = [x**2 for x in range(1, 6)]
print(f"Squares: {squares}")

# With condition
evens = [x for x in range(10) if x % 2 == 0]
print(f"Even numbers: {evens}")

# Nested
pairs = [(x, y) for x in range(1, 3) for y in range(1, 3)]
print(f"Pairs: {pairs}")

# String manipulation
words = ["hello", "world", "python"]
uppercase = [w.upper() for w in words]
print(f"Uppercase: {uppercase}")

# ==================== (4) Two-Pointer Technique ====================
print("\n[4] Two-Pointer Technique (Reverse String)")
print("-" * 40)

def reverse_array(arr: List[int]) -> List[int]:
    """Reverse array using two pointers"""
    arr = arr.copy()
    left, right = 0, len(arr) - 1

    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

    return arr

arr = [1, 2, 3, 4, 5]
print(f"Original: {arr}")
print(f"Reversed: {reverse_array(arr)}")
print("→ Two pointers swap elements from ends moving inward")

# ==================== (5) Two-Pointer: Merge Sorted Arrays ====================
print("\n[5] Two-Pointer: Merge Sorted Arrays")
print("-" * 40)

def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """Merge two sorted arrays"""
    result = []
    i, j = 0, 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    result.extend(arr1[i:])
    result.extend(arr2[j:])

    return result

arr1 = [1, 3, 5, 7]
arr2 = [2, 4, 6, 8]
merged = merge_sorted_arrays(arr1, arr2)
print(f"{arr1} + {arr2}")
print(f"= {merged}")
print("→ Time: O(n+m), Space: O(n+m)")

# ==================== (6) Sliding Window ====================
print("\n[6] Sliding Window: Max Sum in Window")
print("-" * 40)

def max_sum_window(arr: List[int], window_size: int) -> int:
    """Find maximum sum of any contiguous subarray of given size"""
    if window_size > len(arr):
        return sum(arr)

    # Calculate sum of first window
    window_sum = sum(arr[:window_size])
    max_sum = window_sum

    # Slide window
    for i in range(1, len(arr) - window_size + 1):
        window_sum = window_sum - arr[i - 1] + arr[i + window_size - 1]
        max_sum = max(max_sum, window_sum)

    return max_sum

arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
window_size = 3
result = max_sum_window(arr, window_size)
print(f"Array: {arr}")
print(f"Window size: {window_size}")
print(f"Maximum sum: {result} (which is 10+2+3=15)")
print("→ Time: O(n), Space: O(1)")

# ==================== (7) Prefix Sum ====================
print("\n[7] Prefix Sum: Fast Range Queries")
print("-" * 40)

def build_prefix_sum(arr: List[int]) -> List[int]:
    """Build prefix sum array"""
    prefix = [0]
    for num in arr:
        prefix.append(prefix[-1] + num)
    return prefix

def range_sum(prefix: List[int], left: int, right: int) -> int:
    """Get sum of arr[left:right+1] in O(1) using prefix sum"""
    return prefix[right + 1] - prefix[left]

arr = [1, 2, 3, 4, 5, 6]
prefix = build_prefix_sum(arr)
print(f"Array: {arr}")
print(f"Prefix: {prefix}")

# Query range sums in O(1)
print(f"Sum [0:2]: {range_sum(prefix, 0, 2)} (should be 1+2+3=6)")
print(f"Sum [1:4]: {range_sum(prefix, 1, 4)} (should be 2+3+4+5=14)")
print(f"Sum [3:5]: {range_sum(prefix, 3, 5)} (should be 4+5+6=15)")
print("→ Preprocessing: O(n), Queries: O(1)")

# ==================== (8) Remove Duplicates ====================
print("\n[8] Remove Duplicates")
print("-" * 40)

def remove_duplicates_list(arr: List[int]) -> List[int]:
    """Remove duplicates (unordered)"""
    return list(dict.fromkeys(arr))  # Preserves order in Python 3.7+

def remove_duplicates_sorted(arr: List[int]) -> List[int]:
    """Remove duplicates from sorted array in-place"""
    if len(arr) <= 1:
        return arr

    arr = arr.copy()
    write_idx = 1

    for read_idx in range(1, len(arr)):
        if arr[read_idx] != arr[read_idx - 1]:
            arr[write_idx] = arr[read_idx]
            write_idx += 1

    return arr[:write_idx]

arr = [1, 2, 2, 3, 3, 3, 4]
result = remove_duplicates_sorted(arr)
print(f"Original: {arr}")
print(f"Deduplicated: {result}")
print("→ Time: O(n), Space: O(1)")

# ==================== (9) Find Element ====================
print("\n[9] Find Operations")
print("-" * 40)

arr = [10, 20, 30, 20, 40]

# Find index (O(n))
if 30 in arr:
    print(f"Index of 30: {arr.index(30)}")

# Count occurrences (O(n))
count = arr.count(20)
print(f"Count of 20: {count}")

# Find all indices
indices = [i for i, x in enumerate(arr) if x == 20]
print(f"All indices of 20: {indices}")

# ==================== (10) Matrix Operations ====================
print("\n[10] 2D Arrays (Matrices)")
print("-" * 40)

# Create matrix
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

print("Matrix:")
for row in matrix:
    print(f"  {row}")

print(f"\nElement at [0][2]: {matrix[0][2]}")
print(f"Row 1: {matrix[1]}")
print(f"Column 0: {[row[0] for row in matrix]}")

# Transpose (swap rows and columns)
transposed = [[matrix[j][i] for j in range(len(matrix))]
              for i in range(len(matrix[0]))]
print(f"\nTransposed:")
for row in transposed:
    print(f"  {row}")

# ==================== (11) Performance Tips ====================
print("\n[11] Performance Comparison")
print("-" * 40)

import time

def append_method(n):
    """Building list with append"""
    arr = []
    for i in range(n):
        arr.append(i)
    return arr

def insert_method(n):
    """Building list with insert(0) - BAD PRACTICE"""
    arr = []
    for i in range(n):
        arr.insert(0, i)  # O(n) operation!
    return arr

n = 1000
print(f"Building list with {n} elements:")

# Append (efficient)
start = time.time()
append_method(n)
append_time = (time.time() - start) * 1000
print(f"  Using append():      {append_time:.3f} ms ✓")

# Insert (inefficient)
start = time.time()
insert_method(n)
insert_time = (time.time() - start) * 1000
print(f"  Using insert(0, x):  {insert_time:.3f} ms ✗")

print(f"  Difference: {insert_time/append_time:.1f}x slower!")
print("  → Always append() instead of insert(0, x)")

print("\n" + "=" * 60)
print("Next: Learn about Strings (Topic 03)")
print("=" * 60)
