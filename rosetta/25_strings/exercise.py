"""
Rosetta Code Challenges -- Strings

Five string tasks. Descriptions written for this platform.
"""

from typing import Dict, List

print("=" * 70)
print("ROSETTA CODE: Strings")
print("=" * 70)

# ==================== EASY ====================
print("\n[EASY PROBLEMS]")
print("-" * 70)

print("\n1. COUNT OCCURRENCES OF A SUBSTRING")
print("Input: A string and a substring")
print("Output: How many times it appears, without overlapping")
print("Example: 'the three truths','th' -> 3;  'ababababab','abab' -> 2")
def count_substring(text: str, needle: str) -> int:
    """
    Non-overlapping: after a match, continue from the end of it. 'ababababab'
    contains 'abab' twice by that rule, not four times.

    An empty needle has no sensible answer; return 0.
    """
    # TODO: Write your code here
    pass

print("\n2. LETTER FREQUENCY")
print("Input: A string")
print("Output: A map from each letter to how often it appears")
print("Example: 'Hello' -> {'h':1,'e':1,'l':2,'o':1}")
def letter_frequency(text: str) -> Dict[str, int]:
    """
    Letters only -- skip digits, spaces and punctuation. Case-insensitive, and
    the keys come back lower case. Letters that do not appear are absent from
    the map rather than present with a zero.
    """
    # TODO: Write your code here
    pass

# ==================== MEDIUM ====================
print("\n\n[MEDIUM PROBLEMS]")
print("-" * 70)

print("\n3. BALANCED BRACKETS")
print("Input: A string of brackets")
print("Output: True if every bracket is closed in the right order")
print("Example: '[[]]' -> True,  '][' -> False,  '' -> True")
def is_balanced(text: str) -> bool:
    """
    Handle (), [] and {}. A stack is the whole trick: push an opener, and on a
    closer check that it matches what you pop.

    Two failures to get right: closing something that was never opened, and
    reaching the end with openers still on the stack.
    """
    # TODO: Write your code here
    pass

print("\n4. COMMA QUIBBLING")
print("Input: A list of words")
print("Output: Them joined in English, wrapped in braces")
print("Example: [] -> '{}',  ['ABC'] -> '{ABC}',  ['A','B','C'] -> '{A, B and C}'")
def quibble(words: List[str]) -> str:
    """
    Commas between all but the last pair, which is joined with ' and '. Empty
    input gives '{}'.

    The interesting part is that the separator is not uniform, so a plain join
    cannot do it alone.
    """
    # TODO: Write your code here
    pass

print("\n5. WORD WRAP")
print("Input: A string and a line width")
print("Output: The text broken into lines no longer than the width")
print("Example: width 10 -> ['the quick','brown fox']")
def word_wrap(text: str, width: int) -> List[str]:
    """
    Greedy wrapping: put as many words on a line as fit, then start the next.
    Split on whitespace and join with single spaces; do not break a word, even
    one longer than the width -- it gets a line to itself.

    Return an empty list for empty input.
    """
    # TODO: Write your code here
    pass
