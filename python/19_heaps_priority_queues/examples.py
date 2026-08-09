"""
Examples: Heaps & Priority Queues

Build a heap from scratch, then drill the four patterns:
top-K, two-heap median, k-way merge, and scheduling.
"""

import heapq
import itertools
import random
import time
from typing import List, Tuple, Any, Optional

print("=" * 70)
print("HEAPS & PRIORITY QUEUES")
print("=" * 70)

# ==================== (1) The Structure ====================
print("\n[1] The Structure: A Complete Tree in a Flat Array")
print("-" * 70)

def show_heap(arr: List[int], label: str = "") -> None:
    """Print a heap as a tree, level by level."""
    if label:
        print(f"  {label}")
    if not arr:
        print("    (empty)")
        return
    level = 0
    i = 0
    n = len(arr)
    while i < n:
        count = 1 << level
        row = arr[i:i + count]
        pad = " " * (2 ** (4 - min(level, 3)))
        print(f"    {pad}{'   '.join(f'{v:>2}' for v in row)}")
        i += count
        level += 1

heap = [1, 3, 5, 7, 9, 8]
print(f"  array: {heap}")
print(f"  index:  0  1  2  3  4  5\n")
show_heap(heap, "as a tree:")

print("\n  Index arithmetic (0-indexed):")
print("    parent(i)      = (i - 1) // 2")
print("    left_child(i)  = 2*i + 1")
print("    right_child(i) = 2*i + 2\n")

print(f"  {'i':>3} {'value':>6} {'parent':>8} {'children':>14}")
print("  " + "-" * 36)
for i in range(len(heap)):
    p = (i - 1) // 2
    l, r = 2 * i + 1, 2 * i + 2
    parent = f"{heap[p]}" if i > 0 else "-"
    kids = []
    if l < len(heap):
        kids.append(str(heap[l]))
    if r < len(heap):
        kids.append(str(heap[r]))
    print(f"  {i:>3} {heap[i]:>6} {parent:>8} {', '.join(kids) or '-':>14}")

print("\n  -> Every parent <= both children. That is the ONLY guarantee.")
print("  -> Siblings are unrelated. The array is NOT sorted.")
print("  -> No pointers: the tree shape is pure index arithmetic.")

# ==================== (2) Sift Up / Sift Down ====================
print("\n[2] The Two Core Operations")
print("-" * 70)

def sift_up(heap: List, i: int, trace: bool = False) -> int:
    """Bubble heap[i] toward the root. Returns swap count."""
    swaps = 0
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] < heap[parent]:
            if trace:
                print(f"      swap {heap[i]} (idx {i}) with parent "
                      f"{heap[parent]} (idx {parent})")
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
            swaps += 1
        else:
            break
    return swaps


def sift_down(heap: List, i: int, n: int, trace: bool = False) -> int:
    """Push heap[i] toward the leaves. Returns swap count."""
    swaps = 0
    while True:
        smallest = i
        for child in (2 * i + 1, 2 * i + 2):
            if child < n and heap[child] < heap[smallest]:
                smallest = child
        if smallest == i:
            return swaps
        if trace:
            print(f"      swap {heap[i]} (idx {i}) with child "
                  f"{heap[smallest]} (idx {smallest})")
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest
        swaps += 1


print("SIFT UP -- inserting 0 into [1, 3, 5, 7, 9, 8]:")
h = [1, 3, 5, 7, 9, 8]
h.append(0)
print(f"    append at the end: {h}")
sift_up(h, len(h) - 1, trace=True)
print(f"    result: {h}")
show_heap(h)

print("\nSIFT DOWN -- removing the root from that heap:")
h[0], h[-1] = h[-1], h[0]
removed = h.pop()
print(f"    swap root with last, pop -> removed {removed}, array {h}")
sift_down(h, 0, len(h), trace=True)
print(f"    result: {h}")
show_heap(h)

print("\n  -> Both walk one root-to-leaf path: O(log n)")
print("  -> Pop swaps the LAST element into the root; removing heap[0]")
print("     directly would leave a hole and break completeness.")

# ==================== (3) A Heap From Scratch ====================
print("\n[3] A Complete MinHeap Implementation")
print("-" * 70)

class MinHeap:
    """Binary min-heap built from scratch. Mirrors heapq's semantics."""

    def __init__(self, items: Optional[List] = None):
        self.data: List = list(items) if items else []
        self.sift_count = 0
        if self.data:
            self.heapify()

    def __len__(self) -> int:
        return len(self.data)

    def peek(self):
        """O(1)"""
        if not self.data:
            raise IndexError("peek from an empty heap")
        return self.data[0]

    def push(self, value) -> None:
        """O(log n)"""
        self.data.append(value)
        self.sift_count += sift_up(self.data, len(self.data) - 1)

    def pop(self):
        """O(log n)"""
        if not self.data:
            raise IndexError("pop from an empty heap")
        self.data[0], self.data[-1] = self.data[-1], self.data[0]
        smallest = self.data.pop()
        if self.data:
            self.sift_count += sift_down(self.data, 0, len(self.data))
        return smallest

    def pushpop(self, value):
        """Push then pop with ONE sift. O(log n)"""
        if self.data and self.data[0] < value:
            value, self.data[0] = self.data[0], value
            self.sift_count += sift_down(self.data, 0, len(self.data))
        return value

    def heapify(self) -> None:
        """Build in O(n) -- sift down from the last parent to the root."""
        n = len(self.data)
        for i in range(n // 2 - 1, -1, -1):
            self.sift_count += sift_down(self.data, i, n)

    def is_valid(self) -> bool:
        """Verify the heap property at every node."""
        n = len(self.data)
        for i in range(n):
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and self.data[child] < self.data[i]:
                    return False
        return True

    def sorted_drain(self) -> List:
        """Pop everything -- this is heap sort."""
        return [self.pop() for _ in range(len(self.data))]


values = [9, 4, 7, 1, 8, 2, 6, 3, 5]
mh = MinHeap(values)
print(f"  heapify({values})")
print(f"    -> {mh.data}")
print(f"    valid heap: {mh.is_valid()}")
show_heap(mh.data)

print(f"\n  peek()  -> {mh.peek()}  (O(1), no work)")
print(f"  push(0) -> ", end="")
mh.push(0)
print(f"{mh.data}")
print(f"  pop()   -> {mh.pop()}, heap now {mh.data}")

drained = MinHeap(values).sorted_drain()
print(f"\n  Draining the heap gives sorted output (this IS heap sort):")
print(f"    {drained}")
print(f"    correctly sorted: {drained == sorted(values)}")

# ==================== (4) Heapify is O(n), Not O(n log n) ====================
print("\n[4] Why heapify is O(n) -- Measured")
print("-" * 70)

print("The argument: half the nodes are leaves and do ZERO work. A quarter")
print("sit one level up and do at most 1 swap. An eighth do at most 2...\n")
print("  Total = n/2*0 + n/4*1 + n/8*2 + n/16*3 + ...  =  n * sum(k/2^(k+1))")
print("        = n * 1  =  O(n)   -- the series converges to a constant\n")

print(f"  {'n':>8} {'heapify swaps':>15} {'n pushes swaps':>16} {'swaps/n':>9}")
print("  " + "-" * 52)
for n in [1000, 4000, 16_000, 64_000]:
    random.seed(n)
    arr = [random.randint(0, 1_000_000) for _ in range(n)]

    h1 = MinHeap()
    h1.data = list(arr)
    h1.sift_count = 0
    h1.heapify()
    heapify_swaps = h1.sift_count

    h2 = MinHeap()
    for v in arr:
        h2.push(v)
    push_swaps = h2.sift_count

    print(f"  {n:>8} {heapify_swaps:>15,} {push_swaps:>16,} "
          f"{heapify_swaps / n:>9.2f}")

print("\n  -> swaps/n stays FLAT as n grows 64x. That is the signature of O(n).")
print("     If heapify were O(n log n), that column would grow with log(n).")

# Wall clock too
print("\n  Wall clock on 200,000 items:")
random.seed(1)
big = [random.randint(0, 10_000_000) for _ in range(200_000)]

start = time.perf_counter()
h = list(big)
heapq.heapify(h)
heapify_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
h2: List[int] = []
for v in big:
    heapq.heappush(h2, v)
push_ms = (time.perf_counter() - start) * 1000

print(f"    heapq.heapify   : {heapify_ms:>8.1f}ms   O(n)")
print(f"    200k heappushes : {push_ms:>8.1f}ms   O(n log n)")
print(f"    -> heapify is {push_ms / heapify_ms:.1f}x faster for the same result")
print(f"    Both produce valid heaps: {h[0] == h2[0] == min(big)}")

# ==================== (5) Python's heapq ====================
print("\n[5] Python's heapq (Min-Heap on a Plain List)")
print("-" * 70)

h: List[int] = []
for v in [5, 1, 8, 3, 9, 2]:
    heapq.heappush(h, v)

print(f"  after pushes    : {h}")
print(f"  h[0] (peek)     : {h[0]}      <- just index it, O(1)")
print(f"  heappop()       : {heapq.heappop(h)}, heap now {h}")
print(f"  nsmallest(3, h) : {heapq.nsmallest(3, h)}")
print(f"  nlargest(3, h)  : {heapq.nlargest(3, h)}")

print("\n  MAX-heap via negation (heapq is min-only):")
max_h: List[int] = []
for v in [5, 1, 8, 3, 9, 2]:
    heapq.heappush(max_h, -v)          # negate going in
print(f"    stored (negated): {max_h}")
print(f"    largest         : {-max_h[0]}       <- negate coming out")
print(f"    pop order       : ", end="")
print([-heapq.heappop(max_h) for _ in range(len(max_h))])

print("\n  heappushpop vs heapreplace (both = one sift, not two):")
a = [1, 3, 5]
b = [1, 3, 5]
print(f"    heap = {a}, new item = 0  (SMALLER than the root)")
print(f"      heappushpop -> returns {heapq.heappushpop(a, 0)}, heap {a}"
      f"   (rejected 0, heap unchanged)")
print(f"      heapreplace -> returns {heapq.heapreplace(b, 0)}, heap {b}"
      f"   (evicted 1, 0 went in)")
print("    -> For top-K, heappushpop is what you want: it naturally")
print("       rejects items that do not qualify.")

# The tuple tie-break bug
print("\n  THE TUPLE TIE-BREAK BUG (a real production scar):")

class Task:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Task({self.name})"

buggy: List[Tuple[int, Task]] = []
heapq.heappush(buggy, (1, Task("a")))
try:
    heapq.heappush(buggy, (1, Task("b")))       # SAME priority -> compares Tasks
    print("    no error raised")
except TypeError as e:
    print(f"    TypeError on equal priorities: {e}")
    print("    -> It only fails WHEN A TIE OCCURS. Passes your tests,")
    print("       explodes in production.")

counter = itertools.count()
fixed: List[Tuple[int, int, Task]] = []
for name in "abc":
    heapq.heappush(fixed, (1, next(counter), Task(name)))
print(f"    Fixed with a counter: pop order = "
      f"{[heapq.heappop(fixed)[2].name for _ in range(len(fixed))]}")
print("    -> The counter breaks ties AND makes the queue stable (FIFO")
print("       within equal priorities).")

# ==================== (6) Pattern: Top-K ====================
print("\n[6] Pattern: Top-K Elements")
print("-" * 70)

print("THE KEY INVERSION: to find the K LARGEST, use a MIN-heap of size K.")
print("You want cheap access to the WEAKEST survivor, so you can evict it.\n")

def top_k_largest(nums: List[int], k: int) -> List[int]:
    """K largest. O(n log k) time, O(k) space."""
    heap: List[int] = []
    for n in nums:
        if len(heap) < k:
            heapq.heappush(heap, n)
        elif n > heap[0]:                       # beats the weakest keeper
            heapq.heappushpop(heap, n)
    return sorted(heap, reverse=True)


def kth_largest(nums: List[int], k: int) -> int:
    """The k-th largest = the root of that size-K min-heap."""
    heap: List[int] = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)
        # heap[0] is now the k-th largest seen so far
    return heap[0]


random.seed(7)
data = random.sample(range(1, 1000), 20)
print(f"  data (20 items): {sorted(data, reverse=True)[:8]} ...")
print(f"  top_k_largest(data, 5) -> {top_k_largest(data, 5)}")
print(f"  verify via sort        -> {sorted(data, reverse=True)[:5]}")
print(f"  kth_largest(data, 3)   -> {kth_largest(data, 3)}"
      f"   (verify: {sorted(data, reverse=True)[2]})")

# Walk through the heap state to make the eviction visible
print("\n  Watching the size-3 min-heap evolve (k=3, largest):")
demo = [5, 12, 3, 20, 8, 15, 1]
hp: List[int] = []
print(f"    {'item':>6}  {'action':<22} {'heap (min at [0])':<20}")
print("    " + "-" * 52)
for v in demo:
    if len(hp) < 3:
        heapq.heappush(hp, v)
        action = "push (still filling)"
    elif v > hp[0]:
        evicted = heapq.heappushpop(hp, v)
        action = f"evict {evicted}, admit {v}"
    else:
        action = f"reject ({v} <= {hp[0]})"
    print(f"    {v:>6}  {action:<22} {sorted(hp)}")
print(f"\n    final top 3: {sorted(hp, reverse=True)}"
      f"   (verify: {sorted(demo, reverse=True)[:3]})")

# Benchmark: heap vs sort vs nlargest, as k varies
print("\n  Benchmark: n = 500,000, varying k")
random.seed(3)
big_data = [random.randint(0, 10_000_000) for _ in range(500_000)]

print(f"    {'k':>8} {'heap O(n log k)':>17} {'sort O(n log n)':>17} "
      f"{'nlargest':>11} {'winner':>10}")
print("    " + "-" * 68)
for k in [10, 1000, 100_000]:
    start = time.perf_counter()
    r_heap = top_k_largest(big_data, k)
    t_heap = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    r_sort = sorted(big_data, reverse=True)[:k]
    t_sort = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    r_nl = heapq.nlargest(k, big_data)
    t_nl = (time.perf_counter() - start) * 1000

    assert r_heap == r_sort == r_nl, f"mismatch at k={k}"
    best = min([(t_heap, "heap"), (t_sort, "sort"), (t_nl, "nlargest")])[1]
    print(f"    {k:>8} {t_heap:>15.1f}ms {t_sort:>15.1f}ms "
          f"{t_nl:>9.1f}ms {best:>10}")

print("\n    All three returned identical results at every k.")
print("    -> The heap wins when k is SMALL relative to n.")
print("    -> As k approaches n, sorting wins -- you are paying log k ~ log n")
print("       per element plus heap overhead, so just sort.")
print("    -> In real code use heapq.nlargest: same complexity, C-optimised.")

# The streaming argument
print("\n  The argument that sorting cannot answer: STREAMS")
print("    A size-k heap needs O(k) memory regardless of stream length.")
print("    Sorting needs O(n) -- you must hold everything.")
stream_k = 5
stream_heap: List[int] = []
random.seed(11)
for _ in range(1_000_000):                       # 1M items, never stored
    v = random.randint(0, 10_000_000)
    if len(stream_heap) < stream_k:
        heapq.heappush(stream_heap, v)
    elif v > stream_heap[0]:
        heapq.heappushpop(stream_heap, v)
print(f"    Processed 1,000,000 streamed items holding only {stream_k} at a time")
print(f"    Top {stream_k}: {sorted(stream_heap, reverse=True)}")

# ==================== (7) Pattern: Two Heaps (Median) ====================
print("\n[7] Pattern: Two Heaps -- Running Median")
print("-" * 70)

class MedianFinder:
    """
    low  = max-heap (negated) holding the smaller half
    high = min-heap holding the larger half
    Invariant: len(low) == len(high) or len(low) == len(high) + 1
    """

    def __init__(self):
        self.low: List[int] = []        # max-heap via negation
        self.high: List[int] = []       # min-heap

    def add(self, num: int) -> None:
        """O(log n)"""
        heapq.heappush(self.low, -num)
        # Move the largest of `low` into `high` -- guarantees correct placement
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # Rebalance so low is never smaller than high
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self) -> float:
        """O(1)"""
        if not self.low:
            raise ValueError("no elements yet")
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2

    def state(self) -> str:
        return (f"low(max)={sorted((-x for x in self.low), reverse=True)} "
                f"high(min)={sorted(self.high)}")


mf = MedianFinder()
stream = [5, 15, 1, 3, 8, 7, 9, 2]
print(f"  {'add':>5}  {'median':>7}  state")
print("  " + "-" * 58)
for v in stream:
    mf.add(v)
    print(f"  {v:>5}  {mf.median():>7.1f}  {mf.state()}")

# Verify against brute force
print("\n  Verifying against a full sort at every step:")
random.seed(21)
mf2 = MedianFinder()
seen: List[int] = []
errors = 0
for _ in range(2000):
    v = random.randint(0, 10_000)
    mf2.add(v)
    seen.append(v)
    s = sorted(seen)
    n = len(s)
    expected = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    if abs(mf2.median() - expected) > 1e-9:
        errors += 1
print(f"    2,000 insertions, mismatches vs sorted(): {errors}  "
      f"({'PASS' if not errors else 'FAIL'})")

# Cost comparison
print("\n  Cost of maintaining a median over 20,000 insertions:")
random.seed(31)
vals = [random.randint(0, 100_000) for _ in range(20_000)]

start = time.perf_counter()
mf3 = MedianFinder()
for v in vals:
    mf3.add(v)
    mf3.median()
two_heap_ms = (time.perf_counter() - start) * 1000

SAMPLE = 300
start = time.perf_counter()
acc: List[int] = []
for v in vals[:SAMPLE]:
    acc.append(v)
    s = sorted(acc)
    n = len(s)
    _ = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
resort_ms = (time.perf_counter() - start) * 1000
resort_projected = resort_ms / SAMPLE * len(vals)

start = time.perf_counter()
import bisect
acc2: List[int] = []
for v in vals:
    bisect.insort(acc2, v)
    n = len(acc2)
    _ = acc2[n // 2] if n % 2 else (acc2[n // 2 - 1] + acc2[n // 2]) / 2
insort_ms = (time.perf_counter() - start) * 1000

print(f"    Two heaps                : {two_heap_ms:>9.1f}ms   O(log n) add")
print(f"    bisect.insort + index    : {insort_ms:>9.1f}ms   O(n) add (C memmove)")
print(f"    Re-sort each time ({SAMPLE} samp.): {resort_ms:>9.1f}ms")
print(f"    Re-sort (projected 20k)  : {resort_projected:>9.1f}ms   O(n log n) add")
print(f"\n    Two heaps vs re-sorting  : ~{resort_projected / two_heap_ms:.0f}x faster")
if insort_ms < two_heap_ms:
    print(f"    bisect.insort is {two_heap_ms / insort_ms:.1f}x FASTER than two heaps here --")
    print(f"      its O(n) insert is a single C memmove, which beats two")
    print(f"      interpreted heap operations at n = 20,000. The heap wins")
    print(f"      asymptotically; in CPython the crossover is further out.")
else:
    print(f"    Two heaps vs bisect.insort: {insort_ms / two_heap_ms:.1f}x faster")

# ==================== (8) Pattern: K-Way Merge ====================
print("\n[8] Pattern: K-Way Merge")
print("-" * 70)

def merge_k_sorted(lists: List[List[int]]) -> List[int]:
    """Merge k sorted lists. O(N log k) where N = total elements."""
    heap: List[Tuple[int, int, int]] = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))     # (value, list idx, pos)

    out: List[int] = []
    while heap:
        value, li, pos = heapq.heappop(heap)
        out.append(value)
        if pos + 1 < len(lists[li]):
            heapq.heappush(heap, (lists[li][pos + 1], li, pos + 1))
    return out


lists = [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
print(f"  Input lists ({len(lists)} sorted lists):")
for i, l in enumerate(lists):
    print(f"    {i}: {l}")
merged = merge_k_sorted(lists)
print(f"\n  merged: {merged}")
print(f"  correct: {merged == sorted(sum(lists, []))}")
print(f"  heap never held more than {len(lists)} items (one per list)")

# Benchmark against concat+sort
print("\n  Benchmark: 500 sorted lists, 200 items each (100,000 total)")
random.seed(41)
many = [sorted(random.randint(0, 1_000_000) for _ in range(200))
        for _ in range(500)]

start = time.perf_counter()
r1 = merge_k_sorted(many)
heap_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
flat: List[int] = []
for l in many:
    flat.extend(l)
r2 = sorted(flat)
sort_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
r3 = list(heapq.merge(*many))
hqmerge_ms = (time.perf_counter() - start) * 1000

print(f"    {'Approach':<28} {'Time':>11}  Complexity")
print("    " + "-" * 56)
print(f"    {'Manual heap merge':<28} {heap_ms:>9.1f}ms  O(N log k)")
print(f"    {'heapq.merge (C-assisted)':<28} {hqmerge_ms:>9.1f}ms  O(N log k), lazy")
print(f"    {'concat + Timsort':<28} {sort_ms:>9.1f}ms  O(N log N)")
print(f"\n    All identical: {r1 == r2 == r3}")
if sort_ms < heap_ms:
    print(f"    concat+sort is {heap_ms / sort_ms:.1f}x faster in wall clock!")
    print(f"      Timsort DETECTS the sorted runs and merges them in C. Our")
    print(f"      pure-Python heap cannot compete on constant factor.")
print(f"    -> The heap's real advantage is STREAMING: heapq.merge is lazy")
print(f"       and holds only k items, so it merges files larger than RAM.")
print(f"       That is external merge sort, and sorting cannot do it.")

# ==================== (9) Pattern: Scheduling ====================
print("\n[9] Pattern: Scheduling -- a Heap Keyed by Time")
print("-" * 70)

def min_meeting_rooms(intervals: List[Tuple[int, int]]) -> int:
    """Fewest rooms needed. O(n log n)"""
    if not intervals:
        return 0
    intervals = sorted(intervals, key=lambda x: x[0])
    rooms: List[int] = []                      # min-heap of end times

    for start, end in intervals:
        if rooms and rooms[0] <= start:        # earliest-freeing room is free
            heapq.heapreplace(rooms, end)
        else:
            heapq.heappush(rooms, end)
    return len(rooms)


def min_meeting_rooms_sweep(intervals: List[Tuple[int, int]]) -> int:
    """Sweep-line alternative. Also O(n log n), no heap."""
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()
    cur = best = 0
    for _, delta in events:
        cur += delta
        best = max(best, cur)
    return best


meetings = [(0, 30), (5, 10), (15, 20), (25, 35), (30, 40)]
print(f"  Meetings: {meetings}")
print(f"  Rooms needed (heap)  : {min_meeting_rooms(meetings)}")
print(f"  Rooms needed (sweep) : {min_meeting_rooms_sweep(meetings)}")

# Show the heap state
print("\n  Heap of end times as each meeting is placed:")
rooms: List[int] = []
for s, e in sorted(meetings):
    if rooms and rooms[0] <= s:
        freed = heapq.heapreplace(rooms, e)
        note = f"reuse room freed at {freed}"
    else:
        heapq.heappush(rooms, e)
        note = "open a NEW room"
    print(f"    ({s:>2},{e:>2})  {note:<24} end times: {sorted(rooms)}")

# Cross-verify on random input
random.seed(51)
mismatch = 0
for _ in range(500):
    iv = []
    for _ in range(random.randint(1, 25)):
        a = random.randint(0, 50)
        iv.append((a, a + random.randint(1, 20)))
    if min_meeting_rooms(iv) != min_meeting_rooms_sweep(iv):
        mismatch += 1
print(f"\n  500 random inputs, heap vs sweep mismatches: {mismatch}  "
      f"({'PASS' if not mismatch else 'FAIL'})")

# Task scheduler simulation
print("\n  Event simulation -- 'what happens next?' is just a pop:")

def simulate_cpu(tasks: List[Tuple[str, int, int]]) -> List[Tuple[int, str]]:
    """
    tasks: (name, arrival, duration). Shortest-job-first among the arrived.
    Returns the completion timeline.
    """
    pending = sorted(tasks, key=lambda t: t[1])
    ready: List[Tuple[int, int, str]] = []      # (duration, arrival, name)
    counter = itertools.count()
    now = 0
    timeline = []
    i = 0

    while i < len(pending) or ready:
        # Admit everything that has arrived by `now`
        while i < len(pending) and pending[i][1] <= now:
            name, arrival, dur = pending[i]
            heapq.heappush(ready, (dur, next(counter), name))
            i += 1
        if not ready:
            now = pending[i][1]                 # idle: jump to next arrival
            continue
        dur, _, name = heapq.heappop(ready)     # shortest job available
        now += dur
        timeline.append((now, name))
    return timeline


tasks = [("compile", 0, 5), ("lint", 1, 1), ("test", 2, 4),
         ("deploy", 3, 2), ("notify", 10, 1)]
print(f"    Tasks (name, arrival, duration): {tasks}")
print(f"\n    {'Finished at':>12}  Task")
print("    " + "-" * 28)
for t, name in simulate_cpu(tasks):
    print(f"    {t:>12}  {name}")
print("\n    -> The heap always surfaces the shortest READY job. Same shape")
print("       as Dijkstra: 'always process the cheapest option next.'")

# ==================== (10) The Limitation: No Search ====================
print("\n[10] The Limitation: A Heap Cannot Search")
print("-" * 70)

h = list(range(1000))
random.seed(61)
random.shuffle(h)
heapq.heapify(h)

target = 500
start = time.perf_counter()
found = target in h                     # O(n) linear scan
scan_us = (time.perf_counter() - start) * 1e6

print(f"  Finding an arbitrary value in a 1,000-element heap:")
print(f"    `500 in heap` -> {found}, took {scan_us:.1f}us via a LINEAR SCAN")
print(f"    There is no structure to exploit: only heap[0] is positioned.")
print(f"    Deleting an arbitrary item is O(n) too -- you must find it first.")

print("\n  The practical fix: LAZY DELETION")

class LazyHeap:
    """
    A heap supporting O(log n) amortised removal of arbitrary items,
    by marking them dead and skipping them on pop.
    This is exactly how real Dijkstra implementations handle decrease-key.
    """

    def __init__(self):
        self.heap: List[int] = []
        self.dead: dict = {}            # value -> pending deletion count
        self.live = 0

    def push(self, v: int) -> None:
        heapq.heappush(self.heap, v)
        self.live += 1

    def remove(self, v: int) -> None:
        """Mark dead. O(1) -- the cost is deferred to pop."""
        self.dead[v] = self.dead.get(v, 0) + 1
        self.live -= 1

    def _purge(self) -> None:
        while self.heap and self.dead.get(self.heap[0], 0):
            self.dead[self.heap[0]] -= 1
            if not self.dead[self.heap[0]]:
                del self.dead[self.heap[0]]
            heapq.heappop(self.heap)

    def peek(self) -> int:
        self._purge()
        return self.heap[0]

    def pop(self) -> int:
        self._purge()
        self.live -= 1
        return heapq.heappop(self.heap)

    def __len__(self) -> int:
        return self.live


lz = LazyHeap()
for v in [5, 1, 8, 3, 9, 2]:
    lz.push(v)
print(f"    pushed 5,1,8,3,9,2  -> min = {lz.peek()}, len = {len(lz)}")
lz.remove(1)
print(f"    remove(1)           -> min = {lz.peek()}, len = {len(lz)}")
lz.remove(2)
print(f"    remove(2)           -> min = {lz.peek()}, len = {len(lz)}")
print(f"    drain               -> {[lz.pop() for _ in range(len(lz))]}")
print("\n    -> Deletions are O(1); the cost is paid lazily on pop.")
print("       Each item is purged at most once, so it stays amortised O(log n).")

print("\n  When you need BOTH min-extraction and arbitrary deletion often,")
print("  a balanced BST (Topic 17) gives you both in O(log n) honestly.")

# ==================== (11) Verification Suite ====================
print("\n[11] Verification Against Brute Force")
print("-" * 70)

random.seed(2024)
checks = {}

# MinHeap invariant + sorted drain
fails = 0
for _ in range(300):
    arr = [random.randint(-500, 500) for _ in range(random.randint(0, 40))]
    mh = MinHeap(arr)
    if not mh.is_valid() or mh.sorted_drain() != sorted(arr):
        fails += 1
checks["MinHeap heapify + drain"] = fails

# push/pop interleaved against a sorted list model
fails = 0
for _ in range(300):
    mh = MinHeap()
    model: List[int] = []
    for _ in range(60):
        if not model or random.random() < 0.6:
            v = random.randint(-100, 100)
            mh.push(v)
            bisect.insort(model, v)
        else:
            if mh.pop() != model.pop(0):
                fails += 1
                break
    if not mh.is_valid():
        fails += 1
checks["Interleaved push/pop"] = fails

# pushpop matches heapq.heappushpop
fails = 0
for _ in range(300):
    arr = [random.randint(0, 100) for _ in range(random.randint(1, 20))]
    v = random.randint(0, 100)
    mine = MinHeap(arr)
    r1 = mine.pushpop(v)
    ref = list(arr)
    heapq.heapify(ref)
    r2 = heapq.heappushpop(ref, v)
    if r1 != r2 or sorted(mine.data) != sorted(ref):
        fails += 1
checks["pushpop vs heapq"] = fails

# top-K
fails = 0
for _ in range(300):
    arr = [random.randint(-1000, 1000) for _ in range(random.randint(1, 60))]
    k = random.randint(1, len(arr))
    if top_k_largest(arr, k) != sorted(arr, reverse=True)[:k]:
        fails += 1
checks["top_k_largest"] = fails

# k-way merge
fails = 0
for _ in range(200):
    ls = [sorted(random.randint(0, 100) for _ in range(random.randint(0, 15)))
          for _ in range(random.randint(1, 8))]
    if merge_k_sorted(ls) != sorted(sum(ls, [])):
        fails += 1
checks["merge_k_sorted"] = fails

# meeting rooms
fails = 0
for _ in range(300):
    iv = []
    for _ in range(random.randint(0, 20)):
        a = random.randint(0, 40)
        iv.append((a, a + random.randint(1, 15)))
    if min_meeting_rooms(iv) != min_meeting_rooms_sweep(iv):
        fails += 1
checks["min_meeting_rooms"] = fails

print(f"  {'Check':<30} {'Failures':>10}  Verdict")
print("  " + "-" * 52)
for name, f in checks.items():
    print(f"  {name:<30} {f:>10}  {'PASS' if f == 0 else 'FAIL'}")

print("\n-> Every implementation cross-checked against a brute-force model")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
