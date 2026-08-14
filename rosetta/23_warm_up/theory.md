# Warm-up — Reading a Task Precisely

Rosetta Code tasks are small, which is what makes them useful: there is nowhere
to hide a misunderstanding. Almost every failure in this module is a misread
statement rather than a missing algorithm.

## What This Course Is For

The same task, in any language the platform runs. That is the whole idea, and it
is not a gimmick — writing FizzBuzz in Python and then in TypeScript exposes
which parts of your solution were the *problem* and which were the *language*.

Every task here is graded against one set of reference expectations, whichever
language you choose. So a Python solution and a TypeScript solution are held to
exactly the same standard, and switching language mid-course costs you nothing.

Tasks are deliberately short. None of them needs a data structure you have not
already met, and several are one loop. The difficulty is in the edges.

## Inclusive, Exclusive, and Off By One

More of these tasks hinge on a boundary than on anything else.

- **Sum multiples of 3 and 5 below 10** means 3, 5, 6 and 9 — *not* 10. Below is
  exclusive.
- **The letters `a` to `e`** means five letters. Inclusive at both ends.
- **The first 8 Fibonacci numbers** is a count, not an index.

When a statement says "below", "up to", "through", or "the first n", stop and
decide which end is included before writing anything. A test that expects 23 and
gets 33 is almost always this, and no amount of staring at the loop body will
show it to you.

## Producing Values, Not Printing Them

The classic form of FizzBuzz prints as it goes. Here it returns a list, and
every task in this course returns a value.

That is not fussiness. A function that prints cannot be tested, composed, or
reused; one that returns can be all three. It is also the only form that works
across languages — `print` and `console.log` differ, but a list of strings is a
list of strings.

```python
# The shape almost every task in this module takes
def transform(n):
    out = []
    for i in range(1, n + 1):
        out.append(decide(i))
    return out
```

Note the types too: FizzBuzz returns `["1", "2", "Fizz"]`, with the numbers as
**text**. Mixing numbers and strings in one list is legal in both Python and
JavaScript and wrong in both.

## Simulate First, Then Look for the Pattern

**100 doors** is the first task here with a closed-form answer, and the right way
to reach it is to not look for one.

Write the simulation: `n` doors, `n` passes, toggle every `i`-th door. It is six
lines and it is obviously correct. Run it, print the answer for `n = 100`, and
read the output:

```
1, 4, 9, 16, 25, 36, 49, 64, 81, 100
```

The perfect squares. Now you can ask *why* — a door is toggled once per divisor,
and only a perfect square has an odd number of divisors, because its square root
pairs with itself. That reasoning is available to you only after the simulation
has shown you what to explain.

This order matters more than it looks. Guessing the pattern first and coding it
directly means you have no way to tell a clever answer from a wrong one. The
reference solution for this task is the brute-force version, on purpose.
