"""Runnable demonstrations for the Warm-up module."""

print("=" * 60)
print("1. Why 100 doors leaves the perfect squares open")
print("=" * 60)


def simulate(n):
    doors = [False] * (n + 1)
    for step in range(1, n + 1):
        for door in range(step, n + 1, step):
            doors[door] = not doors[door]
    return [i for i in range(1, n + 1) if doors[i]]


for n in (10, 25, 100):
    print(f"  n={n:3} -> {simulate(n)}")
print("\n  Those are the perfect squares. A door is toggled once per divisor,")
print("  and only a square has an odd divisor count -- its root pairs with itself.")
print(f"  divisors of 12: {[d for d in range(1, 13) if 12 % d == 0]}  (even count -> closed)")
print(f"  divisors of 16: {[d for d in range(1, 17) if 16 % d == 0]}  (odd count  -> open)")

print("\n" + "=" * 60)
print("2. The leap-year rule, and the year that breaks a naive one")
print("=" * 60)
for year in (1896, 1900, 2000, 2023, 2024, 2100):
    naive = year % 4 == 0
    correct = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    flag = "  <-- naive rule is wrong here" if naive != correct else ""
    print(f"  {year}: divisible by 4 = {str(naive):5} actual = {str(correct):5}{flag}")

print("\n" + "=" * 60)
print("3. Inclusive versus exclusive, counted out")
print("=" * 60)
print(f"  multiples of 3 or 5 below 10 : {[i for i in range(1, 10) if i % 3 == 0 or i % 5 == 0]}"
      f" -> {sum(i for i in range(1, 10) if i % 3 == 0 or i % 5 == 0)}")
print(f"  ...up to and including 10    : {[i for i in range(1, 11) if i % 3 == 0 or i % 5 == 0]}"
      f" -> {sum(i for i in range(1, 11) if i % 3 == 0 or i % 5 == 0)}")
print("  One word in the statement, a different answer.")
