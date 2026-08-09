"""
Examples: Basic Searching Algorithms

Demonstrate linear search, binary search, and search patterns.
"""

from typing import List, Tuple
import time

print("=" * 60)
print("BASIC SEARCHING - EXAMPLES")
print("=" * 60)

# ==================== (1) Linear Search ====================
print("\n[1] Linear Search (Sequential Search)")
print("-" * 40)

def linear_search(arr: List[int], target: int) -> int:
    """Search by checking each element"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

arr = [5, 2, 8, 1, 9, 3, 7]
targets = [8, 4, 3]

for target in targets:
    idx = linear_search(arr, target)
    result = f"index {idx}" if idx >= 0 else "not found"
    print(f"  Search for {target}: {result}")

print("→ Time: O(n), Space: O(1)")
print("→ Works on unsorted data")

# ==================== (2) Binary Search ====================
print("\n[2] Binary Search (Sorted Array)")
print("-" * 40)

def binary_search(arr: List[int], target: int) -> int:
    """Search on sorted array by dividing in half"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

sorted_arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
targets = [7, 1, 19, 4]

print(f"Array: {sorted_arr}\n")
for target in targets:
    idx = binary_search(sorted_arr, target)
    result = f"index {idx}" if idx >= 0 else "not found"
    print(f"  Search for {target}: {result}")

print("→ Time: O(log n), Space: O(1)")
print("→ Requires sorted array")

# ==================== (3) First & Last Occurrence ====================
print("\n[3] Find First and Last Occurrence")
print("-" * 40)

def find_first(arr: List[int], target: int) -> int:
    """Find first index of target"""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result

def find_last(arr: List[int], target: int) -> int:
    """Find last index of target"""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1  # Keep searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result

arr_with_dupes = [1, 2, 2, 2, 2, 3, 4, 5, 5, 5, 6]
target = 2

first = find_first(arr_with_dupes, target)
last = find_last(arr_with_dupes, target)

print(f"Array: {arr_with_dupes}")
print(f"Target: {target}")
print(f"First occurrence: index {first}")
print(f"Last occurrence: index {last}")
print(f"Count: {last - first + 1 if first >= 0 else 0}")

print("→ Time: O(log n), Space: O(1)")
print("→ Handles duplicates correctly")

# ==================== (4) Search Insert Position ====================
print("\n[4] Search Insert Position")
print("-" * 40)

def search_insert(arr: List[int], target: int) -> int:
    """Find position to insert target"""
    left, right = 0, len(arr)

    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left

sorted_arr = [1, 3, 5, 6, 9]
targets = [5, 7, 0, 10]

print(f"Array: {sorted_arr}\n")
for target in targets:
    pos = search_insert(sorted_arr, target)
    print(f"  Insert {target} at index {pos}")

print("→ Time: O(log n), Space: O(1)")
print("→ Useful for insertion operations")

# ==================== (5) Two-Pointer Sum ====================
print("\n[5] Two-Pointer Search (Two Sum)")
print("-" * 40)

def two_sum_sorted(arr: List[int], target: int) -> Tuple[int, int]:
    """Find two elements that sum to target"""
    left, right = 0, len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return None

sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
targets = [11, 5, 17]

print(f"Array: {sorted_arr}\n")
for target in targets:
    result = two_sum_sorted(sorted_arr, target)
    if result:
        i, j = result
        print(f"  {target} = {sorted_arr[i]} + {sorted_arr[j]} (indices {i}, {j})")
    else:
        print(f"  {target}: Not found")

print("→ Time: O(n), Space: O(1)")
print("→ Two pointers meet in middle")

# ==================== (6) Sliding Window ====================
print("\n[6] Sliding Window Search")
print("-" * 40)

def max_sum_subarray(arr: List[int], k: int) -> int:
    """Find max sum of k consecutive elements"""
    if len(arr) < k:
        return None

    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(len(arr) - k):
        window_sum = window_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, window_sum)

    return max_sum

arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
k = 4

max_sum = max_sum_subarray(arr, k)
print(f"Array: {arr}")
print(f"Window size: {k}")
print(f"Maximum sum in subarray: {max_sum}")

print("→ Time: O(n), Space: O(1)")
print("→ Efficient for fixed window operations")

# ==================== (7) Rotated Array Search ====================
print("\n[7] Rotated Array Binary Search")
print("-" * 40)

def search_rotated(arr: List[int], target: int) -> int:
    """Search in rotated sorted array"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid

        # Determine which half is properly sorted
        if arr[left] <= arr[mid]:
            # Left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1

# [4, 5, 6, 7, 0, 1, 2] is [0, 1, 2, 4, 5, 6, 7] rotated left by 4
rotated = [4, 5, 6, 7, 0, 1, 2]
targets = [0, 7, 3, 6]

print(f"Rotated array: {rotated}\n")
for target in targets:
    idx = search_rotated(rotated, target)
    result = f"index {idx}" if idx >= 0 else "not found"
    print(f"  Search for {target}: {result}")

print("→ Time: O(log n), Space: O(1)")
print("→ Handles rotated sorted arrays")

# ==================== (8) Linear vs Binary Comparison ====================
print("\n[8] Performance Comparison")
print("-" * 40)

def benchmark_searches(size: int, iterations: int = 100):
    """Compare linear vs binary search"""
    import random

    arr = list(range(size))
    targets = [random.randint(0, size - 1) for _ in range(iterations)]

    # Linear search
    start = time.time()
    for target in targets:
        linear_search(arr, target)
    linear_time = (time.time() - start) * 1000

    # Binary search
    start = time.time()
    for target in targets:
        binary_search(arr, target)
    binary_time = (time.time() - start) * 1000

    return linear_time, binary_time

print("Search 100 random elements in array:\n")
print(f"{'Size':<10} {'Linear':<12} {'Binary':<12} {'Speedup':<10}")
print("-" * 44)

for size in [1000, 10000, 100000]:
    linear, binary = benchmark_searches(size)
    speedup = linear / binary if binary > 0 else 0
    print(f"{size:<10} {linear:>6.2f}ms {'':<2} {binary:>6.2f}ms {'':<2} {speedup:>6.1f}x")

print("\n→ Binary search dramatically faster on large arrays")

# ==================== (9) Complexity Summary ====================
print("\n[9] Complexity Summary")
print("-" * 40)

algorithms = {
    "Linear Search": ("O(n)", "O(1)", "Any"),
    "Binary Search": ("O(log n)", "O(1)", "Sorted"),
    "Two-Pointer": ("O(n)", "O(1)", "Sorted"),
    "Sliding Window": ("O(n)", "O(1)", "Any"),
}

print(f"{'Algorithm':<20} {'Time':<15} {'Space':<10} {'Requires':<15}")
print("-" * 60)
for algo, (time, space, req) in algorithms.items():
    print(f"{algo:<20} {time:<15} {space:<10} {req:<15}")

print("\n" + "=" * 60)
print("Next: Solve search problems and build applications!")
print("=" * 60)
