"""
Project: Basic Searching Applications in Real World

Build practical systems using searching algorithms:
1. Library Book Finder
2. E-commerce Product Search
3. Version Control (find commit)
4. Real-time Autocomplete
"""

from typing import List, Tuple, Optional
import time
from bisect import bisect_left, bisect_right

print("=" * 70)
print("PROJECT: Basic Searching Applications")
print("=" * 70)

# ==================== PART 1: Library Book Finder ====================
print("\n[PART 1] Library Book Finder (Binary Search)")
print("-" * 70)

class LibraryBookFinder:
    """Find books in library using binary search"""

    def __init__(self, books: List[Tuple[str, int]]):
        """books: List of (title, isbn) sorted by isbn"""
        self.books = sorted(books, key=lambda x: x[1])

    def find_by_isbn(self, isbn: int) -> Optional[str]:
        """Find book by ISBN using binary search"""
        left, right = 0, len(self.books) - 1

        while left <= right:
            mid = (left + right) // 2
            if self.books[mid][1] == isbn:
                return self.books[mid][0]
            elif self.books[mid][1] < isbn:
                left = mid + 1
            else:
                right = mid - 1

        return None

    def find_isbn_range(self, min_isbn: int, max_isbn: int) -> List[str]:
        """Find all books in ISBN range"""
        result = []
        for title, isbn in self.books:
            if min_isbn <= isbn <= max_isbn:
                result.append(title)
        return result

    def find_insertion_position(self, isbn: int) -> int:
        """Find where to insert new book"""
        left, right = 0, len(self.books)

        while left < right:
            mid = (left + right) // 2
            if self.books[mid][1] < isbn:
                left = mid + 1
            else:
                right = mid

        return left

# Test library finder
print("Library Book Finder Demo:\n")
books = [
    ("Python Basics", 101),
    ("Advanced Python", 205),
    ("Data Structures", 150),
    ("Algorithms", 180),
    ("Web Development", 220),
]

library = LibraryBookFinder(books)

# Search by ISBN
print("Search by ISBN:")
for isbn in [150, 999, 205]:
    result = library.find_by_isbn(isbn)
    print(f"  ISBN {isbn}: {result if result else 'Not found'}")

# Find insertion position
print(f"\nInsert position for ISBN 160: {library.find_insertion_position(160)}")

print("→ Time: O(log n) for single search")
print("→ Range queries still O(n) in worst case")

# ==================== PART 2: E-commerce Product Search ====================
print("\n[PART 2] E-commerce Product Search")
print("-" * 70)

class Product:
    """Product with price for searching"""
    def __init__(self, name: str, price: float, rating: float):
        self.name = name
        self.price = price
        self.rating = rating

    def __repr__(self):
        return f"{self.name}(${self.price}, {self.rating}⭐)"

class ProductCatalog:
    """Search products by price using binary search"""

    def __init__(self, products: List[Product]):
        # Sort by price
        self.by_price = sorted(products, key=lambda p: p.price)
        # Sort by rating
        self.by_rating = sorted(products, key=lambda p: -p.rating)

    def find_by_price(self, target_price: float) -> Optional[Product]:
        """Find product by exact price"""
        left, right = 0, len(self.by_price) - 1

        while left <= right:
            mid = (left + right) // 2
            if abs(self.by_price[mid].price - target_price) < 0.01:
                return self.by_price[mid]
            elif self.by_price[mid].price < target_price:
                left = mid + 1
            else:
                right = mid - 1

        return None

    def find_in_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Find all products in price range"""
        results = []
        for product in self.by_price:
            if min_price <= product.price <= max_price:
                results.append(product)
        return results

    def find_affordable(self, budget: float) -> List[Product]:
        """Find products within budget, sorted by rating"""
        affordable = [p for p in self.by_price if p.price <= budget]
        return sorted(affordable, key=lambda p: -p.rating)

# Test product search
print("E-commerce Product Search Demo:\n")
products = [
    Product("Laptop", 999.99, 4.8),
    Product("Mouse", 29.99, 4.5),
    Product("Keyboard", 79.99, 4.6),
    Product("Monitor", 299.99, 4.7),
    Product("USB Cable", 9.99, 4.2),
]

catalog = ProductCatalog(products)

# Find by price range
print("Products $20-$100:")
for product in catalog.find_in_price_range(20, 100):
    print(f"  {product}")

# Affordable products
print(f"\nTop-rated products under $500:")
for product in catalog.find_affordable(500)[:3]:
    print(f"  {product}")

print("→ Time: O(log n) for range finding, O(n log n) with sorting")

# ==================== PART 3: Version Control (Find Commit) ====================
print("\n[PART 3] Version Control - Find First Bad Version")
print("-" * 70)

class VersionControl:
    """Find first bad version using binary search"""

    def __init__(self, bad_version: int):
        """bad_version: First version that is bad (or -1 if none)"""
        self.bad_version = bad_version

    def is_bad(self, version: int) -> bool:
        """Check if version is bad"""
        return self.bad_version >= 0 and version >= self.bad_version

    def find_first_bad(self, total_versions: int) -> int:
        """Find first bad version using binary search"""
        left, right = 1, total_versions

        while left < right:
            mid = (left + right) // 2
            if self.is_bad(mid):
                right = mid  # This version is bad, search left
            else:
                left = mid + 1  # This version is good, search right

        return left if self.is_bad(left) else -1

# Test version control
print("Version Control Demo:\n")
vc = VersionControl(bad_version=8)  # Version 8 and after are bad

result = vc.find_first_bad(20)
print(f"Total versions: 20")
print(f"First bad version: {result}")
print(f"Checked versions: ~{int(__import__('math').log2(20)) + 1} (binary search)")

# Linear search would need ~8 checks
print(f"Linear search would need: ~{vc.bad_version} checks")
print(f"Speedup: {vc.bad_version / (__import__('math').log2(20) + 1):.1f}x faster")

print("→ Time: O(log n) with binary search")
print("→ Much better than O(n) linear search")

# ==================== PART 4: Autocomplete with Prefix ====================
print("\n[PART 4] Real-time Autocomplete System")
print("-" * 70)

class AutocompleteIndex:
    """Index for fast prefix-based autocomplete"""

    def __init__(self, words: List[str]):
        self.words = sorted(set(words))

    def find_with_prefix(self, prefix: str) -> List[str]:
        """Find all words with given prefix"""
        if not prefix:
            return self.words

        # Find first word with prefix
        left = bisect_left(self.words, prefix)
        result = []

        # Add all words starting with prefix
        for word in self.words[left:]:
            if word.startswith(prefix):
                result.append(word)
            else:
                break

        return result

    def count_with_prefix(self, prefix: str) -> int:
        """Count words with prefix"""
        return len(self.find_with_prefix(prefix))

# Test autocomplete
print("Autocomplete Demo:\n")
words = [
    "apple", "application", "apply", "appreciate",
    "banana", "band", "bank",
    "car", "card", "care", "careful",
    "dog", "door", "doubt",
]

autocomplete = AutocompleteIndex(words)

prefixes = ["ap", "ba", "car", "do", "z"]
for prefix in prefixes:
    suggestions = autocomplete.find_with_prefix(prefix)
    count = autocomplete.count_with_prefix(prefix)
    print(f"  '{prefix}': {count} match(es) → {suggestions[:5]}")

print("\n→ Time: O(log n) to find first match + O(k) to get k results")
print("→ Much faster than checking every word")

# ==================== PART 5: Performance Analysis ====================
print("\n[PART 5] Search Performance Analysis")
print("-" * 70)

def benchmark_searches(size: int):
    """Compare search algorithms"""
    import random

    data = sorted(random.sample(range(size * 10), size))
    targets = random.sample(data, min(100, size // 10))

    # Linear search
    start = time.time()
    for target in targets:
        for item in data:
            if item == target:
                break
    linear_time = (time.time() - start) * 1000

    # Binary search
    start = time.time()
    for target in targets:
        left, right = 0, len(data) - 1
        while left <= right:
            mid = (left + right) // 2
            if data[mid] == target:
                break
            elif data[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
    binary_time = (time.time() - start) * 1000

    # Bisect (Python's built-in binary search)
    start = time.time()
    for target in targets:
        bisect_left(data, target)
    bisect_time = (time.time() - start) * 1000

    return linear_time, binary_time, bisect_time

print("Performance Benchmarks (100 searches):\n")
print(f"{'Size':<10} {'Linear':<12} {'Binary':<12} {'Bisect':<12} {'Speedup':<10}")
print("-" * 56)

for size in [1000, 10000, 100000]:
    linear, binary, bisect = benchmark_searches(size)
    speedup = linear / binary if binary > 0 else 0
    print(
        f"{size:<10} {linear:>6.2f}ms {'':<2} {binary:>6.2f}ms {'':<2} {bisect:>6.2f}ms {'':<2} {speedup:>6.1f}x"
    )

print("\n→ Binary search dramatically faster on large datasets")
print("→ Bisect is optimized C implementation (fastest)")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World Searching Applications:

1. Library Book Finder
   - Binary search for exact ISBN match
   - Range queries for price ranges
   - Fast insertion position finding

2. E-commerce Product Search
   - Find products by price (binary search)
   - Filter by price range
   - Sort results by rating within budget

3. Version Control
   - Find first bad version
   - Binary search with custom comparator
   - Much faster than linear approach

4. Autocomplete System
   - Fast prefix matching with binary search
   - Indexed word storage for quick lookup
   - Scales to millions of words

Key Insights:

✓ Binary search: O(log n) on sorted data
✓ Linear search: O(n) but works on any data
✓ Two-pointer: O(n) for sorted pair problems
✓ Preprocessing (sorting) enables fast queries
✓ Use binary search when data is sorted
✓ Combined with other structures (BST, hash map)

Common Real-World Uses:

- Database queries (index lookups)
- Text editors (find and replace)
- E-commerce (product filtering)
- Maps/GPS (location finding)
- Spell checkers (word suggestions)
- Version control (commit finding)
- Time series data (event lookup)
- Range queries (price, date ranges)

Performance Characteristics:

Algorithm           Time        Space    Requirements
─────────────────────────────────────────────────────
Linear Search       O(n)        O(1)     None
Binary Search       O(log n)    O(1)     Sorted
Two-Pointer         O(n)        O(1)     Sorted
Sliding Window       O(n)        O(1)     None
Index Lookup        O(log n)    O(n)     Preprocessing

Trade-offs:

- Speed vs Data Requirements: Binary needs sorted data
- Preprocessing Cost: Sort once, query fast
- Space vs Time: Index (more space, faster queries)
- Static vs Dynamic: Harder to maintain sorted data

Next Steps:
1. Master binary search variations
2. Solve LeetCode search problems
3. Learn to apply searches with other algorithms
4. Move to Topic 11: Graphs (Basics)
""")

print("=" * 70)
print("Project Complete! Topic 10 Finished Successfully!")
print("=" * 70)
