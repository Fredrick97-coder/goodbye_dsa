"""
Examples: Tries & String Algorithms

Demonstrate tries, KMP, Rabin-Karp, Z-algorithm, Aho-Corasick,
suffix arrays, and Manacher's algorithm.
"""

import random
import time
from collections import deque
from typing import List, Tuple, Dict, Optional

print("=" * 70)
print("TRIES & STRING ALGORITHMS")
print("=" * 70)

# ==================== (1) The Naive Baseline ====================
print("\n[1] The Naive Baseline (and Why It Is Slow)")
print("-" * 70)

def naive_search(text: str, pattern: str) -> Tuple[List[int], int]:
    """Check every position. Returns (matches, comparison count)."""
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return matches, comparisons

text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
matches, cmps = naive_search(text, pattern)
print(f"Text    : {text}")
print(f"Pattern : {pattern}")
print(f"Matches : {matches}")
print(f"Comparisons: {cmps}")

# The adversarial case
bad_text = "a" * 2000 + "b"
bad_pattern = "a" * 20 + "b"
_, bad_cmps = naive_search(bad_text, bad_pattern)
print(f"\nAdversarial input: text = 'a'*2000 + 'b', pattern = 'a'*20 + 'b'")
print(f"  Comparisons: {bad_cmps:,}  (n*m would be {len(bad_text) * len(bad_pattern):,})")
print("  -> Every position matches 20 chars, then fails. All that work discarded.")

print("\n-> The fix behind every algorithm below: a MISMATCH IS INFORMATION.")
print("   Naive search throws it away and restarts at i+1.")

# ==================== (2) Trie ====================
print("\n[2] Trie (Prefix Tree)")
print("-" * 70)

class TrieNode:
    __slots__ = ("children", "is_word", "count")

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_word = False
        self.count = 0             # words passing through this node


class Trie:
    """Prefix tree. All operations O(m) in the key length."""

    def __init__(self):
        self.root = TrieNode()
        self.num_words = 0
        self.num_nodes = 1

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self.num_nodes += 1
            node = node.children[ch]
            node.count += 1
        if not node.is_word:
            self.num_words += 1
        node.is_word = True

    def _walk(self, s: str) -> Optional[TrieNode]:
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def count_prefix(self, prefix: str) -> int:
        node = self._walk(prefix)
        return node.count if node else 0

    def words_with_prefix(self, prefix: str) -> List[str]:
        node = self._walk(prefix)
        if not node:
            return []
        out = []
        def dfs(n: TrieNode, path: str):
            if n.is_word:
                out.append(prefix + path)
            for ch in sorted(n.children):
                dfs(n.children[ch], path + ch)
        dfs(node, "")
        return out

    def longest_prefix_of(self, query: str) -> str:
        """Longest stored word that is a prefix of `query`. O(m)"""
        node = self.root
        best = ""
        for i, ch in enumerate(query):
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.is_word:
                best = query[:i + 1]
        return best


words = ["cat", "car", "card", "care", "careful", "dog", "do", "done"]
trie = Trie()
for w in words:
    trie.insert(w)

print(f"Inserted: {words}")
print(f"  Words : {trie.num_words}")
print(f"  Nodes : {trie.num_nodes}  (total chars = {sum(len(w) for w in words)})")

print("\nExact search:")
for q in ["car", "care", "ca", "cars", "do"]:
    print(f"  search({q!r:<8}) -> {trie.search(q)}")

print("\nPrefix queries (what a hash set cannot do):")
for p in ["car", "ca", "do", "x"]:
    print(f"  starts_with({p!r:<6}) -> {str(trie.starts_with(p)):<6}"
          f" count = {trie.count_prefix(p)}")

print("\nAutocomplete -- words_with_prefix:")
for p in ["car", "do", "ca"]:
    print(f"  '{p}' -> {trie.words_with_prefix(p)}")

print("\nLongest stored prefix of a query (how IP routers match):")
for q in ["careful", "cardboard", "doneness", "zebra"]:
    result = trie.longest_prefix_of(q)
    print(f"  '{q:<11}' -> '{result}'" if result else f"  '{q:<11}' -> (none)")

# Trie vs set for prefix work
print("\nTrie vs set: prefix search on 20,000 words")
random.seed(1)
letters = "abcdefghijklmnopqrstuvwxyz"
corpus = ["".join(random.choice(letters) for _ in range(random.randint(4, 9)))
          for _ in range(20_000)]

big_trie = Trie()
for w in corpus:
    big_trie.insert(w)
word_set = set(corpus)

probes = ["".join(random.choice(letters) for _ in range(3)) for _ in range(300)]

start = time.perf_counter()
for p in probes:
    big_trie.count_prefix(p)
trie_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for p in probes:
    sum(1 for w in word_set if w.startswith(p))
set_ms = (time.perf_counter() - start) * 1000

print(f"  Trie count_prefix : {trie_ms:>9.2f}ms   O(m)")
print(f"  Set scan          : {set_ms:>9.2f}ms   O(n*m)")
print(f"  -> trie is {set_ms / trie_ms:.0f}x faster for prefix counting")

# But exact lookup is a different story
start = time.perf_counter()
for w in corpus[:5000]:
    big_trie.search(w)
trie_exact_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for w in corpus[:5000]:
    _ = w in word_set
set_exact_ms = (time.perf_counter() - start) * 1000

print(f"\n  Trie exact search : {trie_exact_ms:>9.2f}ms")
print(f"  Set membership    : {set_exact_ms:>9.2f}ms")
print(f"  -> set is {trie_exact_ms / set_exact_ms:.0f}x faster for EXACT lookup")
print("  -> Use a trie for PREFIX work. Use a set for exact membership.")

# ==================== (3) KMP ====================
print("\n[3] KMP (Knuth-Morris-Pratt)")
print("-" * 70)

def build_lps(pattern: str) -> List[int]:
    """
    lps[i] = length of the longest proper prefix of pattern[0..i]
    that is also a suffix of it. O(m) amortized.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0

    for i in range(1, m):
        while length > 0 and pattern[i] != pattern[length]:
            length = lps[length - 1]        # fall back
        if pattern[i] == pattern[length]:
            length += 1
        lps[i] = length

    return lps


def kmp_search(text: str, pattern: str) -> Tuple[List[int], int]:
    """O(n + m). `i` never backs up. Returns (matches, comparisons)."""
    if not pattern:
        return [], 0
    lps = build_lps(pattern)
    matches = []
    comparisons = 0
    j = 0

    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            comparisons += 1
            j = lps[j - 1]
        comparisons += 1
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)
            j = lps[j - 1]                  # allow overlapping matches
    return matches, comparisons


pattern = "ababcabab"
lps = build_lps(pattern)

print(f"Pattern: {pattern}")
print(f"\n  {'i':>3}  {'char':>5}  {'prefix[0..i]':>14}  {'lps':>4}  meaning")
print("  " + "-" * 62)
for i, ch in enumerate(pattern):
    pre = pattern[:i + 1]
    meaning = f"'{pattern[:lps[i]]}' is both prefix and suffix" if lps[i] else "no overlap"
    print(f"  {i:>3}  {ch:>5}  {pre:>14}  {lps[i]:>4}  {meaning}")

text = "ABABDABACDABABCABAB".lower()
pat = "ababcabab"
kmp_matches, kmp_cmps = kmp_search(text, pat)
naive_matches, naive_cmps = naive_search(text, pat)

print(f"\nSearching '{pat}' in '{text}':")
print(f"  KMP   matches: {kmp_matches}, comparisons: {kmp_cmps}")
print(f"  Naive matches: {naive_matches}, comparisons: {naive_cmps}")
print(f"  Same result: {kmp_matches == naive_matches}")

# Adversarial case
_, kmp_bad = kmp_search(bad_text, bad_pattern)
print(f"\nAdversarial input ('a'*2000+'b' vs 'a'*20+'b'):")
print(f"  Naive comparisons: {bad_cmps:>8,}")
print(f"  KMP comparisons  : {kmp_bad:>8,}")
print(f"  -> KMP does {bad_cmps / kmp_bad:.0f}x less work. It has NO bad inputs.")

# Overlapping matches
overlap_text = "aaaaa"
overlap_pat = "aa"
ov, _ = kmp_search(overlap_text, overlap_pat)
print(f"\nOverlapping matches: '{overlap_pat}' in '{overlap_text}' -> {ov}")
print("  -> j = lps[j-1] after a hit is what preserves overlaps.")
print("     Setting j = 0 would return [0, 2] and miss the rest.")

# ==================== (4) Rabin-Karp ====================
print("\n[4] Rabin-Karp (Rolling Hash)")
print("-" * 70)

BASE = 256
MOD = 1_000_000_007

def rabin_karp(text: str, pattern: str) -> Tuple[List[int], int, int]:
    """
    O(n + m) expected. Returns (matches, hash_hits, false_positives).
    Every hash hit MUST be verified -- hashes collide.
    """
    n, m = len(text), len(pattern)
    if m > n or m == 0:
        return [], 0, 0

    high = pow(BASE, m - 1, MOD)

    pat_hash = 0
    win_hash = 0
    for i in range(m):
        pat_hash = (pat_hash * BASE + ord(pattern[i])) % MOD
        win_hash = (win_hash * BASE + ord(text[i])) % MOD

    matches = []
    hash_hits = 0
    false_positives = 0

    for i in range(n - m + 1):
        if win_hash == pat_hash:
            hash_hits += 1
            if text[i:i + m] == pattern:        # THE verification step
                matches.append(i)
            else:
                false_positives += 1
        if i < n - m:
            win_hash = ((win_hash - ord(text[i]) * high) * BASE
                        + ord(text[i + m])) % MOD

    return matches, hash_hits, false_positives


text = "the quick brown fox jumps over the lazy dog, the end"
pat = "the"
rk_matches, hits, fps = rabin_karp(text, pat)

print(f"Text   : {text}")
print(f"Pattern: '{pat}'")
print(f"Matches: {rk_matches}")
print(f"Hash hits: {hits}, false positives: {fps}")

print("\nThe rolling step -- O(1) per shift:")
demo = "abcde"
m = 3
h = 0
for i in range(m):
    h = (h * BASE + ord(demo[i])) % MOD
print(f"  hash('{demo[0:3]}') = {h}")
high = pow(BASE, m - 1, MOD)
for i in range(len(demo) - m):
    h = ((h - ord(demo[i]) * high) * BASE + ord(demo[i + m])) % MOD
    print(f"  roll -> hash('{demo[i+1:i+1+m]}') = {h}"
          f"   (removed '{demo[i]}', added '{demo[i+m]}')")

# Where Rabin-Karp shines: many same-length patterns
print("\nRabin-Karp's real strength: MANY same-length patterns, one pass")

def multi_pattern_rk(text: str, patterns: List[str]) -> List[Tuple[int, str]]:
    """All patterns must share a length. O(n + k*m)."""
    if not patterns:
        return []
    m = len(patterns[0])
    n = len(text)
    if m > n:
        return []

    high = pow(BASE, m - 1, MOD)
    table: Dict[int, List[str]] = {}
    for p in patterns:
        h = 0
        for ch in p:
            h = (h * BASE + ord(ch)) % MOD
        table.setdefault(h, []).append(p)

    win = 0
    for i in range(m):
        win = (win * BASE + ord(text[i])) % MOD

    found = []
    for i in range(n - m + 1):
        for cand in table.get(win, []):
            if text[i:i + m] == cand:
                found.append((i, cand))
        if i < n - m:
            win = ((win - ord(text[i]) * high) * BASE + ord(text[i + m])) % MOD
    return found


dna = "ACGTACGTGCATGCATACGTTGCAACGTACGT"
motifs = ["ACGT", "GCAT", "TGCA", "TTTT"]
found = multi_pattern_rk(dna, motifs)

print(f"  DNA    : {dna}")
print(f"  Motifs : {motifs}")
print(f"  Found {len(found)} occurrences in ONE pass:")
by_motif: Dict[str, List[int]] = {}
for pos, mot in found:
    by_motif.setdefault(mot, []).append(pos)
for mot in motifs:
    positions = by_motif.get(mot, [])
    print(f"    {mot}: {positions if positions else 'not present'}")

print("\n-> One rolling hash checked against a SET of pattern hashes")
print("-> KMP would need one full pass per pattern")

# ==================== (5) Z-Algorithm ====================
print("\n[5] Z-Algorithm")
print("-" * 70)

def z_function(s: str) -> List[int]:
    """z[i] = length of the longest substring at i matching a prefix of s. O(n)"""
    n = len(s)
    z = [0] * n
    left = right = 0

    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])      # reuse earlier work
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


s = "aabcaabxaaaz"
z = z_function(s)

print(f"String: {s}")
print(f"\n  {'i':>3}  {'char':>5}  {'z[i]':>5}  match")
print("  " + "-" * 44)
for i in range(len(s)):
    if i == 0:
        print(f"  {i:>3}  {s[i]:>5}  {'-':>5}  (whole string)")
    else:
        m = f"'{s[i:i+z[i]]}' == '{s[:z[i]]}'" if z[i] else "no prefix match"
        print(f"  {i:>3}  {s[i]:>5}  {z[i]:>5}  {m}")

def z_search(text: str, pattern: str) -> List[int]:
    """Pattern matching via Z. Separator must not appear in either string."""
    combined = pattern + "\x00" + text
    z = z_function(combined)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]


text = "ababcababcabc"
pat = "abc"
print(f"\nz_search('{pat}' in '{text}') -> {z_search(text, pat)}")
print(f"  Verify with KMP -> {kmp_search(text, pat)[0]}")
print("\n-> Same O(n+m) as KMP, but easier to derive from scratch")
print("-> Also gives periodicity, distinct substring counts, and rotations")

# ==================== (6) Aho-Corasick ====================
print("\n[6] Aho-Corasick (Many Patterns, One Pass)")
print("-" * 70)

class AhoCorasick:
    """Trie + KMP-style failure links. O(n + total matches) search."""

    def __init__(self, patterns: List[str]):
        self.goto: List[Dict[str, int]] = [{}]
        self.fail: List[int] = [0]
        self.output: List[List[str]] = [[]]

        for p in patterns:
            node = 0
            for ch in p:
                if ch not in self.goto[node]:
                    self.goto.append({})
                    self.fail.append(0)
                    self.output.append([])
                    self.goto[node][ch] = len(self.goto) - 1
                node = self.goto[node][ch]
            self.output[node].append(p)

        self._build_failure_links()

    def _build_failure_links(self) -> None:
        """BFS: a node's failure link is its longest proper suffix in the trie."""
        queue = deque()
        for ch, nxt in self.goto[0].items():
            self.fail[nxt] = 0
            queue.append(nxt)

        while queue:
            node = queue.popleft()
            for ch, nxt in self.goto[node].items():
                queue.append(nxt)
                f = self.fail[node]
                while f and ch not in self.goto[f]:
                    f = self.fail[f]
                self.fail[nxt] = self.goto[f].get(ch, 0)
                if self.fail[nxt] == nxt:
                    self.fail[nxt] = 0
                # Inherit the failure target's matches -- this is essential
                self.output[nxt] = self.output[nxt] + self.output[self.fail[nxt]]

    def search(self, text: str) -> List[Tuple[int, str]]:
        node = 0
        results = []
        for i, ch in enumerate(text):
            while node and ch not in self.goto[node]:
                node = self.fail[node]
            node = self.goto[node].get(ch, 0)
            for p in self.output[node]:
                results.append((i - len(p) + 1, p))
        return results

    def num_nodes(self) -> int:
        return len(self.goto)


patterns = ["he", "she", "his", "hers"]
ac = AhoCorasick(patterns)
text = "ushers hishers he"

print(f"Patterns: {patterns}")
print(f"Text    : {text}")
print(f"Automaton nodes: {ac.num_nodes()}")

results = ac.search(text)
print(f"\nMatches found in ONE pass ({len(results)} total):")
for pos, p in results:
    print(f"  pos {pos:>2}: '{p}'   {' ' * pos}{'^' * len(p)}")

print("\nNote 'she' at position 1 ALSO reports 'he' at position 2.")
print("That is the output-inheritance step -- 'he' is a suffix of 'she'.")

# Verify against running KMP per pattern
kmp_all = []
for p in patterns:
    for pos in kmp_search(text, p)[0]:
        kmp_all.append((pos, p))
print(f"\nCross-check against {len(patterns)} separate KMP passes:")
print(f"  Aho-Corasick: {sorted(results)}")
print(f"  KMP x{len(patterns)}       : {sorted(kmp_all)}")
print(f"  Identical: {sorted(results) == sorted(kmp_all)}")

# Benchmark: k patterns
print("\nBenchmark: 200 patterns in a 200,000-char text")
random.seed(42)
big_text = "".join(random.choice("abcdefg") for _ in range(200_000))
many_patterns = ["".join(random.choice("abcdefg") for _ in range(4))
                 for _ in range(200)]
many_patterns = list(set(many_patterns))

start = time.perf_counter()
ac_big = AhoCorasick(many_patterns)
ac_build_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
ac_results = ac_big.search(big_text)
ac_search_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
kmp_count = 0
for p in many_patterns:
    kmp_count += len(kmp_search(big_text, p)[0])
kmp_total_ms = (time.perf_counter() - start) * 1000

print(f"  Patterns: {len(many_patterns)}, text: {len(big_text):,} chars")
print(f"  Aho-Corasick build : {ac_build_ms:>9.1f}ms  ({ac_big.num_nodes():,} nodes)")
print(f"  Aho-Corasick search: {ac_search_ms:>9.1f}ms  ({len(ac_results):,} matches)")
print(f"  KMP x{len(many_patterns)} passes    : {kmp_total_ms:>9.1f}ms  ({kmp_count:,} matches)")
print(f"  Same match count: {len(ac_results) == kmp_count}")
print(f"  -> Aho-Corasick (build+search) is "
      f"{kmp_total_ms / (ac_build_ms + ac_search_ms):.1f}x faster")
print("  -> One pass instead of k passes. This is why IDS/antivirus use it.")

# ==================== (7) Suffix Array ====================
print("\n[7] Suffix Array + LCP")
print("-" * 70)

def build_suffix_array(s: str) -> List[int]:
    """Prefix doubling. O(n log^2 n) -- simple and fast enough in practice."""
    n = len(s)
    if n == 0:
        return []
    k = 1
    rank = [ord(c) for c in s]
    sa = list(range(n))

    while True:
        key = lambda i: (rank[i], rank[i + k] if i + k < n else -1)
        sa.sort(key=key)

        new_rank = [0] * n
        for i in range(1, n):
            new_rank[sa[i]] = new_rank[sa[i - 1]] + (key(sa[i]) != key(sa[i - 1]))
        rank = new_rank

        if rank[sa[-1]] == n - 1:
            break
        k *= 2

    return sa


def build_lcp(s: str, sa: List[int]) -> List[int]:
    """Kasai's algorithm. O(n)"""
    n = len(s)
    if n == 0:
        return []
    rank = [0] * n
    for i, suffix in enumerate(sa):
        rank[suffix] = i

    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


s = "banana"
sa = build_suffix_array(s)
lcp = build_lcp(s, sa)

print(f"String: {s}")
print(f"\n  {'rank':>5}  {'SA':>4}  {'suffix':<10}  {'LCP':>4}  shared with previous")
print("  " + "-" * 58)
for i, idx in enumerate(sa):
    shared = s[sa[i]:sa[i] + lcp[i]] if lcp[i] else ""
    note = f"'{shared}'" if shared else "-"
    print(f"  {i:>5}  {idx:>4}  {s[idx:]:<10}  {lcp[i]:>4}  {note}")

def sa_search(s: str, sa: List[int], pattern: str) -> List[int]:
    """Binary search the sorted suffixes. O(m log n)"""
    m = len(pattern)
    lo, hi = 0, len(sa)
    while lo < hi:
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid] + m] < pattern:
            lo = mid + 1
        else:
            hi = mid
    start = lo

    hi = len(sa)
    while lo < hi:
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid] + m] <= pattern:
            lo = mid + 1
        else:
            hi = mid

    return sorted(sa[start:lo])


print(f"\nBinary search for patterns in the suffix array:")
for p in ["ana", "na", "ban", "xyz"]:
    result = sa_search(s, sa, p)
    print(f"  '{p:<4}' -> {result if result else 'not found'}"
          f"   (verify: {kmp_search(s, p)[0]})")

# What LCP unlocks
def longest_repeated_substring(s: str) -> str:
    sa_ = build_suffix_array(s)
    lcp_ = build_lcp(s, sa_)
    if not lcp_ or max(lcp_) == 0:
        return ""
    best = max(range(len(lcp_)), key=lambda i: lcp_[i])
    return s[sa_[best]:sa_[best] + lcp_[best]]

def count_distinct_substrings(s: str) -> int:
    n = len(s)
    sa_ = build_suffix_array(s)
    lcp_ = build_lcp(s, sa_)
    return n * (n + 1) // 2 - sum(lcp_)

def longest_common_substring(a: str, b: str) -> str:
    """Concatenate with a separator, then find the max LCP across the boundary."""
    combined = a + "\x01" + b
    sa_ = build_suffix_array(combined)
    lcp_ = build_lcp(combined, sa_)
    split = len(a)

    best_len, best_pos = 0, 0
    for i in range(1, len(sa_)):
        # The two suffixes must come from DIFFERENT halves
        in_a_prev = sa_[i - 1] < split
        in_a_curr = sa_[i] < split
        if in_a_prev != in_a_curr and lcp_[i] > best_len:
            best_len, best_pos = lcp_[i], sa_[i]
    return combined[best_pos:best_pos + best_len]


print("\nWhat the LCP array unlocks:")
for test in ["banana", "abcabcabc", "mississippi"]:
    lrs = longest_repeated_substring(test)
    distinct = count_distinct_substrings(test)
    print(f"  '{test}'")
    print(f"    longest repeated substring : '{lrs}'")
    print(f"    distinct substrings        : {distinct}"
          f"   (n(n+1)/2 = {len(test)*(len(test)+1)//2}, minus sum(LCP))")

pairs = [("abcdefgh", "cdefzz"), ("programming", "gaming"),
         ("sequence", "consequence")]
print("\n  Longest common substring (concatenate + max cross-boundary LCP):")
for a, b in pairs:
    print(f"    '{a}' & '{b}' -> '{longest_common_substring(a, b)}'")

# Build once, query many
print("\nThe suffix array's real value: build ONCE, query forever")
random.seed(9)
doc = "".join(random.choice("acgt") for _ in range(20_000))
queries = ["".join(random.choice("acgt") for _ in range(6)) for _ in range(2000)]

start = time.perf_counter()
doc_sa = build_suffix_array(doc)
sa_build_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
sa_hits = sum(len(sa_search(doc, doc_sa, q)) for q in queries)
sa_query_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
kmp_hits = sum(len(kmp_search(doc, q)[0]) for q in queries)
kmp_q_ms = (time.perf_counter() - start) * 1000

print(f"  Text: {len(doc):,} chars, {len(queries):,} pattern queries")
print(f"  SA build            : {sa_build_ms:>9.1f}ms  (one time)")
print(f"  SA queries          : {sa_query_ms:>9.1f}ms  O(m log n) each")
print(f"  SA total            : {sa_build_ms + sa_query_ms:>9.1f}ms")
print(f"  KMP (no index)      : {kmp_q_ms:>9.1f}ms  O(n) each")
print(f"  Same hit count: {sa_hits == kmp_hits}  ({sa_hits:,} hits)")
print(f"  -> index amortizes: {kmp_q_ms / (sa_build_ms + sa_query_ms):.1f}x faster overall")

# ==================== (8) Manacher's Algorithm ====================
print("\n[8] Manacher's Algorithm (All Palindromes in O(n))")
print("-" * 70)

def manacher(s: str) -> str:
    """Longest palindromic substring. O(n)"""
    if not s:
        return ""

    t = "#" + "#".join(s) + "#"          # handles odd and even lengths uniformly
    n = len(t)
    radius = [0] * n
    center = right = 0

    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            radius[i] = min(right - i, radius[mirror])   # symmetry reuse

        while (i - radius[i] - 1 >= 0 and i + radius[i] + 1 < n
               and t[i - radius[i] - 1] == t[i + radius[i] + 1]):
            radius[i] += 1

        if i + radius[i] > right:
            center, right = i, i + radius[i]

    best = max(range(n), key=lambda i: radius[i])
    start = (best - radius[best]) // 2
    return s[start:start + radius[best]]


def longest_palindrome_naive(s: str) -> str:
    """Expand from every center. O(n^2)"""
    if not s:
        return ""
    best = s[0]
    for i in range(len(s)):
        for lo, hi in ((i, i), (i, i + 1)):     # odd and even centers
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                if hi - lo + 1 > len(best):
                    best = s[lo:hi + 1]
                lo -= 1
                hi += 1
    return best


tests = ["babad", "cbbd", "racecar", "abacabad", "forgeeksskeegfor", "a"]
print(f"  {'Input':<20} {'Manacher':<14} {'Naive O(n^2)':<14} Match")
print("  " + "-" * 62)
for t in tests:
    mres = manacher(t)
    nres = longest_palindrome_naive(t)
    # Multiple valid answers of equal length are both correct
    ok = len(mres) == len(nres) and mres == mres[::-1]
    print(f"  {t:<20} {mres:<14} {nres:<14} {ok}")

print("\nBenchmark -- the input SHAPE decides whether the naive version hurts:")
random.seed(3)

cases = [
    ("random 'ab' (4,000)", "".join(random.choice("ab") for _ in range(4000))),
    ("all same char 'a'*4000", "a" * 4000),
    ("one huge palindrome", "ab" * 1000 + "ba" * 1000),
]

print(f"  {'Input':<24} {'Manacher':>11} {'Naive':>11} {'Ratio':>9} {'Len':>6}")
print("  " + "-" * 66)
for label, txt in cases:
    start = time.perf_counter()
    m_result = manacher(txt)
    m_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    n_result = longest_palindrome_naive(txt)
    n_ms = (time.perf_counter() - start) * 1000

    assert len(m_result) == len(n_result), f"length mismatch on {label}"
    assert m_result == m_result[::-1], f"not a palindrome on {label}"
    print(f"  {label:<24} {m_ms:>9.2f}ms {n_ms:>9.2f}ms "
          f"{n_ms / m_ms:>8.1f}x {len(m_result):>6}")

print("\n  -> On RANDOM text the naive version is competitive (often faster):")
print("     each center expansion fails after a couple of characters, so it")
print("     never reaches its O(n^2) behaviour, and it has no preprocessing.")
print("  -> On repetitive text it collapses, exactly as the bound predicts.")
print("     Manacher's value is the GUARANTEE, not the average case.")
print("  -> All outputs verified equal in length and confirmed palindromic.")

# ==================== (9) Python's Built-ins ====================
print("\n[9] Reality Check: Python's Built-in Search")
print("-" * 70)

print("CPython implements str.find in C (a two-way / Crochemore-Perrin")
print("variant). A hand-written KMP in Python competes against C, and loses.\n")

random.seed(77)
hay = "".join(random.choice("abcdefghij") for _ in range(500_000))
needle = "".join(random.choice("abcdefghij") for _ in range(8))
hay = hay[:250_000] + needle + hay[250_000:]        # guarantee a hit

def find_all_builtin(text: str, pattern: str) -> List[int]:
    out, start = [], 0
    while True:
        i = text.find(pattern, start)
        if i == -1:
            return out
        out.append(i)
        start = i + 1

start = time.perf_counter()
builtin_res = find_all_builtin(hay, needle)
builtin_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
kmp_res, _ = kmp_search(hay, needle)
kmp_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
rk_res, _, _ = rabin_karp(hay, needle)
rk_ms = (time.perf_counter() - start) * 1000

print(f"Searching an 8-char needle in a {len(hay):,}-char haystack:")
print(f"  {'Method':<24} {'Time':>11}  Matches")
print("  " + "-" * 48)
print(f"  {'str.find loop (C)':<24} {builtin_ms:>9.1f}ms  {len(builtin_res)}")
print(f"  {'KMP (pure Python)':<24} {kmp_ms:>9.1f}ms  {len(kmp_res)}")
print(f"  {'Rabin-Karp (pure Python)':<24} {rk_ms:>9.1f}ms  {len(rk_res)}")
print(f"\n  All agree: {builtin_res == kmp_res == rk_res}")
print(f"  -> str.find is {kmp_ms / builtin_ms:.0f}x faster than our KMP")
print("\n  The lesson is NOT that KMP is useless. It is that you should:")
print("    - use str.find / in / re for ordinary single-pattern search")
print("    - reach for these algorithms when built-ins cannot express the")
print("      problem: multi-pattern (Aho-Corasick), prefix queries (trie),")
print("      streaming input (KMP), repeated-substring analysis (suffix array)")

# ==================== (10) Verification Suite ====================
print("\n[10] Cross-Verification Under Random Inputs")
print("-" * 70)

random.seed(2718)
print("Running 400 random (text, pattern) pairs through every algorithm")
print("and comparing against the naive reference implementation.\n")

algos = {
    "KMP": lambda t, p: kmp_search(t, p)[0],
    "Rabin-Karp": lambda t, p: rabin_karp(t, p)[0],
    "Z-algorithm": lambda t, p: z_search(t, p),
    "Suffix array": lambda t, p: sa_search(t, build_suffix_array(t), p),
    "Aho-Corasick": lambda t, p: [pos for pos, _ in AhoCorasick([p]).search(t)],
    "str.find loop": lambda t, p: find_all_builtin(t, p),
}
failures = {name: 0 for name in algos}

for _ in range(400):
    alphabet = random.choice(["ab", "abc", "abcdefgh"])
    t = "".join(random.choice(alphabet) for _ in range(random.randint(1, 60)))
    p = "".join(random.choice(alphabet) for _ in range(random.randint(1, 5)))
    expected = naive_search(t, p)[0]
    for name, fn in algos.items():
        if fn(t, p) != expected:
            failures[name] += 1

print(f"  {'Algorithm':<18} {'Mismatches':>12}  Verdict")
print("  " + "-" * 46)
for name in algos:
    verdict = "PASS" if failures[name] == 0 else "FAIL"
    print(f"  {name:<18} {failures[name]:>12}  {verdict}")

# Palindrome verification
pal_fail = 0
for _ in range(400):
    t = "".join(random.choice("abc") for _ in range(random.randint(1, 40)))
    m_res = manacher(t)
    n_res = longest_palindrome_naive(t)
    if len(m_res) != len(n_res) or m_res != m_res[::-1]:
        pal_fail += 1
print(f"  {'Manacher':<18} {pal_fail:>12}  {'PASS' if not pal_fail else 'FAIL'}")

# Trie verification
trie_fail = 0
for _ in range(100):
    ws = ["".join(random.choice("abc") for _ in range(random.randint(1, 6)))
          for _ in range(20)]
    tr = Trie()
    for w in ws:
        tr.insert(w)
    pre = "".join(random.choice("abc") for _ in range(random.randint(1, 3)))
    expected_words = sorted(set(w for w in ws if w.startswith(pre)))
    if sorted(tr.words_with_prefix(pre)) != expected_words:
        trie_fail += 1
    if tr.count_prefix(pre) != sum(1 for w in ws if w.startswith(pre)):
        trie_fail += 1
print(f"  {'Trie':<18} {trie_fail:>12}  {'PASS' if not trie_fail else 'FAIL'}")

print("\n-> Every algorithm verified against a brute-force reference")

print("\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
