# Tries & String Algorithms - Text at Scale

Master the trie, KMP, Rabin-Karp, Z-algorithm, Aho-Corasick, suffix arrays,
and Manacher's algorithm — the structures and tricks that make text search fast.

---

## 1. The Naive Baseline

Before any clever algorithm, know what you are beating.

```python
def naive_search(text, pattern):
    """Check every starting position. O(n * m)"""
    n, m = len(text), len(pattern)
    matches = []
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:      # up to m comparisons
            matches.append(i)
    return matches
```

**Worst case**: `text = "aaaa...a"`, `pattern = "aaa...ab"`. Every position
matches m-1 characters then fails — O(n·m) comparisons.

The insight every fast algorithm shares: **a failed match tells you
something**. Naive search throws that information away and restarts at
`i + 1`. Everything below is a different way of keeping it.

---

## 2. Tries (Prefix Trees)

A trie stores strings by shared prefix. Each edge is a character; each path
from the root is a prefix.

```
Insert: "cat", "car", "card", "care", "dog"

           (root)
           /    \
          c      d
          |      |
          a      o
         / \     |
        t   r    g*
        *   *
           / \
          d   e
          *   *

* marks the end of a word
```

```python
class TrieNode:
    __slots__ = ("children", "is_word", "count")

    def __init__(self):
        self.children = {}       # char -> TrieNode
        self.is_word = False
        self.count = 0           # words passing through, for prefix counting


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """O(m) where m = len(word)"""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        node.is_word = True

    def search(self, word):
        """Exact match. O(m)"""
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix):
        """Does any word have this prefix? O(m)"""
        return self._walk(prefix) is not None

    def count_prefix(self, prefix):
        """How many words share this prefix? O(m)"""
        node = self._walk(prefix)
        return node.count if node else 0

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def words_with_prefix(self, prefix):
        """All completions. O(m + total output size)"""
        node = self._walk(prefix)
        if not node:
            return []
        out = []
        def dfs(n, path):
            if n.is_word:
                out.append(prefix + path)
            for ch, child in n.children.items():
                dfs(child, path + ch)
        dfs(node, "")
        return out
```

### Why Not Just a Hash Set?

| Operation | Trie | Hash set |
|-----------|------|----------|
| Exact lookup | O(m) | **O(m)** avg (hashing reads all m chars) |
| Prefix exists | **O(m)** | O(n·m) — scan everything |
| All words with prefix | **O(m + k)** | O(n·m) |
| Sorted iteration | **O(n·m)** | needs a sort |
| Longest prefix of a query | **O(m)** | not possible |
| Memory | higher (node per char) | lower |

A hash set matches the trie on exact lookup and beats it on memory. The trie
exists for **prefix** work. If you never ask a prefix question, use a set.

**Time**: insert/search/prefix all O(m). **Space**: O(total characters), or
O(ALPHABET · nodes) with array-based children.

### Compressed Trie (Radix Tree)

A plain trie wastes nodes on non-branching chains. A radix tree collapses
them into single edges holding whole substrings.

```
Trie for "romane", "romanus", "romulus":

    r-o-m-a-n-e            r-o-m
            \-u-s      =>      ├── an ── e
    r-o-m-u-l-u-s              │      └── us
                               └── ulus
```

Nodes drop from ~15 to ~5. **Real use**: IP routing tables (longest-prefix
match), Ethereum's Merkle Patricia trie, `git`'s object store.

---

## 3. KMP (Knuth-Morris-Pratt)

**Idea**: precompute, for each prefix of the pattern, the longest proper
prefix that is also a suffix. On a mismatch, jump the pattern forward by that
much instead of restarting.

### The Failure Function (LPS Array)

`lps[i]` = length of the longest proper prefix of `pattern[0..i]` that is
also a suffix of it.

```
pattern:  a  b  a  b  c  a  b  a  b
index:    0  1  2  3  4  5  6  7  8
lps:      0  0  1  2  0  1  2  3  4
                              ^
        pattern[0..7] = "ababcaba"
        "aba" is both a prefix and a suffix -> lps[7] = 3
```

```python
def build_lps(pattern):
    """O(m) time, O(m) space"""
    m = len(pattern)
    lps = [0] * m
    length = 0                       # length of the current match

    for i in range(1, m):
        while length > 0 and pattern[i] != pattern[length]:
            length = lps[length - 1]     # fall back
        if pattern[i] == pattern[length]:
            length += 1
        lps[i] = length

    return lps
```

The inner `while` looks like it could make this O(m²), but `length` only ever
increases m times total, so the amortized cost is O(m).

### The Search

```python
def kmp_search(text, pattern):
    """O(n + m) time, O(m) space. Never backs up in the text."""
    if not pattern:
        return []
    lps = build_lps(pattern)
    matches = []
    j = 0                            # chars of pattern matched so far

    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = lps[j - 1]           # shift the pattern, keep i fixed
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)
            j = lps[j - 1]           # allow overlapping matches
    return matches
```

**The key property**: `i` never decreases. Each text character is examined
once. That is what turns O(n·m) into O(n + m).

**Time**: O(n + m), **Space**: O(m). Worst case equals best case — KMP has no
bad inputs, which is why it is the safe default.

---

## 4. Rabin-Karp (Rolling Hash)

**Idea**: hash the pattern once, then roll a hash across the text. Compare
hashes (O(1)) and only compare strings when hashes match.

```
Rolling from window [i, i+m) to [i+1, i+1+m):

  remove text[i] * BASE^(m-1), multiply by BASE, add text[i+m]

  hash("abc") = a*B^2 + b*B^1 + c*B^0
  hash("bcd") = (hash("abc") - a*B^2) * B + d
```

```python
def rabin_karp(text, pattern, base=256, mod=1_000_000_007):
    """O(n + m) expected, O(n * m) worst case (all hashes collide)"""
    n, m = len(text), len(pattern)
    if m > n or m == 0:
        return []

    high = pow(base, m - 1, mod)     # BASE^(m-1) mod p

    pat_hash = 0
    win_hash = 0
    for i in range(m):
        pat_hash = (pat_hash * base + ord(pattern[i])) % mod
        win_hash = (win_hash * base + ord(text[i])) % mod

    matches = []
    for i in range(n - m + 1):
        if win_hash == pat_hash and text[i:i + m] == pattern:
            matches.append(i)        # verify -- hashes can collide
        if i < n - m:
            win_hash = ((win_hash - ord(text[i]) * high) * base
                        + ord(text[i + m])) % mod
    return matches
```

**Always verify on a hash match.** Skipping the `text[i:i+m] == pattern` check
turns a correct algorithm into a probabilistic one.

### Where Rabin-Karp Wins

KMP is better for a single pattern. Rabin-Karp wins when you need **many
patterns of the same length** — hash all of them into a set, then roll once:

```python
def multi_pattern_search(text, patterns):
    """All patterns must be the same length m. One pass, O(n + k*m)."""
    m = len(patterns[0])
    target_hashes = {hash_of(p): p for p in patterns}
    # roll one hash across text, check membership in target_hashes
```

It also generalizes to 2D (image patch matching) and underpins **duplicate
substring detection** (Rabin fingerprinting, used by `rsync` and dedup
storage).

**Time**: O(n + m) expected, O(n·m) worst case. **Space**: O(1).

---

## 5. Z-Algorithm

`z[i]` = length of the longest substring starting at `i` that matches a prefix
of the whole string.

```
s:    a  a  b  c  a  a  b  x  a  a  a  z
z:    -  1  0  0  3  1  0  0  2  2  1  0
                  ^
      s[4:] = "aabxaaaz" shares "aab" with s[0:] -> z[4] = 3
```

```python
def z_function(s):
    """O(n) time, O(n) space"""
    n = len(s)
    z = [0] * n
    left = right = 0                 # current rightmost [left, right) match

    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])    # reuse prior work
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z
```

**Pattern matching with Z**: build `pattern + "\x00" + text` and look for
`z[i] == len(pattern)`. Simpler to derive than KMP's LPS, same O(n + m).

Also gives you: all distinct substrings count, string periodicity, and the
smallest rotation.

---

## 6. Aho-Corasick (Multi-Pattern Matching)

**Problem**: find all occurrences of k patterns in one pass.

Running KMP k times costs O(k·n). Aho-Corasick does it in **O(n + total
pattern length + matches)** — a trie with KMP-style failure links.

```
Patterns: "he", "she", "his", "hers"

Trie with failure links (dashed) pointing to the longest proper
suffix that is also a node in the trie:

  root -h-> h -e-> he(*)
        \        \-r-> her -s-> hers(*)
         \-s-> s -h-> sh -e-> she(*)
          \-i          ⋮
           
  failure: she -> he  (because "he" is a suffix of "she")
  So matching "she" ALSO reports "he".
```

```python
from collections import deque

class AhoCorasick:
    def __init__(self, patterns):
        self.goto = [{}]             # node -> {char: node}
        self.fail = [0]
        self.output = [[]]           # patterns ending at this node

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

    def _build_failure_links(self):
        """BFS. A node's failure link is the longest proper suffix in the trie."""
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
                # Inherit matches from the failure target
                self.output[nxt] += self.output[self.fail[nxt]]

    def search(self, text):
        """One pass. O(n + matches)"""
        node = 0
        results = []
        for i, ch in enumerate(text):
            while node and ch not in self.goto[node]:
                node = self.fail[node]
            node = self.goto[node].get(ch, 0)
            for pattern in self.output[node]:
                results.append((i - len(pattern) + 1, pattern))
        return results
```

**Real use**: intrusion detection (Snort), virus scanners (ClamAV), spam
filters, `grep -F` with many patterns, DNA motif search.

---

## 7. Suffix Arrays

A suffix array is the sorted order of all suffixes — a compact stand-in for a
suffix tree, using far less memory.

```
s = "banana"

Suffixes:              Sorted:            SA
0: banana              5: a               [5,
1: anana               3: ana              3,
2: nana                1: anana            1,
3: ana                 0: banana           0,
4: na                  4: na               4,
5: a                   2: nana             2]
```

```python
def build_suffix_array(s):
    """
    O(n log^2 n) prefix-doubling. Simple and fast enough in practice.
    (O(n) algorithms like DC3/SA-IS exist but are far more code.)
    """
    n = len(s)
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

        if rank[sa[-1]] == n - 1:            # all ranks distinct
            break
        k *= 2

    return sa
```

### Searching with a Suffix Array

Since suffixes are sorted, **binary search** finds any pattern:

```python
def sa_search(s, sa, pattern):
    """O(m log n) -- all occurrences as a contiguous SA range."""
    lo, hi = 0, len(sa)
    while lo < hi:                           # first suffix >= pattern
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid] + len(pattern)] < pattern:
            lo = mid + 1
        else:
            hi = mid
    start = lo

    hi = len(sa)
    while lo < hi:                           # first suffix > pattern
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid] + len(pattern)] <= pattern:
            lo = mid + 1
        else:
            hi = mid

    return sorted(sa[start:lo])
```

### LCP Array

`lcp[i]` = longest common prefix of `sa[i]` and `sa[i-1]`. Kasai's algorithm
builds it in O(n):

```python
def build_lcp(s, sa):
    """Kasai's algorithm. O(n)"""
    n = len(s)
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
                h -= 1                       # amortization trick
    return lcp
```

**What LCP unlocks**:
- **Longest repeated substring** = `max(lcp)`
- **Number of distinct substrings** = `n(n+1)/2 - sum(lcp)`
- **Longest common substring of two strings**: concatenate with a separator,
  then find the max LCP between suffixes from different halves

**Real use**: bioinformatics (BWA, Bowtie read aligners), `bzip2` via the
Burrows-Wheeler transform, full-text search indexes, plagiarism detection.

---

## 8. Manacher's Algorithm (All Palindromes in O(n))

**Problem**: longest palindromic substring. Naive expansion from each center
is O(n²).

Manacher's reuses palindrome symmetry to get O(n).

```python
def manacher(s):
    """
    Longest palindromic substring in O(n).
    Transform with separators so odd/even lengths are handled uniformly.
    """
    if not s:
        return ""

    t = "#" + "#".join(s) + "#"          # "aba" -> "#a#b#a#"
    n = len(t)
    radius = [0] * n
    center = right = 0

    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            radius[i] = min(right - i, radius[mirror])   # reuse symmetry

        while (i - radius[i] - 1 >= 0 and i + radius[i] + 1 < n
               and t[i - radius[i] - 1] == t[i + radius[i] + 1]):
            radius[i] += 1

        if i + radius[i] > right:
            center, right = i, i + radius[i]

    best = max(range(n), key=lambda i: radius[i])
    start = (best - radius[best]) // 2
    return s[start:start + radius[best]]
```

**Time**: O(n) — `right` only moves forward, so the total inner-loop work is
linear. **Space**: O(n).

---

## 9. Algorithm Comparison

| Algorithm | Preprocess | Search | Space | Best for |
|-----------|-----------|--------|-------|----------|
| Naive | — | O(n·m) | O(1) | tiny inputs, one-off |
| **KMP** | O(m) | **O(n)** | O(m) | single pattern, guaranteed linear |
| **Rabin-Karp** | O(m) | O(n) exp. | O(1) | many same-length patterns, 2D |
| **Z-algorithm** | — | O(n + m) | O(n) | prefix problems, easier to derive |
| Boyer-Moore | O(m + σ) | O(n/m) best | O(σ) | long patterns, large alphabets |
| **Aho-Corasick** | O(Σm) | **O(n + z)** | O(Σm·σ) | many patterns at once |
| **Trie** | O(Σm) | O(m) | O(Σm) | prefix queries, autocomplete |
| **Suffix array** | O(n log n) | O(m log n) | O(n) | many queries on fixed text |
| Suffix automaton | O(n) | O(m) | O(n·σ) | all substrings, online |
| **Manacher** | — | O(n) | O(n) | all palindromic substrings |

σ = alphabet size, z = number of matches, Σm = total pattern length.

**Python reality check**: `str.find`, `in`, and `re` are implemented in C
(CPython uses a Crochemore-Perrin / two-way variant). A hand-written KMP in
Python will usually **lose** to `text.find(pattern)` despite matching
asymptotics. Write KMP to understand it and for cases the built-ins cannot
express — not to beat `in`.

---

## 10. Choosing an Approach

```
One pattern, one search?
└── use text.find() / in / re. Done. It is C-optimized.

One pattern, need guaranteed linear time or streaming?
└── KMP

Many patterns, one text pass?
└── Aho-Corasick

Many patterns, all the same length?
└── Rabin-Karp with a hash set

Prefix queries (autocomplete, longest-prefix match, spell check)?
└── Trie (radix tree if memory matters)

Fixed text, many different pattern queries?
└── Suffix array + LCP (build once, query forever)

Palindrome substrings?
└── Manacher

Longest repeated / common substring?
└── Suffix array + LCP
```

---

## 11. Common Pitfalls

1. **Forgetting to verify a Rabin-Karp hash match.** Hash equality is not
   string equality. Always compare the actual substring.
2. **Off-by-one in the LPS fallback.** It is `j = lps[j - 1]`, not `lps[j]`.
   The latter loops forever.
3. **Overlapping matches.** After a KMP hit, set `j = lps[j - 1]` to keep
   finding overlaps. Setting `j = 0` misses them (`"aaa"` in `"aaaa"`).
4. **Empty pattern.** Every algorithm here needs an explicit guard; `m = 0`
   otherwise produces either a crash or n+1 spurious matches.
5. **Aho-Corasick output inheritance.** A node must inherit its failure
   target's matches, or `"she"` will not report the nested `"he"`.
6. **Separator collisions.** When concatenating strings for a suffix array or
   Z-based search, the separator must not appear in the input. Use `\x00`.
7. **Trie memory.** A dict per node is heavy in Python — ~200 bytes each.
   For a fixed lowercase alphabet, a 26-slot list or a radix tree is far
   leaner.
8. **Manacher's index arithmetic.** The transformed string has length
   `2n + 1`; converting a center and radius back to original coordinates is
   where nearly every bug lives.
9. **Assuming your KMP beats `in`.** Measure it. In CPython it usually does
   not, and claiming otherwise is simply wrong.

---

## 12. Key Takeaways

✅ **Naive search is O(n·m)** because it discards what a mismatch taught it
✅ **Tries answer prefix questions** in O(m); a hash set cannot answer them at all
✅ **KMP** builds an LPS array so `i` never backs up — O(n + m), no bad inputs
✅ **Rabin-Karp** rolls a hash in O(1) per shift; always verify on a hit
✅ **Z-algorithm** is KMP's easier-to-derive cousin, same complexity
✅ **Aho-Corasick** = trie + failure links: k patterns in ONE pass
✅ **Suffix array + LCP** answers repeated/common-substring questions in O(n log n)
✅ **Manacher** finds every palindromic substring in O(n) via symmetry reuse
✅ **Use the built-ins** for ordinary search; these algorithms are for the
   problems built-ins cannot express

**Interview Focus**:
- Derive the LPS array by hand on a small pattern; that is the actual test
- Explain *why* KMP is O(n): `i` is monotonic, `j` decreases only via `lps`
- Mention the Rabin-Karp verification step unprompted — interviewers watch for it
- Recognize "multiple patterns" → Aho-Corasick, "autocomplete" → trie,
  "longest repeated substring" → suffix array
- Say out loud that `str.find` is the right answer for the simple case

**You have reached the end of the learning path.** Eighteen topics, from
Big-O notation to suffix arrays. Go build something.
