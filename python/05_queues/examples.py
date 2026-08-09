"""
Examples: Queues - First In, First Out (FIFO)

Demonstrates queue operations, implementations, and common applications.
"""

from collections import deque
from typing import List, Optional

print("=" * 60)
print("QUEUES - PRACTICAL EXAMPLES")
print("=" * 60)

# ==================== (1) Basic Queue using deque ====================
print("\n[1] Basic Queue Using collections.deque")
print("-" * 40)

queue = deque()

# Enqueue (add to rear) - O(1)
queue.append(10)
queue.append(20)
queue.append(30)
print(f"After enqueuing 10, 20, 30: {list(queue)}")

# Peek (look at front) - O(1)
print(f"Front element (peek): {queue[0]}")

# Dequeue (remove from front) - O(1)
front = queue.popleft()
print(f"Dequeued element: {front}")
print(f"Queue after dequeue: {list(queue)}")

# Check if empty
print(f"Is empty: {len(queue) == 0}")
print(f"Queue size: {len(queue)}")

print("→ Always use deque, never list.pop(0) which is O(n)!")

# ==================== (2) Custom Queue Class ====================
print("\n[2] Custom Queue Class Implementation")
print("-" * 40)

class Queue:
    """Simple Queue implementation using deque"""

    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        """Add item to rear - O(1)"""
        self.items.append(item)

    def dequeue(self):
        """Remove and return front item - O(1)"""
        if not self.is_empty():
            return self.items.popleft()
        return None

    def front(self):
        """View front item without removing - O(1)"""
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return len(self.items) == 0

    def size(self):
        """Get number of items - O(1)"""
        return len(self.items)

    def __repr__(self):
        return f"Queue({list(self.items)})"

queue = Queue()
queue.enqueue(5)
queue.enqueue(10)
queue.enqueue(15)

print(f"Queue: {queue}")
print(f"Front: {queue.front()}")
print(f"Dequeue: {queue.dequeue()}")
print(f"Size: {queue.size()}")
print(f"Is empty: {queue.is_empty()}")

# ==================== (3) Queue vs Stack Comparison ====================
print("\n[3] Queue (FIFO) vs Stack (LIFO) Comparison")
print("-" * 40)

# Queue - FIFO
queue = deque()
queue.append('A')
queue.append('B')
queue.append('C')
print(f"Queue after adding A, B, C: {list(queue)}")
print(f"Queue removal order: {queue.popleft()}, {queue.popleft()}, {queue.popleft()}")

# Stack - LIFO
stack = []
stack.append('A')
stack.append('B')
stack.append('C')
print(f"\nStack after adding A, B, C: {stack}")
print(f"Stack removal order: {stack.pop()}, {stack.pop()}, {stack.pop()}")

print("→ Queue: First in, First out (A, B, C)")
print("→ Stack: Last in, First out (C, B, A)")

# ==================== (4) Circular Queue Concept ====================
print("\n[4] Circular Queue (Space Reuse)")
print("-" * 40)

class CircularQueue:
    """Circular Queue with fixed size"""

    def __init__(self, max_size):
        self.items = [None] * max_size
        self.max_size = max_size
        self.front_idx = -1
        self.rear_idx = -1

    def enqueue(self, item):
        """Add item"""
        if (self.rear_idx + 1) % self.max_size == self.front_idx:
            print("Queue is full!")
            return False

        self.rear_idx = (self.rear_idx + 1) % self.max_size
        self.items[self.rear_idx] = item

        if self.front_idx == -1:
            self.front_idx = 0

        return True

    def dequeue(self):
        """Remove item"""
        if self.front_idx == -1:
            print("Queue is empty!")
            return None

        item = self.items[self.front_idx]

        if self.front_idx == self.rear_idx:
            self.front_idx = -1
            self.rear_idx = -1
        else:
            self.front_idx = (self.front_idx + 1) % self.max_size

        return item

cq = CircularQueue(5)
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
print(f"Circular Queue: {cq.items}")
print(f"Dequeue: {cq.dequeue()}")
print(f"Enqueue 40: {cq.enqueue(40)}")
print(f"Circular Queue after reuse: {cq.items}")

# ==================== (5) Breadth-First Search (BFS) ====================
print("\n[5] Breadth-First Search (BFS) Using Queue")
print("-" * 40)

def bfs(graph, start):
    """BFS traversal of graph"""
    visited = set([start])
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
}

print("Graph:", graph)
bfs_result = bfs(graph, 'A')
print(f"BFS from A: {bfs_result}")
print("→ Visits level by level (breadth first)")

# ==================== (6) Level-Order Tree Traversal ====================
print("\n[6] Level-Order Tree Traversal")
print("-" * 40)

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def level_order_traversal(root):
    """Traverse tree level by level"""
    if not root:
        return []

    queue = deque([root])
    result = []

    while queue:
        level_size = len(queue)
        level_values = []

        # Process all nodes at current level
        for _ in range(level_size):
            node = queue.popleft()
            level_values.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level_values)

    return result

# Build tree
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

levels = level_order_traversal(root)
print(f"Tree structure:")
print(f"       1")
print(f"      / \\")
print(f"     2   3")
print(f"    / \\")
print(f"   4   5")
print(f"\nLevel-order (BFS): {levels}")

# ==================== (7) Printer Queue Simulation ====================
print("\n[7] Printer Queue Simulation")
print("-" * 40)

class PrinterQueue:
    """Simulate a printer queue"""

    def __init__(self):
        self.queue = deque()

    def send_to_printer(self, document):
        """Add document to print queue"""
        self.queue.append(document)
        print(f"  Sent '{document}' to printer")

    def print_next(self):
        """Print next document in queue"""
        if self.queue:
            doc = self.queue.popleft()
            print(f"  Printing '{doc}'...")
            return doc
        else:
            print("  Queue is empty!")
            return None

    def queue_status(self):
        """Show current queue"""
        return list(self.queue)

printer = PrinterQueue()
printer.send_to_printer("Document1.pdf")
printer.send_to_printer("Document2.pdf")
printer.send_to_printer("Document3.pdf")

print(f"Queue: {printer.queue_status()}")
printer.print_next()
printer.print_next()
print(f"Queue: {printer.queue_status()}")

# ==================== (8) Rotating Array (Queue Application) ====================
print("\n[8] Rotating Array Using Queue")
print("-" * 40)

def rotate_array(arr, k):
    """Rotate array to right by k positions"""
    queue = deque(arr)

    # Move first element to end, k times
    for _ in range(k % len(arr)):
        queue.append(queue.popleft())

    return list(queue)

arr = [1, 2, 3, 4, 5]
rotated = rotate_array(arr, 2)
print(f"Original: {arr}")
print(f"Rotated right by 2: {rotated}")
print("→ Move elements from front to rear k times")

# ==================== (9) Deque (Double-Ended Queue) ====================
print("\n[9] Deque - Double-Ended Queue")
print("-" * 40)

dq = deque()

# Add to both ends
dq.append(5)        # Add to right
dq.appendleft(1)    # Add to left
dq.append(7)
dq.appendleft(3)

print(f"Deque after operations: {list(dq)}")

# Remove from both ends
dq.pop()            # Remove from right
dq.popleft()        # Remove from left

print(f"After removing from both ends: {list(dq)}")
print("→ Deque allows operations at both ends")

# ==================== (10) Task Scheduling ====================
print("\n[10] Task Scheduling Queue")
print("-" * 40)

class TaskScheduler:
    """Schedule and execute tasks"""

    def __init__(self):
        self.queue = deque()

    def add_task(self, task):
        """Add task to schedule"""
        self.queue.append(task)
        print(f"  Task added: {task}")

    def execute_next(self):
        """Execute next task"""
        if self.queue:
            task = self.queue.popleft()
            print(f"  Executing: {task}")
            return task
        else:
            print("  No tasks to execute!")
            return None

    def pending_tasks(self):
        """Get remaining tasks"""
        return list(self.queue)

scheduler = TaskScheduler()
scheduler.add_task("Task A")
scheduler.add_task("Task B")
scheduler.add_task("Task C")

print(f"Pending: {scheduler.pending_tasks()}")
scheduler.execute_next()
scheduler.execute_next()
print(f"Pending: {scheduler.pending_tasks()}")

# ==================== (11) Generate Numbers Using BFS ====================
print("\n[11] Generate Binary Numbers (BFS Pattern)")
print("-" * 40)

def generate_binary_numbers(n):
    """Generate first n binary numbers using queue"""
    queue = deque(['1'])
    result = []

    for _ in range(n):
        num = queue.popleft()
        result.append(num)

        # Add next numbers (append 0 and 1 to current)
        queue.append(num + '0')
        queue.append(num + '1')

    return result

binary = generate_binary_numbers(10)
print(f"First 10 binary numbers: {binary}")
print("→ BFS-style generation using queue")

# ==================== (12) Complexity Analysis ====================
print("\n[12] Queue Complexity Summary")
print("-" * 40)

operations = {
    "enqueue(x)": "O(1)",
    "dequeue()": "O(1)",
    "front()": "O(1)",
    "isEmpty()": "O(1)",
    "size()": "O(1)",
}

print("Queue Operation Complexities:")
print(f"{'Operation':<20} {'Time Complexity':<15} {'Space':<10}")
print("-" * 45)
for op, complexity in operations.items():
    print(f"{op:<20} {complexity:<15} {'N/A':<10}")

print("\nOverall:")
print("  Space Complexity: O(n) where n = number of elements")
print("  All operations: O(1) constant time")

print("\n" + "=" * 60)
print("Next: Complete exercises and build the project!")
print("=" * 60)
