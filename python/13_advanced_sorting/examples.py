"""
Examples: Advanced Sorting Algorithms

Demonstrate merge sort, quick sort, heap sort, and non-comparison sorts.
"""

import random
import time
from typing import List

print("=" * 70)
print("ADVANCED SORTING ALGORITHMS")
print("=" * 70)

# ==================== (1) Merge Sort ====================
print("\n[1] Merge Sort (Divide & Conquer)")
print("-" * 70)

def merge_sort(arr: List[int]) -> List[int]:
    """Divide into halves, sort recursively, merge"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted arrays"""
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

arr = [38, 27, 43, 3, 9, 82, 10]
sorted_arr = merge_sort(arr)

print(f"Original: {arr}")
print(f"Sorted:   {sorted_arr}")
print("→ Time: O(n log n), Space: O(n)")
print("→ Always O(n log n), stable, extra space needed")

# ==================== (2) Quick Sort ====================
print("\n[2] Quick Sort (Divide & Conquer)")
print("-" * 70)

def quick_sort(arr: List[int], low: int = 0, high: int = None) -> List[int]:
    """Partition around pivot, sort recursively"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)

    return arr

def partition(arr: List[int], low: int, high: int) -> int:
    """Partition using last element as pivot"""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

arr = [38, 27, 43, 3, 9, 82, 10]
quick_sort(arr)

print(f"Original: [38, 27, 43, 3, 9, 82, 10]")
print(f"Sorted:   {arr}")
print("→ Time: O(n log n) avg, O(n²) worst")
print("→ In-place, cache-friendly, practical choice")
print("→ Use random pivot to avoid O(n²) on sorted data")

# ==================== (3) Heap Sort ====================
print("\n[3] Heap Sort")
print("-" * 70)

def heap_sort(arr: List[int]) -> List[int]:
    """Build max heap, extract elements in order"""
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, i, n)

    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_down(arr, 0, i)

    return arr

def heapify_down(arr: List[int], i: int, n: int):
    """Move element down to maintain heap property"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_down(arr, largest, n)

arr = [38, 27, 43, 3, 9, 82, 10]
heap_sort(arr)

print(f"Original: [38, 27, 43, 3, 9, 82, 10]")
print(f"Sorted:   {arr}")
print("→ Time: O(n log n) always")
print("→ In-place, O(1) space, guaranteed performance")
print("→ Used in real-time systems, not cache-friendly")

# ==================== (4) Counting Sort ====================
print("\n[4] Counting Sort (Non-Comparison)")
print("-" * 70)

def counting_sort(arr: List[int], max_val: int = None) -> List[int]:
    """Count frequency, reconstruct sorted array"""
    if not arr:
        return arr

    if max_val is None:
        max_val = max(arr)

    counts = [0] * (max_val + 1)

    # Count frequencies
    for num in arr:
        counts[num] += 1

    # Reconstruct
    idx = 0
    for num in range(max_val + 1):
        for _ in range(counts[num]):
            arr[idx] = num
            idx += 1

    return arr

arr = [4, 2, 8, 3, 9, 2, 1, 5]
counting_sort(arr, 9)

print(f"Original: [4, 2, 8, 3, 9, 2, 1, 5]")
print(f"Sorted:   {arr}")
print("→ Time: O(n + k) where k = range")
print("→ Space: O(k), not in-place")
print("→ Only for non-negative integers")

# ==================== (5) Radix Sort ====================
print("\n[5] Radix Sort (Non-Comparison)")
print("-" * 70)

def radix_sort(arr: List[int]) -> List[int]:
    """Sort by digits, least significant to most"""
    if not arr:
        return arr

    max_num = max(arr)
    exp = 1

    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr

def counting_sort_by_digit(arr: List[int], exp: int):
    """Count sort by single digit at position exp"""
    n = len(arr)
    output = [0] * n
    counts = [0] * 10

    for num in arr:
        digit = (num // exp) % 10
        counts[digit] += 1

    for i in range(1, 10):
        counts[i] += counts[i - 1]

    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[counts[digit] - 1] = arr[i]
        counts[digit] -= 1

    for i in range(n):
        arr[i] = output[i]

arr = [170, 45, 75, 90, 2, 8, 802, 24]
radix_sort(arr)

print(f"Original: [170, 45, 75, 90, 2, 8, 802, 24]")
print(f"Sorted:   {arr}")
print("→ Time: O(d × (n + k)) where d = digits")
print("→ Stable, good for large datasets")

# ==================== (6) Bucket Sort ====================
print("\n[6] Bucket Sort (Non-Comparison)")
print("-" * 70)

def bucket_sort(arr: List[float], num_buckets: int = 10) -> List[float]:
    """Distribute into buckets, sort each, concatenate"""
    if len(arr) == 0:
        return arr

    min_val = min(arr)
    max_val = max(arr)
    bucket_range = (max_val - min_val) / num_buckets

    # Create buckets
    buckets = [[] for _ in range(num_buckets)]

    # Distribute
    for num in arr:
        if num == max_val:
            idx = num_buckets - 1
        else:
            idx = int((num - min_val) / bucket_range)
        buckets[idx].append(num)

    # Sort and concatenate
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))

    return sorted_arr

arr = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
sorted_arr = bucket_sort(arr)

print(f"Original: {arr}")
print(f"Sorted:   {sorted_arr}")
print("→ Time: O(n + k) average, O(n²) worst")
print("→ Good for uniformly distributed data")

# ==================== (7) Shell Sort ====================
print("\n[7] Shell Sort (Adaptive Insertion)")
print("-" * 70)

def shell_sort(arr: List[int]) -> List[int]:
    """Insertion sort with increasing gaps"""
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i

            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = temp

        gap //= 2

    return arr

arr = [38, 27, 43, 3, 9, 82, 10]
shell_sort(arr)

print(f"Original: [38, 27, 43, 3, 9, 82, 10]")
print(f"Sorted:   {arr}")
print("→ Time: O(n log n) to O(n^1.5)")
print("→ In-place, simple implementation")

# ==================== (8) Algorithm Comparison ====================
print("\n[8] Performance Comparison")
print("-" * 70)

def benchmark_sorts(size: int):
    """Compare all sorting algorithms"""
    arr_base = [random.randint(0, 10000) for _ in range(size)]

    results = {}

    # Merge Sort
    arr = arr_base.copy()
    start = time.time()
    merge_sort(arr)
    results["Merge Sort"] = (time.time() - start) * 1000

    # Quick Sort
    arr = arr_base.copy()
    start = time.time()
    quick_sort(arr)
    results["Quick Sort"] = (time.time() - start) * 1000

    # Heap Sort
    arr = arr_base.copy()
    start = time.time()
    heap_sort(arr)
    results["Heap Sort"] = (time.time() - start) * 1000

    # Python's built-in
    arr = arr_base.copy()
    start = time.time()
    arr.sort()
    results["Timsort (built-in)"] = (time.time() - start) * 1000

    return results

print("Performance (in milliseconds):\n")
print(f"{'Algorithm':<20} {'1K items':<12} {'10K items':<12}")
print("-" * 44)

times_1k = benchmark_sorts(1000)
times_10k = benchmark_sorts(10000)

for algo in times_1k.keys():
    print(f"{algo:<20} {times_1k[algo]:>8.2f}ms", end="")
    print(f"  {times_10k[algo]:>8.2f}ms")

print("\n→ Quick Sort and Timsort most practical")
print("→ Merge Sort predictable O(n log n)")
print("→ Heap Sort good for guaranteed performance")

# ==================== (9) Stability Demonstration ====================
print("\n[9] Sorting Stability (Order Preservation)")
print("-" * 70)

def stable_sort_demo():
    """Show stable vs unstable sorting"""
    # Tuples: (value, original_index)
    data = [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd')]

    # Stable merge sort (preserves order of equal elements)
    print(f"Original: {data}")
    print(f"Stable:   {sorted(data)}")  # Python's sorted is stable
    print("→ Equal elements (3) keep original order: (3,'a') before (3,'c')")

stable_sort_demo()

print("→ Stable: Merge, Counting, Radix, Bucket, Insertion")
print("→ Unstable: Quick, Heap, Shell")

# ==================== (10) Complexity Summary ====================
print("\n[10] Algorithm Complexity Summary")
print("-" * 70)

algorithms = {
    "Merge Sort": ("O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Yes"),
    "Quick Sort": ("O(n log n)", "O(n log n)", "O(n²)", "O(log n)", "No"),
    "Heap Sort": ("O(n log n)", "O(n log n)", "O(n log n)", "O(1)", "No"),
    "Counting": ("O(n+k)", "O(n+k)", "O(n+k)", "O(k)", "Yes"),
    "Radix": ("O(dn+k)", "O(dn+k)", "O(dn+k)", "O(n)", "Yes"),
    "Bucket": ("O(n+k)", "O(n+k)", "O(n²)", "O(n)", "Yes"),
}

print(f"{'Algorithm':<15} {'Best':<12} {'Average':<12} {'Worst':<12} {'Space':<10} {'Stable':<8}")
print("-" * 69)

for algo, (best, avg, worst, space, stable) in algorithms.items():
    print(f"{algo:<15} {best:<12} {avg:<12} {worst:<12} {space:<10} {stable:<8}")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
