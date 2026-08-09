# Introduction to Data Structures and Algorithms

Understanding algorithms and their efficiency is fundamental to computer science and software engineering.

---

## 1. What is an Algorithm?

An **algorithm** is a step-by-step procedure to solve a problem. It takes input, processes it, and produces output.

**Example:** Finding the largest number in a list
```python
def find_max(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num
```

---

## 2. What is a Data Structure?

A **data structure** is a way of organizing and storing data so it can be accessed and modified efficiently.

### Common Data Structures:
- **Arrays/Lists** - Ordered collection of elements
- **Linked Lists** - Elements connected via pointers
- **Stacks** - LIFO (Last-In-First-Out)
- **Queues** - FIFO (First-In-First-Out)
- **Trees** - Hierarchical structure
- **Graphs** - Connected nodes with edges
- **Hash Tables** - Key-value pairs

---

## 3. Big-O Notation (Time Complexity)

**Big-O** describes how an algorithm's performance scales with input size (n).

### Common Complexities (Best to Worst):

| Notation | Name | Example | Speed |
|----------|------|---------|-------|
| **O(1)** | Constant | Accessing array by index | ⚡ Fastest |
| **O(log n)** | Logarithmic | Binary search | ⚡⚡ |
| **O(n)** | Linear | Simple loop through array | ⚡⚡⚡ |
| **O(n log n)** | Linearithmic | Merge sort, Quick sort | ⚡⚡⚡⚡ |
| **O(n²)** | Quadratic | Nested loops | 🐢 Slower |
| **O(n³)** | Cubic | Triple nested loops | 🐢🐢 |
| **O(2ⁿ)** | Exponential | Recursive (no memoization) | 🐢🐢🐢 |
| **O(n!)** | Factorial | Generate all permutations | 🐢🐢🐢🐢 |

### Visualizing Complexity:
```
For n = 1,000:
- O(1)      → 1 operation
- O(log n)  → ~10 operations
- O(n)      → 1,000 operations
- O(n²)     → 1,000,000 operations
- O(2ⁿ)     → 2^1000 operations (HUGE!)
```

---

## 4. Understanding Big-O with Examples

### O(1) - Constant Time
```python
def get_first_element(arr):
    return arr[0]  # Always 1 operation
```

### O(n) - Linear Time
```python
def find_sum(arr):
    total = 0
    for num in arr:  # Loops n times
        total += num
    return total
```

### O(n²) - Quadratic Time
```python
def print_pairs(arr):
    for i in arr:           # Outer loop: n times
        for j in arr:       # Inner loop: n times
            print(i, j)     # Total: n * n = n² operations
```

### O(log n) - Logarithmic Time
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1  # Eliminate half of remaining elements
        else:
            right = mid - 1
    return -1
```

---

## 5. Space Complexity

Space complexity describes the **amount of extra memory** an algorithm uses relative to input size.

| Notation | Meaning | Example |
|----------|---------|---------|
| **O(1)** | Constant space | `swap(a, b)` - only a few variables |
| **O(n)** | Linear space | Creating an array of size n |
| **O(n²)** | Quadratic space | 2D matrix of size n×n |
| **O(log n)** | Logarithmic space | Recursive call stack (depth) |

---

## 6. Trade-offs: Time vs Space

Sometimes you can optimize time by using more space, and vice versa.

**Example:** Finding duplicates

### Low Time, High Space
```python
def has_duplicates_fast(arr):
    seen = set()  # Extra O(n) space
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False
# Time: O(n), Space: O(n)
```

### High Time, Low Space
```python
def has_duplicates_memory(arr):
    for i in range(len(arr)):  # O(n²) time
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False
# Time: O(n²), Space: O(1)
```

---

## 7. How to Analyze Algorithms

### Step 1: Identify the loops
Count how many times operations repeat.

### Step 2: Count operations
Determine what happens in each loop iteration.

### Step 3: Find the dominant term
Ignore constants and lower-order terms.

```python
def example(n):
    for i in range(n):          # Runs n times
        print(i)                # O(1) operation
    
    for i in range(n):          # Runs n times
        for j in range(n):      # Runs n times
            print(i, j)         # O(1) operation
    
    return 42                   # O(1) operation

# Total: n + n² + 1 = n² + n + 1
# Drop lower order terms and constants: O(n²)
```

---

## 8. Best, Average, and Worst Case

Algorithms can have different complexities depending on input:

- **Best Case** - Minimum time/space
- **Average Case** - Expected time/space  
- **Worst Case** - Maximum time/space (usually what we care about)

**Example: Linear Search**
```python
def linear_search(arr, target):
    for num in arr:
        if num == target:
            return True
    return False

# Best case: O(1) - target is first element
# Average case: O(n) - target in middle
# Worst case: O(n) - target not found or last element
```

---

## 9. Optimization Techniques

### 1. **Early Exit**
Stop as soon as you find the answer.

### 2. **Preprocessing**
Sort or organize data first for faster queries.

### 3. **Caching / Memoization**
Store results you've already computed.

### 4. **Divide and Conquer**
Split problem into smaller subproblems.

### 5. **Dynamic Programming**
Build solutions from subproblems (covered later).

---

## 10. Practical Guidelines

- **O(n) or better** - Good for most problems ✅
- **O(n log n)** - Acceptable, often optimal ✅
- **O(n²)** - Works for n < 10,000; risky for larger ⚠️
- **O(2ⁿ)** or worse - Only for very small inputs (n < 20) ❌

---

## Key Takeaways

✅ **Algorithm**: Step-by-step solution  
✅ **Data Structure**: How data is organized  
✅ **Big-O**: Describes scalability  
✅ **Time vs Space**: Usually a trade-off  
✅ **Worst Case**: What we usually analyze  
✅ **Optimization**: Reduce complexity through clever design  

---

## Next Steps

Master these concepts before moving to specific data structures and algorithms. Revisit this guide whenever you're analyzing algorithm efficiency.
