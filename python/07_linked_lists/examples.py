"""
Examples: Linked Lists - Singly, Doubly, and Circular

Demonstrates linked list operations and common patterns.
"""

from typing import Optional

print("=" * 60)
print("LINKED LISTS - PRACTICAL EXAMPLES")
print("=" * 60)

# ==================== Node Definition ====================
print("\n[0] Node Structure")
print("-" * 40)

class Node:
    """Singly linked list node"""

    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"

# Create a simple node
node = Node(10)
print(f"Created node: {node}")
print(f"Node data: {node.data}")
print(f"Node next: {node.next}")
print("→ Node contains data and pointer to next node")

# ==================== (1) Singly Linked List Basic Operations ====================
print("\n[1] Singly Linked List - Basic Operations")
print("-" * 40)

class SinglyLinkedList:
    """Singly linked list implementation"""

    def __init__(self):
        self.head = None

    def insert_at_head(self, data):
        """Insert at beginning - O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        """Insert at end - O(n)"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete_head(self):
        """Delete first node - O(1)"""
        if self.head:
            self.head = self.head.next

    def print_list(self):
        """Print all elements"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" → ".join(elements) + " → NULL")

    def search(self, target):
        """Search for element - O(n)"""
        current = self.head
        while current:
            if current.data == target:
                return True
            current = current.next
        return False

# Test operations
ll = SinglyLinkedList()
ll.insert_at_head(30)
ll.insert_at_head(20)
ll.insert_at_head(10)
print(f"After inserting 10, 20, 30 at head: ", end="")
ll.print_list()

ll.insert_at_end(40)
print(f"After inserting 40 at end: ", end="")
ll.print_list()

ll.delete_head()
print(f"After deleting head: ", end="")
ll.print_list()

print(f"Search for 20: {ll.search(20)}")
print(f"Search for 100: {ll.search(100)}")
print("→ Insertion at head: O(1), at end: O(n)")

# ==================== (2) Traverse Linked List ====================
print("\n[2] Traverse Linked List (Forward & Reverse)")
print("-" * 40)

def traverse_forward(head):
    """Print forward"""
    result = []
    current = head
    while current:
        result.append(current.data)
        current = current.next
    return result

def traverse_reverse_recursive(node, result=None):
    """Print in reverse using recursion"""
    if result is None:
        result = []
    if not node:
        return result
    traverse_reverse_recursive(node.next, result)
    result.append(node.data)
    return result

ll = SinglyLinkedList()
for val in [1, 2, 3, 4, 5]:
    ll.insert_at_end(val)

forward = traverse_forward(ll.head)
reverse = traverse_reverse_recursive(ll.head)

print(f"List: {ll}")
print(f"Forward: {forward}")
print(f"Reverse: {reverse}")
print("→ Forward O(n), Reverse O(n) with call stack")

# ==================== (3) Reverse Linked List ====================
print("\n[3] Reverse Linked List (Iterative)")
print("-" * 40)

def reverse_iterative(head):
    """Reverse linked list iteratively"""
    prev = None
    current = head

    while current:
        next_temp = current.next  # Save next
        current.next = prev       # Reverse the link
        prev = current            # Move prev
        current = next_temp       # Move current

    return prev  # New head

ll = SinglyLinkedList()
for val in [1, 2, 3, 4, 5]:
    ll.insert_at_end(val)

print(f"Original: {traverse_forward(ll.head)}")
ll.head = reverse_iterative(ll.head)
print(f"Reversed: {traverse_forward(ll.head)}")
print("→ Time: O(n), Space: O(1)")

# ==================== (4) Find Middle ====================
print("\n[4] Find Middle Using Two Pointers")
print("-" * 40)

def find_middle(head):
    """Find middle node using slow and fast pointers"""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow.data if slow else None

ll = SinglyLinkedList()
for val in [1, 2, 3, 4, 5]:
    ll.insert_at_end(val)

middle = find_middle(ll.head)
print(f"List: {traverse_forward(ll.head)}")
print(f"Middle element: {middle}")
print("→ Slow pointer: 1 step, Fast pointer: 2 steps")
print("→ Time: O(n), Space: O(1)")

# ==================== (5) Detect Cycle ====================
print("\n[5] Detect Cycle (Floyd's Algorithm)")
print("-" * 40)

def has_cycle(head):
    """Detect cycle using slow and fast pointers"""
    if not head:
        return False

    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:  # They meet = cycle exists
            return True

    return False

# List with cycle
ll_cycle = SinglyLinkedList()
ll_cycle.insert_at_head(3)
ll_cycle.insert_at_head(2)
ll_cycle.insert_at_head(1)
# Create cycle: 3 → 2 → 1 → 2 (cycle)
cycle_node = ll_cycle.head.next  # Node with 2
ll_cycle.head.next.next.next = cycle_node  # Point to cycle

print(f"List with cycle: 1 → 2 → 3 → 2 (cycle)")
print(f"Has cycle: {has_cycle(ll_cycle.head)}")

ll_normal = SinglyLinkedList()
for val in [1, 2, 3]:
    ll_normal.insert_at_end(val)
print(f"Normal list: {traverse_forward(ll_normal.head)}")
print(f"Has cycle: {has_cycle(ll_normal.head)}")
print("→ Time: O(n), Space: O(1)")

# ==================== (6) Merge Two Sorted Lists ====================
print("\n[6] Merge Two Sorted Linked Lists")
print("-" * 40)

def merge_sorted_lists(l1, l2):
    """Merge two sorted linked lists"""
    dummy = Node(0)
    current = dummy

    while l1 and l2:
        if l1.data <= l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # Attach remaining
    current.next = l1 if l1 else l2

    return dummy.next

# Create two sorted lists
ll1 = SinglyLinkedList()
for val in [1, 3, 5]:
    ll1.insert_at_end(val)

ll2 = SinglyLinkedList()
for val in [2, 4, 6]:
    ll2.insert_at_end(val)

merged_head = merge_sorted_lists(ll1.head, ll2.head)
merged = traverse_forward(merged_head)

print(f"List 1: {[1, 3, 5]}")
print(f"List 2: {[2, 4, 6]}")
print(f"Merged: {merged}")
print("→ Time: O(n + m), Space: O(1)")

# ==================== (7) Remove Duplicates ====================
print("\n[7] Remove Duplicates from Sorted List")
print("-" * 40)

def remove_duplicates(head):
    """Remove consecutive duplicates"""
    current = head

    while current and current.next:
        if current.data == current.next.data:
            current.next = current.next.next
        else:
            current = current.next

    return head

ll = SinglyLinkedList()
for val in [1, 1, 2, 2, 2, 3, 4, 4, 5]:
    ll.insert_at_end(val)

print(f"Original: {traverse_forward(ll.head)}")
remove_duplicates(ll.head)
print(f"Deduplicated: {traverse_forward(ll.head)}")
print("→ Time: O(n), Space: O(1)")

# ==================== (8) Doubly Linked List ====================
print("\n[8] Doubly Linked List")
print("-" * 40)

class DNode:
    """Doubly linked list node"""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    """Doubly linked list"""

    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = DNode(data)
        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node
        new_node.prev = current

    def print_forward(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def print_backward(self):
        result = []
        current = self.head
        if not current:
            return result

        while current.next:
            current = current.next

        while current:
            result.append(current.data)
            current = current.prev
        return result

dll = DoublyLinkedList()
for val in [1, 2, 3, 4, 5]:
    dll.insert(val)

print(f"Forward:  {dll.print_forward()}")
print(f"Backward: {dll.print_backward()}")
print("→ Traverse in both directions")
print("→ Space: O(n) extra for prev pointers")

# ==================== (9) Complexity Summary ====================
print("\n[9] Linked List Complexity Summary")
print("-" * 40)

operations = {
    "Access": "O(n)",
    "Search": "O(n)",
    "Insert at head": "O(1)",
    "Insert at end": "O(n)",
    "Delete head": "O(1)",
    "Delete at pos": "O(n)",
}

print(f"{'Operation':<20} {'Complexity':<10}")
print("-" * 30)
for op, complexity in operations.items():
    print(f"{op:<20} {complexity:<10}")

print("\nSpace: O(n) for n elements")
print("→ Trade-off: O(1) insertions/deletions vs O(n) access")

print("\n" + "=" * 60)
print("Next: Complete exercises and build linked list projects!")
print("=" * 60)
