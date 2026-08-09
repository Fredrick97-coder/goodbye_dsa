"""
Exercises: Linked Lists

Practice implementing and solving linked list problems.
"""

from typing import Optional

print("=" * 60)
print("EXERCISES: Linked Lists")
print("=" * 60)

# Node class provided
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 60)

# EASY 1: Create and Print
print("\n1. CREATE AND PRINT LINKED LIST")
print("Problem: Create a linked list and print all elements")
print("Input: values [1, 2, 3, 4, 5]")
print("Output: '1 -> 2 -> 3 -> 4 -> 5 -> NULL'")
print("\nWrite your solution:")

def create_and_print_list(values):
    """Create linked list from values and return head"""
    # TODO: Write your code here
    pass

# EASY 2: Search in Linked List
print("\n2. SEARCH IN LINKED LIST")
print("Problem: Find if element exists in linked list")
print("Input: head, target=3")
print("Output: True/False")
print("\nWrite your solution:")

def search_linked_list(head: Optional[Node], target: int) -> bool:
    """Search for target in linked list"""
    # TODO: Write your code here
    pass

# EASY 3: Get Length
print("\n3. GET LENGTH OF LINKED LIST")
print("Problem: Count number of nodes")
print("Input: 1 -> 2 -> 3 -> NULL")
print("Output: 3")
print("\nWrite your solution:")

def get_length(head: Optional[Node]) -> int:
    """Get length of linked list"""
    # TODO: Write your code here
    pass

# EASY 4: Find Tail
print("\n4. FIND TAIL NODE")
print("Problem: Find the last node")
print("Input: 1 -> 2 -> 3 -> NULL")
print("Output: Node with data 3")
print("\nWrite your solution:")

def find_tail(head: Optional[Node]) -> Optional[Node]:
    """Find last node in linked list"""
    # TODO: Write your code here
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 60)

# MEDIUM 1: Reverse Linked List
print("\n5. REVERSE LINKED LIST")
print("Problem: Reverse the entire linked list")
print("Input: 1 -> 2 -> 3 -> 4 -> NULL")
print("Output: 4 -> 3 -> 2 -> 1 -> NULL")
print("Constraint: O(n) time, O(1) space")
print("\nWrite your solution:")

def reverse_linked_list(head: Optional[Node]) -> Optional[Node]:
    """Reverse linked list iteratively"""
    # TODO: Write your code here
    pass

# MEDIUM 2: Find Middle
print("\n6. FIND MIDDLE NODE")
print("Problem: Find middle of linked list")
print("Input: 1 -> 2 -> 3 -> 4 -> 5 -> NULL")
print("Output: Node with data 3 (middle)")
print("Constraint: Use two-pointer technique")
print("\nWrite your solution:")

def find_middle(head: Optional[Node]) -> Optional[Node]:
    """Find middle node using slow and fast pointers"""
    # TODO: Write your code here
    pass

# MEDIUM 3: Merge Two Sorted Lists
print("\n7. MERGE TWO SORTED LINKED LISTS")
print("Problem: Merge two sorted linked lists")
print("Input: 1 -> 3 -> 5, 2 -> 4 -> 6")
print("Output: 1 -> 2 -> 3 -> 4 -> 5 -> 6")
print("\nWrite your solution:")

def merge_sorted_lists(l1: Optional[Node], l2: Optional[Node]) -> Optional[Node]:
    """Merge two sorted linked lists"""
    # TODO: Write your code here
    pass

# MEDIUM 4: Remove Element
print("\n8. REMOVE ELEMENT FROM LINKED LIST")
print("Problem: Remove all nodes with specific value")
print("Input: 1 -> 2 -> 3 -> 2 -> 4, val=2")
print("Output: 1 -> 3 -> 4")
print("\nWrite your solution:")

def remove_element(head: Optional[Node], val: int) -> Optional[Node]:
    """Remove all nodes with given value"""
    # TODO: Write your code here
    pass

# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 60)

# HARD 1: Detect Cycle
print("\n9. DETECT CYCLE IN LINKED LIST")
print("Problem: Check if linked list has a cycle")
print("Visual: 1 -> 2 -> 3 -> 2 (cycle)")
print("Output: True")
print("Constraint: O(n) time, O(1) space (Floyd's algorithm)")
print("\nWrite your solution:")

def has_cycle(head: Optional[Node]) -> bool:
    """Detect cycle using slow and fast pointers"""
    # TODO: Write your code here
    pass

# HARD 2: Palindrome Check
print("\n10. CHECK IF LINKED LIST IS PALINDROME")
print("Problem: Check if linked list reads same forwards and backwards")
print("Input: 1 -> 2 -> 3 -> 2 -> 1 -> NULL")
print("Output: True")
print("Constraint: O(n) time")
print("\nWrite your solution:")

def is_palindrome(head: Optional[Node]) -> bool:
    """Check if linked list is palindrome"""
    # TODO: Write your code here
    # Hint: Find middle, reverse second half, compare
    pass

# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 60)

# CHALLENGE 1: Add Two Numbers
print("\n11. ADD TWO NUMBERS REPRESENTED BY LINKED LISTS")
print("Problem: Add two numbers stored in reverse linked lists")
print("Input: 2 -> 4 -> 3 (represents 342), 5 -> 6 -> 4 (represents 465)")
print("Output: 7 -> 0 -> 8 (represents 807, which is 342 + 465)")
print("\nWrite your solution:")

def add_two_numbers(l1: Optional[Node], l2: Optional[Node]) -> Optional[Node]:
    """Add two numbers represented by linked lists"""
    # TODO: Write your code here
    # Hint: Traverse both lists simultaneously with carry
    pass

# CHALLENGE 2: Reorder List
print("\n12. REORDER LINKED LIST")
print("Problem: Reorder list as L0 → Ln → L1 → Ln-1 → L2 → Ln-2...")
print("Input: 1 -> 2 -> 3 -> 4 -> 5")
print("Output: 1 -> 5 -> 2 -> 4 -> 3")
print("Constraint: O(n) time, O(1) space")
print("\nWrite your solution:")

def reorder_list(head: Optional[Node]) -> None:
    """Reorder linked list in place"""
    # TODO: Write your code here
    # Hint: Find middle, reverse second half, merge

    pass

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Linked List Concepts:
1. Node structure (data + pointer)
2. Traversal (forward and backward)
3. Operations (insert, delete, search)
4. Patterns (two pointers, dummy node, reversal)
5. Types (singly, doubly, circular)

Key Algorithms:
- Reverse linked list (iterative & recursive)
- Find middle (slow-fast pointers)
- Detect cycle (Floyd's algorithm)
- Merge sorted lists
- Palindrome check
- Add two numbers

Time Complexities:
- Access: O(n)
- Search: O(n)
- Insert/Delete at head: O(1)
- Insert/Delete at position: O(n)

Common Patterns:
1. Two pointers (find middle, cycle detection)
2. Dummy node (simplify edge cases)
3. Reversal (iterative with 3 pointers)
4. Merge (two pointer technique)

Edge Cases:
- Empty list
- Single node
- Two nodes
- Cycle in list
- List with duplicates

Next: Complete the project building real linked list applications
""")
