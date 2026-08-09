"""
Exercises: Introduction to DSA

Practice analyzing time and space complexity, and identifying patterns.
Solve these problems and identify the time complexity of your solution.
"""

from typing import List, Tuple

print("=" * 60)
print("EXERCISES: Introduction to DSA")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

# EASY 1: Find Maximum Element
print("\n1. FIND MAXIMUM ELEMENT")
print("Problem: Find the maximum element in an array")
print("Input: [3, 1, 4, 1, 5, 9, 2, 6]")
print("Output: 9")
print("\nWrite your solution:")

def find_max(arr: List[int]) -> int:
    """Find maximum element in array"""
    # TODO: Write your code here
    pass

# Test
test_arr = [3, 1, 4, 1, 5, 9, 2, 6]
# result = find_max(test_arr)
# print(f"Maximum: {result}")
# What is the time complexity? _____ (O(1), O(log n), O(n), O(n²), or other?)

# EASY 2: Count Occurrences
print("\n2. COUNT OCCURRENCES")
print("Problem: Count how many times a target appears in array")
print("Input: [1, 2, 2, 3, 2, 4], target=2")
print("Output: 3")
print("\nWrite your solution:")

def count_occurrences(arr: List[int], target: int) -> int:
    """Count occurrences of target in array"""
    # TODO: Write your code here
    pass

# Test
# result = count_occurrences([1, 2, 2, 3, 2, 4], 2)
# print(f"Count: {result}")
# What is the time complexity? _____

# EASY 3: Sum of Array
print("\n3. SUM OF ARRAY")
print("Problem: Calculate sum of all elements")
print("Input: [1, 2, 3, 4, 5]")
print("Output: 15")
print("\nWrite your solution:")

def array_sum(arr: List[int]) -> int:
    """Calculate sum of array"""
    # TODO: Write your code here
    pass

# EASY 4: Check if Element Exists
print("\n4. CHECK IF ELEMENT EXISTS")
print("Problem: Check if a target element exists in array")
print("Input: [10, 20, 30, 40], target=30")
print("Output: True")
print("\nWrite your solution:")

def element_exists(arr: List[int], target: int) -> bool:
    """Check if target exists in array"""
    # TODO: Write your code here
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

# MEDIUM 1: Find All Pairs with Sum
print("\n5. FIND ALL PAIRS WITH SUM")
print("Problem: Find all pairs of elements that sum to target")
print("Input: [2, 7, 11, 15], target=9")
print("Output: [(2, 7)]")
print("\nWrite your solution:")
print("Hint: Try both O(n²) and O(n) approaches")

def find_pairs_sum_naive(arr: List[int], target: int) -> List[Tuple[int, int]]:
    """Find pairs with sum - O(n²) approach"""
    # TODO: Write your code here (nested loop approach)
    pass

def find_pairs_sum_optimized(arr: List[int], target: int) -> List[Tuple[int, int]]:
    """Find pairs with sum - O(n) approach"""
    # TODO: Write your code here (use set or hash map)
    pass

# MEDIUM 2: Check Duplicates
print("\n6. CHECK FOR DUPLICATES")
print("Problem: Check if array has any duplicate elements")
print("Input: [1, 2, 3, 2, 1]")
print("Output: True")
print("\nWrite your solution:")
print("Hint: Try both O(n²) and O(n) approaches")

def has_duplicates_naive(arr: List[int]) -> bool:
    """Check duplicates - O(n²) approach"""
    # TODO: Write your code here
    pass

def has_duplicates_optimized(arr: List[int]) -> bool:
    """Check duplicates - O(n) approach"""
    # TODO: Write your code here
    pass

# MEDIUM 3: Missing Number
print("\n7. FIND MISSING NUMBER")
print("Problem: Array has numbers 1 to n, except one is missing")
print("Input: [1, 2, 4, 5] (missing 3)")
print("Output: 3")
print("\nWrite your solution:")
print("Hint: Can you do it in O(n) time and O(1) space?")

def find_missing_number(arr: List[int]) -> int:
    """Find missing number in sequence"""
    # TODO: Write your code here
    # Hint: Think about the sum formula: n*(n+1)/2
    pass

# MEDIUM 4: Merge Sorted Arrays
print("\n8. MERGE TWO SORTED ARRAYS")
print("Problem: Merge two sorted arrays into one sorted array")
print("Input: [1, 3, 5], [2, 4, 6]")
print("Output: [1, 2, 3, 4, 5, 6]")
print("\nWrite your solution:")

def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """Merge two sorted arrays"""
    # TODO: Write your code here
    # What is the time complexity?
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

# HARD 1: Find All Subarrays with Sum
print("\n9. FIND SUBARRAYS WITH SUM")
print("Problem: Find all contiguous subarrays that sum to target")
print("Input: [1, 2, 3, 1, 1, 1], target=3")
print("Output: Indices of start and end of subarrays")
print("\nWrite your solution:")
print("Hint: Use a hash map with cumulative sums")

def find_subarrays_with_sum(arr: List[int], target: int) -> List[Tuple[int, int]]:
    """Find subarrays with target sum"""
    # TODO: Write your code here
    pass

# HARD 2: Analyze Complexity
print("\n10. COMPLEXITY ANALYSIS")
print("Analyze the time complexity of the following function:")

def mystery_function(arr: List[int]) -> int:
    count = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i] == arr[j]:
                count += 1
    return count

print("""
def mystery_function(arr: List[int]) -> int:
    count = 0
    for i in range(len(arr)):        # Loop 1: runs n times
        for j in range(len(arr)):    # Loop 2: runs n times
            if arr[i] == arr[j]:     # Comparison: O(1)
                count += 1           # Operation: O(1)
    return count

What is the time complexity? _____
What is the space complexity? _____
""")

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

print("\n11. OPTIMIZE THIS FUNCTION")
print("""
Current implementation:
def find_closest_pair(arr: List[int]) -> Tuple[int, int]:
    min_diff = float('inf')
    pair = (0, 0)

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            diff = abs(arr[i] - arr[j])
            if diff < min_diff:
                min_diff = diff
                pair = (arr[i], arr[j])

    return pair

Problem: Current time complexity is O(n²)
Challenge: Optimize to O(n log n) by:
1. Sorting the array
2. Comparing only adjacent elements
3. Explain why this works
""")

def find_closest_pair_optimized(arr: List[int]) -> Tuple[int, int]:
    """Find pair with minimum difference"""
    # TODO: Implement the optimized version
    pass

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Key Points to Remember:
1. Always analyze time and space complexity
2. Identify loops and count iterations
3. Look for trade-offs (time vs space)
4. Optimize by:
   - Reducing nested loops
   - Using appropriate data structures
   - Sorting when it helps

Next: Move to Arrays & Lists (Topic 02)
""")
