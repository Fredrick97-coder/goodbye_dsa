# Advanced Sorting - Efficient & Specialized Algorithms

Master divide-and-conquer, comparison-based, and non-comparison sorting algorithms.

---

## 1. Sorting Algorithm Landscape

### Comparison-Based Sorting
Compare elements to determine order.

```
O(n log n) average/best: Merge Sort, Quick Sort, Heap Sort
O(n²) worst: Quick Sort (bad pivot), Insertion Sort
O(n log n) worst: Merge Sort, Heap Sort
```

### Non-Comparison Sorting
Use properties of data (digits, ranges) instead of comparisons.

```
O(n+k): Counting Sort, Radix Sort, Bucket Sort
Limited to specific data types (integers, fixed digits)
```

---

## 2. Merge Sort (Divide & Conquer)

**Algorithm**: Divide array in half, sort recursively, merge sorted halves.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result
```

**Characteristics**:
- **Time**: O(n log n) always
- **Space**: O(n) for temp arrays
- **Stable**: Yes (equal elements preserve order)
- **In-place**: No
- **Best for**: Linked lists, stable sorting, guaranteed performance

---

## 3. Quick Sort (Divide & Conquer)

**Algorithm**: Partition around pivot, sort left and right recursively.

```python
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    
    return arr

def partition(arr, low, high):
    # Choose last element as pivot
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**Characteristics**:
- **Time**: O(n log n) average, O(n²) worst case
- **Space**: O(log n) for recursion
- **Stable**: No (typical implementation)
- **In-place**: Yes
- **Best for**: General purpose, in-memory sorting, practical performance

**Pivot Selection Strategies**:
- First/Last element: O(n²) on sorted data
- Random element: Expected O(n log n)
- Median-of-three: Better than first/last
- Median-of-medians: O(n log n) guaranteed (rarely used)

---

## 4. Heap Sort

**Algorithm**: Build max heap, repeatedly extract maximum.

```python
def heap_sort(arr):
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, i, n)
    
    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_down(arr, 0, i)
    
    return arr

def heapify_down(arr, i, n):
    largest = i
    left, right = 2 * i + 1, 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_down(arr, largest, n)
```

**Characteristics**:
- **Time**: O(n log n) always
- **Space**: O(1) in-place
- **Stable**: No
- **In-place**: Yes
- **Best for**: Guaranteed performance, space-critical, real-time systems

---

## 5. Counting Sort (Non-Comparison)

**Algorithm**: Count frequency of each value, reconstruct sorted array.

```python
def counting_sort(arr, max_val):
    if not arr:
        return arr
    
    # Count frequencies
    counts = [0] * (max_val + 1)
    for num in arr:
        counts[num] += 1
    
    # Reconstruct
    idx = 0
    for num in range(max_val + 1):
        for _ in range(counts[num]):
            arr[idx] = num
            idx += 1
    
    return arr
```

**Characteristics**:
- **Time**: O(n + k) where k = range
- **Space**: O(k) for counts array
- **Stable**: Can be made stable
- **In-place**: No
- **Best for**: Small integer ranges, when k ≤ n

**Limitations**:
- ✗ Only for non-negative integers
- ✗ Bad if range is huge (e.g., 1 to 10^9)
- ✗ Memory proportional to range

---

## 6. Radix Sort (Non-Comparison)

**Algorithm**: Sort by digits, least significant to most significant.

```python
def radix_sort(arr):
    if not arr:
        return arr
    
    max_num = max(arr)
    exp = 1
    
    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    counts = [0] * 10
    
    for num in arr:
        digit = (num // exp) % 10
        counts[digit] += 1
    
    for i in range(1, 10):
        counts[i] += counts[i - 1]
    
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[counts[digit] - 1] = arr[i]
        counts[digit] -= 1
    
    for i in range(n):
        arr[i] = output[i]
```

**Characteristics**:
- **Time**: O(d × (n + k)) where d = digits, k = 10
- **Space**: O(n + k)
- **Stable**: Yes
- **In-place**: No
- **Best for**: Multiple sort keys (tuples), large datasets with small digit count

---

## 7. Bucket Sort

**Algorithm**: Distribute into buckets, sort each bucket, concatenate.

```python
def bucket_sort(arr, num_buckets=10):
    if len(arr) == 0:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    bucket_range = (max_val - min_val) / num_buckets
    
    # Create buckets
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements
    for num in arr:
        if num == max_val:
            idx = num_buckets - 1
        else:
            idx = int((num - min_val) / bucket_range)
        buckets[idx].append(num)
    
    # Sort buckets and concatenate
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))  # Use any sort for small buckets
    
    return sorted_arr
```

**Characteristics**:
- **Time**: O(n + k) average, O(n²) worst
- **Space**: O(n + k)
- **Stable**: Can be made stable
- **In-place**: No
- **Best for**: Uniformly distributed data, floating point numbers

---

## 8. Shell Sort (Insertion Variant)

**Algorithm**: Insertion sort with increasing gap sequences.

```python
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            
            arr[j] = temp
        
        gap //= 2
    
    return arr
```

**Characteristics**:
- **Time**: O(n log n) to O(n^1.5) depending on gap sequence
- **Space**: O(1)
- **Stable**: No
- **In-place**: Yes
- **Best for**: Medium-sized arrays, simple implementation, adaptive data

---

## 9. Sorting Algorithm Comparison

| Algorithm | Best | Average | Worst | Space | Stable | In-place | Notes |
|-----------|------|---------|-------|-------|--------|----------|-------|
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No | Guaranteed |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Yes | Practical |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Yes | Guaranteed |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | No | Ints only |
| Radix | O(dn+k) | O(dn+k) | O(dn+k) | O(n) | Yes | No | Fixed digits |
| Bucket | O(n+k) | O(n+k) | O(n²) | O(n) | Yes | No | Uniform dist |
| Shell | O(n log n) | O(n^1.25) | O(n^2) | O(1) | No | Yes | Adaptive |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes | Small arrays |
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes | Educational |

---

## 10. When to Use Each Algorithm

### Use Merge Sort:
- ✓ Need guaranteed O(n log n)
- ✓ Stability required
- ✓ Linked lists (no random access)
- ✓ External sorting (disk-based)

### Use Quick Sort:
- ✓ General purpose sorting
- ✓ In-memory performance critical
- ✓ Cache locality important
- ✓ Practical default choice

### Use Heap Sort:
- ✓ Guaranteed O(n log n) with O(1) space
- ✓ Real-time systems
- ✓ Priority queue needed
- ✓ No recursion available

### Use Counting Sort:
- ✓ Small integer range (k ≤ n)
- ✓ All values in known range
- ✓ Speed critical, not memory

### Use Radix Sort:
- ✓ Multiple sort keys
- ✓ Fixed-length integers/strings
- ✓ Very large datasets
- ✓ Stability required

### Use Bucket Sort:
- ✓ Uniformly distributed data
- ✓ Floating point numbers
- ✓ External sorting
- ✓ Distributed systems

---

## 11. Optimization Techniques

### 1. Choosing Pivot (Quick Sort)
```python
# Random pivot avoids O(n²) on sorted data
import random

def partition_random(arr, low, high):
    random_idx = random.randint(low, high)
    arr[random_idx], arr[high] = arr[high], arr[random_idx]
    return partition(arr, low, high)
```

### 2. 3-Way Partition (Handling Duplicates)
```python
def partition_3way(arr, low, high):
    # Handles many equal elements efficiently
    # Returns (lt, gt) where arr[low..lt-1] < pivot
    # arr[lt..gt] == pivot, arr[gt+1..high] > pivot
    pass
```

### 3. Adaptive Sorting (Tim Sort - Python)
Hybrid of merge and insertion sort.
- Uses insertion for small runs
- Merges runs with merge sort
- Detects existing order

### 4. Hybrid Approaches
```python
def hybrid_sort(arr):
    if len(arr) < 10:
        return insertion_sort(arr)
    else:
        return quick_sort(arr)
```

---

## 12. Stability in Sorting

**Stable**: Equal elements keep relative order
**Unstable**: Equal elements may reorder

```
Original:  [(2, 'a'), (1, 'b'), (2, 'c')]
After stable sort by key 0:  [(1, 'b'), (2, 'a'), (2, 'c')]
After unstable sort by key 0: [(1, 'b'), (2, 'c'), (2, 'a')]
```

**Stable**: Merge, Counting, Radix, Bucket, Insertion
**Unstable**: Quick, Heap, Shell

---

## 13. Key Takeaways

✅ **Merge Sort**: O(n log n) guaranteed, stable, space trade-off  
✅ **Quick Sort**: O(n log n) practical, in-place, cache-friendly  
✅ **Heap Sort**: O(n log n) guaranteed, O(1) space, no recursion  
✅ **Counting Sort**: O(n+k) for small ranges, non-comparison  
✅ **Radix Sort**: O(dn+k) for fixed-length numbers, stable  
✅ **Stability**: Matters when sorting objects by one key  
✅ **In-place**: Critical for large datasets  
✅ **Hybrid**: Modern sorts combine techniques  

**Default Choice**: Quick Sort or Tim Sort (Python default)  
**Interview Favorite**: Merge and Quick Sort implementations

Next: Practice implementing and comparing sorting algorithms!
