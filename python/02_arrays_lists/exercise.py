"""
Exercises: Arrays and Lists

Practice working with arrays, implementing algorithms, and analyzing complexity.
"""

from typing import List, Tuple

print("=" * 60)
print("EXERCISES: Arrays and Lists")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

# EASY 1: Find Second Maximum
print("\n1. FIND SECOND MAXIMUM")
print("Problem: Find the second largest element in array")
print("Input: [10, 20, 30, 40, 50]")
print("Output: 40")
print("\nYour solution:")

def find_second_max(arr: List[int]) -> int:
    """Find second maximum element"""
    # TODO: Write your code here
    pass

# EASY 2: Remove Duplicates
print("\n2. REMOVE DUPLICATES")
print("Problem: Remove duplicates from array")
print("Input: [1, 2, 2, 3, 3, 3, 4]")
print("Output: [1, 2, 3, 4]")
print("Note: Can you do it without using set()?")
print("\nYour solution:")

def remove_duplicates(arr: List[int]) -> List[int]:
    """Remove duplicates, preserve order"""
    # TODO: Write your code here
    pass

# EASY 3: Count Occurrences
print("\n3. COUNT ELEMENT OCCURRENCES")
print("Problem: Count how many times each element appears")
print("Input: [1, 2, 2, 3, 2, 4, 3]")
print("Output: {1: 1, 2: 3, 3: 2, 4: 1}")
print("\nYour solution:")

def count_elements(arr: List[int]) -> dict:
    """Count occurrences of each element"""
    # TODO: Write your code here
    pass

# EASY 4: Reverse Array
print("\n4. REVERSE ARRAY")
print("Problem: Reverse array in-place")
print("Input: [1, 2, 3, 4, 5]")
print("Output: [5, 4, 3, 2, 1]")
print("Bonus: Do it without using slicing or extra arrays")
print("\nYour solution:")

def reverse_array(arr: List[int]) -> List[int]:
    """Reverse array in-place"""
    # TODO: Write your code here
    # Hint: Use two pointers
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

# MEDIUM 1: Two Sum
print("\n5. TWO SUM")
print("Problem: Find two elements that sum to target")
print("Input: [2, 7, 11, 15], target=9")
print("Output: [0, 1] (indices of 2 and 7)")
print("Bonus: Solve in O(n) time")
print("\nYour solution:")

def two_sum(arr: List[int], target: int) -> Tuple[int, int]:
    """Find two elements that sum to target"""
    # TODO: Write your code here
    pass

# MEDIUM 2: Rotate Array
print("\n6. ROTATE ARRAY")
print("Problem: Rotate array right by k positions")
print("Input: [1, 2, 3, 4, 5], k=2")
print("Output: [4, 5, 1, 2, 3]")
print("Bonus: Can you do it in O(1) space?")
print("\nYour solution:")

def rotate_array(arr: List[int], k: int) -> List[int]:
    """Rotate array right by k positions"""
    # TODO: Write your code here
    pass

# MEDIUM 3: Merge Sorted Arrays
print("\n7. MERGE SORTED ARRAYS")
print("Problem: Merge two sorted arrays")
print("Input: [1, 3, 5], [2, 4, 6]")
print("Output: [1, 2, 3, 4, 5, 6]")
print("\nYour solution:")

def merge_sorted(arr1: List[int], arr2: List[int]) -> List[int]:
    """Merge two sorted arrays"""
    # TODO: Write your code here
    pass

# MEDIUM 4: Max Subarray Sum
print("\n8. MAXIMUM SUBARRAY SUM")
print("Problem: Find maximum sum of contiguous subarray")
print("Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]")
print("Output: 6 (subarray [4, -1, 2, 1])")
print("Bonus: This is Kadane's Algorithm!")
print("\nYour solution:")

def max_subarray_sum(arr: List[int]) -> int:
    """Find maximum subarray sum"""
    # TODO: Write your code here
    # Hint: Keep track of current sum and maximum sum
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

# HARD 1: Contains Duplicate II
print("\n9. CONTAINS DUPLICATE II")
print("Problem: Check if any element appears twice within k indices")
print("Input: [99, 99], k=2")
print("Output: True")
print("Input: [1, 0, 1, 1], k=1")
print("Output: False")
print("\nYour solution:")

def contains_duplicate_k(arr: List[int], k: int) -> bool:
    """Check if duplicate exists within k indices"""
    # TODO: Write your code here
    # Hint: Use sliding window
    pass

# HARD 2: Trapping Rain Water
print("\n10. TRAPPING RAIN WATER")
print("Problem: Calculate water trapped between elevation bars")
print("Input: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]")
print("Output: 6 (units of water trapped)")
print("Visual:")
print("""
        |                 |
    |   |   |         |   | |
| | | | | | | |   | | | | | | |
0 1 0 2 1 0 1 3 2 1 2 1
    Water: 1 unit + 1 unit + 2 units + 2 units = 6
""")
print("\nYour solution:")

def trap_rain_water(height: List[int]) -> int:
    """Calculate trapped water"""
    # TODO: Write your code here
    # Hint: For each position, trapped water = min(max_left, max_right) - height
    pass

# HARD 3: Product of Array Except Self
print("\n11. PRODUCT OF ARRAY EXCEPT SELF")
print("Problem: Calculate product of all elements except current")
print("Input: [1, 2, 3, 4]")
print("Output: [24, 12, 8, 6]")
print("Constraint: Do it without division and in O(n) space")
print("\nYour solution:")

def product_except_self(arr: List[int]) -> List[int]:
    """Calculate product except self"""
    # TODO: Write your code here
    # Hint: Use prefix and suffix products
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

# CHALLENGE 1: Sliding Window Maximum
print("\n12. SLIDING WINDOW MAXIMUM")
print("Problem: Find maximum in each sliding window")
print("Input: [1, 3, -1, -3, 5, 3, 6, 7], k=3")
print("Output: [3, 3, 5, 5, 6, 7]")
print("""
Window [1, 3, -1] → max = 3
       [3, -1, -3] → max = 3
       [-1, -3, 5] → max = 5
       [-3, 5, 3] → max = 5
       [5, 3, 6] → max = 6
       [3, 6, 7] → max = 7
""")
print("\nYour solution:")

def sliding_window_max(arr: List[int], k: int) -> List[int]:
    """Find maximum in each sliding window"""
    # TODO: Write your code here
    # Hint: Use deque (double-ended queue)
    pass

# CHALLENGE 2: Longest Consecutive Sequence
print("\n13. LONGEST CONSECUTIVE SEQUENCE")
print("Problem: Find length of longest consecutive elements sequence")
print("Input: [100, 4, 200, 1, 3, 2]")
print("Output: 4 (sequence is [1, 2, 3, 4])")
print("Constraint: O(n) time complexity")
print("\nYour solution:")

def longest_consecutive(arr: List[int]) -> int:
    """Find longest consecutive sequence"""
    # TODO: Write your code here
    # Hint: Use set for O(1) lookups
    pass

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Array Concepts to Master:
1. Indexing and slicing (understand O(n) for slicing!)
2. Two-pointer technique
3. Sliding window for efficient range operations
4. Prefix/suffix sums for range queries
5. Hash maps for O(1) lookups
6. In-place modifications to save space

Key Algorithms:
- Two sum
- Reverse array
- Rotate array
- Merge sorted arrays
- Kadane's algorithm (max subarray)
- Trapping rain water

Performance Tips:
- Use append() not insert(0)
- Use list comprehensions
- Avoid slicing in loops
- Consider space-time tradeoffs

Next: Topic 03 - Strings
""")
