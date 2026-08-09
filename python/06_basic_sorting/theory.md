# Basic Sorting Algorithms

Master the fundamental sorting algorithms and understand their trade-offs.

---

## 1. What is Sorting?

**Sorting** is the process of arranging elements in a specific order (usually ascending or descending).

### Why Learn Basic Sorts?
- Foundation for understanding complex algorithms
- Interview favorites despite being "simple"
- Useful for small datasets
- Great for learning algorithm analysis
- Understand trade-offs and optimizations

### Real-world examples:
- Sorting student grades
- Arranging contact lists
- Ordering search results
- Organizing file listings

---

## 2. Bubble Sort

**Idea**: Compare adjacent elements and swap if out of order. "Bubbles" largest element to end each pass.

### Implementation:
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
```

### Complexity:
- **Best case**: O(n) - already sorted (with early exit)
- **Average case**: O(n²) - random order
- **Worst case**: O(n²) - reverse sorted
- **Space**: O(1) - sorts in place
- **Stable**: Yes - equal elements keep order

### Visual:
```
Pass 1: [5, 3, 8, 4, 2] → [3, 5, 4, 2, 8]
Pass 2: [3, 5, 4, 2, 8] → [3, 4, 2, 5, 8]
Pass 3: [3, 4, 2, 5, 8] → [3, 2, 4, 5, 8]
Pass 4: [3, 2, 4, 5, 8] → [2, 3, 4, 5, 8] ✓
```

### When to use:
- Small arrays (n < 50)
- Nearly sorted data
- Teaching/learning
- ❌ Never use in production!

---

## 3. Selection Sort

**Idea**: Find minimum element and place at beginning. Repeat for rest of array.

### Implementation:
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

### Complexity:
- **Best case**: O(n²) - always scans all
- **Average case**: O(n²) - no advantage
- **Worst case**: O(n²) - reverse sorted
- **Space**: O(1) - sorts in place
- **Stable**: No - moves elements

### Visual:
```
[5, 3, 8, 4, 2]
Min = 2, swap: [2, 3, 8, 4, 5]
Min = 3, swap: [2, 3, 8, 4, 5]
Min = 4, swap: [2, 3, 4, 8, 5]
Min = 5, swap: [2, 3, 4, 5, 8] ✓
```

### When to use:
- When writes are expensive (minimizes swaps)
- Small arrays
- ❌ Generally avoid for other reasons

---

## 4. Insertion Sort

**Idea**: Build sorted array one element at a time. Insert each element into correct position.

### Implementation:
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

### Complexity:
- **Best case**: O(n) - already sorted
- **Average case**: O(n²) - random order
- **Worst case**: O(n²) - reverse sorted
- **Space**: O(1) - sorts in place
- **Stable**: Yes - maintains relative order

### Visual:
```
[5, 3, 8, 4, 2]
[3, 5, 8, 4, 2] - insert 3
[3, 5, 8, 4, 2] - 8 already in place
[3, 4, 5, 8, 2] - insert 4
[2, 3, 4, 5, 8] - insert 2 ✓
```

### When to use:
- Nearly sorted data (O(n) best case!)
- Small arrays (n < 50)
- Online sorting (elements arrive one by one)
- Hybrid algorithms (final stage of quicksort)

---

## 5. Complexity Comparison

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| **Bubble** | O(n) | O(n²) | O(n²) | O(1) | Yes |
| **Selection** | O(n²) | O(n²) | O(n²) | O(1) | No |
| **Insertion** | O(n) | O(n²) | O(n²) | O(1) | Yes |

### Key Differences:
- **Bubble**: Simple but slow. Early exit helps.
- **Selection**: Consistent O(n²), minimizes swaps.
- **Insertion**: Best for nearly sorted data.

---

## 6. Sorting Stability

A sort is **stable** if equal elements maintain their original order.

```python
# Original: [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]
# Sort by first element

# Stable result: [(1, 'b'), (1, 'd'), (2, 'a'), (2, 'c')]
# (1, 'b') comes before (1, 'd') ✓
# (2, 'a') comes before (2, 'c') ✓

# Unstable result: [(1, 'd'), (1, 'b'), (2, 'c'), (2, 'a')]
# (1, 'd') now before (1, 'b') ✗
```

- **Stable**: Bubble Sort, Insertion Sort, Merge Sort
- **Unstable**: Selection Sort, Quicksort, Heap Sort

---

## 7. In-Place vs Out-of-Place

- **In-place**: O(1) extra space (all basic sorts)
- **Out-of-place**: O(n) extra space (merge sort)

Trade-off: Space vs. convenience

---

## 8. Practical Optimizations

### Optimization 1: Early Exit (Bubble Sort)
```python
def bubble_sort_optimized(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            return arr  # Already sorted!
    return arr
```

### Optimization 2: Adaptive Insertion Sort
Works great on nearly sorted data (O(n) best case).

### Optimization 3: Hybrid Approach
Use insertion sort for small sub-arrays in larger sorts.

---

## 9. Real-World Usage

| Scenario | Best Sort | Why |
|----------|-----------|-----|
| Small array (n < 50) | Insertion | O(n) for nearly sorted |
| Nearly sorted | Insertion | O(n) best case |
| General purpose | Merge Sort (not in basic) | O(n log n) guaranteed |
| Memory limited | Quicksort (not in basic) | O(log n) space |
| Stability needed | Merge Sort | Keeps equal order |

### Important Rule:
**Never use basic sorts in production!** Use Python's built-in `sorted()` or `.sort()` which use optimized algorithms (Timsort).

---

## 10. Algorithm Selection Guide

```
Is data nearly sorted?
├─ YES → Use Insertion Sort (O(n) best case!)
└─ NO → Is it small (n < 50)?
    ├─ YES → Use Insertion Sort or Bubble Sort (fine for teaching)
    └─ NO → Use Merge Sort or built-in sort (Python's sorted())
```

---

## 11. Sorting Algorithm Characteristics

| Feature | Bubble | Selection | Insertion |
|---------|--------|-----------|-----------|
| **Easy to code** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Efficient** | ✗ | ✗ | ⭐ (near-sorted) |
| **In-place** | ✓ | ✓ | ✓ |
| **Stable** | ✓ | ✗ | ✓ |
| **Adaptive** | ✓ | ✗ | ✓ |
| **Best for** | Teaching | Theory | Nearly sorted |

---

## 12. Practice Counting Swaps & Comparisons

Understanding cost metrics:

```python
# Count comparisons
def bubble_sort_with_count(arr):
    comparisons = 0
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr, comparisons

arr = [5, 3, 8, 1, 2]
sorted_arr, comps = bubble_sort_with_count(arr)
print(f"Comparisons: {comps}")  # 10 for array of 5
```

For array of size n:
- **Comparisons**: n(n-1)/2 ≈ O(n²)
- **Swaps**: 0 to n(n-1)/2 depending on data

---

## Key Takeaways

✅ **Bubble Sort**: Simple, teaches basics, slow  
✅ **Selection Sort**: Minimal swaps, consistent O(n²)  
✅ **Insertion Sort**: Best for nearly sorted, O(n) best case  
✅ **Complexity**: All O(n²) average/worst, O(1) space  
✅ **Stability**: Matters for equal elements  
✅ **In-practice**: Use built-in sort(), not these!  
✅ **Learning**: Master these to understand advanced sorts  

Next: See practical implementations and when to use each!
