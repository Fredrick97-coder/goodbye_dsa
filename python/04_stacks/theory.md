# Stacks - Last In, First Out (LIFO)

A stack is a linear data structure where elements are added and removed from the same end (top).

---

## 1. What is a Stack?

A **stack** follows the **LIFO principle** (Last-In-First-Out):
- Last element added is the first one removed
- Like a stack of plates: add to top, remove from top

### Real-world examples:
- Browser back button (undo stack)
- Function call stack in programming
- Expression evaluation (parentheses matching)
- Undo/Redo in text editors

---

## 2. Stack Operations

| Operation | Time | Description |
|-----------|------|-------------|
| **push(x)** | O(1) | Add element to top |
| **pop()** | O(1) | Remove and return top element |
| **peek()** / **top()** | O(1) | View top element without removing |
| **isEmpty()** | O(1) | Check if stack is empty |
| **size()** | O(1) | Get number of elements |

### Visual Representation:
```
Push 1, 2, 3

     ___
    | 3 |  ← top (push/pop here)
    | 2 |
    | 1 |
    |___|

Pop removes 3, then 2, then 1
```

---

## 3. Implementation

### Using Python List
```python
stack = []
stack.append(10)      # push - O(1)
stack.pop()           # pop - O(1)
stack[-1]             # peek - O(1)
len(stack) == 0       # isEmpty - O(1)
```

### Using collections.deque (Better for performance)
```python
from collections import deque
stack = deque()
stack.append(10)      # push - O(1)
stack.pop()           # pop - O(1)
stack[-1]             # peek - O(1)
```

### Custom Stack Class
```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

---

## 4. Common Stack Problems

### Problem 1: Valid Parentheses
**Goal**: Check if parentheses are balanced
```
"()" → Valid
"(())" → Valid
"([{}])" → Valid
"([)]" → Invalid (wrong order)

Solution: Push opening brackets, pop when finding closing
```

### Problem 2: Reverse String
```
"hello" → "olleh"

Solution: Push all characters, pop to reverse
```

### Problem 3: Expression Evaluation
```
Infix:   1 + 2 * 3
Postfix: 1 2 3 * +

Use stack for postfix evaluation
```

---

## 5. Stack Applications

### 1. **Function Call Stack**
```
main() calls func1()
  func1() calls func2()
    func2() executes
  func1() resumes
main() resumes

Stack: [main, func1, func2] → [main, func1] → [main]
```

### 2. **Expression Parsing**
- Checking balanced parentheses
- Converting infix to postfix
- Evaluating postfix expressions

### 3. **Undo/Redo**
```
User actions: Type A → Type B → Type C
Undo stack: [A, B, C]
Pop → Undo C
Pop → Undo B
```

### 4. **Browser History**
- Back button uses stack
- Each visited page pushed
- Back pops from stack

### 5. **Depth-First Search (DFS)**
- Traversing trees/graphs
- Stack-based iteration

---

## 6. Stack vs Queue

| Feature | Stack | Queue |
|---------|-------|-------|
| Order | LIFO | FIFO |
| Insert | Top | Rear |
| Remove | Top | Front |
| Use case | Undo, parsing | Scheduling, BFS |

---

## 7. Complexity Analysis

```python
# All operations are O(1)
stack = deque()

stack.append(x)      # O(1) - push
stack.pop()          # O(1) - pop
stack[-1]            # O(1) - peek
len(stack)           # O(1) - size
```

**Space Complexity**: O(n) where n is number of elements

---

## 8. Practice Problems

**Easy**:
- Valid parentheses
- Reverse string using stack

**Medium**:
- Next greater element
- Daily temperatures
- Min stack (track minimum)

**Hard**:
- Largest rectangle in histogram
- Trapping rain water
- Expression evaluation

---

## 9. Tips and Pitfalls

✓ **DO**:
- Use deque for better performance
- Handle empty stack exceptions
- Peek before pop to avoid errors
- Use stacks for recursive problems

✗ **DON'T**:
- Use list insert(0) with stacks (O(n))
- Forget to check if stack is empty
- Confuse with queue (different order)

---

## Key Takeaways

✅ **Stack**: LIFO data structure  
✅ **Operations**: O(1) for push, pop, peek  
✅ **Use**: Parsing, undo, function calls, DFS  
✅ **Python**: Use deque from collections  
✅ **Common**: Parenthesis matching is classic  

Next: Learn about Queues (Topic 05)
