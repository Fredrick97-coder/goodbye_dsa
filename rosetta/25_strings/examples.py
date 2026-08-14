"""Runnable demonstrations for the Strings module."""

print("=" * 60)
print("1. Why a counter is not enough for brackets")
print("=" * 60)


def by_counter(text):
    depth = 0
    for ch in text:
        depth += 1 if ch in "([{" else -1 if ch in ")]}" else 0
        if depth < 0:
            return False
    return depth == 0


def by_stack(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


for text in ("[[]]", "][", "([)]", "{[()]}", "("):
    c, s = by_counter(text), by_stack(text)
    flag = "  <-- counter is WRONG" if c != s else ""
    print(f"  {text:8} counter={str(c):5} stack={str(s):5}{flag}")
print("  '([)]' is balanced by depth and unbalanced in fact. Order needs a stack.")

print("\n" + "=" * 60)
print("2. Overlapping or not")
print("=" * 60)
text, needle = "ababababab", "abab"
overlapping = [i for i in range(len(text) - len(needle) + 1)
               if text.startswith(needle, i)]
non = []
i = 0
while (found := text.find(needle, i)) != -1:
    non.append(found)
    i = found + len(needle)
print(f"  {text!r} contains {needle!r}")
print(f"    overlapping     : {len(overlapping)} at {overlapping}")
print(f"    non-overlapping : {len(non)} at {non}   <-- what this task asks for")

print("\n" + "=" * 60)
print("3. Greedy word wrap, and where it is not optimal")
print("=" * 60)


def wrap(text, width):
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


sample = "the quick brown fox jumps over the lazy dog"
for width in (10, 16, 24):
    lines = wrap(sample, width)
    print(f"  width {width}:")
    for line in lines:
        print(f"    |{line:<{width}}| {len(line)}")
    slack = [width - len(line) for line in lines[:-1]]
    print(f"    trailing gaps on full lines: {slack}")
print("  Greedy minimises lines, not raggedness. Balancing the gaps needs DP")
print("  (Knuth-Plass, which is what TeX does).")
