"""
Project: Greedy Algorithms in the Real World

Build practical systems using greedy algorithms:
1. Content Distribution (Huffman Coding)
2. Event Scheduling (Activity Selection)
3. Task Management (Job Sequencing)
4. Resource Allocation (Greedy Assignment)
"""

import heapq
from typing import List, Tuple, Dict
from dataclasses import dataclass
import time

print("=" * 70)
print("PROJECT: Greedy Algorithms Applications")
print("=" * 70)

# ==================== PART 1: Data Compression (Huffman) ====================
print("\n[PART 1] Data Compression (Huffman Coding)")
print("-" * 70)

class HuffmanNode:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class DataCompressor:
    """Compress data using Huffman coding"""

    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}

    def build_huffman_tree(self, text: str):
        """Build Huffman tree from text"""
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1

        if len(freq) == 1:
            self.codes = {list(freq.keys())[0]: "0"}
            return

        heap = [HuffmanNode(f, c) for c, f in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            parent = HuffmanNode(left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, parent)

        root = heap[0]
        self._build_codes(root)

    def _build_codes(self, node, code=""):
        """Traverse tree to generate codes"""
        if node.char:
            self.codes[node.char] = code
            self.reverse_codes[code] = node.char
        else:
            if node.left:
                self._build_codes(node.left, code + "0")
            if node.right:
                self._build_codes(node.right, code + "1")

    def compress(self, text: str) -> Tuple[str, Dict]:
        """Compress text"""
        self.build_huffman_tree(text)
        encoded = "".join(self.codes[char] for char in text)
        return encoded, self.codes

    def decompress(self, encoded: str) -> str:
        """Decompress text"""
        decoded = []
        i = 0
        while i < len(encoded):
            for length in range(1, len(encoded) - i + 1):
                code = encoded[i:i+length]
                if code in self.reverse_codes:
                    decoded.append(self.reverse_codes[code])
                    i += length
                    break
        return "".join(decoded)

# Test Data Compressor
print("Data Compression Demo:\n")
compressor = DataCompressor()

original_text = "mississippi"
compressed, codes = compressor.compress(original_text)
decompressed = compressor.decompress(compressed)

print(f"Original text: '{original_text}'")
print(f"Length: {len(original_text)} characters")

print(f"\nHuffman codes:")
for char, code in sorted(codes.items()):
    print(f"  {char}: {code}")

print(f"\nCompressed: {compressed}")
print(f"Length: {len(compressed)} bits")

original_bits = len(original_text) * 8
print(f"\nCompression ratio: {original_bits} → {len(compressed)} bits")
print(f"Reduction: {(1 - len(compressed)/original_bits)*100:.1f}%")

print(f"\nDecompressed: '{decompressed}'")
print(f"Verified: {decompressed == original_text}")

print("→ Time: O(n log n), Space: O(n)")
print("→ Real applications: ZIP, gzip, PNG compression")

# ==================== PART 2: Event Scheduling (Activity Selection) ====================
print("\n[PART 2] Event Scheduling (Maximum Non-Overlapping)")
print("-" * 70)

@dataclass
class Event:
    name: str
    start: float
    end: float

class EventScheduler:
    """Schedule maximum non-overlapping events"""

    def __init__(self):
        self.events = []

    def add_event(self, name: str, start: float, end: float):
        """Add event"""
        self.events.append(Event(name, start, end))

    def schedule_maximum(self) -> List[Event]:
        """Select maximum non-overlapping events (activity selection)"""
        if not self.events:
            return []

        # Sort by end time
        sorted_events = sorted(self.events, key=lambda e: e.end)

        scheduled = [sorted_events[0]]
        last_end = sorted_events[0].end

        for event in sorted_events[1:]:
            if event.start >= last_end:
                scheduled.append(event)
                last_end = event.end

        return scheduled

# Test Event Scheduler
print("Event Scheduling Demo:\n")
scheduler = EventScheduler()

events = [
    ("Meeting A", 9.0, 10.5),
    ("Meeting B", 10.0, 11.5),
    ("Lunch", 12.0, 13.0),
    ("Meeting C", 11.0, 12.0),
    ("Meeting D", 13.0, 14.5),
    ("Meeting E", 14.0, 15.0),
]

for name, start, end in events:
    scheduler.add_event(name, start, end)

scheduled = scheduler.schedule_maximum()

print("Available events:")
for name, start, end in sorted(events, key=lambda e: e[1]):
    print(f"  {name:<12} {start:>5.1f}-{end:>5.1f}")

print(f"\nMaximum non-overlapping schedule ({len(scheduled)} events):")
for i, event in enumerate(scheduled, 1):
    print(f"  {i}. {event.name:<12} {event.start:>5.1f}-{event.end:>5.1f}")

print("→ Time: O(n log n), Space: O(n)")
print("→ Greedy: always pick earliest finishing event")

# ==================== PART 3: Task Scheduling (Job Sequencing) ====================
print("\n[PART 3] Task Scheduling (Maximize Profit)")
print("-" * 70)

@dataclass
class Task:
    name: str
    deadline: int
    profit: int

class TaskScheduler:
    """Schedule tasks to maximize profit"""

    def __init__(self):
        self.tasks = []

    def add_task(self, name: str, deadline: int, profit: int):
        """Add task with deadline and profit"""
        self.tasks.append(Task(name, deadline, profit))

    def schedule_optimal(self) -> Tuple[int, Dict]:
        """Maximize profit using job sequencing"""
        if not self.tasks:
            return 0, {}

        # Sort by profit (descending)
        sorted_tasks = sorted(self.tasks, key=lambda t: t.profit, reverse=True)

        max_deadline = max(t.deadline for t in sorted_tasks)
        schedule = {}
        total_profit = 0

        for task in sorted_tasks:
            # Try to schedule at latest slot before deadline
            for slot in range(task.deadline - 1, -1, -1):
                if slot not in schedule:
                    schedule[slot] = task
                    total_profit += task.profit
                    break

        return total_profit, schedule

# Test Task Scheduler
print("Task Scheduling Demo:\n")
scheduler = TaskScheduler()

tasks = [
    ("T1", 4, 100),
    ("T2", 1, 50),
    ("T3", 3, 30),
    ("T4", 2, 40),
    ("T5", 2, 60),
]

for name, deadline, profit in tasks:
    scheduler.add_task(name, deadline, profit)

max_profit, schedule = scheduler.schedule_optimal()

print("Tasks (deadline, profit):")
for task in tasks:
    print(f"  {task[0]:<3} Deadline: {task[1]}, Profit: ${task[2]}")

print(f"\nOptimal schedule (maximize profit):")
for slot in sorted(schedule.keys()):
    task = schedule[slot]
    print(f"  Slot {slot + 1}: {task.name} (profit: ${task.profit})")

print(f"\nTotal profit: ${max_profit}")

print("→ Time: O(n²), Space: O(n)")
print("→ Greedy: schedule high-profit tasks first")

# ==================== PART 4: Resource Allocation (Greedy Matching) ====================
print("\n[PART 4] Resource Allocation (Optimal Matching)")
print("-" * 70)

class ResourceAllocator:
    """Allocate resources optimally to recipients"""

    def __init__(self):
        self.resources = []
        self.recipients = []

    def add_resource(self, resource_id: str, capability: int):
        """Add resource with capability level"""
        self.resources.append((resource_id, capability))

    def add_recipient(self, recipient_id: str, need: int):
        """Add recipient with need level"""
        self.recipients.append((recipient_id, need))

    def allocate_optimal(self) -> Tuple[List[Tuple], int]:
        """Maximize satisfied recipients (greedy matching)"""
        # Sort both by capability/need
        sorted_resources = sorted(self.resources, key=lambda x: x[1])
        sorted_recipients = sorted(self.recipients, key=lambda x: x[1])

        allocations = []
        total_satisfied = 0

        r_idx = 0
        for rec_id, need in sorted_recipients:
            while r_idx < len(sorted_resources):
                res_id, capability = sorted_resources[r_idx]
                if capability >= need:
                    allocations.append((rec_id, res_id, need))
                    total_satisfied += 1
                    r_idx += 1
                    break
                r_idx += 1

        return allocations, total_satisfied

# Test Resource Allocator
print("Resource Allocation Demo:\n")
allocator = ResourceAllocator()

resources = [
    ("R1", 5),
    ("R2", 10),
    ("R3", 3),
    ("R4", 15),
]

recipients = [
    ("User A", 8),
    ("User B", 3),
    ("User C", 12),
    ("User D", 2),
]

for res_id, capability in resources:
    allocator.add_resource(res_id, capability)

for rec_id, need in recipients:
    allocator.add_recipient(rec_id, need)

allocations, satisfied = allocator.allocate_optimal()

print("Resources (capability):")
for res_id, cap in resources:
    print(f"  {res_id}: level {cap}")

print("\nRecipients (need):")
for rec_id, need in recipients:
    print(f"  {rec_id}: needs level {need}")

print(f"\nOptimal allocation ({satisfied}/{len(recipients)} satisfied):")
for rec_id, res_id, need in allocations:
    print(f"  {rec_id} ← {res_id} (need: {need})")

print("→ Time: O(n log n), Space: O(n)")
print("→ Greedy: match smallest need first")

# ==================== PART 5: Algorithm Comparison ====================
print("\n[PART 5] Greedy Algorithm Comparison")
print("-" * 70)

print("Algorithm Characteristics:\n")

algorithms = {
    "Activity Selection": {
        "greedy": True,
        "time": "O(n log n)",
        "space": "O(n)",
        "use": "Non-overlapping events"
    },
    "Huffman Coding": {
        "greedy": True,
        "time": "O(n log n)",
        "space": "O(n)",
        "use": "Data compression"
    },
    "Job Sequencing": {
        "greedy": True,
        "time": "O(n²)",
        "space": "O(n)",
        "use": "Maximize profit"
    },
    "Fractional Knapsack": {
        "greedy": True,
        "time": "O(n log n)",
        "space": "O(n)",
        "use": "Max value (divisible)"
    },
    "0/1 Knapsack": {
        "greedy": False,
        "time": "O(nW)",
        "space": "O(nW)",
        "use": "Max value (indivisible)"
    },
    "Coin Change": {
        "greedy": False,
        "time": "O(nC)",
        "space": "O(n)",
        "use": "Min coins (arbitrary)"
    },
}

print(f"{'Algorithm':<25} {'Greedy?':<10} {'Time':<15} {'Space':<10} {'Use Case':<20}")
print("-" * 80)

for algo, info in algorithms.items():
    greedy = "✓" if info["greedy"] else "✗"
    print(f"{algo:<25} {greedy:<10} {info['time']:<15} {info['space']:<10} {info['use']:<20}")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World Greedy Algorithm Applications:

1. Data Compression (Huffman Coding)
   - Optimal variable-length prefix codes
   - Greedy: Merge two smallest frequency nodes
   - Result: ~30% compression for English text
   - Real apps: ZIP, gzip, PNG, JPEG

2. Event Scheduling (Activity Selection)
   - Schedule maximum non-overlapping events
   - Greedy: Always pick earliest finishing event
   - Optimal for unweighted activities
   - Real apps: Calendar apps, room scheduling

3. Task Scheduling (Job Sequencing)
   - Maximize profit with deadline constraints
   - Greedy: Schedule high-profit tasks first
   - Handles deadlines and profits
   - Real apps: Project management, task queues

4. Resource Allocation (Greedy Matching)
   - Allocate limited resources to recipients
   - Greedy: Match smallest need first
   - Maximize satisfied recipients
   - Real apps: Cloud computing, task assignment

Key Insights:

✓ Greedy = Fast when it works (O(n log n) typical)
✓ Greedy = Optimal for specific problem classes
✗ Greedy ≠ Always optimal (test counterexamples!)
✓ Huffman = Proven optimal (information theory)
✓ Activity = Proven optimal (exchange argument)
✓ Fractional = Proven optimal (ratio argument)

Greedy vs Other Approaches:

Greedy Advantages:
✓ Fast: Often O(n log n) vs DP O(n²)
✓ Simple: Intuitive solutions
✓ Memory: Less space than DP
✓ Online: Can make decisions immediately

Greedy Disadvantages:
✗ Not always optimal (0/1 knapsack)
✗ Problem-specific (need to prove)
✗ No future consideration
✗ Can't backtrack

Algorithm Selection:

For Maximum Non-Overlapping:
→ Activity Selection (greedy ✓)
→ Weighted Interval (DP needed)

For Data Compression:
→ Huffman Coding (greedy ✓)
→ LZ77/LZ78 (different approach)

For Profit Maximization:
→ Fractional Knapsack (greedy ✓)
→ 0/1 Knapsack (DP needed)
→ Job Sequencing (greedy ✓)

Interview Preparation:

1. Recognize Greedy Problems:
   - "Maximum/minimum number..."
   - "Non-overlapping items..."
   - "Optimal ordering..."

2. Prove Greedy Correctness:
   - Exchange argument
   - Induction
   - Show counterexample if false

3. Implement Efficiently:
   - Use appropriate sorting
   - Consider priority queues
   - Handle edge cases

4. Compare Approaches:
   - Greedy vs DP
   - When each applies
   - Complexity trade-offs

Real-World Impact:

- Compression: Billions of files use Huffman daily
- Scheduling: Every calendar app uses activity selection
- Task Management: Project tools use job sequencing
- Resource Allocation: Cloud providers use greedy matching
- Network Routing: Dijkstra (greedy) in all routers

Complexity Reference:

Problem                 Greedy?  Time        Space   Use
────────────────────────────────────────────────────────
Activity Selection      ✓        O(n log n)  O(n)    Events
Huffman Coding          ✓        O(n log n)  O(n)    Compress
Job Sequencing          ✓        O(n²)       O(n)    Tasks
Fractional Knapsack     ✓        O(n log n)  O(n)    Divisible
0/1 Knapsack            ✗        O(nW)       O(W)    DP
Coin Change             ✗        O(nC)       O(n)    DP
Dijkstra                ✓        O((V+E)logV) O(V)   Shortest
MST                     ✓        O(E log E)  O(V)    Spanning

Next: Master greedy algorithm pattern recognition and proofs!
""")

print("=" * 70)
print("🎉 Topic 15 Complete! Greedy Algorithms Mastered!")
print("=" * 70)
print("\n✅ ADVANCED LEVEL 75% COMPLETE...")
print("   3 more topics to complete (Topics 16-18)")
print("   Ready for Topic 16: Bit Manipulation\n")
