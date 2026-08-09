"""
Project: Text Analysis & Pattern Matching Tool

Build a practical tool that:
1. Analyzes text statistics
2. Finds patterns and keywords
3. Detects plagiarism/similarity
4. Provides transformations and compression
5. Generates text statistics

This project applies:
- String operations and transformations
- Pattern matching algorithms
- Similarity metrics
- Text analysis techniques
"""

import re
from collections import Counter
from typing import List, Dict, Tuple

print("=" * 70)
print("PROJECT: Text Analysis & Pattern Matching Tool")
print("=" * 70)

# ==================== PART 1: Text Statistics ====================
print("\n[PART 1] Text Statistics & Analysis")
print("-" * 70)

class TextAnalyzer:
    """Analyze text statistics"""

    def __init__(self, text: str):
        self.text = text
        self.words = text.split()
        self.chars = text

    def get_statistics(self) -> Dict:
        """Get comprehensive text statistics"""
        stats = {
            "total_chars": len(self.chars),
            "total_words": len(self.words),
            "unique_words": len(set(w.lower() for w in self.words)),
            "avg_word_length": sum(len(w) for w in self.words) / len(self.words) if self.words else 0,
            "longest_word": max(self.words, key=len) if self.words else "",
            "unique_chars": len(set(self.text.lower())),
        }
        return stats

    def word_frequency(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """Get most frequent words"""
        words = [w.lower() for w in self.words]
        counter = Counter(words)
        return counter.most_common(top_n)

    def char_frequency(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get most frequent characters"""
        chars = [c for c in self.text.lower() if c.isalnum()]
        counter = Counter(chars)
        return counter.most_common(top_n)

# Test analyzer
text = "The quick brown fox jumps over the lazy dog. The dog was very lazy."
analyzer = TextAnalyzer(text)

print(f"Text: '{text}'\n")

stats = analyzer.get_statistics()
print("Text Statistics:")
for key, value in stats.items():
    if isinstance(value, float):
        print(f"  {key:20} : {value:.2f}")
    else:
        print(f"  {key:20} : {value}")

print("\nTop 3 Most Frequent Words:")
for word, count in analyzer.word_frequency(3):
    print(f"  '{word}' : {count} times")

print("\nTop 5 Most Frequent Characters:")
for char, count in analyzer.char_frequency(5):
    print(f"  '{char}' : {count} times")

# ==================== PART 2: Pattern Matching ====================
print("\n[PART 2] Pattern Matching & Text Search")
print("-" * 70)

class PatternMatcher:
    """Find patterns in text"""

    @staticmethod
    def find_all_occurrences(text: str, pattern: str) -> List[int]:
        """Find all occurrences of pattern"""
        indices = []
        for i in range(len(text) - len(pattern) + 1):
            if text[i:i+len(pattern)] == pattern:
                indices.append(i)
        return indices

    @staticmethod
    def find_email_addresses(text: str) -> List[str]:
        """Extract email addresses"""
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.findall(pattern, text)

    @staticmethod
    def find_urls(text: str) -> List[str]:
        """Extract URLs"""
        pattern = r"https?://[^\s]+"
        return re.findall(pattern, text)

    @staticmethod
    def find_phone_numbers(text: str) -> List[str]:
        """Extract phone numbers"""
        pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
        return re.findall(pattern, text)

# Test pattern matcher
print("Extracting Patterns from Text:\n")

text_with_patterns = """
Contact us at:
Email: john.doe@example.com or jane@company.org
Phone: 555-123-4567 or 555.987.6543
Website: https://www.example.com
Social: https://twitter.com/username
"""

print(f"Text: {text_with_patterns}\n")

print("Emails found:")
for email in PatternMatcher.find_email_addresses(text_with_patterns):
    print(f"  {email}")

print("\nURLs found:")
for url in PatternMatcher.find_urls(text_with_patterns):
    print(f"  {url}")

print("\nPhone numbers found:")
for phone in PatternMatcher.find_phone_numbers(text_with_patterns):
    print(f"  {phone}")

# ==================== PART 3: String Similarity ====================
print("\n[PART 3] String Similarity Detection")
print("-" * 70)

class SimilarityAnalyzer:
    """Measure similarity between strings"""

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate edit distance between two strings"""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize first row and column
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Fill the table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],    # delete
                        dp[i][j-1],    # insert
                        dp[i-1][j-1]   # replace
                    )

        return dp[m][n]

    @staticmethod
    def similarity_percentage(s1: str, s2: str) -> float:
        """Calculate similarity as percentage (0-100)"""
        distance = SimilarityAnalyzer.levenshtein_distance(s1, s2)
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 100.0
        return (1 - distance / max_len) * 100

    @staticmethod
    def jaccard_similarity(s1: str, s2: str) -> float:
        """Calculate Jaccard similarity (set-based)"""
        set1 = set(s1.lower())
        set2 = set(s2.lower())
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union) if union else 0

# Test similarity analyzer
pairs = [
    ("hello", "hello"),
    ("hello", "hallo"),
    ("kitten", "sitting"),
    ("saturday", "sunday"),
]

print("String Similarity Comparison:\n")
print(f"{'String 1':<15} {'String 2':<15} {'Distance':<10} {'Similarity %':<15}")
print("-" * 55)

for s1, s2 in pairs:
    distance = SimilarityAnalyzer.levenshtein_distance(s1, s2)
    similarity = SimilarityAnalyzer.similarity_percentage(s1, s2)
    print(f"{s1:<15} {s2:<15} {distance:<10} {similarity:>6.1f}%")

# ==================== PART 4: String Transformations ====================
print("\n[PART 4] String Transformations & Processing")
print("-" * 70)

class StringTransformer:
    """Transform strings in various ways"""

    @staticmethod
    def compress_string(s: str) -> str:
        """Compress string by grouping consecutive chars"""
        if not s:
            return ""

        result = []
        count = 1

        for i in range(1, len(s)):
            if s[i] == s[i-1]:
                count += 1
            else:
                result.append(s[i-1] + str(count))
                count = 1

        result.append(s[-1] + str(count))
        compressed = "".join(result)

        return compressed if len(compressed) < len(s) else s

    @staticmethod
    def remove_duplicates(s: str) -> str:
        """Remove consecutive duplicate characters"""
        if not s:
            return ""

        result = [s[0]]
        for i in range(1, len(s)):
            if s[i] != s[i-1]:
                result.append(s[i])

        return "".join(result)

    @staticmethod
    def reverse_words(s: str) -> str:
        """Reverse order of words"""
        return " ".join(s.split()[::-1])

    @staticmethod
    def capitalize_words(s: str) -> str:
        """Capitalize first letter of each word"""
        return " ".join(word.capitalize() for word in s.split())

# Test transformations
print("String Transformations:\n")

text = "aabbccddee"
print(f"Original: '{text}'")
print(f"Compressed: '{StringTransformer.compress_string(text)}'")

text2 = "hello world python"
print(f"\nOriginal: '{text2}'")
print(f"Reversed words: '{StringTransformer.reverse_words(text2)}'")
print(f"Capitalized: '{StringTransformer.capitalize_words(text2)}'")

text3 = "aabbccaa"
print(f"\nOriginal: '{text3}'")
print(f"Remove consecutive dupes: '{StringTransformer.remove_duplicates(text3)}'")

# ==================== PART 5: Palindrome Analysis ====================
print("\n[PART 5] Palindrome Detection & Analysis")
print("-" * 70)

class PalindromeAnalyzer:
    """Analyze palindromes"""

    @staticmethod
    def is_palindrome(s: str) -> bool:
        """Check if string is palindrome (ignore case & non-alphanumeric)"""
        cleaned = "".join(c.lower() for c in s if c.isalnum())
        return cleaned == cleaned[::-1]

    @staticmethod
    def longest_palindrome_substring(s: str) -> str:
        """Find longest palindromic substring (expand around center)"""
        if not s:
            return ""

        def expand_around_center(left: int, right: int) -> str:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left+1:right]

        longest = ""
        for i in range(len(s)):
            # Odd length palindromes
            p1 = expand_around_center(i, i)
            if len(p1) > len(longest):
                longest = p1

            # Even length palindromes
            p2 = expand_around_center(i, i+1)
            if len(p2) > len(longest):
                longest = p2

        return longest

# Test palindrome analyzer
test_cases = [
    "racecar",
    "hello",
    "A man a plan a canal Panama",
    "Madam, I'm Adam",
]

print("Palindrome Detection:\n")
for text in test_cases:
    is_pal = PalindromeAnalyzer.is_palindrome(text)
    status = "✓ Palindrome" if is_pal else "✗ Not palindrome"
    print(f"  '{text}' → {status}")

print("\nFinding Longest Palindrome Substrings:\n")
test_strings = [
    "babad",
    "cbbd",
    "forgeeksskeegfor",
]

for s in test_strings:
    longest = PalindromeAnalyzer.longest_palindrome_substring(s)
    print(f"  '{s}' → '{longest}' (length {len(longest)})")

# ==================== PART 6: Text Search Engine ====================
print("\n[PART 6] Simple Search Engine")
print("-" * 70)

class SimpleSearchEngine:
    """Simple keyword search in documents"""

    def __init__(self, documents: List[str]):
        self.documents = documents
        self.index = self._build_index()

    def _build_index(self) -> Dict[str, List[int]]:
        """Build keyword index"""
        index = {}
        for doc_idx, doc in enumerate(self.documents):
            words = doc.lower().split()
            for word in words:
                word_clean = "".join(c for c in word if c.isalnum())
                if word_clean:
                    if word_clean not in index:
                        index[word_clean] = []
                    if doc_idx not in index[word_clean]:
                        index[word_clean].append(doc_idx)
        return index

    def search(self, query: str) -> List[Tuple[int, str]]:
        """Search for documents containing query"""
        keywords = query.lower().split()
        results = []

        for keyword in keywords:
            keyword_clean = "".join(c for c in keyword if c.isalnum())
            if keyword_clean in self.index:
                for doc_idx in self.index[keyword_clean]:
                    results.append((doc_idx, self.documents[doc_idx]))

        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for item in results:
            if item[0] not in seen:
                seen.add(item[0])
                unique_results.append(item)

        return unique_results

# Test search engine
documents = [
    "Python is a great programming language",
    "Java is also used for programming",
    "Data science uses Python extensively",
    "Web development with JavaScript",
]

engine = SimpleSearchEngine(documents)

print("Search Engine Example:\n")
print("Documents:")
for i, doc in enumerate(documents):
    print(f"  {i}: '{doc}'")

queries = ["Python", "programming", "JavaScript"]
for query in queries:
    results = engine.search(query)
    print(f"\nSearching for '{query}':")
    for doc_idx, doc in results:
        print(f"  Doc {doc_idx}: '{doc}'")

# ==================== PART 7: Performance Comparison ====================
print("\n[PART 7] Algorithm Performance Analysis")
print("-" * 70)

import time

def benchmark_palindrome_check(n_iterations: int):
    """Benchmark palindrome checking"""
    palindrome = "a" * 1000 + "b" + "a" * 1000
    not_palindrome = "abcdefghijklmnopqrstuvwxyz" * 77

    # Check palindrome
    start = time.time()
    for _ in range(n_iterations):
        PalindromeAnalyzer.is_palindrome(palindrome)
    time_pal = (time.time() - start) * 1000

    start = time.time()
    for _ in range(n_iterations):
        PalindromeAnalyzer.is_palindrome(not_palindrome)
    time_not_pal = (time.time() - start) * 1000

    return time_pal, time_not_pal

print("Performance Benchmarks:\n")
print("Palindrome Check (1000 iterations):")
time_pal, time_not_pal = benchmark_palindrome_check(1000)
print(f"  Actual palindrome:     {time_pal:.2f} ms")
print(f"  Not palindrome:        {time_not_pal:.2f} ms")
print("  → Linear O(n) algorithm, early exit when mismatch found")

# ==================== PART 8: Summary ====================
print("\n" + "=" * 70)
print("PROJECT SUMMARY")
print("=" * 70)

print("""
Topics Covered:

1. Text Analysis
   - Character and word statistics
   - Frequency analysis
   - Text metrics
   - Complexity: O(n)

2. Pattern Matching
   - Substring search
   - Email/URL/Phone extraction
   - Regular expressions
   - Naive: O(n*m), Regex: O(n)

3. String Similarity
   - Levenshtein distance (edit distance)
   - Similarity percentage
   - Jaccard similarity
   - Complexity: O(n*m) for DP approach

4. String Transformations
   - String compression
   - Duplicate removal
   - Word reversal
   - Capitalization
   - Complexity: O(n)

5. Palindrome Analysis
   - Palindrome detection
   - Longest palindrome substring
   - Expand around center
   - Complexity: O(n²) for expansion

6. Search Engine
   - Inverted index creation
   - Keyword search
   - Document retrieval
   - Complexity: O(n) build, O(1) average search

7. Performance Analysis
   - Benchmarking algorithms
   - Comparing approaches
   - Optimization techniques

Real-World Applications:

✓ Text editors (find/replace)
✓ Search engines (keyword indexing)
✓ Plagiarism detection (similarity)
✓ Spell checkers (edit distance)
✓ Email/phone validators (regex)
✓ Data compression (string compression)
✓ Social media (hashtag search)
✓ Databases (full-text search)

Key Algorithms:

✓ Edit distance (Levenshtein)
✓ Longest palindrome (expand center)
✓ Substring search (naive, KMP)
✓ Pattern matching (regex)
✓ Inverted index (search)
✓ String compression (RLE)

Performance Insights:

- Most operations: O(n) or O(n²)
- Edit distance: O(n*m) with DP
- Regex matching: O(n) average
- String comparison: O(min(n,m))
- Building index: O(n*m) worst case

Learning Points:

✓ Strings are immutable
✓ Use join() not += in loops
✓ Two-pointer works for palindromes
✓ Hash maps track frequencies
✓ DP solves edit distance
✓ Early exit optimizes comparisons
✓ Regex is powerful but can be slow
✓ Indexing enables fast search

Next Steps:
1. Implement KMP algorithm for O(n+m) search
2. Add more pattern types (regex extended)
3. Implement Rabin-Karp for faster matching
4. Add support for Unicode normalization
5. Move to Topic 05: Queues
""")

print("=" * 70)
print("Project Complete! Topic 03 Finished Successfully!")
print("=" * 70)
