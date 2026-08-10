# Data Structures and Algorithms (DSA) - Python Learning Path

A comprehensive guide to mastering Data Structures and Algorithms in Python, organized from **Beginner** to **Advanced** levels.

Each topic includes:
- **theory.md** - Conceptual understanding and explanations
- **examples.py** - Practical code examples
- **exercise.py** - Problems to solve for practice
- **project.py** - Real-world projects to apply concepts

---

## 📚 Learning Path Overview

### **BEGINNER LEVEL** - Foundations
| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Introduction to DSA](./01_introduction_to_dsa) | Big-O notation, Time/Space complexity, Algorithm basics |
| 02 | [Arrays & Lists](./02_arrays_lists) | Static arrays, Dynamic arrays, List operations |
| 03 | [Strings & String Manipulation](./03_strings) | String basics, Patterns, Substring problems |
| 04 | [Stacks](./04_stacks) | LIFO, Push/Pop, Applications |
| 05 | [Queues](./05_queues) | FIFO, Enqueue/Dequeue, Circular queues |
| 06 | [Basic Sorting Algorithms](./06_basic_sorting) | Bubble, Selection, Insertion sort |

### **INTERMEDIATE LEVEL** - Core Structures
| # | Topic | Key Concepts |
|---|-------|--------------|
| 07 | [Linked Lists](./07_linked_lists) | Singly, Doubly, Circular lists |
| 08 | [Trees - Basics](./08_trees_basics) | Binary trees, BST, Traversals |
| 09 | [Hash Maps & Hash Tables](./09_hash_maps) | Hashing, Collision handling, Dictionary problems |
| 10 | [Basic Searching Algorithms](./10_basic_searching) | Linear, Binary search, Search optimization |
| 11 | [Graphs - Basics](./11_graphs_basics) | Adjacency matrix/list, BFS, DFS |

### **ADVANCED LEVEL** - Optimization & Complex Algorithms
| # | Topic | Key Concepts |
|---|-------|--------------|
| 12 | [Dynamic Programming](./12_dynamic_programming) | Memoization, Tabulation, DP patterns |
| 13 | [Advanced Sorting Algorithms](./13_advanced_sorting) | Merge sort, Quick sort, Heap sort |
| 14 | [Graph Algorithms](./14_graph_algorithms) | Dijkstra, Bellman-Ford, Floyd-Warshall |
| 15 | [Greedy Algorithms](./15_greedy_algorithms) | Activity selection, Huffman coding, MST |
| 16 | [Bit Manipulation](./16_bit_manipulation) | Bitwise operations, Bit DP |
| 17 | [Advanced Trees](./17_advanced_trees) | AVL, Red-Black, Segment trees |
| 18 | [Trie & String Algorithms](./18_trie_string_algorithms) | Trie structure, KMP, Rabin-Karp |

---

## 🎤 Interview-Gap Topics (19-22)

Added to cover categories that appear constantly in interviews but had no
dedicated topic above.

| # | Topic | Key Concepts |
|---|-------|--------------|
| 19 | [Heaps & Priority Queues](./19_heaps_priority_queues) | Binary heap, `heapq`, top-K, two-heap median, k-way merge |
| 20 | [Backtracking](./20_backtracking) | Choose/explore/undo, subsets, permutations, N-Queens, Sudoku |
| 21 | [Intervals & Matrix Patterns](./21_intervals_matrix) | Merge intervals, sweep line, spiral, rotate, islands, multi-source BFS |
| 22 | [Math for Interviews](./22_math_for_interviews) | Sieve, GCD/LCM, modular arithmetic, fast power, combinatorics, overflow |

---

## 🧪 Practice Tools

Two commands. Full guide in **[PRACTICE.md](./PRACTICE.md)**.

```bash
python check.py 19        # test YOUR solutions against reference tests
python check.py --todo    # progress across all 22 topics
python drill.py -n 5      # 5 random problems with the TOPIC HIDDEN
python drill.py --stats   # what you have drawn, and your times
```

`check.py` tells you when an answer is wrong and prints the failing input —
reading theory builds recognition, but only a feedback loop builds recall.
`drill.py` hides the topic, because recognising *which* technique applies is a
separate skill from executing it, and no `exercise.py` can train it.

---

## 🎯 How to Use This Repository

### **For Beginners:**
1. Start with **Introduction to DSA** (Topic 01)
2. Follow the topics sequentially (01 → 06)
3. For each topic:
   - Read `theory.md` to understand concepts
   - Run `examples.py` to see practical implementations
   - Complete `exercise.py` with multiple difficulty levels
   - Build the `project.py` to solidify understanding

### **For Intermediate Learners:**
1. Review Beginner topics as needed
2. Move to Intermediate level (Topics 07 → 11)
3. Attempt harder exercises and projects

### **For Advanced Learners:**
1. Jump directly to Advanced topics (Topics 12 → 18)
2. Focus on optimization and solving complex problems
3. Complete challenging projects

### **Best Practices:**
- **Don't skip**: Each topic builds on previous knowledge
- **Code along**: Type out examples, don't just read
- **Do exercises**: Try before looking at solutions
- **Build projects**: Apply multiple concepts together
- **Revisit**: Return to previous topics when needed
- **Track progress**: Mark completed topics

---

## 📊 Complexity Cheat Sheet

### Time Complexity (Big-O)
```
O(1)      < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
constant    logarithmic linear linearithmic quadratic exponential factorial
(best)                                                      (worst)
```

### Space Complexity
- **O(1)** - Constant (few variables)
- **O(log n)** - Recursive call stack
- **O(n)** - Linear (arrays, lists)
- **O(n²)** - Nested structures

---

## 🔧 Quick Setup

```bash
# Navigate to python folder
cd /Users/incognito/Documents/Learning/DSA/python

# Run examples for any topic
python 01_introduction_to_dsa/examples.py

# Run exercises
python 01_introduction_to_dsa/exercise.py

# Run projects
python 01_introduction_to_dsa/project.py
```

---

## 📖 Recommended Study Schedule

| Week | Topics | Hours |
|------|--------|-------|
| 1-2 | Topic 01-02 (Intro, Arrays) | 10-15 |
| 3-4 | Topic 03-05 (Strings, Stacks, Queues) | 10-15 |
| 5-6 | Topic 06-07 (Sorting, Linked Lists) | 10-15 |
| 7-9 | Topic 08-11 (Trees, Hash, Graphs, Search) | 15-20 |
| 10-12 | Topic 12-14 (DP, Advanced Sort, Graph Algo) | 15-20 |
| 13+ | Topic 15-18 (Greedy, Bit, Advanced Trees, Tries) | 15-20 |

**Total: 75-125 hours of focused learning**

---

## 🎓 Progress Tracker

Use this to track your progress:

- [ ] 01 - Introduction to DSA
- [ ] 02 - Arrays & Lists
- [ ] 03 - Strings
- [ ] 04 - Stacks
- [ ] 05 - Queues
- [ ] 06 - Basic Sorting
- [ ] 07 - Linked Lists
- [ ] 08 - Trees (Basics)
- [ ] 09 - Hash Maps
- [ ] 10 - Basic Searching
- [ ] 11 - Graphs (Basics)
- [ ] 12 - Dynamic Programming
- [ ] 13 - Advanced Sorting
- [ ] 14 - Graph Algorithms
- [ ] 15 - Greedy Algorithms
- [ ] 16 - Bit Manipulation
- [ ] 17 - Advanced Trees
- [ ] 18 - Tries & String Algorithms

---

## 📝 Tips for Success

1. **Understand, don't memorize** - Focus on WHY algorithms work
2. **Visualize** - Draw trees, graphs, trace through code
3. **Practice** - Solve many problems, not just read solutions
4. **Code from scratch** - Don't rely on copy-paste
5. **Analyze complexity** - Always ask "Is this optimal?"
6. **Test edge cases** - Empty arrays, single elements, large inputs
7. **Refactor** - Improve solutions even after they work

---

## 🚀 After Completing This Path

Once you've mastered Python DSA:
- Move to other languages (C++, Java, Go, Rust, TypeScript, C#)
- Solve coding challenges (LeetCode, HackerRank, Codeforces)
- Study system design
- Prepare for interviews
- Contribute to open-source projects

---

**Happy Learning!** 🎉
