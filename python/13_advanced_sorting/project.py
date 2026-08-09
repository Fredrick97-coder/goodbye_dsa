"""
Project: Advanced Sorting in the Real World

Build practical systems using sorting:
1. Leaderboard System (Quick Sort)
2. Data Analytics (Merge Sort)
3. Event Scheduling (Custom Sort)
4. Search Index Building (Radix Sort)
"""

import random
import time
from typing import List, Tuple
from dataclasses import dataclass

print("=" * 70)
print("PROJECT: Advanced Sorting Applications")
print("=" * 70)

# ==================== PART 1: Leaderboard System ====================
print("\n[PART 1] Leaderboard System (Quick Sort)")
print("-" * 70)

@dataclass
class Player:
    name: str
    score: int
    level: int

    def __repr__(self):
        return f"{self.name}(score={self.score}, level={self.level})"

class Leaderboard:
    """Game leaderboard with dynamic ranking"""

    def __init__(self):
        self.players = []

    def add_player(self, name: str, score: int, level: int):
        """Add or update player"""
        for p in self.players:
            if p.name == name:
                p.score = max(p.score, score)
                p.level = max(p.level, level)
                return
        self.players.append(Player(name, score, level))

    def quick_sort_by_score(self, low: int = 0, high: int = None):
        """Sort players by score (descending) using quick sort"""
        if high is None:
            high = len(self.players) - 1

        if low < high:
            pivot_idx = self.partition(low, high)
            self.quick_sort_by_score(low, pivot_idx - 1)
            self.quick_sort_by_score(pivot_idx + 1, high)

    def partition(self, low: int, high: int) -> int:
        """Partition by score (descending)"""
        pivot = self.players[high].score
        i = low - 1

        for j in range(low, high):
            if self.players[j].score > pivot:  # Descending
                i += 1
                self.players[i], self.players[j] = self.players[j], self.players[i]

        self.players[i + 1], self.players[high] = (
            self.players[high],
            self.players[i + 1],
        )
        return i + 1

    def get_ranking(self) -> List[Tuple[int, Player]]:
        """Get ranked list (1st place, 2nd place, ...)"""
        self.quick_sort_by_score()
        return [(i + 1, p) for i, p in enumerate(self.players)]

# Test leaderboard
print("Leaderboard Demo:\n")
board = Leaderboard()

players_data = [
    ("Alice", 1500, 10),
    ("Bob", 2300, 15),
    ("Charlie", 1800, 12),
    ("Diana", 2100, 14),
    ("Eve", 2300, 16),  # Tie with Bob
]

for name, score, level in players_data:
    board.add_player(name, score, level)

ranking = board.get_ranking()
print("Current Leaderboard:\n")
for rank, player in ranking[:5]:
    print(f"  #{rank}. {player.name:<10} Score: {player.score:>5} Level: {player.level}")

print("→ Time: O(n log n) average, O(1) space in-place")
print("→ Dynamic updates as players earn points")

# ==================== PART 2: Data Analytics (Merge Sort) ====================
print("\n[PART 2] Data Analytics (Merge Sort - Stable)")
print("-" * 70)

@dataclass
class Transaction:
    date: str
    amount: float
    category: str

    def __repr__(self):
        return f"{self.date}:{self.category}:${self.amount:.2f}"

class DataAnalytics:
    """Analyze transaction data with stable sorting"""

    def __init__(self):
        self.transactions = []

    def add_transaction(self, date: str, amount: float, category: str):
        """Record transaction"""
        self.transactions.append(Transaction(date, amount, category))

    def merge_sort(self, key_func, reverse: bool = False) -> List[Transaction]:
        """Stable merge sort by any key"""
        if len(self.transactions) <= 1:
            return self.transactions

        def merge(left, right):
            result = []
            i = j = 0

            while i < len(left) and j < len(right):
                left_val = key_func(left[i])
                right_val = key_func(right[j])

                if (left_val <= right_val) != reverse:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

            result.extend(left[i:])
            result.extend(right[j:])
            return result

        def sort_helper(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            return merge(sort_helper(arr[:mid]), sort_helper(arr[mid:]))

        return sort_helper(self.transactions)

    def analyze_by_category_and_amount(self) -> List[Transaction]:
        """Sort by category first, then by amount (stable)"""
        # First sort by amount
        analytics = DataAnalytics()
        analytics.transactions = self.transactions.copy()
        sorted_by_amount = analytics.merge_sort(lambda t: t.amount)

        # Then sort by category (stable maintains amount order within category)
        analytics.transactions = sorted_by_amount
        return analytics.merge_sort(lambda t: t.category)

# Test analytics
print("Transaction Analysis Demo:\n")
analytics = DataAnalytics()

transactions = [
    ("2026-01-15", 120.50, "Food"),
    ("2026-01-20", 45.00, "Transport"),
    ("2026-01-10", 200.00, "Food"),
    ("2026-01-25", 80.00, "Transport"),
    ("2026-01-05", 55.00, "Food"),
]

for date, amount, category in transactions:
    analytics.add_transaction(date, amount, category)

result = analytics.analyze_by_category_and_amount()

print("Sorted by Category, then Amount (stable):\n")
for i, txn in enumerate(result):
    print(f"  {i+1}. {txn}")

print("→ Time: O(n log n), Space: O(n)")
print("→ Stable: items with same category keep amount order")

# ==================== PART 3: Event Scheduling (Custom Sort) ====================
print("\n[PART 3] Event Scheduling (Interval Sorting)")
print("-" * 70)

@dataclass
class Event:
    name: str
    start: int
    end: int
    priority: int

    def __repr__(self):
        return f"{self.name}({self.start}-{self.end}, P{self.priority})"

class EventScheduler:
    """Schedule events optimally"""

    def __init__(self):
        self.events = []

    def add_event(self, name: str, start: int, end: int, priority: int):
        """Add event with time and priority"""
        self.events.append(Event(name, start, end, priority))

    def sort_by_priority_and_start(self) -> List[Event]:
        """Sort by priority (high first), then start time"""
        # Using Python's built-in sort (Timsort, stable)
        return sorted(
            self.events, key=lambda e: (-e.priority, e.start)  # Negative for descending
        )

    def find_max_non_overlapping(self) -> List[Event]:
        """Greedy: select max non-overlapping events (sorted by end time)"""
        if not self.events:
            return []

        # Sort by end time
        sorted_events = sorted(self.events, key=lambda e: e.end)

        selected = [sorted_events[0]]

        for event in sorted_events[1:]:
            if event.start >= selected[-1].end:
                selected.append(event)

        return selected

# Test scheduler
print("Event Scheduling Demo:\n")
scheduler = EventScheduler()

events = [
    ("Meeting A", 9, 11, 3),
    ("Standup", 10, 10.5, 5),
    ("Lunch", 12, 13, 1),
    ("Meeting B", 14, 15, 2),
    ("Code Review", 11, 12, 4),
]

for name, start, end, priority in events:
    scheduler.add_event(name, start, end, priority)

print("Events sorted by Priority, then Start Time:\n")
sorted_events = scheduler.sort_by_priority_and_start()
for i, event in enumerate(sorted_events):
    print(f"  {i+1}. {event}")

print("\nNon-overlapping events (max selection):\n")
non_overlap = scheduler.find_max_non_overlapping()
for i, event in enumerate(non_overlap):
    print(f"  {i+1}. {event}")

print("→ Multi-key sort with custom comparator")
print("→ Greedy scheduling is optimal for non-overlapping selection")

# ==================== PART 4: Search Index (Radix Sort) ====================
print("\n[PART 4] Search Index (Radix Sort for IDs)")
print("-" * 70)

@dataclass
class Document:
    doc_id: int
    title: str
    relevance: int

    def __repr__(self):
        return f"Doc#{self.doc_id}: {self.title}"

class SearchIndex:
    """Index documents with fast radix-based sorting"""

    def __init__(self):
        self.documents = []

    def add_document(self, doc_id: int, title: str, relevance: int):
        """Add document to index"""
        self.documents.append(Document(doc_id, title, relevance))

    def radix_sort_by_id(self) -> List[Document]:
        """Sort documents by ID using radix sort"""
        if not self.documents:
            return []

        max_id = max(d.doc_id for d in self.documents)
        exp = 1

        while max_id // exp > 0:
            self.counting_sort_by_digit(exp)
            exp *= 10

        return self.documents

    def counting_sort_by_digit(self, exp: int):
        """Sort by single digit"""
        n = len(self.documents)
        output = [None] * n
        counts = [0] * 10

        for doc in self.documents:
            digit = (doc.doc_id // exp) % 10
            counts[digit] += 1

        for i in range(1, 10):
            counts[i] += counts[i - 1]

        for i in range(n - 1, -1, -1):
            digit = (self.documents[i].doc_id // exp) % 10
            output[counts[digit] - 1] = self.documents[i]
            counts[digit] -= 1

        self.documents = output

    def get_by_relevance(self) -> List[Document]:
        """Sort by relevance (descending) for search results"""
        return sorted(self.documents, key=lambda d: -d.relevance)

# Test search index
print("Search Index Demo:\n")
index = SearchIndex()

docs = [
    (1003, "Python Guide", 95),
    (1001, "Sorting Algorithms", 100),
    (1002, "Data Structures", 98),
    (1005, "Graph Theory", 85),
    (1004, "Dynamic Programming", 92),
]

for doc_id, title, relevance in docs:
    index.add_document(doc_id, title, relevance)

print("Indexed documents (sorted by ID via Radix):\n")
index.radix_sort_by_id()
for i, doc in enumerate(index.documents):
    print(f"  {i+1}. {doc}")

print("\nSearch results (sorted by relevance):\n")
results = index.get_by_relevance()
for i, doc in enumerate(results[:5]):
    print(f"  #{i+1} relevance. {doc}")

print("→ Time: O(d × (n + 10)) for radix, d=4 digits")
print("→ Used in databases for efficient indexing")

# ==================== PART 5: Performance Comparison ====================
print("\n[PART 5] Sorting Algorithm Performance")
print("-" * 70)

def benchmark_sorting_methods(size: int):
    """Compare different sorting algorithms on random data"""
    data = [random.randint(0, 100000) for _ in range(size)]

    times = {}

    # Quick Sort
    arr = data.copy()
    def quick_sort_impl(a, low=0, high=None):
        if high is None:
            high = len(a) - 1
        if low < high:
            pivot = a[high]
            i = low - 1
            for j in range(low, high):
                if a[j] < pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
            a[i + 1], a[high] = a[high], a[i + 1]
            quick_sort_impl(a, low, i)
            quick_sort_impl(a, i + 2, high)
        return a

    start = time.time()
    quick_sort_impl(arr)
    times["Quick Sort"] = (time.time() - start) * 1000

    # Python's built-in (Timsort)
    arr = data.copy()
    start = time.time()
    arr.sort()
    times["Timsort (built-in)"] = (time.time() - start) * 1000

    # Heap Sort
    def heap_sort_impl(a):
        n = len(a)
        for i in range(n // 2 - 1, -1, -1):
            heapify(a, i, n)
        for i in range(n - 1, 0, -1):
            a[0], a[i] = a[i], a[0]
            heapify(a, 0, i)
        return a

    def heapify(a, i, n):
        largest = i
        l, r = 2 * i + 1, 2 * i + 2
        if l < n and a[l] > a[largest]:
            largest = l
        if r < n and a[r] > a[largest]:
            largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(a, largest, n)

    arr = data.copy()
    start = time.time()
    heap_sort_impl(arr)
    times["Heap Sort"] = (time.time() - start) * 1000

    return times

print("Performance Comparison:\n")
print(f"{'Algorithm':<20} {'10K items':<15} {'50K items':<15}")
print("-" * 50)

for size in [10000, 50000]:
    times = benchmark_sorting_methods(size)
    if size == 10000:
        times_10k = times
    else:
        times_50k = times

for algo in times_10k.keys():
    print(f"{algo:<20} {times_10k[algo]:>8.2f}ms {'':<2} {times_50k[algo]:>8.2f}ms")

print("\n→ Timsort best for real-world data")
print("→ Quick Sort practical for random data")
print("→ Heap Sort consistent O(n log n)")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World Sorting Applications:

1. Leaderboard System (Quick Sort)
   - In-place sorting for game rankings
   - Dynamic updates as scores change
   - O(n log n) average performance
   - Used in: Gaming, competitions, sports

2. Data Analytics (Merge Sort)
   - Stable sorting for multi-key analysis
   - Preserve order for equal keys
   - O(n log n) guaranteed
   - Used in: Financial analysis, reporting

3. Event Scheduling (Custom Sort)
   - Multi-key sorting with priorities
   - Greedy interval scheduling
   - Optimal non-overlapping selection
   - Used in: Calendar apps, conference scheduling

4. Search Index (Radix Sort)
   - Fast integer sorting for IDs
   - O(d*(n+k)) for fixed digit count
   - Stable and predictable
   - Used in: Databases, search engines

Key Insights:

✓ Quick Sort: practical choice, in-place, cache-friendly
✓ Merge Sort: stable, guaranteed O(n log n)
✓ Heap Sort: guaranteed O(n log n), O(1) space
✓ Timsort: modern default, adaptive, fast on real data
✓ Stability matters for multi-key sorting
✓ Algorithm choice depends on data characteristics

Sorting in Production:

1. General Purpose: Python's sorted() / Timsort
2. For Stability: Merge Sort or Timsort
3. For Space: Heap Sort or Quick Sort
4. For Speed on Real Data: Quick Sort or Timsort
5. For Guaranteed Time: Merge Sort or Heap Sort

Algorithm Complexity Reference:

Algorithm       Best        Average     Worst       Space   Stable
───────────────────────────────────────────────────────────────────
Quick Sort      O(n logn)   O(n logn)   O(n²)       O(logn) No
Merge Sort      O(n logn)   O(n logn)   O(n logn)   O(n)    Yes
Heap Sort       O(n logn)   O(n logn)   O(n logn)   O(1)    No
Timsort         O(n)        O(n logn)   O(n logn)   O(n)    Yes
Counting Sort   O(n+k)      O(n+k)      O(n+k)      O(k)    Yes
Radix Sort      O(d*n)      O(d*n)      O(d*n)      O(n)    Yes

When to Optimize:

1. Profile first (use actual data)
2. Consider data characteristics:
   - Nearly sorted? (Timsort wins)
   - Random? (Quick Sort good)
   - Fixed range? (Radix/Counting Sort)
   - Huge dataset? (Merge Sort or Timsort)

3. Consider constraints:
   - Space critical? (Heap Sort)
   - Stability needed? (Merge Sort)
   - Guaranteed time? (Merge/Heap)
   - Cache friendly? (Quick Sort)

Interview Preparation:

✓ Implement: Merge Sort, Quick Sort, Heap Sort
✓ Know: Time/space complexity, stability
✓ Understand: Partition, merge, heapify
✓ Discuss: When to use each algorithm
✓ Optimize: For specific use cases
✓ Trade-offs: Speed vs space vs stability

Next: Master advanced sorting techniques and optimize for production!
""")

print("=" * 70)
print("🎉 Topic 13 Complete! Advanced Sorting Mastered!")
print("=" * 70)
print("\n✅ ADVANCED LEVEL PROGRESSING...")
print("   5 more topics to complete (Topics 14-18)")
print("   Ready for Topic 14: Graph Algorithms\n")
