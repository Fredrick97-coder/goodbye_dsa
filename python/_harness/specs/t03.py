"""Specs for Topic 03 -- Strings."""

from collections import Counter

from ..spec import spec


def _is_pal(s):
    """Alphanumeric-only, case-insensitive -- the usual convention."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]


def _first_unique(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


def _valid_parens(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def _longest_unique_substr(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
        best = max(best, len(seen))
    return best


def _is_rotation(a, b):
    return len(a) == len(b) and b in (a + a)


def _longest_pal(s):
    if not s:
        return ""
    best = s[0]
    for i in range(len(s)):
        for j in range(i + len(best), len(s) + 1):
            sub = s[i:j]
            if sub == sub[::-1] and len(sub) > len(best):
                best = sub
    return best


def _compress(s):
    if not s:
        return ""
    out = []
    run = 1
    for i in range(1, len(s) + 1):
        if i < len(s) and s[i] == s[i - 1]:
            run += 1
        else:
            out.append(s[i - 1] + (str(run) if run > 1 else ""))
            run = 1
    return "".join(out)


def _min_window(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        have = Counter()
        for j in range(i, len(s)):
            have[s[j]] += 1
            if all(have[c] >= n for c, n in need.items()):
                cand = s[i:j + 1]
                if not best or len(cand) < len(best):
                    best = cand
                break
    return best


def _edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def g_str(rng, alphabet="abc", lo=0, hi=10):
    return ("".join(rng.choice(alphabet) for _ in range(rng.randint(lo, hi))),)


def g_two_str(rng, alphabet="abc", hi=8):
    return (g_str(rng, alphabet, 0, hi)[0], g_str(rng, alphabet, 0, hi)[0])


def g_parens(rng):
    return ("".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 10))),)


SPECS = [
    spec(1, "reverse_string", ref=lambda s: s[::-1], gen=g_str,
         cases=[(("hello",), "olleh"), (("",), "")]),
    spec(2, "is_palindrome", ref=_is_pal,
         gen=lambda r: g_str(r, "aA b1", 0, 10),
         cases=[(("racecar",), True), (("hello",), False),
                (("A man, a plan, a canal: Panama",), True), (("",), True)],
         note="alphanumeric only, case-insensitive"),
    spec(3, "is_anagram", ref=lambda a, b: sorted(a) == sorted(b),
         gen=g_two_str,
         cases=[(("listen", "silent"), True), (("ab", "abc"), False)]),
    spec(4, "count_vowels", ref=lambda s: sum(c in "aeiouAEIOU" for c in s),
         gen=lambda r: g_str(r, "aeiouxyz", 0, 12),
         cases=[(("hello",), 2), (("xyz",), 0)]),
    spec(5, "first_unique_char", ref=_first_unique, gen=g_str,
         cases=[(("leetcode",), 0), (("aabb",), -1), (("",), -1)]),
    spec(6, "is_valid_parentheses", ref=_valid_parens, gen=g_parens,
         cases=[(("()[]{}",), True), (("(]",), False), (("",), True),
                (("([)]",), False)]),
    spec(7, "length_of_longest_substring", ref=_longest_unique_substr,
         gen=lambda r: g_str(r, "abcd", 0, 14),
         cases=[(("abcabcbb",), 3), (("bbbbb",), 1), (("",), 0)]),
    spec(8, "is_rotation", ref=_is_rotation, gen=g_two_str,
         cases=[(("waterbottle", "erbottlewat"), True),
                (("abc", "acb"), False)]),
    spec(9, "longest_palindrome",
         prop=lambda s: None if s is None else (len(s), s == s[::-1]),
         gen=lambda r: g_str(r, "ab", 1, 12),
         ref=lambda s: (len(_longest_pal(s)), True),
         cases=[(("babad",), (3, True)), (("cbbd",), (2, True)),
                (("a",), (1, True))],
         note="any longest palindrome is accepted"),
    spec(10, "compress_string", ref=_compress,
         gen=lambda r: g_str(r, "aab", 0, 12),
         cases=[(("aabcccccaaa",), "a2bc5a3"), (("abc",), "abc"),
                (("",), "")],
         note="runs of 1 keep no digit: 'abc' -> 'abc'"),
    # `prop` is applied to the ACTUAL only, so a `ref` paired with it must
    # already return the transformed value -- here, the length.
    spec(11, "min_window_substring",
         ref=lambda s, t: len(_min_window(s, t)),
         gen=lambda r: (g_str(r, "abc", 0, 12)[0], g_str(r, "abc", 0, 3)[0]),
         prop=lambda s: None if s is None else len(s),
         cases=[(("ADOBECODEBANC", "ABC"), 4), (("a", "aa"), 0)],
         note="only the length is compared, so equally short windows both pass"),
    spec(12, "edit_distance", ref=_edit_distance, gen=g_two_str,
         cases=[(("horse", "ros"), 3), (("", "abc"), 3), (("a", "a"), 0)]),
]
