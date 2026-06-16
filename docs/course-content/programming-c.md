# C Programming Course Coverage

Total lessons: 53

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Day 1: Variables and output

Objective: Store values, name them clearly, and print results.

Concepts taught:
- A variable is a named box in memory that holds a value you can read and change later.
- You assign with '=': the name goes on the left, the value on the right.
- Pick clear names (score, user_name) so the code explains itself.
- Printing a variable shows its current value, which is how you check your work.
- When you read code, track each variable's current value and the line where that value last changed.
- A useful variable name says what the value means in the problem, not only what type it has.

Example:
```c
#include <stdio.h>      // brings in printf for output
int main(void) {        // every C program starts at main
    int score = 10;     // C needs an explicit type (int)
    printf("%d\n", score); // %d prints an int; \n is a newline
    return 0;           // 0 tells the OS it succeeded
}
```

Practice: Create two variables: one holding a sample name (text) and one holding a sample age (a number). Print both on one line, e.g. 'Alex 21'.

Quick check: What is the main purpose of a variable?

## Day 2: Types and conversions

Objective: Recognize numbers, text, booleans, and basic casts.

Concepts taught:
- Every value has a type: integers (3), decimals/floats (3.14), text/strings ("hi"), and booleans (true/false).
- The type decides what operations are legal: adding numbers differs from joining text.
- Converting (casting) turns one type into another, e.g. the text "42" into the number 42.
- Mixing types carelessly is a common bug, so always know what type a value is.
- Types are also promises: a function that expects an int should not receive unparsed text, and a pointer should not receive a plain value.
- When a value crosses a boundary such as input, file parsing, or function parameters, re-check the type assumption at that boundary.

Example:
```c
#include <stdio.h>
#include <stdlib.h>
int main(void) {
    const char *text = "42";              // text that looks like a number
    int n = (int)strtol(text, NULL, 10);  // convert base-10 text to int
    printf("%d\n", n + 5);               // arithmetic now works -> 47
    return 0;
}
```

Practice: Make a variable holding the text "10", convert it to a number, add 5, and print the result. It should print 15, not 105.

Quick check: Why do types matter?

## Day 3: Bitwise operations

Objective: Manipulate individual bits with AND, OR, XOR, NOT, and shifts.

Concepts taught:
- Bitwise operators work on the binary representation of integers, one bit position at a time.
- The core operators are AND (&), OR (|), XOR (^), NOT/complement (~), left shift (<<), and right shift (>>).
- AND keeps a bit only when both inputs have 1 there; OR keeps it when either input has 1; XOR keeps it when the bits differ.
- A mask is an integer with 1s in the positions you want to inspect or change.
- Use flags by assigning each option a power-of-two value, combining options with |, testing with &, toggling with ^, and clearing with & plus a complemented mask.
- Left shift by k moves bits left and is equivalent to multiplying unsigned values by 2^k when no overflow occurs.
- Right shift by k moves bits right; unsigned shifts behave like division by 2^k, while signed behavior depends on the language.
- Parenthesize bit tests such as (flags & READ) != 0 because comparison and bitwise precedence rules are easy to misread.

Example:
```c
#include <stdio.h>
int main(void) {
    unsigned READ = 4, WRITE = 2, EXEC = 1;
    unsigned flags = READ | WRITE;      /* combine */
    printf("%d\n", (flags & WRITE) != 0);
    flags ^= EXEC;                      /* toggle */
    printf("%u\n", flags);
    return 0;
}
```

Practice: Create READ=4, WRITE=2, and EXEC=1 flags. Combine READ and WRITE, print whether WRITE is enabled, then toggle EXEC and print the final flag value.

Quick check: Which bitwise operator tests whether a flag bit is present?

## Day 4: Input and simple programs

Objective: Read user input and turn it into useful values.

Concepts taught:
- Programs get useful when they react to data the user types in.
- Input almost always arrives as text, even when the user types digits.
- Before doing math on it, convert that text into a number (int or float).
- Guard against unexpected input so the program does not crash.
- Treat user input as untrusted: validate that it exists, has the expected shape, and can be converted before using it.
- Separate reading input from processing it so the core logic can be tested without typing at the console.

Example:
```c
#include <stdio.h>
int main(void) {
    int num;                 // where the input will be stored
    printf("Enter a number: ");
    scanf("%d", &num);       // read an int into num (& = its address)
    printf("%d\n", num * 2); // use the value once it is read
    return 0;
}
```

Practice: Ask the user for their age, convert the typed text to a number, add 1, and print 'Next year you will be ' followed by that number.

Quick check: What should you usually do before using numeric input?

## Day 5: Conditionals

Objective: Use if/else logic to make decisions.

Concepts taught:
- Conditionals let a program choose between paths based on a true/false test.
- 'if' runs a block only when its condition is true; 'else' covers the other case; else-if chains more checks.
- Comparison operators (==, !=, <, >, <=, >=) produce the booleans you test.
- Combine conditions with and / or / not to express richer rules.
- Order conditions from most specific to most general when only one branch should run.
- Write the boundary values next to the condition, then test exactly those boundaries.

Example:
```c
#include <stdio.h>
int main(void) {
    int age = 20;            // the value to test
    if (age >= 18)           // parentheses hold the condition
        printf("adult\n");   // runs when the condition is true
    else
        printf("minor\n");   // runs otherwise
    return 0;
}
```

Practice: Set a number variable. Print 'positive' if it is greater than 0, 'negative' if it is less than 0, and 'zero' otherwise.

Quick check: Which construct lets code choose between branches?

## Day 6: Loops

Objective: Repeat work with for/while loops and trace loop state.

Concepts taught:
- A loop repeats a block of code so you do not copy-paste the same lines.
- Use a 'for' loop when you know how many times or are walking a collection; use 'while' to repeat until a condition turns false.
- The loop variable changes each pass; tracing it by hand reveals how the loop behaves.
- Make sure the loop can end, or it runs forever (an infinite loop).
- Before writing a loop, name the loop invariant: what should be true before and after every pass.
- Trace the first iteration, a middle iteration, and the final iteration to catch off-by-one mistakes.

Example:
```c
#include <stdio.h>
int main(void) {
    // for (start; condition; step) repeats while condition holds
    for (int i = 1; i <= 5; i++)  // i counts 1..5
        printf("%d\n", i);       // body runs once per pass
    return 0;
}
```

Practice: Use a loop to print the numbers 1 through 10, each on its own line.

Quick check: What do loops help you avoid writing repeatedly?

## Day 7: Functions and methods

Objective: Package logic into reusable units with parameters and returns.

Concepts taught:
- A function packages a piece of logic under a name so you can reuse it.
- Parameters are the inputs you pass in; the return value is the result you get back.
- Calling a function runs its body with the arguments you supply.
- Functions keep code short, testable, and free of duplication.
- A strong function has one job, a small parameter list, and a return value or side effect that is easy to describe.
- If a function mutates data, say who owns that data and whether callers can see the mutation.

Example:
```c
#include <stdio.h>
int add(int a, int b) {     // declare return and parameter types
    return a + b;           // hand the sum back to the caller
}
int main(void) {
    printf("%d\n", add(2, 3)); // call add and print 5
    return 0;
}
```

Practice: Write a function called square that takes one number and returns it multiplied by itself. Call square(4) and print the result (16).

Quick check: What keyword returns a value from a function/method?

## Day 8: Reading and translating pseudo-code

Objective: Read algorithmic pseudo-code and translate it faithfully to code.

Concepts taught:
- Pseudo-code describes an algorithm without committing to one programming language's syntax.
- Common notation includes arrows for assignment, 'for i = 1 to n' loops, 'while condition do', 'if/then/else', and mathematical symbols such as infinity.
- Translate structure first: function signature, base cases, loops, conditionals, and return points.
- Then translate data access carefully; pseudo-code is often 1-indexed and inclusive, while C, Java, and Python arrays are 0-indexed.
- Preserve the invariant the pseudo-code relies on, such as 'left half is already sorted' during merge sort.
- Verify the translation by tracing both versions on the same tiny input and comparing intermediate state, not just the final answer.
- The most common translation bugs are off-by-one loop bounds, missing recursive base cases, and copying mathematical notation without adapting it to real code.

Example:
```c
#include <stdio.h>
int main(void) {
    int total = 0;
    for (int i = 1; i <= 5; i++) {      /* pseudo-code "1 to 5" */
        total += i;
    }
    printf("%d\n", total);             /* 15 */
    return 0;
}
```

Practice: Translate this pseudo-code to working code and print the result: total <- 0; for i = 1 to 5 do total <- total + i; return total. It should print 15.

Quick check: What kind of bug often appears when translating 1-indexed pseudo-code to real arrays?

## Day 9: Arrays and lists

Objective: Store many values and iterate through them safely.

Concepts taught:
- An array (or list) stores many values in a single ordered container.
- Each item has an index; most languages start at 0, so the first item is index 0.
- You loop over the items to process them one by one.
- Reading past the last valid index is a classic out-of-bounds error.
- Arrays are best when you need compact indexed storage and predictable traversal.
- Always connect the loop bounds to the array length; hard-coded lengths become bugs when input size changes.

Example:
```c
#include <stdio.h>
int main(void) {
    int nums[] = {3, 1, 4};      // a fixed-size array of ints
    for (int i = 0; i < 3; i++)  // index from 0 to length-1
        printf("%d\n", nums[i]); // nums[i] reads element i
    return 0;
}
```

Practice: Make an array/list of the three numbers 3, 1, 4. Loop through it and print their total (8).

Quick check: What is the first index in most C/Python/Java arrays?

## Day 10: Strings

Objective: Process text by indexing, slicing, comparing, and counting.

Concepts taught:
- A string is an ordered sequence of characters (letters, digits, symbols).
- You can index single characters, slice ranges, measure length, and compare strings.
- Strings are often immutable, so 'changing' one usually builds a new string.
- Many problems (palindromes, counting) are just careful string traversal.
- Text processing is usually parsing: strip noise, split into meaningful parts, validate the parts, then convert types.
- In C, remember that a string is a char array ending with '\0'; forgetting room for that terminator causes memory bugs.

Example:
```c
#include <stdio.h>
#include <string.h>          // strlen is declared here
int main(void) {
    char word[] = "level";   // a C string is a char array
    printf("%zu\n", strlen(word)); // counts chars before the \0
    return 0;
}
```

Practice: Set a variable to the word "hello". Print its length (5), then print just its first character (h).

Quick check: What is a string made of?

## Day 11: Hash maps and dictionaries

Objective: Use key-value lookup to reduce repeated scans.

Concepts taught:
- A hash map (dictionary) stores key -> value pairs for fast lookup by key.
- Looking up, inserting, and updating by key are about constant time (O(1)) on average.
- They shine when you would otherwise scan a list repeatedly, e.g. counting occurrences.
- Keys are unique; assigning an existing key overwrites its value.
- Hash maps trade ordering for fast access; choose them when the key is the natural way to find the value.
- Reason about the key's equality rule first because the hash table is only correct when equal keys are treated consistently.

Example:
```c
C has no built-in hash map. Start with arrays/counting tables for small key ranges, then learn structs plus a hash table implementation.
```

Practice: Count how many times each letter appears in the word "apple" using a hash map/dictionary, then print the counts.

Quick check: What is the main advantage of a hash map lookup?

## Day 12: Stacks

Objective: Model last-in-first-out workflows and parentheses problems.

Concepts taught:
- A stack is a last-in, first-out (LIFO) collection: the most recent item comes off first.
- The two core operations are push (add to the top) and pop (remove from the top).
- Think of a stack of plates: you take the top one.
- Stacks model undo history, function calls, and matching brackets/parentheses.
- Stacks are a control-flow data structure: they remember what must be finished later.
- When debugging stack logic, write the stack contents after each push and pop.

Example:
```c
#include <stdio.h>
int main(void) {
    int stack[100];      // an array used as a stack
    int top = 0;         // index of the next free slot
    stack[top++] = 1;    // push 1
    stack[top++] = 2;    // push 2
    int x = stack[--top]; // pop the top value (2)
    printf("%d\n", x);
    return 0;
}
```

Practice: Push the numbers 1, 2, then 3 onto a stack. Pop them off one at a time and print each — they should come out 3, 2, 1.

Quick check: Which item is removed first from a stack?

## Day 13: Two pointers

Objective: Solve sorted-array and in-place problems with two indexes.

Concepts taught:
- The two-pointer technique uses two indexes moving through data to avoid nested loops.
- Common setups: one pointer at each end moving inward, or a slow/fast pair moving the same way.
- It works best on sorted arrays or when pairing/comparing elements.
- It often turns an O(n^2) scan into a single O(n) pass.
- The pointer movement rule is the algorithm: be able to explain why moving left or right cannot skip a valid answer.
- Stop conditions matter; left < right is different from left <= right when the same element cannot be used twice.

Example:
```c
#include <stdio.h>
int main(void) {
    int nums[] = {1, 2, 3, 4, 6};   // sorted
    int left = 0, right = 4, target = 7;
    while (left < right) {          // move pointers inward
        int s = nums[left] + nums[right];
        if (s == target) { printf("%d %d\n", left, right); break; }
        else if (s < target) left++;  // too small
        else right--;                 // too big
    }
    return 0;
}
```

Practice: Given the sorted list [1, 2, 3, 4, 6], use one pointer at each end to find a pair that adds up to 7, and print the two values (1 and 6).

Quick check: Two pointers usually means tracking how many indexes?

## Day 14: Sliding window

Objective: Track a moving range for substring and subarray problems.

Concepts taught:
- A sliding window tracks a contiguous range (subarray/substring) that grows and shrinks as you scan.
- Expand the window by moving the right edge; shrink it by moving the left edge.
- Keep a running total or count so you do not recompute the whole window each step.
- Great for 'longest/shortest/best run that satisfies X' problems.
- A window solution depends on maintaining a summary, such as count, sum, or frequency map, as the endpoints move.
- Ask whether the constraint is fixed-size or variable-size because that decides whether the left edge moves every step or only when invalid.

Example:
```c
#include <stdio.h>
int main(void) {
    int nums[] = {2, 1, 5, 1, 3, 2}, n = 6, k = 3;
    int window = 0;
    for (int i = 0; i < k; i++) window += nums[i]; // first window
    int best = window;
    for (int i = k; i < n; i++) {        // slide right
        window += nums[i] - nums[i - k]; // add new, drop old
        if (window > best) best = window;
    }
    printf("%d\n", best);  // 9
    return 0;
}
```

Practice: Given [2, 1, 5, 1, 3, 2], use a window of size 3 to find and print the largest sum of any 3 numbers in a row (9).

Quick check: A sliding window tracks a moving what?

## Day 15: Binary search

Objective: Cut a sorted or monotonic search space in half.

Concepts taught:
- Binary search finds a target by repeatedly halving a sorted search space.
- Check the middle: if it matches you are done; otherwise discard the half that cannot contain it.
- It needs sorted data, or any condition that is monotonic (false then true).
- It runs in O(log n), far faster than scanning every element.
- Binary search is not only for arrays; it works on any answer space where the predicate changes one direction.
- Use one consistent interval convention, such as closed [lo, hi] or half-open [lo, hi), and keep the update rules matched to it.

Example:
```c
#include <stdio.h>
int main(void) {
    int nums[] = {1, 3, 5, 7, 9}, lo = 0, hi = 4, target = 7;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;     // middle index
        if (nums[mid] == target) { printf("%d\n", mid); break; }
        else if (nums[mid] < target) lo = mid + 1; // right half
        else hi = mid - 1;                          // left half
    }
    return 0;
}
```

Practice: Given the sorted list [1, 3, 5, 7, 9], use binary search to find the value 7 and print its index (3).

Quick check: Binary search requires sorted data or what kind of predicate?

## Day 16: Classes and objects

Objective: Group data and behavior into reusable types.

Concepts taught:
- A class is a blueprint that bundles related data (fields) with behavior (methods).
- An object is one instance made from that class, with its own copy of the data.
- Methods act on the object's own data (this / self).
- Classes help model real things and keep related code together.
- Classes are strongest when they protect a small set of invariants behind methods.
- Fields describe state; methods describe allowed state transitions.

Example:
```c
C has structs, not classes. Use a struct for data and functions that receive a pointer to that struct.
```

Practice: Define a class called Dog with a name and a method bark() that prints '<name> says woof'. Create a Dog named Rex and call bark().

Quick check: Classes group data with what?

## Day 17: Linked lists

Objective: Reason about nodes, next pointers, and pointer rewiring.

Concepts taught:
- A linked list is a chain of nodes; each node holds a value and a reference to the next node.
- Unlike an array there is no direct index, so you reach an item by following next pointers.
- Inserting or removing is cheap once you are at the spot (just rewire pointers); finding the spot is O(n).
- The list ends when a node's next is null/None.
- Diagram each node as data plus next, and draw arrows before coding an insert or delete.
- If you overwrite a next pointer before saving the rest of the list, the diagram shows the lost chain immediately.
- Linked lists make local insert/delete cheap only after you already have the relevant node or previous node.

Example:
```c
#include <stdio.h>
#include <stdlib.h>
struct Node { int value; struct Node *next; }; // value + next
int main(void) {
    struct Node *a = malloc(sizeof(struct Node)); // node 1
    a->value = 1;
    a->next = malloc(sizeof(struct Node));        // node 2
    a->next->value = 2;
    a->next->next = NULL;                         // end of list
    for (struct Node *n = a; n; n = n->next)      // follow next
        printf("%d\n", n->value);
    return 0;
}
```

Practice: Build a linked list of three nodes holding 1, 2, 3. Then walk the list from the start and print each value.

Quick check: A linked list node stores a value and a reference to what?

## Day 18: Recursion

Objective: Solve a problem by reducing it to smaller versions.

Concepts taught:
- Recursion solves a problem by having a function call itself on a smaller version of the problem.
- Every recursion needs a base case that stops it, or it never ends (stack overflow).
- Each call must move closer to the base case.
- Many tree and divide-and-conquer problems are naturally recursive.
- Write the base case first, then the smaller recursive call, then how the current frame combines that result.
- A recursion trace is a stack trace: each call has its own parameters and locals.

Example:
```c
#include <stdio.h>
int factorial(int n) {       // n! = n * (n-1) * ... * 1
    if (n <= 1) return 1;    // base case stops the recursion
    return n * factorial(n - 1); // call itself on a smaller n
}
int main(void) {
    printf("%d\n", factorial(5)); // 120
    return 0;
}
```

Practice: Write a recursive function that computes the factorial of a number (n! = n*(n-1)*...*1). Call it with 5 and print the result (120).

Quick check: What must every recursive solution have?

## Day 19: Trees

Objective: Traverse tree-shaped data with DFS and BFS.

Concepts taught:
- A tree is a hierarchy of nodes starting from a single root; each node has children.
- A binary tree limits each node to at most two children (left and right).
- Visit nodes with traversals: depth-first (DFS: pre/in/post-order) or breadth-first (BFS, level by level).
- Trees model file systems, decisions, and sorted data (binary search trees).
- Draw tree nodes as values with left and right child links; omitted children are null leaves.
- For DFS, draw the call stack beside the tree; for BFS, draw the queue contents at each level.
- Visualization tools are useful because they make traversal order and frontier state visible.

Example:
```c
#include <stdio.h>
struct Node { int value; struct Node *left, *right; };
void visit(struct Node *n) { // depth-first pre-order
    if (!n) return;          // base case: empty branch
    printf("%d\n", n->value);
    visit(n->left);
    visit(n->right);
}
int main(void) {
    struct Node root = {1, NULL, NULL}; // a single-node tree
    visit(&root);            // prints 1
    return 0;
}
```

Practice: Build a small binary tree: a root holding 1 with children 2 and 3. Write a function that visits and prints every node's value.

Quick check: What is the top node of a tree called?

## Day 20: Graphs

Objective: Represent connections and traverse with BFS/DFS.

Concepts taught:
- A graph is a set of nodes (vertices) joined by edges; connections can be one-way or two-way.
- Common representations: an adjacency list (each node lists its neighbors) or an adjacency matrix.
- Traverse with BFS (level by level, good for shortest unweighted paths) or DFS (go deep first).
- Track visited nodes so you do not loop forever on cycles.
- Draw nodes as circles and edges as arrows or lines; write weights directly on weighted edges.
- Adjacency lists are usually better for sparse graphs; adjacency matrices make edge lookup simple but cost O(V^2) space.
- For BFS, number nodes by discovery order; for DFS, mark when the search backtracks; for Dijkstra, track frontier distances.

Example:
```c
#include <stdio.h>
int main(void) {
    // adjacency matrix: edge[a][b] == 1 means a connects to b
    int edge[3][3] = {{0,1,1},{0,0,1},{0,0,0}};
    int from = 0;
    for (int to = 0; to < 3; to++)        // node 0 neighbors
        if (edge[from][to]) printf("0 -> %d\n", to);
    return 0;
}
```

Practice: Store this graph as an adjacency list: node 0 connects to 1 and 2; node 1 connects to 2. Print all the neighbors of node 0.

Quick check: Graph traversal usually uses BFS or what?

## Day 21: Dynamic programming

Objective: Define state, recurrence, base cases, and order.

Concepts taught:
- Dynamic programming solves a problem by combining answers to overlapping subproblems.
- Define the state (what a subproblem means), the recurrence (how states combine), and the base cases.
- Store (memoize) computed answers so each subproblem is solved only once.
- It turns exponential brute force into polynomial time when subproblems repeat.
- DP becomes manageable when you can say exactly what one table cell or memo entry means.
- Pascal's triangle is a clear DP model: each interior value depends on the two values above it.
- Counting operations alongside runtime helps connect the recurrence to empirical growth.

Example:
```c
#include <stdio.h>
int main(void) {
    int n = 10, dp[11];      // dp[i] = i-th Fibonacci number
    dp[0] = 0; dp[1] = 1;    // base cases
    for (int i = 2; i <= n; i++)        // build up from small i
        dp[i] = dp[i - 1] + dp[i - 2];  // the recurrence
    printf("%d\n", dp[n]);   // 55
    return 0;
}
```

Practice: Compute the 10th Fibonacci number by storing each answer in an array/dictionary as you build up. Print the result (55).

Quick check: DP usually stores answers to smaller what?

## Day 22: Heaps and priority queues

Objective: Repeatedly access the smallest or largest item efficiently.

Concepts taught:
- A heap always gives quick access to the smallest (min-heap) or largest (max-heap) item.
- Push and pop are O(log n); peeking at the top item is O(1).
- Use it as a priority queue when you repeatedly need the next most-important item.
- It is ideal for top-k, scheduling, and merging sorted streams.
- A heap gives priority order, not full sorted order; only the root is guaranteed to be the next item.
- Dijkstra uses a min-heap so the next expanded node is the currently cheapest frontier node.

Example:
```c
C has no built-in heap. Store items in an array where the children of index i are 2*i+1 and 2*i+2, and sift values up or down to keep the smallest on top, or use a library.
```

Practice: Put the numbers 5, 1, 8, 3 into a min-heap / priority queue, then remove and print the smallest item (1).

Quick check: A heap is useful when repeatedly taking the min or what?

## Day 23: Matrices

Objective: Traverse rows, columns, and neighbors without index bugs.

Concepts taught:
- A matrix is a 2D grid of values indexed by row and column (grid[r][c]).
- The outer loop usually walks rows; the inner loop walks columns.
- Neighbors are the cells up/down/left/right (sometimes diagonals); check bounds before accessing.
- Off-by-one errors and swapped row/column indexes are the most common bugs.
- Always name dimensions as rows first, columns second; grid[r][c] means row r, column c.
- When matrices represent graphs, matrix[i][j] means the edge from i to j; zero often means no edge unless zero-weight edges are allowed.

Example:
```c
#include <stdio.h>
int main(void) {
    int grid[2][3] = {{1,2,3},{4,5,6}}; // 2 rows, 3 columns
    for (int r = 0; r < 2; r++) {        // walk rows
        for (int c = 0; c < 3; c++)      // walk columns
            printf("%d ", grid[r][c]);   // read one cell
        printf("\n");
    }
    return 0;
}
```

Practice: Make a 2x3 grid of numbers ([[1,2,3],[4,5,6]]). Loop through it and print each row on its own line.

Quick check: A matrix is indexed by row and what?

## Day 24: Design problems

Objective: Build small APIs that preserve invariants over operations.

Concepts taught:
- Design problems ask you to build a small component with specific operations (e.g. a cache or queue).
- Focus on the invariants: the rules that must stay true after every operation.
- Pick data structures that make the required operations efficient.
- Think through edge cases: empty state, capacity limits, and repeated keys.
- Start design problems by listing operations, required complexity, and invariants.
- A good design makes invalid states hard to create and easy to detect in tests.

Example:
```c
#include <stdio.h>
#define CAP 2
struct Stack { int items[CAP]; int size; }; // invariant: size <= CAP
void push(struct Stack *s, int x) {
    if (s->size < CAP) s->items[s->size++] = x; // enforce the cap
}
int main(void) {
    struct Stack s = {{0}, 0};
    push(&s, 1); push(&s, 2); push(&s, 3); // third push ignored
    printf("%d\n", s.size);  // 2
    return 0;
}
```

Practice: Design a Stack class with a capacity of 2 whose push() ignores new items when full. Push 1, 2, 3, then print how many items it holds (2).

Quick check: Design problems are mostly about preserving what over operations?

## Day 25: Systems overview and Linux

Objective: Use Linux command-line tools, permissions, shell redirection, gcc flags, and Makefiles.

Concepts taught:
- Systems programming starts with the operating system: kernel services, user-space programs, files, processes, and permissions.
- The Linux shell lets you navigate, inspect files, compose tools with pipes, redirect input/output, and configure environment variables.
- gcc flags such as -Wall, -Wextra, -g, and -o make compiler feedback and debugging easier.
- A Makefile records how files depend on each other so rebuilds are repeatable.
- Terminal literacy matters because C systems work often happens outside an IDE.
- Shell redirection and pipes are part of the testing surface for command-line C tools.
- Makefiles matter once a lab has multiple .c files because they encode dependencies and flags consistently.

Example:
```c
$ cat > hello.c
#include <stdio.h>
int main(void) { printf("hello\n"); return 0; }
$ gcc -Wall -Wextra -g -o hello hello.c
$ ./hello > out.txt
```

Practice: Write the shell commands to create hello.c, compile it with gcc -Wall -Wextra -g -o hello hello.c, run it, and redirect output to out.txt.

Quick check: What gcc flag includes debug symbols for gdb?

## Day 26: C foundations and headers

Objective: Write C with primitive types, control flow, functions, headers, preprocessing, printf, and scanf.

Concepts taught:
- C has explicit primitive types and does not protect you from many invalid operations at runtime.
- Header files declare interfaces; source files define implementation.
- The preprocessor handles #include, #define, and include guards before the compiler sees normal C.
- Function prototypes let one file call functions defined later or elsewhere.
- printf and scanf require format specifiers that match the actual argument types.
- Headers are contracts between files; keep definitions in .c files unless a constant or macro truly belongs in the interface.
- Compiler warnings are teaching feedback, not noise; fix them before chasing runtime bugs.

Example:
```c
/* math_utils.h */
#ifndef MATH_UTILS_H
#define MATH_UTILS_H
int add(int a, int b);
#endif
/* main.c calls add(2, 3) and prints with printf("%d\n", result). */
```

Practice: Create a tiny two-file C program: math_utils.h declares add(), math_utils.c defines it, and main.c calls it with printf.

Quick check: What file type usually declares C function prototypes?

## Day 27: Command-line arguments in C

Objective: Use argc and argv to configure command-line programs without recompiling.

Concepts taught:
- A command-line C program can declare main as int main(int argc, char **argv) or int main(int argc, char *argv[]).
- argc is the argument count; it is at least 1 because argv[0] is the program name.
- argv is an array of C strings; argv[1] is the first user-supplied argument when argc > 1.
- Always check argc before reading argv[i], or the program can read past the argument array.
- Convert numeric arguments with strtol or strtod so you can detect invalid input instead of trusting atoi silently.
- Command-line arguments make tools reusable: the same executable can read different files, choose a sort, or change input size without recompiling.
- Print usage text to stderr and return a nonzero status when required arguments are missing.

Example:
```c
int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file>\n", argv[0]);
        return 1;
    }
    printf("program=%s file=%s\n", argv[0], argv[1]);
    return 0;
}
```

Practice: Write a C program that requires one filename argument, prints usage to stderr if it is missing, and prints argv[0] and argv[1] when present.

Quick check: Which argv index holds the first user-supplied argument?

## Day 28: File I/O in C

Objective: Read and write files safely with fopen, fgets, fread, fwrite, and fclose.

Concepts taught:
- fopen(path, mode) returns a FILE* or NULL on failure; always check the return value before using the handle.
- Common modes are "r" for read, "w" for overwrite/write, "a" for append, and binary variants such as "rb" and "wb".
- fgets(buffer, size, file) reads at most size - 1 characters, stops at newline or EOF, and always null-terminates when it succeeds.
- Strip a trailing newline after fgets when the line represents a name, key, or token rather than a whole printed line.
- fscanf reads formatted data from a file; fread and fwrite read/write binary blocks with explicit byte counts.
- fclose flushes buffered output and releases the file descriptor; every successful fopen needs a matching fclose on all paths.
- stdin, stdout, and stderr are already-open FILE* streams; use fprintf(stderr, ...) for errors so normal output can be redirected cleanly.
- The lab pattern is argc/argv path validation, fopen, loop with fgets, parse and validate each line, build a data structure, close the file, then free all allocated memory.

Example:
```c
FILE *fp = fopen(argv[1], "r");
if (!fp) { perror(argv[1]); return 1; }
char line[256];
int lines = 0;
while (fgets(line, sizeof line, fp) != NULL) {
    lines++;
}
fclose(fp);
printf("%d\n", lines);
```

Practice: Write a C program that opens the filename from argv[1], reads it line by line with fgets, counts the lines, closes the file, and prints the count.

Quick check: What does fopen return on failure?

## Day 29: Pointers and memory management

Objective: Use pointers, arrays, dynamic allocation, pointer parameters, valgrind, and safe memory habits.

Concepts taught:
- A pointer stores an address; dereferencing follows the address to read or write the pointed value.
- Arrays and pointers are closely related, but arrays still have storage and size context you must track yourself.
- Passing a pointer lets a function mutate caller-owned data, which is C's pass-by-reference pattern.
- Pointer-to-pointer forms such as char **argv let a function update a pointer or walk arrays of strings.
- Function pointers let you store callable behavior, such as callbacks or sort comparators.
- malloc/calloc/realloc allocate heap memory; every successful allocation needs a matching free when ownership ends.
- Valgrind helps find leaks, invalid reads/writes, double frees, and use-after-free bugs.
- Draw stack variables and heap blocks separately; arrows should show which pointer owns or refers to each block.
- For every malloc, write down the matching free location and which function is responsible for it.

Example:
```c
void increment(int *p) { (*p)++; }
int *value = malloc(sizeof *value);
*value = 41;
increment(value);
printf("%d\n", *value);   /* 42 */
free(value);
```

Practice: Write a C function increment(int *p), allocate an int with malloc, call increment, print the value, then free it.

Quick check: What C function releases heap memory?

## Day 30: Structs and custom data types

Objective: Define structs, typedefs, enums, unions, self-referential nodes, and allocated records.

Concepts taught:
- struct groups fields into one custom record type.
- typedef can give a struct a shorter name but should not hide pointer ownership rules.
- Self-referential structs support linked lists, trees, and graphs by storing pointers to the same struct type.
- Enums name integer states; unions let multiple fields share the same memory when only one is active.
- Dynamically allocated structs need clear create/destroy functions to keep ownership explicit.
- Struct layout turns related fields into one unit, which is essential for nodes, graph edges, table entries, and records.
- Self-referential structs need a named struct tag because the type refers to itself before the typedef is complete.

Example:
```c
typedef struct Node {
    int value;
    struct Node *next;
} Node;
Node *n = malloc(sizeof *n);
n->value = 1; n->next = NULL;
free(n);
```

Practice: Define a typedef struct Student with name and id, allocate one Student, fill fields, print it, and free it.

Quick check: What C keyword groups fields into a custom record?

## Day 31: Debugging, assembly, and CPU basics

Objective: Debug C with gdb and connect compiled code to registers, branches, and CPU execution.

Concepts taught:
- gdb lets you set breakpoints, step by line or instruction, print variables, and inspect the call stack.
- Assembly exposes registers, moves, arithmetic, comparisons, jumps, calls, and returns generated from C.
- The CPU repeatedly fetches, decodes, and executes instructions.
- Registers are tiny fast storage locations; memory is addressed through loads and stores.
- Reading simple assembly helps explain undefined behavior, stack frames, and optimization surprises.
- Godbolt Compiler Explorer lets you paste C and compare generated assembly across compilers and optimization levels.
- Try x * 32 and x << 5 at different optimization levels; compilers often generate the same shift instruction.
- Assembly inspection is most useful when tied to a question: why is this slower, where is this branch, or what did optimization remove?

Example:
```c
$ gdb ./app
(gdb) break main
(gdb) run
(gdb) next
(gdb) print i
(gdb) disassemble /m main
```

Practice: Write a short C loop and list the gdb commands to break at main, step, print the loop variable, and inspect the backtrace.

Quick check: What debugger is commonly used for C programs on Linux?

## Day 32: Compilers, linkers, and code generation

Objective: Trace preprocessing, compilation, assembly, linking, object files, and symbol resolution.

Concepts taught:
- The C build pipeline preprocesses, compiles to assembly, assembles to object files, and links into an executable.
- Object files contain compiled code plus symbols that the linker resolves across files and libraries.
- Static linking copies library code into the executable; dynamic linking loads shared libraries at runtime.
- Name resolution fails when declarations, definitions, or linker inputs disagree.
- Separate compilation keeps large C programs modular but requires accurate headers and build rules.
- A declaration tells the compiler a symbol exists; a definition gives the linker actual storage or code to connect.
- Linker errors usually mean the build command or function definitions do not match the headers.

Example:
```c
$ gcc -E main.c -o main.i      # preprocess
$ gcc -S main.i -o main.s      # compile to assembly
$ gcc -c main.s -o main.o      # assemble
$ gcc main.o util.o -o app     # link symbols into executable
```

Practice: Write commands that compile main.c and util.c into .o files, link them into app, then explain which step resolves symbols.

Quick check: What build stage resolves symbols across object files?

## Day 33: Function pointers in C

Objective: Declare function pointers, build dispatch tables, and use callbacks with qsort.

Concepts taught:
- A function pointer stores the address of a function whose parameter and return types match the pointer type.
- Declare one as return_type (*name)(param_types); the parentheses around *name are required.
- Assign a function pointer with the function name, such as cmp = compare_ints; no call parentheses are used during assignment.
- Call through the pointer with ptr(args) or (*ptr)(args); both forms are common C.
- Use typedef to keep signatures readable, for example typedef int (*cmp_t)(const void *, const void *).
- Arrays of function pointers are dispatch tables: pick behavior by index or enum instead of a long if/else chain.
- Callbacks pass behavior into reusable algorithms; qsort(base, count, size, compare) is the standard library example.
- Common bugs are missing declaration parentheses, mismatched signatures, storing a pointer to the wrong function type, and calling a NULL function pointer.

Example:
```c
int add(int a, int b) { return a + b; }
int mul(int a, int b) { return a * b; }
typedef int (*op_t)(int, int);
op_t ops[] = {add, mul};
printf("%d\n", ops[1](6, 7));  /* 42 */
```

Practice: Create two small int functions, store them in an array of function pointers, call one by index, and print the result.

Quick check: What C standard library sort function takes a compare callback?

## Day 34: Bitwise operations and bit fields in C

Objective: Apply bitwise operators to flags, masks, hashing, and packed struct fields.

Concepts taught:
- C bitwise work should usually use unsigned integer types such as uint32_t so shifts and overflow are predictable.
- Bit fields can pack flags inside a struct, for example unsigned int active : 1, but exact layout is implementation-defined.
- Masks let you set, clear, toggle, and test specific bits in permissions, status words, and hardware-style registers.
- Hash functions use shifts and XOR to mix input bits so similar strings land in different buckets.
- Right-shifting a signed negative integer is implementation-defined, so prefer unsigned values for portable bit algorithms.
- Shifting by a negative count or by a count greater than or equal to the width of the type is undefined behavior.
- Use fixed-width types from stdint.h when the number of bits matters.

Example:
```c
#include <stdint.h>
uint32_t set_bit(uint32_t x, unsigned bit) { return x | (1u << bit); }
uint32_t clear_bit(uint32_t x, unsigned bit) { return x & ~(1u << bit); }
int test_bit(uint32_t x, unsigned bit) { return (x & (1u << bit)) != 0; }
printf("%d\n", test_bit(set_bit(0, 3), 3));
```

Practice: Write C functions set_bit, clear_bit, toggle_bit, and test_bit for a uint32_t value. Demonstrate each with printf.

Quick check: What unsigned fixed-width header provides uint32_t?

## Day 35: Processes and memory hierarchy

Objective: Explain processes, stack frames, heap/data/text segments, caches, locality, and virtual memory.

Concepts taught:
- A process is a running program with its own virtual address space and OS-managed state.
- C program memory is commonly described as text, data, BSS, heap, and stack segments.
- Each function call creates a stack frame for return address, saved state, parameters, and locals.
- The memory hierarchy moves from registers to cache to RAM to disk, with latency increasing at each level.
- Virtual memory maps pages through page tables so each process sees a private address space.
- Spatial and temporal locality explain why contiguous arrays often outperform pointer-heavy structures.
- Stack frames explain why local variables disappear after return and why deep recursion can fail.
- Cache locality explains why contiguous arrays can outperform pointer-heavy structures even with the same Big-O.

Example:
```c
int global_count;              /* BSS */
int initialized = 3;           /* data */
int main(void) {
    int local = 1;             /* stack */
    int *heap = malloc(sizeof *heap); /* heap */
    free(heap);
}
```

Practice: Draw or write a labeled memory map for one C program showing text, data, BSS, heap, stack, and one variable in each where possible.

Quick check: Which memory region grows and shrinks as functions call and return?

## Day 36: Concurrency and threads

Objective: Use pthreads, joins, mutexes, shared state, race-condition reasoning, and deadlock avoidance.

Concepts taught:
- Threads share a process address space, so communication is easy and accidental races are also easy.
- pthread_create starts work in a new thread; pthread_join waits for it to finish.
- A race condition occurs when correctness depends on unpredictable timing between threads.
- Mutexes protect critical sections so only one thread mutates shared state at a time.
- Producer-consumer designs use locks or condition variables to coordinate handoff between threads.
- Deadlock can happen when threads hold locks while waiting for locks held by each other.
- If two threads can touch the same mutable value, decide which lock or ownership rule protects it.
- Race bugs are schedule-dependent, so passing once does not prove the code is safe.

Example:
```c
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
int counter = 0;
void *worker(void *arg) {
    pthread_mutex_lock(&lock);
    counter++;
    pthread_mutex_unlock(&lock);
    return NULL;
}
```

Practice: Write a pthread counter example guarded by a mutex. Include the race that would occur if the lock were removed.

Quick check: What pthread primitive protects a critical section?

## Day 37: Networking and sockets

Objective: Build a basic client-server model with IPs, ports, TCP sockets, send, and recv.

Concepts taught:
- Networking code usually models clients connecting to servers over IP addresses and ports.
- TCP provides reliable byte streams; UDP sends datagrams without the same delivery guarantees.
- A server socket binds, listens, accepts a connection, then sends/receives bytes.
- A client socket connects to a server, then uses send and recv to exchange data.
- Socket code must handle partial reads/writes, errors, and resource cleanup.
- Sockets are file descriptors with protocol behavior; they still need close and error checks.
- TCP sends a stream, not message objects, so code must handle partial reads and writes.

Example:
```c
int fd = socket(AF_INET, SOCK_STREAM, 0);
bind(fd, (struct sockaddr *)&addr, sizeof addr);
listen(fd, 8);
int client = accept(fd, NULL, NULL);
recv(client, buffer, sizeof buffer, 0);
send(client, "ok", 2, 0);
```

Practice: Sketch the server-side socket call order: socket, bind, listen, accept, recv, send, close. Add one line describing the client connect path.

Quick check: Which server socket call waits for an incoming client connection?

## Day 38: Linked lists in C

Objective: Implement singly and doubly linked lists with insert, delete, search, traversal, and full cleanup.

Concepts taught:
- Linked list operations are pointer rewrites: insert, delete, search, traverse, and free.
- Head/tail insertions need different edge-case handling when the list is empty.
- Deletion must reconnect neighbors before freeing the removed node.
- Doubly linked lists trade extra memory for easier backward traversal and deletion.
- Generic lists with void* require clear ownership and casting rules.
- For delete operations, keep track of both current and previous nodes so you can reconnect the chain.
- Freeing a list requires saving next before freeing current; otherwise you lose the only path forward.

Example:
```c
Node *insert_head(Node *head, int value) {
    Node *n = malloc(sizeof *n);
    n->value = value;
    n->next = head;
    return n;
}
```

Practice: Implement insert_head, search, delete_value, print_list, and free_list for a singly linked list of ints.

Quick check: What must you do to every heap-allocated linked-list node when done?

## Day 39: Stacks and queues in C

Objective: Implement stack and queue ADTs with arrays, linked lists, and circular-buffer tradeoffs.

Concepts taught:
- A stack supports push, pop, and peek with LIFO behavior.
- A queue supports enqueue and dequeue with FIFO behavior.
- Array-backed ADTs need capacity checks and sometimes circular indexing.
- Linked implementations grow flexibly but allocate one node per item.
- Stacks support expression evaluation; queues support BFS and producer-consumer buffering.
- Array stacks are simple and cache-friendly but fixed-capacity unless resized.
- Circular queues avoid moving elements by wrapping front and back indexes with modulo arithmetic.

Example:
```c
typedef struct { int items[8]; int top; } Stack;
int push(Stack *s, int x) {
    if (s->top == 8) return 0;
    s->items[s->top++] = x;
    return 1;
}
```

Practice: Implement either an array stack with capacity checks or a circular-array queue with wraparound indexes.

Quick check: Which ADT removes the oldest inserted item first?

## Day 40: Formal algorithm analysis

Objective: Analyze loops and recurrences with Big-O, Omega, Theta, substitution, Master theorem, and amortization.

Concepts taught:
- Big-O is an upper bound, Big-Omega is a lower bound, and Big-Theta is a tight bound.
- Loop analysis depends on how many times each statement runs as n grows.
- Recursive algorithms can be described with recurrences such as T(n)=2T(n/2)+n.
- Substitution, recursion trees, and the Master theorem are ways to solve recurrences.
- Best case, worst case, and average case describe different input scenarios for the same algorithm.
- Amortized analysis explains average cost over a sequence of operations, not random average case.
- State what n represents before analyzing; n might be elements, vertices, edges, rows, or characters.
- Separate theoretical growth from measured runtime because constants and hardware still affect small inputs.

Example:
```c
for (int i = 0; i < n; i++)
for (int j = 0; j < n; j++)
        work();
/* n*n calls, so time is O(n^2), Omega(n^2), and Theta(n^2). */
```

Practice: Analyze one nested loop and one recurrence. State Big-O, Big-Omega, Big-Theta, and the reasoning.

Quick check: What notation gives a tight asymptotic bound?

## Day 41: Runtime benchmarking in C

Objective: Time code with clock_gettime, report elapsed seconds, and compare algorithm runtimes.

Concepts taught:
- clock_gettime(CLOCK_MONOTONIC, &ts) captures a high-resolution monotonic timestamp that is not affected by wall-clock changes.
- struct timespec stores seconds in tv_sec and nanoseconds in tv_nsec.
- Compute elapsed seconds as (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9.
- Time only the code you mean to measure; printing inside the timed block can dominate the algorithm runtime.
- Run multiple trials and compare medians or trends because OS scheduling, cache state, and background processes create noise.
- Use the same input sizes, compiler flags, machine, and data-generation method when comparing algorithms.
- Empirical timings should support your Big-O reasoning; they do not replace asymptotic analysis.

Example:
```c
struct timespec start, end;
clock_gettime(CLOCK_MONOTONIC, &start);
run_algorithm();
clock_gettime(CLOCK_MONOTONIC, &end);
double seconds = (end.tv_sec - start.tv_sec)
    + (end.tv_nsec - start.tv_nsec) / 1e9;
printf("%f\n", seconds);
```

Practice: Use clock_gettime(CLOCK_MONOTONIC) to time a loop or sort function across at least three input sizes, then print a timing table.

Quick check: Which clock should C benchmarks use to avoid wall-clock adjustments?

## Day 42: Quadratic sorting

Objective: Trace selection, insertion, and bubble sort, including stability and in-place behavior.

Concepts taught:
- Selection sort repeatedly selects the smallest remaining item and places it in final position.
- Insertion sort builds a sorted prefix and is efficient on nearly sorted data.
- Bubble sort repeatedly swaps adjacent inverted pairs; early exit stops when no swaps occur.
- Stable sorts preserve the relative order of equal keys.
- In-place algorithms use only small extra memory beyond the input array.
- Sorting labs should trace the array after each outer pass so the invariant becomes visible.
- An early-exit bubble sort changes the best case from quadratic work to linear checking.

Example:
```c
for (int i = 1; i < n; i++) {
    int x = a[i], j = i - 1;
    while (j >= 0 && a[j] > x) { a[j + 1] = a[j]; j--; }
    a[j + 1] = x;             /* insertion sort */
}
```

Practice: Implement insertion sort in C and add comments tracing how the sorted prefix grows on [5, 2, 4, 1].

Quick check: Which quadratic sort is often efficient on nearly sorted data?

## Day 43: Random test data in C

Objective: Generate random arrays, graphs, and test inputs with reproducible seeds.

Concepts taught:
- srand(seed) initializes C's pseudo-random number generator; call it once near the start of main.
- srand(time(NULL)) changes the sequence between runs, while srand(42) makes a test replayable.
- rand() returns an integer from 0 through RAND_MAX; rand() % n gives a simple value in [0, n) but can be biased.
- For sorting tests, generate sorted, reversed, random, duplicate-heavy, empty, and single-element arrays.
- For graph tests, generate edge candidates and add an edge when a random value is below a chosen probability.
- When a random test fails, print the seed, size, and case type so the same input can be reproduced.
- Random tests find surprising cases, but they should sit beside deterministic boundary tests.

Example:
```c
srand(42);                     /* fixed seed for replay */
int values[8];
for (int i = 0; i < 8; i++) {
    values[i] = rand() % 100;
}
printf("seed=42 first=%d\n", values[0]);
```

Practice: Generate a random array using srand with a fixed seed, sort it, verify it is sorted, and print the seed plus pass/fail.

Quick check: Why print the seed when a random test fails?

## Day 44: N log n sorting and proofs

Objective: Implement merge sort and quicksort while reasoning about lower bounds and loop invariants.

Concepts taught:
- Merge sort divides the array, sorts halves, then merges into sorted order.
- Quicksort partitions around a pivot; pivot choice controls worst-case risk.
- Comparison sorting has a lower bound of Omega(n log n) in the general case.
- Loop invariants state what remains true before and after each loop iteration.
- Correctness proofs connect invariants, termination, and postconditions.
- Merge sort uses extra temporary storage, so it is not in-place in the strict sense.
- When translating pseudo-code merge sort, be explicit about inclusive bounds l, m, and r.

Example:
```c
int partition(int a[], int lo, int hi) {
    int pivot = a[hi], i = lo;
    for (int j = lo; j < hi; j++)
        if (a[j] <= pivot) swap(&a[i++], &a[j]);
    swap(&a[i], &a[hi]);
    return i;
}
```

Practice: Implement merge sort or quicksort in C and write a loop invariant for the merge or partition step.

Quick check: What proof tool states what remains true each loop iteration?

## Day 45: Trees, heaps, and heap sort

Objective: Implement binary trees, BST operations, heap operations, heap sort, and priority queues.

Concepts taught:
- Binary tree nodes store a value and left/right child pointers.
- Tree traversals include inorder, preorder, postorder, and level-order BFS.
- BST search, insert, and delete rely on the invariant left < node < right.
- Heaps keep the min or max at the root while allowing efficient insert and extract.
- Heap sort builds a heap then repeatedly extracts the next ordered item.
- When building a tree from file input, parse one line, validate it, insert it, then move to the next line.
- Tree traversal output is easiest to verify by comparing preorder, inorder, and postorder on a small known tree.

Example:
```c
typedef struct Node { int key; struct Node *left, *right; } Node;
Node *search(Node *root, int key) {
    if (!root || root->key == key) return root;
    return key < root->key ? search(root->left, key)
                           : search(root->right, key);
}
```

Practice: Implement BST search and insert, then describe how a min-heap would store the same values in an array.

Quick check: What BST invariant compares values in the left subtree to the node?

## Day 46: Hash tables in C

Objective: Build hash maps with hash functions, chaining, open addressing, load factor, and resizing.

Concepts taught:
- A hash function maps keys to bucket indexes and should spread typical keys evenly.
- Chaining stores collisions in bucket lists; open addressing probes for another slot.
- Load factor measures how full the table is and guides resizing.
- Average lookup can be O(1), but poor hashing or high load can degrade to O(n).
- A C hash map must handle key ownership, equality, collision storage, and cleanup.
- Collision metrics such as longest chain and filled-bucket percentage reveal more than total collision count alone.
- Load factor has to be interpreted with the collision strategy; chaining and open addressing degrade differently.

Example:
```c
unsigned hash(const char *s) {
    unsigned h = 5381;
    while (*s) h = h * 33u + (unsigned char)*s++;
    return h;
}
/* bucket = hash(key) % capacity; collisions go in a linked list. */
```

Practice: Build a small chained hash table for string keys with insert and search. Track load factor after each insert.

Quick check: What hash-table metric usually triggers resizing?

## Day 47: Hash function design in C

Objective: Implement and compare djb2, FNV-1a, and Jenkins OAAT hash functions.

Concepts taught:
- A good non-cryptographic hash spreads typical keys uniformly and is cheap enough to run on every lookup.
- The avalanche effect means a small input change should flip many output bits, reducing clustered collisions.
- djb2 starts at 5381 and updates with hash = hash * 33 + c; the multiply by 33 can be written as (hash << 5) + hash.
- FNV-1a starts with an offset basis, XORs each byte into the hash, then multiplies by the FNV prime.
- Jenkins one-at-a-time repeatedly adds bytes, shifts, and XORs, then performs final mix steps for stronger avalanche.
- Compare algorithms on the same dataset and table size using total collisions, longest chain, average non-empty chain length, filled buckets, and load factor.
- No simple hash is best for every dataset; choose based on key shape, table size, collision cost, and performance budget.
- These functions are not cryptographic hashes; use a cryptographic library when collision resistance against attackers matters.

Example:
```c
uint32_t djb2(const char *s) {
    uint32_t hash = 5381u;
    while (*s) {
        hash = ((hash << 5) + hash) + (unsigned char)*s++;
    }
    return hash;
}
```

Practice: Implement djb2 and FNV-1a for strings, hash the same list of words into a fixed table size, and print collision counts.

Quick check: What hash property means small input changes affect many output bits?

## Day 48: Graph algorithms

Objective: Represent graphs and implement BFS, DFS, topological sort, Dijkstra, and MST awareness.

Concepts taught:
- Graphs can be represented as adjacency matrices or adjacency lists.
- BFS explores by distance layers and gives shortest paths in unweighted graphs.
- DFS explores deeply and supports cycle checks, connected components, and topological sort.
- Topological sort orders a DAG so every edge goes from earlier to later in the output.
- Dijkstra computes shortest paths when edge weights are nonnegative.
- Minimum spanning tree algorithms such as Prim and Kruskal connect weighted undirected graphs cheaply.
- Converting an adjacency list to a matrix means visiting each stored edge and writing matrix[src][dst] = weight.
- Converting a matrix to a list means scanning every cell and adding an edge for each nonzero or present value.
- Dense graphs push you toward matrices; sparse graphs usually favor adjacency lists.

Example:
```c
int graph[4][4] = {{0,1,1,0},{0,0,0,1},{0,0,0,1},{0,0,0,0}};
int queue[4], front = 0, back = 0, seen[4] = {1,0,0,0};
queue[back++] = 0;             /* BFS starts at node 0 */
```

Practice: Represent a graph with adjacency lists and implement BFS that prints distance from a start node.

Quick check: Which graph algorithm finds shortest paths in unweighted graphs?

## Day 49: Greedy algorithms

Objective: Use greedy choice and optimal substructure, and test where greedy algorithms fail.

Concepts taught:
- Greedy algorithms make the locally best choice and never revisit it.
- They are correct only when the problem has a greedy choice property and optimal substructure.
- Activity selection and fractional knapsack are classic successful greedy examples.
- Huffman coding uses greedy merging to build optimal prefix codes.
- A proof of greedy correctness often uses exchange arguments or contradiction-style reasoning.
- Counterexamples are essential because many problems look greedy but require DP or search.
- A greedy algorithm needs a proof or counterexample search, not only a plausible local rule.
- When a greedy idea fails, the failure case often points to a DP state you were missing.

Example:
```c
typedef struct { int start, finish; } Activity;
/* Sort by finish time, then choose the next activity whose start
   is >= the finish time of the last chosen activity. */
```

Practice: Implement activity selection after sorting intervals by finish time. Add one counterexample where a different greedy rule fails.

Quick check: What property justifies making a locally optimal choice?

## Day 50: Dynamic programming in C

Objective: Design memoized and tabulated solutions for Fibonacci, coin change, knapsack, and LCS.

Concepts taught:
- DP applies when subproblems overlap and optimal solutions contain optimal substructure.
- Memoization solves recursively and caches answers; tabulation fills a table bottom-up.
- A good DP solution defines state, recurrence, base cases, iteration order, and answer extraction.
- Coin change, 0/1 knapsack, and LCS show different state shapes.
- Space optimization keeps only the rows or states needed for future transitions.
- For Pascal's triangle, a 2D table makes dependencies visible: table[n][k] depends on table[n-1][k-1] and table[n-1][k].
- Memoized recursion and bottom-up tabulation can compute the same values in different orders.

Example:
```c
int dp[amount + 1];
dp[0] = 0;
for (int x = 1; x <= amount; x++) dp[x] = INF;
for (int x = 1; x <= amount; x++)
    for (int i = 0; i < coin_count; i++)
        if (coins[i] <= x) dp[x] = min(dp[x], 1 + dp[x - coins[i]]);
```

Practice: Implement bottom-up coin change or LCS in C. Name the state, recurrence, base cases, and table order.

Quick check: What DP approach fills a table from base cases upward?

## Day 51: Integrated C review

Objective: Connect memory, compilation, sorting, recurrences, and dynamic programming in one review exercise.

Concepts taught:
- Use this review lesson to integrate earlier C systems and algorithm topics instead of learning a brand-new data structure.
- Trace stack vs. heap lifetime, pointer aliasing, malloc/free ownership, and command-line argument flow without running the code.
- Review compilation stages: preprocessing, compiling, assembling, linking, object files, symbols, and executable output.
- Be ready to compare selection, insertion, bubble, merge, and quicksort by runtime, space use, stability, and invariants.
- Practice recurrence setup and dynamic-programming state definitions because these connect Modules 04 through 06.

Example:
```c
/* Midterm review map:
   - stack/local variables vs heap malloc/free ownership
   - gcc preprocessing -> compile -> assemble -> link
   - insertion/selection/bubble vs merge/quick sort tradeoffs
   - recurrence setup and DP state/base/table order
*/
```

Practice: Create a one-page review map linking stack/heap ownership, compilation stages, sorting tradeoffs, recurrence setup, and dynamic-programming state.

Quick check: Which C memory region stores malloc-allocated objects?

## Day 52: Correctness proofs and invariants

Objective: State preconditions, postconditions, loop invariants, induction steps, and termination arguments.

Concepts taught:
- Correctness proofs explain why an algorithm returns the right answer for every valid input, not just why it seems to work on examples.
- A precondition states what must be true before the algorithm starts; a postcondition states what must be true when it finishes.
- A loop invariant is true before the loop, preserved by each iteration, and useful when the loop terminates.
- Induction proves recursive and iterative algorithms by showing a base case and a step from smaller or earlier cases to the next case.
- Connect correctness arguments to sorting, graph traversal, greedy choices, dynamic programming recurrences, and hash-table invariants.

Example:
```c
/* Binary search correctness:
   Precondition: array is sorted.
   Invariant: if target exists, it is inside [lo, hi].
   Each step keeps the invariant and shrinks the interval.
   Termination gives either found index or empty interval.
*/
```

Practice: Write a correctness argument for insertion sort or binary search. State the precondition, postcondition, loop invariant, and why termination gives the result.

Quick check: What proof statement must stay true before and after every loop iteration?

## Day 53: Recursion and divide-and-conquer

Objective: Trace C recursion, stack growth, termination, tail recursion, and divide/conquer/combine patterns.

Concepts taught:
- Every recursive function needs a base case, recursive case, and progress toward termination.
- C recursion uses stack frames, so deep recursion can overflow the stack.
- Divide-and-conquer splits a problem, solves independent subproblems, and combines their answers.
- Merge sort, quicksort, binary search, and fast exponentiation all fit this pattern.
- Tail recursion can often be rewritten as iteration when stack use matters.
- Divide-and-conquer should shrink the input each call and combine results only after subproblems are solved.
- Trace recursion with parameters, not only return values, because wrong bounds cause most C recursion bugs.

Example:
```c
int binary_search(int a[], int lo, int hi, int target) {
    if (lo > hi) return -1;
    int mid = (lo + hi) / 2;
    if (a[mid] == target) return mid;
    if (a[mid] < target) return binary_search(a, mid + 1, hi, target);
    return binary_search(a, lo, mid - 1, target);
}
```

Practice: Write recursive binary search in C, then rewrite it iteratively and compare stack usage.

Quick check: What three steps describe divide-and-conquer?
