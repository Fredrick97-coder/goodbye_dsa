"""Specs for Topic 04 -- Stacks."""

from ..spec import spec


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


def _next_greater(arr):
    out = []
    for i, v in enumerate(arr):
        nxt = -1
        for w in arr[i + 1:]:
            if w > v:
                nxt = w
                break
        out.append(nxt)
    return out


def _remove_outer(s):
    out = []
    depth = 0
    for ch in s:
        if ch == "(":
            if depth:
                out.append(ch)
            depth += 1
        else:
            depth -= 1
            if depth:
                out.append(ch)
    return "".join(out)


def _eval_postfix(expr):
    stack = []
    for tok in expr.split():
        if tok in "+-*/":
            b, a = stack.pop(), stack.pop()
            stack.append({"+": a + b, "-": a - b,
                          "*": a * b, "/": a / b if b else 0}[tok])
        else:
            stack.append(float(tok))
    return stack[-1] if stack else 0.0


def _largest_rect(heights):
    best = 0
    for i in range(len(heights)):
        lo = heights[i]
        for j in range(i, len(heights)):
            lo = min(lo, heights[j])
            best = max(best, lo * (j - i + 1))
    return best


def _trap(height):
    if len(height) < 3:
        return 0
    return sum(min(max(height[:i + 1]), max(height[i:])) - height[i]
               for i in range(len(height)))


def _daily_temps(temps):
    out = []
    for i, t in enumerate(temps):
        wait = 0
        for j in range(i + 1, len(temps)):
            if temps[j] > t:
                wait = j - i
                break
        out.append(wait)
    return out


def _calculate(s):
    """Basic calculator: + - ( ) and unary minus, no * or /."""
    total, sign, num = 0, 1, 0
    stack = []
    for ch in s + "+":
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            total += sign * num
            num = 0
            sign = 1 if ch == "+" else -1
        elif ch == "(":
            stack.append((total, sign))
            total, sign = 0, 1
        elif ch == ")":
            total += sign * num
            num = 0
            prev, psign = stack.pop()
            total = prev + psign * total
            sign = 1
    return total


def g_parens(rng):
    return ("".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 10))),)


def g_balanced_parens(rng):
    """Well-formed round brackets wrapped in an outer pair."""
    depth = 0
    out = []
    for _ in range(rng.randint(1, 6)):
        if depth == 0 or rng.random() < 0.6:
            out.append("(")
            depth += 1
        else:
            out.append(")")
            depth -= 1
    out += [")"] * depth
    s = "".join(out)
    return ("(" + s + ")",)


def g_arr(rng, lo=-20, hi=20, nmin=0, nmax=15):
    return ([rng.randint(lo, hi) for _ in range(rng.randint(nmin, nmax))],)


def g_heights(rng):
    return ([rng.randint(0, 10) for _ in range(rng.randint(0, 12))],)


def g_postfix(rng):
    """Build a valid postfix expression by construction."""
    toks = [str(rng.randint(1, 9))]
    for _ in range(rng.randint(0, 4)):
        toks.append(str(rng.randint(1, 9)))
        toks.append(rng.choice("+-*"))
    # ensure operand/operator balance
    operands = sum(1 for t in toks if t not in "+-*")
    ops = len(toks) - operands
    toks += ["+"] * max(0, operands - 1 - ops)
    return (" ".join(toks),)


SPECS = [
    # NOTE the method names are isEmpty / getMin (camelCase) in this
    # exercise file, not is_empty / get_min. Verified against the source
    # rather than assumed.
    spec(1, "Stack",
         script=lambda cls: (lambda s: [
             s.push(1), s.push(2), s.push(3),
             s.pop(), s.peek(), s.isEmpty(), s.size(),
         ][3:])(cls()),
         ref_script=lambda: [3, 2, False, 2],
         note="push 1,2,3 then pop/peek/isEmpty/size"),
    spec(2, "is_valid_parentheses", ref=_valid_parens, gen=g_parens,
         cases=[(("()[]{}",), True), (("(]",), False), (("",), True),
                (("([)]",), False), (("{[]}",), True)]),
    spec(3, "reverse_string", ref=lambda s: s[::-1],
         gen=lambda r: ("".join(r.choice("abc")
                                for _ in range(r.randint(0, 10))),),
         cases=[(("hello",), "olleh"), (("",), "")]),
    spec(4, "next_greater_element", ref=_next_greater, gen=g_arr,
         cases=[(([4, 5, 2, 25],), [5, 25, 25, -1]), (([],), [])],
         note="-1 when nothing greater follows"),
    spec(5, "decimal_to_binary", ref=lambda n: bin(n)[2:] if n else "0",
         gen=lambda r: (r.randint(0, 10000),),
         cases=[((10,), "1010"), ((0,), "0"), ((255,), "11111111")]),
    spec(6, "remove_outermost_parentheses", ref=_remove_outer,
         gen=g_balanced_parens,
         cases=[(("(()())(())",), "()()()"), (("()",), "")]),
    spec(7, "evaluate_postfix", ref=_eval_postfix, gen=g_postfix, tol=1e-6,
         cases=[(("2 3 +",), 5.0), (("5 1 2 + 4 * + 3 -",), 14.0)]),
    spec(8, "MinStack",
         script=lambda cls: (lambda s: [
             s.push(3), s.push(1), s.push(2),
             s.getMin(), s.pop(), s.getMin(), s.top(),
         ][3:])(cls()),
         ref_script=lambda: [1, 2, 1, 1],
         note="push 3,1,2 -> getMin 1; pop 2 -> getMin 1, top 1"),
    spec(9, "largest_rectangle_histogram", ref=_largest_rect, gen=g_heights,
         cases=[(([2, 1, 5, 6, 2, 3],), 10), (([],), 0), (([1],), 1)]),
    spec(10, "trap_rain_water", ref=_trap, gen=g_heights,
         cases=[(([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6), (([],), 0)]),
    spec(11, "daily_temperatures", ref=_daily_temps,
         gen=lambda r: ([r.randint(30, 80) for _ in range(r.randint(0, 12))],),
         cases=[(([73, 74, 75, 71, 69, 72, 76, 73],),
                 [1, 1, 4, 2, 1, 1, 0, 0]), (([],), [])]),
    spec(12, "calculate", ref=_calculate,
         cases=[(("1 + 1",), 2), ((" 2-1 + 2 ",), 3),
                (("(1+(4+5+2)-3)+(6+8)",), 23)],
         note="+ - ( ) only"),
]
