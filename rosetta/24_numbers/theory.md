# Numbers — Euclid, Fixed Points, and Growth

Five tasks about integers. Two are ancient algorithms worth knowing exactly, two
are loops that need a stopping condition you have to supply yourself, and one is
about how fast numbers grow.

## Euclid's Algorithm

The greatest common divisor of two numbers is the largest integer dividing both.
The naive method — try every candidate down from the smaller number — works and
is `O(min(a, b))`.

Euclid's method is `O(log min(a, b))` and is two lines:

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)
```

The insight is that any common divisor of `a` and `b` also divides `a mod b`, so
the pair can be replaced by a smaller pair with the same answer. Repeat until one
side is zero; the other is the gcd.

Three edges decide whether your version is right:

| Input | Answer | Why |
|---|---|---|
| `gcd(0, 5)` | 5 | every integer divides 0 |
| `gcd(0, 0)` | 0 | by convention |
| `gcd(-4, 6)` | 2 | the *greatest* divisor is positive |

The `abs` at the end is not decoration — `a % b` in Python follows the sign of
`b`, and in JavaScript it follows the sign of `a`. Returning the absolute value
makes the function agree with itself in both languages.

## From gcd to lcm

The least common multiple follows directly:

```
lcm(a, b) = |a * b| / gcd(a, b)
```

Divide *before* multiplying — `a // gcd(a, b) * b` — and the intermediate value
never exceeds the answer. Multiply first and you can overflow a fixed-width
integer in a language that has them, for no reason.

And `lcm(0, n)` is 0, which you have to special-case: the formula would divide by
`gcd(0, 0) = 0`.

## Iterating to a Fixed Point

**Hailstone** and **happy numbers** are the same shape: apply a rule repeatedly
until something happens. The difference is what "something" is.

Hailstone stops at 1, and every input tested has been observed to reach it —
though *nobody has proved it always does*. The Collatz conjecture is open. Your
loop is relying on an unproven claim, which is worth knowing even though it will
not bite you here.

Happy numbers are different: they either reach 1 or **fall into a cycle**, and
the cycle is why a naive `while n != 1` hangs forever on input 4.

```python
seen = set()
while n != 1 and n not in seen:
    seen.add(n)
    n = sum(int(d) ** 2 for d in str(n))
return n == 1
```

Any unhappy number enters the same cycle — `4, 16, 37, 58, 89, 145, 42, 20, 4` —
so `while n != 1 and n != 4` also works and uses no memory. The `seen` set is the
version to write first, because it is correct without needing that fact.

## How Fast Factorial Grows

`factorial(20)` fits in a 64-bit integer. `factorial(21)` does not.

Python integers are arbitrary precision, so this task is easy there and the
growth is invisible. In JavaScript, `Number` is a float64 and loses exactness
above 2⁵³ — `factorial(19)` is already wrong in the last digits. TypeScript
solutions to this task need `BigInt` to stay correct past 18.

That is a real difference between the languages rather than a quirk of the task,
and it is exactly the sort of thing writing the same task twice teaches you.

And `0!` is 1, not 0. It is the empty product — the same reason an empty sum is
0. Most wrong first attempts return 0.
