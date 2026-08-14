"""Runnable demonstrations for the Numbers module."""

import math

print("=" * 60)
print("1. Euclid's algorithm, step by step")
print("=" * 60)


def gcd_trace(a, b):
    steps = []
    while b:
        steps.append(f"({a}, {b})")
        a, b = b, a % b
    steps.append(f"({a}, 0)")
    return abs(a), " -> ".join(steps)


for pair in ((48, 18), (1071, 462), (17, 5)):
    answer, trace = gcd_trace(*pair)
    print(f"  gcd{pair} = {answer}")
    print(f"    {trace}")

print("\n  Compare the work: trial division tries every candidate.")
a, b = 1_000_003, 999_983
naive = sum(1 for d in range(1, min(a, b) + 1) if a % d == 0 and b % d == 0)
_, trace = gcd_trace(a, b)
print(f"    trial division on ({a}, {b}): ~{min(a, b):,} iterations")
print(f"    Euclid: {trace.count('->') + 1} iterations")

print("\n" + "=" * 60)
print("2. Hailstone: short input, long journey")
print("=" * 60)


def hailstone(n):
    out = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


for n in (7, 27, 97):
    seq = hailstone(n)
    print(f"  {n:3}: {len(seq):3} steps, peaks at {max(seq):,}")
print(f"  27 in full: {hailstone(27)[:12]} ... {hailstone(27)[-4:]}")
print("  Nobody has proved this always terminates. It always has, so far.")

print("\n" + "=" * 60)
print("3. Unhappy numbers all fall into the same cycle")
print("=" * 60)


def digit_squares(n):
    return sum(int(d) ** 2 for d in str(n))


for start in (4, 16, 2, 11):
    seen, n = [], start
    while n not in seen and len(seen) < 12:
        seen.append(n)
        n = digit_squares(n)
    print(f"  {start:3}: {seen[:9]}{' ...' if len(seen) >= 9 else ''}")
print("  The loop 4,16,37,58,89,145,42,20 catches every unhappy number,")
print("  which is why testing for 4 works as well as remembering everything.")

print("\n" + "=" * 60)
print("4. Where factorial stops being exact")
print("=" * 60)
print("  Python integers never lose precision. A float64 -- JavaScript's only")
print("  number type -- stops being exact above 2**53:")
for n in (18, 19, 20, 21, 25):
    exact = math.factorial(n)
    as_float = float(exact)
    ok = "exact" if as_float == exact else f"OFF BY {abs(exact - int(as_float)):,}"
    print(f"  {n}! = {exact:<26,} as float64: {ok}")
print("  This is why a TypeScript solution needs BigInt past 18.")
