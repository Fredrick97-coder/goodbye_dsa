# Arrays and Lists

Arrays and lists are fundamental data structures. Python provides dynamic lists built-in, but understanding how they work is crucial.

---

## 1. What is an Array?

An **array** is a fixed-size collection of elements of the same type, stored in contiguous memory locations.

### Properties of Arrays:
- **Fixed size** - Cannot grow or shrink
- **Contiguous memory** - Elements stored back-to-back
- **Random access** - Get/set any element in O(1)
- **Type-specific** - Traditional arrays store one type

### Array Operations:
| Operation | Time | Space | Description |
|-----------|------|-------|-------------|
| Access element | O(1) | - | Direct memory lookup |
| Search element | O(n) | - | Must scan all elements |
| Insert at beginning | O(n) | O(n) | Shift all elements |
| Insert at end | O(1) | O(1) | Just append |
| Delete from beginning | O(n) | - | Shift remaining elements |
| Delete from end | O(1) | - | Just remove |

---

## 2. What is a List?

A **list** is a dynamic array that can grow and shrink. Python lists are dynamic arrays.

### Dynamic Array Implementation:
When a Python list is full and you add an element:
1. A new, larger array is created (usually 1.5x or 2x size)
2. All elements are copied
3. New element is added
4. Old array is discarded

This happens **rarely** (amortized), so append is O(1) amortized.

```python
# Python lists
arr = [1, 2, 3]
arr.append(4)           # O(1) amortized
arr.insert(0, 0)        # O(n) - must shift elements
arr.pop()               # O(1) - remove last
arr.pop(0)              # O(n) - remove first, must shift
```

---

## 3. Indexing and Slicing

### Indexing (0-based):
```python
arr = [10, 20, 30, 40, 50]
arr[0]      # 10 (first)
arr[2]      # 30 (third)
arr[-1]     # 50 (last)
arr[-2]     # 40 (second last)
```

### Slicing:
```python
arr = [10, 20, 30, 40, 50]
arr[1:4]    # [20, 30, 40] - from index 1 to 3
arr[:3]     # [10, 20, 30] - first 3 elements
arr[2:]     # [30, 40, 50] - from index 2 to end
arr[::2]    # [10, 30, 50] - every 2nd element
arr[::-1]   # [50, 40, 30, 20, 10] - reverse
```

**Slicing creates a NEW list (O(n) time, O(n) space)**

---

## 4. List Methods and Complexity

| Method | Time | Meaning |
|--------|------|---------|
| `append(x)` | O(1) | Add to end |
| `insert(i, x)` | O(n) | Insert at index i |
| `pop()` | O(1) | Remove last |
| `pop(i)` | O(n) | Remove at index i |
| `remove(x)` | O(n) | Remove first occurrence of x |
| `index(x)` | O(n) | Find index of x |
| `count(x)` | O(n) | Count occurrences of x |
| `extend(lst)` | O(k) | Add k elements from list |
| `sort()` | O(n log n) | Sort in place |
| `reverse()` | O(n) | Reverse in place |

---

## 5. List Comprehensions

List comprehensions are concise and fast (implemented in C).

```python
# Create list of squares
squares = [x**2 for x in range(10)]         # [0, 1, 4, 9, 16, ...]

# Filter elements
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# Nested comprehensions
matrix = [[i+j for j in range(3)] for i in range(3)]
# [[0, 1, 2], [1, 2, 3], [2, 3, 4]]

# Time complexity: O(n) where n is result size
```

---

## 6. Common Array Patterns

### Two-Pointer Technique
```python
def two_pointer_example(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        # Process arr[left] and arr[right]
        left += 1
        right -= 1
```

### Sliding Window
```python
def sliding_window_example(arr, window_size):
    for i in range(len(arr) - window_size + 1):
        window = arr[i:i + window_size]
        # Process window
```

### Prefix Sum
```python
def prefix_sum(arr):
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

# Query sum from index i to j in O(1):
# sum(arr[i:j+1]) = prefix[j+1] - prefix[i]
```

---

## 7. Multidimensional Arrays

Python doesn't have true multidimensional arrays, but we can simulate them:

```python
# 2D Array (Matrix)
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

matrix[0][0]  # 1 (row 0, column 0)
matrix[1][2]  # 6 (row 1, column 2)

# Important: Avoid this mistake!
# Wrong: [[0] * 3] * 3 - creates same row 3 times
# Right: [[0] * 3 for _ in range(3)] - creates 3 different rows
```

---

## 8. Array Copying

```python
original = [1, 2, 3]

# Shallow copy (only copy references)
shallow = original.copy()       # O(n)
shallow = original[:]           # O(n) slicing
shallow = list(original)        # O(n)

# Deep copy (copy elements recursively)
import copy
deep = copy.deepcopy(original)  # O(n) for simple types
```

---

## 9. Useful Array Operations

```python
# Finding
arr.index(x)        # O(n) - first index of x
arr.count(x)        # O(n) - count occurrences

# Maximum/Minimum
max(arr)            # O(n)
min(arr)            # O(n)

# Sum
sum(arr)            # O(n)

# All/Any
all([True, True])   # O(n) - all True?
any([False, True])  # O(n) - any True?

# Zip
list(zip([1,2], [3,4]))  # [(1,3), (2,4)]

# Enumerate
for i, val in enumerate(arr):
    print(f"{i}: {val}")
```

---

## 10. Performance Tips

1. **Use append(), not insert(0, x)**
   - `append()` is O(1), `insert(0, x)` is O(n)

2. **Use list comprehensions**
   - Faster than loops, cleaner code

3. **Avoid slicing in loops**
   - `arr[i:]` creates a new list each time

4. **Use generators for large data**
   - `(x for x in range(1000000))` doesn't create list

5. **Prefer extend() over += for lists**
   - Both work, but extend() is clearer

---

## Key Takeaways

✅ **Arrays** provide O(1) access but fixed size  
✅ **Lists** are dynamic arrays, better for general use  
✅ **Append** is O(1) amortized, **insert** is O(n)  
✅ **Slicing** creates new lists (O(n) time and space)  
✅ **List comprehensions** are fast and pythonic  
✅ **Two-pointer** and **sliding window** are key patterns  
