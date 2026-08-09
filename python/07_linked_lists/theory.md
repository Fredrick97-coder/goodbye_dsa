# Linked Lists - Dynamic Data Structures

Master linked lists and understand when to use them instead of arrays.

---

## 1. What is a Linked List?

A **linked list** is a linear data structure where elements (nodes) are connected via pointers/references.

### Key Differences from Arrays:

| Feature | Array | Linked List |
|---------|-------|-------------|
| **Access** | O(1) - direct index | O(n) - must traverse |
| **Insert** | O(n) - may shift | O(1) - if at known position |
| **Delete** | O(n) - may shift | O(1) - if at known position |
| **Space** | Contiguous memory | Non-contiguous memory |
| **Size** | Fixed | Dynamic |

### Visual Representation:
```
Array:        [10] [20] [30] [40] [50]
              (contiguous memory)

Linked List:  [10|→] [20|→] [30|→] [40|→] [50|NULL]
              (scattered memory, connected by pointers)
```

---

## 2. Node Structure

Each node contains:
- **Data**: The value stored
- **Pointer/Reference**: Link to the next node

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Points to next node
```

---

## 3. Types of Linked Lists

### Singly Linked List
- Each node points to the next node
- Unidirectional traversal
- Simplest form

```
Head → [10|→] → [20|→] → [30|→] → [40|NULL]
```

### Doubly Linked List
- Each node points to both next and previous
- Bidirectional traversal
- More memory but easier backward traversal

```
NULL ← [10|↔] ↔ [20|↔] ↔ [30|↔] ↔ [40|NULL]
```

### Circular Linked List
- Last node points back to first node
- Creates a cycle
- Useful for round-robin algorithms

```
[10|→] → [20|→] → [30|→] → [40|→]
  ↑___________________________|
```

---

## 4. Singly Linked List Operations

| Operation | Time | Description |
|-----------|------|-------------|
| **Access** | O(n) | Must traverse from head |
| **Search** | O(n) | Linear search |
| **Insert at head** | O(1) | Direct insertion |
| **Insert at position** | O(n) | Find position then insert |
| **Delete from head** | O(1) | Direct deletion |
| **Delete at position** | O(n) | Find then delete |

### Implementation:

```python
class SinglyLinkedList:
    def __init__(self):
        self.head = None
    
    def insert_at_head(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def delete_head(self):
        if self.head:
            self.head = self.head.next
    
    def search(self, target):
        current = self.head
        while current:
            if current.data == target:
                return True
            current = current.next
        return False
```

---

## 5. Traversal

### Forward Traversal:
```python
def print_list(head):
    current = head
    while current:
        print(current.data, end=" → ")
        current = current.next
    print("NULL")
```

### Reverse Traversal (Recursive):
```python
def print_reverse(node):
    if not node:
        return
    print_reverse(node.next)
    print(node.data, end=" ")
```

---

## 6. Common Linked List Problems

### Problem 1: Reverse a Linked List
```
Original: 1 → 2 → 3 → 4 → NULL
Reversed: 4 → 3 → 2 → 1 → NULL
```

Approaches:
- Iterative: O(n) time, O(1) space
- Recursive: O(n) time, O(n) space (call stack)

### Problem 2: Find Middle
```
1 → 2 → 3 → 4 → 5 → NULL
        ↑ (middle)
```

Using two pointers (slow and fast):
- Slow: moves 1 step
- Fast: moves 2 steps
- When fast reaches end, slow is at middle

### Problem 3: Detect Cycle
```
1 → 2 → 3
    ↑   ↓
    ← ← 4

Floyd's cycle detection (tortoise & hare)
```

### Problem 4: Merge Two Sorted Lists
```
List 1: 1 → 3 → 5 → NULL
List 2: 2 → 4 → 6 → NULL
Result: 1 → 2 → 3 → 4 → 5 → 6 → NULL
```

---

## 7. Doubly Linked List

### Advantages:
- Traverse both directions
- Easier deletion (have previous pointer)
- Useful for undo/redo

### Disadvantages:
- Extra space for previous pointer
- More complex operations

```python
class DNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
```

---

## 8. Complexity Comparison: Linked List vs Array

| Operation | Array | Singly LL | Doubly LL |
|-----------|-------|-----------|-----------|
| Access | O(1) | O(n) | O(n) |
| Search | O(n) | O(n) | O(n) |
| Insert at head | O(n) | O(1) | O(1) |
| Insert at end | O(1) | O(n)* | O(1)** |
| Delete head | O(n) | O(1) | O(1) |
| Delete at pos | O(n) | O(n) | O(n) |
| Space | O(n) | O(n) | O(n) |

*With tail pointer, O(1)  
**With tail pointer, O(1)

---

## 9. When to Use Linked Lists

### Use Linked Lists When:
- ✓ Frequent insertions/deletions at head
- ✓ Don't need random access
- ✓ Unknown size in advance
- ✓ Need dynamic memory

### Use Arrays When:
- ✓ Need random access O(1)
- ✓ Mostly reading, few insertions
- ✓ Memory is contiguous/faster
- ✓ Cache-friendly performance

---

## 10. Memory Layout

### Arrays:
```
Memory: [A][A][A][A][A]...
         └─ contiguous
```

### Linked Lists:
```
Memory: [N][.][.][N][.][N][.][.][.][N]...
         └─ scattered, connected by pointers
```

**Implication**: Linked lists have worse cache locality but better insertion/deletion flexibility.

---

## 11. Linked List Patterns

### Pattern 1: Two Pointers
```python
# Find middle using slow and fast pointers
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is at middle
```

### Pattern 2: Dummy Node
```python
# Simplifies head-related operations
dummy = Node(0)
dummy.next = head
current = dummy
# Now don't need special case for head
```

### Pattern 3: Reversal
```python
# Iterative reversal
prev, curr = None, head
while curr:
    next_temp = curr.next
    curr.next = prev
    prev = curr
    curr = next_temp
```

---

## 12. Key Takeaways

✅ **Linked List**: Dynamic, pointer-based data structure  
✅ **Access**: O(n) but insertion/deletion at known position is O(1)  
✅ **Types**: Singly, Doubly, Circular  
✅ **Common patterns**: Two pointers, dummy node, reversal  
✅ **When to use**: Frequent insertions/deletions  
✅ **Trade-off**: Slower access, faster modifications  

Next: See practical implementations and solve linked list problems!
