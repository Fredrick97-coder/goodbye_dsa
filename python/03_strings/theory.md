# Strings and String Manipulation

Strings are immutable sequences of characters. Mastering string algorithms is essential for many DSA problems.

---

## 1. What is a String?

A **string** is an immutable sequence of Unicode characters. Once created, it cannot be modified.

### String Properties:
- **Immutable** - Cannot change characters in place
- **Ordered** - Characters have positions
- **Indexable** - Access characters by index
- **Iterable** - Can loop through characters
- **Unicode** - Supports all languages

### Basic Operations:
```python
s = "hello"
s[0]           # 'h' - indexing (O(1))
s[1:4]         # 'ell' - slicing (O(n))
len(s)         # 5 - length (O(1))
s + " world"   # concatenation creates new string (O(n))
"l" in s       # membership check (O(n))
```

---

## 2. String Immutability

Since strings are immutable, modification creates a new string:

```python
s = "hello"
s = s + " world"  # Creates new string, doesn't modify original

# This is inefficient in a loop:
result = ""
for char in "hello":
    result += char  # O(n²) time! Creates new string each iteration

# Better: use list and join (O(n)):
result = "".join(["h", "e", "l", "l", "o"])
```

---

## 3. String Methods and Complexity

| Method | Time | Purpose |
|--------|------|---------|
| `len(s)` | O(1) | Get string length |
| `s[i]` | O(1) | Access character by index |
| `s[i:j]` | O(j-i) | Get substring |
| `s.find(sub)` | O(n*m) | Find substring (naive) |
| `s.count(sub)` | O(n) | Count occurrences |
| `s.split()` | O(n) | Split by delimiter |
| `s.join(list)` | O(n) | Join strings |
| `s.replace(a, b)` | O(n) | Replace substring |
| `s.upper()` / `s.lower()` | O(n) | Change case |
| `s.strip()` | O(n) | Remove whitespace |

### Key Insight:
**Always use `"".join(list)` not `s += item`** in loops!

```python
# O(n²) - BAD
s = ""
for char in chars:
    s += char

# O(n) - GOOD
s = "".join(chars)
```

---

## 4. Common String Patterns

### Pattern 1: Two-Pointer Technique
```python
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True

# Time: O(n), Space: O(1)
```

### Pattern 2: Sliding Window
```python
def longest_substring_without_repeating(s: str) -> int:
    char_index = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1
        
        char_index[s[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Time: O(n), Space: O(min(n, alphabet_size))
```

### Pattern 3: Hash Map / Set
```python
def anagram(s1: str, s2: str) -> bool:
    """Check if two strings are anagrams"""
    return sorted(s1) == sorted(s2)  # O(n log n)
    
    # Or using hash map (O(n)):
    from collections import Counter
    return Counter(s1) == Counter(s2)

# Time: O(n), Space: O(1) or O(26) for English
```

### Pattern 4: KMP Algorithm (Advanced)
For efficient substring search:
```python
# Knuth-Morris-Pratt: O(n + m) for finding pattern in text
# Better than naive O(n*m) approach
```

---

## 5. String Comparison & Ordering

### Lexicographic Ordering:
Strings are compared character by character using ASCII/Unicode values.

```python
"abc" < "abd"  # True ('c' < 'd')
"a" < "b"      # True
"abc" < "abcd" # True (shorter is less)
```

### Sorting Strings:
```python
words = ["banana", "apple", "cherry"]
sorted_words = sorted(words)  # O(n log n)
# Result: ['apple', 'banana', 'cherry']
```

---

## 6. String Searching Algorithms

### Naive Search - O(n*m)
```python
def naive_search(text: str, pattern: str) -> int:
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i+len(pattern)] == pattern:
            return i
    return -1
```

### Built-in Methods - O(n) average
```python
"hello world".find("world")      # 6
"hello world".index("world")     # 6 (raises error if not found)
"hello".startswith("hel")        # True
"world".endswith("ld")           # True
```

### Advanced: KMP Algorithm - O(n+m)
More efficient for large texts and patterns.

---

## 7. String Transformations

### Common Transformations:
```python
s = "hello world"

# Case conversion (O(n))
s.upper()           # "HELLO WORLD"
s.lower()           # "hello world"
s.title()           # "Hello World"
s.capitalize()      # "Hello world"

# Stripping (O(n))
"  hello  ".strip()     # "hello"
"xxxhelloxxx".strip("x")  # "hello"

# Splitting and joining (O(n))
s.split(" ")        # ["hello", "world"]
"-".join(["a", "b"])  # "a-b"

# Replacement (O(n))
s.replace("world", "python")  # "hello python"
```

---

## 8. String Validation

Common validation patterns:

```python
# Check if palindrome
def is_palindrome(s: str) -> bool:
    s = s.lower()
    return s == s[::-1]  # O(n)

# Check if anagram
def is_anagram(s1: str, s2: str) -> bool:
    return sorted(s1) == sorted(s2)  # O(n log n)

# Check if valid parentheses
def is_valid_parentheses(s: str) -> bool:
    # (use stack - covered in Topic 04)
    pass

# Check if all unique characters
def has_unique_chars(s: str) -> bool:
    return len(set(s)) == len(s)  # O(n)

# Check if string is rotation of another
def is_rotation(s1: str, s2: str) -> bool:
    return len(s1) == len(s2) and s2 in s1 + s1
    # "waterbottle" is rotation of "erbottlewat"
```

---

## 9. Complexity Comparison

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| **Palindrome check** | O(n) | O(1) | Two-pointer |
| **Anagram check** | O(n log n) | O(1) | Sorting |
| **Anagram check** | O(n) | O(n) | Hash map |
| **Substring search** | O(n*m) | O(1) | Naive |
| **Substring search** | O(n+m) | O(m) | KMP |
| **Reverse string** | O(n) | O(1) | In-place (list) |
| **Remove duplicates** | O(n) | O(n) | Hash set |
| **Longest palindrome** | O(n³) | O(1) | Brute force |
| **Longest palindrome** | O(n²) | O(n) | DP approach |

---

## 10. Regular Expressions (Optional)

For pattern matching:

```python
import re

# Check pattern
re.match(r"^[a-z]+$", "hello")     # Match only letters
re.search(r"\d+", "abc123def")      # Find digits
re.findall(r"\w+", "hello world")   # Find all words
re.sub(r"\s+", "-", "a b c")        # Replace spaces with dash

# Time complexity depends on regex pattern
```

---

## 11. Practical Tips

✓ **Use `in` operator** for membership (more readable)  
✓ **Prefer `str.join()`** over `+=` in loops  
✓ **Use list comprehensions** for transformations  
✓ **Consider `.isdigit()`, `.isalpha()` methods**  
✓ **Remember: strings are immutable**  
✓ **Two-pointer works great for palindromes**  
✓ **Sliding window for substrings**  
✓ **Hash map for character counts**  

---

## 12. Common Pitfalls

❌ **Using `s += char` in loop** → O(n²)  
❌ **Slicing unnecessarily** → Creates new strings  
❌ **Forgetting strings are immutable** → No in-place modifications  
❌ **Using `==` for comparison** → Can be slow for long strings  
❌ **Ignoring case sensitivity** → Different characters!  
❌ **Not handling empty strings** → Edge case!  

---

## Key Takeaways

✅ **Immutable**: Modifications create new strings  
✅ **O(1) access**: Index-based access is constant time  
✅ **Slicing is O(n)**: Creates new string  
✅ **String concatenation in loops**: Use `join()` not `+=`  
✅ **Two-pointer**: Great for palindromes  
✅ **Sliding window**: Efficient for substrings  
✅ **Hash map**: Track character frequencies  
✅ **Common patterns**: Apply to many problems  

Next: Learn about practical string algorithms with examples!
