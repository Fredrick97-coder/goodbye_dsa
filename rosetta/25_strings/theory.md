# Strings — Stacks, Tallies, and Separators

Four of the five tasks in this module are a single scan over a string. The fifth
is a greedy loop. What varies is what you carry as you go.

## A Stack Is the Answer to Nesting

**Balanced brackets** is the canonical use of a stack, and once you see the shape
you will recognise it in JSON parsers, expression evaluators and HTML validators.

Push every opener. On a closer, pop and check it matches:

```python
pairs = {")": "(", "]": "[", "}": "{"}
stack = []
for ch in text:
    if ch in "([{":
        stack.append(ch)
    elif ch in pairs:
        if not stack or stack.pop() != pairs[ch]:
            return False
return not stack
```

Two failures hide in that code and both are easy to omit:

- **Closing what was never opened** — `][`. The stack is empty when `]` arrives,
  so the `not stack` check is what catches it. Without it, `pop()` throws.
- **Ending with openers left** — `(`. The loop completes without a mismatch, so
  the *final* `return not stack` is what catches it.

A counter instead of a stack handles one bracket type and quietly accepts
`([)]`. Once there are two kinds of bracket, order matters, and only a stack
records order.

## Maps as Tallies

**Letter frequency** returns a map from letter to count. The pattern is the same
in every language:

```python
counts = {}
for ch in text.lower():
    if ch.isalpha():
        counts[ch] = counts.get(ch, 0) + 1
```

The decision worth being deliberate about is **absent versus zero**. This task
omits letters that never appear rather than listing them with a count of 0. Both
are defensible; they are different answers, and the tests pick one.

Note `.get(ch, 0)` — reading a missing key. Python raises `KeyError` on plain
indexing, JavaScript returns `undefined` and `undefined + 1` is `NaN`. Same bug,
two very different symptoms, which is why the default belongs in the read.

## Overlapping or Not

**Count occurrences of a substring** has one decision in it, and the statement
makes it: matches do not overlap.

```
'ababababab' contains 'abab' ... twice? or four times?
 abab                          -> positions 0 and 4     (non-overlapping)
 abab  abab  abab  abab        -> positions 0, 2, 4, 6  (overlapping)
```

Non-overlapping means that after a match you resume from its **end**, not from
one character on. Python's `str.count` already does this, so the reference is one
line — but if you are writing the scan yourself, the resume index is the whole
task.

An empty needle matches everywhere and nowhere; this task defines it as 0 rather
than infinity.

## When the Separator Is Not Uniform

**Comma quibbling** looks like a join and is not:

```
[]              -> {}
['ABC']         -> {ABC}
['A','B','C']   -> {A, B and C}
```

The last separator differs from the rest, so no single `join` produces it. Join
all but the last element, then attach the last with ` and `. The empty and
single-element cases have to be handled before that, because "all but the last"
is meaningless for them.

This is the same structure as English list formatting anywhere — and the reason
`Intl.ListFormat` exists in JavaScript.

## Greedy Line Breaking

**Word wrap** fills each line with as many words as fit, then starts a new one.
Greedy, one pass, no lookahead:

```python
if len(current) + 1 + len(word) <= width:
    current += " " + word     # the +1 is the space
else:
    lines.append(current)
    current = word
```

The `+ 1` for the space is where off-by-one errors live.

Two cases decide correctness: a word **longer than the width** gets a line to
itself rather than being broken, and empty input returns no lines rather than one
empty line.

Greedy is not optimal, incidentally. Minimising the *raggedness* of the whole
paragraph needs dynamic programming — that is Knuth–Plass, and it is what TeX
does. This task wants the greedy answer, which is what almost every browser does.
