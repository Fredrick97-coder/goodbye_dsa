"""Specs for Topic 09 -- Hash Maps."""

from collections import Counter, defaultdict

from ..spec import as_sorted, as_sorted_inner, spec


def _two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def _first_unique(s):
    c = Counter(s)
    for i, ch in enumerate(s):
        if c[ch] == 1:
            return i
    return -1


def _group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups["".join(sorted(s))].append(s)
    return list(groups.values())


def _majority(nums):
    return Counter(nums).most_common(1)[0][0]


def _word_pattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):
        return False
    fwd, back = {}, {}
    for p, w in zip(pattern, words):
        if fwd.setdefault(p, w) != w or back.setdefault(w, p) != p:
            return False
    return True


def _longest_unique(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for ch in s[i:]:
            if ch in seen:
                break
            seen.add(ch)
        best = max(best, len(seen))
    return best


def _find_anagrams(s, p):
    need = Counter(p)
    n = len(p)
    return [i for i in range(len(s) - n + 1) if Counter(s[i:i + n]) == need]


def _valid_sudoku(board):
    seen = set()
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == ".":
                continue
            keys = [("r", r, v), ("c", c, v), ("b", r // 3, c // 3, v)]
            for k in keys:
                if k in seen:
                    return False
                seen.add(k)
    return True


def g_nums_target(rng):
    nums = [rng.randint(-15, 15) for _ in range(rng.randint(2, 12))]
    return (nums, rng.randint(-20, 20))


def g_str(rng, alphabet="abc", lo=0, hi=12):
    return ("".join(rng.choice(alphabet) for _ in range(rng.randint(lo, hi))),)


def g_words(rng):
    return ([("".join(rng.choice("abc") for _ in range(rng.randint(1, 4))))
             for _ in range(rng.randint(0, 8))],)


def g_majority(rng):
    n = rng.randint(1, 9)
    maj = rng.randint(0, 5)
    arr = [maj] * (n + 1) + [rng.randint(6, 9) for _ in range(n)]
    rng.shuffle(arr)
    return (arr,)


VALID_SUDOKU = [
    list("53..7...."), list("6..195..."), list(".98....6."),
    list("8...6...3"), list("4..8.3..1"), list("7...2...6"),
    list(".6....28."), list("...419..5"), list("....8..79"),
]
BAD_SUDOKU = [row[:] for row in VALID_SUDOKU]
BAD_SUDOKU[0][1] = "5"          # duplicate 5 in row 0

SPECS = [
    spec(1, "two_sum", ref=_two_sum, gen=g_nums_target,
         cases=[(([2, 7, 11, 15], 9), [0, 1])]),
    spec(2, "is_anagram", ref=lambda a, b: sorted(a) == sorted(b),
         gen=lambda r: (g_str(r)[0], g_str(r)[0]),
         cases=[(("anagram", "nagaram"), True), (("rat", "car"), False)]),
    spec(3, "contains_duplicate", ref=lambda a: len(a) != len(set(a)),
         gen=lambda r: ([r.randint(0, 8) for _ in range(r.randint(0, 12))],),
         cases=[(([1, 2, 3, 1],), True), (([1, 2, 3],), False)]),
    spec(4, "first_unique_char", ref=_first_unique, gen=g_str,
         cases=[(("leetcode",), 0), (("aabb",), -1)]),
    spec(5, "group_anagrams", ref=_group_anagrams, gen=g_words,
         norm=as_sorted_inner,
         cases=[((["eat", "tea", "tan", "ate", "nat", "bat"],),
                 [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]])]),
    spec(6, "majority_element", ref=_majority, gen=g_majority,
         cases=[(([3, 2, 3],), 3), (([2, 2, 1, 1, 1, 2, 2],), 2)]),
    spec(7, "is_valid_sudoku",
         cases=[((VALID_SUDOKU,), True), ((BAD_SUDOKU,), False)]),
    spec(8, "word_pattern", ref=_word_pattern,
         gen=lambda r: ("".join(r.choice("ab") for _ in range(r.randint(1, 4))),
                        " ".join(r.choice(["dog", "cat"])
                                 for _ in range(r.randint(1, 4)))),
         cases=[(("abba", "dog cat cat dog"), True),
                (("abba", "dog cat cat fish"), False),
                (("aaaa", "dog cat cat dog"), False)]),
    spec(10, "length_of_longest_substring", ref=_longest_unique,
         gen=lambda r: g_str(r, "abcd", 0, 14),
         cases=[(("abcabcbb",), 3), (("",), 0)]),
    spec(11, "find_anagrams", ref=_find_anagrams,
         gen=lambda r: (g_str(r, "ab", 0, 12)[0], g_str(r, "ab", 1, 3)[0]),
         cases=[(("cbaebabacd", "abc"), [0, 6]), (("abab", "ab"), [0, 1, 2])]),
    spec(12, "top_k_frequent", norm=as_sorted,
         cases=[(([1, 1, 1, 2, 2, 3], 2), [1, 2]), (([1], 1), [1])]),
]
