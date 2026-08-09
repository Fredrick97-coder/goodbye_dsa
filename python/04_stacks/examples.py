"""
Examples: Stacks - Last In, First Out (LIFO)

Demonstrates stack operations, implementations, and common applications.
"""

from collections import deque
from typing import List, Optional

print("=" * 60)
print("STACKS - PRACTICAL EXAMPLES")
print("=" * 60)

# ==================== (1) Basic Stack using List ====================
print("\n[1] Basic Stack Using Python List")
print("-" * 40)

stack = []

# Push (append to end) - O(1)
stack.append(10)
stack.append(20)
stack.append(30)
print(f"After pushing 10, 20, 30: {stack}")

# Peek (look at top) - O(1)
print(f"Top element (peek): {stack[-1]}")

# Pop (remove from end) - O(1)
popped = stack.pop()
print(f"Popped element: {popped}")
print(f"Stack after pop: {stack}")

# Check if empty
print(f"Is empty: {len(stack) == 0}")
print(f"Stack size: {len(stack)}")

# ==================== (2) Better Stack using deque ====================
print("\n[2] Stack Using collections.deque (Better Performance)")
print("-" * 40)

from collections import deque

stack = deque()

# Push - O(1)
stack.append(100)
stack.append(200)
stack.append(300)
print(f"After pushing: {list(stack)}")

# Peek - O(1)
print(f"Top element: {stack[-1]}")

# Pop - O(1)
print(f"Popped: {stack.pop()}")
print(f"Stack: {list(stack)}")

print("→ deque is better than list for stack (O(1) operations)")

# ==================== (3) Custom Stack Class ====================
print("\n[3] Custom Stack Class")
print("-" * 40)

class Stack:
    """Simple Stack implementation"""

    def __init__(self):
        self.items = deque()

    def push(self, item):
        """Add item to top of stack - O(1)"""
        self.items.append(item)

    def pop(self):
        """Remove and return top item - O(1)"""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """View top item without removing - O(1)"""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """Check if stack is empty - O(1)"""
        return len(self.items) == 0

    def size(self):
        """Get number of items - O(1)"""
        return len(self.items)

    def __repr__(self):
        return f"Stack({list(self.items)})"

stack = Stack()
stack.push(5)
stack.push(10)
stack.push(15)

print(f"Stack: {stack}")
print(f"Peek: {stack.peek()}")
print(f"Pop: {stack.pop()}")
print(f"Size: {stack.size()}")
print(f"Is empty: {stack.is_empty()}")

# ==================== (4) Valid Parentheses ====================
print("\n[4] Valid Parentheses Check")
print("-" * 40)

def is_valid_parentheses(s: str) -> bool:
    """Check if parentheses are balanced"""
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}

    for char in s:
        if char in pairs:  # Opening bracket
            stack.append(char)
        elif char in pairs.values():  # Closing bracket
            if not stack or pairs[stack.pop()] != char:
                return False

    return len(stack) == 0

test_cases = [
    "()",
    "()[]{}",
    "([{}])",
    "([)]",
    "{[}",
    "",
    "(",
]

print("Testing valid parentheses:")
for test in test_cases:
    result = is_valid_parentheses(test)
    status = "✓" if result else "✗"
    print(f"  '{test}' → {result} {status}")

print("→ Time: O(n), Space: O(n)")

# ==================== (5) Reverse String ====================
print("\n[5] Reverse String Using Stack")
print("-" * 40)

def reverse_string(s: str) -> str:
    """Reverse a string using stack"""
    stack = list(s)
    reversed_str = ""

    while stack:
        reversed_str += stack.pop()

    return reversed_str

original = "hello"
reversed_str = reverse_string(original)
print(f"Original: {original}")
print(f"Reversed: {reversed_str}")
print("→ Push all chars, pop in reverse order")

# ==================== (6) Reverse Number ====================
print("\n[6] Reverse Number Using Stack")
print("-" * 40)

def reverse_number(num: int) -> int:
    """Reverse digits of a number"""
    stack = []
    is_negative = num < 0
    num = abs(num)

    # Push all digits
    while num > 0:
        stack.append(num % 10)
        num //= 10

    # Pop and rebuild
    result = 0
    while stack:
        result = result * 10 + stack.pop()

    return -result if is_negative else result

num = 12345
result = reverse_number(num)
print(f"Original: {num}")
print(f"Reversed: {result}")

# ==================== (7) Stack Overflow Example ====================
print("\n[7] Understanding Stack Size Limits")
print("-" * 40)

def demonstrate_stack_depth():
    """Show how recursion uses stack"""
    stack = Stack()

    # Add 100 items
    for i in range(100):
        stack.push(i)

    print(f"Added 100 items")
    print(f"Stack size: {stack.size()}")
    print(f"Top 5 items (after popping): {[stack.pop() for _ in range(5)]}")
    print(f"Stack size now: {stack.size()}")
    print("→ Stack grows with each push, shrinks with each pop")

demonstrate_stack_depth()

# ==================== (8) Decimal to Binary ====================
print("\n[8] Convert Decimal to Binary Using Stack")
print("-" * 40)

def decimal_to_binary(num: int) -> str:
    """Convert decimal to binary"""
    stack = []

    while num > 0:
        stack.append(num % 2)
        num //= 2

    binary = ""
    while stack:
        binary += str(stack.pop())

    return binary if binary else "0"

decimal = 10
binary = decimal_to_binary(decimal)
print(f"Decimal: {decimal}")
print(f"Binary: {binary}")
print(f"Verify: {int(binary, 2)} = {decimal} ✓")

# ==================== (9) Expression Evaluation - Simple ====================
print("\n[9] Simple Expression Evaluation")
print("-" * 40)

def evaluate_postfix(expression: str) -> float:
    """Evaluate postfix expression (Reverse Polish Notation)
    Example: "5 3 +" = 8
             "5 3 + 2 *" = 16
    """
    stack = []
    operators = {'+', '-', '*', '/'}
    tokens = expression.split()

    for token in tokens:
        if token in operators:
            # Pop two operands
            b = stack.pop()
            a = stack.pop()

            # Apply operator
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b

            stack.append(result)
        else:
            # It's a number
            stack.append(float(token))

    return stack[0]

test_expr = [
    "5 3 +",           # 8
    "5 3 + 2 *",       # 16
    "10 5 /",          # 2
    "3 4 + 2 *",       # 14
]

print("Postfix Expression Evaluation:")
for expr in test_expr:
    result = evaluate_postfix(expr)
    print(f"  '{expr}' = {result}")

print("→ Postfix: no parentheses needed, evaluate left to right")

# ==================== (10) Undo/Redo System ====================
print("\n[10] Simple Undo/Redo System")
print("-" * 40)

class UndoRedoSystem:
    """Simple text editor with undo/redo"""

    def __init__(self):
        self.text = ""
        self.undo_stack = []
        self.redo_stack = []

    def type(self, char: str):
        """Type a character"""
        self.undo_stack.append(self.text)
        self.text += char
        self.redo_stack.clear()  # Clear redo on new action

    def undo(self):
        """Undo last action"""
        if self.undo_stack:
            self.redo_stack.append(self.text)
            self.text = self.undo_stack.pop()

    def redo(self):
        """Redo last undone action"""
        if self.redo_stack:
            self.undo_stack.append(self.text)
            self.text = self.redo_stack.pop()

    def get_text(self):
        return self.text if self.text else "(empty)"

editor = UndoRedoSystem()

print("Text editor undo/redo demo:")
print(f"Start: {editor.get_text()}")

editor.type('H')
print(f"Type 'H': {editor.get_text()}")

editor.type('i')
print(f"Type 'i': {editor.get_text()}")

editor.type('!')
print(f"Type '!': {editor.get_text()}")

editor.undo()
print(f"Undo: {editor.get_text()}")

editor.undo()
print(f"Undo: {editor.get_text()}")

editor.redo()
print(f"Redo: {editor.get_text()}")

# ==================== (11) Matching Brackets ====================
print("\n[11] Find Matching Bracket Position")
print("-" * 40)

def find_matching_bracket(s: str, pos: int) -> int:
    """Find position of matching closing bracket"""
    stack = deque()
    pairs = {'(': ')', '[': ']', '{': '}'}

    for i in range(pos, len(s)):
        if s[i] in pairs:
            stack.append((s[i], i))
        elif s[i] in pairs.values():
            opening, opening_pos = stack.pop()
            if pairs[opening] == s[i] and opening_pos == pos:
                return i

    return -1

s = "((hello) world)"
opening_pos = 1
matching = find_matching_bracket(s, opening_pos)
print(f"String: {s}")
print(f"Opening bracket at position {opening_pos}")
print(f"Matching closing bracket at position {matching}")
print(f"Characters: '{s[opening_pos]}' ... '{s[matching]}'")

# ==================== (12) Complexity Analysis ====================
print("\n[12] Stack Complexity Summary")
print("-" * 40)

operations = {
    "push(x)": "O(1)",
    "pop()": "O(1)",
    "peek()": "O(1)",
    "isEmpty()": "O(1)",
    "size()": "O(1)",
}

print("Stack Operation Complexities:")
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
