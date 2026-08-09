"""
Exercises: Stacks - Last In, First Out (LIFO)

Practice stack operations, implementations, and solving problems with stacks.
Solve these problems and identify the time/space complexity of your solution.
"""

from typing import List, Optional
from collections import deque

print("=" * 60)
print("EXERCISES: Stacks")
print("=" * 60)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

# EASY 1: Implement Basic Stack
print("\n1. IMPLEMENT STACK CLASS")
print("Problem: Create a Stack class with push, pop, peek, isEmpty")
print("""
Methods needed:
- push(x): Add element to top
- pop(): Remove and return top element
- peek(): View top without removing
- isEmpty(): Check if empty
- size(): Get number of elements
""")
print("\nWrite your solution:")

class Stack:
    """Stack implementation"""

    def __init__(self):
        self.items = []

    def push(self, item):
        # TODO: Implement
        pass

    def pop(self):
        # TODO: Implement
        pass

    def peek(self):
        # TODO: Implement
        pass

    def isEmpty(self):
        # TODO: Implement
        pass

    def size(self):
        # TODO: Implement
        pass

# EASY 2: Valid Parentheses
print("\n2. VALID PARENTHESES")
print("Problem: Check if parentheses are balanced")
print("Input: '({[]})'")
print("Output: True")
print("Input: '([)]'")
print("Output: False")
print("\nWrite your solution:")

def is_valid_parentheses(s: str) -> bool:
    """Check if parentheses are balanced"""
    # TODO: Write your code here
    # Hint: Use stack to match opening and closing brackets
    pass

# EASY 3: Reverse String
print("\n3. REVERSE STRING")
print("Problem: Reverse a string using stack")
print("Input: 'hello'")
print("Output: 'olleh'")
print("\nWrite your solution:")

def reverse_string(s: str) -> str:
    """Reverse string using stack"""
    # TODO: Write your code here
    pass

# EASY 4: Next Greater Element
print("\n4. NEXT GREATER ELEMENT")
print("Problem: For each element, find the next greater element")
print("Input: [1, 3, 2, 4]")
print("Output: [3, 4, 4, -1]")
print("Explanation:")
print("  1 → next greater = 3")
print("  3 → next greater = 4")
print("  2 → next greater = 4")
print("  4 → no next greater = -1")
print("\nWrite your solution:")

def next_greater_element(arr: List[int]) -> List[int]:
    """Find next greater element for each position"""
    # TODO: Write your code here
    # Hint: Scan from right, use stack to track potential candidates
    # Time: O(n), Space: O(n)
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

# MEDIUM 1: Decimal to Binary
print("\n5. DECIMAL TO BINARY")
print("Problem: Convert decimal number to binary using stack")
print("Input: 10")
print("Output: '1010'")
print("\nWrite your solution:")

def decimal_to_binary(num: int) -> str:
    """Convert decimal to binary"""
    # TODO: Write your code here
    # Hint: Repeatedly divide by 2, collect remainders in stack
    pass

# MEDIUM 2: Simple Parentheses Removal
print("\n6. REMOVE OUTERMOST PARENTHESES")
print("Problem: Remove outermost layer of parentheses")
print("Input: '(()())(())'")
print("Output: '()()()' ")
print("Input: '(()())(())(()(()))'")
print("Output: '()()()()(())'")
print("\nWrite your solution:")

def remove_outermost_parentheses(s: str) -> str:
    """Remove outermost parentheses from each primitive valid string"""
    # TODO: Write your code here
    # Hint: Track depth of nesting
    pass

# MEDIUM 3: Postfix Expression
print("\n7. EVALUATE POSTFIX EXPRESSION")
print("Problem: Evaluate postfix (Reverse Polish Notation) expression")
print("Input: '5 3 +'")
print("Output: 8")
print("Input: '5 3 + 2 *'")
print("Output: 16")
print("\nWrite your solution:")

def evaluate_postfix(expression: str) -> float:
    """Evaluate postfix expression"""
    # TODO: Write your code here
    # Example: tokens = ['5', '3', '+'] → push 5, push 3, pop both and add
    # Time: O(n), Space: O(n)
    pass

# MEDIUM 4: Min Stack
print("\n8. MIN STACK")
print("Problem: Stack that returns minimum in O(1)")
print("""
Stack operations:
- push(x): Add element
- pop(): Remove top
- top(): Return top
- getMin(): Return minimum element in O(1)

Example:
  push(3), push(2), push(1)
  getMin() → 1
  pop()
  getMin() → 2
""")
print("\nWrite your solution:")

class MinStack:
    """Stack that tracks minimum element"""

    def __init__(self):
        self.stack = []
        # TODO: Add another data structure to track minimums

    def push(self, x: int):
        # TODO: Add element and update minimum
        pass

    def pop(self):
        # TODO: Remove top element
        pass

    def top(self):
        # TODO: Return top element
        pass

    def getMin(self):
        # TODO: Return minimum in O(1)
        pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

# HARD 1: Largest Rectangle in Histogram
print("\n9. LARGEST RECTANGLE IN HISTOGRAM")
print("Problem: Find area of largest rectangle in histogram")
print("Input: [2, 1, 5, 6, 2, 3]")
print("Output: 10 (height 5, width 2)")
print("""
Visual:
      ___
     |   |
  ___|   |___
 |   |   |   | ___
 | _ | _ | _ | _ |
 |2|1|5|6|2|3|
""")
print("Hint: Use stack to track indices of increasing heights")
print("\nWrite your solution:")

def largest_rectangle_histogram(heights: List[int]) -> int:
    """Find largest rectangle area in histogram"""
    # TODO: Write your code here
    # Time: O(n), Space: O(n)
    # Hint: Use stack with indices, pop when current < stack top
    pass

# HARD 2: Trapping Rain Water
print("\n10. TRAPPING RAIN WATER")
print("Problem: Calculate water trapped between elevation bars")
print("Input: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]")
print("Output: 6")
print("""
Visual:
        |
    |   |
|   | | | | |
|_|_|_|_|_|_|
""")
print("\nWrite your solution:")

def trap_rain_water(height: List[int]) -> int:
    """Calculate trapped water"""
    # TODO: Write your code here
    # Note: Can solve with stack or two-pointer
    # For this exercise, try stack approach
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

# CHALLENGE 1: Daily Temperatures
print("\n11. DAILY TEMPERATURES")
print("Problem: For each day, find days until warmer temperature")
print("Input: [73, 74, 75, 71, 69, 72, 76, 73]")
print("Output: [1, 1, 4, 2, 1, 1, 0, 0]")
print("Explanation:")
print("  Day 0 (73°): tomorrow (74°) is warmer → 1 day")
print("  Day 1 (74°): day 2 (75°) is warmer → 1 day")
print("  Day 2 (75°): day 5 (76°) is warmer → 4 days")
print("  Day 7 (73°): no warmer day → 0")
print("\nWrite your solution:")

def daily_temperatures(temperatures: List[int]) -> List[int]:
    """Find days until warmer temperature"""
    # TODO: Write your code here
    # Time: O(n), Space: O(n)
    # Hint: Scan from right to left, maintain stack of indices
    pass

# CHALLENGE 2: Implement Calculator
print("\n12. SIMPLE CALCULATOR")
print("Problem: Evaluate expression with +, -, *, / operators")
print("Input: '2-1+2'")
print("Output: 3")
print("Input: ' 6/2 '")
print("Output: 3")
print("Constraints:")
print("  - No parentheses")
print("  - * and / have higher precedence than + and -")
print("  - Evaluate left to right for same precedence")
print("\nWrite your solution:")

def calculate(s: str) -> int:
    """Calculate expression result"""
    # TODO: Write your code here
    # Time: O(n), Space: O(n)
    # Hint: Use stack to handle operators with precedence
    pass

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Stack Concepts Mastered:
1. LIFO (Last-In-First-Out) principle
2. Basic operations: push, pop, peek in O(1)
3. Matching problems (parentheses, brackets)
4. Monotonic stack for "next greater" problems
5. Using stack for expression evaluation
6. Real-world applications (undo/redo, function calls)

Key Problems:
- Valid parentheses → Check matching
- Next greater element → Monotonic stack
- Largest rectangle → Stack with indices
- Postfix evaluation → Direct stack application

Common Patterns:
1. **Matching**: Use stack to match pairs
2. **Monotonic Stack**: Find next/previous extreme
3. **Expression**: Convert to postfix or evaluate directly
4. **Track Min/Max**: Maintain auxiliary stack

Time Complexities:
- Most problems: O(n) with O(n) space
- Usually scan array once, process each element once

Tips:
✓ Use deque instead of list for better performance
✓ Monotonic stacks are powerful (harder to learn)
✓ Think about what elements you need to "remember"
✓ Test with edge cases (empty, single element)

Next: Complete the project and move to Topic 05 (Queues)
""")
