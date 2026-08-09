# Hash Maps & Hash Tables

Master hash-based data structures for fast lookups, counting, and deduplication.

---

## 1. What is a Hash Map?

A **hash map** (hash table) is a data structure that implements an associative array—a structure that maps keys to values using a **hash function**.

### Key Concepts:
- **Key-Value Pairs**: Store data as (key → value)
- **Hash Function**: Maps key → array index in O(1)
- **Fast Lookup**: Average O(1) time for get/set/delete
- **Dynamic**: Grows as needed (rehashing)

```python
# Simple hash map
hash_map = {}
hash_map["name"] = "Alice"      # O(1) insert
value = hash_map["name"]        # O(1) lookup
del hash_map["name"]            # O(1) delete
```

---

## 2. Hash Function

A **hash function** converts a key to an array index.

### Requirements:
- **Deterministic**: Same input → same output
- **Fast**: O(1) computation
- **Uniform**: Distribute keys evenly
- **Collision-minimizing**: Few collisions

### Example:
```python
def hash_function(key, size):
    return hash(key) % size  # Map to array index 0 to size-1
```

**Problem**: Two different keys may hash to the same index (collision).

---

## 3. Collision Resolution

When two keys hash to the same index:

### Method 1: Chaining
Store collisions in a linked list at each index.

```
Index 0: [("Alice", 25)] → [("Bob", 30)] → None
Index 1: [("Charlie", 35)]
```

- Insert: O(1) average, O(n) worst case (long chain)
- Search: O(1) average, O(n) worst case
- Delete: O(1) average, O(n) worst case

### Method 2: Open Addressing
Find another empty slot using probing.

**Linear Probing**: Try next slot
```
hash(key) = 2, occupied → try 3, 4, 5...
```

**Quadratic Probing**: Try slots 2, 2+1², 2+2², ...

- Less cache-friendly than chaining
- Requires lower load factor
- Can cause clustering

---

## 4. Load Factor & Rehashing

**Load Factor** = (number of entries) / (table size)

```
Load factor = 0.5: Table is 50% full
Load factor = 0.75: Time to rehash (too many collisions)
```

### Rehashing:
When load factor exceeds threshold (typically 0.75):
1. Create larger table (usually 2x size)
2. Re-hash all entries into new table
3. Time: O(n), happens occasionally → amortized O(1) per operation

```python
# Python automatically rehashes when needed
hash_map = {}
hash_map[1] = "a"  # O(1)
hash_map[2] = "b"  # O(1) - may trigger rehash
```

---

## 5. Hash Map Operations

| Operation | Average | Worst Case | Notes |
|-----------|---------|-----------|-------|
| Insert | O(1) | O(n) | Rehash if needed |
| Search | O(1) | O(n) | Collision chain length |
| Delete | O(1) | O(n) | Remove from chain |
| Iterate | O(n) | O(n) | Visit all entries |

---

## 6. Common Hash Map Problems

### Problem 1: Two Sum
Find two numbers that add to target.
```python
# Brute force: O(n²)
# Hash map: O(n) - store seen numbers
```

### Problem 2: Anagram Group
Group anagrams together.
```python
# Use sorted string as key
key = "".join(sorted("listen"))  # "eilnst"
anagrams[key].append("listen")
```

### Problem 3: Frequency Counting
Count element occurrences.
```python
freq = {}
for num in arr:
    freq[num] = freq.get(num, 0) + 1
```

### Problem 4: Duplicate Detection
Find duplicates efficiently.
```python
seen = set()
for num in arr:
    if num in seen:
        return num
    seen.add(num)
```

---

## 7. Hash Map Patterns

### Pattern 1: Counting Frequencies
```python
from collections import Counter

freq = Counter(arr)  # Count all elements
most_common = freq.most_common(k)  # Top k
```

### Pattern 2: Complement Tracking
```python
seen = set()
for num in arr:
    complement = target - num
    if complement in seen:
        return [complement, num]
    seen.add(num)
```

### Pattern 3: Grouping
```python
groups = {}
for item in items:
    key = get_group_key(item)
    if key not in groups:
        groups[key] = []
    groups[key].append(item)
```

### Pattern 4: Caching
```python
cache = {}
def expensive_function(n):
    if n in cache:
        return cache[n]
    result = compute(n)
    cache[n] = result
    return result
```

---

## 8. Hash Map vs Other Structures

| Operation | Hash Map | Array | Linked List | BST |
|-----------|----------|-------|-------------|-----|
| Search | O(1) avg | O(n) | O(n) | O(log n) |
| Insert | O(1) avg | O(n) | O(1) | O(log n) |
| Delete | O(1) avg | O(n) | O(1) | O(log n) |
| Order | No | Yes | No | Yes |
| Space | O(n) | O(n) | O(n) | O(n) |

**Hash Map wins for**:
- ✓ Fast lookup without ordering
- ✓ Counting/frequency problems
- ✓ Deduplication
- ✓ Caching

**Others win for**:
- ✓ Ordered traversal (BST, Array)
- ✓ Range queries (BST)
- ✓ Streaming insertion (Linked List)

---

## 9. Hash Functions for Different Types

### String Hash:
```python
key = "hello"
index = hash(key) % table_size
```

### Integer Hash:
```python
key = 12345
index = key % table_size  # Simple
# Better: (key * 2654435761) % (2^32) # Knuth's constant
```

### Tuple Hash:
```python
key = (1, 2, 3)
index = hash(key) % table_size  # Python handles this
```

---

## 10. Key Takeaways

✅ **Hash Map**: Fast key-value storage O(1) average  
✅ **Hash Function**: Maps key → index deterministically  
✅ **Collision Resolution**: Chaining or open addressing  
✅ **Load Factor**: Trigger rehashing when ~75% full  
✅ **Patterns**: Counting, grouping, caching, complement tracking  
✅ **Trade-offs**: Fast lookup vs no ordering  
✅ **Worst Case**: O(n) with poor hash function or full collisions  

**Best for**: Lookups, counting, deduplication, caching  
**Not for**: Ordered data, range queries

Next: Implement hash maps and solve frequency/deduplication problems!
