"""
Exercises: Strings and String Manipulation

Practice string algorithms, transformations, and pattern matching.
Solve these problems and identify the time/space complexity of your solution.
"""

from typing import List, Tuple

print("=" * 60)
print("EXERCISES: Strings and String Manipulation")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

# EASY 1: Reverse String
print("\n1. REVERSE STRING")
print("Problem: Reverse a string")
print("Input: 'hello'")
print("Output: 'olleh'")
print("Constraint: Do it without using [::-1] slicing")
print("\nYour solution:")

def reverse_string(s: str) -> str:
    """Reverse a string"""
    # TODO: Write your code here
    pass

# EASY 2: Check Palindrome
print("\n2. CHECK PALINDROME")
print("Problem: Check if string is palindrome (ignore case & spaces)")
print("Input: 'A man a plan a canal Panama'")
print("Output: True")
print("\nYour solution:")

def is_palindrome(s: str) -> bool:
    """Check if string is palindrome"""
    # TODO: Write your code here
    # Hint: Clean the string first (remove spaces, lowercase)
    pass

# EASY 3: Anagram Check
print("\n3. CHECK ANAGRAM")
print("Problem: Check if two strings are anagrams")
print("Input: 'listen', 'silent'")
print("Output: True")
print("Bonus: Solve in O(n) with hash map")
print("\nYour solution:")

def is_anagram(s1: str, s2: str) -> bool:
    """Check if strings are anagrams"""
    # TODO: Write your code here
    pass

# EASY 4: Count Vowels
print("\n4. COUNT VOWELS")
print("Problem: Count number of vowels in string")
print("Input: 'hello world'")
print("Output: 3 (e, o, o)")
print("\nYour solution:")

def count_vowels(s: str) -> int:
    """Count vowels in string"""
    # TODO: Write your code here
    # Vowels: a, e, i, o, u (case-insensitive)
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

# MEDIUM 1: First Unique Character
print("\n5. FIRST UNIQUE CHARACTER")
print("Problem: Find first character that appears only once")
print("Input: 'leetcode'")
print("Output: 0 (index of 'l')")
print("Input: 'loveleetcode'")
print("Output: 2 (index of 'v')")
print("Input: 'aabb'")
print("Output: -1 (no unique character)")
print("\nYour solution:")

def first_unique_char(s: str) -> int:
    """Find index of first unique character"""
    # TODO: Write your code here
    # Hint: Use hash map to count frequencies, then iterate once more
    pass

# MEDIUM 2: Valid Parentheses
print("\n6. VALID PARENTHESES")
print("Problem: Check if parentheses are balanced")
print("Input: '()'")
print("Output: True")
print("Input: '([)]'")
print("Output: False")
print("Note: This is a stack problem (Topic 04), but practice with strings")
print("\nYour solution:")

def is_valid_parentheses(s: str) -> bool:
    """Check if parentheses are valid"""
    # TODO: Write your code here
    # Hint: Use stack or recursion
    pass

# MEDIUM 3: Longest Substring Without Repeating
print("\n7. LONGEST SUBSTRING WITHOUT REPEATING")
print("Problem: Find length of longest substring without repeating chars")
print("Input: 'abcabcbb'")
print("Output: 3 ('abc')")
print("Input: 'bbbbb'")
print("Output: 1 ('b')")
print("Constraint: Use sliding window for O(n)")
print("\nYour solution:")

def length_of_longest_substring(s: str) -> int:
    """Find longest substring without repeating characters"""
    # TODO: Write your code here
    # Hint: Use sliding window with hash map
    pass

# MEDIUM 4: Rotate String
print("\n8. ROTATE STRING")
print("Problem: Check if one string is rotation of another")
print("Input: 'waterbottle', 'erbottlewat'")
print("Output: True")
print("Input: 'abcd', 'acdb'")
print("Output: False")
print("Constraint: Solve in O(n)")
print("\nYour solution:")

def is_rotation(s1: str, s2: str) -> bool:
    """Check if s2 is rotation of s1"""
    # TODO: Write your code here
    # Hint: s2 should appear in s1 + s1
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

# HARD 1: Longest Palindromic Substring
print("\n9. LONGEST PALINDROMIC SUBSTRING")
print("Problem: Find longest palindromic substring")
print("Input: 'babad'")
print("Output: 'bab' or 'aba'")
print("Input: 'cbbd'")
print("Output: 'bb'")
print("Constraint: Try to solve in O(n) or O(n²)")
print("\nYour solution:")

def longest_palindrome(s: str) -> str:
    """Find longest palindromic substring"""
    # TODO: Write your code here
    # Hint 1: Expand around center approach - O(n²)
    # Hint 2: Dynamic programming - O(n²) time, O(n²) space
    pass

# HARD 2: String Compression
print("\n10. STRING COMPRESSION")
print("Problem: Compress string by replacing repeated chars with count")
print("Input: 'aabbcc'")
print("Output: 'a2b2c2'")
print("Input: 'abcdef'")
print("Output: 'abcdef' (no compression if longer)")
print("Note: Return original if compressed is not shorter")
print("\nYour solution:")

def compress_string(s: str) -> str:
    """Compress string with character counts"""
    # TODO: Write your code here
    # Hint: Count consecutive chars, build new string efficiently
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

# CHALLENGE 1: Minimum Window Substring
print("\n11. MINIMUM WINDOW SUBSTRING")
print("Problem: Find smallest substring containing all chars from target")
print("Input: s = 'ADOBECODEBANC', t = 'ABC'")
print("Output: 'BANC' (length 4)")
print("Explanation: 'ADOBEC' also contains but is longer")
print("Constraint: Use sliding window for O(n)")
print("\nYour solution:")

def min_window_substring(s: str, t: str) -> str:
    """Find minimum window substring containing all chars from t"""
    # TODO: Write your code here
    # Time: O(n), Space: O(1) or O(26) for English
    # Hint: Use two pointers and hash map
    pass

# CHALLENGE 2: Edit Distance
print("\n12. EDIT DISTANCE (LEVENSHTEIN)")
print("Problem: Find minimum edits to transform one string to another")
print("Operations: insert, delete, replace (each counts as 1)")
print("Input: 'horse', 'ros'")
print("Output: 3")
print("Explanation: 'horse' → 'hose' → 'rose' → 'ros'")
print("Input: 'intention', 'execution'")
print("Output: 5")
print("\nYour solution:")

def edit_distance(s1: str, s2: str) -> int:
    """Calculate edit distance between two strings"""
    # TODO: Write your code here
    # Hint: Use dynamic programming
    # dp[i][j] = minimum edits to transform s1[0:i] to s2[0:j]
    pass

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
String Concepts to Master:
1. Immutability - strings can't be modified in place
2. Indexing & slicing - get characters and substrings
3. Two-pointer - solve palindrome problems
4. Sliding window - solve substring problems
5. Hash map/Counter - track character frequencies
6. Pattern matching - regex for complex patterns

Key Algorithms:
- Palindrome check (two-pointer)
- Anagram check (sorting or hashing)
- Substring search (naive or KMP)
- Longest substring without repeating (sliding window)
- Longest palindrome (expand around center or DP)
- Edit distance (dynamic programming)

Performance Tips:
✓ Use join() not += for building strings
✓ Use Counter/hash for frequency counting
✓ Two-pointer for palindromes
✓ Sliding window for substrings
✓ DP for optimization problems

Common Patterns:
1. Two-pointer: palindromes, valid sequences
2. Sliding window: substrings, anagrams
3. Hash map: frequencies, character sets
4. Dynamic programming: edit distance, longest palindrome
5. Regex: pattern matching, validation

Next: Complete the project with real-world string problems
""")
