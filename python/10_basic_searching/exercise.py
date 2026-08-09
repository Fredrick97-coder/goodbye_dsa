"""
Exercises: Basic Searching Algorithms

Practice searching techniques and solve common problems.
"""

from typing import List, Tuple, Optional

print("=" * 60)
print("EXERCISES: Basic Searching")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

print("\n1. BINARY SEARCH")
print("Input: Sorted array, target")
print("Output: Index of target, or -1 if not found")
def binary_search(nums: List[int], target: int) -> int:
    # TODO: Implement classic binary search
    pass

print("\n2. SEARCH INSERT POSITION")
print("Input: Sorted array, target")
print("Output: Index where target is or should be inserted")
def search_insert(nums: List[int], target: int) -> int:
    # TODO: Implement to find insertion position
    pass

print("\n3. FIRST BAD VERSION")
print("Input: Versions (0 to n), find first bad version")
print("Output: Index of first bad version")
def first_bad_version(n: int) -> int:
    # TODO: Implement binary search to find first bad
    pass

print("\n4. VALID PERFECT SQUARE")
print("Input: Number num")
print("Output: Is it a perfect square?")
def is_perfect_square(num: int) -> bool:
    # TODO: Implement using binary search
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

print("\n5. FIND FIRST AND LAST OCCURRENCE")
print("Input: Sorted array with duplicates, target")
print("Output: [first_index, last_index]")
def search_range(nums: List[int], target: int) -> List[int]:
    # TODO: Implement to find both first and last
    pass

print("\n6. TWO SUM II (SORTED ARRAY)")
print("Input: Sorted array, target sum")
print("Output: Indices of two numbers that sum to target")
def two_sum(numbers: List[int], target: int) -> List[int]:
    # TODO: Implement using two pointers
    pass

print("\n7. SEARCH IN ROTATED SORTED ARRAY")
print("Input: Rotated sorted array, target")
print("Output: Index of target, or -1")
def search_rotated(nums: List[int], target: int) -> int:
    # TODO: Implement binary search on rotated array
    pass

print("\n8. FIND MINIMUM IN ROTATED SORTED ARRAY")
print("Input: Rotated sorted array (no duplicates)")
print("Output: Minimum element")
def find_min(nums: List[int]) -> int:
    # TODO: Implement using modified binary search
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

print("\n9. SEARCH IN ROTATED SORTED ARRAY II (WITH DUPLICATES)")
print("Input: Rotated sorted array with duplicates, target")
print("Output: Is target present?")
def search_rotated_dup(nums: List[int], target: int) -> bool:
    # TODO: Implement handling duplicates in rotated array
    pass

print("\n10. LONGEST INCREASING SUBSEQUENCE")
print("Input: Array of integers")
print("Output: Length of longest increasing subsequence")
def length_of_lis(nums: List[int]) -> int:
    # TODO: Implement using binary search + dynamic approach
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

print("\n11. PEAK ELEMENT IN MOUNTAIN ARRAY")
print("Input: Mountain array (increases then decreases)")
print("Output: Index of peak element")
def peak_index(arr: List[int]) -> int:
    # TODO: Implement binary search to find peak
    pass

print("\n12. FIND K CLOSEST ELEMENTS")
print("Input: Sorted array, k, x")
print("Output: k elements closest to x")
def find_closest_elements(arr: List[int], k: int, x: int) -> List[int]:
    # TODO: Implement using two pointers or binary search
    pass

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Search Algorithms:
- Linear search: O(n), works on any data
- Binary search: O(log n), requires sorted data
- Two-pointer: O(n), for finding pairs/subarrays
- Sliding window: O(n), for contiguous elements

Key Problems:
- Binary search, search insert position
- First/last occurrence, valid perfect square
- Two sum sorted, rotated array search
- Find minimum in rotated, peak element
- K closest elements, longest increasing subsequence

Patterns:
- Standard binary search with left/right pointers
- Modified binary search (rotated, peak, minimum)
- Two-pointer for sorted array pairs
- Sliding window for subarray operations
- Edge cases: duplicates, rotated arrays

Binary Search Variants:
- Find exact match: return mid
- Find first: update result, move right = mid - 1
- Find last: update result, move left = mid + 1
- Find insertion: return left when not found

Common Pitfalls:
- Using mid = (left + right) // 2 (overflow risk)
- Not handling duplicates in rotated arrays
- Off-by-one errors in while condition
- Forgetting to update left/right pointers

Next: Complete project with real search applications
""")
