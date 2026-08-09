"""
Exercises: Heaps & Priority Queues

Practice heap internals, top-K, two-heap tricks, k-way merge, and scheduling.
"""

from typing import List, Tuple, Any

print("=" * 70)
print("EXERCISES: Heaps & Priority Queues")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. HEAP INDEX ARITHMETIC")
print("Input: An index i in a 0-indexed heap array")
print("Output: Its parent and children indices")
print("Example: i=4 -> parent 1, children 9 and 10")
def parent_index(i: int) -> int:
    # TODO: (i - 1) // 2. Return -1 for the root (i == 0).
    pass

def child_indices(i: int) -> Tuple[int, int]:
    # TODO: (2i + 1, 2i + 2). No bounds checking here -- the caller
    # compares against len(heap).
    pass

print("\n2. SIFT UP")
print("Input: A heap array with heap[i] possibly too small for its position")
print("Output: The array repaired by bubbling heap[i] toward the root")
print("Example: [1,3,5,7,0] with i=4 -> [0,1,5,7,3]")
def sift_up(heap: List[int], i: int) -> None:
    # TODO: While i > 0 and heap[i] < heap[parent]: swap and move up.
    # Stop as soon as the parent is smaller -- everything above is already fine.
    pass

print("\n3. SIFT DOWN")
print("Input: A heap array with heap[i] possibly too large for its position")
print("Output: The array repaired by pushing heap[i] toward the leaves")
print("Example: [9,1,5,7,3] with i=0 -> [1,3,5,7,9]")
def sift_down(heap: List[int], i: int, n: int) -> None:
    # TODO: Find the SMALLEST of {heap[i], left child, right child}.
    # If it is not i, swap and continue from there. Must compare BOTH
    # children -- picking the left one blindly is the classic bug.
    pass

print("\n4. HEAP PUSH AND POP")
print("Input: A valid heap")
print("Output: push adds a value; pop removes and returns the minimum")
print("Example: pop must keep the tree COMPLETE, not leave a hole")
def heap_push(heap: List[int], value: int) -> None:
    # TODO: Append to the end, then sift_up from the last index.
    pass

def heap_pop(heap: List[int]) -> int:
    # TODO: Swap heap[0] with heap[-1], pop the last element, then
    # sift_down from index 0. Do NOT del heap[0] -- that is O(n) and
    # breaks completeness.
    pass

print("\n5. BUILD A HEAP IN O(n)")
print("Input: An arbitrary list")
print("Output: The same list rearranged into a valid min-heap")
print("Example: n pushes is O(n log n); this must be O(n)")
def heapify(arr: List[int]) -> None:
    # TODO: Sift down from the LAST PARENT (n//2 - 1) back to index 0.
    # Leaves need no work -- that is why this is O(n), not O(n log n).
    # Be ready to explain the series argument.
    pass

print("\n6. VALIDATE A HEAP")
print("Input: A list")
print("Output: True if it satisfies the min-heap property everywhere")
print("Example: [1,3,5,7,9] -> True; [1,3,5,0] -> False")
def is_min_heap(arr: List[int]) -> bool:
    # TODO: For every i, both existing children must be >= arr[i].
    # You only need to check parents: range(len(arr) // 2).
    pass

print("\n7. HEAP SORT")
print("Input: A list")
print("Output: A sorted list, using only heap operations")
print("Example: heapify then pop n times")
def heap_sort(arr: List[int]) -> List[int]:
    # TODO: heapify, then repeatedly pop. O(n log n) overall.
    # Bonus: do it IN PLACE with a max-heap, swapping the root to the
    # end and shrinking -- that is the O(1)-space version from Topic 13.
    pass


# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n8. KTH LARGEST ELEMENT")
print("Input: An array and k")
print("Output: The kth largest element")
print("Example: [3,2,1,5,6,4], k=2 -> 5")
def kth_largest(nums: List[int], k: int) -> int:
    # TODO: THE KEY INVERSION -- use a MIN-heap of size k, not a max-heap.
    # Push each element; whenever the heap exceeds k, pop the minimum.
    # The root is then the kth largest. O(n log k) time, O(k) space.
    # Say the inversion out loud in an interview; it is the tell that you
    # understand the pattern rather than reciting it.
    pass

print("\n9. TOP K FREQUENT ELEMENTS")
print("Input: An array and k")
print("Output: The k most frequent values")
print("Example: [1,1,1,2,2,3], k=2 -> [1, 2]")
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    # TODO: Count with a Counter, then run the size-k min-heap pattern
    # keyed on COUNT. Note there is also an O(n) bucket-sort solution --
    # mention it as the follow-up.
    pass

print("\n10. K CLOSEST POINTS TO THE ORIGIN")
print("Input: A list of (x, y) points and k")
print("Output: The k points nearest the origin")
print("Example: [(1,3),(-2,2)], k=1 -> [(-2,2)]")
def k_closest(points: List[Tuple[int, int]], k: int) -> List[Tuple[int, int]]:
    # TODO: Size-k MAX-heap keyed on squared distance (negate for heapq).
    # Here you want the FARTHEST keeper cheaply available so you can evict
    # it -- the mirror image of problem 8. Do not take square roots;
    # squared distance preserves ordering and avoids float error.
    pass

print("\n11. MERGE K SORTED LISTS")
print("Input: A list of sorted lists")
print("Output: One merged sorted list")
print("Example: [[1,4],[2,5],[3,6]] -> [1,2,3,4,5,6]")
def merge_k_sorted(lists: List[List[int]]) -> List[int]:
    # TODO: Seed the heap with the FIRST element of each list as
    # (value, list_index, position). Pop the min, append it, then push
    # that list's next element. O(N log k), and the heap never holds
    # more than k items.
    pass

print("\n12. LAST STONE WEIGHT")
print("Input: Stone weights")
print("Output: The weight of the last remaining stone (0 if none)")
print("Example: [2,7,4,1,8,1] -> 1")
def last_stone_weight(stones: List[int]) -> int:
    # TODO: Repeatedly smash the two HEAVIEST stones together; the
    # difference goes back in. A max-heap (negate) makes each round O(log n).
    pass

print("\n13. MEETING ROOMS II")
print("Input: Meeting intervals (start, end)")
print("Output: The minimum number of rooms required")
print("Example: [(0,30),(5,10),(15,20)] -> 2")
def min_meeting_rooms(intervals: List[Tuple[int, int]]) -> int:
    # TODO: Sort by start. Keep a min-heap of END times -- one entry per
    # occupied room. If the earliest-freeing room is free by this start,
    # reuse it (heapreplace); otherwise open a new one. The answer is the
    # final heap size.
    # There is also a sweep-line solution with no heap; know both.
    pass

print("\n14. TASK SCHEDULER WITH COOLDOWN")
print("Input: Task labels and a cooldown n between identical tasks")
print("Output: The minimum total time slots needed")
print("Example: ['A','A','A','B','B','B'], n=2 -> 8")
def least_interval(tasks: List[str], n: int) -> int:
    # TODO: Greedily run the most frequent available task each round --
    # a max-heap on remaining counts. Tasks in cooldown wait in a queue
    # of (ready_time, count) and return to the heap when eligible.
    # There is also a closed-form math solution; the heap version
    # generalises better.
    pass


# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n15. FIND MEDIAN FROM A DATA STREAM")
print("Input: A stream of numbers, interleaved with median queries")
print("Output: The running median after each insertion")
print("Example: add 1, add 2 -> 1.5; add 3 -> 2")
class MedianFinder:
    def __init__(self):
        # TODO: TWO heaps. `low` is a MAX-heap (negate) for the smaller
        # half; `high` is a MIN-heap for the larger half.
        # Invariant: len(low) == len(high), or len(low) == len(high) + 1.
        pass

    def add_num(self, num: int) -> None:
        # TODO: The reliable dance -- push onto `low`, immediately move
        # low's max over to `high`, then rebalance if `high` got bigger.
        # This places the element correctly with no comparisons at all.
        pass

    def find_median(self) -> float:
        # TODO: O(1). If the halves are unequal, the median is low's top;
        # otherwise average the two tops.
        pass

print("\n16. SLIDING WINDOW MEDIAN")
print("Input: An array and a window size k")
print("Output: The median of every window")
print("Example: [1,3,-1,-3,5,3,6,7], k=3 -> [1,-1,-1,3,5,6]")
def sliding_window_median(nums: List[int], k: int) -> List[float]:
    # TODO: Two heaps PLUS removal, which heaps do not support directly.
    # Use LAZY DELETION: keep a dict of pending removals, and purge the
    # tops before reading them. Track the live sizes yourself, since the
    # raw heap lengths now include dead entries.
    # This is the problem that forces you to confront the heap's real
    # limitation. A balanced BST or SortedList is arguably the better tool.
    pass

print("\n17. SMALLEST RANGE COVERING ELEMENTS FROM K LISTS")
print("Input: k sorted lists")
print("Output: The smallest range [a,b] containing at least one element")
print("        from every list")
print("Example: [[4,10,15],[0,9,12],[5,18,22]] -> [9, 12]")
def smallest_range(lists: List[List[int]]) -> Tuple[int, int]:
    # TODO: Keep one pointer per list in a min-heap. The current range is
    # [heap_min, max_seen]. Advance the list owning the MINIMUM -- it is
    # the only move that can shrink the range. Stop when any list is
    # exhausted. Same skeleton as k-way merge, different bookkeeping.
    pass

print("\n18. REORGANIZE STRING (NO TWO ADJACENT EQUAL)")
print("Input: A string")
print("Output: A rearrangement with no two adjacent characters equal,")
print("        or '' if impossible")
print("Example: 'aab' -> 'aba'; 'aaab' -> ''")
def reorganize_string(s: str) -> str:
    # TODO: Max-heap on character counts. Repeatedly take the TWO most
    # frequent remaining characters and append both -- that guarantees
    # they cannot collide. Impossible exactly when one count exceeds
    # (len(s) + 1) // 2; you can detect that upfront or let the loop fail.
    pass

print("\n19. IPO / MAXIMIZE CAPITAL")
print("Input: k projects to pick, starting capital w, and per-project")
print("       (capital_required, profit)")
print("Output: The maximum final capital")
print("Example: two heaps -- one gating by cost, one choosing by profit")
def find_maximized_capital(k: int, w: int, capital: List[int],
                           profits: List[int]) -> int:
    # TODO: A MIN-heap on required capital holds locked projects; a
    # MAX-heap on profit holds the affordable ones. Each round, unlock
    # everything you can now afford, then take the single most profitable.
    # Two heaps serving two different questions -- the pattern worth seeing.
    pass


# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n20. INDEXED HEAP WITH decrease_key")
print("Input: Priority updates for items already in the heap")
print("Output: O(log n) priority changes, not O(n)")
print("Example: what a textbook Dijkstra actually assumes exists")
class IndexedHeap:
    def __init__(self):
        # TODO: A heap array PLUS a dict mapping item -> its current index.
        # Every swap in sift_up/sift_down must update that dict, or the
        # whole thing silently corrupts.
        pass

    def push(self, item: Any, priority: int) -> None:
        # TODO: Standard push, plus register the final index.
        pass

    def decrease_key(self, item: Any, new_priority: int) -> None:
        # TODO: Look up the index in O(1), lower the priority, sift UP.
        # This is what `heapq` cannot do, and why real Dijkstra
        # implementations push duplicates and discard stale entries instead.
        pass

    def pop(self) -> Tuple[Any, int]:
        # TODO: Standard pop, keeping the index map consistent.
        pass

print("\n21. K-WAY EXTERNAL MERGE (STREAMING)")
print("Input: Several sorted iterators too large to hold in memory")
print("Output: A single sorted iterator, holding only k items at a time")
print("Example: this is how external merge sort works")
def external_merge(iterators: List[Any]):
    # TODO: A GENERATOR, not a list -- that is the whole point. Seed the
    # heap with one item per iterator, then yield the min and pull the
    # next item from that same iterator.
    # Compare with heapq.merge, which does exactly this. Then explain why
    # sorting cannot solve this problem at all.
    pass

print("\n22. TOP K FREQUENT WORDS IN A STREAM")
print("Input: A stream of words and k")
print("Output: The current top k, queryable at any time")
print("Example: counts change as the stream advances")
class StreamingTopK:
    def __init__(self, k: int):
        # TODO: A count dict plus a size-k heap. The subtlety: when a
        # word's count RISES, any stale heap entry for it is now wrong.
        # Options: lazy invalidation (store the count in the entry and
        # discard mismatches), or an indexed heap from problem 20.
        # State which trade-off you chose and why.
        pass

    def add(self, word: str) -> None:
        pass

    def top(self) -> List[Tuple[str, int]]:
        pass

print("\n23. MINIMUM COST TO CONNECT STICKS")
print("Input: Stick lengths")
print("Output: The minimum total cost, where joining two sticks costs")
print("        their combined length")
print("Example: [2,4,3] -> 14")
def connect_sticks(sticks: List[int]) -> int:
    # TODO: Always join the two SHORTEST sticks. If this feels familiar,
    # it should -- it is Huffman coding from Topic 15 with the tree
    # thrown away. Recognising the isomorphism is the exercise.
    pass

print("\n24. SLIDING WINDOW MAXIMUM -- HEAP vs MONOTONIC DEQUE")
print("Input: An array and a window size k")
print("Output: The maximum of every window")
print("Example: [1,3,-1,-3,5,3,6,7], k=3 -> [3,3,5,5,6,7]")
def max_sliding_window_heap(nums: List[int], k: int) -> List[int]:
    # TODO: Max-heap with lazy deletion -- store (value, index) and discard
    # tops whose index has fallen out of the window. O(n log n).
    pass

def max_sliding_window_deque(nums: List[int], k: int) -> List[int]:
    # TODO: Now do it in O(n) with a MONOTONIC DEQUE holding indices of a
    # decreasing sequence. Pop from the back anything smaller than the
    # incoming value; pop from the front anything out of the window.
    # Implement BOTH, then time them. The lesson: a heap is often the
    # obvious answer and occasionally the wrong one.
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Heaps & Priority Queues Cheat Sheet:

1. The One Question a Heap Answers:
   "What is the best (smallest/largest) item RIGHT NOW?" -- asked
   repeatedly, while items keep arriving and leaving.

   Not membership (use a set). Not full order (use a sort). Not ranges
   (use a balanced BST). If you pop everything out anyway, you have
   written a slower sort.

2. The Structure:
   A COMPLETE binary tree stored in a flat array.

     parent(i)      = (i - 1) // 2
     left_child(i)  = 2*i + 1
     right_child(i) = 2*i + 2

   Heap property: every parent <= both children (min-heap).
   What is NOT guaranteed: sibling order, or that the array is sorted.
   Only heap[0] is meaningful. Printing the array to "check" misleads you.

3. The Whole Implementation:
   sift_up   -- after appending, bubble toward the root
   sift_down -- after removing the root, push toward the leaves

   push : append + sift_up                       O(log n)
   pop  : swap root with last, shrink, sift_down O(log n)
   peek : heap[0]                                O(1)

   Pop must SWAP the last element in. Deleting heap[0] directly leaves a
   hole and breaks completeness.

4. heapify is O(n), Not O(n log n):
   Sift down from the last parent (n//2 - 1) to the root.

     n/2 * 0 + n/4 * 1 + n/8 * 2 + ... = n * sum(k / 2^(k+1)) = n * 1

   Half the nodes are leaves and do zero work. The series converges.
   Be ready to prove this -- it is a favourite follow-up.

5. Python's heapq:
   A MIN-heap of functions operating on a plain list. No heap object.

     heappush / heappop / heapify / heappushpop / heapreplace
     nsmallest / nlargest / merge

   Max-heap: negate going in AND coming out. Say it out loud; the
   interviewer knows it is a wart.

   heappushpop vs heapreplace -- both are ONE sift instead of two:
     heappushpop(h, x)  push then pop; if x < root, returns x unchanged
     heapreplace(h, x)  pop then push; always evicts the old root

   For top-K, heappushpop is the right one -- it rejects non-qualifiers.

6. THE Tuple Tie-Break Bug:
   (priority, obj) raises TypeError when priorities tie and obj has no
   __lt__. It only fails ON A TIE -- passes your tests, breaks in
   production. Fix with a monotonic counter:

     heappush(h, (priority, next(counter), obj))

   This also makes the queue stable (FIFO within equal priorities).

7. Pattern -- Top K (the inversion that matters):

   K LARGEST  -> MIN-heap of size k   (evict the weakest keeper)
   K SMALLEST -> MAX-heap of size k   (evict the strongest keeper)

   Getting this backwards is the most common heap mistake by a wide margin.

   Approach            Time        Space   Use when
   ─────────────────────────────────────────────────────────────
   sort, take k        O(n log n)  O(n)    k close to n; need sorted
   size-k heap         O(n log k)  O(k)    k << n, or STREAMING
   quickselect         O(n) avg    O(1)    one-shot kth, in memory
   heapq.nlargest      O(n log k)  O(k)    real Python code

   The heap's unbeatable case is STREAMING: O(k) memory regardless of
   stream length. You cannot sort what you cannot hold.

8. Pattern -- Two Heaps (running median):
   low  = max-heap of the smaller half
   high = min-heap of the larger half
   Keep sizes within 1; the median sits on top. O(log n) add, O(1) read.

   The reliable insertion dance: push onto low, move low's max to high,
   then rebalance if high overgrew. No comparisons needed.

9. Pattern -- K-Way Merge:
   Heap of (value, source_index, position), one entry per source.
   O(N log k) instead of O(N log N) for concat-and-sort, and it STREAMS --
   which is what makes external merge sort possible.

10. Pattern -- Scheduling (a heap keyed by TIME):
    The root answers "what happens next?" Meeting rooms, CPU scheduling,
    event simulation, task cooldown all share this shape.

11. Heaps You Already Used:
    Topic 13  Heap Sort      heapify + n pops, O(1) extra space
    Topic 14  Dijkstra       always expand the nearest vertex
    Topic 14  Prim's MST     always take the cheapest edge
    Topic 15  Huffman        always merge the two smallest frequencies

    The shared phrase is "ALWAYS TAKE THE SMALLEST X NEXT." That sentence
    is the heap's signature -- when you hear it, reach for a heap.

12. THE Limitation -- A Heap Cannot Search:
    Finding an arbitrary item is O(n). Deleting one is O(n). There is no
    decrease_key in heapq.

    Fixes, in order of practicality:
      LAZY DELETION   mark dead in a dict, purge on pop (most common)
      indexed heap    dict of item -> index, maintained on every swap
      balanced BST    gives min-extraction AND deletion honestly

    Real Dijkstra implementations push duplicate entries and skip stale
    ones. That IS lazy deletion.

Complexity Reference:

Operation              Time        Note
──────────────────────────────────────────────────────────────
peek min               O(1)        heap[0]
push                   O(log n)    append + sift up
pop min                O(log n)    swap + shrink + sift down
heappushpop            O(log n)    one sift, not two
build via n pushes     O(n log n)  the naive way
build via heapify      O(n)        sift down from last parent
heap sort              O(n log n)  O(1) extra space
find arbitrary item    O(n)        NO search structure
delete arbitrary item  O(n)        must find it first
merge two heaps        O(n)        re-heapify
top-K                  O(n log k)  size-k heap
k-way merge            O(N log k)  size-k heap

Space: O(n) for the heap, O(1) auxiliary.

Problem Recognition Guide:

"kth largest / smallest"              -> size-k heap (mind the inversion)
"top k frequent"                      -> count, then size-k heap
"k closest / nearest"                 -> size-k max-heap on distance
"running / streaming median"          -> two heaps
"merge k sorted things"               -> heap of size k
"minimum rooms / machines / CPUs"     -> heap of end times
"always process the cheapest next"    -> heap (Dijkstra shape)
"repeatedly combine the two smallest" -> heap (Huffman shape)
"sliding window maximum"              -> monotonic deque BEATS the heap
"kth element, one shot, in memory"    -> quickselect beats the heap
"need min AND arbitrary delete"       -> balanced BST, or lazy deletion

Common Pitfalls:

1. Max-heap for top-K largest. It is a MIN-heap of size k.
2. Forgetting heapq is min-only; or negating on the way in but not out.
3. The (priority, object) TypeError on ties. Add a counter.
4. Assuming the heap array is sorted. Only heap[0] is positioned.
5. Popping from an empty heap -- IndexError. Guard with `while heap:`.
6. n pushes instead of heapify: O(n log n) for an O(n) job.
7. Comparing only the left child in sift_down.
8. Trying to update a priority in place. There is no decrease_key.
9. Reaching for a heap when a monotonic deque is O(n) (window maximum)
   or quickselect is O(n) (one-shot kth).

Interview Tips:

1. State the min-heap-for-max-K inversion explicitly and explain WHY:
   you need the weakest survivor cheaply so you can evict it.
2. Prove heapify is O(n) with the series argument, not hand-waving.
3. Compare against BOTH sorting and quickselect, and say when each wins.
4. Bring up the tuple tie-break bug unprompted. It reads as scar tissue
   from real work, which is exactly the signal you want to send.
5. Name the limitation (no search, no decrease_key) before you are asked,
   then offer lazy deletion as the fix.
6. Mention heapq.nlargest / heapq.merge for production code. Knowing the
   stdlib is part of the job.

Learning Progression:

1. Basic: index arithmetic, sift up/down, push/pop, heapify
2. Intermediate: top-K and its inversion, k-way merge, meeting rooms
3. Advanced: two-heap median, lazy deletion, sliding window median
4. Expert: indexed heaps with decrease_key, streaming merges, and knowing
   when a deque or quickselect beats a heap outright

Next: implement each stub, then run project.py to see heaps running a
task queue, a rate limiter, an event simulator, and a log merger.
""")
