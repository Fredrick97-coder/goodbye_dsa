# Basic Searching Algorithms

Master fundamental search techniques: linear search, binary search, and search patterns.

---

## 1. What is Searching?

**Searching** is finding an element (or elements) in a data structure that match specific criteria.

### Two Main Categories:
1. **Linear Search**: Check elements one by one
2. **Binary Search**: Divide and conquer on sorted data

### Key Questions:
- Is the data sorted?
- Do we need the first, last, or any occurrence?
- Are there duplicates?
- What's the acceptable time complexity?

---

## 2. Linear Search

**Linear search** (sequential search) checks each element until finding the target.

### Algorithm:
```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

### Characteristics:
- **Time**: O(n) average, O(n) worst case
- **Space**: O(1)
- **Requirements**: None (works on unsorted data)
- **Best for**: Small arrays or unsorted data

### When to Use:
- ✓ Unsorted data
- ✓ Small datasets
- ✓ Linked lists
- ✓ Any occurrence is fine

### When NOT to Use:
- ✗ Large sorted arrays (use binary search)
- ✗ Performance-critical (binary search is faster)

---

## 3. Binary Search

**Binary search** eliminates half the remaining elements with each comparison.

### Requirements:
- **Sorted array** (ascending or descending)

### Algorithm:
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1      # Target in right half
        else:
            right = mid - 1     # Target in left half
    
    return -1                   # Not found
```

### Characteristics:
- **Time**: O(log n) average, O(log n) worst case
- **Space**: O(1) iterative, O(log n) recursive
- **Requirements**: **Sorted array**
- **Best for**: Large sorted arrays

### Example Trace:
```
Array: [1, 3, 5, 7, 9, 11, 13]
Target: 7

Step 1: left=0, right=6, mid=3, arr[3]=7 → Found! Return 3
```

### Why It's Faster:
```
Linear Search: Check 1, 2, 3, 4... up to 1 million items
Binary Search: Check middle, eliminate half, repeat
              log₂(1,000,000) ≈ 20 checks!
```

---

## 4. Binary Search Variants

### Variant 1: Find First Occurrence
```python
def find_first(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1     # Keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result
```

### Variant 2: Find Last Occurrence
```python
def find_last(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1      # Keep searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result
```

### Variant 3: Find Insert Position
```python
def search_insert(arr, target):
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

---

## 5. Search Patterns

### Pattern 1: Two-Pointer Search
Find two elements matching a condition.

```python
def find_pair_sum(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None
```

**Time**: O(n), **Space**: O(1)

### Pattern 2: Sliding Window Search
Find contiguous subarray matching criteria.

```python
def max_sum_subarray(arr, k):
    if len(arr) < k:
        return None
    
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(len(arr) - k):
        window_sum = window_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

**Time**: O(n), **Space**: O(1)

### Pattern 3: Rotated Array Search
Binary search on rotated sorted array.

```python
def search_rotated(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        
        # Determine which half is sorted
        if arr[left] <= arr[mid]:
            # Left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1
```

---

## 6. Complexity Comparison

| Algorithm | Best | Average | Worst | Space | Requirements |
|-----------|------|---------|-------|-------|--------------|
| Linear | O(1) | O(n) | O(n) | O(1) | None |
| Binary | O(1) | O(log n) | O(log n) | O(1) | Sorted |
| Two-Pointer | O(1) | O(n) | O(n) | O(1) | Sorted |
| Sliding Window | O(k) | O(n) | O(n) | O(1) | None |

---

## 7. When to Use Which Algorithm

### Use Linear Search:
- ✓ Unsorted data
- ✓ Small arrays (< 100 elements)
- ✓ Linked lists
- ✓ Need multiple passes anyway

### Use Binary Search:
- ✓ Large sorted arrays
- ✓ Need O(log n) performance
- ✓ Find insertion point
- ✓ Range queries

### Use Two-Pointer:
- ✓ Sorted array
- ✓ Find pair with specific sum
- ✓ Remove duplicates
- ✓ Container with most water

### Use Sliding Window:
- ✓ Find subarray/substring
- ✓ Window size is fixed or dynamic
- ✓ Contiguous elements matter
- ✓ Optimization problem

---

## 8. Common Search Problems

### Problem 1: Find Missing Number
```python
# Sorted array, one number missing
# Time: O(log n) with binary search
```

### Problem 2: Find Peak Element
```python
# Array increases then decreases
# Find the peak value
# Time: O(log n) with modified binary search
```

### Problem 3: Find Rotated Minimum
```python
# Rotated sorted array
# Find minimum value
# Time: O(log n) with binary search
```

### Problem 4: Longest Prefix Match
```python
# Find longest matching prefix
# Time: O(n * k) where k = prefix length
```

---

## 9. Edge Cases & Gotchas

### Issue 1: Off-by-One Errors
```python
# Wrong: right = len(arr) (out of bounds)
# Correct: right = len(arr) - 1
```

### Issue 2: Integer Overflow
```python
# Wrong: mid = (left + right) // 2
# Correct: mid = left + (right - left) // 2
```

### Issue 3: Infinite Loop
```python
# Wrong: don't update left/right correctly
# Always ensure: left < right eventually
```

### Issue 4: Duplicates
```python
# Binary search doesn't handle duplicates well
# Use variants to find first/last occurrence
```

---

## 10. Key Takeaways

✅ **Linear Search**: O(n), works on any data  
✅ **Binary Search**: O(log n), requires sorted data  
✅ **Two-Pointer**: O(n), efficient on sorted arrays  
✅ **Sliding Window**: O(n), great for subarray problems  
✅ **Trade-offs**: Speed vs data requirements  
✅ **Edge Cases**: Handle duplicates, boundaries, empty arrays  
✅ **Variants**: First/last occurrence, insertion position  

**Best for**: Lookups, filtering, finding thresholds  
**Not for**: Modifying data (that's insertion)

Next: Implement search algorithms and solve problems!
