"""
Exercises: Advanced Sorting Algorithms

Practice implementing and applying sorting algorithms.
"""

from typing import List

print("=" * 70)
print("EXERCISES: Advanced Sorting Algorithms")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. IMPLEMENT MERGE SORT")
print("Input: Array of integers")
print("Output: Sorted array")
def merge_sort(arr: List[int]) -> List[int]:
    # TODO: Implement merge sort (divide into halves, merge)
    pass

print("\n2. IMPLEMENT QUICK SORT")
print("Input: Array of integers")
print("Output: Sorted array")
def quick_sort(arr: List[int]) -> List[int]:
    # TODO: Implement quick sort (partition around pivot)
    pass

print("\n3. IMPLEMENT HEAP SORT")
print("Input: Array of integers")
print("Output: Sorted array")
def heap_sort(arr: List[int]) -> List[int]:
    # TODO: Implement heap sort (build heap, extract elements)
    pass

print("\n4. COUNTING SORT")
print("Input: Array of non-negative integers, max value")
print("Output: Sorted array")
def counting_sort(arr: List[int], max_val: int) -> List[int]:
    # TODO: Implement counting sort (count frequencies)
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n5. RADIX SORT")
print("Input: Array of non-negative integers")
print("Output: Sorted array")
def radix_sort(arr: List[int]) -> List[int]:
    # TODO: Implement radix sort (sort by digits)
    pass

print("\n6. BUCKET SORT")
print("Input: Array of floats [0, 1)")
print("Output: Sorted array")
def bucket_sort(arr: List[float]) -> List[float]:
    # TODO: Implement bucket sort (distribute into buckets)
    pass

print("\n7. SORT WITH CUSTOM COMPARATOR")
print("Input: Array of tuples (value, priority)")
print("Output: Sorted by priority first, then value")
def custom_sort(items: List[tuple]) -> List[tuple]:
    # TODO: Implement using any algorithm with custom key
    pass

print("\n8. MERGE K SORTED ARRAYS")
print("Input: List of sorted arrays")
print("Output: Single merged sorted array")
def merge_k_arrays(arrays: List[List[int]]) -> List[int]:
    # TODO: Implement merge using divide and conquer
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n9. QUICK SELECT (Find Kth Smallest)")
print("Input: Array, k")
print("Output: Kth smallest element (O(n) expected)")
def quick_select(arr: List[int], k: int) -> int:
    # TODO: Implement quick select using partition
    pass

print("\n10. INVERSION COUNT")
print("Input: Array of integers")
print("Output: Number of inversions (i < j but arr[i] > arr[j])")
def count_inversions(arr: List[int]) -> int:
    # TODO: Use merge sort to count inversions in O(n log n)
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n11. SORT ARRAY WITH RANGE CONSTRAINTS")
print("Input: Array where each element at index i is at most k positions away")
print("Output: Sorted array efficiently")
def sort_nearly_sorted(arr: List[int], k: int) -> List[int]:
    # TODO: Use min-heap of size k for O(n log k)
    pass

print("\n12. MULTIKEY SORT (STABLE SORT GUARANTEE)")
print("Input: Array of tuples with multiple keys")
print("Output: Sorted by primary key, secondary key, etc (stable)")
def multikey_sort(items: List[tuple], keys: List[int]) -> List[tuple]:
    # TODO: Implement stable multikey sorting
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Sorting Algorithm Categories:

Comparison-Based:
- Merge Sort: O(n log n), stable, extra space
- Quick Sort: O(n log n) avg, in-place, practical
- Heap Sort: O(n log n) guaranteed, O(1) space
- Shell Sort: O(n^1.5), in-place, adaptive

Non-Comparison:
- Counting Sort: O(n+k), limited to small ranges
- Radix Sort: O(d*(n+k)), stable, fixed digits
- Bucket Sort: O(n+k) avg, good for uniform distribution

Algorithm Selection:

For General Purpose:
✓ Quick Sort (practical, in-place, cache-friendly)
✓ Merge Sort (guaranteed, stable)
✓ Python's Timsort (hybrid, adaptive)

For Specific Constraints:
✓ Heap Sort: guaranteed O(n log n), O(1) space
✓ Counting Sort: small integer range
✓ Radix Sort: multiple sort keys, large data
✓ Bucket Sort: floating point, uniform distribution

For Special Cases:
✓ Insertion Sort: nearly sorted, small arrays
✓ Bubble Sort: educational, almost sorted
✓ Shell Sort: simple O(n^1.5)

Important Concepts:

1. Stability: Preserve order of equal elements
   - Matters when sorting objects by one attribute
   - Stable: Merge, Counting, Radix, Bucket
   - Unstable: Quick, Heap

2. In-Place: Don't need extra space
   - Memory critical: Quick, Heap, Shell
   - Can use extra: Merge, Counting, Radix

3. Adaptive: Fast on nearly sorted data
   - Insertion Sort: O(n) on sorted
   - Bubble Sort: O(n) on sorted
   - Timsort: detects runs

4. Cache Friendly:
   - Quick Sort: good locality
   - Merge Sort: sequential access
   - Heap Sort: poor locality (random jumps)

5. Worst Case Avoidance:
   - Quick Sort: randomized pivot avoids O(n²)
   - Merge Sort: always O(n log n)
   - Heap Sort: always O(n log n)

Advanced Topics:

1. External Sorting:
   - Sorting data larger than RAM
   - Merge sort with disk I/O

2. Parallel Sorting:
   - Quick sort: divide into partitions
   - Merge sort: merge in parallel
   - Bitonic sort: parallel hardware

3. Specialized Sorts:
   - Topological sort: DAG ordering
   - Counting sort: histogram equalization
   - Radix sort: numerical analysis

4. Lower Bounds:
   - Comparison-based: Ω(n log n) lower bound
   - Non-comparison: can beat with O(n+k)

Common Mistakes:

1. Using O(n²) sorts on large data
2. Not considering stability requirement
3. Ignoring cache effects
4. Bad pivot choice in Quick Sort
5. Not handling edge cases (empty, single element)
6. Assuming all sorts are equal performance

Practice Tips:

1. Implement all O(n log n) sorts
2. Understand divide-and-conquer
3. Know stability of each algorithm
4. Practice custom comparators
5. Benchmark on real data
6. Understand space vs time tradeoffs
7. Handle duplicates correctly

Interview Tips:

✓ Merge Sort: explain divide/conquer, merge process
✓ Quick Sort: pivot selection, partitioning
✓ Heap Sort: heap structure, heapify operations
✓ Know when to use each (trade-offs)
✓ Implement one from scratch
✓ Explain stability and space complexity
✓ Discuss worst-case scenarios

Next: Implement sorting algorithms and optimize for real scenarios!
""")
