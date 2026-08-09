"""
Examples: Strings and String Manipulation

Demonstrates string operations, algorithms, and common patterns.
"""

from typing import List
from collections import Counter
import re

print("=" * 60)
print("STRINGS AND STRING MANIPULATION - EXAMPLES")
print("=" * 60)

# ==================== (1) Basic String Operations ====================
print("\n[1] Basic String Operations")
print("-" * 40)

s = "hello world"
print(f"String: '{s}'")
print(f"Length: {len(s)} (O(1))")
print(f"First char: '{s[0]}' (O(1))")
print(f"Last char: '{s[-1]}' (O(1))")
print(f"Substring [0:5]: '{s[0:5]}' (O(n))")
print(f"Reversed: '{s[::-1]}' (O(n))")
print(f"Upper: '{s.upper()}' (O(n))")
print(f"Contains 'world': {'world' in s} (O(n))")
print("→ Different operations have different complexities")

# ==================== (2) String Immutability ====================
print("\n[2] String Immutability")
print("-" * 40)

original = "hello"
print(f"Original: {original}")

# Creating new strings (not modifying original)
modified1 = original + " world"
modified2 = original.upper()
modified3 = original.replace("l", "L")

print(f"After '+': {original} (unchanged!)")
print(f"Upper version: {modified2}")
print(f"Replaced version: {modified3}")
print("→ Strings are immutable, operations create new strings")

# ==================== (3) Efficient String Building ====================
print("\n[3] Efficient String Building")
print("-" * 40)

chars = ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']

# Inefficient way (O(n²) - creates new string each time)
result_bad = ""
for char in chars[:3]:  # Just first 3 for demo
    result_bad += char
print(f"Using += (BAD for loops): '{result_bad}'")

# Efficient way (O(n) - builds once)
result_good = "".join(chars)
print(f"Using join() (GOOD): '{result_good}'")
print("→ Always use ''.join() for building strings in loops!")

# ==================== (4) Palindrome Check ====================
print("\n[4] Palindrome Check - Two-Pointer Technique")
print("-" * 40)

def is_palindrome(s: str) -> bool:
    """Check if string is palindrome using two-pointer"""
    s = s.lower().replace(" ", "")
    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1

    return True

test_cases = [
    "racecar",
    "madam",
    "hello",
    "A man a plan a canal Panama",
]

print("Testing palindromes:")
for test in test_cases:
    result = is_palindrome(test)
    status = "✓" if result else "✗"
    print(f"  '{test}' → {result} {status}")

print("→ Time: O(n), Space: O(1) with two-pointer")

# ==================== (5) Anagram Check ====================
print("\n[5] Anagram Check")
print("-" * 40)

def is_anagram_sort(s1: str, s2: str) -> bool:
    """Check anagram using sorting"""
    return sorted(s1.lower()) == sorted(s2.lower())

def is_anagram_hash(s1: str, s2: str) -> bool:
    """Check anagram using hash map (Counter)"""
    return Counter(s1.lower()) == Counter(s2.lower())

pairs = [
    ("listen", "silent"),
    ("hello", "world"),
    ("abc", "cab"),
]

print("Testing anagrams:")
for s1, s2 in pairs:
    result_sort = is_anagram_sort(s1, s2)
    result_hash = is_anagram_hash(s1, s2)
    status = "✓" if result_sort else "✗"
    print(f"  '{s1}' vs '{s2}' → {result_sort} {status}")

print("→ Sort: O(n log n), Hash: O(n)")

# ==================== (6) Reverse String ====================
print("\n[6] Reverse String")
print("-" * 40)

def reverse_string_slice(s: str) -> str:
    """Reverse using slicing"""
    return s[::-1]

def reverse_string_manual(s: str) -> str:
    """Reverse manually - good to understand"""
    result = ""
    for i in range(len(s) - 1, -1, -1):
        result += s[i]
    return result

def reverse_string_efficient(s: str) -> str:
    """Reverse efficiently using join and reversed()"""
    return "".join(reversed(s))

s = "hello"
print(f"Original: {s}")
print(f"Slicing: {reverse_string_slice(s)}")
print(f"Manual loop: {reverse_string_manual(s)}")
print(f"Using reversed(): {reverse_string_efficient(s)}")
print("→ All O(n), slicing is most Pythonic")

# ==================== (7) Substring Search ====================
print("\n[7] Substring Search")
print("-" * 40)

def find_substring(text: str, pattern: str) -> int:
    """Find first occurrence of pattern"""
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i+len(pattern)] == pattern:
            return i
    return -1

text = "hello world, hello python"
patterns = ["world", "hello", "xyz"]

print(f"Text: '{text}'")
for pattern in patterns:
    index = find_substring(text, pattern)
    result = f"index {index}" if index != -1 else "not found"
    print(f"  Find '{pattern}': {result}")

print("→ Naive: O(n*m), Built-in find(): O(n)")

# ==================== (8) Character Frequency Count ====================
print("\n[8] Character Frequency Count")
print("-" * 40)

def count_frequencies(s: str) -> dict:
    """Count character frequencies"""
    return Counter(s)

def most_frequent_char(s: str) -> tuple:
    """Find most frequent character"""
    counts = Counter(s)
    if not counts:
        return None, 0
    char, count = counts.most_common(1)[0]
    return char, count

s = "hello world"
freq = count_frequencies(s)

print(f"String: '{s}'")
print(f"Character frequencies: {dict(freq)}")

char, count = most_frequent_char(s)
print(f"Most frequent: '{char}' ({count} times)")
print("→ Time: O(n), Space: O(k) where k = unique chars")

# ==================== (9) Longest Substring Without Repeating ====================
print("\n[9] Longest Substring Without Repeating - Sliding Window")
print("-" * 40)

def longest_substring(s: str) -> tuple:
    """Find longest substring without repeating chars"""
    char_index = {}
    left = 0
    max_length = 0
    max_start = 0

    for right in range(len(s)):
        # If char seen and is in current window
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1

        char_index[s[right]] = right

        if right - left + 1 > max_length:
            max_length = right - left + 1
            max_start = left

    return s[max_start:max_start+max_length], max_length

test_cases = [
    "abcabcbb",    # "abc" = 3
    "bbbbb",       # "b" = 1
    "pwwkew",      # "wke" = 3
    "au",          # "au" = 2
]

print("Finding longest substring without repeating:")
for s in test_cases:
    substring, length = longest_substring(s)
    print(f"  '{s}' → '{substring}' (length {length})")

print("→ Time: O(n), Space: O(min(n, alphabet_size))")

# ==================== (10) String Rotation Check ====================
print("\n[10] String Rotation Check")
print("-" * 40)

def is_rotation(s1: str, s2: str) -> bool:
    """Check if s2 is rotation of s1"""
    if len(s1) != len(s2):
        return False
    return s2 in s1 + s1

test_cases = [
    ("waterbottle", "erbottlewat", True),
    ("hello", "llohe", True),
    ("hello", "world", False),
]

print("Checking string rotations:")
for s1, s2, expected in test_cases:
    result = is_rotation(s1, s2)
    status = "✓" if result == expected else "✗"
    print(f"  Is '{s2}' rotation of '{s1}'? {result} {status}")

print("→ Time: O(n), Space: O(n) - clever trick!")

# ==================== (11) String Transformations ====================
print("\n[11] String Transformations")
print("-" * 40)

s = "hello world python"

print(f"Original: '{s}'")
print(f"Upper: '{s.upper()}'")
print(f"Lower: '{s.lower()}'")
print(f"Title: '{s.title()}'")
print(f"Capitalize: '{s.capitalize()}'")
print(f"Reverse: '{s[::-1]}'")
print(f"Replace: '{s.replace('world', 'universe')}'")
print(f"Split: {s.split()}")
print(f"Join: {'-'.join(['a', 'b', 'c'])}")
print(f"Strip: '{' hello '.strip()}'")
print("→ All transformations: O(n) time")

# ==================== (12) Pattern Matching with Regex ====================
print("\n[12] Pattern Matching with Regular Expressions")
print("-" * 40)

text = "Email: john@example.com, Phone: 555-1234"

print(f"Text: '{text}'")

# Find email pattern
emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
print(f"Emails found: {emails}")

# Find phone pattern
phones = re.findall(r"\d{3}-\d{4}", text)
print(f"Phones found: {phones}")

# Replace pattern
masked = re.sub(r"\d", "*", text)
print(f"Masked digits: '{masked}'")

# Check if matches pattern
is_valid_email = bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", "test@example.com"))
print(f"Is valid email? {is_valid_email}")

print("→ Regex: O(n) for most patterns, O(n*m) for complex ones")

print("\n" + "=" * 60)
print("Next: Complete exercises and build the project!")
print("=" * 60)
