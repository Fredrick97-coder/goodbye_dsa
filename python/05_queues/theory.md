# Queues - First In, First Out (FIFO)

A queue is a linear data structure where elements are added at the rear and removed from the front.

---

## 1. What is a Queue?

A **queue** follows the **FIFO principle** (First-In-First-Out):
- First element added is the first one removed
- Like a line at a supermarket: first customer served leaves first
- Like a printer queue: first document sent gets printed first

### Real-world examples:
- Printer queue (documents)
- Customer service queue (people waiting)
- Task scheduling (jobs to process)
- Breadth-first search (traversal)
- Message queues (systems)

---

## 2. Queue Operations

| Operation | Time | Description |
|-----------|------|-------------|
| **enqueue(x)** | O(1) | Add element to rear |
| **dequeue()** | O(1) | Remove and return front element |
| **front()** / **peek()** | O(1) | View front element without removing |
| **isEmpty()** | O(1) | Check if queue is empty |
| **size()** | O(1) | Get number of elements |

### Visual Representation:
```
enqueue (add to rear)  →  [1, 2, 3, 4, 5]  →  dequeue (remove from front)
                        rear ↑      front ↑
```

---

## 3. Implementation Approaches

### Approach 1: Using Python List (Simple but Inefficient)
```python
queue = []
queue.append(10)        # enqueue - O(1)
queue.pop(0)            # dequeue - O(n) ❌ BAD!
queue[0]                # front - O(1)
```
❌ **Problem**: `pop(0)` is O(n) because it shifts all elements!

### Approach 2: Using collections.deque (Best)
```python
from collections import deque
queue = deque()
queue.append(10)        # enqueue - O(1) ✅
queue.popleft()         # dequeue - O(1) ✅
queue[0]                # front - O(1) ✅
```
✅ **Best choice** for queues in Python!

### Approach 3: Custom Queue Class
```python
class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        return None
    
    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

---

## 4. Circular Queue

A **circular queue** reuses the space at the front after dequeuing.

### Benefits:
- More efficient space usage
- Prevents "wasted" space in array-based queues
- Useful for fixed-size applications

### How it works:
```
Normal queue (linear):
Enqueue 1,2,3,4 then Dequeue 1,2 → space wasted
[_, _, 3, 4]

Circular queue:
Enqueue 1,2,3,4 then Dequeue 1,2 → space reused
[5, 6, 3, 4] → wrap around
```

---

## 5. Queue vs Stack

| Feature | Queue | Stack |
|---------|-------|-------|
| Order | FIFO | LIFO |
| Insert | Rear | Top |
| Remove | Front | Top |
| Use case | BFS, scheduling, messaging | DFS, undo, parsing |
| Real-world | Supermarket line | Stack of plates |

---

## 6. Common Queue Applications

### 1. **Breadth-First Search (BFS)**
```python
# Graph traversal using queue
def bfs(start_node):
    queue = deque([start_node])
    visited = set([start_node])
    
    while queue:
        node = queue.popleft()
        # Process node
        for neighbor in node.neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
```

### 2. **Level-Order Tree Traversal**
```python
# Visit tree level by level
def level_order(root):
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        # Process node
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

### 3. **Task Scheduling**
```python
# Process tasks in order
task_queue = deque()

def add_task(task):
    task_queue.append(task)

def process_next_task():
    if task_queue:
        task = task_queue.popleft()
        execute(task)
```

### 4. **Printer Queue**
```python
# Documents printed in order received
printer_queue = deque()

def send_to_printer(document):
    printer_queue.append(document)

def print_next():
    if printer_queue:
        doc = printer_queue.popleft()
        print_document(doc)
```

### 5. **Message Queue**
```python
# Process messages asynchronously
message_queue = deque()

def receive_message(msg):
    message_queue.append(msg)

def process_messages():
    while message_queue:
        msg = message_queue.popleft()
        handle_message(msg)
```

---

## 7. Complexity Analysis

### Time Complexity:
```python
queue = deque()

queue.append(x)         # O(1) - enqueue
queue.popleft()         # O(1) - dequeue
queue[0]                # O(1) - peek
len(queue)              # O(1) - size
```

### Space Complexity: O(n)
Where n is the number of elements in the queue.

---

## 8. Queue Problems

### Easy:
- Implement queue from scratch
- Reverse a queue
- Generate binary numbers

### Medium:
- Sliding window maximum (with deque)
- Rotting oranges (BFS)
- Perfect squares (BFS)

### Hard:
- Number of islands (BFS)
- Shortest path in matrix
- Word ladder (BFS)

---

## 9. Deque (Double-Ended Queue)

A **deque** allows insertion and removal at both ends.

```python
from collections import deque

dq = deque()

# Add to both ends
dq.append(5)           # Add to right
dq.appendleft(1)       # Add to left

# Remove from both ends
dq.pop()               # Remove from right
dq.popleft()           # Remove from left

# Access both ends
dq[0]                  # Left end
dq[-1]                 # Right end
```

### Applications:
- Sliding window problems
- Palindrome checking
- Undo/Redo with bounds
- Circular queue implementation

---

## 10. Common Patterns

### Pattern 1: Process Level by Level
```python
queue = deque([root])
level = 0

while queue:
    size = len(queue)      # Current level size
    level_items = []
    
    for _ in range(size):  # Process all items at this level
        node = queue.popleft()
        level_items.append(node)
        
        # Add children for next level
        for child in node.children:
            queue.append(child)
    
    # Process level_items
    level += 1
```

### Pattern 2: BFS Shortest Path
```python
queue = deque([(start, 0)])    # (node, distance)
visited = {start}

while queue:
    node, dist = queue.popleft()
    
    if node == target:
        return dist
    
    for neighbor in node.neighbors:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append((neighbor, dist + 1))

return -1  # Not found
```

### Pattern 3: Rotting Oranges (Time-based BFS)
```python
queue = deque()
fresh_count = 0

# Initialize: add all rotten oranges
for i in range(m):
    for j in range(n):
        if grid[i][j] == 2:
            queue.append((i, j, 0))  # Include time
        elif grid[i][j] == 1:
            fresh_count += 1

# BFS with time tracking
max_time = 0
while queue and fresh_count:
    x, y, time = queue.popleft()
    max_time = time
    
    for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
            grid[nx][ny] = 2
            fresh_count -= 1
            queue.append((nx, ny, time + 1))

return max_time if fresh_count == 0 else -1
```

---

## 11. Key Takeaways

✅ **Queue**: FIFO data structure  
✅ **Operations**: O(1) for enqueue, dequeue, peek  
✅ **Use deque**: Always use deque, never list.pop(0)  
✅ **BFS**: Queues enable level-by-level traversal  
✅ **Circular**: Reuse space efficiently  
✅ **Deque**: Double-ended for flexibility  
✅ **Common**: Scheduling, messaging, graph traversal  

---

## 12. Tips & Common Mistakes

### Do's ✅
- Use `deque` from collections
- Track visited nodes in BFS
- Process level by level carefully
- Return -1 if element not found

### Don'ts ❌
- Use `list.pop(0)` - it's O(n)!
- Forget visited set (infinite loops)
- Mix up queue and stack order
- Forget boundaries in BFS

Next: See practical queue implementations and real problems!
