"""
Exercises: Tries & String Algorithms

Practice tries, KMP, Rabin-Karp, Z-algorithm, Aho-Corasick,
suffix arrays, and Manacher's algorithm.
"""

from typing import List, Tuple, Dict, Optional

print("=" * 70)
print("EXERCISES: Tries & String Algorithms")
print("=" * 70)


class TrieNode:
    """Provided for you."""
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_word = False
        self.count = 0          # words passing through this node


# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. TRIE: INSERT AND SEARCH")
print("Input: A sequence of words, then query words")
print("Output: True for exact stored words, False otherwise")
print("Example: insert 'cat' -> search('cat')=True, search('ca')=False")
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        # TODO: Walk from the root, creating a child node for each missing
        # character. Mark the FINAL node with is_word = True.
        pass

    def search(self, word: str) -> bool:
        # TODO: Walk the word. Return False if any character is missing.
        # At the end, return node.is_word -- reaching a node is not enough.
        pass

    def starts_with(self, prefix: str) -> bool:
        # TODO: Same walk, but reaching the end is sufficient. No is_word check.
        pass

print("\n2. COUNT WORDS WITH A GIVEN PREFIX")
print("Input: A trie and a prefix")
print("Output: How many stored words start with it")
print("Example: {'car','card','care'} with prefix 'car' -> 3")
def count_prefix(trie: Trie, prefix: str) -> int:
    # TODO: Maintain a `count` on each node during insert (increment it for
    # every node you pass through). Then this is one walk + one field read.
    # The alternative -- DFS-counting the subtree -- also works but is O(k).
    pass

print("\n3. AUTOCOMPLETE")
print("Input: A trie and a prefix")
print("Output: All stored words starting with that prefix, sorted")
print("Example: prefix 'ca' -> ['car', 'card', 'care', 'cat']")
def autocomplete(trie: Trie, prefix: str) -> List[str]:
    # TODO: Walk to the prefix node, then DFS the subtree collecting every
    # node with is_word set. Iterate children in sorted order for sorted output.
    pass

print("\n4. LONGEST COMMON PREFIX OF A WORD LIST")
print("Input: List of strings")
print("Output: Their longest shared prefix")
print("Example: ['flower','flow','flight'] -> 'fl'")
def longest_common_prefix(words: List[str]) -> str:
    # TODO: Two options. (a) Build a trie and walk down while each node has
    # exactly one child and is not a word end. (b) Compare characters column
    # by column -- simpler and O(total chars). Implement either; note which
    # one you would use in an interview and why.
    pass

print("\n5. BUILD THE LPS (FAILURE) ARRAY")
print("Input: A pattern string")
print("Output: lps[i] = longest proper prefix of pattern[0..i] that is also")
print("        a suffix of it")
print("Example: 'ababcabab' -> [0,0,1,2,0,1,2,3,4]")
def build_lps(pattern: str) -> List[int]:
    # TODO: Track `length` = current match length, starting at 0.
    # For i from 1: while length > 0 and mismatch, fall back with
    # length = lps[length - 1]. On a match, length += 1. Store lps[i] = length.
    # It is lps[length - 1], NOT lps[length] -- the latter loops forever.
    pass

print("\n6. NAIVE PATTERN SEARCH (THE BASELINE)")
print("Input: Text and pattern")
print("Output: All starting indices where pattern occurs")
print("Example: 'aaaa', 'aa' -> [0, 1, 2]  (overlaps count)")
def naive_search(text: str, pattern: str) -> List[int]:
    # TODO: Check every start position. Write this first -- you need a
    # brute-force reference to verify every clever algorithm below.
    pass


# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n7. KMP SEARCH")
print("Input: Text and pattern")
print("Output: All match positions, in O(n + m)")
print("Example: 'ababcababcabc', 'abc' -> [2, 7, 10]")
def kmp_search(text: str, pattern: str) -> List[int]:
    # TODO: Build the LPS, then sweep the text with j = chars matched.
    # On a mismatch: j = lps[j-1] and DO NOT advance i -- that is the
    # whole trick. On a full match, record it and set j = lps[j-1] so
    # overlapping occurrences are still found.
    # Guard the empty pattern.
    pass

print("\n8. RABIN-KARP SEARCH")
print("Input: Text and pattern")
print("Output: All match positions, using a rolling hash")
print("Example: expected O(n + m); worst case O(n * m)")
def rabin_karp(text: str, pattern: str, base: int = 256,
               mod: int = 1_000_000_007) -> List[int]:
    # TODO: Hash the pattern and the first window. Then slide:
    #   win = ((win - ord(text[i]) * base^(m-1)) * base + ord(text[i+m])) % mod
    # Precompute base^(m-1) with pow(base, m-1, mod).
    # CRITICAL: on a hash match you MUST still compare the actual substring.
    # Hashes collide. Skipping that check makes the algorithm merely probable.
    pass

print("\n9. Z-FUNCTION")
print("Input: A string")
print("Output: z[i] = length of the longest substring at i that matches")
print("        a prefix of the whole string")
print("Example: 'aabcaabxaaaz' -> [_,1,0,0,3,1,0,0,2,2,1,0]")
def z_function(s: str) -> List[int]:
    # TODO: Maintain the rightmost known match window [left, right).
    # If i < right, seed z[i] = min(right - i, z[i - left]) to reuse prior
    # work, then extend by brute force. Update the window when you pass it.
    pass

print("\n10. PATTERN SEARCH VIA THE Z-FUNCTION")
print("Input: Text and pattern")
print("Output: Match positions")
print("Example: build pattern + separator + text, then look for z[i] == m")
def z_search(text: str, pattern: str) -> List[int]:
    # TODO: Concatenate with a separator that CANNOT appear in either
    # string -- '\\x00' is the safe choice. Any position where z equals
    # len(pattern) is a match; convert the index back to text coordinates.
    pass

print("\n11. IMPLEMENT A WORD DICTIONARY WITH WILDCARDS")
print("Input: Words to add, then search patterns where '.' matches any char")
print("Output: True if any stored word matches the pattern")
print("Example: add 'bad','dad' -> search('.ad') = True, search('b..') = True")
class WildcardDictionary:
    def __init__(self):
        self.root = TrieNode()

    def add(self, word: str) -> None:
        # TODO: Ordinary trie insert.
        pass

    def search(self, pattern: str) -> bool:
        # TODO: DFS with backtracking. On a literal character, follow that one
        # child. On '.', try EVERY child. This is why a trie beats a regex scan
        # here -- shared prefixes are explored once, not once per word.
        pass

print("\n12. REPLACE WORDS WITH THEIR SHORTEST ROOT")
print("Input: A list of roots, and a sentence")
print("Output: Each word replaced by the shortest root that prefixes it")
print("Example: roots ['cat','bat','rat'], 'the cattle was rattled'")
print("         -> 'the cat was rat'")
def replace_words(roots: List[str], sentence: str) -> str:
    # TODO: Build a trie of roots. For each word, walk down and stop at the
    # FIRST node marked is_word -- that is the shortest matching root.
    # This is the same longest/shortest-prefix-match idea IP routers use.
    pass

print("\n13. LONGEST REPEATED SUBSTRING")
print("Input: A string")
print("Output: The longest substring occurring at least twice")
print("Example: 'banana' -> 'ana'")
def longest_repeated_substring(s: str) -> str:
    # TODO: Build the suffix array and the LCP array. The answer is the
    # substring at the position of max(lcp) -- two adjacent sorted suffixes
    # sharing k characters means that k-length string appears twice.
    pass


# ==================== HARD ====================
print("\n\n[HARD PROBLEMS]")
print("-" * 70)

print("\n14. BUILD A SUFFIX ARRAY")
print("Input: A string")
print("Output: Indices of all suffixes in sorted order")
print("Example: 'banana' -> [5, 3, 1, 0, 4, 2]")
def build_suffix_array(s: str) -> List[int]:
    # TODO: Prefix doubling. Rank each position by its first character, then
    # repeatedly sort by the PAIR (rank[i], rank[i+k]) and re-rank, doubling
    # k each round. Stop when all ranks are distinct.
    # O(n log^2 n) with a comparison sort -- good enough. O(n) algorithms
    # (SA-IS, DC3) exist but are far more code.
    pass

print("\n15. BUILD THE LCP ARRAY (KASAI'S ALGORITHM)")
print("Input: A string and its suffix array")
print("Output: lcp[i] = common prefix length of sa[i] and sa[i-1]")
print("Example: 'banana' -> [0, 1, 3, 0, 0, 2]")
def build_lcp(s: str, sa: List[int]) -> List[int]:
    # TODO: Invert sa into rank. Walk the ORIGINAL string positions i = 0..n-1
    # carrying h (the current LCP length). Extend h by comparison, store it,
    # then decrement h by one before moving on. That single decrement is the
    # amortization trick that makes the whole thing O(n).
    pass

print("\n16. AHO-CORASICK: MULTI-PATTERN SEARCH")
print("Input: A list of patterns, then a text")
print("Output: All (position, pattern) matches in ONE pass")
print("Example: ['he','she','his','hers'] in 'ushers' -> she@1, he@2, hers@2")
class AhoCorasick:
    def __init__(self, patterns: List[str]):
        # TODO: Build a trie (goto table), then compute failure links by BFS.
        # A node's failure link points to the longest proper suffix of its
        # string that is also a trie node.
        # CRITICAL: each node must INHERIT its failure target's output list,
        # or nested matches ('he' inside 'she') will be missed.
        pass

    def search(self, text: str) -> List[Tuple[int, str]]:
        # TODO: Single pass. On a character with no outgoing edge, follow
        # failure links until one exists or you reach the root. Report every
        # pattern in the current node's output list.
        pass

print("\n17. MANACHER'S ALGORITHM")
print("Input: A string")
print("Output: The longest palindromic substring, in O(n)")
print("Example: 'babad' -> 'bab' or 'aba' (both valid)")
def manacher(s: str) -> str:
    # TODO: Transform s into '#a#b#a#' so odd and even lengths are handled
    # uniformly. Track the rightmost palindrome [center, right). For each i
    # inside it, seed radius[i] from its MIRROR (2*center - i), capped at
    # right - i, then extend. Convert the best center/radius back to original
    # coordinates -- start = (best - radius[best]) // 2.
    # The index arithmetic is where nearly every bug lives. Test on 'a',
    # 'aa', 'aba', 'abba', and ''.
    pass

print("\n18. SHORTEST PALINDROME BY PREPENDING")
print("Input: A string")
print("Output: The shortest palindrome formable by adding characters in front")
print("Example: 'aacecaaa' -> 'aaacecaaa'")
def shortest_palindrome(s: str) -> str:
    # TODO: Elegant KMP trick. Build combined = s + separator + reverse(s),
    # then compute its LPS. The final LPS value is the length of the longest
    # palindromic PREFIX of s. Prepend the reverse of the remaining tail.
    pass

print("\n19. LONGEST COMMON SUBSTRING OF TWO STRINGS")
print("Input: Two strings")
print("Output: Their longest shared contiguous substring")
print("Example: 'programming', 'gaming' -> 'ming'")
def longest_common_substring(a: str, b: str) -> str:
    # TODO: Concatenate a + separator + b, build the suffix array and LCP.
    # Scan adjacent pairs and keep the max LCP where the two suffixes come
    # from DIFFERENT halves (compare their start index against len(a)).
    # Without that cross-boundary check you would match a against itself.
    pass


# ==================== CHALLENGE ====================
print("\n[CHALLENGE PROBLEMS]")
print("-" * 70)

print("\n20. COUNT DISTINCT SUBSTRINGS")
print("Input: A string")
print("Output: The number of distinct non-empty substrings")
print("Example: 'banana' -> 15")
def count_distinct_substrings(s: str) -> int:
    # TODO: Total substrings is n(n+1)/2. Every LCP value counts substrings
    # that were already seen in an earlier suffix, so subtract sum(lcp).
    # One line once you have the suffix array and LCP -- but be sure you can
    # explain WHY it works.
    pass

print("\n21. STREAM CHECKER (KMP OVER A LIVE STREAM)")
print("Input: A set of words, then characters arriving one at a time")
print("Output: After each character, whether any word just completed")
print("Example: this is where KMP's 'never back up' property earns its keep")
class StreamChecker:
    def __init__(self, words: List[str]):
        # TODO: Build an Aho-Corasick automaton over the words. Keep the
        # current automaton state as your only mutable data.
        # Note: a trie of REVERSED words plus a bounded history buffer also
        # works, but the automaton needs no buffer at all.
        pass

    def query(self, letter: str) -> bool:
        # TODO: Advance one state transition (following failure links as
        # needed) and report whether the new state has any output.
        # O(1) amortized per character, O(1) extra space. You cannot re-read
        # the stream, which rules out most other algorithms.
        pass

print("\n22. COMPRESSED TRIE (RADIX TREE)")
print("Input: A word list")
print("Output: A trie where non-branching chains are collapsed into one edge")
print("Example: 'romane','romanus','romulus' -> ~5 nodes instead of ~15")
class RadixTree:
    def __init__(self):
        # TODO: Each edge holds a SUBSTRING, not a single character.
        pass

    def insert(self, word: str) -> None:
        # TODO: Walk edges matching as far as they agree. On a partial match,
        # SPLIT that edge into a shared prefix plus two children. This split
        # case is the entire difficulty -- handle it before anything else.
        pass

    def search(self, word: str) -> bool:
        # TODO: Follow edges, consuming whole substrings at a time.
        pass

    def node_count(self) -> int:
        # TODO: Count nodes and compare against a plain trie on the same
        # input. Report the reduction -- that is the point of the structure.
        pass

print("\n23. WILDCARD AND REGEX-LITE MATCHING")
print("Input: A string and a pattern with '?' (one char) and '*' (any run)")
print("Output: Whether the pattern matches the whole string")
print("Example: ('adceb', '*a*b') -> True")
def wildcard_match(s: str, pattern: str) -> bool:
    # TODO: This one is DP, not a string-search algorithm -- included so you
    # can feel the difference. dp[i][j] = does s[:i] match pattern[:j]?
    # '*' either consumes nothing (dp[i][j-1]) or one more char (dp[i-1][j]).
    # There is a greedy two-pointer solution in O(1) space; try DP first,
    # then find the greedy one.
    pass

print("\n24. BURROWS-WHEELER TRANSFORM")
print("Input: A string")
print("Output: Its BWT, plus the inverse transform to recover the original")
print("Example: 'banana$' -> 'annb$aa'; this is how bzip2 works")
def bwt_transform(s: str) -> str:
    # TODO: Append a sentinel '$' that sorts before everything. The BWT is
    # the last character of each row of the sorted rotation matrix -- which
    # you can read straight off the suffix array: s[sa[i] - 1].
    pass

def bwt_inverse(bwt: str) -> str:
    # TODO: Repeated sorting reconstruction, or the LF-mapping. The fact that
    # this is invertible AT ALL is the surprise worth understanding.
    pass

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
Tries & String Algorithms Cheat Sheet:

1. The Core Insight:
   Naive search is O(n*m) because it THROWS AWAY what a mismatch taught it
   and restarts at i+1. Every fast algorithm below is a different way of
   keeping that information:
     KMP           remembers prefix-suffix overlaps (the LPS array)
     Z-algorithm   remembers the rightmost match window
     Rabin-Karp    remembers a rolling hash of the window
     Aho-Corasick  remembers all patterns at once (trie + failure links)
     Suffix array  remembers the sorted order of every suffix

2. Tries:
   insert / search / prefix-exists : O(m) in the key length
   space                           : O(total characters)

   Use a trie for PREFIX questions -- autocomplete, longest-prefix match,
   wildcard search, shared-prefix traversal.
   Use a hash set for EXACT membership. It is faster and smaller.
   A trie that never answers a prefix query is the wrong data structure.

   Radix tree (compressed trie) collapses non-branching chains. Used by
   IP routing tables, git's object store, Ethereum's Patricia trie.

3. KMP:
   lps[i] = longest proper prefix of pattern[0..i] that is also its suffix.

   Search : i NEVER decreases. On a mismatch, j = lps[j-1] shifts the
            PATTERN, not the text pointer. That is the whole algorithm.
   Time   : O(n + m). Worst case equals best case -- no bad inputs.
   Overlaps: after a hit, j = lps[j-1]. Setting j = 0 misses overlaps.
   Gotcha : lps[j-1], never lps[j]. The latter loops forever.

4. Rabin-Karp:
   Rolling hash, O(1) per shift:
     win = ((win - ord(out) * base^(m-1)) * base + ord(in)) % mod

   ALWAYS verify a hash match against the real substring. Hashes collide.
   Best for: many same-length patterns (hash them into a set, one pass),
   2D patch matching, and fingerprinting (rsync, dedup storage).
   Time: O(n + m) expected, O(n*m) worst case.

5. Z-Algorithm:
   z[i] = longest substring at i matching a prefix of the whole string.
   Same O(n) as KMP but easier to derive under pressure. For matching,
   build pattern + '\\x00' + text and look for z[i] == len(pattern).
   Also yields periodicity, distinct substring counts, minimal rotation.

6. Aho-Corasick:
   A trie plus KMP-style failure links. Finds ALL k patterns in ONE pass.
   Time  : O(n + total pattern length + number of matches)
   vs KMP: running KMP k times costs O(k*n) -- the gap grows with k.
   CRITICAL: a node must inherit its failure target's output list, or
   nested matches ('he' inside 'she') go unreported.
   Real use: Snort IDS, ClamAV, spam filters, grep -F, DNA motif search.

7. Suffix Arrays:
   The sorted order of all suffixes. A suffix tree's memory-efficient cousin.
   Build : O(n log^2 n) by prefix doubling (O(n) via SA-IS / DC3)
   Search: O(m log n) by binary search -- matches form a contiguous range

   With the LCP array (Kasai, O(n)) you get:
     longest repeated substring   = max(lcp)
     distinct substring count     = n(n+1)/2 - sum(lcp)
     longest common substring     = max cross-boundary lcp after concat

   The economics: build ONCE, query forever. For a single query, use KMP.
   Real use: BWA/Bowtie read aligners, bzip2 (via BWT), full-text indexes.

8. Manacher's Algorithm:
   Every palindromic substring in O(n) by reusing palindrome symmetry.
   Transform to '#a#b#a#' so odd and even centers unify.
   Seed each radius from its mirror, capped by the current right boundary.
   Honest note: on RANDOM text the naive O(n^2) expansion is competitive,
   because each center fails fast and there is no preprocessing. Manacher's
   value is the GUARANTEE on repetitive input, not the average case.

Complexity Reference:

Algorithm        Preprocess    Search       Space    Best for
─────────────────────────────────────────────────────────────────────────
Naive            -             O(n*m)       O(1)     tiny one-off inputs
KMP              O(m)          O(n)         O(m)     single pattern, streaming
Rabin-Karp       O(m)          O(n) exp.    O(1)     many equal-length patterns
Z-algorithm      -             O(n+m)       O(n)     prefix problems
Boyer-Moore      O(m+sigma)    O(n/m) best  O(sigma) long patterns, big alphabet
Aho-Corasick     O(sum m)      O(n+z)       O(sum m) many patterns, one pass
Trie             O(sum m)      O(m)         O(sum m) prefix queries
Suffix array     O(n log n)    O(m log n)   O(n)     many queries, fixed text
Suffix automaton O(n)          O(m)         O(n*s)   all substrings, online
Manacher         -             O(n)         O(n)     palindromic substrings

sigma = alphabet size, z = match count, sum m = total pattern length.

Choosing an Approach:

  One pattern, one search
    -> text.find() / in / re. It is C-optimized. Do not hand-roll.
  One pattern, need a linear guarantee or a stream you cannot re-read
    -> KMP
  Many patterns, one text pass
    -> Aho-Corasick
  Many patterns, all the same length
    -> Rabin-Karp with a hash set
  Prefix queries (autocomplete, routing, spell check)
    -> Trie, or a radix tree if memory is tight
  Fixed text, many different pattern queries
    -> Suffix array + LCP (amortize the build)
  Palindromic substrings
    -> Manacher
  Longest repeated or common substring
    -> Suffix array + LCP

The Python Reality Check:

  CPython's str.find and `in` are implemented in C using a two-way
  (Crochemore-Perrin) algorithm. A hand-written KMP in pure Python will
  usually LOSE to text.find() despite identical asymptotics, often by an
  order of magnitude.

  This does not make these algorithms useless. It makes them the right tool
  for problems the built-ins cannot express:
    - multiple patterns simultaneously      -> Aho-Corasick
    - prefix and wildcard queries           -> trie
    - streaming input you cannot re-read    -> KMP
    - repeated-substring structure          -> suffix array
    - a hard guarantee on adversarial input -> KMP over naive

  Measure before claiming a speedup. "My KMP is faster than `in`" is
  almost always false in CPython.

Common Pitfalls:

1. Skipping Rabin-Karp's verification step. Hash equality is not string
   equality.
2. Writing lps[j] instead of lps[j-1] in the fallback. Infinite loop.
3. Setting j = 0 after a KMP match, which silently drops overlapping hits.
4. No empty-pattern guard. Every algorithm here needs one.
5. Forgetting Aho-Corasick's output inheritance -- nested matches vanish.
6. Choosing a separator that appears in the input. Use '\\x00' or '\\x01'.
7. Ignoring trie memory. A dict per node is ~200 bytes in CPython; a
   26-slot list or a radix tree is far leaner for a fixed alphabet.
8. Manacher index arithmetic. The transformed string has length 2n+1.
   Test '', 'a', 'aa', 'aba', 'abba' before trusting it.
9. Missing the cross-boundary check in longest-common-substring, which
   matches a string against itself.

Problem Recognition Guide:

"autocomplete / typeahead"              -> trie
"longest prefix match"                  -> trie / radix tree
"find all these words in this document" -> Aho-Corasick
"does this substring exist"             -> str.find, or KMP if streaming
"count occurrences of many k-grams"     -> Rabin-Karp
"longest repeated substring"            -> suffix array + LCP
"longest common substring"              -> suffix array + LCP
"longest palindromic substring"         -> Manacher
"is one string a rotation of another"   -> Z-algorithm, or s in (t+t)
"shortest palindrome by prepending"     -> KMP on s + sep + reverse(s)
"compress this text"                    -> BWT (suffix array) + Huffman

Interview Tips:

1. Derive the LPS array by hand on a 6-character pattern. That is the
   actual test -- reciting the code is not.
2. Explain WHY KMP is O(n): i is monotonically increasing, and j only
   decreases through lps, whose total decrease is bounded by m.
3. Mention Rabin-Karp's verification step WITHOUT being prompted.
   Interviewers specifically watch for whether you skip it.
4. Say "str.find would handle this" for the simple case before writing
   KMP. Reaching for a hand-rolled algorithm when a built-in exists is
   a signal you do not know the library.
5. For multi-pattern, name Aho-Corasick even if you cannot code it fully.
   Recognizing it is most of the credit.
6. Draw the trie. Every trie problem becomes obvious once drawn.

Learning Progression:

1. Basic: trie insert/search/prefix, naive search, the LPS array
2. Intermediate: KMP, Rabin-Karp, Z-function, wildcard trie search
3. Advanced: Aho-Corasick, suffix arrays, Kasai's LCP, Manacher
4. Expert: radix trees, suffix automata, BWT, persistent/compressed indexes

Next: Implement each stub, then run project.py to see these algorithms
powering a search engine, a content filter, a plagiarism detector, and
a DNA analyzer.

This is the FINAL topic of the learning path. Eighteen topics, from Big-O
notation to suffix arrays. Finish these exercises and you have covered the
full curriculum.
""")
