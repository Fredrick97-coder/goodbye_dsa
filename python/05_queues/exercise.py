"""
Exercises: Queues - First In, First Out (FIFO)

Practice queue operations, implementations, and solving problems with queues.
Solve these problems and identify the time/space complexity of your solution.
"""

from collections import deque
from typing import List, Optional

print("=" * 60)
print("EXERCISES: Queues")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

# EASY 1: Implement Queue Class
print("\n1. IMPLEMENT QUEUE CLASS")
print("Problem: Create a Queue class with enqueue, dequeue, front, isEmpty")
print("""
Methods needed:
- enqueue(x): Add element to rear
- dequeue(): Remove and return front element
- front(): View front element without removing
- isEmpty(): Check if empty
- size(): Get number of elements
""")
print("\nWrite your solution:")

class Queue:
    """Queue implementation"""

    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        # TODO: Implement
        pass

    def dequeue(self):
        # TODO: Implement
        pass

    def front(self):
        # TODO: Implement
        pass

    def isEmpty(self):
        # TODO: Implement
        pass

    def size(self):
        # TODO: Implement
        pass

# EASY 2: Reverse a Queue
print("\n2. REVERSE A QUEUE")
print("Problem: Reverse the order of elements in a queue")
print("Input: Queue [1, 2, 3, 4, 5]")
print("Output: Queue [5, 4, 3, 2, 1]")
print("Constraint: Don't use lists, only queue operations and stack")
print("\nYour solution:")

def reverse_queue(queue):
    """Reverse a queue"""
    # TODO: Write your code here
    # Hint: Use a stack as helper data structure
    pass

# EASY 3: Rotate Queue
print("\n3. ROTATE QUEUE")
print("Problem: Rotate queue to right by k positions")
print("Input: [1, 2, 3, 4, 5], k=2")
print("Output: [4, 5, 1, 2, 3]")
print("\nYour solution:")

def rotate_queue(q, k):
    """Rotate queue right by k positions"""
    # TODO: Write your code here
    # Hint: Move element from front to rear, k times
    pass

# EASY 4: Queue Size
print("\n4. QUEUE SIZE OPERATIONS")
print("Problem: Track queue size after series of operations")
print("Operations: enqueue(5), enqueue(10), dequeue(), enqueue(20)")
print("Output: Size after each operation")
print("\nYour solution:")

def track_queue_operations(operations):
    """Track queue size after operations"""
    # TODO: Write your code here
    # operations = [('enqueue', 5), ('enqueue', 10), ('dequeue',), ...]
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

# MEDIUM 1: Number of Recent Calls
print("\n5. NUMBER OF RECENT CALLS")
print("Problem: Count function calls in last 3000 ms")
print("Input: calls at [100, 300, 803, 806, 1000, 1100]")
print("ping(2000) → 4 calls in [2000-3000, 2000] = [806, 1000, 1100, 2000]")
print("\nYour solution:")

class RecentCounter:
    """Count recent function calls"""

    def __init__(self):
        self.queue = deque()

    def ping(self, t: int) -> int:
        """Add timestamp and return count in last 3000 ms"""
        # TODO: Write your code here
        # Hint: Keep only calls within [t-3000, t]
        pass

# MEDIUM 2: Moving Average from Data Stream
print("\n6. MOVING AVERAGE FROM DATA STREAM")
print("Problem: Calculate moving average of last 3 elements")
print("Input: [1, 10, 3, 1, 0]")
print("Output: ")
print("  next(1) → 1.0")
print("  next(10) → 5.5 (avg of 1, 10)")
print("  next(3) → 4.67 (avg of 1, 10, 3)")
print("  next(1) → 4.67 (avg of 10, 3, 1)")
print("  next(0) → 1.33 (avg of 3, 1, 0)")
print("\nYour solution:")

class MovingAverage:
    """Calculate moving average of last n elements"""

    def __init__(self, size: int):
        self.size = size
        self.queue = deque()
        self.sum = 0

    def next(self, val: int) -> float:
        """Add value and return moving average"""
        # TODO: Write your code here
        # Maintain queue of last 'size' elements
        pass

# MEDIUM 3: BFS Level Order
print("\n7. LEVEL ORDER TRAVERSAL")
print("Problem: Traverse binary tree level by level")
print("""
Tree:
    1
   / \\
  2   3
 / \\
4   5

Output: [[1], [2, 3], [4, 5]]
""")
print("\nYour solution:")

def level_order_traversal(root):
    """Traverse tree level by level using queue"""
    # TODO: Write your code here
    # Hint: Process all nodes at each level together
    pass

# MEDIUM 4: Reveal Cards in Increasing Order
print("\n8. REVEAL CARDS IN INCREASING ORDER")
print("Problem: Find original deck order given reveal sequence")
print("If deck = [17,13,11,2,3,5,7], reveal gives [2,13,3,11,5,17,7]")
print("Reverse the process using queue")
print("\nYour solution:")

def deck_revealed_increasing(deck: List[int]) -> List[int]:
    """Find original deck order"""
    # TODO: Write your code here
    # Hint: Process revealed order in reverse with a queue
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

# HARD 1: Rotting Oranges
print("\n9. ROTTING ORANGES")
print("Problem: Find minimum time for all fresh oranges to rot (BFS)")
print("""
Grid (2=rotten, 1=fresh, 0=empty):
[[2,1,1],
 [1,1,0],
 [0,1,1]]

Rotten spreads to adjacent fresh oranges each minute.
Output: 4 minutes to rot all fresh oranges
""")
print("\nYour solution:")

def oranges_rotting(grid: List[List[int]]) -> int:
    """Find time for all oranges to rot using BFS"""
    # TODO: Write your code here
    # Hint: Use BFS with time tracking from all rotten starting points
    pass

# HARD 2: Number of Islands
print("\n10. NUMBER OF ISLANDS")
print("Problem: Count islands in grid using BFS")
print("""
Grid:
[['1','1','0','0','0'],
 ['1','1','0','0','0'],
 ['0','0','1','0','0'],
 ['0','0','0','1','1']]

Output: 3 islands
""")
print("\nYour solution:")

def num_islands(grid: List[List[str]]) -> int:
    """Count islands using BFS"""
    # TODO: Write your code here
    # Hint: Use BFS to explore each island completely
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

# CHALLENGE 1: Shortest Path in Matrix
print("\n11. SHORTEST PATH IN MATRIX (BFS)")
print("Problem: Find shortest path from start to end in matrix")
print("Can move in 4 directions (up, down, left, right)")
print("Return length of shortest path, or -1 if no path exists")
print("\nYour solution:")

def shortest_path_matrix(grid: List[List[int]]) -> int:
    """Find shortest path using BFS"""
    # TODO: Write your code here
    # Hint: BFS guarantees shortest path in unweighted graph
    # Start from (0,0), find path to (m-1, n-1)
    pass

# CHALLENGE 2: Word Ladder
print("\n12. WORD LADDER (BFS)")
print("Problem: Find shortest transformation sequence from start to end word")
print("""
Example:
Start: "hit"
End: "cog"
Dict: ["hot", "dot", "dog", "lot", "log", "cog"]

Transformation:
hit → hot → dot → dog → cog
Output: 5 (length of transformation sequence)
""")
print("Constraint: Each step changes exactly one letter")
print("\nYour solution:")

def word_ladder(start: str, end: str, word_list: List[str]) -> int:
    """Find shortest word transformation sequence using BFS"""
    # TODO: Write your code here
    # Hint: Model as graph where words are nodes, edges exist between
    #       words that differ by one letter
    pass

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Queue Concepts to Master:
1. FIFO (First-In-First-Out) principle
2. O(1) operations: enqueue, dequeue, front
3. Queue vs Stack (opposite orderings)
4. BFS (Breadth-First Search)
5. Level-order tree traversal
6. Circular queues for space efficiency
7. Deque (double-ended queue)

Key Algorithms:
- BFS for shortest path
- Level-order traversal
- Rotting oranges (multi-source BFS)
- Word ladder (BFS on word graph)
- Number of islands (BFS/DFS)

Performance Tips:
✓ Use deque, never list.pop(0)
✓ Use BFS for unweighted shortest path
✓ Track visited nodes to avoid cycles
✓ Handle level-by-level processing carefully
✓ Use deque for double-ended operations

Common Patterns:
1. BFS: Queue-based level traversal
2. Level tracking: Process all nodes at current level
3. Time tracking: Include timestamp in queue
4. Multi-source: Start with multiple queue items
5. Visited set: Track explored nodes

Next: Complete the project with real BFS applications
""")
