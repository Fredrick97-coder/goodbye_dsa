"""
Project: Hash Map Applications in the Real World

Build practical systems using hash maps:
1. URL Shortener
2. Word Frequency Analyzer
3. Auto-complete suggestion system
4. Session manager (cache)
"""

from collections import defaultdict, Counter
from typing import List, Dict, Tuple
import time

print("=" * 70)
print("PROJECT: Hash Map Applications in the Real World")
print("=" * 70)

# ==================== PART 1: URL Shortener ====================
print("\n[PART 1] URL Shortener Service")
print("-" * 70)

class URLShortener:
    """Map long URLs to short codes and back"""

    def __init__(self):
        self.long_to_short: Dict[str, str] = {}
        self.short_to_long: Dict[str, str] = {}
        self.counter = 0

    def _encode(self, num: int) -> str:
        """Convert number to base62 string"""
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""
        while num > 0:
            result = chars[num % 62] + result
            num //= 62
        return result if result else "0"

    def shorten(self, long_url: str) -> str:
        """Convert long URL to short code"""
        if long_url in self.long_to_short:
            return self.long_to_short[long_url]

        short_code = self._encode(self.counter)
        self.counter += 1

        self.long_to_short[long_url] = short_code
        self.short_to_long[short_code] = long_url
        return short_code

    def expand(self, short_code: str) -> str:
        """Expand short code back to long URL"""
        return self.short_to_long.get(short_code, "Not found")

# Test URL shortener
print("URL Shortener Demo:\n")
shortener = URLShortener()

urls = [
    "https://www.example.com/very/long/path/to/resource",
    "https://github.com/user/repository/blob/main/file.py",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
]

for url in urls:
    short = shortener.shorten(url)
    print(f"  Long:  {url}")
    print(f"  Short: {short}")
    print(f"  Expand: {shortener.expand(short)}\n")

print("→ Time: O(1) for shorten/expand with hash maps")
print("→ Space: O(n) for storing URL pairs")

# ==================== PART 2: Word Frequency Analyzer ====================
print("\n[PART 2] Word Frequency Analyzer")
print("-" * 70)

class TextAnalyzer:
    """Analyze text for word frequencies and patterns"""

    def __init__(self, text: str):
        self.text = text
        self.words = self._tokenize(text)
        self.freq = Counter(self.words)

    def _tokenize(self, text: str) -> List[str]:
        """Split text into words"""
        import re
        text = text.lower()
        words = re.findall(r'\b[a-z]+\b', text)
        return words

    def most_common(self, k: int = 5) -> List[Tuple[str, int]]:
        """Get k most frequent words"""
        return self.freq.most_common(k)

    def word_frequency(self, word: str) -> int:
        """Get frequency of specific word"""
        return self.freq.get(word, 0)

    def unique_words(self) -> int:
        """Count unique words"""
        return len(self.freq)

    def total_words(self) -> int:
        """Count total words"""
        return len(self.words)

# Test word analyzer
print("Text Analysis Demo:\n")
sample_text = """
The quick brown fox jumps over the lazy dog. The dog was very lazy.
The quick fox is quick and clever. This fox jumped and jumped again.
"""

analyzer = TextAnalyzer(sample_text)

print(f"Total words: {analyzer.total_words()}")
print(f"Unique words: {analyzer.unique_words()}")
print(f"\nTop 5 most common words:")
for word, count in analyzer.most_common(5):
    print(f"  '{word}': {count} times")

print(f"\nFrequency of 'quick': {analyzer.word_frequency('quick')}")
print(f"Frequency of 'dog': {analyzer.word_frequency('dog')}")

print("\n→ Time: O(n) to build frequency map, O(1) per lookup")
print("→ Space: O(unique words)")

# ==================== PART 3: Auto-complete System ====================
print("\n[PART 3] Auto-complete Suggestion System")
print("-" * 70)

class TrieNode:
    """Node in trie structure"""
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.frequency = 0

class AutocompleteSystem:
    """Suggest words based on prefix"""

    def __init__(self, words: List[str]):
        self.root = TrieNode()
        self.word_freq = Counter(words)

        for word in words:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_word = True
            node.frequency = self.word_freq[word]

    def search(self, prefix: str, limit: int = 3) -> List[str]:
        """Get top suggestions for prefix"""
        # Find prefix node
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # DFS to find all words with this prefix
        suggestions = []

        def dfs(node, word):
            if node.is_word:
                suggestions.append((word, node.frequency))
            for char, child in node.children.items():
                dfs(child, word + char)

        dfs(node, prefix)

        # Sort by frequency (descending) and return top limit
        suggestions.sort(key=lambda x: -x[1])
        return [word for word, freq in suggestions[:limit]]

# Test autocomplete
print("Auto-complete System Demo:\n")
words = ["apple", "app", "application", "apply", "approve", "apricot", "april"]
autocomplete = AutocompleteSystem(words)

prefixes = ["ap", "app", "apr"]
for prefix in prefixes:
    suggestions = autocomplete.search(prefix, limit=3)
    print(f"  Prefix '{prefix}': {suggestions}")

print("\n→ Time: O(m + n log n) where m = prefix length, n = matches")
print("→ Space: O(total characters in words)")

# ==================== PART 4: Session Manager ====================
print("\n[PART 4] Session Manager with Expiration")
print("-" * 70)

class SessionManager:
    """Manage user sessions with timeout"""

    def __init__(self, timeout_seconds: int = 300):
        self.sessions: Dict[str, dict] = {}
        self.timeout = timeout_seconds

    def create_session(self, user_id: str, data: dict) -> str:
        """Create new session"""
        session_id = f"session_{user_id}_{int(time.time())}"
        self.sessions[session_id] = {
            "user_id": user_id,
            "data": data,
            "created_at": time.time(),
        }
        return session_id

    def get_session(self, session_id: str) -> dict:
        """Get session data if not expired"""
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]
        elapsed = time.time() - session["created_at"]

        if elapsed > self.timeout:
            del self.sessions[session_id]
            return None

        return session["data"]

    def update_session(self, session_id: str, data: dict) -> bool:
        """Update session data"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            elapsed = time.time() - session["created_at"]

            if elapsed <= self.timeout:
                session["data"].update(data)
                return True

        return False

    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def active_sessions(self) -> int:
        """Count active sessions"""
        now = time.time()
        active = 0
        expired = []

        for sid, session in self.sessions.items():
            elapsed = now - session["created_at"]
            if elapsed > self.timeout:
                expired.append(sid)
            else:
                active += 1

        # Clean up expired
        for sid in expired:
            del self.sessions[sid]

        return active

# Test session manager
print("Session Manager Demo:\n")
manager = SessionManager(timeout_seconds=100)

# Create sessions
sid1 = manager.create_session("user1", {"role": "admin", "ip": "192.168.1.1"})
sid2 = manager.create_session("user2", {"role": "user", "ip": "192.168.1.2"})

print(f"Created session 1: {sid1}")
print(f"Created session 2: {sid2}")

# Get sessions
data1 = manager.get_session(sid1)
print(f"\nSession 1 data: {data1}")

# Update session
manager.update_session(sid1, {"last_action": "login"})
print(f"Updated session 1: {manager.get_session(sid1)}")

# Active sessions
print(f"\nActive sessions: {manager.active_sessions()}")

# Delete
manager.delete_session(sid2)
print(f"After deleting session 2: {manager.active_sessions()} active")

print("\n→ Time: O(1) for create/get/update/delete")
print("→ Space: O(active sessions)")

# ==================== PART 5: Analysis ====================
print("\n[PART 5] Hash Map Performance Analysis")
print("-" * 70)

def benchmark_operations(size: int):
    """Benchmark hash map operations"""
    hash_map = {}

    # Insert
    start = time.time()
    for i in range(size):
        hash_map[f"key_{i}"] = i
    insert_time = (time.time() - start) * 1000

    # Search
    start = time.time()
    for i in range(0, size, 2):
        _ = hash_map.get(f"key_{i}")
    search_time = (time.time() - start) * 1000

    # Delete
    start = time.time()
    for i in range(0, size, 4):
        del hash_map[f"key_{i}"]
    delete_time = (time.time() - start) * 1000

    return insert_time, search_time, delete_time

print("Performance Benchmarks:\n")
print(f"{'Size':<10} {'Insert':<12} {'Search':<12} {'Delete':<12}")
print("-" * 46)

for size in [1000, 10000, 100000]:
    insert, search, delete = benchmark_operations(size)
    print(
        f"{size:<10} {insert:>6.2f}ms {'':<2} {search:>6.2f}ms {'':<2} {delete:>6.2f}ms"
    )

print("\n→ All operations scale linearly O(n) for the whole dataset")
print("→ Individual operations are O(1) average case")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Real-World Hash Map Applications:

1. URL Shortener
   - Map long URLs to short codes
   - Bidirectional mapping
   - O(1) encode/decode operations

2. Word Frequency Analyzer
   - Count word occurrences
   - Find most common words
   - Text analysis and statistics

3. Auto-complete System
   - Suggest words by prefix
   - Rank by frequency
   - Fast retrieval with Trie + hash map

4. Session Manager
   - Store user session data
   - Handle timeouts and expiration
   - O(1) create/get/delete operations

Key Insights:

✓ Hash maps provide O(1) average lookup
✓ Perfect for counting and deduplication
✓ Two-direction maps solve many problems
✓ Combine with other structures (Trie, LinkedList)
✓ Always consider collision resolution
✓ Load factor affects performance

Common Real-World Uses:

- Caching (browsers, databases, CDNs)
- Deduplication (removing duplicates)
- Frequency analysis (word count, analytics)
- Session management (web apps)
- Database indexing (hash indexes)
- Symbol tables (compilers)
- Password verification (salt + hash)
- De-duplication in data pipelines

Performance Characteristics:

Operation    Average    Worst Case    Notes
─────────────────────────────────────────
Insert       O(1)       O(n)          With rehashing
Search       O(1)       O(n)          Hash collision chain
Delete       O(1)       O(n)          Remove from chain
Iterate      O(n)       O(n)          Visit all items
Rehash       O(n)       O(n)          Occasional operation

Next Steps:
1. Master hash map operations
2. Solve LeetCode hash map problems
3. Combine with other data structures
4. Move to Topic 10: Basic Searching
""")

print("=" * 70)
print("Project Complete! Topic 09 Finished Successfully!")
print("=" * 70)
