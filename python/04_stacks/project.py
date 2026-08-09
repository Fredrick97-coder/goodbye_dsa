"""
Project: Expression Parser & Calculator

Build a practical tool that:
1. Validates expressions (parentheses, brackets)
2. Converts infix to postfix (Shunting Yard algorithm)
3. Evaluates expressions
4. Provides error handling and detailed output

This project applies:
- Basic stack operations
- Expression parsing
- Operator precedence
- Algorithm implementation
"""

from collections import deque
from typing import List, Tuple
import re

print("=" * 70)
print("PROJECT: Expression Parser & Calculator")
print("=" * 70)

# ==================== PART 1: Expression Validation ====================
print("\n[PART 1] Validate Expression Syntax")
print("-" * 70)

class ExpressionValidator:
    """Validate mathematical expressions"""

    def __init__(self):
        self.pairs = {'(': ')', '[': ']', '{': '}'}
        self.errors = []

    def validate(self, expression: str) -> Tuple[bool, List[str]]:
        """Validate parentheses and brackets"""
        self.errors = []
        stack = deque()

        for i, char in enumerate(expression):
            if char in self.pairs:  # Opening bracket
                stack.append((char, i))

            elif char in self.pairs.values():  # Closing bracket
                if not stack:
                    self.errors.append(
                        f"Unexpected closing '{char}' at position {i}"
                    )
                else:
                    opening, opening_pos = stack.pop()
                    if self.pairs[opening] != char:
                        self.errors.append(
                            f"Mismatched: '{opening}' at {opening_pos} "
                            f"and '{char}' at {i}"
                        )

        # Check for unclosed brackets
        for opening, pos in stack:
            self.errors.append(f"Unclosed '{opening}' at position {pos}")

        return len(self.errors) == 0, self.errors

# Test validator
validator = ExpressionValidator()

test_expressions = [
    "(())",
    "([{}])",
    "([)]",
    "{[}",
    "(((",
    ")))",
]

print("Testing Expression Validation:\n")
for expr in test_expressions:
    valid, errors = validator.validate(expr)
    status = "✓ VALID" if valid else "✗ INVALID"
    print(f"  {expr:<15} → {status}")
    if errors:
        for error in errors:
            print(f"      Error: {error}")

print("→ Time: O(n), Space: O(n)")

# ==================== PART 2: Infix to Postfix Conversion ====================
print("\n[PART 2] Convert Infix to Postfix (Shunting Yard Algorithm)")
print("-" * 70)

class InfixToPostfixConverter:
    """Convert infix notation to postfix notation"""

    def __init__(self):
        # Operator precedence (higher = evaluated first)
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        # Associativity: 'L' = left, 'R' = right
        self.associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}

    def convert(self, infix: str) -> str:
        """Convert infix expression to postfix (RPN)

        Algorithm (Shunting Yard by Dijkstra):
        1. Scan tokens left to right
        2. Operands → output
        3. Operators → stack (consider precedence)
        4. Left paren → stack
        5. Right paren → pop to output until left paren
        """
        tokens = self._tokenize(infix)
        output = []
        operator_stack = deque()

        for token in tokens:
            # Operand
            if self._is_operand(token):
                output.append(token)

            # Operator
            elif token in self.precedence:
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in self.precedence and
                       self._should_pop(token, operator_stack[-1])):
                    output.append(operator_stack.pop())

                operator_stack.append(token)

            # Left parenthesis
            elif token == '(':
                operator_stack.append(token)

            # Right parenthesis
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())

                if operator_stack:
                    operator_stack.pop()  # Remove '('

        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())

        return ' '.join(output)

    def _tokenize(self, expression: str) -> List[str]:
        """Split expression into tokens"""
        # Remove spaces and split into tokens
        tokens = []
        current_num = ""

        for char in expression.replace(" ", ""):
            if char.isdigit() or char == '.':
                current_num += char
            else:
                if current_num:
                    tokens.append(current_num)
                    current_num = ""
                tokens.append(char)

        if current_num:
            tokens.append(current_num)

        return tokens

    def _is_operand(self, token: str) -> bool:
        """Check if token is a number"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _should_pop(self, current_op: str, stack_op: str) -> bool:
        """Decide if operator on stack should be popped"""
        if self.precedence[stack_op] > self.precedence[current_op]:
            return True
        elif self.precedence[stack_op] == self.precedence[current_op]:
            return self.associativity[current_op] == 'L'
        return False

# Test converter
converter = InfixToPostfixConverter()

infix_expressions = [
    "1 + 2",
    "1 + 2 * 3",
    "(1 + 2) * 3",
    "1 + 2 * 3 - 4",
    "((5 + 3) * 2) / (4 - 1)",
]

print("Converting Infix to Postfix:\n")
for infix in infix_expressions:
    postfix = converter.convert(infix)
    print(f"  Infix:   {infix:<20} → Postfix: {postfix}")

print("\n→ Shunting Yard Algorithm: O(n) time, O(n) space")

# ==================== PART 3: Postfix Expression Evaluation ====================
print("\n[PART 3] Evaluate Postfix Expressions")
print("-" * 70)

class PostfixEvaluator:
    """Evaluate postfix (RPN) expressions"""

    def evaluate(self, postfix: str) -> float:
        """Evaluate postfix expression

        Algorithm:
        1. Scan tokens left to right
        2. Operands → push to stack
        3. Operators → pop two operands, apply, push result
        4. Final result is top of stack
        """
        stack = deque()
        tokens = postfix.split()

        for token in tokens:
            if self._is_operand(token):
                stack.append(float(token))
            else:
                # Pop two operands (order matters for - and /)
                operand2 = stack.pop()
                operand1 = stack.pop()

                result = self._apply_operator(operand1, operand2, token)
                stack.append(result)

        return stack[0] if stack else 0

    def _is_operand(self, token: str) -> bool:
        """Check if token is a number"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _apply_operator(self, a: float, b: float, op: str) -> float:
        """Apply operator"""
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a / b if b != 0 else float('inf')
        elif op == '^':
            return a ** b
        return 0

# Test evaluator
evaluator = PostfixEvaluator()

postfix_expressions = [
    "5 3 +",              # 8
    "5 3 + 2 *",          # 16
    "5 3 + 2 / 1 -",      # 3
    "10 5 / 3 +",         # 5
    "2 3 ^ 4 +",          # 12 (2^3 + 4)
]

print("Evaluating Postfix Expressions:\n")
for postfix in postfix_expressions:
    result = evaluator.evaluate(postfix)
    print(f"  {postfix:<20} = {result}")

print("\n→ Postfix Evaluation: O(n) time, O(n) space")

# ==================== PART 4: Complete Expression Calculator ====================
print("\n[PART 4] Complete Expression Calculator")
print("-" * 70)

class ExpressionCalculator:
    """Complete calculator: validate → convert → evaluate"""

    def __init__(self):
        self.validator = ExpressionValidator()
        self.converter = InfixToPostfixConverter()
        self.evaluator = PostfixEvaluator()

    def calculate(self, expression: str) -> Tuple[bool, float, str]:
        """Calculate expression result"""
        # Validate
        valid, errors = self.validator.validate(expression)
        if not valid:
            return False, 0, "; ".join(errors)

        try:
            # Convert to postfix
            postfix = self.converter.convert(expression)

            # Evaluate
            result = self.evaluator.evaluate(postfix)

            return True, result, f"Postfix: {postfix}"

        except Exception as e:
            return False, 0, str(e)

# Test calculator
calculator = ExpressionCalculator()

test_expressions = [
    "1 + 2",
    "1 + 2 * 3",
    "(1 + 2) * 3",
    "10 / 2 + 3",
    "((5 + 3) * 2) / (4 - 1)",
    "(1 + 2",  # Invalid
    "1 + 2 * 3 / 4",
]

print("Complete Expression Calculator:\n")
for expr in test_expressions:
    valid, result, info = calculator.calculate(expr)

    if valid:
        print(f"  Expression: {expr:<25}")
        print(f"    ✓ Result: {result}")
        print(f"    {info}\n")
    else:
        print(f"  Expression: {expr:<25}")
        print(f"    ✗ Error: {info}\n")

# ==================== PART 5: Browser Back Button Simulation ====================
print("\n[PART 5] Browser Navigation History")
print("-" * 70)

class BrowserHistory:
    """Simulate browser back/forward navigation"""

    def __init__(self):
        self.history = deque()
        self.forward_stack = deque()
        self.current = None

    def visit(self, url: str):
        """Visit a new URL"""
        if self.current:
            self.history.append(self.current)

        self.current = url
        self.forward_stack.clear()  # Clear forward history on new visit

    def back(self) -> str:
        """Go back to previous URL"""
        if self.history:
            self.forward_stack.append(self.current)
            self.current = self.history.pop()
            return self.current
        return None

    def forward(self) -> str:
        """Go forward to next URL"""
        if self.forward_stack:
            self.history.append(self.current)
            self.current = self.forward_stack.pop()
            return self.current
        return None

    def get_current(self) -> str:
        return self.current

# Test browser
browser = BrowserHistory()

print("Browser Navigation Simulation:\n")

urls = ["google.com", "github.com", "stackoverflow.com", "linkedin.com"]

for url in urls:
    browser.visit(url)
    print(f"Visit: {url}")

print(f"Current: {browser.get_current()}\n")

print("Go back:")
print(f"  {browser.back()}")
print(f"  {browser.back()}")
print(f"Current: {browser.get_current()}\n")

print("Visit new URL:")
browser.visit("twitter.com")
print(f"  Visit: twitter.com")
print(f"Current: {browser.get_current()}\n")

print("Go forward (cleared by new visit):")
result = browser.forward()
print(f"  Result: {result} (None because forward history was cleared)\n")

# ==================== PART 6: Performance Comparison ====================
print("\n[PART 6] Algorithm Performance Analysis")
print("-" * 70)

import time

def benchmark_validation(expression: str, iterations: int):
    """Benchmark validation"""
    validator = ExpressionValidator()
    start = time.time()

    for _ in range(iterations):
        validator.validate(expression)

    return (time.time() - start) * 1000

# Complex expression
complex_expr = "(" * 100 + "1" + ")" * 100

iterations = 1000
time_ms = benchmark_validation(complex_expr, iterations)

print(f"Validation Performance:")
print(f"  Expression depth: 100 levels of nesting")
print(f"  Iterations: {iterations:,}")
print(f"  Total time: {time_ms:.2f} ms")
print(f"  Per expression: {time_ms/iterations:.4f} ms")
print(f"  → Linear O(n) algorithm handles large expressions quickly")

# ==================== PART 7: Error Handling ====================
print("\n[PART 7] Comprehensive Error Handling")
print("-" * 70)

error_test_cases = [
    ("(()", "Unclosed parenthesis"),
    ("())", "Extra closing parenthesis"),
    ("([)]", "Mismatched brackets"),
    ("{[}]", "Incorrectly nested"),
    ("", "Empty expression"),
]

print("Error Detection Examples:\n")

for expr, description in error_test_cases:
    valid, errors = validator.validate(expr)
    print(f"  {description}:")
    print(f"    Expression: '{expr}'")
    if valid:
        print(f"    Status: ✓ Valid")
    else:
        print(f"    Status: ✗ Invalid")
        for error in errors:
            print(f"      • {error}")
    print()

# ==================== PART 8: Summary ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Topics Covered:

1. Expression Validation
   - Check matching parentheses/brackets
   - Detect mismatches and unclosed brackets
   - Detailed error reporting
   - Complexity: O(n) time, O(n) space

2. Infix to Postfix Conversion (Shunting Yard)
   - Convert human-readable infix to RPN
   - Handle operator precedence correctly
   - Respect associativity rules
   - Complexity: O(n) time, O(n) space

3. Postfix Expression Evaluation
   - Simple stack-based algorithm
   - Direct result without parentheses
   - More efficient than evaluating infix
   - Complexity: O(n) time, O(n) space

4. Complete Calculator Pipeline
   - Validate → Convert → Evaluate
   - Error handling at each stage
   - Detailed output for debugging

5. Real-World Application
   - Browser navigation with back/forward
   - Practical stack usage
   - State management

6. Performance Analysis
   - All algorithms linear O(n)
   - Stack operations critical for efficiency
   - Handles deep nesting gracefully

Key Algorithms:

✓ Stack-based validation
✓ Shunting Yard (Dijkstra) algorithm
✓ Postfix evaluation
✓ Precedence and associativity handling

Real-World Applications:

1. **Compilers** - Parse and evaluate expressions
2. **Calculators** - Scientific and financial
3. **Browsers** - Navigation history
4. **Undo/Redo** - Text editors
5. **Function calls** - Program execution stack

Learning Points:

✓ Stacks enable efficient parsing
✓ Operator precedence is important
✓ Converting between notations is useful
✓ Validation prevents runtime errors
✓ Linear algorithms are scalable

Performance Metrics:

All major operations: O(n) time complexity
All use O(n) extra space for stack
Linear scaling means:
  - 1,000 tokens: ~1ms
  - 100,000 tokens: ~100ms
  - 1,000,000 tokens: ~1000ms

Next Steps:
1. Try different operators (mod, power, etc.)
2. Add support for decimal numbers
3. Implement variable support (e.g., "x + 5")
4. Build a full calculator UI
5. Move to Topic 05: Queues
""")

print("=" * 70)
print("Project Complete! Topic 04 Finished Successfully!")
print("=" * 70)
