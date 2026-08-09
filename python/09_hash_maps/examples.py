"""
Examples: Hash Maps & Hash Tables

Demonstrate practical hash map applications and patterns.
"""

from collections import Counter, defaultdict
from typing import List, Dict

print("=" * 60)
print("HASH MAPS - EXAMPLES")
print("=" * 60)

# ==================== (1) Basic Operations ====================
print("\n[1] Basic Hash Map Operations")
print("-" * 40)

hash_map = {}

# Insert (O(1))
hash_map["name"] = "Alice"
hash_map["age"] = 25
hash_map["city"] = "NYC"

print(f"Hash map: {hash_map}")
print(f"Get 'name': {hash_map['name']}")
print(f"Update 'age' to 26: ", end="")
hash_map["age"] = 26
print(hash_map["age"])

# Delete (O(1))
del hash_map["city"]
print(f"After deleting 'city': {hash_map}")

print("→ Time: O(1) for insert, get, delete")

# ==================== (2) Frequency Counting ====================
print("\n[2] Frequency Counting")
print("-" * 40)

def count_frequency(arr: List[int]) -> Dict[int, int]:
    freq = {}
    for num in arr:
        freq[num] = freq.get(num, 0) + 1
    return freq

arr = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
freq = count_frequency(arr)
print(f"Array: {arr}")
print(f"Frequencies: {freq}")
print(f"Most frequent: {max(freq, key=freq.get)}")

# Using Counter (built-in)
freq2 = Counter(arr)
print(f"Top 2 frequent: {freq2.most_common(2)}")
print("→ Time: O(n) for counting, O(1) per lookup")

# ==================== (3) Two Sum ====================
print("\n[3] Two Sum Problem")
print("-" * 40)

def two_sum(arr: List[int], target: int):
    """Find two numbers that add to target"""
    seen = {}
    for num in arr:
        complement = target - num
        if complement in seen:
            return (complement, num)
        seen[num] = True
    return None

arr = [2, 7, 11, 15]
target = 9
result = two_sum(arr, target)
print(f"Array: {arr}")
print(f"Target: {target}")
print(f"Two sum: {result}")
print("→ Time: O(n), Space: O(n)")

# ==================== (4) Anagrams ====================
print("\n[4] Group Anagrams")
print("-" * 40)

def group_anagrams(words: List[str]) -> Dict[str, List[str]]:
    """Group words that are anagrams"""
    groups = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)
    return dict(groups)

words = ["listen", "silent", "hello", "world", "enlist", "low"]
grouped = group_anagrams(words)
print(f"Words: {words}")
print(f"Grouped by anagram:")
for key, group in grouped.items():
    print(f"  {key}: {group}")
print("→ Time: O(n * k log k) where k = max word length")

# ==================== (5) First Unique Character ====================
print("\n[5] First Unique Character")
print("-" * 40)

def first_unique_char(s: str) -> int:
    """Find index of first character that appears only once"""
    freq = Counter(s)
    for i, char in enumerate(s):
        if freq[char] == 1:
            return i
    return -1

strings = ["leetcode", "loveleetcode", "aabb"]
for s in strings:
    idx = first_unique_char(s)
    char = s[idx] if idx >= 0 else "None"
    print(f"  '{s}' → index {idx} ('{char}')")
print("→ Time: O(n), Space: O(1) for lowercase letters")

# ==================== (6) Valid Anagram ====================
print("\n[6] Valid Anagram Check")
print("-" * 40)

def is_anagram(s1: str, s2: str) -> bool:
    """Check if two strings are anagrams"""
    return Counter(s1) == Counter(s2)

pairs = [("listen", "silent"), ("hello", "world"), ("abc", "bca")]
for s1, s2 in pairs:
    result = is_anagram(s1, s2)
    print(f"  '{s1}' and '{s2}' → {result}")
print("→ Time: O(n), Space: O(1) for fixed alphabet")

# ==================== (7) Contains Duplicate ====================
print("\n[7] Duplicate Detection")
print("-" * 40)

def contains_duplicate(arr: List[int]) -> bool:
    """Check if array has duplicates"""
    seen = set()
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False

arrays = [[1, 2, 3, 4], [1, 2, 2, 3], [99, 99]]
for arr in arrays:
    result = contains_duplicate(arr)
    print(f"  {arr} → {result}")
print("→ Time: O(n), Space: O(n)")

# ==================== (8) Majority Element ====================
print("\n[8] Majority Element")
print("-" * 40)

def majority_element(arr: List[int]):
    """Find element appearing > n/2 times"""
    freq = Counter(arr)
    majority = len(arr) // 2
    for num, count in freq.items():
        if count > majority:
            return num
    return None

arrays = [[3, 2, 3], [2, 2, 1, 1, 1, 2, 2], [1]]
for arr in arrays:
    result = majority_element(arr)
    print(f"  {arr} → {result}")
print("→ Time: O(n), Space: O(n)")

# ==================== (9) Hash Function Collision ====================
print("\n[9] Hash Function & Collisions")
print("-" * 40)

class SimpleHashMap:
    """Simple hash map with chaining collision resolution"""

    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def set(self, key, value):
        index = self._hash(key)
        # Check if key exists and update
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        # Add new entry
        self.table[index].append((key, value))

    def get(self, key):
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def print_table(self):
        for i, chain in enumerate(self.table):
            if chain:
                print(f"  Index {i}: {chain}")

hm = SimpleHashMap(5)
hm.set("a", 1)
hm.set("b", 2)
hm.set("c", 3)
hm.set("a", 10)  # Update

print("Simple hash map with chaining:")
hm.print_table()
print(f"Get 'a': {hm.get('a')}")
print(f"Get 'b': {hm.get('b')}")
print("→ Chaining handles collisions by storing linked list")

# ==================== (10) Caching with Hash Map ====================
print("\n[10] Memoization / Caching")
print("-" * 40)

def fibonacci_cached(n: int, cache: dict = None) -> int:
    """Fibonacci with memoization"""
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    result = fibonacci_cached(n - 1, cache) + fibonacci_cached(n - 2, cache)
    cache[n] = result
    return result

def fibonacci_uncached(n: int) -> int:
    """Fibonacci without caching - exponential time"""
    if n <= 1:
        return n
    return fibonacci_uncached(n - 1) + fibonacci_uncached(n - 2)

import time

n = 35
print(f"Computing fibonacci({n}):")

start = time.time()
result_cached = fibonacci_cached(n)
time_cached = (time.time() - start) * 1000

start = time.time()
result_uncached = fibonacci_uncached(n)
time_uncached = (time.time() - start) * 1000

print(f"  With caching:    {result_cached} (≈{time_cached:.2f}ms)")
print(f"  Without caching: {result_uncached} (≈{time_uncached:.2f}ms)")
print(f"  Speed improvement: {time_uncached/time_cached:.0f}x faster!")

# ==================== (11) Default Dict ====================
print("\n[11] defaultdict for Grouping")
print("-" * 40)

from collections import defaultdict

def count_by_mod(numbers: List[int]):
    """Group numbers by their modulo"""
    groups = defaultdict(list)
    for num in numbers:
        groups[num % 3].append(num)
    return dict(groups)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
groups = count_by_mod(numbers)
print(f"Numbers: {numbers}")
print(f"Grouped by mod 3:")
for mod, nums in sorted(groups.items()):
    print(f"  mod {mod}: {nums}")
print("→ defaultdict avoids KeyError on missing keys")

# ==================== (12) Complexity Summary ====================
print("\n[12] Complexity Summary")
print("-" * 40)

operations = {
    "Insert": "O(1) avg, O(n) worst",
    "Search": "O(1) avg, O(n) worst",
    "Delete": "O(1) avg, O(n) worst",
    "Update": "O(1) avg, O(n) worst",
    "Iterate": "O(n)",
}

print(f"{'Operation':<20} {'Time Complexity':<25}")
print("-" * 45)
for op, complexity in operations.items():
    print(f"{op:<20} {complexity:<25}")

print("\nAverage case: O(1) with good hash function")
print("Worst case: O(n) with many collisions")

print("\n" + "=" * 60)
print("Next: Solve hash map problems and build applications!")
print("=" * 60)
