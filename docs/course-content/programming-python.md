# Python Programming Course Coverage

Total lessons: 34

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Day 1: Variables and output

Objective: Store values, name them clearly, and print results.

Concepts taught:
- A variable is a named box in memory that holds a value you can read and change later.
- You assign with '=': the name goes on the left, the value on the right.
- Pick clear names (score, user_name) so the code explains itself.
- Printing a variable shows its current value, which is how you check your work.

Example:
```python
# A variable is a name that stores a value so you can reuse it.
name = "Ryu"        # text wrapped in quotes is a string
score = 10          # a whole number is an integer
print(name, score)  # print shows values, separated by a space
```

Practice: Create two variables: one holding your name (text) and one holding your age (a number). Print both on one line, e.g. 'Ryu 21'.

Quick check: What is the main purpose of a variable?

## Day 2: Types and conversions

Objective: Recognize numbers, text, booleans, and basic casts.

Concepts taught:
- Every value has a type: integers (3), decimals/floats (3.14), text/strings ("hi"), and booleans (true/false).
- The type decides what operations are legal: adding numbers differs from joining text.
- Converting (casting) turns one type into another, e.g. the text "42" into the number 42.
- Mixing types carelessly is a common bug, so always know what type a value is.

Example:
```python
n = 42                    # an integer
pi = 3.14                 # a float (decimal number)
text = "42"               # a string that only looks like a number
print(int(text) + n)      # int("42") converts text to 42, so this is 84
print(type(pi).__name__)  # float
```

Practice: Make a variable holding the text "10", convert it to a number, add 5, and print the result. It should print 15, not 105.

Quick check: Why do types matter?

## Day 3: Input and simple programs

Objective: Read user input and turn it into useful values.

Concepts taught:
- Programs get useful when they react to data the user types in.
- Input almost always arrives as text, even when the user types digits.
- Before doing math on it, convert that text into a number (int or float).
- Guard against unexpected input so the program does not crash.

Example:
```python
# input() always returns text, so convert before doing math.
raw = input("Enter a number: ")  # e.g. the user types 10
num = int(raw)                   # turn the text "10" into the integer 10
print(num * 2)                   # now arithmetic works -> 20
```

Practice: Ask the user for their age, convert the typed text to a number, add 1, and print 'Next year you will be ' followed by that number.

Quick check: What should you usually do before using numeric input?

## Day 4: Conditionals

Objective: Use if/else logic to make decisions.

Concepts taught:
- Conditionals let a program choose between paths based on a true/false test.
- 'if' runs a block only when its condition is true; 'else' covers the other case; else-if chains more checks.
- Comparison operators (==, !=, <, >, <=, >=) produce the booleans you test.
- Combine conditions with and / or / not to express richer rules.

Example:
```python
age = 20              # the value we want to test
if age >= 18:         # if this condition is True, run the block
    print("adult")    # indentation marks what belongs to the if
else:                 # otherwise fall through to here
    print("minor")    # runs only when the condition was False
```

Practice: Set a number variable. Print 'positive' if it is greater than 0, 'negative' if it is less than 0, and 'zero' otherwise.

Quick check: Which construct lets code choose between branches?

## Day 5: Loops

Objective: Repeat work with for/while loops and trace loop state.

Concepts taught:
- A loop repeats a block of code so you do not copy-paste the same lines.
- Use a 'for' loop when you know how many times or are walking a collection; use 'while' to repeat until a condition turns false.
- The loop variable changes each pass; tracing it by hand reveals how the loop behaves.
- Make sure the loop can end, or it runs forever (an infinite loop).

Example:
```python
# range(1, 6) gives 1,2,3,4,5 -- the stop value 6 is excluded.
for n in range(1, 6):  # n takes each value in turn
    print(n)           # the body runs once per pass
```

Practice: Use a loop to print the numbers 1 through 10, each on its own line.

Quick check: What do loops help you avoid writing repeatedly?

## Day 6: Functions and methods

Objective: Package logic into reusable units with parameters and returns.

Concepts taught:
- A function packages a piece of logic under a name so you can reuse it.
- Parameters are the inputs you pass in; the return value is the result you get back.
- Calling a function runs its body with the arguments you supply.
- Functions keep code short, testable, and free of duplication.

Example:
```python
def add(a, b):       # def names a reusable function with inputs
    return a + b     # return hands a value back to the caller

print(add(2, 3))     # call the function; this prints 5
```

Practice: Write a function called square that takes one number and returns it multiplied by itself. Call square(4) and print the result (16).

Quick check: What keyword returns a value from a function/method?

## Day 7: Arrays and lists

Objective: Store many values and iterate through them safely.

Concepts taught:
- An array (or list) stores many values in a single ordered container.
- Each item has an index; most languages start at 0, so the first item is index 0.
- You loop over the items to process them one by one.
- Reading past the last valid index is a classic out-of-bounds error.

Example:
```python
nums = [3, 1, 4]   # a list holds many values in order
for n in nums:     # the loop visits each item once
    print(n)       # prints 3, then 1, then 4
```

Practice: Make an array/list of the three numbers 3, 1, 4. Loop through it and print their total (8).

Quick check: What is the first index in most C/Python/Java arrays?

## Day 8: Strings

Objective: Process text by indexing, slicing, comparing, and counting.

Concepts taught:
- A string is an ordered sequence of characters (letters, digits, symbols).
- You can index single characters, slice ranges, measure length, and compare strings.
- Strings are often immutable, so 'changing' one usually builds a new string.
- Many problems (palindromes, counting) are just careful string traversal.

Example:
```python
word = "level"             # a string is a sequence of characters
# word[::-1] reverses the string; equal means it is a palindrome.
print(word == word[::-1])  # True when it reads the same backward
```

Practice: Set a variable to the word "hello". Print its length (5), then print just its first character (h).

Quick check: What is a string made of?

## Day 9: Hash maps and dictionaries

Objective: Use key-value lookup to reduce repeated scans.

Concepts taught:
- A hash map (dictionary) stores key -> value pairs for fast lookup by key.
- Looking up, inserting, and updating by key are about constant time (O(1)) on average.
- They shine when you would otherwise scan a list repeatedly, e.g. counting occurrences.
- Keys are unique; assigning an existing key overwrites its value.

Example:
```python
counts = {}                 # a dict maps keys to values
for ch in "banana":         # look at each character
    counts[ch] = counts.get(ch, 0) + 1  # add 1, default 0 if new
print(counts)               # {'b': 1, 'a': 3, 'n': 2}
```

Practice: Count how many times each letter appears in the word "apple" using a hash map/dictionary, then print the counts.

Quick check: What is the main advantage of a hash map lookup?

## Day 10: Stacks

Objective: Model last-in-first-out workflows and parentheses problems.

Concepts taught:
- A stack is a last-in, first-out (LIFO) collection: the most recent item comes off first.
- The two core operations are push (add to the top) and pop (remove from the top).
- Think of a stack of plates: you take the top one.
- Stacks model undo history, function calls, and matching brackets/parentheses.

Example:
```python
stack = []          # a plain list works as a stack
stack.append(1)     # push 1 onto the top
stack.append(2)     # push 2 onto the top
top = stack.pop()   # pop removes and returns the top item (2)
print(top, stack)   # 2 [1]
```

Practice: Push the numbers 1, 2, then 3 onto a stack. Pop them off one at a time and print each — they should come out 3, 2, 1.

Quick check: Which item is removed first from a stack?

## Day 11: Two pointers

Objective: Solve sorted-array and in-place problems with two indexes.

Concepts taught:
- The two-pointer technique uses two indexes moving through data to avoid nested loops.
- Common setups: one pointer at each end moving inward, or a slow/fast pair moving the same way.
- It works best on sorted arrays or when pairing/comparing elements.
- It often turns an O(n^2) scan into a single O(n) pass.

Example:
```python
nums = [1, 2, 3, 4, 6]          # must be sorted
left, right = 0, len(nums) - 1  # one pointer at each end
target = 7
while left < right:             # move the pointers inward
    s = nums[left] + nums[right]
    if s == target:
        print(left, right); break   # found a pair that sums to 7
    elif s < target:
        left += 1               # too small: raise the low end
    else:
        right -= 1              # too big: lower the high end
```

Practice: Given the sorted list [1, 2, 3, 4, 6], use one pointer at each end to find a pair that adds up to 7, and print the two values (1 and 6).

Quick check: Two pointers usually means tracking how many indexes?

## Day 12: Sliding window

Objective: Track a moving range for substring and subarray problems.

Concepts taught:
- A sliding window tracks a contiguous range (subarray/substring) that grows and shrinks as you scan.
- Expand the window by moving the right edge; shrink it by moving the left edge.
- Keep a running total or count so you do not recompute the whole window each step.
- Great for 'longest/shortest/best run that satisfies X' problems.

Example:
```python
nums = [2, 1, 5, 1, 3, 2]   # largest sum of any 3 in a row?
k = 3
window = sum(nums[:k])      # sum of the first window
best = window
for i in range(k, len(nums)):        # slide the window right
    window += nums[i] - nums[i - k]  # add the new item, drop the old
    best = max(best, window)
print(best)                 # 9 (from 5, 1, 3)
```

Practice: Given [2, 1, 5, 1, 3, 2], use a window of size 3 to find and print the largest sum of any 3 numbers in a row (9).

Quick check: A sliding window tracks a moving what?

## Day 13: Binary search

Objective: Cut a sorted or monotonic search space in half.

Concepts taught:
- Binary search finds a target by repeatedly halving a sorted search space.
- Check the middle: if it matches you are done; otherwise discard the half that cannot contain it.
- It needs sorted data, or any condition that is monotonic (false then true).
- It runs in O(log n), far faster than scanning every element.

Example:
```python
nums = [1, 3, 5, 7, 9]   # binary search needs sorted data
target = 7
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2     # look at the middle
    if nums[mid] == target:
        print(mid); break    # found it (index 3)
    elif nums[mid] < target:
        lo = mid + 1         # answer is in the right half
    else:
        hi = mid - 1         # answer is in the left half
```

Practice: Given the sorted list [1, 3, 5, 7, 9], use binary search to find the value 7 and print its index (3).

Quick check: Binary search requires sorted data or what kind of predicate?

## Day 14: Classes and objects

Objective: Group data and behavior into reusable types.

Concepts taught:
- A class is a blueprint that bundles related data (fields) with behavior (methods).
- An object is one instance made from that class, with its own copy of the data.
- Methods act on the object's own data (this / self).
- Classes help model real things and keep related code together.

Example:
```python
class Counter:          # a class is a blueprint for objects
    def __init__(self): # __init__ runs when you create one
        self.value = 0  # self stores data on the instance
    def inc(self):      # a method is a function tied to the object
        self.value += 1 # update this instance's own value
```

Practice: Define a class called Dog with a name and a method bark() that prints '<name> says woof'. Create a Dog named Rex and call bark().

Quick check: Classes group data with what?

## Day 15: Linked lists

Objective: Reason about nodes, next pointers, and pointer rewiring.

Concepts taught:
- A linked list is a chain of nodes; each node holds a value and a reference to the next node.
- Unlike an array there is no direct index, so you reach an item by following next pointers.
- Inserting or removing is cheap once you are at the spot (just rewire pointers); finding the spot is O(n).
- The list ends when a node's next is null/None.

Example:
```python
class Node:                # one link in the chain
    def __init__(self, value):
        self.value = value
        self.next = None   # points to the next node, None at the end

a = Node(1)                # build the chain 1 -> 2
a.next = Node(2)
node = a
while node:                # walk it by following .next
    print(node.value)
    node = node.next
```

Practice: Build a linked list of three nodes holding 1, 2, 3. Then walk the list from the start and print each value.

Quick check: A linked list node stores a value and a reference to what?

## Day 16: Recursion

Objective: Solve a problem by reducing it to smaller versions.

Concepts taught:
- Recursion solves a problem by having a function call itself on a smaller version of the problem.
- Every recursion needs a base case that stops it, or it never ends (stack overflow).
- Each call must move closer to the base case.
- Many tree and divide-and-conquer problems are naturally recursive.

Example:
```python
def factorial(n):          # n! = n * (n-1) * ... * 1
    if n <= 1:             # base case: stops the recursion
        return 1
    return n * factorial(n - 1)  # call itself on a smaller n

print(factorial(5))        # 120
```

Practice: Write a recursive function that computes the factorial of a number (n! = n*(n-1)*...*1). Call it with 5 and print the result (120).

Quick check: What must every recursive solution have?

## Day 17: Trees

Objective: Traverse tree-shaped data with DFS and BFS.

Concepts taught:
- A tree is a hierarchy of nodes starting from a single root; each node has children.
- A binary tree limits each node to at most two children (left and right).
- Visit nodes with traversals: depth-first (DFS: pre/in/post-order) or breadth-first (BFS, level by level).
- Trees model file systems, decisions, and sorted data (binary search trees).

Example:
```python
class Node:                # a binary tree node
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

root = Node(1)             # build a tiny tree
root.left = Node(2)
root.right = Node(3)

def visit(node):           # depth-first pre-order traversal
    if not node:           # base case: empty branch
        return
    print(node.value)
    visit(node.left)
    visit(node.right)

visit(root)                # 1 2 3
```

Practice: Build a small binary tree: a root holding 1 with children 2 and 3. Write a function that visits and prints every node's value.

Quick check: What is the top node of a tree called?

## Day 18: Graphs

Objective: Represent connections and traverse with BFS/DFS.

Concepts taught:
- A graph is a set of nodes (vertices) joined by edges; connections can be one-way or two-way.
- Common representations: an adjacency list (each node lists its neighbors) or an adjacency matrix.
- Traverse with BFS (level by level, good for shortest unweighted paths) or DFS (go deep first).
- Track visited nodes so you do not loop forever on cycles.

Example:
```python
# adjacency list: each node maps to its list of neighbors
graph = {1: [2, 3], 2: [4], 3: [], 4: []}
visited = set()
stack = [1]                # depth-first search from node 1
while stack:
    node = stack.pop()
    if node in visited:    # skip nodes already seen
        continue
    visited.add(node)
    print(node)
    stack.extend(graph[node])  # queue up the neighbors
```

Practice: Store this graph as an adjacency list: node 0 connects to 1 and 2; node 1 connects to 2. Print all the neighbors of node 0.

Quick check: Graph traversal usually uses BFS or what?

## Day 19: Dynamic programming

Objective: Define state, recurrence, base cases, and order.

Concepts taught:
- Dynamic programming solves a problem by combining answers to overlapping subproblems.
- Define the state (what a subproblem means), the recurrence (how states combine), and the base cases.
- Store (memoize) computed answers so each subproblem is solved only once.
- It turns exponential brute force into polynomial time when subproblems repeat.

Example:
```python
# nth Fibonacci number, reusing answers to subproblems
memo = {0: 0, 1: 1}        # base cases
def fib(n):
    if n not in memo:      # solve each subproblem only once
        memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]

print(fib(10))             # 55
```

Practice: Compute the 10th Fibonacci number by storing each answer in an array/dictionary as you build up. Print the result (55).

Quick check: DP usually stores answers to smaller what?

## Day 20: Heaps and priority queues

Objective: Repeatedly access the smallest or largest item efficiently.

Concepts taught:
- A heap always gives quick access to the smallest (min-heap) or largest (max-heap) item.
- Push and pop are O(log n); peeking at the top item is O(1).
- Use it as a priority queue when you repeatedly need the next most-important item.
- It is ideal for top-k, scheduling, and merging sorted streams.

Example:
```python
import heapq               # the min-heap helpers live here
nums = [5, 1, 8, 3]
heapq.heapify(nums)        # rearrange the list into a heap
heapq.heappush(nums, 2)    # add a value, keeping heap order
print(heapq.heappop(nums)) # 1 -- always the smallest item
```

Practice: Put the numbers 5, 1, 8, 3 into a min-heap / priority queue, then remove and print the smallest item (1).

Quick check: A heap is useful when repeatedly taking the min or what?

## Day 21: Matrices

Objective: Traverse rows, columns, and neighbors without index bugs.

Concepts taught:
- A matrix is a 2D grid of values indexed by row and column (grid[r][c]).
- The outer loop usually walks rows; the inner loop walks columns.
- Neighbors are the cells up/down/left/right (sometimes diagonals); check bounds before accessing.
- Off-by-one errors and swapped row/column indexes are the most common bugs.

Example:
```python
grid = [[1, 2, 3],         # a 2D grid: rows of columns
        [4, 5, 6]]
for r in range(len(grid)):          # walk each row
    for c in range(len(grid[0])):   # walk each column
        print(grid[r][c], end=" ")  # grid[r][c] reads one cell
    print()                # newline after each row
```

Practice: Make a 2x3 grid of numbers ([[1,2,3],[4,5,6]]). Loop through it and print each row on its own line.

Quick check: A matrix is indexed by row and what?

## Day 22: Design problems

Objective: Build small APIs that preserve invariants over operations.

Concepts taught:
- Design problems ask you to build a small component with specific operations (e.g. a cache or queue).
- Focus on the invariants: the rules that must stay true after every operation.
- Pick data structures that make the required operations efficient.
- Think through edge cases: empty state, capacity limits, and repeated keys.

Example:
```python
class Stack:               # design a stack with a size limit
    def __init__(self, cap):
        self.cap = cap     # invariant: never hold more than cap
        self.items = []
    def push(self, x):
        if len(self.items) < self.cap:  # enforce the invariant
            self.items.append(x)
    def pop(self):
        return self.items.pop() if self.items else None

s = Stack(2)
s.push(1); s.push(2); s.push(3)  # third push is ignored (cap 2)
print(s.items)             # [1, 2]
```

Practice: Design a Stack class with a capacity of 2 whose push() ignores new items when full. Push 1, 2, 3, then print how many items it holds (2).

Quick check: Design problems are mostly about preserving what over operations?

## Day 23: Python basics and environment

Objective: Use the REPL, scripts, IDEs, dynamic typing, numeric types, strings, truthiness, None, and docstrings.

Concepts taught:
- Python can run interactively in a REPL or from script files, which makes experimentation fast.
- Names are dynamically typed: the value has a type, and the name can later refer to another type.
- Numeric types include int, float, and complex; / produces true division and // produces floor division.
- Strings support slicing, f-strings, common methods, and Unicode text by default.
- Truthiness, None, comments, and docstrings are basic tools for readable Python programs.

Example:
```python
"""Small script demonstrating Python basics."""
n = 7
ratio = 7 / 2
floor = 7 // 2
name = "Ryu"
print(f"{name}: {n}, {ratio}, {floor}, truthy={bool(name)}, none={None}")
```

Practice: Write a Python script that demonstrates int, float, complex, / vs //, f-strings, truthiness, None, and a module docstring.

Quick check: What Python value represents no value?

## Day 24: Python control flow

Objective: Use if/elif/else, loops, range, break, continue, pass, nested tracing, and match-case.

Concepts taught:
- if/elif/else branches are driven by booleans and truthy/falsy values.
- for loops iterate over ranges, strings, lists, dictionaries, files, and any iterable.
- while loops continue until their condition becomes false, so loop state must change.
- break exits, continue skips, and pass is an explicit placeholder.
- match-case can express structural pattern matching for fixed shapes and tagged data.

Example:
```python
command = "run"
match command:
    case "run":
        for i in range(5):
            if i == 2: continue
            if i == 4: break
            print(i)
    case _:
        pass
```

Practice: Write a Python program that uses if/elif/else, for/range, while, break, continue, pass, and match-case on a simple command string.

Quick check: What Python statement is an explicit no-op placeholder?

## Day 25: Functions, scope, and call patterns

Objective: Write Python functions with defaults, keyword args, *args, **kwargs, lambdas, LEGB scope, and recursion.

Concepts taught:
- Python functions can use positional arguments, keyword arguments, defaults, *args, and **kwargs.
- The LEGB rule resolves names through local, enclosing, global, and built-in scopes.
- Closures capture variables from an enclosing function so inner functions can remember state.
- Lambdas create small anonymous functions, usually for callbacks or key functions.
- Higher-order functions accept or return functions, such as map, filter, and sorted(key=...).
- Type hints document intended types and help tools, but Python still checks most types at runtime.

Example:
```python
def summarize(*nums: int, scale: int = 1, **labels: str) -> int:
    total = sum(nums) * scale
    print(labels.get("name", "total"), total)
    return total
words = sorted(["pear", "fig", "apple"], key=lambda w: len(w))
```

Practice: Write a function summarize(*nums, scale=1, **labels), use a lambda as sorted(key=...), and add type hints.

Quick check: What acronym describes Python name lookup order?

## Day 26: Built-in data structures

Objective: Use lists, tuples, dictionaries, sets, comprehensions, unpacking, and copy semantics.

Concepts taught:
- Lists are mutable ordered sequences; tuples are ordered and usually immutable.
- Dictionaries map keys to values and preserve insertion order in modern Python.
- Sets store unique items and support union, intersection, and difference.
- Comprehensions build lists, dicts, and sets from compact loop/filter expressions, and generator expressions stay lazy.
- Shallow copies duplicate the outer container; deep copies recursively copy nested objects.

Example:
```python
squares = [n*n for n in range(5)]
index = {value: i for i, value in enumerate(squares)}
evens = {n for n in squares if n % 2 == 0}
first, *rest = squares
shallow = [rest, evens].copy()
```

Practice: Use a list comprehension, dict comprehension, set operation, tuple unpacking, and a shallow-copy example in one short script.

Quick check: Which Python built-in stores unique items?

## Day 27: Strings, regex, and encodings

Objective: Process text with string methods, formatting, regular expressions, and UTF-8 awareness.

Concepts taught:
- String methods such as split, join, strip, replace, and find solve many parsing tasks without regex.
- f-strings are the standard readable way to interpolate values into text.
- The re module supports matching, searching, findall, and substitution with regular expressions.
- ASCII is a small character set; UTF-8 can encode all Unicode characters and is the default expectation for most modern text.
- Text pipelines should be explicit about encoding when reading files from unknown sources.

Example:
```python
import re
raw = " name: Ryu, score: 42 "
parts = [p.strip() for p in raw.split(",")]
print(" | ".join(parts))
print(re.findall(r"\d+", raw))
```

Practice: Parse a comma-separated sentence using split/strip, rebuild it with join, then use re.findall to extract numbers.

Quick check: What Python module provides regular expressions?

## Day 28: File I/O and data handling

Objective: Read and write text, binary, CSV, JSON, command-line arguments, and argparse options.

Concepts taught:
- Use with open(...) as f so files close even when an exception occurs.
- Text files decode bytes into str; binary files read and write raw bytes.
- The csv module handles commas, quotes, and rows better than manual splitting.
- json.loads and json.dumps convert between JSON text and Python data.
- sys.argv is raw command-line input; argparse gives typed options, help text, and validation.

Example:
```python
import argparse, csv, json
parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()
with open(args.input, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(json.dumps(rows, indent=2))
```

Practice: Read a CSV file, convert rows to dictionaries, write JSON output, and add argparse for input/output paths.

Quick check: What statement should you use so files close automatically?

## Day 29: Python error handling

Objective: Handle exceptions with try/except/else/finally, raise custom exceptions, and use assertions.

Concepts taught:
- try/except handles expected failures without crashing the whole program.
- else runs only when no exception occurred; finally runs for cleanup either way.
- Common exceptions include ValueError, TypeError, KeyError, IndexError, and FileNotFoundError.
- raise reports a failure intentionally, and custom exception classes make domain errors clearer.
- assert is useful for internal sanity checks, not for validating user input in production.

Example:
```python
class InvalidAgeError(ValueError): pass
def parse_age(text: str) -> int:
    try:
        age = int(text)
        if age < 0: raise InvalidAgeError("age must be nonnegative")
        return age
    except ValueError as exc:
        raise InvalidAgeError("bad age") from exc
```

Practice: Write a safe_int function that catches ValueError, raises a custom InvalidAgeError for negative values, and uses finally for cleanup text.

Quick check: What keyword intentionally raises an exception?

## Day 30: Object-oriented Python

Objective: Build classes with dunder methods, inheritance, properties, dataclasses, and abstract base classes.

Concepts taught:
- __init__ initializes each instance, and self names the current object.
- Class variables are shared by the class; instance variables belong to one object.
- Dunder methods such as __str__, __repr__, __eq__, __hash__, and __lt__ integrate objects with Python syntax.
- Inheritance and super reuse behavior, while multiple inheritance follows the method resolution order.
- @property, dataclasses, and abstract base classes from abc help express clean object APIs.

Example:
```python
from dataclasses import dataclass
@dataclass(order=True, frozen=True)
class Point:
    x: int
    y: int
    @property
    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y)
```

Practice: Create a @dataclass Point with __str__, __eq__, __lt__, a @property, and an abstract Shape base class.

Quick check: What method initializes a Python object?

## Day 31: Iterators, generators, and decorators

Objective: Implement iteration protocols, yield generators, decorators, functools.wraps, and context managers.

Concepts taught:
- The iterator protocol uses __iter__ and __next__ so objects can work in for loops.
- A generator function uses yield to produce values lazily without building a full list.
- Generator expressions are lazy versions of list comprehensions.
- Decorators wrap functions with extra behavior while keeping the call site unchanged.
- Context managers define __enter__ and __exit__, or use contextlib, to manage setup and cleanup.

Example:
```python
import functools
def log_calls(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print("calling", fn.__name__)
        return fn(*args, **kwargs)
    return wrapper
def countdown(n):
    while n > 0:
        yield n
        n -= 1
```

Practice: Write a countdown generator, a timing/logging decorator with functools.wraps, and a context manager using contextlib.

Quick check: What keyword makes a generator function produce values lazily?

## Day 32: Modules, packages, and environments

Objective: Organize imports, packages, virtual environments, requirements, standard library modules, and main guards.

Concepts taught:
- The interpreter, scripts, and IDEs are all normal ways to run Python during development.
- import and from ... import bring module names into the current file.
- Packages are directories with Python modules and often an __init__.py file.
- Virtual environments isolate installed packages so projects do not break each other.
- requirements.txt records dependencies; pip installs them into the active environment.
- if __name__ == '__main__' keeps script behavior separate from import behavior.

Example:
```python
# package layout:
# program/__init__.py
# program/main.py
# requirements.txt
if __name__ == "__main__":
    from program.main import main
    main()
```

Practice: Sketch a package layout with __init__.py, a main guard, requirements.txt, and commands to create/activate a venv.

Quick check: What file commonly records Python package dependencies?

## Day 33: Testing in Python

Objective: Write unittest and pytest tests with fixtures, parametrization, mocks, coverage, and TDD workflow.

Concepts taught:
- unittest organizes tests into classes with assertions and optional setUp/tearDown methods.
- pytest favors simple test functions, powerful assertions, fixtures, and parametrization.
- TDD writes a failing test first, then implements the smallest code that passes.
- Mocks replace slow or external dependencies so tests stay focused and repeatable.
- Coverage helps reveal untested code paths but does not prove the assertions are meaningful.

Example:
```python
import pytest
@pytest.mark.parametrize("text,expected", [("1", 1), ("02", 2)])
def test_parse_int(text, expected):
    assert int(text) == expected
@pytest.fixture
def sample_user():
    return {"name": "Ryu"}
```

Practice: Write pytest tests with one fixture, one parametrize case, and one mock for a function that calls an external API.

Quick check: What pytest feature supplies reusable test setup?

## Day 34: Python for AI/ML readiness

Objective: Use NumPy, Pandas, plotting, notebooks, HTTP requests, and async awareness for AI engineering workflows.

Concepts taught:
- NumPy arrays support vectorized numeric operations and broadcasting across shapes.
- Pandas Series and DataFrames make tabular cleaning, filtering, grouping, and CSV loading productive.
- Matplotlib and Seaborn help inspect distributions, trends, and model results visually.
- Jupyter notebooks are useful for exploration, but production logic should move into tested modules.
- AI engineering also needs API calls with requests and basic awareness of async workflows.

Example:
```python
import numpy as np
import pandas as pd
df = pd.DataFrame({"team": ["a", "a", "b"], "score": [1, 3, 5]})
print(df.groupby("team")["score"].mean())
vector = np.array(df["score"])
print(vector * 2)
```

Practice: Load a CSV into Pandas, compute one groupby summary, convert one column to a NumPy array, and plot a simple chart.

Quick check: What Pandas object represents a table of rows and columns?
