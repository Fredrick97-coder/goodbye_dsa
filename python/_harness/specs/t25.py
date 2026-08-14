"""Specs for Rosetta module 25 -- Strings."""

import re

from ..spec import spec


def _ref_count_substring(text, needle):
    return text.count(needle) if needle else 0


def _ref_letter_frequency(text):
    out = {}
    for ch in text.lower():
        if ch.isalpha() and ch.isascii():
            out[ch] = out.get(ch, 0) + 1
    return out


def _ref_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def _ref_quibble(words):
    if not words:
        return "{}"
    if len(words) == 1:
        return "{" + words[0] + "}"
    return "{" + ", ".join(words[:-1]) + " and " + words[-1] + "}"


def _ref_word_wrap(text, width):
    words = text.split()
    if not words:
        return []
    lines, current = [], words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def g_brackets(rng):
    return ("".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 12))),)


def g_words(rng):
    pool = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
            "extraordinarily", "a"]
    return (" ".join(rng.choice(pool) for _ in range(rng.randint(0, 14))),
            rng.randint(5, 20))


SPECS = [
    spec(1, "count_substring", ref=_ref_count_substring,
         gen=lambda r: ("".join(r.choice("ab") for _ in range(r.randint(0, 16))),
                        "".join(r.choice("ab") for _ in range(r.randint(1, 3)))),
         cases=[(("the three truths", "th"), 3),
                (("ababababab", "abab"), 2),
                (("aaa", "aa"), 1),
                (("abc", "d"), 0),
                (("abc", ""), 0)],
         note="non-overlapping, so 'ababababab' contains 'abab' twice"),

    spec(2, "letter_frequency", ref=_ref_letter_frequency,
         gen=lambda r: ("".join(r.choice("aabBc! 12") for _ in range(r.randint(0, 20))),),
         cases=[(("Hello",), {"h": 1, "e": 1, "l": 2, "o": 1}),
                (("",), {}),
                (("A a! 1",), {"a": 2})],
         note="letters only, lower-cased keys, absent letters omitted"),

    spec(3, "is_balanced", ref=_ref_balanced, gen=g_brackets,
         cases=[(("",), True), (("[]",), True), (("[[]]",), True),
                (("][",), False), (("([)]",), False), (("{[()]}",), True),
                (("(",), False)],
         note="handles (), [] and {}; the empty string is balanced"),

    spec(4, "quibble", ref=_ref_quibble,
         gen=lambda r: ([r.choice(["ABC", "DEF", "G", "HI"])
                         for _ in range(r.randint(0, 6))],),
         cases=[(([],), "{}"), ((["ABC"],), "{ABC}"),
                ((["ABC", "DEF"],), "{ABC and DEF}"),
                ((["A", "B", "C"],), "{A, B and C}")],
         note="commas between all but the final pair, which uses ' and '"),

    spec(5, "word_wrap", ref=_ref_word_wrap, gen=g_words,
         cases=[(("the quick brown fox", 10), ["the quick", "brown fox"]),
                (("", 10), []),
                (("extraordinarily long", 5), ["extraordinarily", "long"]),
                (("a b c", 1), ["a", "b", "c"])],
         note="greedy; never break a word, even one wider than the limit"),
]
