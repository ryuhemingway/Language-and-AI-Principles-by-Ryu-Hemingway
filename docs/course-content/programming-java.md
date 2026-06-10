# Java Programming Course Coverage

Total lessons: 40

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Day 1: Variables and output

Objective: Store values, name them clearly, and print results.

Concepts taught:
- A variable is a named box in memory that holds a value you can read and change later.
- You assign with '=': the name goes on the left, the value on the right.
- Pick clear names (score, user_name) so the code explains itself.
- Printing a variable shows its current value, which is how you check your work.

Example:
```java
public class Main {                       // code lives in a class
    public static void main(String[] args) {  // program entry point
        int score = 10;                   // a typed variable
        System.out.println(score);        // print, then newline
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        int n = 42;                  // integer
        double pi = 3.14;            // floating-point
        String text = "42";          // text that looks like a number
        System.out.println(Integer.parseInt(text) + n); // parse -> 84
    }
}
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
```java
import java.util.Scanner;            // Scanner reads input
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int num = sc.nextInt();      // read an int the user types
        System.out.println(num * 2); // use the value
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        int age = 20;                    // value to test
        if (age >= 18)                   // condition in parentheses
            System.out.println("adult"); // runs when true
        else
            System.out.println("minor"); // runs otherwise
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        // for (start; condition; step) repeats while true
        for (int n = 1; n <= 5; n++)     // n counts 1..5
            System.out.println(n);       // body runs each pass
    }
}
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
```java
public class Main {
    static int add(int a, int b) {       // typed params + return
        return a + b;                    // send the sum back
    }
    public static void main(String[] args) {
        System.out.println(add(2, 3));   // prints 5
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        int[] nums = {3, 1, 4};          // an array of ints
        for (int n : nums)               // for-each visits each item
            System.out.println(n);       // prints 3, 1, 4
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        String word = "level";           // String holds text
        System.out.println(word.length()); // length() counts chars
    }
}
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
```java
import java.util.*;          // Map and HashMap live here
public class Main {
    public static void main(String[] args) {
        Map<Character, Integer> counts = new HashMap<>(); // key->count
        for (char ch : "banana".toCharArray())   // each character
            counts.put(ch, counts.getOrDefault(ch, 0) + 1); // +1, def 0
        System.out.println(counts);      // {a=3, b=1, n=2}
    }
}
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
```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        Deque<Integer> stack = new ArrayDeque<>(); // used as a stack
        stack.push(1);               // push onto the top
        stack.push(2);
        System.out.println(stack.pop()); // pop the top -> 2
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4, 6}; // sorted
        int left = 0, right = 4, target = 7;
        while (left < right) {        // move pointers inward
            int s = nums[left] + nums[right];
            if (s == target) { System.out.println(left + "," + right); break; }
            else if (s < target) left++; // too small
            else right--;                // too big
        }
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        int[] nums = {2, 1, 5, 1, 3, 2};
        int k = 3, window = 0;
        for (int i = 0; i < k; i++) window += nums[i]; // first window
        int best = window;
        for (int i = k; i < nums.length; i++) {    // slide right
            window += nums[i] - nums[i - k];        // add new, drop old
            best = Math.max(best, window);
        }
        System.out.println(best);  // 9
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        int[] nums = {1, 3, 5, 7, 9};
        int lo = 0, hi = 4, target = 7;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;     // middle index
            if (nums[mid] == target) { System.out.println(mid); break; }
            else if (nums[mid] < target) lo = mid + 1; // right half
            else hi = mid - 1;                          // left half
        }
    }
}
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
```java
class Counter {           // a class bundles data and behavior
    int value = 0;        // a field stored on each object
    void inc() {          // a method that acts on this object
        value++;          // increase this object's value by 1
    }
}
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
```java
public class Main {
    static class Node {          // one link in the chain
        int value; Node next;
        Node(int v) { value = v; }
    }
    public static void main(String[] args) {
        Node a = new Node(1);    // build 1 -> 2
        a.next = new Node(2);
        for (Node n = a; n != null; n = n.next) // follow next
            System.out.println(n.value);
    }
}
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
```java
public class Main {
    static int factorial(int n) {    // n! = n * (n-1) * ... * 1
        if (n <= 1) return 1;        // base case stops recursion
        return n * factorial(n - 1); // smaller subproblem
    }
    public static void main(String[] args) {
        System.out.println(factorial(5)); // 120
    }
}
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
```java
public class Main {
    static class Node {          // a binary tree node
        int value; Node left, right;
        Node(int v) { value = v; }
    }
    static void visit(Node n) {  // depth-first pre-order
        if (n == null) return;   // base case: empty branch
        System.out.println(n.value);
        visit(n.left);
        visit(n.right);
    }
    public static void main(String[] args) {
        Node root = new Node(1);
        root.left = new Node(2);
        visit(root);             // 1 2
    }
}
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
```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        // adjacency list: a node maps to its neighbors
        Map<Integer, List<Integer>> g = new HashMap<>();
        g.put(0, Arrays.asList(1, 2));
        for (int to : g.get(0))  // list node 0 neighbors
            System.out.println("0 -> " + to);
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        int n = 10;
        int[] dp = new int[n + 1];   // dp[i] = i-th Fibonacci
        dp[0] = 0; dp[1] = 1;        // base cases
        for (int i = 2; i <= n; i++)        // build up
            dp[i] = dp[i - 1] + dp[i - 2];  // the recurrence
        System.out.println(dp[n]);   // 55
    }
}
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
```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        // PriorityQueue is a min-heap by default
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        heap.add(5); heap.add(1); heap.add(8);
        System.out.println(heap.poll()); // 1 -- smallest first
    }
}
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
```java
public class Main {
    public static void main(String[] args) {
        int[][] grid = {{1, 2, 3}, {4, 5, 6}}; // 2 rows, 3 cols
        for (int r = 0; r < grid.length; r++) {      // walk rows
            for (int c = 0; c < grid[0].length; c++) // walk columns
                System.out.print(grid[r][c] + " ");  // one cell
            System.out.println();
        }
    }
}
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
```java
public class Main {
    static class Stack {         // a stack with a size limit
        int[] items; int size = 0;
        Stack(int cap) { items = new int[cap]; } // invariant: size<=cap
        void push(int x) {
            if (size < items.length) items[size++] = x; // enforce cap
        }
    }
    public static void main(String[] args) {
        Stack s = new Stack(2);
        s.push(1); s.push(2); s.push(3); // third push ignored
        System.out.println(s.size);  // 2
    }
}
```

Practice: Design a Stack class with a capacity of 2 whose push() ignores new items when full. Push 1, 2, 3, then print how many items it holds (2).

Quick check: Design problems are mostly about preserving what over operations?

## Day 23: Java language foundations

Objective: Cover CS 5004 Java type systems, operators, arrays, strings, constants, and type safety.

Concepts taught:
- Java separates primitive types (int, double, boolean, char, long, float, byte, short) from reference types such as String, arrays, and objects.
- Autoboxing wraps primitives in reference types when generics or collections require objects, but you should still know when values are copied vs. referenced.
- Use final for constants and name variables consistently so intent is visible before a reader studies the expression.
- Operators include arithmetic, relational, logical, bitwise, and ternary forms; each has precedence and type rules.
- Strings are immutable, so repeated modification should use StringBuilder; casts can widen safely or narrow with risk.

Example:
```java
import java.util.*;
public class Main {
    public static void main(String[] args) {
        final int MAX = 3;              // constant
        int count = 2;                  // primitive
        double widened = count;         // widening cast is safe
        StringBuilder sb = new StringBuilder("AI");
        int[] scores = {90, 95, 100};   // array reference
        System.out.println(sb.append("/ML") + " " + widened + " " + scores[MAX - 1]);
    }
}
```

Practice: Write a Java class that declares one primitive, one final constant, one StringBuilder, one array, and one safe widening cast. Print each result.

Quick check: What Java keyword marks a variable as a constant after assignment?

## Day 24: Java control flow

Objective: Use Java branch and loop constructs deliberately, including tracing and early exits.

Concepts taught:
- if/else-if/else chains select one branch; switch and modern switch expressions are clearer for fixed sets of cases.
- for loops are good for counted repetition, enhanced for loops walk collections, while loops repeat until a condition changes, and do-while runs at least once.
- Trace loops with a state table: iteration number, variables before the body, condition result, and variables after the body.
- break exits a loop or switch immediately; continue skips to the next loop iteration.
- Nested loops multiply work, so they matter for both correctness and Big-O analysis.

Example:
```java
int score = 82;
String grade = switch (score / 10) {
    case 10, 9 -> "A";
    case 8 -> "B";
    default -> "review";
};
for (int i = 0; i < 3; i++) {           // trace i: 0, 1, 2
    if (i == 1) continue;               // skip one pass
    System.out.println(grade + " " + i);
}
```

Practice: Write a Java method that takes an int score and returns a letter grade using if/else or switch. Add a loop that prints a state table for scores 0, 25, 50, 75, 100.

Quick check: What loop form always runs its body at least once?

## Day 25: Methods, scope, and contracts

Objective: Design methods with signatures, purpose statements, preconditions, postconditions, scope, and recursion.

Concepts taught:
- A method signature states the method name, parameter types, and return type; void means the method returns no value.
- Overloading lets one class define multiple methods with the same name but different parameter lists.
- Static methods belong to the class, while instance methods act on a specific object.
- Java is pass-by-value: primitive values are copied, and object reference values are copied, so methods can mutate the referred object but not rebind the caller's variable.
- Purpose statements, preconditions, and postconditions make behavior testable before implementation details are known.
- Local variables live only within their scope; recursive calls create new stack frames until a base case stops them.

Example:
```java
/** Returns n!, precondition: n >= 0, postcondition: result >= 1. */
static int factorial(int n) {
    if (n <= 1) return 1;               // base case
    return n * factorial(n - 1);        // recursive case
}
```

Practice: Write a Java method with a purpose comment, precondition, postcondition, parameters, return value, and one recursive helper.

Quick check: What does void mean in a Java method signature?

## Day 26: Classes, objects, and constructors

Objective: Build Java classes with fields, constructors, methods, this, access control, and toString.

Concepts taught:
- A class defines fields, constructors, and methods; an object is an instance allocated with new.
- Constructors establish valid initial state and can be overloaded or chained with this(...) to avoid duplication.
- this names the current object, which is useful when parameter names match field names.
- Access modifiers control visibility: private for implementation details, public for the supported API, and protected/package-private for narrower sharing.
- Getters and setters expose state safely when direct field access would break an invariant.
- toString gives objects a useful text representation for debugging and tests.

Example:
```java
class BankAccount {
    private int balance;
    BankAccount() { this(0); }
    BankAccount(int balance) { this.balance = balance; }
    void deposit(int amount) { balance += amount; }
    public String toString() { return "balance=" + balance; }
}
```

Practice: Create a BankAccount class with private balance, overloaded constructors, deposit, withdraw, and toString. Use this where field and parameter names match.

Quick check: What keyword refers to the current Java object?

## Day 27: Enums and exceptions

Objective: Represent fixed domains with enums and handle failure with Java exceptions.

Concepts taught:
- An enum represents a fixed set of named values and can also define fields, constructors, and methods.
- Exceptions model failures without mixing error paths into normal return values.
- Checked exceptions must be declared or caught; unchecked exceptions usually represent programming errors or invalid runtime conditions.
- try/catch/finally separates risky code, recovery logic, and cleanup.
- Use throw to raise a specific failure and throws in a method signature to declare checked failures.

Example:
```java
enum Status { NEW, PAID, SHIPPED }
static Status ship(Status s) {
    if (s != Status.PAID) throw new IllegalStateException("pay first");
    return Status.SHIPPED;
}
```

Practice: Create an enum OrderStatus and a method that throws IllegalArgumentException for invalid transitions. Catch it in main and print a useful message.

Quick check: Are checked exceptions required to be caught or declared?

## Day 28: Encapsulation and invariants

Objective: Protect object state with information hiding, invariants, cohesion, and immutable design.

Concepts taught:
- Encapsulation keeps representation private so callers cannot put an object into an invalid state.
- A class invariant is a rule that must be true after construction and after every public method call.
- Information hiding lets you change fields or helper methods without breaking users of the class.
- High cohesion means a class has one clear responsibility; loose coupling means classes depend on narrow contracts.
- Immutable objects enforce invariants by setting all state at construction time and exposing no mutators.

Example:
```java
final class Range {
    private final int start, end;        // invariant: start <= end
    Range(int start, int end) {
        if (end < start) throw new IllegalArgumentException();
        this.start = start; this.end = end;
    }
    boolean contains(int x) { return start <= x && x <= end; }
}
```

Practice: Design an immutable Range class whose constructor rejects end < start and whose methods never expose mutable internal state.

Quick check: What is a rule that must remain true for an object called?

## Day 29: Inheritance and polymorphism

Objective: Use subclassing, overriding, super, dynamic dispatch, and composition tradeoffs.

Concepts taught:
- extends creates an is-a relationship where a subclass inherits fields and methods from a superclass.
- Overriding replaces superclass behavior for a method with the same signature; overloading creates a different signature.
- super calls superclass constructors or methods when the subclass needs shared setup or behavior.
- Dynamic dispatch chooses the runtime object's method implementation, even when the variable type is the superclass.
- Every class ultimately inherits from Object, and instanceof plus casting control safe upcasting and downcasting.
- Prefer composition when the relationship is has-a or when inheritance would expose too much implementation detail.

Example:
```java
abstract class Shape { abstract double area(); }
class Circle extends Shape {
    double r; Circle(double r) { this.r = r; }
    @Override double area() { return Math.PI * r * r; }
}
Shape s = new Circle(2);                // upcast
System.out.println(s.area());           // dynamic dispatch
```

Practice: Create Shape, Circle, and Rectangle classes. Override area(), store them in a Shape[] array, and show dynamic dispatch in a loop.

Quick check: What chooses the overridden method based on the runtime object?

## Day 30: Abstract classes and interfaces

Objective: Model contracts with interfaces, abstract classes, Comparable, Comparator, and interface-based design.

Concepts taught:
- Abstract classes can hold shared state and partial implementation while leaving abstract methods for subclasses.
- Interfaces define behavior contracts and let unrelated classes be used through the same API.
- A class can implement multiple interfaces, which is often cleaner than deep inheritance.
- Default interface methods provide shared behavior without forcing every implementation to duplicate it.
- Comparable defines natural ordering; Comparator defines external/custom ordering.

Example:
```java
interface Payable { int pay(); }
abstract class Employee implements Payable { String name; }
class Hourly extends Employee {
    int hours, rate;
    public int pay() { return hours * rate; }
}
```

Practice: Define a Payable interface and an abstract Employee class. Implement two employee types and sort them with a Comparator.

Quick check: What Java construct defines a behavior contract implemented by classes?

## Day 31: Equality, comparison, and hashing

Objective: Implement equals, hashCode, Comparable, and Comparator without breaking Java contracts.

Concepts taught:
- == compares primitive values or object references; equals should compare meaningful object state.
- equals must be reflexive, symmetric, transitive, consistent, and false for null.
- If two objects are equal, hashCode must return the same value or hash-based collections break.
- Comparable.compareTo should agree with equals when natural ordering and equality represent the same concept.
- Comparator is safer when you need multiple sort orders for the same type.

Example:
```java
class Student {
    final int id;
    Student(int id) { this.id = id; }
    public boolean equals(Object o) {
        return o instanceof Student s && id == s.id;
    }
    public int hashCode() { return Integer.hashCode(id); }
}
```

Practice: Create a Student class and override equals and hashCode based on id. Add two equal students to a HashSet and show only one remains.

Quick check: If equals says two objects are equal, what method must agree?

## Day 32: Generics and higher-order functions

Objective: Use type parameters, bounded generics, lambdas, functional interfaces, and streams.

Concepts taught:
- Generics let classes and methods work with a type parameter instead of Object casts.
- Bounds such as <T extends Comparable<T>> let generic code rely on required behavior.
- Wildcards express variance: ? extends T for producers, ? super T for consumers.
- Functional interfaces represent one-method contracts that lambdas and method references can implement.
- Streams create pipelines such as filter, map, and reduce, but they should still be readable and testable.

Example:
```java
static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}
int total = java.util.List.of(1, 2, 3).stream()
    .filter(n -> n % 2 == 1).map(n -> n * n).reduce(0, Integer::sum);
```

Practice: Write a generic max method for Comparable values, then use a stream pipeline to filter, map, and reduce a list of numbers.

Quick check: What Java feature lets a class use a type parameter like T?

## Day 33: Recursive lists and ADTs

Objective: Implement recursive linked structures and separate list interfaces from concrete implementations.

Concepts taught:
- Recursive data definitions describe a value in terms of a base case and a smaller value of the same shape.
- A linked list node stores data plus a reference to the next node; recursive traversal follows next until null.
- Insertion and deletion require careful pointer rewiring so no nodes are skipped or leaked conceptually.
- An ADT interface should say what operations mean without exposing node internals.
- ArrayList provides fast index access; LinkedList provides cheap local insert/remove but slower search.

Example:
```java
interface IntList { int size(); }
class Node implements IntList {
    int value; IntList rest;
    Node(int value, IntList rest) { this.value = value; this.rest = rest; }
    public int size() { return 1 + rest.size(); }
}
class Empty implements IntList { public int size() { return 0; } }
```

Practice: Define a ListNode class and a ListADT interface. Implement recursive size() and iterative append() for a singly linked list.

Quick check: What value usually marks the end of a linked list in Java?

## Day 34: ADTs and Java collections

Objective: Choose and use stacks, queues, trees, maps, lists, sets, iterators, and collection utilities.

Concepts taught:
- ADTs define operations and behavior, while implementations choose arrays, links, trees, hashes, or heaps.
- Stacks are LIFO, queues are FIFO, trees model hierarchy/order, and maps store key-value associations.
- Java Collections separates interfaces (List, Set, Queue, Map) from implementations (ArrayList, HashMap, TreeSet, etc.).
- Iterators provide uniform traversal and let containers hide their internal storage.
- Collections utilities and streams are useful when they make intent clearer than manual loops.

Example:
```java
Deque<Integer> stack = new ArrayDeque<>();
Queue<Integer> queue = new ArrayDeque<>();
Map<String, Integer> counts = new HashMap<>();
stack.push(1); queue.add(1);
counts.put("ai", counts.getOrDefault("ai", 0) + 1);
```

Practice: Solve one small task three ways: Stack/Deque for reverse order, Queue for FIFO order, and Map for counting keys.

Quick check: Which Java collection interface stores key-value pairs?

## Day 35: Design patterns

Objective: Recognize and implement common creational, structural, and behavioral Java design patterns.

Concepts taught:
- A design pattern is a reusable solution shape for a recurring design problem, not code to copy blindly.
- Factory and Builder help construct objects while hiding complicated creation logic.
- Decorator and Adapter wrap objects to add behavior or translate interfaces.
- Strategy, Observer, Iterator, Visitor, and Command separate behavior that changes from objects that use it.
- These patterns appear when construction, variation, traversal, or event flow should stay independent from concrete classes.
- The right pattern should reduce coupling or duplication; the wrong pattern adds ceremony.

Example:
```java
interface DiscountStrategy { int apply(int cents); }
class NoDiscount implements DiscountStrategy {
    public int apply(int cents) { return cents; }
}
class HalfOff implements DiscountStrategy {
    public int apply(int cents) { return cents / 2; }
}
```

Practice: Implement Strategy for two discount rules, then briefly identify where Factory or Decorator would fit in the same program.

Quick check: Which pattern swaps interchangeable algorithms behind one interface?

## Day 36: Model-View-Controller

Objective: Separate model state, view rendering, and controller input using clear interfaces.

Concepts taught:
- MVC separates domain state (Model), presentation (View), and input/application flow (Controller).
- The model should expose clear operations and avoid depending on console, GUI, or web details.
- A controller translates user input into model calls and chooses what the view should render next.
- A view displays state but should not own business rules.
- Refactor toward MVC by extracting one responsibility at a time from a monolithic program.

Example:
```java
class CounterModel { private int n; void inc() { n++; } int value() { return n; } }
class CounterView { String render(int n) { return "Count: " + n; } }
class CounterController {
    CounterModel model; CounterView view;
    String click() { model.inc(); return view.render(model.value()); }
}
```

Practice: Split a tiny counter app into CounterModel, CounterView, and CounterController classes with no printing inside the model.

Quick check: In MVC, which part owns domain state and rules?

## Day 37: Testing, debugging, and docs

Objective: Write JUnit tests, debug with breakpoints, document with Javadoc, and manage builds with Gradle.

Concepts taught:
- JUnit tests encode expected behavior with @Test methods, assertions, and setup/teardown when needed.
- Boundary cases and equivalence partitions catch more bugs than only testing happy paths.
- Black-box tests focus on public behavior; white-box tests use knowledge of implementation paths.
- Breakpoints, stepping, and watch variables let you inspect runtime state instead of guessing.
- Javadoc and Gradle make a project easier to understand, build, test, and share.

Example:
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
class BankAccountTest {
    @Test void depositIncreasesBalance() {
        BankAccount account = new BankAccount(10);
        account.deposit(5);
        assertEquals("balance=15", account.toString());
    }
}
```

Practice: Write a JUnit-style test plan for BankAccount: normal deposit, overdraft boundary, negative input, and toString output. Include one Javadoc comment.

Quick check: What Java testing framework commonly uses @Test?

## Day 38: Algorithm analysis in Java

Objective: Estimate time and space complexity for loops, recursive methods, ADTs, and divide-and-conquer code.

Concepts taught:
- Big-O describes how work grows as input size grows, ignoring constant factors.
- Common classes include O(1), O(log n), O(n), O(n log n), O(n^2), and O(2^n).
- Nested loops, recursive branching, and ADT choices usually dominate complexity.
- Space complexity counts extra memory such as arrays, recursion stack frames, and maps.
- Divide-and-conquer splits a problem, solves subproblems, and combines results.

Example:
```java
// O(log n) time, O(1) extra space.
static boolean binarySearch(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (a[mid] == target) return true;
        if (a[mid] < target) lo = mid + 1; else hi = mid - 1;
    }
    return false;
}
```

Practice: For three Java snippets you write (single loop, nested loop, binary search), add comments with time and space complexity.

Quick check: What complexity class describes binary search?

## Day 39: UML and diagramming

Objective: Read and draw class diagrams with fields, methods, visibility, inheritance, composition, and dependencies.

Concepts taught:
- A UML class diagram summarizes classes, fields, methods, and visibility without showing full code.
- Inheritance, realization, composition, aggregation, and dependency arrows represent different relationships.
- Interfaces can be shown separately so the diagram emphasizes contracts instead of implementations.
- Composition means the whole strongly owns the parts; aggregation means a looser has-a relationship.
- A useful diagram explains collaboration boundaries for a medium-sized program.

Example:
```java
// UML text sketch:
// Library *-- Book
// Member --> Loan
// LoanRepository ..> Loan
// + public, - private, # protected
```

Practice: Write a text UML sketch for a Library system with Book, Member, Loan, and LoanRepository. Include visibility and relationships.

Quick check: In UML, what relationship represents a strong whole-part ownership?

## Day 40: Packages, modules, and organization

Objective: Organize Java projects with packages, imports, JAR/classpath basics, and dependency boundaries.

Concepts taught:
- Packages group related classes and prevent name collisions across a project.
- Import statements depend on package names, so directory layout and package declarations should match.
- A coherent package exposes clear public interfaces and keeps implementation classes internal where possible.
- JAR files bundle compiled classes and metadata; classpaths tell Java where dependencies live.
- Build tools such as Gradle standardize source layout, dependencies, tests, and repeatable tasks.

Example:
```java
// src/main/java/program/model/CounterModel.java
package program.model;
import java.util.Objects;
// Gradle dependency example:
// testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
```

Practice: Sketch a Java project layout with packages model, view, controller, and test. Include one import and one Gradle dependency line.

Quick check: What Java declaration groups a class into a namespace?
