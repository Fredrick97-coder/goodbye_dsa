"""
Project: Linked List Applications & Analysis

Build practical linked list implementations and solve real problems:
1. LRU Cache using doubly linked list
2. Music playlist (circular linked list)
3. Undo/Redo system
4. Performance comparison with arrays
"""

from typing import Optional, Dict

print("=" * 70)
print("PROJECT: Linked List Applications & Analysis")
print("=" * 70)

# ==================== Node Classes ====================

class Node:
    """Singly linked list node"""
    def __init__(self, data):
        self.data = data
        self.next = None

class DNode:
    """Doubly linked list node"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

# ==================== PART 1: LRU Cache ====================
print("\n[PART 1] LRU Cache Using Doubly Linked List")
print("-" * 70)

class LRUCache:
    """LRU Cache implementation with O(1) get/put"""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[int, DNode] = {}
        self.head = DNode(0, 0)
        self.tail = DNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: DNode) -> None:
        """Add node right after head (most recent)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: DNode) -> None:
        """Remove node from list"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: DNode) -> None:
        """Move node to head (mark as most recent)"""
        self._remove_node(node)
        self._add_node(node)

    def get(self, key: int) -> int:
        """Get value and mark as recently used"""
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Put key-value pair, evict LRU if needed"""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            if len(self.cache) == self.capacity:
                # Evict LRU (last node before tail)
                lru = self.tail.prev
                self._remove_node(lru)
                del self.cache[lru.key]

            # Add new node
            new_node = DNode(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)

# Test LRU Cache
print("LRU Cache Demo (capacity=2):\n")
lru = LRUCache(2)

operations = [
    ("put(1, 1)", lambda: lru.put(1, 1)),
    ("put(2, 2)", lambda: lru.put(2, 2)),
    ("get(1)", lambda: lru.get(1)),
    ("put(3, 3) - evicts 2", lambda: lru.put(3, 3)),
    ("get(2) - returns -1", lambda: lru.get(2)),
    ("put(4, 4) - evicts 1", lambda: lru.put(4, 4)),
    ("get(1) - returns -1", lambda: lru.get(1)),
    ("get(3, 4)", lambda: (lru.get(3), lru.get(4))),
]

for desc, op in operations:
    result = op()
    print(f"  {desc:<35} → {result if result else 'done'}")

print("\n→ Time: O(1) for get/put with doubly linked list")
print("→ Space: O(capacity)")

# ==================== PART 2: Circular Playlist ====================
print("\n[PART 2] Music Playlist (Circular Linked List)")
print("-" * 70)

class Song(Node):
    """Song node for circular linked list"""
    def __init__(self, title):
        self.title = title
        self.next = None

class Playlist:
    """Circular linked list for music playlist"""

    def __init__(self):
        self.current = None

    def add_song(self, title):
        """Add song to playlist"""
        new_song = Song(title)

        if not self.current:
            self.current = new_song
            new_song.next = new_song  # Point to itself
        else:
            # Find last song
            last = self.current
            while last.next != self.current:
                last = last.next

            last.next = new_song
            new_song.next = self.current

    def play_next(self):
        """Play next song in playlist"""
        if self.current:
            song = self.current
            self.current = self.current.next
            return song.title
        return None

    def print_playlist(self, limit=None):
        """Print playlist"""
        if not self.current:
            return []

        songs = []
        node = self.current
        count = 0

        while True:
            songs.append(node.title)
            node = node.next
            count += 1

            if node == self.current or (limit and count >= limit):
                break

        return songs

# Test playlist
print("Playlist Demo:\n")
playlist = Playlist()
songs = ["Song A", "Song B", "Song C", "Song D"]

for song in songs:
    playlist.add_song(song)
    print(f"  Added: {song}")

print(f"\nPlaylist: {playlist.print_playlist()}")
print("\nPlaying next 6 times (circular):")
for i in range(6):
    next_song = playlist.play_next()
    print(f"  {i+1}. Now playing: {next_song}")

print("\n→ Circular structure: last node points to first")
print("→ Useful for round-robin scheduling")

# ==================== PART 3: Undo/Redo System ====================
print("\n[PART 3] Undo/Redo System with Doubly Linked List")
print("-" * 70)

class History:
    """Undo/Redo system using doubly linked list"""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.current_state = ""

    def do_action(self, action):
        """Perform action"""
        self.undo_stack.append(self.current_state)
        self.current_state = action
        self.redo_stack.clear()

    def undo(self):
        """Undo last action"""
        if self.undo_stack:
            self.redo_stack.append(self.current_state)
            self.current_state = self.undo_stack.pop()

    def redo(self):
        """Redo last undone action"""
        if self.redo_stack:
            self.undo_stack.append(self.current_state)
            self.current_state = self.redo_stack.pop()

    def get_state(self):
        return self.current_state if self.current_state else "(empty)"

# Test undo/redo
print("Undo/Redo Demo:\n")
history = History()

actions = [
    ("Type 'Hello'", "Hello"),
    ("Type ' World'", "Hello World"),
    ("Type '!'", "Hello World!"),
]

for desc, state in actions:
    history.do_action(state)
    print(f"  {desc:<20} → State: '{history.get_state()}'")

print(f"\nUndo:")
history.undo()
print(f"  After undo → State: '{history.get_state()}'")

history.undo()
print(f"  After undo → State: '{history.get_state()}'")

print(f"\nRedo:")
history.redo()
print(f"  After redo → State: '{history.get_state()}'")

print("\n→ Doubly linked list allows bidirectional navigation")
print("→ Perfect for undo/redo with forward and backward history")

# ==================== PART 4: Performance Analysis ====================
print("\n[PART 4] Linked List vs Array Performance")
print("-" * 70)

import time

def benchmark_insertion(size):
    """Compare insertion performance"""
    # Array: insert at beginning
    arr = list(range(size))
    start = time.time()
    for _ in range(10):
        arr.insert(0, -1)
    arr_time = (time.time() - start) * 1000

    # Linked list: insert at beginning
    head = None
    for val in range(size):
        new = Node(val)
        new.next = head
        head = new

    start = time.time()
    for _ in range(10):
        new = Node(-1)
        new.next = head
        head = new
    ll_time = (time.time() - start) * 1000

    return arr_time, ll_time

print("Inserting at beginning (10 times):\n")
print(f"{'Size':<10} {'Array':<15} {'Linked List':<15} {'Winner':<15}")
print("-" * 55)

for size in [100, 1000, 5000]:
    arr_t, ll_t = benchmark_insertion(size)
    winner = "Linked List" if ll_t < arr_t else "Array"
    print(f"{size:<10} {arr_t:>6.3f} ms{'':<8} {ll_t:>6.3f} ms{'':<8} {winner:<15}")

print("\n→ Linked list much faster for beginning insertions")
print("→ Array slower because it shifts all elements")

# ==================== PART 5: Summary ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World Linked List Applications:

1. LRU Cache
   - Uses doubly linked list for O(1) operations
   - Maintains insertion order and recency
   - Critical for memory management, browser caching

2. Music Playlist
   - Circular linked list for round-robin
   - Continuous playback without bounds checking
   - Used in: audio players, scheduling systems

3. Undo/Redo System
   - Doubly linked list for bidirectional navigation
   - Maintains history forward and backward
   - Used in: text editors, design tools, IDEs

Performance Characteristics:

Operation        Array          Linked List
─────────────────────────────────────────
Access           O(1)           O(n)
Search           O(n)           O(n)
Insert at head   O(n)           O(1) ✓
Insert at end    O(1)           O(n)
Delete head      O(n)           O(1) ✓
Delete at pos    O(n)           O(n)

Key Insights:

✓ Use linked lists for frequent insertions/deletions at head
✓ Use arrays for random access
✓ Doubly linked lists enable bidirectional traversal
✓ Circular linked lists enable continuous loops
✓ Dummy nodes simplify edge case handling
✓ Two-pointer technique solves many problems (middle, cycle)

Common Problems:

✓ Reverse linked list (iterative & recursive)
✓ Find middle (slow-fast pointers)
✓ Detect cycle (Floyd's algorithm)
✓ Merge sorted lists
✓ Check palindrome
✓ Add two numbers
✓ Reorder list

Space-Time Trade-offs:

Singly LL:
  Best for: one-way traversal, head operations
  Space: O(1) pointers (one per node)

Doubly LL:
  Best for: bidirectional ops, close-to-end insertions
  Space: O(1) extra per node for prev pointer

Circular LL:
  Best for: round-robin, wrap-around scenarios
  Space: Same as singly LL

Interview Tips:

1. Draw the list and trace operations
2. Use dummy node to simplify edge cases
3. Two pointers for finding middle/cycle
4. Reverse second half for palindrome checks
5. Always handle None/null cases
6. Think about prev pointer operations (doubly LL)

Next Steps:
1. Master linked list operations thoroughly
2. Practice on LeetCode medium-level problems
3. Understand trade-offs with arrays
4. Move to Topic 08: Trees (basics)
""")

print("=" * 70)
print("Project Complete! Topic 07 Finished Successfully!")
print("=" * 70)
