"""
Project: Sorting Algorithm Analyzer & Comparison

Build a comprehensive tool that:
1. Implements all three basic sorts
2. Compares performance metrics
3. Analyzes on different data types
4. Visualizes results
5. Determines optimal use cases
6. Provides recommendations

This project applies:
- Sorting algorithm implementation
- Performance measurement
- Data analysis
- Algorithm comparison
- Real-world decision making
"""

import time
import random
from typing import List, Tuple, Dict, Callable

print("=" * 70)
print("PROJECT: Sorting Algorithm Analyzer & Comparison")
print("=" * 70)

# ==================== PART 1: Implement All Three Sorts ====================
print("\n[PART 1] Implement Three Basic Sorting Algorithms")
print("-" * 70)

class SortingAlgorithms:
    """Collection of basic sorting algorithms"""

    @staticmethod
    def bubble_sort(arr: List[int]) -> List[int]:
        """Bubble sort with early exit optimization"""
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

    @staticmethod
    def selection_sort(arr: List[int]) -> List[int]:
        """Selection sort - find minimum each iteration"""
        arr = arr.copy()
        n = len(arr)

        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

        return arr

    @staticmethod
    def insertion_sort(arr: List[int]) -> List[int]:
        """Insertion sort - build sorted array incrementally"""
        arr = arr.copy()

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1

            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1

            arr[j + 1] = key

        return arr

# Test implementations
test_arr = [64, 34, 25, 12, 22, 11, 90]
expected = sorted(test_arr)

sorts = {
    "Bubble Sort": SortingAlgorithms.bubble_sort,
    "Selection Sort": SortingAlgorithms.selection_sort,
    "Insertion Sort": SortingAlgorithms.insertion_sort,
}

print("Testing all implementations:")
for name, func in sorts.items():
    result = func(test_arr)
    status = "✓" if result == expected else "✗"
    print(f"  {name:<20} {status}")

# ==================== PART 2: Performance Metrics ====================
print("\n[PART 2] Measure Performance Metrics")
print("-" * 70)

class MetricsCollector:
    """Collect performance metrics for sorting algorithms"""

    @staticmethod
    def bubble_sort_metrics(arr: List[int]) -> Dict:
        """Bubble sort with detailed metrics"""
        arr = arr.copy()
        comparisons = 0
        swaps = 0
        n = len(arr)

        for i in range(n):
            swapped = False
            for j in range(n - 1 - i):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
                    swapped = True
            if not swapped:
                break

        return {
            "comparisons": comparisons,
            "swaps": swaps,
            "operations": comparisons + swaps,
        }

    @staticmethod
    def selection_sort_metrics(arr: List[int]) -> Dict:
        """Selection sort with detailed metrics"""
        arr = arr.copy()
        comparisons = 0
        swaps = 0
        n = len(arr)

        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                comparisons += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                swaps += 1

        return {
            "comparisons": comparisons,
            "swaps": swaps,
            "operations": comparisons + swaps,
        }

    @staticmethod
    def insertion_sort_metrics(arr: List[int]) -> Dict:
        """Insertion sort with detailed metrics"""
        arr = arr.copy()
        comparisons = 0
        swaps = 0

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1

            while j >= 0 and arr[j] > key:
                comparisons += 1
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1

            arr[j + 1] = key

        return {
            "comparisons": comparisons,
            "swaps": swaps,
            "operations": comparisons + swaps,
        }

# Compare metrics on different datasets
datasets = {
    "Random": [random.randint(1, 100) for _ in range(20)],
    "Sorted": list(range(1, 21)),
    "Reverse": list(range(20, 0, -1)),
    "Duplicates": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4] * 2,
}

print("Performance metrics on different datasets:\n")
for dataset_name, arr in datasets.items():
    print(f"{dataset_name} dataset: {arr[:5]}...")
    print(f"{'Algorithm':<18} {'Comparisons':<15} {'Swaps':<15} {'Total':<15}")
    print("-" * 60)

    bubble_m = MetricsCollector.bubble_sort_metrics(arr)
    selection_m = MetricsCollector.selection_sort_metrics(arr)
    insertion_m = MetricsCollector.insertion_sort_metrics(arr)

    print(f"{'Bubble':<18} {bubble_m['comparisons']:<15} {bubble_m['swaps']:<15} {bubble_m['operations']:<15}")
    print(f"{'Selection':<18} {selection_m['comparisons']:<15} {selection_m['swaps']:<15} {selection_m['operations']:<15}")
    print(f"{'Insertion':<18} {insertion_m['comparisons']:<15} {insertion_m['swaps']:<15} {insertion_m['operations']:<15}")
    print()

# ==================== PART 3: Timing Analysis ====================
print("\n[PART 3] Execution Time Comparison")
print("-" * 70)

def benchmark_sort(func: Callable, arr: List[int]) -> float:
    """Measure execution time of sort function"""
    start = time.time()
    func(arr.copy())
    return (time.time() - start) * 1000  # milliseconds

# Test on increasing sizes
sizes = [100, 500, 1000]
print(f"{'Size':<10} {'Bubble':<15} {'Selection':<15} {'Insertion':<15}")
print("-" * 55)

for size in sizes:
    arr = [random.randint(1, 1000) for _ in range(size)]

    bubble_time = benchmark_sort(SortingAlgorithms.bubble_sort, arr)
    selection_time = benchmark_sort(SortingAlgorithms.selection_sort, arr)
    insertion_time = benchmark_sort(SortingAlgorithms.insertion_sort, arr)

    print(f"{size:<10} {bubble_time:<15.3f} {selection_time:<15.3f} {insertion_time:<15.3f}")

print("\n→ All are O(n²), roughly same performance for small inputs")

# ==================== PART 4: Stability Check ====================
print("\n[PART 4] Stability Analysis")
print("-" * 70)

class StabilityTest:
    """Test if sorting algorithm is stable"""

    @staticmethod
    def bubble_sort_stable(arr: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
        """Bubble sort on tuples"""
        arr = arr.copy()
        n = len(arr)

        for i in range(n):
            for j in range(n - 1 - i):
                if arr[j][0] > arr[j + 1][0]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr

    @staticmethod
    def selection_sort_stable(arr: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
        """Selection sort on tuples"""
        arr = arr.copy()
        n = len(arr)

        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j][0] < arr[min_idx][0]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

        return arr

    @staticmethod
    def insertion_sort_stable(arr: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
        """Insertion sort on tuples"""
        arr = arr.copy()

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1

            while j >= 0 and arr[j][0] > key[0]:
                arr[j + 1] = arr[j]
                j -= 1

            arr[j + 1] = key

        return arr

# Test stability
test_data = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]
expected_stable = [(1, 'b'), (1, 'd'), (2, 'a'), (2, 'c')]

print("Testing stability on data: [(2,'a'), (1,'b'), (2,'c'), (1,'d')]")
print(f"Expected (stable): {expected_stable}\n")

bubble_result = StabilityTest.bubble_sort_stable(test_data)
selection_result = StabilityTest.selection_sort_stable(test_data)
insertion_result = StabilityTest.insertion_sort_stable(test_data)

print(f"Bubble sort:    {bubble_result}")
print(f"  Stable? {'✓ YES' if bubble_result == expected_stable else '✗ NO'}")

print(f"\nSelection sort: {selection_result}")
print(f"  Stable? {'✓ YES' if selection_result == expected_stable else '✗ NO'}")

print(f"\nInsertion sort: {insertion_result}")
print(f"  Stable? {'✓ YES' if insertion_result == expected_stable else '✗ NO'}")

# ==================== PART 5: Adaptive Behavior ====================
print("\n[PART 5] Adaptive Behavior Analysis")
print("-" * 70)

test_cases = [
    ("Already Sorted", list(range(1, 51))),
    ("Reverse Sorted", list(range(50, 0, -1))),
    ("Nearly Sorted", list(range(1, 51))[:-3] + [50, 48, 49]),
    ("Random", [random.randint(1, 100) for _ in range(50)]),
]

print("Comparing insertion sort performance on different inputs:")
print(f"{'Input Type':<20} {'Comparisons':<15} {'Adaptive?':<15}")
print("-" * 50)

for name, arr in test_cases:
    metrics = MetricsCollector.insertion_sort_metrics(arr)
    comps = metrics['comparisons']
    adaptive = "✓ YES" if comps < 50 * 49 / 2 else "✗ NO"
    print(f"{name:<20} {comps:<15} {adaptive:<15}")

print("\n→ Insertion sort is ADAPTIVE: better on nearly sorted data!")

# ==================== PART 6: Algorithm Selection Guide ====================
print("\n[PART 6] Algorithm Selection Guide")
print("-" * 70)

def recommend_algorithm(data_description: str) -> str:
    """Recommend sorting algorithm based on data characteristics"""
    recommendations = {
        "Very small array (n < 10)": "Any sort works, insertion is simplest",
        "Small array (n < 50)": "Insertion sort (O(n) if nearly sorted)",
        "Nearly sorted": "Insertion sort - O(n) best case!",
        "Random order": "Insertion sort (still O(n²) but simple)",
        "Large array": "Use Python's sorted() - it uses Timsort",
        "Memory critical": "Bubble or Selection (both O(1) space)",
        "Must be stable": "Bubble or Insertion (avoid Selection)",
        "Minimize writes": "Selection sort (minimizes swaps)",
    }
    return recommendations.get(data_description, "Unknown")

print("When to use each algorithm:\n")
for scenario, recommendation in {
    "Very small array (n < 10)": recommend_algorithm("Very small array (n < 10)"),
    "Small array (n < 50)": recommend_algorithm("Small array (n < 50)"),
    "Nearly sorted": recommend_algorithm("Nearly sorted"),
    "Must be stable": recommend_algorithm("Must be stable"),
    "Memory critical": recommend_algorithm("Memory critical"),
    "Production code": "ALWAYS use Python's sorted() or .sort()",
}.items():
    print(f"  {scenario:<25} → {recommendation}")

# ==================== PART 7: Summary & Learning ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Topics Covered:

1. Algorithm Implementation
   - All three basic sorts implemented
   - Verified correctness
   - Tested on various inputs

2. Performance Metrics
   - Comparison counting
   - Swap counting
   - Total operation counting
   - Different inputs affect performance

3. Timing Analysis
   - Real execution time measurement
   - Scaling with array size
   - All O(n²) confirmed empirically

4. Stability Analysis
   - Bubble: STABLE ✓
   - Selection: UNSTABLE ✗
   - Insertion: STABLE ✓

5. Adaptive Behavior
   - Insertion sort adapts to nearly sorted
   - Best case O(n) vs O(n²) average
   - Others don't adapt

6. Real-World Usage
   - All are O(1) space (in-place)
   - All are O(n²) worst case
   - Python's Timsort is better option
   - Understand for interviews/learning

Key Insights:

✓ Bubble sort: Simple, early exit helps, stable
✓ Selection sort: Consistent performance, unstable
✓ Insertion sort: Best for small/nearly sorted, stable
✓ All are impractical for production (use Timsort)
✓ Understanding them teaches algorithm analysis
✓ Trade-offs: simplicity vs stability vs performance

Complexity Summary:

Algorithm      | Best   | Average | Worst  | Space | Stable
Bubble         | O(n)   | O(n²)   | O(n²)  | O(1)  | Yes
Selection      | O(n²)  | O(n²)   | O(n²)  | O(1)  | No
Insertion      | O(n)   | O(n²)   | O(n²)  | O(1)  | Yes

When to Use (in interviews):

1. "Sort this array" → Implement quicksort or mergesort
2. "Explain sorting" → Talk about these three basics
3. "Optimize this sort" → Add early exit, adapt, etc.
4. "Compare sorts" → Time, space, stability, adaptivity
5. "Real code" → ALWAYS use built-in sort()

Learning Value:

✓ Teaches algorithm analysis basics
✓ Understand best/average/worst cases
✓ Learn about stability and in-place
✓ Foundation for advanced algorithms
✓ Interview preparation

Next Steps:
1. Master these three thoroughly
2. Learn quicksort and mergesort
3. Understand Timsort (Python's sort)
4. Practice on LeetCode/HackerRank
5. Move to intermediate data structures
""")

print("=" * 70)
print("Project Complete! Topic 06 Finished Successfully!")
print("=" * 70)
print("\n🎉 BEGINNER LEVEL COMPLETE! 🎉")
print("All 6 beginner topics are now finished!")
print("Ready to move to intermediate level (Topics 07-11)")
