# Heaps & Priority Queues - "Give Me the Best One"

Master the binary heap, Python's `heapq`, the top-K pattern, two-heap
tricks, and k-way merging — the toolkit for every "smallest/largest/median"
question.

---

## 1. The Question a Heap Answers

Not "is X present?" (that's a hash set) and not "give me sorted order"
(that's a sort). A heap answers exactly one question, repeatedly and cheaply:

> **"What is the smallest (or largest) item right now?"**

...while items keep arriving and leaving.

| Structure | Get min | Remove min | Insert | Keeps full order? |
|-----------|---------|------------|--------|-------------------|
| Unsorted list | O(n) | O(n) | O(1) | no |
| Sorted list | O(1) | O(1) end / O(n) front | **O(n)** | yes |
| **Binary heap** | **O(1)** | **O(log n)** | **O(log n)** | **no** |
| Balanced BST | O(log n) | O(log n) | O(log n) | yes |

The heap's trade is deliberate: it gives up full ordering to make
insert-and-extract-min both logarithmic. If you need the whole sorted
sequence, sort. If you need *the best one, over and over*, use a heap.

---

## 2. The Structure

A binary heap is a **complete binary tree** stored in a flat array.

**Heap property (min-heap)**: every parent ≤ both of its children.

```
        1
      /   \
     3     5          array: [1, 3, 5, 7, 9, 8]
    / \   /            index:  0  1  2  3  4  5
   7   9 8
```

Note what is *not* guaranteed: the array is not sorted, and siblings have no
relationship. Only the parent-child edge is ordered. That weaker invariant
is exactly why it's cheap to maintain.

### Array Index Arithmetic

For a 0-indexed array:

```python
parent(i)      = (i - 1) // 2
left_child(i)  = 2 * i + 1
right_child(i) = 2 * i + 2
```

No pointers, no allocation per node — the tree structure is implied by
arithmetic. This is why heaps are fast in practice, not just in theory.

**Height** of a complete tree with n nodes is ⌊log₂ n⌋, which bounds every
operation below.

---

## 3. The Two Core Operations

Everything a heap does is `sift_up` and `sift_down`.

### Sift Up (after inserting at the end)

```python
def sift_up(heap, i):
    """Bubble heap[i] toward the root until the parent is smaller."""
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] < heap[parent]:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break
```

### Sift Down (after removing the root)

```python
def sift_down(heap, i, n):
    """Push heap[i] toward the leaves until both children are larger."""
    while True:
        smallest = i
        for child in (2 * i + 1, 2 * i + 2):
            if child < n and heap[child] < heap[smallest]:
                smallest = child
        if smallest == i:
            return
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest
```

### Push and Pop

```python
def push(heap, value):
    """Append, then sift up. O(log n)"""
    heap.append(value)
    sift_up(heap, len(heap) - 1)

def pop(heap):
    """Swap root with last, shrink, sift down. O(log n)"""
    heap[0], heap[-1] = heap[-1], heap[0]
    smallest = heap.pop()
    if heap:
        sift_down(heap, 0, len(heap))
    return smallest
```

The pop trick matters: you can't just remove `heap[0]` (that leaves a hole
and shifts everything). Swapping the last element into the root keeps the
tree complete, then one sift-down restores the invariant.

---

## 4. Heapify: Building a Heap in O(n)

The obvious way to build a heap is n pushes — O(n log n). But you can do it
in **O(n)**:

```python
def heapify(arr):
    """Sift down from the last parent to the root. O(n), not O(n log n)."""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):     # last parent -> root
        sift_down(arr, i, n)
```

**Why O(n)?** Most nodes are near the bottom and barely move. Half the nodes
are leaves (0 work), a quarter are one level up (≤1 swap), an eighth are two
levels up (≤2 swaps)...

```
Total work = n/2 · 0 + n/4 · 1 + n/8 · 2 + n/16 · 3 + ...
           = n · Σ(k / 2^(k+1))
           = n · 1
           = O(n)
```

The series converges to a constant. This is a favourite interview follow-up:
*"you said heapify is O(n) — prove it."*

---

## 5. Python's `heapq`

Python ships a **min-heap** operating on ordinary lists. There's no heap
object — the functions mutate a list in place.

```python
import heapq

h = []
heapq.heappush(h, 5)
heapq.heappush(h, 1)
heapq.heappush(h, 3)

h[0]                        # 1 -- peek, O(1), no function call needed
heapq.heappop(h)            # 1 -- O(log n)

heapq.heapify(existing)     # O(n), in place
heapq.heappushpop(h, x)     # push then pop, one sift
heapq.heapreplace(h, x)     # pop then push, one sift
heapq.nsmallest(k, iterable)
heapq.nlargest(k, iterable)
heapq.merge(*sorted_iters)  # lazy k-way merge, returns an iterator
```

### Max-Heap in Python

`heapq` is min-only. Three ways to get a max-heap:

```python
# 1. Negate on the way in and out (most common, integers/floats)
heapq.heappush(h, -value)
largest = -heapq.heappop(h)

# 2. Wrap in a class with inverted __lt__
# 3. heapq._heapify_max(...)  -- private, do not rely on it
```

Negation is the idiomatic answer. Say it out loud in an interview; it's a
known Python wart and interviewers expect you to know the workaround.

### `heappushpop` vs `heapreplace`

Both do a push and a pop with **one** sift instead of two — meaningfully
faster in a hot loop.

| | Order | If new item is smaller than the root |
|---|---|---|
| `heappushpop(h, x)` | push, then pop | returns `x` itself; heap unchanged |
| `heapreplace(h, x)` | pop, then push | returns the old root; `x` goes in |

For the top-K pattern, `heappushpop` is what you want — it naturally
rejects items that don't qualify.

### Tuples and Tie-Breaking

Heaps compare whole tuples element by element:

```python
heapq.heappush(h, (priority, task))
```

**The classic bug**: if two priorities tie, Python compares the second
element. If that's an object without `__lt__`, you get a `TypeError` — and
only sometimes, when a tie happens to occur. Fix it with a monotonic
counter:

```python
counter = itertools.count()
heapq.heappush(h, (priority, next(counter), task))   # never ties
```

This also makes the queue **stable** — equal priorities come out in
insertion order.

---

## 6. Pattern: Top-K Elements

**The insight that trips people up**: to find the K *largest* items, use a
**min**-heap of size K.

Why: you want cheap access to the *weakest survivor*, so you can evict it
when something better arrives. That weakest item is the min of your K
keepers.

```python
def top_k_largest(nums, k):
    """K largest elements. O(n log k) time, O(k) space."""
    heap = []
    for n in nums:
        if len(heap) < k:
            heapq.heappush(heap, n)
        elif n > heap[0]:                    # better than the weakest keeper
            heapq.heappushpop(heap, n)       # one sift, not two
    return heap                              # unsorted; sort if needed
```

### Why Not Just Sort?

| Approach | Time | Space | When |
|----------|------|-------|------|
| Sort, take K | O(n log n) | O(n) | k close to n; you need them sorted |
| **Heap of size K** | **O(n log k)** | **O(k)** | **k ≪ n** |
| Quickselect | O(n) average | O(1) | one-shot, in-memory, k-th only |
| `heapq.nlargest` | O(n log k) | O(k) | just use this in real Python code |

The heap wins decisively when **k ≪ n** or when data **streams** — you can't
sort a stream you can't hold in memory, but a size-K heap needs only O(k).

**Honest note**: for a one-shot in-memory k-th element, quickselect is
O(n) and beats the heap asymptotically. The heap wins on streaming and on
"keep the top K updated as data arrives."

---

## 7. Pattern: Two Heaps (Running Median)

To track the median of a growing stream, split the data at the middle:

- **Max-heap** (`low`) holds the smaller half
- **Min-heap** (`high`) holds the larger half
- Keep sizes balanced within 1

The median is then at the top of one or both heaps — O(1) to read.

```python
class MedianFinder:
    def __init__(self):
        self.low = []      # max-heap (negated values)
        self.high = []     # min-heap

    def add(self, num):
        """O(log n)"""
        heapq.heappush(self.low, -num)
        # Move the largest of `low` over to `high`
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # Rebalance so len(low) >= len(high), differing by at most 1
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        """O(1)"""
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
```

The push-then-move dance looks redundant but guarantees the element lands in
the correct half without any comparisons. Worth memorising as a unit.

**Real use**: p50/p95 latency dashboards, adaptive thresholds, streaming
statistics.

---

## 8. Pattern: K-Way Merge

Merging k sorted sequences with a heap of size k:

```python
def merge_k_sorted(lists):
    """O(N log k) where N is the total element count."""
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))    # (value, list index, pos)

    out = []
    while heap:
        value, li, pos = heapq.heappop(heap)
        out.append(value)
        if pos + 1 < len(lists[li]):
            heapq.heappush(heap, (lists[li][pos + 1], li, pos + 1))
    return out
```

Concatenating and sorting is O(N log N). The heap is **O(N log k)**, and
since k ≪ N usually, that's a real win. More importantly, the heap version
is **streaming** — it never holds all N items, which matters for external
merge sort on data larger than memory.

`heapq.merge()` does exactly this, lazily. Use it in production code.

---

## 9. Pattern: Scheduling and Simulation

A heap keyed by *time* turns "what happens next?" into a pop.

```python
def min_meeting_rooms(intervals):
    """Fewest rooms needed. O(n log n)"""
    intervals.sort(key=lambda x: x[0])          # by start time
    rooms = []                                  # min-heap of end times

    for start, end in intervals:
        if rooms and rooms[0] <= start:         # earliest room is free
            heapq.heapreplace(rooms, end)
        else:
            heapq.heappush(rooms, end)

    return len(rooms)
```

The heap holds one end-time per occupied room. Its root is the room that
frees up soonest — precisely the question you need answered at each step.

This same shape solves task scheduling, CPU scheduling, event simulation,
and the "reorganize string" family.

---

## 10. Heaps You Have Already Used

Heaps appeared earlier in this curriculum without a dedicated chapter:

| Topic | Where | Why a heap |
|-------|-------|------------|
| 13 Advanced Sorting | Heap Sort | heapify then pop n times → O(n log n), in place |
| 14 Graph Algorithms | Dijkstra | always expand the nearest unvisited vertex |
| 14 Graph Algorithms | Prim's MST | always take the cheapest edge leaving the tree |
| 15 Greedy Algorithms | Huffman coding | always merge the two lowest frequencies |

Notice the common phrasing: *"always take the smallest X next."* That
sentence is the heap's signature. When a greedy algorithm needs the best
remaining option repeatedly, a heap is what makes it O(log n) per step
instead of O(n).

---

## 11. Complexity Summary

| Operation | Time | Note |
|-----------|------|------|
| Peek min | **O(1)** | just `heap[0]` |
| Push | O(log n) | append + sift up |
| Pop min | O(log n) | swap + shrink + sift down |
| `heappushpop` / `heapreplace` | O(log n) | one sift, not two |
| Build via n pushes | O(n log n) | the naive way |
| **Build via heapify** | **O(n)** | sift down from the last parent |
| Heap sort | O(n log n) | heapify + n pops, O(1) extra space |
| Find arbitrary element | **O(n)** | no search structure — a real limitation |
| Delete arbitrary element | **O(n)** | must find it first |
| Merge two heaps | O(n) | re-heapify; use a Fibonacci heap for O(1) |
| Top-K | O(n log k) | size-K heap |
| K-way merge | O(N log k) | size-K heap |

**Space**: O(n) for the heap, O(1) auxiliary for all operations.

### The Limitation Worth Knowing

A heap **cannot search**. Finding whether value X is present is O(n) — no
better than a list. If you need both "give me the min" *and* "remove this
specific item," you need either:

- an **indexed heap** (a dict mapping value → position, updated on every swap), or
- **lazy deletion**: mark items dead in a set and skip them on pop, or
- a different structure entirely (a balanced BST gives both in O(log n))

Lazy deletion is by far the most common practical answer.

---

## 12. Choosing a Structure

```
Do you repeatedly need the best/smallest/largest item?
├── NO
│   ├── need full sorted order?      -> sort (Timsort)
│   ├── need membership tests?       -> set / dict
│   └── need ranges or successor?    -> balanced BST (Topic 17)
└── YES
    ├── also need to delete arbitrary items?
    │   ├── frequently  -> balanced BST, or heap + lazy deletion
    │   └── rarely      -> heap + lazy deletion
    ├── k-th element, one shot, fits in memory? -> quickselect, O(n)
    ├── top K from a stream?                    -> min-heap of size k
    ├── running median?                         -> two heaps
    ├── merge k sorted sources?                 -> heap of size k
    └── "always process the nearest/cheapest next"? -> heap (Dijkstra shape)
```

---

## 13. Common Pitfalls

1. **Using a max-heap for top-K largest.** It's a **min**-heap of size K.
   Getting this backwards is the single most common heap mistake.
2. **Forgetting `heapq` is min-only.** Negate for a max-heap, and say so
   out loud.
3. **Negating without un-negating.** If you push `-x`, you must return
   `-heappop(h)`. Easy to drop on one branch.
4. **Tuple tie-break `TypeError`.** `(priority, obj)` explodes when
   priorities tie and `obj` has no `__lt__` — and only on ties, so it passes
   your tests and fails in production. Add a counter.
5. **Assuming the heap array is sorted.** It isn't. Only `heap[0]` is
   meaningful. Printing the list to "check" it will mislead you.
6. **`heapq.heapify` on a list of lists.** It mutates in place and compares
   inner lists elementwise — rarely what you meant.
7. **Popping from an empty heap.** `IndexError`. Guard `while heap:`.
8. **Building with n pushes when heapify would do.** O(n log n) vs O(n) for
   the same result.
9. **Trying to update a priority in place.** There's no `decrease_key` in
   `heapq`. Push a new entry and lazily discard the stale one — this is
   exactly what Dijkstra implementations do.
10. **Reaching for a heap when you need one sort.** If you pop everything
    out anyway, you just wrote a slower sort.

---

## 14. Key Takeaways

✅ **A heap answers one question**: "what's the best item right now?"
✅ **Complete tree in a flat array** — children at `2i+1`, `2i+2`, parent at `(i-1)//2`
✅ **Only the parent-child edge is ordered** — siblings are unrelated, the array is not sorted
✅ **`sift_up` and `sift_down`** are the whole implementation
✅ **`heapify` is O(n)**, not O(n log n) — most nodes barely move; be ready to prove it
✅ **Top-K largest needs a MIN-heap of size K** — you evict the weakest keeper
✅ **`heapq` is min-only**; negate for a max-heap
✅ **Add a counter to tuples** to avoid tie-break `TypeError` and get stability
✅ **Two heaps track a running median** in O(log n) add, O(1) read
✅ **Heaps cannot search** — O(n) to find an arbitrary item; use lazy deletion
✅ **"Always take the smallest next"** is the phrase that signals a heap

**Interview Focus**:
- State the min-heap-for-max-K inversion explicitly; it's the tell that you
  actually understand the pattern rather than recalling a template
- Prove heapify is O(n) when asked — the series argument, not hand-waving
- Compare against sorting *and* quickselect, and say when each wins
- Mention `heappushpop` as the one-sift optimisation
- Bring up the tuple tie-break bug unprompted; it's a real-world scar
- Name the limitation (no search) before the interviewer does

Next: implement the heap from scratch, then drill the four patterns —
top-K, two-heap median, k-way merge, and scheduling!
