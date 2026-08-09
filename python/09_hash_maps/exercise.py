"""
Exercises: Hash Maps & Hash Tables

Practice hash map operations and solve common problems.
"""

from typing import List, Dict, Tuple
from collections import Counter, defaultdict

print("=" * 60)
print("EXERCISES: Hash Maps & Hash Tables")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

print("\n1. TWO SUM")
print("Input: Array, target sum")
print("Output: Indices of two numbers that add to target")
def two_sum(nums: List[int], target: int) -> List[int]:
    # TODO: Implement using hash map for O(n) solution
    pass

print("\n2. VALID ANAGRAM")
print("Input: Two strings s and t")
print("Output: Is t an anagram of s?")
def is_anagram(s: str, t: str) -> bool:
    # TODO: Implement using character frequency
    pass

print("\n3. CONTAINS DUPLICATE")
print("Input: Array of integers")
print("Output: Does array contain duplicates?")
def contains_duplicate(nums: List[int]) -> bool:
    # TODO: Implement using set
    pass

print("\n4. FIRST UNIQUE CHARACTER")
print("Input: String s")
print("Output: Index of first character appearing once")
def first_unique_char(s: str) -> int:
    # TODO: Implement using frequency map
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

print("\n5. GROUP ANAGRAMS")
print("Input: List of strings")
print("Output: Grouped by anagrams")
def group_anagrams(strs: List[str]) -> List[List[str]]:
    # TODO: Implement using sorted string as key
    pass

print("\n6. MAJORITY ELEMENT")
print("Input: Array where element appears > n/2 times")
print("Output: The majority element")
def majority_element(nums: List[int]) -> int:
    # TODO: Implement using Counter
    pass

print("\n7. VALID SUDOKU")
print("Input: 9x9 Sudoku board")
print("Output: Is it valid (no duplicates in rows/cols/boxes)?")
def is_valid_sudoku(board: List[List[str]]) -> bool:
    # TODO: Implement using hash sets for validation
    pass

print("\n8. WORD PATTERN")
print("Input: Pattern string and word string")
print("Output: Does word follow pattern?")
def word_pattern(pattern: str, s: str) -> bool:
    # TODO: Implement using two-direction mapping
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

print("\n9. LRU CACHE")
print("Input: Capacity, get/put operations")
print("Output: Cache with O(1) get/put")
def lru_cache_operations():
    # TODO: Implement using hash map + doubly linked list
    pass

print("\n10. LONGEST SUBSTRING WITHOUT REPEATING")
print("Input: String s")
print("Output: Length of longest substring without repeating characters")
def length_of_longest_substring(s: str) -> int:
    # TODO: Implement using sliding window + hash map
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

print("\n11. FIND ALL ANAGRAMS IN STRING")
print("Input: String s and pattern p")
print("Output: Indices where anagram of p starts in s")
def find_anagrams(s: str, p: str) -> List[int]:
    # TODO: Implement using sliding window with hash maps
    pass

print("\n12. MOST FREQUENT K ELEMENTS")
print("Input: Array nums, k")
print("Output: K most frequent elements")
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    # TODO: Implement using Counter and heap/bucket sort
    pass

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Hash Map Concepts:
- Insert/search/delete: O(1) average case
- Hash function: Maps keys to indices
- Collision resolution: Chaining or open addressing
- Load factor: Triggers rehashing at ~0.75

Key Problems:
- Two sum, anagrams, frequency counting
- Duplicate detection, first unique element
- Group anagrams, majority element
- LRU cache, sliding window with hash map
- Pattern matching, top K elements

Patterns:
- Frequency counting with Counter
- Complement tracking (two sum)
- Grouping by key (anagrams)
- Sliding window with hash map
- Two-direction mapping (pattern)
- Bucket sorting for top K

Common Pitfalls:
- Not handling hash collisions
- Assuming O(1) always (worst case O(n))
- Not using defaultdict for grouping
- Forgetting to check key existence

Next: Complete project with real hash map applications
""")
