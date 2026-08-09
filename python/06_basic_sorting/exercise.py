"""
Exercises: Basic Sorting Algorithms

Practice implementing and analyzing Bubble, Selection, and Insertion sorts.
Solve these problems and identify time/space complexity of your solution.
"""

from typing import List, Tuple

print("=" * 60)
print("EXERCISES: Basic Sorting Algorithms")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

# EASY 1: Implement Bubble Sort
print("\n1. IMPLEMENT BUBBLE SORT")
print("Problem: Sort array using bubble sort")
print("Input: [64, 34, 25, 12, 22, 11, 90]")
print("Output: [11, 12, 22, 25, 34, 64, 90]")
print("Bonus: Add early exit optimization")
print("\nWrite your solution:")

def bubble_sort(arr: List[int]) -> List[int]:
    """Bubble sort implementation"""
    # TODO: Write your code here
    pass

# EASY 2: Implement Selection Sort
print("\n2. IMPLEMENT SELECTION SORT")
print("Problem: Sort array using selection sort")
print("Input: [64, 34, 25, 12, 22, 11, 90]")
print("Output: [11, 12, 22, 25, 34, 64, 90]")
print("\nWrite your solution:")

def selection_sort(arr: List[int]) -> List[int]:
    """Selection sort implementation"""
    # TODO: Write your code here
    pass

# EASY 3: Implement Insertion Sort
print("\n3. IMPLEMENT INSERTION SORT")
print("Problem: Sort array using insertion sort")
print("Input: [64, 34, 25, 12, 22, 11, 90]")
print("Output: [11, 12, 22, 25, 34, 64, 90]")
print("\nWrite your solution:")

def insertion_sort(arr: List[int]) -> List[int]:
    """Insertion sort implementation"""
    # TODO: Write your code here
    pass

# EASY 4: Sort Descending
print("\n4. SORT IN DESCENDING ORDER")
print("Problem: Sort array in descending order")
print("Input: [3, 1, 4, 1, 5, 9, 2, 6]")
print("Output: [9, 6, 5, 4, 3, 2, 1, 1]")
print("Constraint: Modify comparison operator")
print("\nWrite your solution:")

def bubble_sort_descending(arr: List[int]) -> List[int]:
    """Bubble sort in descending order"""
    # TODO: Write your code here
    # Hint: Change comparison from > to <
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

# MEDIUM 1: Count Comparisons
print("\n5. COUNT COMPARISONS")
print("Problem: Count number of comparisons during bubble sort")
print("Input: [5, 2, 8, 1, 9]")
print("Output: (sorted_array, comparison_count)")
print("Comparisons: For each pass, count every comparison operation")
print("\nWrite your solution:")

def bubble_sort_count_comparisons(arr: List[int]) -> Tuple[List[int], int]:
    """Bubble sort returning array and comparison count"""
    # TODO: Write your code here
    # Each comparison in the inner loop counts as 1
    pass

# MEDIUM 2: Count Swaps
print("\n6. COUNT SWAPS")
print("Problem: Count number of swaps during bubble sort")
print("Input: [5, 2, 8, 1, 9]")
print("Output: (sorted_array, swap_count)")
print("Note: Swaps vary based on input (0 to n²/2)")
print("\nWrite your solution:")

def bubble_sort_count_swaps(arr: List[int]) -> Tuple[List[int], int]:
    """Bubble sort returning array and swap count"""
    # TODO: Write your code here
    # Count only actual swaps, not comparisons
    pass

# MEDIUM 3: Sort Objects
print("\n7. SORT OBJECTS BY KEY")
print("Problem: Sort list of tuples by first element")
print("Input: [(2, 'b'), (1, 'c'), (2, 'a'), (1, 'b')]")
print("Output: [(1, 'c'), (1, 'b'), (2, 'b'), (2, 'a')]")
print("Constraint: Use bubble sort, maintain stability if possible")
print("\nWrite your solution:")

def sort_tuples(arr: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
    """Sort tuples by first element using bubble sort"""
    # TODO: Write your code here
    # Change comparison to work on first element
    pass

# MEDIUM 4: Sort Strings
print("\n8. SORT STRINGS")
print("Problem: Sort list of strings alphabetically")
print("Input: ['zebra', 'apple', 'banana', 'cherry']")
print("Output: ['apple', 'banana', 'cherry', 'zebra']")
print("\nWrite your solution:")

def sort_strings(arr: List[str]) -> List[str]:
    """Sort strings using insertion sort"""
    # TODO: Write your code here
    # String comparison works with > and <
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

# HARD 1: Analyze Algorithm Performance
print("\n9. ANALYZE ALGORITHM PERFORMANCE")
print("Problem: Implement all three sorts and compare")
print("Task: Sort different types of arrays and report metrics")
print("""
Test on:
- Random array
- Already sorted array
- Reverse sorted array
- Array with duplicates

Report: time, comparisons, swaps for each
""")
print("\nWrite your solution:")

def performance_analysis(arr: List[int]) -> dict:
    """Analyze performance of different sorts"""
    # TODO: Write your code here
    # Return dict with metrics for bubble, selection, insertion
    # Example: {
    #     'bubble': {'time': 0.005, 'comparisons': 10, 'swaps': 5},
    #     'selection': {...},
    #     'insertion': {...}
    # }
    pass

# HARD 2: Adaptive Sorting
print("\n10. ADAPTIVE INSERTION SORT")
print("Problem: Insertion sort adapts to partially sorted arrays")
print("Demonstrate that nearly sorted arrays sort faster")
print("""
Test cases:
- [1, 2, 3, 4, 5] (already sorted)
- [1, 2, 4, 3, 5] (nearly sorted)
- [5, 4, 3, 2, 1] (reverse sorted)

Report comparisons for each
""")
print("\nWrite your solution:")

def compare_adaptive_performance(arrays: List[List[int]]) -> dict:
    """Compare insertion sort performance on different inputs"""
    # TODO: Write your code here
    # Return comparison counts for each array
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

# CHALLENGE 1: Bidirectional Bubble Sort
print("\n11. COCKTAIL SORT (BIDIRECTIONAL BUBBLE)")
print("Problem: Implement cocktail sort (alternates directions)")
print("""
Regular bubble sort: moves largest to right
Cocktail sort:
  - First pass: move largest to right
  - Second pass: move smallest to left
  - Repeat alternating directions

Advantage: Reduces passes needed for some inputs
""")
print("\nWrite your solution:")

def cocktail_sort(arr: List[int]) -> List[int]:
    """Cocktail sort - bidirectional bubble sort"""
    # TODO: Write your code here
    # Alternate between left->right and right->left passes
    pass

# CHALLENGE 2: Optimized Selection Sort
print("\n12. DOUBLE SELECTION SORT")
print("Problem: Optimize selection sort with two pointers")
print("""
Idea: In each pass, find BOTH min and max
- Put min at left
- Put max at right
- Reduces number of passes by ~50%

Find minimum and maximum simultaneously
""")
print("\nWrite your solution:")

def double_selection_sort(arr: List[int]) -> List[int]:
    """Selection sort finding min and max each pass"""
    # TODO: Write your code here
    # Two pointers: one for min, one for max
    # Place both in one pass
    pass

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Sorting Concepts to Master:
1. Basic implementations (Bubble, Selection, Insertion)
2. Time complexity analysis (best, average, worst)
3. Space complexity (all O(1) in-place)
4. Stability (maintains order of equal elements)
5. Swap and comparison counting
6. Adaptive behavior (e.g., insertion on nearly sorted)
7. Real-world vs. practical sorts

Key Differences:
- Bubble: Simple, early exit helps
- Selection: Consistent O(n²), minimizes swaps
- Insertion: Best for nearly sorted, O(n) best case

When to Use:
- Small arrays only (n < 50)
- Teaching/learning
- Nearly sorted data (insertion sort)
- Never in production (use built-in sort!)

Performance Tips:
✓ Add early exit to bubble sort
✓ Insertion sort for nearly sorted data
✓ Count comparisons/swaps to verify complexity
✓ Understand stable vs unstable
✓ Always use Python's sorted() in practice

Optimizations:
- Bidirectional bubble (cocktail sort)
- Double selection (min + max each pass)
- Adaptive insertion sort
- Hybrid approaches (small arrays as base case)

Next: Complete the project comparing all three algorithms
""")
