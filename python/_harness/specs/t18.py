"""Specs for Topic 18 -- Tries & String Algorithms.

The pattern-matching problems are all checked against a naive scan, which is
obviously correct and completely unlike the algorithms being tested.
"""

from ..spec import spec


def _naive_search(text, pattern):
    if not pattern:
        return []
    return [i for i in range(len(text) - len(pattern) + 1)
            if text[i:i + len(pattern)] == pattern]


def _build_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    for i in range(1, m):
        while length and pattern[i] != pattern[length]:
            length = lps[length - 1]
        if pattern[i] == pattern[length]:
            length += 1
        lps[i] = length
    return lps


def _z_function(s):
    n = len(s)
    z = [0] * n
    left = right = 0
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


def _lcp_of_words(words):
    if not words:
        return ""
    out = []
    for chars in zip(*words):
        if len(set(chars)) != 1:
            break
        out.append(chars[0])
    return "".join(out)


def _longest_repeated(s):
    """Longest substring occurring at least twice. Brute force."""
    n = len(s)
    for length in range(n - 1, 0, -1):
        seen = set()
        for i in range(n - length + 1):
            sub = s[i:i + length]
            if sub in seen:
                return sub
            seen.add(sub)
    return ""


def _suffix_array(s):
    return sorted(range(len(s)), key=lambda i: s[i:])


def _lcp_array(s, sa):
    n = len(s)
    if n == 0:
        return []
    lcp = [0] * n
    for i in range(1, n):
        a, b = sa[i - 1], sa[i]
        k = 0
        while a + k < n and b + k < n and s[a + k] == s[b + k]:
            k += 1
        lcp[i] = k
    return lcp


def _manacher_len(s):
    """Length of the longest palindromic substring, by brute force."""
    best = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            sub = s[i:j]
            if sub == sub[::-1]:
                best = max(best, len(sub))
    return best


def _shortest_palindrome(s):
    """Prepend the fewest characters. Brute force on the palindromic prefix."""
    if not s:
        return ""
    for k in range(len(s), 0, -1):
        if s[:k] == s[:k][::-1]:
            return s[k:][::-1] + s
    return s


def _longest_common_substring(a, b):
    best = ""
    for i in range(len(a)):
        for j in range(i + len(best) + 1, len(a) + 1):
            if a[i:j] in b:
                best = a[i:j]
            else:
                break
    return best


def _count_distinct_substrings(s):
    return len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)})


def _replace_words(roots, sentence):
    rs = sorted(roots, key=len)
    out = []
    for word in sentence.split():
        repl = word
        for r in rs:
            if word.startswith(r):
                repl = r
                break
        out.append(repl)
    return " ".join(out)


def _wildcard_match(s, pattern):
    """'?' one char, '*' any run. DP -- independent of a greedy solution."""
    m, n = len(s), len(pattern)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        if pattern[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[j - 1] == "*":
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[j - 1] == "?" or pattern[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]


def g_text_pattern(rng, alphabet="ab", tmax=14, pmax=4):
    text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, tmax)))
    pat = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, pmax)))
    return (text, pat)


def g_str(rng, alphabet="abc", lo=0, hi=12):
    return ("".join(rng.choice(alphabet) for _ in range(rng.randint(lo, hi))),)


def g_nonempty_str(rng, alphabet="ab", hi=10):
    return (g_str(rng, alphabet, 1, hi)[0],)


def g_words(rng):
    return ([g_str(rng, "ab", 1, 5)[0] for _ in range(rng.randint(0, 6))],)


SPECS = [
    spec(2, "Trie",
         script=lambda cls: (lambda t: [
             [t.insert(w) for w in ("cat", "car", "card")],
             t.search("car"), t.search("ca"), t.search("cards"),
             t.starts_with("ca"), t.starts_with("dog"),
         ][1:])(cls()),
         ref_script=lambda: [True, False, False, True, False]),
    spec(4, "longest_common_prefix", ref=_lcp_of_words, gen=g_words,
         cases=[((["flower", "flow", "flight"],), "fl"),
                ((["dog", "racecar"],), ""), (([],), "")]),
    spec(5, "build_lps", ref=_build_lps, gen=lambda r: g_nonempty_str(r),
         cases=[(("ababcabab",), [0, 0, 1, 2, 0, 1, 2, 3, 4]),
                (("aaaa",), [0, 1, 2, 3]), (("abc",), [0, 0, 0])]),
    spec(6, "naive_search", ref=_naive_search, gen=g_text_pattern,
         cases=[(("aaaa", "aa"), [0, 1, 2]),
                (("abcabc", "abc"), [0, 3]),
                (("abc", "xyz"), [])]),
    spec(7, "kmp_search", ref=_naive_search, gen=g_text_pattern,
         cases=[(("ababcababcabc", "abc"), [2, 7, 10]),
                (("aaaa", "aa"), [0, 1, 2]),
                (("abc", "xyz"), [])],
         note="overlapping matches must be reported"),
    spec(8, "rabin_karp", ref=_naive_search, gen=g_text_pattern,
         cases=[(("ababcababcabc", "abc"), [2, 7, 10]),
                (("aaaa", "aa"), [0, 1, 2])]),
    spec(9, "z_function", ref=_z_function, gen=lambda r: g_nonempty_str(r),
         cases=[(("aabcaabxaaaz",), [0, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0])],
         note="z[0] is conventionally 0 here"),
    spec(10, "z_search", ref=_naive_search, gen=g_text_pattern,
         cases=[(("ababcababcabc", "abc"), [2, 7, 10])]),
    spec(12, "replace_words", ref=_replace_words,
         gen=lambda r: (g_words(r)[0] or ["a"],
                        " ".join(g_str(r, "ab", 1, 5)[0]
                                 for _ in range(r.randint(1, 4)))),
         cases=[((["cat", "bat", "rat"], "the cattle was rattled by the battery"),
                 "the cat was rat by the bat")]),
    spec(13, "longest_repeated_substring",
         prop=lambda s: None if s is None else len(s),
         ref=lambda s: len(_longest_repeated(s)),
         gen=lambda r: g_nonempty_str(r, "ab", 12),
         cases=[(("banana",), 3), (("abcdef",), 0)],
         note="only the LENGTH is compared; ties are legitimate"),
    spec(14, "build_suffix_array", ref=_suffix_array,
         gen=lambda r: g_nonempty_str(r, "ab", 12),
         cases=[(("banana",), [5, 3, 1, 0, 4, 2])]),
    spec(15, "build_lcp", ref=_lcp_array,
         gen=lambda r: (lambda s: (s, _suffix_array(s)))(
             g_nonempty_str(r, "ab", 12)[0]),
         cases=[(("banana", [5, 3, 1, 0, 4, 2]), [0, 1, 3, 0, 0, 2])]),
    spec(17, "manacher", prop=lambda s: None if s is None else len(s),
         ref=lambda s: _manacher_len(s),
         gen=lambda r: g_nonempty_str(r, "ab", 14),
         cases=[(("babad",), 3), (("cbbd",), 2), (("a",), 1)],
         note="only the LENGTH is compared; several answers can tie"),
    spec(18, "shortest_palindrome", ref=_shortest_palindrome,
         gen=lambda r: g_str(r, "ab", 0, 10),
         cases=[(("aacecaaa",), "aaacecaaa"), (("abcd",), "dcbabcd"),
                (("",), "")]),
    spec(19, "longest_common_substring",
         prop=lambda s: None if s is None else len(s),
         ref=lambda a, b: len(_longest_common_substring(a, b)),
         gen=lambda r: (g_str(r, "ab", 0, 10)[0], g_str(r, "ab", 0, 10)[0]),
         cases=[(("programming", "gaming"), 4), (("abc", "xyz"), 0)],
         note="only the LENGTH is compared"),
    spec(20, "count_distinct_substrings", ref=_count_distinct_substrings,
         gen=lambda r: g_str(r, "ab", 0, 11),
         cases=[(("banana",), 15), (("aaa",), 3), (("",), 0)]),
    spec(23, "wildcard_match", ref=_wildcard_match,
         gen=lambda r: (g_str(r, "ab", 0, 8)[0],
                        "".join(r.choice("ab?*") for _ in range(r.randint(0, 6)))),
         cases=[(("adceb", "*a*b"), True), (("aa", "a"), False),
                (("aa", "*"), True), (("cb", "?a"), False),
                (("", "*"), True), (("", ""), True)]),
]


# ---------------------------------------------------------- added coverage

def _trie_of(module, words):
    """
    A trie built directly out of the provided TrieNode.

    `autocomplete` takes a trie, and building it with the learner's own Trie
    class would make problem 3 fail whenever problem 1 is unwritten. TrieNode
    is given to the learner complete, so the spec can assemble the structure
    itself and keep the two problems independent.
    """
    class _Holder:
        pass

    root = module.TrieNode()
    for word in words:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, module.TrieNode())
            node.count += 1
        node.is_word = True
    holder = _Holder()
    holder.root = root
    return holder


_AUTO_WORDS = ["car", "card", "care", "cat", "dog", "do"]


def c_autocomplete(module):
    trie = _trie_of(module, _AUTO_WORDS)
    return [((trie, "ca"), ["car", "card", "care", "cat"]),
            ((trie, "do"), ["do", "dog"]),
            ((trie, "z"), []),
            ((trie, ""), sorted(_AUTO_WORDS))]


def _ref_bwt(s):
    """BWT via the sorted rotations of s + sentinel."""
    text = s + "$"
    rotations = sorted(text[i:] + text[:i] for i in range(len(text)))
    return "".join(rot[-1] for rot in rotations)


def _ref_bwt_inverse(bwt):
    """
    Standard repeated-sorting reconstruction, returning the original WITHOUT
    the sentinel.
    """
    rows = [""] * len(bwt)
    for _ in range(len(bwt)):
        rows = sorted(bwt[i] + rows[i] for i in range(len(bwt)))
    for row in rows:
        if row.endswith("$"):
            return row[:-1]
    return ""


def g_bwt_text(rng):
    return ("".join(rng.choice("ab_n") for _ in range(rng.randint(1, 12))),)


def g_bwt_code(rng):
    return (_ref_bwt("".join(rng.choice("ab_n")
                             for _ in range(rng.randint(1, 12)))),)


def _ref_aho(patterns, text):
    """Brute force: every occurrence of every pattern, as (start, pattern)."""
    out = []
    for pat in patterns:
        if not pat:
            continue
        start = text.find(pat)
        while start != -1:
            out.append((start, pat))
            start = text.find(pat, start + 1)
    return out


def _as_hit_set(hits):
    if hits is None:
        return None
    return sorted(tuple(h) for h in hits)


def g_aho(rng):
    letters = "abc"
    patterns = sorted({"".join(rng.choice(letters)
                               for _ in range(rng.randint(1, 3)))
                       for _ in range(rng.randint(1, 4))})
    text = "".join(rng.choice(letters) for _ in range(rng.randint(0, 20)))
    return (patterns, text)


SPECS += [
    spec(1, "Trie",
         script=lambda cls: (lambda t: [
             [t.insert(w) for w in ("cat", "car", "care")],
             t.search("cat"), t.search("ca"), t.search("care"),
             t.search("dog"), t.search(""),
         ][1:])(cls()),
         ref_script=lambda: [True, False, True, False, False],
         note="insert cat/car/care, then search cat, ca, care, dog and the "
              "empty string. Reaching a node is not enough -- only words that "
              "were inserted count"),

    spec(3, "autocomplete", build_cases=c_autocomplete,
         note="results sorted; an empty prefix returns every word. The trie "
              "you are handed is already built, so this does not depend on "
              "problem 1"),

    spec(11, "WildcardDictionary",
         script=lambda cls: (lambda d: [
             [d.add(w) for w in ("bad", "dad", "mad")],
             d.search("pad"), d.search("bad"), d.search(".ad"),
             d.search("b.."), d.search("..."), d.search("b"),
         ][1:])(cls()),
         ref_script=lambda: [False, True, True, True, True, False],
         note="'.' matches exactly one character, so a pattern only matches "
              "words of the same length"),

    spec(16, "AhoCorasick",
         script=lambda cls: sorted(
             tuple(hit) for hit in
             cls(["he", "she", "his", "hers"]).search("ushers")),
         ref_script=lambda: sorted([(1, "she"), (2, "he"), (2, "hers")]),
         note="search returns (start_index, pattern) for EVERY occurrence, "
              "including overlaps -- 'she' at 1 and 'he' at 2 both count"),

    spec(21, "StreamChecker",
         script=lambda cls: (lambda sc: [sc.query(ch) for ch in "abcdef"])(
             cls(["cd", "f", "kl"])),
         ref_script=lambda: [False, False, False, True, False, True],
         note="query returns True when any stored word is a SUFFIX of the "
              "stream so far. Feeding a..f with words cd/f/kl: True at 'd' "
              "and at 'f'"),

    spec(22, "RadixTree",
         script=lambda cls: (lambda t: [
             [t.insert(w) for w in ("romane", "romanus", "romulus")],
             t.search("romane"), t.search("roman"), t.search("romulus"),
             t.search("rom"), t.search("romanu"),
         ][1:])(cls()),
         ref_script=lambda: [True, False, True, False, False],
         note="compression is an internal detail; what is graded is that "
              "search still answers exactly for stored words"),

    spec(24, "bwt_transform", ref=_ref_bwt, gen=g_bwt_text,
         cases=[(("banana",), "annb$aa")],
         note="the input does NOT carry the sentinel -- append '$' yourself. "
              "'banana' -> 'annb$aa', matching the stated example"),
    spec(24, "bwt_inverse", ref=_ref_bwt_inverse, gen=g_bwt_code,
         cases=[(("annb$aa",), "banana")],
         note="return the original string WITHOUT the sentinel"),

    # A second scenario for the same problem: nested and overlapping patterns
    # are where a wrong failure-link implementation shows up.
    spec(16, "AhoCorasick",
         script=lambda cls: sorted(
             tuple(hit) for hit in cls(["a", "ab", "bc"]).search("abcabc")),
         ref_script=lambda: sorted([(0, "a"), (0, "ab"), (1, "bc"),
                                    (3, "a"), (3, "ab"), (4, "bc")]),
         note="overlapping and nested patterns must all be reported"),
]
