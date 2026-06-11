#!/usr/bin/env python3
"""
Programming Fundamentals and AI - By Ryu Hemingway.

Run `Learn` to start the interactive tutor, or:
  Learn leetcode stats
  Learn leetcode next
  Learn --track ai_principles --module rag
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import warnings
from datetime import datetime, timedelta
from pathlib import Path

warnings.filterwarnings(
    "ignore",
    message="urllib3 v2 only supports OpenSSL 1.1.1+",
    category=Warning,
)

try:
    import requests
except ImportError:
    print("Run:  pip install requests")
    sys.exit(1)


# ── Config & data loading ─────────────────────────────────────────────────

BASE = Path(__file__).resolve().parent
CONFIG_PATH = Path(os.environ.get("LEARN_CONFIG_PATH", BASE / "config.json")).expanduser()
PROFILE_PATH = BASE / "profile.md"
DEADLINES_PATH = BASE / "deadlines.json"
SKILLS_PATH = BASE / "skills.json"
OUTPUT_DIR = BASE / "output"
DATA_DIR = BASE / "data"
PROGRESS_DIR = Path(os.environ.get("LEARN_PROGRESS_DIR", DATA_DIR)).expanduser()
LEETCODE_CATALOG_PATH = DATA_DIR / "leetcode_catalog.json"
LEETCODE_PROGRESS_PATH = PROGRESS_DIR / "leetcode_progress.json"
LEARNING_PROGRESS_PATH = PROGRESS_DIR / "learning_progress.json"


ANSI_ENABLED = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


class ANSI:
    reset = "\033[0m" if ANSI_ENABLED else ""
    bold = "\033[1m" if ANSI_ENABLED else ""
    dim = "\033[2m" if ANSI_ENABLED else ""
    cyan = "\033[96m" if ANSI_ENABLED else ""
    green = "\033[92m" if ANSI_ENABLED else ""
    amber = "\033[33m" if ANSI_ENABLED else ""
    red = "\033[31m" if ANSI_ENABLED else ""
    magenta = "\033[35m" if ANSI_ENABLED else ""


# Color palettes. "dark" uses the bright defaults; "light" swaps to darker
# foregrounds that stay legible on a light background and drops dim (which is
# nearly invisible on white) to a readable gray.
THEMES = {
    "dark": {"cyan": "\033[96m", "green": "\033[92m", "amber": "\033[33m",
             "red": "\033[31m", "magenta": "\033[35m", "dim": "\033[2m"},
    "light": {"cyan": "\033[96m", "green": "\033[92m", "amber": "\033[38;5;130m",
              "red": "\033[31m", "magenta": "\033[35m", "dim": "\033[38;5;240m"},
}

CURRENT_THEME = "dark"


def apply_theme(theme: str) -> None:
    """Switch the active ANSI palette. No-op for colors when output is not a TTY."""
    global CURRENT_THEME
    if theme not in THEMES:
        theme = "dark"
    CURRENT_THEME = theme
    if not ANSI_ENABLED:
        return
    for name, code in THEMES[theme].items():
        setattr(ANSI, name, code)


def _term_width() -> int:
    return max(72, min(110, shutil.get_terminal_size((96, 24)).columns))


def _strip_ansi(text: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", text)


def _display_len(text: str) -> int:
    return len(_strip_ansi(text))


def _center_text(text: str, width: int | None = None) -> str:
    # Box/wrap widths stay capped (_term_width), but centering pads against the
    # live terminal width so panels stay centered when the window is widened.
    cols = width if width is not None else shutil.get_terminal_size((96, 24)).columns
    visible = _display_len(text)
    if visible >= cols:
        return text
    return " " * ((cols - visible) // 2) + text


def ui_line(text: str = "", color: str = "", bold: bool = False) -> None:
    prefix = (ANSI.bold if bold else "") + color
    print(_center_text(f"{prefix}{text}{ANSI.reset}" if prefix else text))


def ui_blank() -> None:
    print()


def ui_rule(char: str = "─", color: str = ANSI.dim) -> None:
    ui_line(char * min(84, _term_width() - 8), color=color)


def _box_content_left() -> int:
    """Column where text inside an ANSI box begins (centered box + '│ ' border).

    Used to align the multi-line code editor with the boxes above it.
    """
    width = min(84, _term_width() - 8)
    cols = shutil.get_terminal_size((96, 24)).columns
    return max(0, (cols - width) // 2 + 2)


def ui_box(lines: list[str], title: str = "", color: str = ANSI.cyan) -> None:
    width = min(84, _term_width() - 8)
    inner = width - 4
    if title:
        title_text = f" {title} "
        left = max(0, (inner - _display_len(title_text)) // 2)
        right = max(0, inner - left - _display_len(title_text))
        ui_line(f"╭{'─' * left}{title_text}{'─' * right}╮", color=color)
    else:
        ui_line(f"╭{'─' * inner}╮", color=color)
    rendered = []
    for line in lines:
        raw = _strip_ansi(line)
        if not raw:
            rendered.append("")
            continue
        if raw.startswith(("    ", "#", "}", "{")):
            rendered.append(raw[:inner - 1] + "…" if len(raw) > inner else raw)
            continue
        rendered.extend(textwrap.wrap(raw, width=inner) or [""])
    for raw in rendered:
        pad = inner - len(raw)
        ui_line(f"│ {raw}{' ' * pad} │", color=color)
    ui_line(f"╰{'─' * inner}╯", color=color)


def ui_menu(title: str, options: list[str]) -> None:
    ui_box([f"[{i}] {option}" for i, option in enumerate(options, 1)], title=title, color=ANSI.cyan)


def _boxed_input_geometry() -> tuple[int, int]:
    width = min(84, _term_width() - 8)
    left = max(0, (shutil.get_terminal_size((96, 24)).columns - width) // 2)
    return width, left


def _read_boxed_line(title: str = "Input", submit_on_ctrl_p: bool = False, toolbar: str = "") -> str:
    """Read one line inside a centered box. Ctrl-D/EOF exits cleanly."""
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        width, left = _boxed_input_geometry()
        inner = width - 4
        ui_line(f"╭{'─' * inner}╮", color=ANSI.green)
        try:
            value = input(f"{' ' * left}{ANSI.green}│ > {ANSI.reset}")
        except EOFError:
            print()
            raise SystemExit(0)
        print()
        ui_line(f"╰{'─' * inner}╯", color=ANSI.green)
        return value

    try:
        from prompt_toolkit.application import Application
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.layout import Layout
        from prompt_toolkit.layout.containers import HSplit, VSplit, Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.dimension import Dimension
        from prompt_toolkit.widgets import Frame, TextArea
    except ImportError:
        width, left = _boxed_input_geometry()
        inner = width - 4
        ui_line(f"╭{'─' * inner}╮", color=ANSI.green)
        try:
            value = input(f"{' ' * left}{ANSI.green}│ > {ANSI.reset}")
        except EOFError:
            print()
            raise SystemExit(0)
        print()
        ui_line(f"╰{'─' * inner}╯", color=ANSI.green)
        return value

    width, left = _boxed_input_geometry()
    text_area = TextArea(
        multiline=False,
        wrap_lines=False,
        prompt="> ",
        width=Dimension.exact(width - 4),
        height=1,
    )
    result: dict[str, str] = {"text": ""}
    bindings = KeyBindings()

    @bindings.add("enter")
    def _(event):
        result["text"] = text_area.text
        event.app.exit()

    @bindings.add("c-p")
    def _(event):
        if submit_on_ctrl_p:
            result["text"] = ":commands"
            event.app.exit()

    @bindings.add("c-c")
    def _(event):
        result["text"] = "quit"
        event.app.exit()

    body_rows = [Frame(text_area, title=title)]
    if toolbar:
        body_rows.append(Window(FormattedTextControl(toolbar), height=1, width=Dimension.exact(width)))
    body = VSplit([
        Window(width=Dimension.exact(left)),
        HSplit(body_rows),
    ])
    app: Application = Application(
        layout=Layout(body, focused_element=text_area),
        key_bindings=bindings,
        mouse_support=True,
        full_screen=False,
    )
    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        print()
        raise SystemExit(0)
    return result["text"]


def _read_line(label: str = "> ") -> str:
    """Read one boxed line of input. The label is kept for call-site compatibility."""
    title = "Input" if label.strip() in ("", ">") else label.strip().rstrip(":")
    return _read_boxed_line(title=title or "Input")


def ui_prompt() -> str:
    return _read_line().strip().lower()


def _read_command_line() -> str:
    """Read the home command line. Ctrl-P returns the command-palette sentinel."""
    return _read_boxed_line(
        title="Command",
        submit_on_ctrl_p=True,
        toolbar=" Enter: today's lesson | Ctrl+P: commands | type a tutor question ",
    ).strip()


def _command_palette(title: str, options: list[tuple[str, str, tuple[str, ...]]]) -> str:
    ui_menu(title, [label for _key, label, _aliases in options])
    raw = ui_prompt()
    if not raw:
        return ""
    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(options):
            return options[idx][0]
    for key, _label, aliases in options:
        if raw == key or raw in aliases:
            return key
    ui_line("Command not found.", color=ANSI.amber)
    return ""


def print_learn_banner() -> None:
    ui_blank()
    art = [
        " █████╗ ██╗    ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗███████╗██████╗ ██╗███╗   ██╗ ██████╗ ",
        "██╔══██╗██║    ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║████╗  ██║██╔════╝ ",
        "███████║██║    █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  █████╗  ██████╔╝██║██╔██╗ ██║██║  ███╗",
        "██╔══██║██║    ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  ██╔══╝  ██╔══██╗██║██║╚██╗██║██║   ██║",
        "██║  ██║██║    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗███████╗██║  ██║██║██║ ╚████║╚██████╔╝",
        "╚═╝  ╚═╝╚═╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ",
    ]
    for line in art:
        ui_line(line, color=ANSI.cyan, bold=True)
    ui_blank()
    ui_line("Programming, ML, RAG, evals, and agentic systems - By Ryu Hemingway", color=ANSI.green, bold=True)
    ui_line("Learn programming foundations and applied AI engineering from one terminal.", color=ANSI.dim)
    ui_rule()


LEARN_LANGUAGES = {
    "python": "Python",
    "c": "C",
    "java": "Java",
}


LEARN_AI_PROVIDERS = {
    "offline": "Offline only",
    "local": "Local AI (LM Studio)",
    "claude": "Claude",
    "openai": "OpenAI",
    "deepseek": "DeepSeek",
}


AI_PROVIDER_MODEL_KEYS = {
    "local": "local_model",
    "claude": "anthropic_model",
    "openai": "openai_model",
    "deepseek": "deepseek_model",
}


DEEPSEEK_MODELS = {
    "deepseek-v4-flash": "DeepSeek V4 Flash",
    "deepseek-v4-pro": "DeepSeek V4 Pro",
}


DEEPSEEK_LEGACY_MODEL_ALIASES = {
    "deepseek-chat": "deepseek-v4-flash",
    "deepseek-reasoner": "deepseek-v4-flash",
}


KNOWN_PROVIDER_MODELS = {
    "claude": {
        "claude-sonnet-4-20250514": "Claude Sonnet 4",
    },
    "openai": {
        "gpt-4.1-mini": "GPT-4.1 mini",
    },
}


LEARN_TRACKS = {
    "programming": "Programming languages",
    "ai_principles": "Principles of AI",
}


AI_MODULES = {
    "llm_fundamentals": "LLM fundamentals",
    "prompting": "Prompt engineering",
    "embeddings": "Embeddings and vector search",
    "rag": "Retrieval-augmented generation",
    "harnesses": "Evaluation harnesses",
    "agents": "Agentic coding and AI agents",
    "locallm": "Local LLMs",
    "ml_basics": "Machine learning fundamentals",
    "data_engineering": "AI data engineering",
    "transformers": "Neural nets, transformers, and LLMs",
    "mlops": "AI deployment and MLOps",
    "safety": "AI safety, governance, and reliability",
}


LESSON_TOPICS = [
    ("variables", "Variables and output", "Store values, name them clearly, and print results."),
    ("types", "Types and conversions", "Recognize numbers, text, booleans, and basic casts."),
    ("bitwise", "Bitwise operations", "Manipulate individual bits with AND, OR, XOR, NOT, and shifts."),
    ("input", "Input and simple programs", "Read user input and turn it into useful values."),
    ("conditionals", "Conditionals", "Use if/else logic to make decisions."),
    ("loops", "Loops", "Repeat work with for/while loops and trace loop state."),
    ("functions", "Functions and methods", "Package logic into reusable units with parameters and returns."),
    ("pseudocode", "Reading and translating pseudo-code", "Read algorithmic pseudo-code and translate it faithfully to code."),
    ("arrays", "Arrays and lists", "Store many values and iterate through them safely."),
    ("strings", "Strings", "Process text by indexing, slicing, comparing, and counting."),
    ("hash_maps", "Hash maps and dictionaries", "Use key-value lookup to reduce repeated scans."),
    ("stack", "Stacks", "Model last-in-first-out workflows and parentheses problems."),
    ("two_pointers", "Two pointers", "Solve sorted-array and in-place problems with two indexes."),
    ("sliding_window", "Sliding window", "Track a moving range for substring and subarray problems."),
    ("binary_search", "Binary search", "Cut a sorted or monotonic search space in half."),
    ("classes", "Classes and objects", "Group data and behavior into reusable types."),
    ("linked_lists", "Linked lists", "Reason about nodes, next pointers, and pointer rewiring."),
    ("recursion", "Recursion", "Solve a problem by reducing it to smaller versions."),
    ("trees", "Trees", "Traverse tree-shaped data with DFS and BFS."),
    ("graphs", "Graphs", "Represent connections and traverse with BFS/DFS."),
    ("dynamic_programming", "Dynamic programming", "Define state, recurrence, base cases, and order."),
    ("heap", "Heaps and priority queues", "Repeatedly access the smallest or largest item efficiently."),
    ("matrix", "Matrices", "Traverse rows, columns, and neighbors without index bugs."),
    ("design", "Design problems", "Build small APIs that preserve invariants over operations."),
]


# Short, book-style teaching notes for each topic. These are the actual lesson
# content (language-agnostic): enough to understand the idea and attempt the
# practice. The language example below shows the matching syntax.
LESSON_EXPLANATIONS = {
    "variables": [
        "A variable is a named box in memory that holds a value you can read and change later.",
        "You assign with '=': the name goes on the left, the value on the right.",
        "Pick clear names (score, user_name) so the code explains itself.",
        "Printing a variable shows its current value, which is how you check your work.",
    ],
    "types": [
        "Every value has a type: integers (3), decimals/floats (3.14), text/strings (\"hi\"), and booleans (true/false).",
        "The type decides what operations are legal: adding numbers differs from joining text.",
        "Converting (casting) turns one type into another, e.g. the text \"42\" into the number 42.",
        "Mixing types carelessly is a common bug, so always know what type a value is.",
    ],
    "bitwise": [
        "Bitwise operators work on the binary representation of integers, one bit position at a time.",
        "The core operators are AND (&), OR (|), XOR (^), NOT/complement (~), left shift (<<), and right shift (>>).",
        "AND keeps a bit only when both inputs have 1 there; OR keeps it when either input has 1; XOR keeps it when the bits differ.",
        "A mask is an integer with 1s in the positions you want to inspect or change.",
        "Use flags by assigning each option a power-of-two value, combining options with |, testing with &, toggling with ^, and clearing with & plus a complemented mask.",
        "Left shift by k moves bits left and is equivalent to multiplying unsigned values by 2^k when no overflow occurs.",
        "Right shift by k moves bits right; unsigned shifts behave like division by 2^k, while signed behavior depends on the language.",
        "Parenthesize bit tests such as (flags & READ) != 0 because comparison and bitwise precedence rules are easy to misread.",
    ],
    "input": [
        "Programs get useful when they react to data the user types in.",
        "Input almost always arrives as text, even when the user types digits.",
        "Before doing math on it, convert that text into a number (int or float).",
        "Guard against unexpected input so the program does not crash.",
    ],
    "conditionals": [
        "Conditionals let a program choose between paths based on a true/false test.",
        "'if' runs a block only when its condition is true; 'else' covers the other case; else-if chains more checks.",
        "Comparison operators (==, !=, <, >, <=, >=) produce the booleans you test.",
        "Combine conditions with and / or / not to express richer rules.",
    ],
    "loops": [
        "A loop repeats a block of code so you do not copy-paste the same lines.",
        "Use a 'for' loop when you know how many times or are walking a collection; use 'while' to repeat until a condition turns false.",
        "The loop variable changes each pass; tracing it by hand reveals how the loop behaves.",
        "Make sure the loop can end, or it runs forever (an infinite loop).",
    ],
    "functions": [
        "A function packages a piece of logic under a name so you can reuse it.",
        "Parameters are the inputs you pass in; the return value is the result you get back.",
        "Calling a function runs its body with the arguments you supply.",
        "Functions keep code short, testable, and free of duplication.",
    ],
    "pseudocode": [
        "Pseudo-code describes an algorithm without committing to one programming language's syntax.",
        "Common notation includes arrows for assignment, 'for i = 1 to n' loops, 'while condition do', 'if/then/else', and mathematical symbols such as infinity.",
        "Translate structure first: function signature, base cases, loops, conditionals, and return points.",
        "Then translate data access carefully; pseudo-code is often 1-indexed and inclusive, while C, Java, and Python arrays are 0-indexed.",
        "Preserve the invariant the pseudo-code relies on, such as 'left half is already sorted' during merge sort.",
        "Verify the translation by tracing both versions on the same tiny input and comparing intermediate state, not just the final answer.",
        "The most common translation bugs are off-by-one loop bounds, missing recursive base cases, and copying mathematical notation without adapting it to real code.",
    ],
    "arrays": [
        "An array (or list) stores many values in a single ordered container.",
        "Each item has an index; most languages start at 0, so the first item is index 0.",
        "You loop over the items to process them one by one.",
        "Reading past the last valid index is a classic out-of-bounds error.",
    ],
    "strings": [
        "A string is an ordered sequence of characters (letters, digits, symbols).",
        "You can index single characters, slice ranges, measure length, and compare strings.",
        "Strings are often immutable, so 'changing' one usually builds a new string.",
        "Many problems (palindromes, counting) are just careful string traversal.",
    ],
    "hash_maps": [
        "A hash map (dictionary) stores key -> value pairs for fast lookup by key.",
        "Looking up, inserting, and updating by key are about constant time (O(1)) on average.",
        "They shine when you would otherwise scan a list repeatedly, e.g. counting occurrences.",
        "Keys are unique; assigning an existing key overwrites its value.",
    ],
    "stack": [
        "A stack is a last-in, first-out (LIFO) collection: the most recent item comes off first.",
        "The two core operations are push (add to the top) and pop (remove from the top).",
        "Think of a stack of plates: you take the top one.",
        "Stacks model undo history, function calls, and matching brackets/parentheses.",
    ],
    "two_pointers": [
        "The two-pointer technique uses two indexes moving through data to avoid nested loops.",
        "Common setups: one pointer at each end moving inward, or a slow/fast pair moving the same way.",
        "It works best on sorted arrays or when pairing/comparing elements.",
        "It often turns an O(n^2) scan into a single O(n) pass.",
    ],
    "sliding_window": [
        "A sliding window tracks a contiguous range (subarray/substring) that grows and shrinks as you scan.",
        "Expand the window by moving the right edge; shrink it by moving the left edge.",
        "Keep a running total or count so you do not recompute the whole window each step.",
        "Great for 'longest/shortest/best run that satisfies X' problems.",
    ],
    "binary_search": [
        "Binary search finds a target by repeatedly halving a sorted search space.",
        "Check the middle: if it matches you are done; otherwise discard the half that cannot contain it.",
        "It needs sorted data, or any condition that is monotonic (false then true).",
        "It runs in O(log n), far faster than scanning every element.",
    ],
    "classes": [
        "A class is a blueprint that bundles related data (fields) with behavior (methods).",
        "An object is one instance made from that class, with its own copy of the data.",
        "Methods act on the object's own data (this / self).",
        "Classes help model real things and keep related code together.",
    ],
    "linked_lists": [
        "A linked list is a chain of nodes; each node holds a value and a reference to the next node.",
        "Unlike an array there is no direct index, so you reach an item by following next pointers.",
        "Inserting or removing is cheap once you are at the spot (just rewire pointers); finding the spot is O(n).",
        "The list ends when a node's next is null/None.",
    ],
    "recursion": [
        "Recursion solves a problem by having a function call itself on a smaller version of the problem.",
        "Every recursion needs a base case that stops it, or it never ends (stack overflow).",
        "Each call must move closer to the base case.",
        "Many tree and divide-and-conquer problems are naturally recursive.",
    ],
    "trees": [
        "A tree is a hierarchy of nodes starting from a single root; each node has children.",
        "A binary tree limits each node to at most two children (left and right).",
        "Visit nodes with traversals: depth-first (DFS: pre/in/post-order) or breadth-first (BFS, level by level).",
        "Trees model file systems, decisions, and sorted data (binary search trees).",
    ],
    "graphs": [
        "A graph is a set of nodes (vertices) joined by edges; connections can be one-way or two-way.",
        "Common representations: an adjacency list (each node lists its neighbors) or an adjacency matrix.",
        "Traverse with BFS (level by level, good for shortest unweighted paths) or DFS (go deep first).",
        "Track visited nodes so you do not loop forever on cycles.",
    ],
    "dynamic_programming": [
        "Dynamic programming solves a problem by combining answers to overlapping subproblems.",
        "Define the state (what a subproblem means), the recurrence (how states combine), and the base cases.",
        "Store (memoize) computed answers so each subproblem is solved only once.",
        "It turns exponential brute force into polynomial time when subproblems repeat.",
    ],
    "heap": [
        "A heap always gives quick access to the smallest (min-heap) or largest (max-heap) item.",
        "Push and pop are O(log n); peeking at the top item is O(1).",
        "Use it as a priority queue when you repeatedly need the next most-important item.",
        "It is ideal for top-k, scheduling, and merging sorted streams.",
    ],
    "matrix": [
        "A matrix is a 2D grid of values indexed by row and column (grid[r][c]).",
        "The outer loop usually walks rows; the inner loop walks columns.",
        "Neighbors are the cells up/down/left/right (sometimes diagonals); check bounds before accessing.",
        "Off-by-one errors and swapped row/column indexes are the most common bugs.",
    ],
    "design": [
        "Design problems ask you to build a small component with specific operations (e.g. a cache or queue).",
        "Focus on the invariants: the rules that must stay true after every operation.",
        "Pick data structures that make the required operations efficient.",
        "Think through edge cases: empty state, capacity limits, and repeated keys.",
    ],
}


LANGUAGE_NOTES = {
    "python": {
        "file": "solution.py",
        "compile": "",
        "run": "python3 solution.py",
        "syntax": "Python is concise and dynamic: indentation defines blocks, variables do not need declared types, and lists/dicts are built in.",
        "example_prefix": "Python example",
    },
    "c": {
        "file": "solution.c",
        "compile": "gcc solution.c -o solution",
        "run": "./solution",
        "syntax": "C is explicit and close to memory: declare types, compile before running, and pay attention to arrays, pointers, and ownership.",
        "example_prefix": "C example",
    },
    "java": {
        "file": "Main.java",
        "compile": "javac Main.java",
        "run": "java Main",
        "syntax": "Java is class-based and statically typed: most code lives inside classes, methods declare parameter and return types, and the JVM runs compiled bytecode.",
        "example_prefix": "Java example",
    },
}


# Concrete coding exercises per topic. Each says exactly what to build and the
# expected result, so the learner is never left guessing what is being asked.
PRACTICE_TASKS = {
    "variables": "Create two variables: one holding your name (text) and one holding your age (a number). Print both on one line, e.g. 'Ryu 21'.",
    "types": 'Make a variable holding the text "10", convert it to a number, add 5, and print the result. It should print 15, not 105.',
    "bitwise": "Create READ=4, WRITE=2, and EXEC=1 flags. Combine READ and WRITE, print whether WRITE is enabled, then toggle EXEC and print the final flag value.",
    "input": "Ask the user for their age, convert the typed text to a number, add 1, and print 'Next year you will be ' followed by that number.",
    "conditionals": "Set a number variable. Print 'positive' if it is greater than 0, 'negative' if it is less than 0, and 'zero' otherwise.",
    "loops": "Use a loop to print the numbers 1 through 10, each on its own line.",
    "functions": "Write a function called square that takes one number and returns it multiplied by itself. Call square(4) and print the result (16).",
    "pseudocode": "Translate this pseudo-code to working code and print the result: total <- 0; for i = 1 to 5 do total <- total + i; return total. It should print 15.",
    "arrays": "Make an array/list of the three numbers 3, 1, 4. Loop through it and print their total (8).",
    "strings": 'Set a variable to the word "hello". Print its length (5), then print just its first character (h).',
    "hash_maps": 'Count how many times each letter appears in the word "apple" using a hash map/dictionary, then print the counts.',
    "stack": "Push the numbers 1, 2, then 3 onto a stack. Pop them off one at a time and print each — they should come out 3, 2, 1.",
    "two_pointers": "Given the sorted list [1, 2, 3, 4, 6], use one pointer at each end to find a pair that adds up to 7, and print the two values (1 and 6).",
    "sliding_window": "Given [2, 1, 5, 1, 3, 2], use a window of size 3 to find and print the largest sum of any 3 numbers in a row (9).",
    "binary_search": "Given the sorted list [1, 3, 5, 7, 9], use binary search to find the value 7 and print its index (3).",
    "classes": "Define a class called Dog with a name and a method bark() that prints '<name> says woof'. Create a Dog named Rex and call bark().",
    "linked_lists": "Build a linked list of three nodes holding 1, 2, 3. Then walk the list from the start and print each value.",
    "recursion": "Write a recursive function that computes the factorial of a number (n! = n*(n-1)*...*1). Call it with 5 and print the result (120).",
    "trees": "Build a small binary tree: a root holding 1 with children 2 and 3. Write a function that visits and prints every node's value.",
    "graphs": "Store this graph as an adjacency list: node 0 connects to 1 and 2; node 1 connects to 2. Print all the neighbors of node 0.",
    "dynamic_programming": "Compute the 10th Fibonacci number by storing each answer in an array/dictionary as you build up. Print the result (55).",
    "heap": "Put the numbers 5, 1, 8, 3 into a min-heap / priority queue, then remove and print the smallest item (1).",
    "matrix": "Make a 2x3 grid of numbers ([[1,2,3],[4,5,6]]). Loop through it and print each row on its own line.",
    "design": "Design a Stack class with a capacity of 2 whose push() ignores new items when full. Push 1, 2, 3, then print how many items it holds (2).",
}


EXAMPLE_SNIPPETS = {
    "python": {
        "variables": (
            '# A variable is a name that stores a value so you can reuse it.\n'
            'name = "Ryu"        # text wrapped in quotes is a string\n'
            'score = 10          # a whole number is an integer\n'
            'print(name, score)  # print shows values, separated by a space'
        ),
        "conditionals": (
            'age = 20              # the value we want to test\n'
            'if age >= 18:         # if this condition is True, run the block\n'
            '    print("adult")    # indentation marks what belongs to the if\n'
            'else:                 # otherwise fall through to here\n'
            '    print("minor")    # runs only when the condition was False'
        ),
        "loops": (
            '# range(1, 6) gives 1,2,3,4,5 -- the stop value 6 is excluded.\n'
            'for n in range(1, 6):  # n takes each value in turn\n'
            '    print(n)           # the body runs once per pass'
        ),
        "functions": (
            'def add(a, b):       # def names a reusable function with inputs\n'
            '    return a + b     # return hands a value back to the caller\n'
            '\n'
            'print(add(2, 3))     # call the function; this prints 5'
        ),
        "arrays": (
            'nums = [3, 1, 4]   # a list holds many values in order\n'
            'for n in nums:     # the loop visits each item once\n'
            '    print(n)       # prints 3, then 1, then 4'
        ),
        "strings": (
            'word = "level"             # a string is a sequence of characters\n'
            '# word[::-1] reverses the string; equal means it is a palindrome.\n'
            'print(word == word[::-1])  # True when it reads the same backward'
        ),
        "hash_maps": (
            'counts = {}                 # a dict maps keys to values\n'
            'for ch in "banana":         # look at each character\n'
            '    counts[ch] = counts.get(ch, 0) + 1  # add 1, default 0 if new\n'
            'print(counts)               # {\'b\': 1, \'a\': 3, \'n\': 2}'
        ),
        "classes": (
            'class Counter:          # a class is a blueprint for objects\n'
            '    def __init__(self): # __init__ runs when you create one\n'
            '        self.value = 0  # self stores data on the instance\n'
            '    def inc(self):      # a method is a function tied to the object\n'
            '        self.value += 1 # update this instance\'s own value'
        ),
    },
    "c": {
        "variables": (
            '#include <stdio.h>      // brings in printf for output\n'
            'int main(void) {        // every C program starts at main\n'
            '    int score = 10;     // C needs an explicit type (int)\n'
            '    printf("%d\\n", score); // %d prints an int; \\n is a newline\n'
            '    return 0;           // 0 tells the OS it succeeded\n'
            '}'
        ),
        "conditionals": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int age = 20;            // the value to test\n'
            '    if (age >= 18)           // parentheses hold the condition\n'
            '        printf("adult\\n");   // runs when the condition is true\n'
            '    else\n'
            '        printf("minor\\n");   // runs otherwise\n'
            '    return 0;\n'
            '}'
        ),
        "loops": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    // for (start; condition; step) repeats while condition holds\n'
            '    for (int i = 1; i <= 5; i++)  // i counts 1..5\n'
            '        printf("%d\\n", i);       // body runs once per pass\n'
            '    return 0;\n'
            '}'
        ),
        "functions": (
            '#include <stdio.h>\n'
            'int add(int a, int b) {     // declare return and parameter types\n'
            '    return a + b;           // hand the sum back to the caller\n'
            '}\n'
            'int main(void) {\n'
            '    printf("%d\\n", add(2, 3)); // call add and print 5\n'
            '    return 0;\n'
            '}'
        ),
        "arrays": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int nums[] = {3, 1, 4};      // a fixed-size array of ints\n'
            '    for (int i = 0; i < 3; i++)  // index from 0 to length-1\n'
            '        printf("%d\\n", nums[i]); // nums[i] reads element i\n'
            '    return 0;\n'
            '}'
        ),
        "strings": (
            '#include <stdio.h>\n'
            '#include <string.h>          // strlen is declared here\n'
            'int main(void) {\n'
            '    char word[] = "level";   // a C string is a char array\n'
            '    printf("%zu\\n", strlen(word)); // counts chars before the \\0\n'
            '    return 0;\n'
            '}'
        ),
        "hash_maps": 'C has no built-in hash map. Start with arrays/counting tables for small key ranges, then learn structs plus a hash table implementation.',
        "classes": 'C has structs, not classes. Use a struct for data and functions that receive a pointer to that struct.',
    },
    "java": {
        "variables": (
            'public class Main {                       // code lives in a class\n'
            '    public static void main(String[] args) {  // program entry point\n'
            '        int score = 10;                   // a typed variable\n'
            '        System.out.println(score);        // print, then newline\n'
            '    }\n'
            '}'
        ),
        "conditionals": (
            'public class Main {\n'
            '    public static void main(String[] args) {\n'
            '        int age = 20;                    // value to test\n'
            '        if (age >= 18)                   // condition in parentheses\n'
            '            System.out.println("adult"); // runs when true\n'
            '        else\n'
            '            System.out.println("minor"); // runs otherwise\n'
            '    }\n'
            '}'
        ),
        "loops": (
            'public class Main {\n'
            '    public static void main(String[] args) {\n'
            '        // for (start; condition; step) repeats while true\n'
            '        for (int n = 1; n <= 5; n++)     // n counts 1..5\n'
            '            System.out.println(n);       // body runs each pass\n'
            '    }\n'
            '}'
        ),
        "functions": (
            'public class Main {\n'
            '    static int add(int a, int b) {       // typed params + return\n'
            '        return a + b;                    // send the sum back\n'
            '    }\n'
            '    public static void main(String[] args) {\n'
            '        System.out.println(add(2, 3));   // prints 5\n'
            '    }\n'
            '}'
        ),
        "arrays": (
            'public class Main {\n'
            '    public static void main(String[] args) {\n'
            '        int[] nums = {3, 1, 4};          // an array of ints\n'
            '        for (int n : nums)               // for-each visits each item\n'
            '            System.out.println(n);       // prints 3, 1, 4\n'
            '    }\n'
            '}'
        ),
        "strings": (
            'public class Main {\n'
            '    public static void main(String[] args) {\n'
            '        String word = "level";           // String holds text\n'
            '        System.out.println(word.length()); // length() counts chars\n'
            '    }\n'
            '}'
        ),
        "hash_maps": (
            'import java.util.*;          // Map and HashMap live here\n'
            'public class Main {\n'
            '    public static void main(String[] args) {\n'
            '        Map<Character, Integer> counts = new HashMap<>(); // key->count\n'
            '        for (char ch : "banana".toCharArray())   // each character\n'
            '            counts.put(ch, counts.getOrDefault(ch, 0) + 1); // +1, def 0\n'
            '        System.out.println(counts);      // {a=3, b=1, n=2}\n'
            '    }\n'
            '}'
        ),
        "classes": (
            'class Counter {           // a class bundles data and behavior\n'
            '    int value = 0;        // a field stored on each object\n'
            '    void inc() {          // a method that acts on this object\n'
            '        value++;          // increase this object\'s value by 1\n'
            '    }\n'
            '}'
        ),
    },
}


# Additional topic examples (kept here to keep the literal above readable).
EXAMPLE_SNIPPETS["python"].update({
    "types": (
        'n = 42                    # an integer\n'
        'pi = 3.14                 # a float (decimal number)\n'
        'text = "42"               # a string that only looks like a number\n'
        'print(int(text) + n)      # int("42") converts text to 42, so this is 84\n'
        'print(type(pi).__name__)  # float'
    ),
    "input": (
        '# input() always returns text, so convert before doing math.\n'
        'raw = input("Enter a number: ")  # e.g. the user types 10\n'
        'num = int(raw)                   # turn the text "10" into the integer 10\n'
        'print(num * 2)                   # now arithmetic works -> 20'
    ),
    "stack": (
        'stack = []          # a plain list works as a stack\n'
        'stack.append(1)     # push 1 onto the top\n'
        'stack.append(2)     # push 2 onto the top\n'
        'top = stack.pop()   # pop removes and returns the top item (2)\n'
        'print(top, stack)   # 2 [1]'
    ),
    "two_pointers": (
        'nums = [1, 2, 3, 4, 6]          # must be sorted\n'
        'left, right = 0, len(nums) - 1  # one pointer at each end\n'
        'target = 7\n'
        'while left < right:             # move the pointers inward\n'
        '    s = nums[left] + nums[right]\n'
        '    if s == target:\n'
        '        print(left, right); break   # found a pair that sums to 7\n'
        '    elif s < target:\n'
        '        left += 1               # too small: raise the low end\n'
        '    else:\n'
        '        right -= 1              # too big: lower the high end'
    ),
    "sliding_window": (
        'nums = [2, 1, 5, 1, 3, 2]   # largest sum of any 3 in a row?\n'
        'k = 3\n'
        'window = sum(nums[:k])      # sum of the first window\n'
        'best = window\n'
        'for i in range(k, len(nums)):        # slide the window right\n'
        '    window += nums[i] - nums[i - k]  # add the new item, drop the old\n'
        '    best = max(best, window)\n'
        'print(best)                 # 9 (from 5, 1, 3)'
    ),
    "binary_search": (
        'nums = [1, 3, 5, 7, 9]   # binary search needs sorted data\n'
        'target = 7\n'
        'lo, hi = 0, len(nums) - 1\n'
        'while lo <= hi:\n'
        '    mid = (lo + hi) // 2     # look at the middle\n'
        '    if nums[mid] == target:\n'
        '        print(mid); break    # found it (index 3)\n'
        '    elif nums[mid] < target:\n'
        '        lo = mid + 1         # answer is in the right half\n'
        '    else:\n'
        '        hi = mid - 1         # answer is in the left half'
    ),
    "linked_lists": (
        'class Node:                # one link in the chain\n'
        '    def __init__(self, value):\n'
        '        self.value = value\n'
        '        self.next = None   # points to the next node, None at the end\n'
        '\n'
        'a = Node(1)                # build the chain 1 -> 2\n'
        'a.next = Node(2)\n'
        'node = a\n'
        'while node:                # walk it by following .next\n'
        '    print(node.value)\n'
        '    node = node.next'
    ),
    "recursion": (
        'def factorial(n):          # n! = n * (n-1) * ... * 1\n'
        '    if n <= 1:             # base case: stops the recursion\n'
        '        return 1\n'
        '    return n * factorial(n - 1)  # call itself on a smaller n\n'
        '\n'
        'print(factorial(5))        # 120'
    ),
    "trees": (
        'class Node:                # a binary tree node\n'
        '    def __init__(self, value):\n'
        '        self.value = value\n'
        '        self.left = None\n'
        '        self.right = None\n'
        '\n'
        'root = Node(1)             # build a tiny tree\n'
        'root.left = Node(2)\n'
        'root.right = Node(3)\n'
        '\n'
        'def visit(node):           # depth-first pre-order traversal\n'
        '    if not node:           # base case: empty branch\n'
        '        return\n'
        '    print(node.value)\n'
        '    visit(node.left)\n'
        '    visit(node.right)\n'
        '\n'
        'visit(root)                # 1 2 3'
    ),
    "graphs": (
        '# adjacency list: each node maps to its list of neighbors\n'
        'graph = {1: [2, 3], 2: [4], 3: [], 4: []}\n'
        'visited = set()\n'
        'stack = [1]                # depth-first search from node 1\n'
        'while stack:\n'
        '    node = stack.pop()\n'
        '    if node in visited:    # skip nodes already seen\n'
        '        continue\n'
        '    visited.add(node)\n'
        '    print(node)\n'
        '    stack.extend(graph[node])  # queue up the neighbors'
    ),
    "dynamic_programming": (
        '# nth Fibonacci number, reusing answers to subproblems\n'
        'memo = {0: 0, 1: 1}        # base cases\n'
        'def fib(n):\n'
        '    if n not in memo:      # solve each subproblem only once\n'
        '        memo[n] = fib(n - 1) + fib(n - 2)\n'
        '    return memo[n]\n'
        '\n'
        'print(fib(10))             # 55'
    ),
    "heap": (
        'import heapq               # the min-heap helpers live here\n'
        'nums = [5, 1, 8, 3]\n'
        'heapq.heapify(nums)        # rearrange the list into a heap\n'
        'heapq.heappush(nums, 2)    # add a value, keeping heap order\n'
        'print(heapq.heappop(nums)) # 1 -- always the smallest item'
    ),
    "matrix": (
        'grid = [[1, 2, 3],         # a 2D grid: rows of columns\n'
        '        [4, 5, 6]]\n'
        'for r in range(len(grid)):          # walk each row\n'
        '    for c in range(len(grid[0])):   # walk each column\n'
        '        print(grid[r][c], end=" ")  # grid[r][c] reads one cell\n'
        '    print()                # newline after each row'
    ),
    "design": (
        'class Stack:               # design a stack with a size limit\n'
        '    def __init__(self, cap):\n'
        '        self.cap = cap     # invariant: never hold more than cap\n'
        '        self.items = []\n'
        '    def push(self, x):\n'
        '        if len(self.items) < self.cap:  # enforce the invariant\n'
        '            self.items.append(x)\n'
        '    def pop(self):\n'
        '        return self.items.pop() if self.items else None\n'
        '\n'
        's = Stack(2)\n'
        's.push(1); s.push(2); s.push(3)  # third push is ignored (cap 2)\n'
        'print(s.items)             # [1, 2]'
    ),
})

EXAMPLE_SNIPPETS["c"].update({
    "types": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    int n = 42;          // an integer\n'
        '    double pi = 3.14;    // a floating-point number\n'
        "    char letter = 'A';   // a single character\n"
        '    printf("%d %.2f %c\\n", n, pi, letter); // each %.. matches a type\n'
        '    return 0;\n'
        '}'
    ),
    "input": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    int num;                 // where the input will be stored\n'
        '    printf("Enter a number: ");\n'
        '    scanf("%d", &num);       // read an int into num (& = its address)\n'
        '    printf("%d\\n", num * 2); // use the value once it is read\n'
        '    return 0;\n'
        '}'
    ),
    "stack": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    int stack[100];      // an array used as a stack\n'
        '    int top = 0;         // index of the next free slot\n'
        '    stack[top++] = 1;    // push 1\n'
        '    stack[top++] = 2;    // push 2\n'
        '    int x = stack[--top]; // pop the top value (2)\n'
        '    printf("%d\\n", x);\n'
        '    return 0;\n'
        '}'
    ),
    "two_pointers": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    int nums[] = {1, 2, 3, 4, 6};   // sorted\n'
        '    int left = 0, right = 4, target = 7;\n'
        '    while (left < right) {          // move pointers inward\n'
        '        int s = nums[left] + nums[right];\n'
        '        if (s == target) { printf("%d %d\\n", left, right); break; }\n'
        '        else if (s < target) left++;  // too small\n'
        '        else right--;                 // too big\n'
        '    }\n'
        '    return 0;\n'
        '}'
    ),
    "sliding_window": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    int nums[] = {2, 1, 5, 1, 3, 2}, n = 6, k = 3;\n'
        '    int window = 0;\n'
        '    for (int i = 0; i < k; i++) window += nums[i]; // first window\n'
        '    int best = window;\n'
        '    for (int i = k; i < n; i++) {        // slide right\n'
        '        window += nums[i] - nums[i - k]; // add new, drop old\n'
        '        if (window > best) best = window;\n'
        '    }\n'
        '    printf("%d\\n", best);  // 9\n'
        '    return 0;\n'
        '}'
    ),
    "binary_search": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    int nums[] = {1, 3, 5, 7, 9}, lo = 0, hi = 4, target = 7;\n'
        '    while (lo <= hi) {\n'
        '        int mid = (lo + hi) / 2;     // middle index\n'
        '        if (nums[mid] == target) { printf("%d\\n", mid); break; }\n'
        '        else if (nums[mid] < target) lo = mid + 1; // right half\n'
        '        else hi = mid - 1;                          // left half\n'
        '    }\n'
        '    return 0;\n'
        '}'
    ),
    "linked_lists": (
        '#include <stdio.h>\n'
        '#include <stdlib.h>\n'
        'struct Node { int value; struct Node *next; }; // value + next\n'
        'int main(void) {\n'
        '    struct Node *a = malloc(sizeof(struct Node)); // node 1\n'
        '    a->value = 1;\n'
        '    a->next = malloc(sizeof(struct Node));        // node 2\n'
        '    a->next->value = 2;\n'
        '    a->next->next = NULL;                         // end of list\n'
        '    for (struct Node *n = a; n; n = n->next)      // follow next\n'
        '        printf("%d\\n", n->value);\n'
        '    return 0;\n'
        '}'
    ),
    "recursion": (
        '#include <stdio.h>\n'
        'int factorial(int n) {       // n! = n * (n-1) * ... * 1\n'
        '    if (n <= 1) return 1;    // base case stops the recursion\n'
        '    return n * factorial(n - 1); // call itself on a smaller n\n'
        '}\n'
        'int main(void) {\n'
        '    printf("%d\\n", factorial(5)); // 120\n'
        '    return 0;\n'
        '}'
    ),
    "trees": (
        '#include <stdio.h>\n'
        'struct Node { int value; struct Node *left, *right; };\n'
        'void visit(struct Node *n) { // depth-first pre-order\n'
        '    if (!n) return;          // base case: empty branch\n'
        '    printf("%d\\n", n->value);\n'
        '    visit(n->left);\n'
        '    visit(n->right);\n'
        '}\n'
        'int main(void) {\n'
        '    struct Node root = {1, NULL, NULL}; // a single-node tree\n'
        '    visit(&root);            // prints 1\n'
        '    return 0;\n'
        '}'
    ),
    "graphs": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    // adjacency matrix: edge[a][b] == 1 means a connects to b\n'
        '    int edge[3][3] = {{0,1,1},{0,0,1},{0,0,0}};\n'
        '    int from = 0;\n'
        '    for (int to = 0; to < 3; to++)        // node 0 neighbors\n'
        '        if (edge[from][to]) printf("0 -> %d\\n", to);\n'
        '    return 0;\n'
        '}'
    ),
    "dynamic_programming": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    int n = 10, dp[11];      // dp[i] = i-th Fibonacci number\n'
        '    dp[0] = 0; dp[1] = 1;    // base cases\n'
        '    for (int i = 2; i <= n; i++)        // build up from small i\n'
        '        dp[i] = dp[i - 1] + dp[i - 2];  // the recurrence\n'
        '    printf("%d\\n", dp[n]);   // 55\n'
        '    return 0;\n'
        '}'
    ),
    "heap": 'C has no built-in heap. Store items in an array where the children of index i are 2*i+1 and 2*i+2, and sift values up or down to keep the smallest on top, or use a library.',
    "matrix": (
        '#include <stdio.h>\n'
        'int main(void) {\n'
        '    int grid[2][3] = {{1,2,3},{4,5,6}}; // 2 rows, 3 columns\n'
        '    for (int r = 0; r < 2; r++) {        // walk rows\n'
        '        for (int c = 0; c < 3; c++)      // walk columns\n'
        '            printf("%d ", grid[r][c]);   // read one cell\n'
        '        printf("\\n");\n'
        '    }\n'
        '    return 0;\n'
        '}'
    ),
    "design": (
        '#include <stdio.h>\n'
        '#define CAP 2\n'
        'struct Stack { int items[CAP]; int size; }; // invariant: size <= CAP\n'
        'void push(struct Stack *s, int x) {\n'
        '    if (s->size < CAP) s->items[s->size++] = x; // enforce the cap\n'
        '}\n'
        'int main(void) {\n'
        '    struct Stack s = {{0}, 0};\n'
        '    push(&s, 1); push(&s, 2); push(&s, 3); // third push ignored\n'
        '    printf("%d\\n", s.size);  // 2\n'
        '    return 0;\n'
        '}'
    ),
})

EXAMPLE_SNIPPETS["java"].update({
    "types": (
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        int n = 42;                  // integer\n'
        '        double pi = 3.14;            // floating-point\n'
        '        String text = "42";          // text that looks like a number\n'
        '        System.out.println(Integer.parseInt(text) + n); // parse -> 84\n'
        '    }\n'
        '}'
    ),
    "input": (
        'import java.util.Scanner;            // Scanner reads input\n'
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        Scanner sc = new Scanner(System.in);\n'
        '        int num = sc.nextInt();      // read an int the user types\n'
        '        System.out.println(num * 2); // use the value\n'
        '    }\n'
        '}'
    ),
    "stack": (
        'import java.util.*;\n'
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        Deque<Integer> stack = new ArrayDeque<>(); // used as a stack\n'
        '        stack.push(1);               // push onto the top\n'
        '        stack.push(2);\n'
        '        System.out.println(stack.pop()); // pop the top -> 2\n'
        '    }\n'
        '}'
    ),
    "two_pointers": (
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        int[] nums = {1, 2, 3, 4, 6}; // sorted\n'
        '        int left = 0, right = 4, target = 7;\n'
        '        while (left < right) {        // move pointers inward\n'
        '            int s = nums[left] + nums[right];\n'
        '            if (s == target) { System.out.println(left + "," + right); break; }\n'
        '            else if (s < target) left++; // too small\n'
        '            else right--;                // too big\n'
        '        }\n'
        '    }\n'
        '}'
    ),
    "sliding_window": (
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        int[] nums = {2, 1, 5, 1, 3, 2};\n'
        '        int k = 3, window = 0;\n'
        '        for (int i = 0; i < k; i++) window += nums[i]; // first window\n'
        '        int best = window;\n'
        '        for (int i = k; i < nums.length; i++) {    // slide right\n'
        '            window += nums[i] - nums[i - k];        // add new, drop old\n'
        '            best = Math.max(best, window);\n'
        '        }\n'
        '        System.out.println(best);  // 9\n'
        '    }\n'
        '}'
    ),
    "binary_search": (
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        int[] nums = {1, 3, 5, 7, 9};\n'
        '        int lo = 0, hi = 4, target = 7;\n'
        '        while (lo <= hi) {\n'
        '            int mid = (lo + hi) / 2;     // middle index\n'
        '            if (nums[mid] == target) { System.out.println(mid); break; }\n'
        '            else if (nums[mid] < target) lo = mid + 1; // right half\n'
        '            else hi = mid - 1;                          // left half\n'
        '        }\n'
        '    }\n'
        '}'
    ),
    "linked_lists": (
        'public class Main {\n'
        '    static class Node {          // one link in the chain\n'
        '        int value; Node next;\n'
        '        Node(int v) { value = v; }\n'
        '    }\n'
        '    public static void main(String[] args) {\n'
        '        Node a = new Node(1);    // build 1 -> 2\n'
        '        a.next = new Node(2);\n'
        '        for (Node n = a; n != null; n = n.next) // follow next\n'
        '            System.out.println(n.value);\n'
        '    }\n'
        '}'
    ),
    "recursion": (
        'public class Main {\n'
        '    static int factorial(int n) {    // n! = n * (n-1) * ... * 1\n'
        '        if (n <= 1) return 1;        // base case stops recursion\n'
        '        return n * factorial(n - 1); // smaller subproblem\n'
        '    }\n'
        '    public static void main(String[] args) {\n'
        '        System.out.println(factorial(5)); // 120\n'
        '    }\n'
        '}'
    ),
    "trees": (
        'public class Main {\n'
        '    static class Node {          // a binary tree node\n'
        '        int value; Node left, right;\n'
        '        Node(int v) { value = v; }\n'
        '    }\n'
        '    static void visit(Node n) {  // depth-first pre-order\n'
        '        if (n == null) return;   // base case: empty branch\n'
        '        System.out.println(n.value);\n'
        '        visit(n.left);\n'
        '        visit(n.right);\n'
        '    }\n'
        '    public static void main(String[] args) {\n'
        '        Node root = new Node(1);\n'
        '        root.left = new Node(2);\n'
        '        visit(root);             // 1 2\n'
        '    }\n'
        '}'
    ),
    "graphs": (
        'import java.util.*;\n'
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        // adjacency list: a node maps to its neighbors\n'
        '        Map<Integer, List<Integer>> g = new HashMap<>();\n'
        '        g.put(0, Arrays.asList(1, 2));\n'
        '        for (int to : g.get(0))  // list node 0 neighbors\n'
        '            System.out.println("0 -> " + to);\n'
        '    }\n'
        '}'
    ),
    "dynamic_programming": (
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        int n = 10;\n'
        '        int[] dp = new int[n + 1];   // dp[i] = i-th Fibonacci\n'
        '        dp[0] = 0; dp[1] = 1;        // base cases\n'
        '        for (int i = 2; i <= n; i++)        // build up\n'
        '            dp[i] = dp[i - 1] + dp[i - 2];  // the recurrence\n'
        '        System.out.println(dp[n]);   // 55\n'
        '    }\n'
        '}'
    ),
    "heap": (
        'import java.util.*;\n'
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        // PriorityQueue is a min-heap by default\n'
        '        PriorityQueue<Integer> heap = new PriorityQueue<>();\n'
        '        heap.add(5); heap.add(1); heap.add(8);\n'
        '        System.out.println(heap.poll()); // 1 -- smallest first\n'
        '    }\n'
        '}'
    ),
    "matrix": (
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        int[][] grid = {{1, 2, 3}, {4, 5, 6}}; // 2 rows, 3 cols\n'
        '        for (int r = 0; r < grid.length; r++) {      // walk rows\n'
        '            for (int c = 0; c < grid[0].length; c++) // walk columns\n'
        '                System.out.print(grid[r][c] + " ");  // one cell\n'
        '            System.out.println();\n'
        '        }\n'
        '    }\n'
        '}'
    ),
    "design": (
        'public class Main {\n'
        '    static class Stack {         // a stack with a size limit\n'
        '        int[] items; int size = 0;\n'
        '        Stack(int cap) { items = new int[cap]; } // invariant: size<=cap\n'
        '        void push(int x) {\n'
        '            if (size < items.length) items[size++] = x; // enforce cap\n'
        '        }\n'
        '    }\n'
        '    public static void main(String[] args) {\n'
        '        Stack s = new Stack(2);\n'
        '        s.push(1); s.push(2); s.push(3); // third push ignored\n'
        '        System.out.println(s.size);  // 2\n'
        '    }\n'
        '}'
    ),
})


QUIZ_BY_TOPIC = {
    "variables": ("What is the main purpose of a variable?", ["store a value", "store values", "remember a value"]),
    "types": ("Why do types matter?", ["they define what operations are valid", "valid operations", "memory and operations"]),
    "bitwise": ("Which bitwise operator tests whether a flag bit is present?", ["&", "and"]),
    "input": ("What should you usually do before using numeric input?", ["convert it", "parse it", "cast it"]),
    "conditionals": ("Which construct lets code choose between branches?", ["if", "if else", "if/else"]),
    "loops": ("What do loops help you avoid writing repeatedly?", ["duplicate code", "repeated code", "repetition"]),
    "functions": ("What keyword returns a value from a function/method?", ["return"]),
    "pseudocode": ("What kind of bug often appears when translating 1-indexed pseudo-code to real arrays?", ["off by one", "off-by-one", "index"]),
    "arrays": ("What is the first index in most C/Python/Java arrays?", ["0", "zero"]),
    "strings": ("What is a string made of?", ["characters", "chars"]),
    "hash_maps": ("What is the main advantage of a hash map lookup?", ["fast lookup", "o(1)", "constant time"]),
    "stack": ("Which item is removed first from a stack?", ["last", "most recent", "top"]),
    "two_pointers": ("Two pointers usually means tracking how many indexes?", ["2", "two"]),
    "sliding_window": ("A sliding window tracks a moving what?", ["range", "subarray", "substring", "window"]),
    "binary_search": ("Binary search requires sorted data or what kind of predicate?", ["monotonic", "monotone"]),
    "classes": ("Classes group data with what?", ["behavior", "methods", "functions"]),
    "linked_lists": ("A linked list node stores a value and a reference to what?", ["next", "next node"]),
    "recursion": ("What must every recursive solution have?", ["base case", "a base case"]),
    "trees": ("What is the top node of a tree called?", ["root", "root node"]),
    "graphs": ("Graph traversal usually uses BFS or what?", ["dfs", "depth first search"]),
    "dynamic_programming": ("DP usually stores answers to smaller what?", ["subproblems", "problems"]),
    "heap": ("A heap is useful when repeatedly taking the min or what?", ["max", "maximum", "largest"]),
    "matrix": ("A matrix is indexed by row and what?", ["column", "col"]),
    "design": ("Design problems are mostly about preserving what over operations?", ["invariants", "state", "constraints"]),
}


def _clean_snippet(text: str) -> str:
    return textwrap.dedent(text).strip()


def _ai_lesson(
    title: str,
    objective: str,
    fundamentals: list[str],
    build: str,
    quiz: tuple[str, list[str]],
    example: str = "",
    example_title: str = "Example",
) -> dict:
    lesson = {
        "title": title,
        "objective": objective,
        "fundamentals": fundamentals,
        "build": build,
        "quiz": quiz,
    }
    if example:
        lesson["example"] = _clean_snippet(example)
        lesson["example_title"] = example_title
    return lesson


# Course-audit extensions from PROGRAM Curriculum Audit Guide.pdf. These are
# appended after the shared fundamentals so the existing teach -> practice flow
# and LeetCode unlock path stay intact while each language gains course-specific
# depth.
AUDIT_LESSON_TOPICS = {
    "java": [
        ("java_language_foundations", "Java language foundations", "Cover CS 5004 Java type systems, operators, arrays, strings, constants, and type safety."),
        ("java_bitwise_deep", "Bitwise operations in Java", "Use Java bitwise operators, masks, shifts, and unsigned-shift behavior deliberately."),
        ("java_control_flow", "Java control flow", "Use Java branch and loop constructs deliberately, including tracing and early exits."),
        ("java_methods_contracts", "Methods, scope, and contracts", "Design methods with signatures, purpose statements, preconditions, postconditions, scope, and recursion."),
        ("java_classes_constructors", "Classes, objects, and constructors", "Build Java classes with fields, constructors, methods, this, access control, and toString."),
        ("java_enums_exceptions", "Enums and exceptions", "Represent fixed domains with enums and handle failure with Java exceptions."),
        ("java_encapsulation_invariants", "Encapsulation and invariants", "Protect object state with information hiding, invariants, cohesion, and immutable design."),
        ("java_inheritance_polymorphism", "Inheritance and polymorphism", "Use subclassing, overriding, super, dynamic dispatch, and composition tradeoffs."),
        ("java_abstract_interfaces", "Abstract classes and interfaces", "Model contracts with interfaces, abstract classes, Comparable, Comparator, and interface-based design."),
        ("java_equality_hashing", "Equality, comparison, and hashing", "Implement equals, hashCode, Comparable, and Comparator without breaking Java contracts."),
        ("java_generics_hofs", "Generics and higher-order functions", "Use type parameters, bounded generics, lambdas, functional interfaces, and streams."),
        ("java_recursive_lists", "Recursive lists and ADTs", "Implement recursive linked structures and separate list interfaces from concrete implementations."),
        ("java_adts_collections", "ADTs and Java collections", "Choose and use stacks, queues, trees, maps, lists, sets, iterators, and collection utilities."),
        ("java_design_patterns", "Design patterns", "Recognize and implement common creational, structural, and behavioral Java design patterns."),
        ("java_mvc", "Model-View-Controller", "Separate model state, view rendering, and controller input using clear interfaces."),
        ("java_testing_debug_docs", "Testing, debugging, and docs", "Write JUnit tests, debug with breakpoints, document with Javadoc, and manage builds with Gradle."),
        ("java_random_testing", "Random test data in Java", "Generate reproducible arrays, cases, and fixtures with Random and ThreadLocalRandom."),
        ("java_benchmarking", "Runtime benchmarking in Java", "Measure elapsed time with nanoTime, warm up the JVM, and compare algorithms carefully."),
        ("java_big_o", "Algorithm analysis in Java", "Estimate time and space complexity for loops, recursive methods, ADTs, and divide-and-conquer code."),
        ("java_uml", "UML and diagramming", "Read and draw class diagrams with fields, methods, visibility, inheritance, composition, and dependencies."),
        ("java_packages_builds", "Packages, modules, and organization", "Organize Java projects with packages, imports, JAR/classpath basics, and dependency boundaries."),
    ],
    "c": [
        ("c_systems_linux", "Systems overview and Linux", "Use Linux command-line tools, permissions, shell redirection, gcc flags, and Makefiles."),
        ("c_foundations_headers", "C foundations and headers", "Write C with primitive types, control flow, functions, headers, preprocessing, printf, and scanf."),
        ("c_command_line_args", "Command-line arguments in C", "Use argc and argv to configure command-line programs without recompiling."),
        ("c_file_io", "File I/O in C", "Read and write files safely with fopen, fgets, fread, fwrite, and fclose."),
        ("c_pointers_memory", "Pointers and memory management", "Use pointers, arrays, dynamic allocation, pointer parameters, valgrind, and safe memory habits."),
        ("c_structs_types", "Structs and custom data types", "Define structs, typedefs, enums, unions, self-referential nodes, and allocated records."),
        ("c_debug_assembly", "Debugging, assembly, and CPU basics", "Debug C with gdb and connect compiled code to registers, branches, and CPU execution."),
        ("c_compilers_linkers", "Compilers, linkers, and code generation", "Trace preprocessing, compilation, assembly, linking, object files, and symbol resolution."),
        ("c_function_pointers", "Function pointers in C", "Declare function pointers, build dispatch tables, and use callbacks with qsort."),
        ("c_bitwise_deep", "Bitwise operations and bit fields in C", "Apply bitwise operators to flags, masks, hashing, and packed struct fields."),
        ("c_processes_memory", "Processes and memory hierarchy", "Explain processes, stack frames, heap/data/text segments, caches, locality, and virtual memory."),
        ("c_concurrency_threads", "Concurrency and threads", "Use pthreads, joins, mutexes, shared state, race-condition reasoning, and deadlock avoidance."),
        ("c_networking_sockets", "Networking and sockets", "Build a basic client-server model with IPs, ports, TCP sockets, send, and recv."),
        ("c_linked_lists_deep", "Linked lists in C", "Implement singly and doubly linked lists with insert, delete, search, traversal, and full cleanup."),
        ("c_stacks_queues", "Stacks and queues in C", "Implement stack and queue ADTs with arrays, linked lists, and circular-buffer tradeoffs."),
        ("c_algorithm_analysis_formal", "Formal algorithm analysis", "Analyze loops and recurrences with Big-O, Omega, Theta, substitution, Master theorem, and amortization."),
        ("c_benchmarking", "Runtime benchmarking in C", "Time code with clock_gettime, report elapsed seconds, and compare algorithm runtimes."),
        ("c_quadratic_sorts", "Quadratic sorting", "Trace selection, insertion, and bubble sort, including stability and in-place behavior."),
        ("c_random_testing", "Random test data in C", "Generate random arrays, graphs, and test inputs with reproducible seeds."),
        ("c_nlogn_sorts_proofs", "N log n sorting and proofs", "Implement merge sort and quicksort while reasoning about lower bounds and loop invariants."),
        ("c_trees_heaps", "Trees, heaps, and heap sort", "Implement binary trees, BST operations, heap operations, heap sort, and priority queues."),
        ("c_hash_tables", "Hash tables in C", "Build hash maps with hash functions, chaining, open addressing, load factor, and resizing."),
        ("c_hash_algorithms", "Hash function design in C", "Implement and compare djb2, FNV-1a, and Jenkins OAAT hash functions."),
        ("c_graph_algorithms", "Graph algorithms", "Represent graphs and implement BFS, DFS, topological sort, Dijkstra, and MST awareness."),
        ("c_greedy", "Greedy algorithms", "Use greedy choice and optimal substructure, and test where greedy algorithms fail."),
        ("c_dynamic_programming_deep", "Dynamic programming in C", "Design memoized and tabulated solutions for Fibonacci, coin change, knapsack, and LCS."),
        ("c_recursion_divide_conquer", "Recursion and divide-and-conquer", "Trace C recursion, stack growth, termination, tail recursion, and divide/conquer/combine patterns."),
    ],
    "python": [
        ("python_environment", "Python basics and environment", "Use the REPL, scripts, IDEs, dynamic typing, numeric types, strings, truthiness, None, and docstrings."),
        ("python_control_flow_deep", "Python control flow", "Use if/elif/else, loops, range, break, continue, pass, nested tracing, and match-case."),
        ("python_functions_scope", "Functions, scope, and call patterns", "Write Python functions with defaults, keyword args, *args, **kwargs, lambdas, LEGB scope, and recursion."),
        ("python_builtin_data_structures", "Built-in data structures", "Use lists, tuples, dictionaries, sets, comprehensions, unpacking, and copy semantics."),
        ("python_bitwise_deep", "Bitwise operations in Python", "Use Python bitwise operators, masks, shifts, and arbitrary-size integer behavior."),
        ("python_text_processing", "Strings, regex, and encodings", "Process text with string methods, formatting, regular expressions, and UTF-8 awareness."),
        ("python_file_io_data", "File I/O and data handling", "Read and write text, binary, CSV, JSON, command-line arguments, and argparse options."),
        ("python_error_handling", "Python error handling", "Handle exceptions with try/except/else/finally, raise custom exceptions, and use assertions."),
        ("python_oop_deep", "Object-oriented Python", "Build classes with dunder methods, inheritance, properties, dataclasses, and abstract base classes."),
        ("python_iterators_generators_decorators", "Iterators, generators, and decorators", "Implement iteration protocols, yield generators, decorators, functools.wraps, and context managers."),
        ("python_modules_packages_envs", "Modules, packages, and environments", "Organize imports, packages, virtual environments, requirements, standard library modules, and main guards."),
        ("python_testing", "Testing in Python", "Write unittest and pytest tests with fixtures, parametrization, mocks, coverage, and TDD workflow."),
        ("python_test_automation", "Test automation with subprocess", "Automate running compiled programs, capture output, and verify results from Python."),
        ("python_benchmarking", "Runtime benchmarking in Python", "Measure execution time with timeit and perf_counter, and interpret empirical results."),
        ("python_random_testing", "Random test data in Python", "Use the random module to generate arrays, graphs, and test fixtures."),
        ("python_graph_algorithms", "Graph algorithms in Python", "Implement and compare graph algorithms with adjacency maps, heapq, and density-aware testing."),
        ("python_ai_ml_readiness", "Python for AI/ML readiness", "Use NumPy, Pandas, plotting, notebooks, HTTP requests, and async awareness for AI engineering workflows."),
    ],
}


LESSON_EXPLANATIONS.update({
    "java_language_foundations": [
        "Java separates primitive types (int, double, boolean, char, long, float, byte, short) from reference types such as String, arrays, and objects.",
        "Autoboxing wraps primitives in reference types when generics or collections require objects, but you should still know when values are copied vs. referenced.",
        "Use final for constants and name variables consistently so intent is visible before a reader studies the expression.",
        "Operators include arithmetic, relational, logical, bitwise, and ternary forms; each has precedence and type rules.",
        "Strings are immutable, so repeated modification should use StringBuilder; casts can widen safely or narrow with risk.",
    ],
    "java_bitwise_deep": [
        "Java bitwise operators work on int and long values: &, |, ^, ~, <<, >>, and >>>.",
        "Use named constants for masks, usually powers of two such as READ = 1 << 2, WRITE = 1 << 1, and EXEC = 1.",
        "Combine flags with |, test flags with (flags & READ) != 0, toggle with ^, and clear with flags &= ~READ.",
        "<< shifts left, >> shifts right while preserving the sign bit, and >>> shifts right while filling with zero bits.",
        "Bytes and shorts are promoted to int before bitwise work, so cast deliberately when packing or unpacking smaller values.",
        "Parenthesize bitwise checks because equality and relational operators bind differently than many learners expect.",
        "Bitwise Java appears in permissions, color channels, hashCode mixing, compact protocol fields, and LeetCode bit-manipulation problems.",
    ],
    "java_control_flow": [
        "if/else-if/else chains select one branch; switch and modern switch expressions are clearer for fixed sets of cases.",
        "for loops are good for counted repetition, enhanced for loops walk collections, while loops repeat until a condition changes, and do-while runs at least once.",
        "Trace loops with a state table: iteration number, variables before the body, condition result, and variables after the body.",
        "break exits a loop or switch immediately; continue skips to the next loop iteration.",
        "Nested loops multiply work, so they matter for both correctness and Big-O analysis.",
    ],
    "java_methods_contracts": [
        "A method signature states the method name, parameter types, and return type; void means the method returns no value.",
        "Overloading lets one class define multiple methods with the same name but different parameter lists.",
        "Static methods belong to the class, while instance methods act on a specific object.",
        "Java is pass-by-value: primitive values are copied, and object reference values are copied, so methods can mutate the referred object but not rebind the caller's variable.",
        "Purpose statements, preconditions, and postconditions make behavior testable before implementation details are known.",
        "Local variables live only within their scope; recursive calls create new stack frames until a base case stops them.",
    ],
    "java_classes_constructors": [
        "A class defines fields, constructors, and methods; an object is an instance allocated with new.",
        "Constructors establish valid initial state and can be overloaded or chained with this(...) to avoid duplication.",
        "this names the current object, which is useful when parameter names match field names.",
        "Access modifiers control visibility: private for implementation details, public for the supported API, and protected/package-private for narrower sharing.",
        "Getters and setters expose state safely when direct field access would break an invariant.",
        "toString gives objects a useful text representation for debugging and tests.",
    ],
    "java_enums_exceptions": [
        "An enum represents a fixed set of named values and can also define fields, constructors, and methods.",
        "Exceptions model failures without mixing error paths into normal return values.",
        "Checked exceptions must be declared or caught; unchecked exceptions usually represent programming errors or invalid runtime conditions.",
        "try/catch/finally separates risky code, recovery logic, and cleanup.",
        "Use throw to raise a specific failure and throws in a method signature to declare checked failures.",
    ],
    "java_encapsulation_invariants": [
        "Encapsulation keeps representation private so callers cannot put an object into an invalid state.",
        "A class invariant is a rule that must be true after construction and after every public method call.",
        "Information hiding lets you change fields or helper methods without breaking users of the class.",
        "High cohesion means a class has one clear responsibility; loose coupling means classes depend on narrow contracts.",
        "Immutable objects enforce invariants by setting all state at construction time and exposing no mutators.",
    ],
    "java_inheritance_polymorphism": [
        "extends creates an is-a relationship where a subclass inherits fields and methods from a superclass.",
        "Overriding replaces superclass behavior for a method with the same signature; overloading creates a different signature.",
        "super calls superclass constructors or methods when the subclass needs shared setup or behavior.",
        "Dynamic dispatch chooses the runtime object's method implementation, even when the variable type is the superclass.",
        "Every class ultimately inherits from Object, and instanceof plus casting control safe upcasting and downcasting.",
        "Prefer composition when the relationship is has-a or when inheritance would expose too much implementation detail.",
    ],
    "java_abstract_interfaces": [
        "Abstract classes can hold shared state and partial implementation while leaving abstract methods for subclasses.",
        "Interfaces define behavior contracts and let unrelated classes be used through the same API.",
        "A class can implement multiple interfaces, which is often cleaner than deep inheritance.",
        "Default interface methods provide shared behavior without forcing every implementation to duplicate it.",
        "Comparable defines natural ordering; Comparator defines external/custom ordering.",
    ],
    "java_equality_hashing": [
        "== compares primitive values or object references; equals should compare meaningful object state.",
        "equals must be reflexive, symmetric, transitive, consistent, and false for null.",
        "If two objects are equal, hashCode must return the same value or hash-based collections break.",
        "Comparable.compareTo should agree with equals when natural ordering and equality represent the same concept.",
        "Comparator is safer when you need multiple sort orders for the same type.",
    ],
    "java_generics_hofs": [
        "Generics let classes and methods work with a type parameter instead of Object casts.",
        "Bounds such as <T extends Comparable<T>> let generic code rely on required behavior.",
        "Wildcards express variance: ? extends T for producers, ? super T for consumers.",
        "Functional interfaces represent one-method contracts that lambdas and method references can implement.",
        "Streams create pipelines such as filter, map, and reduce, but they should still be readable and testable.",
    ],
    "java_recursive_lists": [
        "Recursive data definitions describe a value in terms of a base case and a smaller value of the same shape.",
        "A linked list node stores data plus a reference to the next node; recursive traversal follows next until null.",
        "Insertion and deletion require careful pointer rewiring so no nodes are skipped or leaked conceptually.",
        "An ADT interface should say what operations mean without exposing node internals.",
        "ArrayList provides fast index access; LinkedList provides cheap local insert/remove but slower search.",
    ],
    "java_adts_collections": [
        "ADTs define operations and behavior, while implementations choose arrays, links, trees, hashes, or heaps.",
        "Stacks are LIFO, queues are FIFO, trees model hierarchy/order, and maps store key-value associations.",
        "Java Collections separates interfaces (List, Set, Queue, Map) from implementations (ArrayList, HashMap, TreeSet, etc.).",
        "Iterators provide uniform traversal and let containers hide their internal storage.",
        "Collections utilities and streams are useful when they make intent clearer than manual loops.",
    ],
    "java_design_patterns": [
        "A design pattern is a reusable solution shape for a recurring design problem, not code to copy blindly.",
        "Factory and Builder help construct objects while hiding complicated creation logic.",
        "Decorator and Adapter wrap objects to add behavior or translate interfaces.",
        "Strategy, Observer, Iterator, Visitor, and Command separate behavior that changes from objects that use it.",
        "These patterns appear when construction, variation, traversal, or event flow should stay independent from concrete classes.",
        "The right pattern should reduce coupling or duplication; the wrong pattern adds ceremony.",
    ],
    "java_mvc": [
        "MVC separates domain state (Model), presentation (View), and input/application flow (Controller).",
        "The model should expose clear operations and avoid depending on console, GUI, or web details.",
        "A controller translates user input into model calls and chooses what the view should render next.",
        "A view displays state but should not own business rules.",
        "Refactor toward MVC by extracting one responsibility at a time from a monolithic program.",
    ],
    "java_testing_debug_docs": [
        "JUnit tests encode expected behavior with @Test methods, assertions, and setup/teardown when needed.",
        "Boundary cases and equivalence partitions catch more bugs than only testing happy paths.",
        "Black-box tests focus on public behavior; white-box tests use knowledge of implementation paths.",
        "Breakpoints, stepping, and watch variables let you inspect runtime state instead of guessing.",
        "Javadoc and Gradle make a project easier to understand, build, test, and share.",
    ],
    "java_random_testing": [
        "java.util.Random creates reproducible pseudo-random values when constructed with a fixed seed, such as new Random(42).",
        "ThreadLocalRandom.current() is convenient for non-reproducible local random values in concurrent code.",
        "Use nextInt(bound) for integers in [0, bound), nextDouble() for [0.0, 1.0), and Collections.shuffle(list, random) for permutations.",
        "Random tests should log the seed, input size, and generated case so a failing case can be replayed exactly.",
        "Generate arrays in multiple shapes: already sorted, reversed, random, duplicate-heavy, empty, and single-element.",
        "Random testing complements hand-picked boundary cases; it does not replace tests for known edge cases.",
    ],
    "java_benchmarking": [
        "System.nanoTime() is the Java clock for elapsed-time measurement; do not use currentTimeMillis for precise benchmark intervals.",
        "Measure elapsed seconds as (end - start) / 1_000_000_000.0 after capturing start and end around only the code under test.",
        "The JVM warms up methods, loads classes, and may JIT-compile hot code, so run warm-up iterations before collecting data.",
        "Run many trials and report a median or range rather than trusting one timing.",
        "Avoid printing, allocating unrelated data, or reading files inside the timed region when the goal is to compare algorithms.",
        "Microbenchmarking Java correctly is hard; for serious work use JMH, but nanoTime is enough to learn growth trends.",
    ],
    "java_big_o": [
        "Big-O describes how work grows as input size grows, ignoring constant factors.",
        "Common classes include O(1), O(log n), O(n), O(n log n), O(n^2), and O(2^n).",
        "Nested loops, recursive branching, and ADT choices usually dominate complexity.",
        "Space complexity counts extra memory such as arrays, recursion stack frames, and maps.",
        "Divide-and-conquer splits a problem, solves subproblems, and combines results.",
    ],
    "java_uml": [
        "A UML class diagram summarizes classes, fields, methods, and visibility without showing full code.",
        "Inheritance, realization, composition, aggregation, and dependency arrows represent different relationships.",
        "Interfaces can be shown separately so the diagram emphasizes contracts instead of implementations.",
        "Composition means the whole strongly owns the parts; aggregation means a looser has-a relationship.",
        "A useful diagram explains collaboration boundaries for a medium-sized program.",
    ],
    "java_packages_builds": [
        "Packages group related classes and prevent name collisions across a project.",
        "Import statements depend on package names, so directory layout and package declarations should match.",
        "A coherent package exposes clear public interfaces and keeps implementation classes internal where possible.",
        "JAR files bundle compiled classes and metadata; classpaths tell Java where dependencies live.",
        "Build tools such as Gradle standardize source layout, dependencies, tests, and repeatable tasks.",
    ],
    "c_systems_linux": [
        "Systems programming starts with the operating system: kernel services, user-space programs, files, processes, and permissions.",
        "The Linux shell lets you navigate, inspect files, compose tools with pipes, redirect input/output, and configure environment variables.",
        "gcc flags such as -Wall, -Wextra, -g, and -o make compiler feedback and debugging easier.",
        "A Makefile records how files depend on each other so rebuilds are repeatable.",
        "Terminal literacy matters because C systems work often happens outside an IDE.",
    ],
    "c_foundations_headers": [
        "C has explicit primitive types and does not protect you from many invalid operations at runtime.",
        "Header files declare interfaces; source files define implementation.",
        "The preprocessor handles #include, #define, and include guards before the compiler sees normal C.",
        "Function prototypes let one file call functions defined later or elsewhere.",
        "printf and scanf require format specifiers that match the actual argument types.",
    ],
    "c_command_line_args": [
        "A command-line C program can declare main as int main(int argc, char **argv) or int main(int argc, char *argv[]).",
        "argc is the argument count; it is at least 1 because argv[0] is the program name.",
        "argv is an array of C strings; argv[1] is the first user-supplied argument when argc > 1.",
        "Always check argc before reading argv[i], or the program can read past the argument array.",
        "Convert numeric arguments with strtol or strtod so you can detect invalid input instead of trusting atoi silently.",
        "Command-line arguments make tools reusable: the same executable can read different files, choose a sort, or change input size without recompiling.",
        "Print usage text to stderr and return a nonzero status when required arguments are missing.",
    ],
    "c_file_io": [
        "fopen(path, mode) returns a FILE* or NULL on failure; always check the return value before using the handle.",
        "Common modes are \"r\" for read, \"w\" for overwrite/write, \"a\" for append, and binary variants such as \"rb\" and \"wb\".",
        "fgets(buffer, size, file) reads at most size - 1 characters, stops at newline or EOF, and always null-terminates when it succeeds.",
        "Strip a trailing newline after fgets when the line represents a name, key, or token rather than a whole printed line.",
        "fscanf reads formatted data from a file; fread and fwrite read/write binary blocks with explicit byte counts.",
        "fclose flushes buffered output and releases the file descriptor; every successful fopen needs a matching fclose on all paths.",
        "stdin, stdout, and stderr are already-open FILE* streams; use fprintf(stderr, ...) for errors so normal output can be redirected cleanly.",
        "The lab pattern is argc/argv path validation, fopen, loop with fgets, parse and validate each line, build a data structure, close the file, then free all allocated memory.",
    ],
    "c_pointers_memory": [
        "A pointer stores an address; dereferencing follows the address to read or write the pointed value.",
        "Arrays and pointers are closely related, but arrays still have storage and size context you must track yourself.",
        "Passing a pointer lets a function mutate caller-owned data, which is C's pass-by-reference pattern.",
        "Pointer-to-pointer forms such as char **argv let a function update a pointer or walk arrays of strings.",
        "Function pointers let you store callable behavior, such as callbacks or sort comparators.",
        "malloc/calloc/realloc allocate heap memory; every successful allocation needs a matching free when ownership ends.",
        "Valgrind helps find leaks, invalid reads/writes, double frees, and use-after-free bugs.",
    ],
    "c_structs_types": [
        "struct groups fields into one custom record type.",
        "typedef can give a struct a shorter name but should not hide pointer ownership rules.",
        "Self-referential structs support linked lists, trees, and graphs by storing pointers to the same struct type.",
        "Enums name integer states; unions let multiple fields share the same memory when only one is active.",
        "Dynamically allocated structs need clear create/destroy functions to keep ownership explicit.",
    ],
    "c_debug_assembly": [
        "gdb lets you set breakpoints, step by line or instruction, print variables, and inspect the call stack.",
        "Assembly exposes registers, moves, arithmetic, comparisons, jumps, calls, and returns generated from C.",
        "The CPU repeatedly fetches, decodes, and executes instructions.",
        "Registers are tiny fast storage locations; memory is addressed through loads and stores.",
        "Reading simple assembly helps explain undefined behavior, stack frames, and optimization surprises.",
    ],
    "c_compilers_linkers": [
        "The C build pipeline preprocesses, compiles to assembly, assembles to object files, and links into an executable.",
        "Object files contain compiled code plus symbols that the linker resolves across files and libraries.",
        "Static linking copies library code into the executable; dynamic linking loads shared libraries at runtime.",
        "Name resolution fails when declarations, definitions, or linker inputs disagree.",
        "Separate compilation keeps large C programs modular but requires accurate headers and build rules.",
    ],
    "c_function_pointers": [
        "A function pointer stores the address of a function whose parameter and return types match the pointer type.",
        "Declare one as return_type (*name)(param_types); the parentheses around *name are required.",
        "Assign a function pointer with the function name, such as cmp = compare_ints; no call parentheses are used during assignment.",
        "Call through the pointer with ptr(args) or (*ptr)(args); both forms are common C.",
        "Use typedef to keep signatures readable, for example typedef int (*cmp_t)(const void *, const void *).",
        "Arrays of function pointers are dispatch tables: pick behavior by index or enum instead of a long if/else chain.",
        "Callbacks pass behavior into reusable algorithms; qsort(base, count, size, compare) is the standard library example.",
        "Common bugs are missing declaration parentheses, mismatched signatures, storing a pointer to the wrong function type, and calling a NULL function pointer.",
    ],
    "c_bitwise_deep": [
        "C bitwise work should usually use unsigned integer types such as uint32_t so shifts and overflow are predictable.",
        "Bit fields can pack flags inside a struct, for example unsigned int active : 1, but exact layout is implementation-defined.",
        "Masks let you set, clear, toggle, and test specific bits in permissions, status words, and hardware-style registers.",
        "Hash functions use shifts and XOR to mix input bits so similar strings land in different buckets.",
        "Right-shifting a signed negative integer is implementation-defined, so prefer unsigned values for portable bit algorithms.",
        "Shifting by a negative count or by a count greater than or equal to the width of the type is undefined behavior.",
        "Use fixed-width types from stdint.h when the number of bits matters.",
    ],
    "c_processes_memory": [
        "A process is a running program with its own virtual address space and OS-managed state.",
        "C program memory is commonly described as text, data, BSS, heap, and stack segments.",
        "Each function call creates a stack frame for return address, saved state, parameters, and locals.",
        "The memory hierarchy moves from registers to cache to RAM to disk, with latency increasing at each level.",
        "Virtual memory maps pages through page tables so each process sees a private address space.",
        "Spatial and temporal locality explain why contiguous arrays often outperform pointer-heavy structures.",
    ],
    "c_concurrency_threads": [
        "Threads share a process address space, so communication is easy and accidental races are also easy.",
        "pthread_create starts work in a new thread; pthread_join waits for it to finish.",
        "A race condition occurs when correctness depends on unpredictable timing between threads.",
        "Mutexes protect critical sections so only one thread mutates shared state at a time.",
        "Producer-consumer designs use locks or condition variables to coordinate handoff between threads.",
        "Deadlock can happen when threads hold locks while waiting for locks held by each other.",
    ],
    "c_networking_sockets": [
        "Networking code usually models clients connecting to servers over IP addresses and ports.",
        "TCP provides reliable byte streams; UDP sends datagrams without the same delivery guarantees.",
        "A server socket binds, listens, accepts a connection, then sends/receives bytes.",
        "A client socket connects to a server, then uses send and recv to exchange data.",
        "Socket code must handle partial reads/writes, errors, and resource cleanup.",
    ],
    "c_linked_lists_deep": [
        "Linked list operations are pointer rewrites: insert, delete, search, traverse, and free.",
        "Head/tail insertions need different edge-case handling when the list is empty.",
        "Deletion must reconnect neighbors before freeing the removed node.",
        "Doubly linked lists trade extra memory for easier backward traversal and deletion.",
        "Generic lists with void* require clear ownership and casting rules.",
    ],
    "c_stacks_queues": [
        "A stack supports push, pop, and peek with LIFO behavior.",
        "A queue supports enqueue and dequeue with FIFO behavior.",
        "Array-backed ADTs need capacity checks and sometimes circular indexing.",
        "Linked implementations grow flexibly but allocate one node per item.",
        "Stacks support expression evaluation; queues support BFS and producer-consumer buffering.",
    ],
    "c_algorithm_analysis_formal": [
        "Big-O is an upper bound, Big-Omega is a lower bound, and Big-Theta is a tight bound.",
        "Loop analysis depends on how many times each statement runs as n grows.",
        "Recursive algorithms can be described with recurrences such as T(n)=2T(n/2)+n.",
        "Substitution, recursion trees, and the Master theorem are ways to solve recurrences.",
        "Best case, worst case, and average case describe different input scenarios for the same algorithm.",
        "Amortized analysis explains average cost over a sequence of operations, not random average case.",
    ],
    "c_benchmarking": [
        "clock_gettime(CLOCK_MONOTONIC, &ts) captures a high-resolution monotonic timestamp that is not affected by wall-clock changes.",
        "struct timespec stores seconds in tv_sec and nanoseconds in tv_nsec.",
        "Compute elapsed seconds as (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9.",
        "Time only the code you mean to measure; printing inside the timed block can dominate the algorithm runtime.",
        "Run multiple trials and compare medians or trends because OS scheduling, cache state, and background processes create noise.",
        "Use the same input sizes, compiler flags, machine, and data-generation method when comparing algorithms.",
        "Empirical timings should support your Big-O reasoning; they do not replace asymptotic analysis.",
    ],
    "c_quadratic_sorts": [
        "Selection sort repeatedly selects the smallest remaining item and places it in final position.",
        "Insertion sort builds a sorted prefix and is efficient on nearly sorted data.",
        "Bubble sort repeatedly swaps adjacent inverted pairs; early exit stops when no swaps occur.",
        "Stable sorts preserve the relative order of equal keys.",
        "In-place algorithms use only small extra memory beyond the input array.",
    ],
    "c_random_testing": [
        "srand(seed) initializes C's pseudo-random number generator; call it once near the start of main.",
        "srand(time(NULL)) changes the sequence between runs, while srand(42) makes a test replayable.",
        "rand() returns an integer from 0 through RAND_MAX; rand() % n gives a simple value in [0, n) but can be biased.",
        "For sorting tests, generate sorted, reversed, random, duplicate-heavy, empty, and single-element arrays.",
        "For graph tests, generate edge candidates and add an edge when a random value is below a chosen probability.",
        "When a random test fails, print the seed, size, and case type so the same input can be reproduced.",
        "Random tests find surprising cases, but they should sit beside deterministic boundary tests.",
    ],
    "c_nlogn_sorts_proofs": [
        "Merge sort divides the array, sorts halves, then merges into sorted order.",
        "Quicksort partitions around a pivot; pivot choice controls worst-case risk.",
        "Comparison sorting has a lower bound of Omega(n log n) in the general case.",
        "Loop invariants state what remains true before and after each loop iteration.",
        "Correctness proofs connect invariants, termination, and postconditions.",
    ],
    "c_trees_heaps": [
        "Binary tree nodes store a value and left/right child pointers.",
        "Tree traversals include inorder, preorder, postorder, and level-order BFS.",
        "BST search, insert, and delete rely on the invariant left < node < right.",
        "Heaps keep the min or max at the root while allowing efficient insert and extract.",
        "Heap sort builds a heap then repeatedly extracts the next ordered item.",
    ],
    "c_hash_tables": [
        "A hash function maps keys to bucket indexes and should spread typical keys evenly.",
        "Chaining stores collisions in bucket lists; open addressing probes for another slot.",
        "Load factor measures how full the table is and guides resizing.",
        "Average lookup can be O(1), but poor hashing or high load can degrade to O(n).",
        "A C hash map must handle key ownership, equality, collision storage, and cleanup.",
    ],
    "c_hash_algorithms": [
        "A good non-cryptographic hash spreads typical keys uniformly and is cheap enough to run on every lookup.",
        "The avalanche effect means a small input change should flip many output bits, reducing clustered collisions.",
        "djb2 starts at 5381 and updates with hash = hash * 33 + c; the multiply by 33 can be written as (hash << 5) + hash.",
        "FNV-1a starts with an offset basis, XORs each byte into the hash, then multiplies by the FNV prime.",
        "Jenkins one-at-a-time repeatedly adds bytes, shifts, and XORs, then performs final mix steps for stronger avalanche.",
        "Compare algorithms on the same dataset and table size using total collisions, longest chain, average non-empty chain length, filled buckets, and load factor.",
        "No simple hash is best for every dataset; choose based on key shape, table size, collision cost, and performance budget.",
        "These functions are not cryptographic hashes; use a cryptographic library when collision resistance against attackers matters.",
    ],
    "c_graph_algorithms": [
        "Graphs can be represented as adjacency matrices or adjacency lists.",
        "BFS explores by distance layers and gives shortest paths in unweighted graphs.",
        "DFS explores deeply and supports cycle checks, connected components, and topological sort.",
        "Topological sort orders a DAG so every edge goes from earlier to later in the output.",
        "Dijkstra computes shortest paths when edge weights are nonnegative.",
        "Minimum spanning tree algorithms such as Prim and Kruskal connect weighted undirected graphs cheaply.",
    ],
    "c_greedy": [
        "Greedy algorithms make the locally best choice and never revisit it.",
        "They are correct only when the problem has a greedy choice property and optimal substructure.",
        "Activity selection and fractional knapsack are classic successful greedy examples.",
        "Huffman coding uses greedy merging to build optimal prefix codes.",
        "A proof of greedy correctness often uses exchange arguments or contradiction-style reasoning.",
        "Counterexamples are essential because many problems look greedy but require DP or search.",
    ],
    "c_dynamic_programming_deep": [
        "DP applies when subproblems overlap and optimal solutions contain optimal substructure.",
        "Memoization solves recursively and caches answers; tabulation fills a table bottom-up.",
        "A good DP solution defines state, recurrence, base cases, iteration order, and answer extraction.",
        "Coin change, 0/1 knapsack, and LCS show different state shapes.",
        "Space optimization keeps only the rows or states needed for future transitions.",
    ],
    "c_recursion_divide_conquer": [
        "Every recursive function needs a base case, recursive case, and progress toward termination.",
        "C recursion uses stack frames, so deep recursion can overflow the stack.",
        "Divide-and-conquer splits a problem, solves independent subproblems, and combines their answers.",
        "Merge sort, quicksort, binary search, and fast exponentiation all fit this pattern.",
        "Tail recursion can often be rewritten as iteration when stack use matters.",
    ],
    "python_environment": [
        "Python can run interactively in a REPL or from script files, which makes experimentation fast.",
        "Names are dynamically typed: the value has a type, and the name can later refer to another type.",
        "Numeric types include int, float, and complex; / produces true division and // produces floor division.",
        "Strings support slicing, f-strings, common methods, and Unicode text by default.",
        "Truthiness, None, comments, and docstrings are basic tools for readable Python programs.",
    ],
    "python_control_flow_deep": [
        "if/elif/else branches are driven by booleans and truthy/falsy values.",
        "for loops iterate over ranges, strings, lists, dictionaries, files, and any iterable.",
        "while loops continue until their condition becomes false, so loop state must change.",
        "break exits, continue skips, and pass is an explicit placeholder.",
        "match-case can express structural pattern matching for fixed shapes and tagged data.",
    ],
    "python_functions_scope": [
        "Python functions can use positional arguments, keyword arguments, defaults, *args, and **kwargs.",
        "The LEGB rule resolves names through local, enclosing, global, and built-in scopes.",
        "Closures capture variables from an enclosing function so inner functions can remember state.",
        "Lambdas create small anonymous functions, usually for callbacks or key functions.",
        "Higher-order functions accept or return functions, such as map, filter, and sorted(key=...).",
        "Type hints document intended types and help tools, but Python still checks most types at runtime.",
    ],
    "python_builtin_data_structures": [
        "Lists are mutable ordered sequences; tuples are ordered and usually immutable.",
        "Dictionaries map keys to values and preserve insertion order in modern Python.",
        "Sets store unique items and support union, intersection, and difference.",
        "Comprehensions build lists, dicts, and sets from compact loop/filter expressions, and generator expressions stay lazy.",
        "Shallow copies duplicate the outer container; deep copies recursively copy nested objects.",
    ],
    "python_bitwise_deep": [
        "Python supports &, |, ^, ~, <<, and >> on integers, just like lower-level languages.",
        "Python integers grow as large as needed, so you do not naturally overflow at 32 or 64 bits.",
        "Use masks with explicit widths when simulating C-style behavior, for example value & 0xffffffff.",
        "Left shift multiplies by powers of two, and right shift performs arithmetic shift on signed integers.",
        "Bit flags still work well in Python when you need compact option sets or LeetCode bit-manipulation practice.",
        "bin(x), x.bit_count(), int.to_bytes, and int.from_bytes are useful helpers when inspecting or packing bits.",
        "Parenthesize bit tests such as (flags & READ) != 0 for clarity even when Python precedence would allow shorter code.",
    ],
    "python_text_processing": [
        "String methods such as split, join, strip, replace, and find solve many parsing tasks without regex.",
        "f-strings are the standard readable way to interpolate values into text.",
        "The re module supports matching, searching, findall, and substitution with regular expressions.",
        "ASCII is a small character set; UTF-8 can encode all Unicode characters and is the default expectation for most modern text.",
        "Text pipelines should be explicit about encoding when reading files from unknown sources.",
    ],
    "python_file_io_data": [
        "Use with open(...) as f so files close even when an exception occurs.",
        "Text files decode bytes into str; binary files read and write raw bytes.",
        "The csv module handles commas, quotes, and rows better than manual splitting.",
        "json.loads and json.dumps convert between JSON text and Python data.",
        "sys.argv is raw command-line input; argparse gives typed options, help text, and validation.",
    ],
    "python_error_handling": [
        "try/except handles expected failures without crashing the whole program.",
        "else runs only when no exception occurred; finally runs for cleanup either way.",
        "Common exceptions include ValueError, TypeError, KeyError, IndexError, and FileNotFoundError.",
        "raise reports a failure intentionally, and custom exception classes make domain errors clearer.",
        "assert is useful for internal sanity checks, not for validating user input in production.",
    ],
    "python_oop_deep": [
        "__init__ initializes each instance, and self names the current object.",
        "Class variables are shared by the class; instance variables belong to one object.",
        "Dunder methods such as __str__, __repr__, __eq__, __hash__, and __lt__ integrate objects with Python syntax.",
        "Inheritance and super reuse behavior, while multiple inheritance follows the method resolution order.",
        "@property, dataclasses, and abstract base classes from abc help express clean object APIs.",
    ],
    "python_iterators_generators_decorators": [
        "The iterator protocol uses __iter__ and __next__ so objects can work in for loops.",
        "A generator function uses yield to produce values lazily without building a full list.",
        "Generator expressions are lazy versions of list comprehensions.",
        "Decorators wrap functions with extra behavior while keeping the call site unchanged.",
        "Context managers define __enter__ and __exit__, or use contextlib, to manage setup and cleanup.",
    ],
    "python_modules_packages_envs": [
        "The interpreter, scripts, and IDEs are all normal ways to run Python during development.",
        "import and from ... import bring module names into the current file.",
        "Packages are directories with Python modules and often an __init__.py file.",
        "Virtual environments isolate installed packages so projects do not break each other.",
        "requirements.txt records dependencies; pip installs them into the active environment.",
        "if __name__ == '__main__' keeps script behavior separate from import behavior.",
    ],
    "python_testing": [
        "unittest organizes tests into classes with assertions and optional setUp/tearDown methods.",
        "pytest favors simple test functions, powerful assertions, fixtures, and parametrization.",
        "TDD writes a failing test first, then implements the smallest code that passes.",
        "Mocks replace slow or external dependencies so tests stay focused and repeatable.",
        "Coverage helps reveal untested code paths but does not prove the assertions are meaningful.",
    ],
    "python_test_automation": [
        "Python is often used as a harness around compiled C programs because it can launch processes, capture output, and summarize results quickly.",
        "subprocess.run([...], capture_output=True, text=True, timeout=5) returns a CompletedProcess with stdout, stderr, and returncode.",
        "Always pass the command as a list of arguments, not one shell string, unless you specifically need shell behavior.",
        "A timeout turns infinite loops or stuck programs into a reported TIMEOUT result instead of a hung test suite.",
        "The harness pattern is: build argv, run the program, inspect returncode, parse stdout/stderr, compare expected output, record the result, and print a summary.",
        "Use csv.writer or csv.DictWriter when the output should become a spreadsheet or graph.",
        "Use difflib.unified_diff for helpful expected-vs-actual output when a program prints the wrong text.",
    ],
    "python_benchmarking": [
        "timeit runs a small statement many times and reduces noise from setup overhead.",
        "timeit.repeat gives multiple trials so you can compare the minimum, median, or spread.",
        "time.perf_counter() is the right clock for elapsed wall time around larger blocks of code.",
        "time.process_time() measures CPU time and excludes sleep or much I/O waiting.",
        "Benchmark the computation separately from printing, file reading, random input generation, and plotting.",
        "Python timings are noisier than C because interpreter overhead, garbage collection, and object allocation are part of the runtime.",
        "Use timing data to compare growth curves, such as list-based Dijkstra versus heap-based Dijkstra as graph density changes.",
    ],
    "python_random_testing": [
        "random.seed(42) makes generated cases deterministic, which is essential for replaying a failure.",
        "random.randint(a, b) includes both endpoints; random.randrange(n) gives values in [0, n).",
        "random.random() returns a float in [0.0, 1.0), useful for probability-based graph edge generation.",
        "random.shuffle(list) permutes a list in place; random.sample draws unique items without replacement.",
        "Generate cases by shape, not only size: empty, one item, sorted, reversed, random, duplicate-heavy, sparse graph, and dense graph.",
        "Log the seed, parameters, and generated input when a random test fails.",
        "Random tests are strongest when paired with assertions that verify invariants, such as 'the output is sorted' or 'all generated edges reference valid nodes'.",
    ],
    "python_graph_algorithms": [
        "Python graph code usually represents an adjacency list as a dict mapping each node to neighbor nodes or (neighbor, weight) pairs.",
        "Dijkstra's algorithm tracks the best-known distance to each node and repeatedly expands the unvisited node with smallest distance.",
        "heapq implements a min-priority queue and makes the next-smallest-distance step efficient.",
        "A list-based Dijkstra scan can be O(V^2); a heap-based implementation is closer to O((V + E) log V) for adjacency lists.",
        "Graph density matters: dense graphs have many edges, so edge processing dominates; sparse graphs make priority-queue overhead more visible.",
        "Use float('inf') for unknown distances and a previous-node map when the actual shortest path must be reconstructed.",
        "Manual tracing and visualizers help confirm frontier updates before trusting runtime measurements.",
    ],
    "python_ai_ml_readiness": [
        "NumPy arrays support vectorized numeric operations and broadcasting across shapes.",
        "Pandas Series and DataFrames make tabular cleaning, filtering, grouping, and CSV loading productive.",
        "Matplotlib and Seaborn help inspect distributions, trends, and model results visually.",
        "Jupyter notebooks are useful for exploration, but production logic should move into tested modules.",
        "AI engineering also needs API calls with requests and basic awareness of async workflows.",
    ],
})

DEEPENED_LESSON_CONTEXT = {
    "variables": [
        "When you read code, track each variable's current value and the line where that value last changed.",
        "A useful variable name says what the value means in the problem, not only what type it has.",
    ],
    "types": [
        "Types are also promises: a function that expects an int should not receive unparsed text, and a pointer should not receive a plain value.",
        "When a value crosses a boundary such as input, file parsing, or function parameters, re-check the type assumption at that boundary.",
    ],
    "input": [
        "Treat user input as untrusted: validate that it exists, has the expected shape, and can be converted before using it.",
        "Separate reading input from processing it so the core logic can be tested without typing at the console.",
    ],
    "conditionals": [
        "Order conditions from most specific to most general when only one branch should run.",
        "Write the boundary values next to the condition, then test exactly those boundaries.",
    ],
    "loops": [
        "Before writing a loop, name the loop invariant: what should be true before and after every pass.",
        "Trace the first iteration, a middle iteration, and the final iteration to catch off-by-one mistakes.",
    ],
    "functions": [
        "A strong function has one job, a small parameter list, and a return value or side effect that is easy to describe.",
        "If a function mutates data, say who owns that data and whether callers can see the mutation.",
    ],
    "arrays": [
        "Arrays are best when you need compact indexed storage and predictable traversal.",
        "Always connect the loop bounds to the array length; hard-coded lengths become bugs when input size changes.",
    ],
    "strings": [
        "Text processing is usually parsing: strip noise, split into meaningful parts, validate the parts, then convert types.",
        "In C, remember that a string is a char array ending with '\\0'; forgetting room for that terminator causes memory bugs.",
    ],
    "hash_maps": [
        "Hash maps trade ordering for fast access; choose them when the key is the natural way to find the value.",
        "Reason about the key's equality rule first because the hash table is only correct when equal keys are treated consistently.",
    ],
    "stack": [
        "Stacks are a control-flow data structure: they remember what must be finished later.",
        "When debugging stack logic, write the stack contents after each push and pop.",
    ],
    "two_pointers": [
        "The pointer movement rule is the algorithm: be able to explain why moving left or right cannot skip a valid answer.",
        "Stop conditions matter; left < right is different from left <= right when the same element cannot be used twice.",
    ],
    "sliding_window": [
        "A window solution depends on maintaining a summary, such as count, sum, or frequency map, as the endpoints move.",
        "Ask whether the constraint is fixed-size or variable-size because that decides whether the left edge moves every step or only when invalid.",
    ],
    "binary_search": [
        "Binary search is not only for arrays; it works on any answer space where the predicate changes one direction.",
        "Use one consistent interval convention, such as closed [lo, hi] or half-open [lo, hi), and keep the update rules matched to it.",
    ],
    "classes": [
        "Classes are strongest when they protect a small set of invariants behind methods.",
        "Fields describe state; methods describe allowed state transitions.",
    ],
    "linked_lists": [
        "Diagram each node as data plus next, and draw arrows before coding an insert or delete.",
        "If you overwrite a next pointer before saving the rest of the list, the diagram shows the lost chain immediately.",
        "Linked lists make local insert/delete cheap only after you already have the relevant node or previous node.",
    ],
    "recursion": [
        "Write the base case first, then the smaller recursive call, then how the current frame combines that result.",
        "A recursion trace is a stack trace: each call has its own parameters and locals.",
    ],
    "trees": [
        "Draw tree nodes as values with left and right child links; omitted children are null leaves.",
        "For DFS, draw the call stack beside the tree; for BFS, draw the queue contents at each level.",
        "Visualization tools are useful because they make traversal order and frontier state visible.",
    ],
    "graphs": [
        "Draw nodes as circles and edges as arrows or lines; write weights directly on weighted edges.",
        "Adjacency lists are usually better for sparse graphs; adjacency matrices make edge lookup simple but cost O(V^2) space.",
        "For BFS, number nodes by discovery order; for DFS, mark when the search backtracks; for Dijkstra, track frontier distances.",
    ],
    "dynamic_programming": [
        "DP becomes manageable when you can say exactly what one table cell or memo entry means.",
        "Pascal's triangle is a clear DP model: each interior value depends on the two values above it.",
        "Counting operations alongside runtime helps connect the recurrence to empirical growth.",
    ],
    "heap": [
        "A heap gives priority order, not full sorted order; only the root is guaranteed to be the next item.",
        "Dijkstra uses a min-heap so the next expanded node is the currently cheapest frontier node.",
    ],
    "matrix": [
        "Always name dimensions as rows first, columns second; grid[r][c] means row r, column c.",
        "When matrices represent graphs, matrix[i][j] means the edge from i to j; zero often means no edge unless zero-weight edges are allowed.",
    ],
    "design": [
        "Start design problems by listing operations, required complexity, and invariants.",
        "A good design makes invalid states hard to create and easy to detect in tests.",
    ],
    "java_language_foundations": [
        "Reading Java well means distinguishing primitive value copying from object reference copying.",
        "Because Java is statically typed, many design errors are best caught by making method signatures precise.",
    ],
    "java_control_flow": [
        "Use switch for fixed categories and if/else for ranges or conditions that are not mutually named cases.",
        "When tracing Java loops, record the condition before the body because the final failed check is part of the loop behavior.",
    ],
    "java_methods_contracts": [
        "A contract lets a caller use a method without reading its implementation.",
        "Recursive Java methods need the same contract as iterative ones: valid inputs, result meaning, and failure behavior.",
    ],
    "java_classes_constructors": [
        "Constructors should leave the object ready to use; do validation before storing invalid fields.",
        "Use this.field when it improves clarity, especially when constructor parameters share field names.",
    ],
    "java_enums_exceptions": [
        "Enums are better than raw strings for fixed states because the compiler catches misspellings.",
        "Use exceptions for exceptional or invalid states, not as a substitute for normal branching.",
    ],
    "java_encapsulation_invariants": [
        "Private fields are not enough by themselves; public methods must also preserve the invariant.",
        "Immutable classes are often easier to test because state cannot change after construction.",
    ],
    "java_inheritance_polymorphism": [
        "Inheritance should express substitutability: a subclass should be usable anywhere the superclass is expected.",
        "If overriding requires many special cases, composition or Strategy may be the clearer design.",
    ],
    "java_abstract_interfaces": [
        "Program to interfaces when callers only need behavior, not implementation details.",
        "Use abstract classes when implementations truly share state or helper behavior.",
    ],
    "java_equality_hashing": [
        "Equality bugs often surface only inside HashSet, HashMap, TreeSet, or sorting code.",
        "If equals uses id, hashCode and compareTo should not silently use a different identity unless you can justify it.",
    ],
    "java_generics_hofs": [
        "Generics move type errors from runtime casts to compile-time feedback.",
        "Use lambdas when the behavior is small and local; name a method when the behavior needs explanation or reuse.",
    ],
    "java_recursive_lists": [
        "Recursive list ADTs make the empty case explicit, which clarifies termination.",
        "Separate the public list API from node internals so callers cannot break links directly.",
    ],
    "java_adts_collections": [
        "Choose the interface by behavior first, then choose the implementation by performance needs.",
        "Iterating while mutating a collection requires care; use iterators or collect changes separately.",
    ],
    "java_design_patterns": [
        "A pattern should solve pressure already visible in the code, such as repeated branching or complicated construction.",
        "Name the pattern only after you can explain what coupling it removes.",
    ],
    "java_mvc": [
        "The model should be testable without a view and usable by more than one kind of interface.",
        "Controllers are translation layers: input events become model operations, then model state becomes view output.",
    ],
    "java_testing_debug_docs": [
        "A good test name states the condition and expected behavior.",
        "Debugging is faster when you first predict the next value, then step and compare prediction to reality.",
    ],
    "java_big_o": [
        "For Java collections, complexity depends on the concrete implementation, not only the interface.",
        "Recursive complexity includes both the number of calls and the cost inside each call.",
    ],
    "java_uml": [
        "A useful UML diagram omits method bodies and focuses on relationships a reader must understand.",
        "Composition, aggregation, and dependency arrows should match real ownership and lifetime in the code.",
    ],
    "java_packages_builds": [
        "Packages should follow responsibility boundaries, not random file grouping.",
        "Build tools make dependency versions and test commands repeatable across machines.",
    ],
    "c_systems_linux": [
        "Shell redirection and pipes are part of the testing surface for command-line C tools.",
        "Makefiles matter once a lab has multiple .c files because they encode dependencies and flags consistently.",
    ],
    "c_foundations_headers": [
        "Headers are contracts between files; keep definitions in .c files unless a constant or macro truly belongs in the interface.",
        "Compiler warnings are teaching feedback, not noise; fix them before chasing runtime bugs.",
    ],
    "c_pointers_memory": [
        "Draw stack variables and heap blocks separately; arrows should show which pointer owns or refers to each block.",
        "For every malloc, write down the matching free location and which function is responsible for it.",
    ],
    "c_structs_types": [
        "Struct layout turns related fields into one unit, which is essential for nodes, graph edges, table entries, and records.",
        "Self-referential structs need a named struct tag because the type refers to itself before the typedef is complete.",
    ],
    "c_debug_assembly": [
        "Godbolt Compiler Explorer lets you paste C and compare generated assembly across compilers and optimization levels.",
        "Try x * 32 and x << 5 at different optimization levels; compilers often generate the same shift instruction.",
        "Assembly inspection is most useful when tied to a question: why is this slower, where is this branch, or what did optimization remove?",
    ],
    "c_compilers_linkers": [
        "A declaration tells the compiler a symbol exists; a definition gives the linker actual storage or code to connect.",
        "Linker errors usually mean the build command or function definitions do not match the headers.",
    ],
    "c_processes_memory": [
        "Stack frames explain why local variables disappear after return and why deep recursion can fail.",
        "Cache locality explains why contiguous arrays can outperform pointer-heavy structures even with the same Big-O.",
    ],
    "c_concurrency_threads": [
        "If two threads can touch the same mutable value, decide which lock or ownership rule protects it.",
        "Race bugs are schedule-dependent, so passing once does not prove the code is safe.",
    ],
    "c_networking_sockets": [
        "Sockets are file descriptors with protocol behavior; they still need close and error checks.",
        "TCP sends a stream, not message objects, so code must handle partial reads and writes.",
    ],
    "c_linked_lists_deep": [
        "For delete operations, keep track of both current and previous nodes so you can reconnect the chain.",
        "Freeing a list requires saving next before freeing current; otherwise you lose the only path forward.",
    ],
    "c_stacks_queues": [
        "Array stacks are simple and cache-friendly but fixed-capacity unless resized.",
        "Circular queues avoid moving elements by wrapping front and back indexes with modulo arithmetic.",
    ],
    "c_algorithm_analysis_formal": [
        "State what n represents before analyzing; n might be elements, vertices, edges, rows, or characters.",
        "Separate theoretical growth from measured runtime because constants and hardware still affect small inputs.",
    ],
    "c_quadratic_sorts": [
        "Sorting labs should trace the array after each outer pass so the invariant becomes visible.",
        "An early-exit bubble sort changes the best case from quadratic work to linear checking.",
    ],
    "c_nlogn_sorts_proofs": [
        "Merge sort uses extra temporary storage, so it is not in-place in the strict sense.",
        "When translating pseudo-code merge sort, be explicit about inclusive bounds l, m, and r.",
    ],
    "c_trees_heaps": [
        "When building a tree from file input, parse one line, validate it, insert it, then move to the next line.",
        "Tree traversal output is easiest to verify by comparing preorder, inorder, and postorder on a small known tree.",
    ],
    "c_hash_tables": [
        "Collision metrics such as longest chain and filled-bucket percentage reveal more than total collision count alone.",
        "Load factor has to be interpreted with the collision strategy; chaining and open addressing degrade differently.",
    ],
    "c_graph_algorithms": [
        "Converting an adjacency list to a matrix means visiting each stored edge and writing matrix[src][dst] = weight.",
        "Converting a matrix to a list means scanning every cell and adding an edge for each nonzero or present value.",
        "Dense graphs push you toward matrices; sparse graphs usually favor adjacency lists.",
    ],
    "c_greedy": [
        "A greedy algorithm needs a proof or counterexample search, not only a plausible local rule.",
        "When a greedy idea fails, the failure case often points to a DP state you were missing.",
    ],
    "c_dynamic_programming_deep": [
        "For Pascal's triangle, a 2D table makes dependencies visible: table[n][k] depends on table[n-1][k-1] and table[n-1][k].",
        "Memoized recursion and bottom-up tabulation can compute the same values in different orders.",
    ],
    "c_recursion_divide_conquer": [
        "Divide-and-conquer should shrink the input each call and combine results only after subproblems are solved.",
        "Trace recursion with parameters, not only return values, because wrong bounds cause most C recursion bugs.",
    ],
    "python_environment": [
        "Use the REPL for quick experiments, but put repeatable work in scripts so it can be rerun and tested.",
        "Python's dynamic typing gives speed while writing; type hints give readers and tools the missing intent.",
    ],
    "python_control_flow_deep": [
        "Python indentation is syntax, so formatting changes program behavior.",
        "A loop over a file, dictionary, or generator consumes values lazily, which can be useful for large inputs.",
    ],
    "python_functions_scope": [
        "Default arguments are evaluated once at function definition time, so avoid mutable defaults like [].",
        "Closures and lambdas are powerful, but named functions are clearer when behavior is reused or tested.",
    ],
    "python_builtin_data_structures": [
        "Python containers are references to objects; copying a list does not automatically deep-copy nested values.",
        "Choose dictionaries for lookup, sets for uniqueness, lists for order, and tuples for fixed records.",
    ],
    "python_text_processing": [
        "Prefer simple string methods before regex when the delimiter or transformation is straightforward.",
        "Always specify encoding when reading course data or generated files that may move across machines.",
    ],
    "python_file_io_data": [
        "Use newline='' with csv files so the csv module handles line endings correctly.",
        "argparse makes scripts usable by other people because it documents inputs and validates options.",
    ],
    "python_error_handling": [
        "Catch the narrowest exception you can handle; broad except blocks hide real bugs.",
        "Use exception messages that include the bad value or context needed to diagnose the failure.",
    ],
    "python_oop_deep": [
        "Dataclasses are excellent for data-focused classes, but behavior-heavy objects still need clear methods and invariants.",
        "Dunder methods let your objects participate naturally in printing, comparison, hashing, and containers.",
    ],
    "python_iterators_generators_decorators": [
        "Generators are ideal when you can produce values one at a time instead of storing an entire result list.",
        "Decorators should preserve metadata with functools.wraps so debugging and docs still show the original function name.",
    ],
    "python_modules_packages_envs": [
        "A main guard keeps importable code from running side effects during tests.",
        "Virtual environments make dependency problems local to one project instead of system-wide.",
    ],
    "python_testing": [
        "Parametrized tests turn a table of examples into one readable test body.",
        "For lab harnesses, tests should report the command run, stdout, stderr, return code, and timeout status.",
    ],
    "python_ai_ml_readiness": [
        "Notebook exploration should produce reusable functions once the workflow stabilizes.",
        "Plots are not just decoration; they reveal outliers, scaling curves, and data quality problems.",
    ],
}

for _topic, _extra_points in DEEPENED_LESSON_CONTEXT.items():
    LESSON_EXPLANATIONS.setdefault(_topic, []).extend(_extra_points)


PRACTICE_TASKS.update({
    "java_language_foundations": "Write a Java class that declares one primitive, one final constant, one StringBuilder, one array, and one safe widening cast. Print each result.",
    "java_bitwise_deep": "Write a Java program with READ, WRITE, and EXEC bit flags. Combine flags, test one flag with &, clear one flag with ~, and print the results.",
    "java_control_flow": "Write a Java method that takes an int score and returns a letter grade using if/else or switch. Add a loop that prints a state table for scores 0, 25, 50, 75, 100.",
    "java_methods_contracts": "Write a Java method with a purpose comment, precondition, postcondition, parameters, return value, and one recursive helper.",
    "java_classes_constructors": "Create a BankAccount class with private balance, overloaded constructors, deposit, withdraw, and toString. Use this where field and parameter names match.",
    "java_enums_exceptions": "Create an enum OrderStatus and a method that throws IllegalArgumentException for invalid transitions. Catch it in main and print a useful message.",
    "java_encapsulation_invariants": "Design an immutable Range class whose constructor rejects end < start and whose methods never expose mutable internal state.",
    "java_inheritance_polymorphism": "Create Shape, Circle, and Rectangle classes. Override area(), store them in a Shape[] array, and show dynamic dispatch in a loop.",
    "java_abstract_interfaces": "Define a Payable interface and an abstract Employee class. Implement two employee types and sort them with a Comparator.",
    "java_equality_hashing": "Create a Student class and override equals and hashCode based on id. Add two equal students to a HashSet and show only one remains.",
    "java_generics_hofs": "Write a generic max method for Comparable values, then use a stream pipeline to filter, map, and reduce a list of numbers.",
    "java_recursive_lists": "Define a ListNode class and a ListADT interface. Implement recursive size() and iterative append() for a singly linked list.",
    "java_adts_collections": "Solve one small task three ways: Stack/Deque for reverse order, Queue for FIFO order, and Map for counting keys.",
    "java_design_patterns": "Implement Strategy for two discount rules, then briefly identify where Factory or Decorator would fit in the same program.",
    "java_mvc": "Split a tiny counter app into CounterModel, CounterView, and CounterController classes with no printing inside the model.",
    "java_testing_debug_docs": "Write a JUnit-style test plan for BankAccount: normal deposit, overdraft boundary, negative input, and toString output. Include one Javadoc comment.",
    "java_random_testing": "Generate a reproducible random int array with new Random(42), sort a copy, and print whether the sorted copy is nondecreasing.",
    "java_benchmarking": "Use System.nanoTime to time sorting arrays of at least two sizes. Warm up once, then print elapsed milliseconds for each size.",
    "java_big_o": "For three Java snippets you write (single loop, nested loop, binary search), add comments with time and space complexity.",
    "java_uml": "Write a text UML sketch for a Library system with Book, Member, Loan, and LoanRepository. Include visibility and relationships.",
    "java_packages_builds": "Sketch a Java project layout with packages model, view, controller, and test. Include one import and one Gradle dependency line.",
    "c_systems_linux": "Write the shell commands to create hello.c, compile it with gcc -Wall -Wextra -g -o hello hello.c, run it, and redirect output to out.txt.",
    "c_foundations_headers": "Create a tiny two-file C program: math_utils.h declares add(), math_utils.c defines it, and main.c calls it with printf.",
    "c_command_line_args": "Write a C program that requires one filename argument, prints usage to stderr if it is missing, and prints argv[0] and argv[1] when present.",
    "c_file_io": "Write a C program that opens the filename from argv[1], reads it line by line with fgets, counts the lines, closes the file, and prints the count.",
    "c_pointers_memory": "Write a C function increment(int *p), allocate an int with malloc, call increment, print the value, then free it.",
    "c_structs_types": "Define a typedef struct Student with name and id, allocate one Student, fill fields, print it, and free it.",
    "c_debug_assembly": "Write a short C loop and list the gdb commands to break at main, step, print the loop variable, and inspect the backtrace.",
    "c_compilers_linkers": "Write commands that compile main.c and util.c into .o files, link them into app, then explain which step resolves symbols.",
    "c_function_pointers": "Create two small int functions, store them in an array of function pointers, call one by index, and print the result.",
    "c_bitwise_deep": "Write C functions set_bit, clear_bit, toggle_bit, and test_bit for a uint32_t value. Demonstrate each with printf.",
    "c_processes_memory": "Draw or write a labeled memory map for one C program showing text, data, BSS, heap, stack, and one variable in each where possible.",
    "c_concurrency_threads": "Write a pthread counter example guarded by a mutex. Include the race that would occur if the lock were removed.",
    "c_networking_sockets": "Sketch the server-side socket call order: socket, bind, listen, accept, recv, send, close. Add one line describing the client connect path.",
    "c_linked_lists_deep": "Implement insert_head, search, delete_value, print_list, and free_list for a singly linked list of ints.",
    "c_stacks_queues": "Implement either an array stack with capacity checks or a circular-array queue with wraparound indexes.",
    "c_algorithm_analysis_formal": "Analyze one nested loop and one recurrence. State Big-O, Big-Omega, Big-Theta, and the reasoning.",
    "c_benchmarking": "Use clock_gettime(CLOCK_MONOTONIC) to time a loop or sort function across at least three input sizes, then print a timing table.",
    "c_quadratic_sorts": "Implement insertion sort in C and add comments tracing how the sorted prefix grows on [5, 2, 4, 1].",
    "c_random_testing": "Generate a random array using srand with a fixed seed, sort it, verify it is sorted, and print the seed plus pass/fail.",
    "c_nlogn_sorts_proofs": "Implement merge sort or quicksort in C and write a loop invariant for the merge or partition step.",
    "c_trees_heaps": "Implement BST search and insert, then describe how a min-heap would store the same values in an array.",
    "c_hash_tables": "Build a small chained hash table for string keys with insert and search. Track load factor after each insert.",
    "c_hash_algorithms": "Implement djb2 and FNV-1a for strings, hash the same list of words into a fixed table size, and print collision counts.",
    "c_graph_algorithms": "Represent a graph with adjacency lists and implement BFS that prints distance from a start node.",
    "c_greedy": "Implement activity selection after sorting intervals by finish time. Add one counterexample where a different greedy rule fails.",
    "c_dynamic_programming_deep": "Implement bottom-up coin change or LCS in C. Name the state, recurrence, base cases, and table order.",
    "c_recursion_divide_conquer": "Write recursive binary search in C, then rewrite it iteratively and compare stack usage.",
    "python_environment": "Write a Python script that demonstrates int, float, complex, / vs //, f-strings, truthiness, None, and a module docstring.",
    "python_control_flow_deep": "Write a Python program that uses if/elif/else, for/range, while, break, continue, pass, and match-case on a simple command string.",
    "python_functions_scope": "Write a function summarize(*nums, scale=1, **labels), use a lambda as sorted(key=...), and add type hints.",
    "python_builtin_data_structures": "Use a list comprehension, dict comprehension, set operation, tuple unpacking, and a shallow-copy example in one short script.",
    "python_bitwise_deep": "Write Python helpers to set, clear, toggle, and test a flag bit. Demonstrate them with READ, WRITE, and EXEC flags.",
    "python_text_processing": "Parse a comma-separated sentence using split/strip, rebuild it with join, then use re.findall to extract numbers.",
    "python_file_io_data": "Read a CSV file, convert rows to dictionaries, write JSON output, and add argparse for input/output paths.",
    "python_error_handling": "Write a safe_int function that catches ValueError, raises a custom InvalidAgeError for negative values, and uses finally for cleanup text.",
    "python_oop_deep": "Create a @dataclass Point with __str__, __eq__, __lt__, a @property, and an abstract Shape base class.",
    "python_iterators_generators_decorators": "Write a countdown generator, a timing/logging decorator with functools.wraps, and a context manager using contextlib.",
    "python_modules_packages_envs": "Sketch a package layout with __init__.py, a main guard, requirements.txt, and commands to create/activate a venv.",
    "python_testing": "Write pytest tests with one fixture, one parametrize case, and one mock for a function that calls an external API.",
    "python_test_automation": "Write a Python harness that runs a compiled program with subprocess.run, captures stdout/stderr, enforces a timeout, and records pass/fail rows.",
    "python_benchmarking": "Use timeit.repeat or perf_counter to compare two functions over increasing input sizes, then print a small timing table.",
    "python_random_testing": "Generate reproducible random arrays and graphs with random.seed(42), then assert basic invariants such as sorted output or valid edge endpoints.",
    "python_graph_algorithms": "Implement heapq-based Dijkstra for a weighted adjacency dict and compare it against a list-scan version on sparse and dense random graphs.",
    "python_ai_ml_readiness": "Load a CSV into Pandas, compute one groupby summary, convert one column to a NumPy array, and plot a simple chart.",
})


QUIZ_BY_TOPIC.update({
    "java_language_foundations": ("What Java keyword marks a variable as a constant after assignment?", ["final"]),
    "java_bitwise_deep": ("Which Java right-shift operator fills with zero bits?", [">>>", "unsigned right shift"]),
    "java_control_flow": ("What loop form always runs its body at least once?", ["do while", "do-while"]),
    "java_methods_contracts": ("What does void mean in a Java method signature?", ["no return value", "returns nothing"]),
    "java_classes_constructors": ("What keyword refers to the current Java object?", ["this"]),
    "java_enums_exceptions": ("Are checked exceptions required to be caught or declared?", ["yes", "caught or declared"]),
    "java_encapsulation_invariants": ("What is a rule that must remain true for an object called?", ["invariant", "class invariant"]),
    "java_inheritance_polymorphism": ("What chooses the overridden method based on the runtime object?", ["dynamic dispatch", "runtime polymorphism"]),
    "java_abstract_interfaces": ("What Java construct defines a behavior contract implemented by classes?", ["interface"]),
    "java_equality_hashing": ("If equals says two objects are equal, what method must agree?", ["hashcode", "hashCode"]),
    "java_generics_hofs": ("What Java feature lets a class use a type parameter like T?", ["generics", "generic"]),
    "java_recursive_lists": ("What value usually marks the end of a linked list in Java?", ["null"]),
    "java_adts_collections": ("Which Java collection interface stores key-value pairs?", ["map"]),
    "java_design_patterns": ("Which pattern swaps interchangeable algorithms behind one interface?", ["strategy"]),
    "java_mvc": ("In MVC, which part owns domain state and rules?", ["model"]),
    "java_testing_debug_docs": ("What Java testing framework commonly uses @Test?", ["junit"]),
    "java_random_testing": ("Why use a fixed random seed in tests?", ["reproducible", "replay", "deterministic"]),
    "java_benchmarking": ("Which Java method should you use for elapsed benchmark timing?", ["nanoTime", "system.nanotime"]),
    "java_big_o": ("What complexity class describes binary search?", ["o log n", "log n", "O(log n)"]),
    "java_uml": ("In UML, what relationship represents a strong whole-part ownership?", ["composition"]),
    "java_packages_builds": ("What Java declaration groups a class into a namespace?", ["package"]),
    "c_systems_linux": ("What gcc flag includes debug symbols for gdb?", ["-g", "g"]),
    "c_foundations_headers": ("What file type usually declares C function prototypes?", ["header", ".h", "h file"]),
    "c_command_line_args": ("Which argv index holds the first user-supplied argument?", ["argv[1]", "1"]),
    "c_file_io": ("What does fopen return on failure?", ["null", "NULL"]),
    "c_pointers_memory": ("What C function releases heap memory?", ["free"]),
    "c_structs_types": ("What C keyword groups fields into a custom record?", ["struct"]),
    "c_debug_assembly": ("What debugger is commonly used for C programs on Linux?", ["gdb"]),
    "c_compilers_linkers": ("What build stage resolves symbols across object files?", ["linking", "linker"]),
    "c_function_pointers": ("What C standard library sort function takes a compare callback?", ["qsort"]),
    "c_bitwise_deep": ("What unsigned fixed-width header provides uint32_t?", ["stdint.h", "stdint"]),
    "c_processes_memory": ("Which memory region grows and shrinks as functions call and return?", ["stack"]),
    "c_concurrency_threads": ("What pthread primitive protects a critical section?", ["mutex", "pthread_mutex"]),
    "c_networking_sockets": ("Which server socket call waits for an incoming client connection?", ["accept"]),
    "c_linked_lists_deep": ("What must you do to every heap-allocated linked-list node when done?", ["free it", "free", "deallocate"]),
    "c_stacks_queues": ("Which ADT removes the oldest inserted item first?", ["queue"]),
    "c_algorithm_analysis_formal": ("What notation gives a tight asymptotic bound?", ["theta", "big theta", "Big-Theta"]),
    "c_benchmarking": ("Which clock should C benchmarks use to avoid wall-clock adjustments?", ["clock_monotonic", "CLOCK_MONOTONIC"]),
    "c_quadratic_sorts": ("Which quadratic sort is often efficient on nearly sorted data?", ["insertion sort"]),
    "c_random_testing": ("Why print the seed when a random test fails?", ["replay", "reproduce", "reproducible"]),
    "c_nlogn_sorts_proofs": ("What proof tool states what remains true each loop iteration?", ["loop invariant", "invariant"]),
    "c_trees_heaps": ("What BST invariant compares values in the left subtree to the node?", ["left less than node", "left < node", "smaller"]),
    "c_hash_tables": ("What hash-table metric usually triggers resizing?", ["load factor"]),
    "c_hash_algorithms": ("What hash property means small input changes affect many output bits?", ["avalanche", "avalanche effect"]),
    "c_graph_algorithms": ("Which graph algorithm finds shortest paths in unweighted graphs?", ["bfs", "breadth first search"]),
    "c_greedy": ("What property justifies making a locally optimal choice?", ["greedy choice property"]),
    "c_dynamic_programming_deep": ("What DP approach fills a table from base cases upward?", ["tabulation", "bottom up", "bottom-up"]),
    "c_recursion_divide_conquer": ("What three steps describe divide-and-conquer?", ["divide conquer combine", "divide, conquer, combine"]),
    "python_environment": ("What Python value represents no value?", ["none"]),
    "python_control_flow_deep": ("What Python statement is an explicit no-op placeholder?", ["pass"]),
    "python_functions_scope": ("What acronym describes Python name lookup order?", ["legb"]),
    "python_builtin_data_structures": ("Which Python built-in stores unique items?", ["set"]),
    "python_bitwise_deep": ("What Python integer method counts set bits?", ["bit_count", "bit count"]),
    "python_text_processing": ("What Python module provides regular expressions?", ["re"]),
    "python_file_io_data": ("What statement should you use so files close automatically?", ["with", "context manager"]),
    "python_error_handling": ("What keyword intentionally raises an exception?", ["raise"]),
    "python_oop_deep": ("What method initializes a Python object?", ["__init__", "init"]),
    "python_iterators_generators_decorators": ("What keyword makes a generator function produce values lazily?", ["yield"]),
    "python_modules_packages_envs": ("What file commonly records Python package dependencies?", ["requirements.txt", "requirements"]),
    "python_testing": ("What pytest feature supplies reusable test setup?", ["fixture", "fixtures"]),
    "python_test_automation": ("What subprocess.run argument prevents a hung program from blocking forever?", ["timeout"]),
    "python_benchmarking": ("What Python module is designed for repeatable microbenchmarks?", ["timeit"]),
    "python_random_testing": ("What random module function makes generated tests reproducible?", ["seed", "random.seed"]),
    "python_graph_algorithms": ("What Python module provides a min-heap priority queue?", ["heapq"]),
    "python_ai_ml_readiness": ("What Pandas object represents a table of rows and columns?", ["dataframe", "data frame"]),
})


AUDIT_EXAMPLE_SNIPPETS = {
    "java": {
        "bitwise": _clean_snippet("""
            public class Main {
                public static void main(String[] args) {
                    int READ = 4, WRITE = 2, EXEC = 1;
                    int flags = READ | WRITE;             // combine flags
                    System.out.println((flags & WRITE) != 0);
                    flags ^= EXEC;                        // toggle execute
                    System.out.println(flags);
                }
            }
        """),
        "pseudocode": _clean_snippet("""
            public class Main {
                public static void main(String[] args) {
                    int total = 0;
                    for (int i = 1; i <= 5; i++) {       // pseudo-code "1 to 5"
                        total += i;
                    }
                    System.out.println(total);            // 15
                }
            }
        """),
        "java_language_foundations": _clean_snippet("""
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
        """),
        "java_bitwise_deep": _clean_snippet("""
            final int READ = 1 << 2, WRITE = 1 << 1, EXEC = 1;
            int flags = READ | WRITE;
            boolean canWrite = (flags & WRITE) != 0;
            flags &= ~READ;                         // clear READ
            int logical = flags >>> 1;              // zero-fill right shift
            System.out.println(canWrite + " " + flags + " " + logical);
        """),
        "java_control_flow": _clean_snippet("""
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
        """),
        "java_methods_contracts": _clean_snippet("""
            /** Returns n!, precondition: n >= 0, postcondition: result >= 1. */
            static int factorial(int n) {
                if (n <= 1) return 1;               // base case
                return n * factorial(n - 1);        // recursive case
            }
        """),
        "java_classes_constructors": _clean_snippet("""
            class BankAccount {
                private int balance;
                BankAccount() { this(0); }
                BankAccount(int balance) { this.balance = balance; }
                void deposit(int amount) { balance += amount; }
                public String toString() { return "balance=" + balance; }
            }
        """),
        "java_enums_exceptions": _clean_snippet("""
            enum Status { NEW, PAID, SHIPPED }
            static Status ship(Status s) {
                if (s != Status.PAID) throw new IllegalStateException("pay first");
                return Status.SHIPPED;
            }
        """),
        "java_encapsulation_invariants": _clean_snippet("""
            final class Range {
                private final int start, end;        // invariant: start <= end
                Range(int start, int end) {
                    if (end < start) throw new IllegalArgumentException();
                    this.start = start; this.end = end;
                }
                boolean contains(int x) { return start <= x && x <= end; }
            }
        """),
        "java_inheritance_polymorphism": _clean_snippet("""
            abstract class Shape { abstract double area(); }
            class Circle extends Shape {
                double r; Circle(double r) { this.r = r; }
                @Override double area() { return Math.PI * r * r; }
            }
            Shape s = new Circle(2);                // upcast
            System.out.println(s.area());           // dynamic dispatch
        """),
        "java_abstract_interfaces": _clean_snippet("""
            interface Payable { int pay(); }
            abstract class Employee implements Payable { String name; }
            class Hourly extends Employee {
                int hours, rate;
                public int pay() { return hours * rate; }
            }
        """),
        "java_equality_hashing": _clean_snippet("""
            class Student {
                final int id;
                Student(int id) { this.id = id; }
                public boolean equals(Object o) {
                    return o instanceof Student s && id == s.id;
                }
                public int hashCode() { return Integer.hashCode(id); }
            }
        """),
        "java_generics_hofs": _clean_snippet("""
            static <T extends Comparable<T>> T max(T a, T b) {
                return a.compareTo(b) >= 0 ? a : b;
            }
            int total = java.util.List.of(1, 2, 3).stream()
                .filter(n -> n % 2 == 1).map(n -> n * n).reduce(0, Integer::sum);
        """),
        "java_recursive_lists": _clean_snippet("""
            interface IntList { int size(); }
            class Node implements IntList {
                int value; IntList rest;
                Node(int value, IntList rest) { this.value = value; this.rest = rest; }
                public int size() { return 1 + rest.size(); }
            }
            class Empty implements IntList { public int size() { return 0; } }
        """),
        "java_adts_collections": _clean_snippet("""
            Deque<Integer> stack = new ArrayDeque<>();
            Queue<Integer> queue = new ArrayDeque<>();
            Map<String, Integer> counts = new HashMap<>();
            stack.push(1); queue.add(1);
            counts.put("ai", counts.getOrDefault("ai", 0) + 1);
        """),
        "java_design_patterns": _clean_snippet("""
            interface DiscountStrategy { int apply(int cents); }
            class NoDiscount implements DiscountStrategy {
                public int apply(int cents) { return cents; }
            }
            class HalfOff implements DiscountStrategy {
                public int apply(int cents) { return cents / 2; }
            }
        """),
        "java_mvc": _clean_snippet("""
            class CounterModel { private int n; void inc() { n++; } int value() { return n; } }
            class CounterView { String render(int n) { return "Count: " + n; } }
            class CounterController {
                CounterModel model; CounterView view;
                String click() { model.inc(); return view.render(model.value()); }
            }
        """),
        "java_testing_debug_docs": _clean_snippet("""
            import org.junit.jupiter.api.Test;
            import static org.junit.jupiter.api.Assertions.*;
            class BankAccountTest {
                @Test void depositIncreasesBalance() {
                    BankAccount account = new BankAccount(10);
                    account.deposit(5);
                    assertEquals("balance=15", account.toString());
                }
            }
        """),
        "java_random_testing": _clean_snippet("""
            Random random = new Random(42);
            int[] values = new int[10];
            for (int i = 0; i < values.length; i++) {
                values[i] = random.nextInt(100);
            }
            Arrays.sort(values);
            System.out.println(Arrays.toString(values));
        """),
        "java_benchmarking": _clean_snippet("""
            int[] values = {5, 3, 1, 4, 2};
            long start = System.nanoTime();
            Arrays.sort(values);
            long end = System.nanoTime();
            double ms = (end - start) / 1_000_000.0;
            System.out.println(ms);
        """),
        "java_big_o": _clean_snippet("""
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
        """),
        "java_uml": _clean_snippet("""
            // UML text sketch:
            // Library *-- Book
            // Member --> Loan
            // LoanRepository ..> Loan
            // + public, - private, # protected
        """),
        "java_packages_builds": _clean_snippet("""
            // src/main/java/program/model/CounterModel.java
            package program.model;
            import java.util.Objects;
            // Gradle dependency example:
            // testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
        """),
    },
    "c": {
        "bitwise": _clean_snippet("""
            #include <stdio.h>
            int main(void) {
                unsigned READ = 4, WRITE = 2, EXEC = 1;
                unsigned flags = READ | WRITE;      /* combine */
                printf("%d\\n", (flags & WRITE) != 0);
                flags ^= EXEC;                      /* toggle */
                printf("%u\\n", flags);
                return 0;
            }
        """),
        "pseudocode": _clean_snippet("""
            #include <stdio.h>
            int main(void) {
                int total = 0;
                for (int i = 1; i <= 5; i++) {      /* pseudo-code "1 to 5" */
                    total += i;
                }
                printf("%d\\n", total);             /* 15 */
                return 0;
            }
        """),
        "c_systems_linux": _clean_snippet("""
            $ cat > hello.c
            #include <stdio.h>
            int main(void) { printf("hello\\n"); return 0; }
            $ gcc -Wall -Wextra -g -o hello hello.c
            $ ./hello > out.txt
        """),
        "c_foundations_headers": _clean_snippet("""
            /* math_utils.h */
            #ifndef MATH_UTILS_H
            #define MATH_UTILS_H
            int add(int a, int b);
            #endif
            /* main.c calls add(2, 3) and prints with printf("%d\\n", result). */
        """),
        "c_command_line_args": _clean_snippet("""
            int main(int argc, char **argv) {
                if (argc < 2) {
                    fprintf(stderr, "usage: %s <file>\\n", argv[0]);
                    return 1;
                }
                printf("program=%s file=%s\\n", argv[0], argv[1]);
                return 0;
            }
        """),
        "c_file_io": _clean_snippet("""
            FILE *fp = fopen(argv[1], "r");
            if (!fp) { perror(argv[1]); return 1; }
            char line[256];
            int lines = 0;
            while (fgets(line, sizeof line, fp) != NULL) {
                lines++;
            }
            fclose(fp);
            printf("%d\\n", lines);
        """),
        "c_pointers_memory": _clean_snippet("""
            void increment(int *p) { (*p)++; }
            int *value = malloc(sizeof *value);
            *value = 41;
            increment(value);
            printf("%d\\n", *value);   /* 42 */
            free(value);
        """),
        "c_structs_types": _clean_snippet("""
            typedef struct Node {
                int value;
                struct Node *next;
            } Node;
            Node *n = malloc(sizeof *n);
            n->value = 1; n->next = NULL;
            free(n);
        """),
        "c_debug_assembly": _clean_snippet("""
            $ gdb ./app
            (gdb) break main
            (gdb) run
            (gdb) next
            (gdb) print i
            (gdb) disassemble /m main
        """),
        "c_compilers_linkers": _clean_snippet("""
            $ gcc -E main.c -o main.i      # preprocess
            $ gcc -S main.i -o main.s      # compile to assembly
            $ gcc -c main.s -o main.o      # assemble
            $ gcc main.o util.o -o app     # link symbols into executable
        """),
        "c_function_pointers": _clean_snippet("""
            int add(int a, int b) { return a + b; }
            int mul(int a, int b) { return a * b; }
            typedef int (*op_t)(int, int);
            op_t ops[] = {add, mul};
            printf("%d\\n", ops[1](6, 7));  /* 42 */
        """),
        "c_bitwise_deep": _clean_snippet("""
            #include <stdint.h>
            uint32_t set_bit(uint32_t x, unsigned bit) { return x | (1u << bit); }
            uint32_t clear_bit(uint32_t x, unsigned bit) { return x & ~(1u << bit); }
            int test_bit(uint32_t x, unsigned bit) { return (x & (1u << bit)) != 0; }
            printf("%d\\n", test_bit(set_bit(0, 3), 3));
        """),
        "c_processes_memory": _clean_snippet("""
            int global_count;              /* BSS */
            int initialized = 3;           /* data */
            int main(void) {
                int local = 1;             /* stack */
                int *heap = malloc(sizeof *heap); /* heap */
                free(heap);
            }
        """),
        "c_concurrency_threads": _clean_snippet("""
            pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
            int counter = 0;
            void *worker(void *arg) {
                pthread_mutex_lock(&lock);
                counter++;
                pthread_mutex_unlock(&lock);
                return NULL;
            }
        """),
        "c_networking_sockets": _clean_snippet("""
            int fd = socket(AF_INET, SOCK_STREAM, 0);
            bind(fd, (struct sockaddr *)&addr, sizeof addr);
            listen(fd, 8);
            int client = accept(fd, NULL, NULL);
            recv(client, buffer, sizeof buffer, 0);
            send(client, "ok", 2, 0);
        """),
        "c_linked_lists_deep": _clean_snippet("""
            Node *insert_head(Node *head, int value) {
                Node *n = malloc(sizeof *n);
                n->value = value;
                n->next = head;
                return n;
            }
        """),
        "c_stacks_queues": _clean_snippet("""
            typedef struct { int items[8]; int top; } Stack;
            int push(Stack *s, int x) {
                if (s->top == 8) return 0;
                s->items[s->top++] = x;
                return 1;
            }
        """),
        "c_algorithm_analysis_formal": _clean_snippet("""
            for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                    work();
            /* n*n calls, so time is O(n^2), Omega(n^2), and Theta(n^2). */
        """),
        "c_benchmarking": _clean_snippet("""
            struct timespec start, end;
            clock_gettime(CLOCK_MONOTONIC, &start);
            run_algorithm();
            clock_gettime(CLOCK_MONOTONIC, &end);
            double seconds = (end.tv_sec - start.tv_sec)
                + (end.tv_nsec - start.tv_nsec) / 1e9;
            printf("%f\\n", seconds);
        """),
        "c_quadratic_sorts": _clean_snippet("""
            for (int i = 1; i < n; i++) {
                int x = a[i], j = i - 1;
                while (j >= 0 && a[j] > x) { a[j + 1] = a[j]; j--; }
                a[j + 1] = x;             /* insertion sort */
            }
        """),
        "c_random_testing": _clean_snippet("""
            srand(42);                     /* fixed seed for replay */
            int values[8];
            for (int i = 0; i < 8; i++) {
                values[i] = rand() % 100;
            }
            printf("seed=42 first=%d\\n", values[0]);
        """),
        "c_nlogn_sorts_proofs": _clean_snippet("""
            int partition(int a[], int lo, int hi) {
                int pivot = a[hi], i = lo;
                for (int j = lo; j < hi; j++)
                    if (a[j] <= pivot) swap(&a[i++], &a[j]);
                swap(&a[i], &a[hi]);
                return i;
            }
        """),
        "c_trees_heaps": _clean_snippet("""
            typedef struct Node { int key; struct Node *left, *right; } Node;
            Node *search(Node *root, int key) {
                if (!root || root->key == key) return root;
                return key < root->key ? search(root->left, key)
                                       : search(root->right, key);
            }
        """),
        "c_hash_tables": _clean_snippet("""
            unsigned hash(const char *s) {
                unsigned h = 5381;
                while (*s) h = h * 33u + (unsigned char)*s++;
                return h;
            }
            /* bucket = hash(key) % capacity; collisions go in a linked list. */
        """),
        "c_hash_algorithms": _clean_snippet("""
            uint32_t djb2(const char *s) {
                uint32_t hash = 5381u;
                while (*s) {
                    hash = ((hash << 5) + hash) + (unsigned char)*s++;
                }
                return hash;
            }
        """),
        "c_graph_algorithms": _clean_snippet("""
            int graph[4][4] = {{0,1,1,0},{0,0,0,1},{0,0,0,1},{0,0,0,0}};
            int queue[4], front = 0, back = 0, seen[4] = {1,0,0,0};
            queue[back++] = 0;             /* BFS starts at node 0 */
        """),
        "c_greedy": _clean_snippet("""
            typedef struct { int start, finish; } Activity;
            /* Sort by finish time, then choose the next activity whose start
               is >= the finish time of the last chosen activity. */
        """),
        "c_dynamic_programming_deep": _clean_snippet("""
            int dp[amount + 1];
            dp[0] = 0;
            for (int x = 1; x <= amount; x++) dp[x] = INF;
            for (int x = 1; x <= amount; x++)
                for (int i = 0; i < coin_count; i++)
                    if (coins[i] <= x) dp[x] = min(dp[x], 1 + dp[x - coins[i]]);
        """),
        "c_recursion_divide_conquer": _clean_snippet("""
            int binary_search(int a[], int lo, int hi, int target) {
                if (lo > hi) return -1;
                int mid = (lo + hi) / 2;
                if (a[mid] == target) return mid;
                if (a[mid] < target) return binary_search(a, mid + 1, hi, target);
                return binary_search(a, lo, mid - 1, target);
            }
        """),
    },
    "python": {
        "bitwise": _clean_snippet("""
            READ, WRITE, EXEC = 4, 2, 1
            flags = READ | WRITE            # combine flags
            print((flags & WRITE) != 0)     # test a flag
            flags ^= EXEC                   # toggle execute
            print(flags)
        """),
        "pseudocode": _clean_snippet("""
            total = 0
            for i in range(1, 6):           # pseudo-code "1 to 5" is inclusive
                total += i
            print(total)                    # 15
        """),
        "python_environment": _clean_snippet("""
            \"\"\"Small script demonstrating Python basics.\"\"\"
            n = 7
            ratio = 7 / 2
            floor = 7 // 2
            name = "Ryu"
            print(f"{name}: {n}, {ratio}, {floor}, truthy={bool(name)}, none={None}")
        """),
        "python_control_flow_deep": _clean_snippet("""
            command = "run"
            match command:
                case "run":
                    for i in range(5):
                        if i == 2: continue
                        if i == 4: break
                        print(i)
                case _:
                    pass
        """),
        "python_functions_scope": _clean_snippet("""
            def summarize(*nums: int, scale: int = 1, **labels: str) -> int:
                total = sum(nums) * scale
                print(labels.get("name", "total"), total)
                return total
            words = sorted(["pear", "fig", "apple"], key=lambda w: len(w))
        """),
        "python_builtin_data_structures": _clean_snippet("""
            squares = [n*n for n in range(5)]
            index = {value: i for i, value in enumerate(squares)}
            evens = {n for n in squares if n % 2 == 0}
            first, *rest = squares
            shallow = [rest, evens].copy()
        """),
        "python_bitwise_deep": _clean_snippet("""
            READ, WRITE, EXEC = 1 << 2, 1 << 1, 1
            flags = READ | WRITE
            can_write = (flags & WRITE) != 0
            flags &= ~READ                  # clear READ
            print(can_write, flags, bin(flags))
        """),
        "python_text_processing": _clean_snippet("""
            import re
            raw = " name: Ryu, score: 42 "
            parts = [p.strip() for p in raw.split(",")]
            print(" | ".join(parts))
            print(re.findall(r"\\d+", raw))
        """),
        "python_file_io_data": _clean_snippet("""
            import argparse, csv, json
            parser = argparse.ArgumentParser()
            parser.add_argument("input")
            args = parser.parse_args()
            with open(args.input, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            print(json.dumps(rows, indent=2))
        """),
        "python_error_handling": _clean_snippet("""
            class InvalidAgeError(ValueError): pass
            def parse_age(text: str) -> int:
                try:
                    age = int(text)
                    if age < 0: raise InvalidAgeError("age must be nonnegative")
                    return age
                except ValueError as exc:
                    raise InvalidAgeError("bad age") from exc
        """),
        "python_oop_deep": _clean_snippet("""
            from dataclasses import dataclass
            @dataclass(order=True, frozen=True)
            class Point:
                x: int
                y: int
                @property
                def manhattan(self) -> int:
                    return abs(self.x) + abs(self.y)
        """),
        "python_iterators_generators_decorators": _clean_snippet("""
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
        """),
        "python_modules_packages_envs": _clean_snippet("""
            # package layout:
            # program/__init__.py
            # program/main.py
            # requirements.txt
            if __name__ == "__main__":
                from program.main import main
                main()
        """),
        "python_testing": _clean_snippet("""
            import pytest
            @pytest.mark.parametrize("text,expected", [("1", 1), ("02", 2)])
            def test_parse_int(text, expected):
                assert int(text) == expected
            @pytest.fixture
            def sample_user():
                return {"name": "Ryu"}
        """),
        "python_test_automation": _clean_snippet("""
            import subprocess
            result = subprocess.run(
                ["./pascal", "10"], capture_output=True, text=True, timeout=5
            )
            passed = result.returncode == 0 and "252" in result.stdout
            print("PASS" if passed else "FAIL", result.stderr)
        """),
        "python_benchmarking": _clean_snippet("""
            import timeit
            elapsed = timeit.repeat(
                "sum(range(1000))", repeat=5, number=1000
            )
            print(min(elapsed))
        """),
        "python_random_testing": _clean_snippet("""
            import random
            random.seed(42)
            values = [random.randint(0, 100) for _ in range(10)]
            sorted_values = sorted(values)
            print(values, sorted_values == sorted(sorted_values))
        """),
        "python_graph_algorithms": _clean_snippet("""
            import heapq
            graph = {"A": [("B", 1), ("C", 4)], "B": [("C", 2)], "C": []}
            dist = {"A": 0}
            heap = [(0, "A")]
            while heap:
                d, node = heapq.heappop(heap)
                for neighbor, weight in graph[node]:
                    nd = d + weight
                    if nd < dist.get(neighbor, float("inf")):
                        dist[neighbor] = nd
                        heapq.heappush(heap, (nd, neighbor))
            print(dist["C"])
        """),
        "python_ai_ml_readiness": _clean_snippet("""
            import numpy as np
            import pandas as pd
            df = pd.DataFrame({"team": ["a", "a", "b"], "score": [1, 3, 5]})
            print(df.groupby("team")["score"].mean())
            vector = np.array(df["score"])
            print(vector * 2)
        """),
    },
}

for _language, _examples in AUDIT_EXAMPLE_SNIPPETS.items():
    EXAMPLE_SNIPPETS.setdefault(_language, {}).update(_examples)


AI_PRINCIPLES_CURRICULUM = {
    "llm_fundamentals": [
        {
            "title": "What LLMs Are Good At",
            "objective": "Understand the practical capabilities and limits of large language models.",
            "fundamentals": [
                "LLMs predict useful continuations from context; they are not databases, calculators, or proof engines by default.",
                "They are strong at language transformation, summarization, drafting, classification, code assistance, and pattern completion.",
                "They are weak when the task requires fresh facts, exact arithmetic, hidden state, strict guarantees, or unsupported private data.",
            ],
            "build": "List five tasks in one app and classify each as good for an LLM, needing tools, or better solved with normal code.",
            "quiz": ("What do LLMs primarily use to produce an answer at request time?", ["context", "prompt context", "prompt"]),
        },
        {
            "title": "Tokens, Context Windows, and Cost",
            "objective": "Learn the units that determine latency, cost, and what the model can see.",
            "fundamentals": [
                "Text is processed as tokens, not characters or words exactly.",
                "The context window is the maximum prompt plus output size the model can handle.",
                "Long prompts increase cost and latency, and can reduce answer quality if they contain irrelevant context.",
            ],
            "build": "Estimate the token budget for a support assistant: system prompt, conversation history, retrieved docs, and answer.",
            "quiz": ("What grows when you send a longer prompt to a paid model API?", ["cost", "latency", "tokens"]),
        },
        {
            "title": "Structured Output and Tool Calling",
            "objective": "Understand how models connect to software systems safely.",
            "fundamentals": [
                "Structured outputs make model responses easier to validate and consume in code.",
                "Tool calling lets a model request a narrow external action instead of pretending it knows the result.",
                "Schemas, validation, retries, and fallbacks are required because models can still produce invalid outputs.",
            ],
            "build": "Design a JSON schema for a task classifier with fields: category, priority, confidence, and rationale.",
            "quiz": ("What should you do before trusting model-generated JSON?", ["validate", "validation", "schema validation"]),
        },
        {
            "title": "Choosing Models",
            "objective": "Learn how to pick models based on task requirements instead of hype.",
            "fundamentals": [
                "Match the model to the task: reasoning, coding, extraction, latency, context length, privacy, and cost all matter.",
                "Small fast models are often enough for classification and extraction; stronger models help with complex reasoning.",
                "Use evaluation harnesses to compare models on your own tasks before switching production traffic.",
            ],
            "build": "Create a comparison table for three models with cost, latency, context length, quality, and deployment constraints.",
            "quiz": ("What should you use to compare models on your own workload?", ["harness", "evaluation", "eval", "evals"]),
        },
    ],
    "prompting": [
        {
            "title": "Instructions, Context, and Output Contracts",
            "objective": "Learn the three parts every reliable prompt needs.",
            "fundamentals": [
                "Instructions define the role, goal, constraints, and decision rules.",
                "Context supplies task-specific facts the model should use.",
                "The output contract defines format, fields, tone, length, and refusal behavior.",
            ],
            "build": "Rewrite a vague prompt into sections: task, constraints, context, output format, and examples.",
            "quiz": ("What part of a prompt defines the response format?", ["output contract", "format", "output format"]),
        },
        {
            "title": "Few-Shot Examples",
            "objective": "Understand when examples beat abstract instructions.",
            "fundamentals": [
                "Few-shot examples show the model exactly how inputs should map to outputs.",
                "Examples are especially useful for style, classification boundaries, and structured extraction.",
                "Bad or inconsistent examples can teach the wrong behavior.",
            ],
            "build": "Write three input/output examples for classifying support tickets by urgency.",
            "quiz": ("What do few-shot examples demonstrate?", ["input output mapping", "examples", "desired behavior"]),
        },
        {
            "title": "Context Management",
            "objective": "Learn how to keep prompts focused as applications grow.",
            "fundamentals": [
                "Do not send everything; send the smallest relevant context that supports the task.",
                "Summarize or retrieve old conversation history instead of blindly appending it forever.",
                "Separate durable instructions from volatile user data and retrieved facts.",
            ],
            "build": "Design a memory policy for a tutor: what to keep, summarize, retrieve, and discard.",
            "quiz": ("What kind of context should you prefer in a model prompt?", ["relevant", "focused", "small relevant context"]),
        },
        {
            "title": "Prompt Debugging",
            "objective": "Learn how to improve prompts systematically.",
            "fundamentals": [
                "Change one thing at a time and test against fixed examples.",
                "Prompt failures often come from missing constraints, ambiguous terms, conflicting instructions, or weak examples.",
                "A prompt is production code: version it, evaluate it, and review changes.",
            ],
            "build": "Take one failing prompt output and write a hypothesis, prompt change, and expected improvement.",
            "quiz": ("What should stay fixed while debugging prompt changes?", ["test cases", "examples", "evals"]),
        },
    ],
    "embeddings": [
        {
            "title": "What Embeddings Represent",
            "objective": "Understand embeddings as numeric representations of semantic similarity.",
            "fundamentals": [
                "An embedding maps text, images, or other content into a vector.",
                "Nearby vectors often represent similar meaning, even when exact words differ.",
                "Embeddings are useful for search, clustering, deduplication, recommendations, and RAG.",
            ],
            "build": "Write five pairs of queries/documents where keyword search might miss the semantic match.",
            "quiz": ("What does an embedding convert text into?", ["vector", "a vector", "numbers"]),
        },
        {
            "title": "Vector Databases and Indexes",
            "objective": "Learn why vector indexes exist and what metadata adds.",
            "fundamentals": [
                "A vector index makes nearest-neighbor search fast over many embeddings.",
                "Vector databases store vectors plus metadata and sometimes original text.",
                "Metadata filters let you restrict search by source, tenant, date, permission, language, or document type.",
            ],
            "build": "Design a vector record schema with id, text, embedding, source, timestamp, and permissions.",
            "quiz": ("What helps restrict vector search by source or permissions?", ["metadata", "filters", "metadata filters"]),
        },
        {
            "title": "Similarity, Recall, and Precision",
            "objective": "Understand retrieval quality tradeoffs.",
            "fundamentals": [
                "Recall means the right item appears somewhere in retrieved results.",
                "Precision means retrieved results are mostly relevant.",
                "Top-k, chunk size, filters, hybrid search, and reranking all affect recall and precision.",
            ],
            "build": "Create 10 search queries and label which chunks should appear in the top 5 results.",
            "quiz": ("What means the right result appears in the retrieved set?", ["recall"]),
        },
        {
            "title": "Reranking and Hybrid Search",
            "objective": "Learn how production retrieval improves beyond plain vector search.",
            "fundamentals": [
                "Hybrid search combines keyword and vector retrieval.",
                "Rerankers rescore candidate chunks for the specific query after broad retrieval.",
                "These steps often improve retrieval for exact names, numbers, code identifiers, and ambiguous queries.",
            ],
            "build": "Plan a two-stage search: retrieve 30 candidates, rerank them, then send the top 5 to the model.",
            "quiz": ("What combines keyword and vector retrieval?", ["hybrid search", "hybrid"]),
        },
    ],
    "rag": [
        {
            "title": "What RAG Solves",
            "objective": "Understand why retrieval-augmented generation exists and when it beats prompting alone.",
            "fundamentals": [
                "LLMs answer from model weights plus prompt context; they do not automatically know your private files.",
                "RAG retrieves relevant external context first, then asks the model to answer using that context.",
                "It is helpful for fresher facts, private knowledge, citations, and reducing unsupported answers.",
            ],
            "build": "Sketch a pipeline: user question -> retrieve matching notes -> place top passages in prompt -> generate answer with citations.",
            "quiz": ("What does the retrieval step add to the model prompt?", ["relevant context", "context", "documents", "passages"]),
        },
        {
            "title": "Documents, Chunks, and Metadata",
            "objective": "Learn how source material becomes searchable retrieval units.",
            "fundamentals": [
                "Documents are split into chunks because whole files are usually too large and too broad.",
                "Good chunks preserve meaning: headings, section boundaries, code blocks, and source metadata matter.",
                "Metadata such as filename, URL, date, owner, and topic helps filtering and citation.",
            ],
            "build": "Take one article, split it into 300-800 token chunks, and attach source/title/page metadata to each chunk.",
            "quiz": ("Why do RAG systems chunk documents?", ["too large", "fit context", "specific retrieval", "smaller pieces"]),
        },
        {
            "title": "Embeddings and Vector Search",
            "objective": "Understand how semantic retrieval finds similar meaning instead of exact words only.",
            "fundamentals": [
                "An embedding converts text into a vector that represents semantic meaning.",
                "Vector search compares vectors to find chunks near the user question.",
                "Keyword search and vector search are complementary; hybrid retrieval often works better than either alone.",
            ],
            "build": "Embed chunks, store vectors in a vector index, embed the question, then retrieve the nearest chunks.",
            "quiz": ("What does an embedding represent?", ["meaning", "semantic meaning", "text meaning", "vector meaning"]),
        },
        {
            "title": "Prompt Assembly and Grounding",
            "objective": "Learn how retrieved passages are turned into a grounded answer prompt.",
            "fundamentals": [
                "The prompt should separate instructions, user question, and retrieved context.",
                "Grounding means the answer should be based on supplied context, not unsupported guesses.",
                "Citations work best when each chunk keeps stable source metadata.",
            ],
            "build": "Write a prompt template with: role, rules, context block, question, and citation requirement.",
            "quiz": ("What should a grounded RAG answer be based on?", ["context", "retrieved context", "supplied context"]),
        },
        {
            "title": "Building a Minimal RAG App",
            "objective": "Understand the smallest working RAG implementation you can build yourself.",
            "fundamentals": [
                "Indexing path: load files, chunk text, embed chunks, store vectors and metadata.",
                "Query path: embed question, retrieve chunks, assemble prompt, call model, return answer.",
                "Start with a local JSON/SQLite store before adding a production vector database.",
            ],
            "build": "Create `ingest.py` and `ask.py`: one builds the index, the other retrieves context and calls local/cloud AI.",
            "quiz": ("Name one file/script in a minimal RAG project.", ["ingest", "ask", "ingest.py", "ask.py"]),
        },
        {
            "title": "RAG Quality and Failure Modes",
            "objective": "Learn how RAG fails and how to measure whether it is improving.",
            "fundamentals": [
                "Bad chunking, weak retrieval, stale data, and vague questions can all produce bad answers.",
                "Evaluate retrieval separately from generation: did the right evidence appear in top results?",
                "Track answer correctness, citation support, refusal behavior, and latency.",
            ],
            "build": "Create 10 question/expected-source pairs and check whether your retriever returns the right chunks.",
            "quiz": ("What should you evaluate separately from generation?", ["retrieval", "retriever", "retrieval quality"]),
        },
    ],
    "harnesses": [
        {
            "title": "What a Harness Is",
            "objective": "Understand harnesses as repeatable systems for running and judging AI behavior.",
            "fundamentals": [
                "A harness wraps a model, prompt, tool, or workflow so it can be tested repeatedly.",
                "It standardizes inputs, expected behavior, scoring, logging, and regression checks.",
                "Harnesses turn subjective demos into comparable engineering evidence.",
            ],
            "build": "Define a CSV/JSON test set with input, expected behavior, tags, and pass/fail criteria.",
            "quiz": ("What does a harness make repeatable?", ["tests", "evaluation", "runs", "model tests"]),
        },
        {
            "title": "Test Cases and Golden Sets",
            "objective": "Learn how to build a useful set of examples before automating scores.",
            "fundamentals": [
                "Golden sets contain representative inputs and expected outcomes.",
                "Include normal cases, edge cases, adversarial cases, and examples from real failures.",
                "Tags help you see whether regressions cluster around retrieval, safety, formatting, or reasoning.",
            ],
            "build": "Create 20 test cases for one assistant task and tag each case by skill or risk.",
            "quiz": ("What should a golden set contain besides normal cases?", ["edge cases", "adversarial cases", "failures"]),
        },
        {
            "title": "Scoring and Rubrics",
            "objective": "Understand exact, heuristic, and judge-based scoring.",
            "fundamentals": [
                "Exact match works for structured outputs, unit tests, and known answers.",
                "Heuristic checks can validate citations, JSON schema, forbidden phrases, or required fields.",
                "LLM-as-judge can help with fuzzy answers, but needs rubrics and calibration.",
            ],
            "build": "Write a rubric with 0/1/2 scores for correctness, groundedness, and format compliance.",
            "quiz": ("What kind of scoring is best for strict JSON fields?", ["exact", "exact match", "schema"]),
        },
        {
            "title": "Building an Evaluation Harness",
            "objective": "Learn the structure of a minimal AI eval harness.",
            "fundamentals": [
                "Runner: loops through test cases and calls the system under test.",
                "Scorer: grades each result using exact checks, rubrics, or judges.",
                "Reporter: saves results, failures, cost, latency, and diffs against prior runs.",
            ],
            "build": "Create `eval.py` that loads test cases, calls your app, scores outputs, and writes `results.json`.",
            "quiz": ("Name one core part of an eval harness.", ["runner", "scorer", "reporter"]),
        },
        {
            "title": "Regression Testing AI Systems",
            "objective": "Learn how harnesses protect prompts and workflows from silent degradation.",
            "fundamentals": [
                "AI changes can improve one behavior while breaking another.",
                "Regression runs compare current results to a previous baseline.",
                "Useful reports show failing examples first, not just aggregate scores.",
            ],
            "build": "Run the same test set before and after a prompt change and compare pass rate plus failed cases.",
            "quiz": ("What do regression runs compare against?", ["baseline", "previous run", "old results"]),
        },
    ],
    "agents": [
        {
            "title": "What Makes a Workflow Agentic",
            "objective": "Understand the difference between a single model call and an agentic loop.",
            "fundamentals": [
                "Agentic workflows let the system plan, use tools, inspect results, and decide next steps.",
                "They are useful when tasks need state, branching, iteration, or external actions.",
                "More autonomy increases the need for boundaries, logging, and evaluation.",
            ],
            "build": "Draw a loop: goal -> plan -> tool call -> observation -> decide -> final answer.",
            "quiz": ("What can an agentic workflow use besides the model?", ["tools", "tool calls", "external tools"]),
        },
        {
            "title": "Tools, State, and Memory",
            "objective": "Learn the building blocks that make agents useful and controllable.",
            "fundamentals": [
                "Tools expose narrow actions such as search, file read, code run, database query, or API call.",
                "State records what has happened so the workflow can continue coherently.",
                "Memory should be explicit and scoped; unbounded memory creates noise and privacy risk.",
            ],
            "build": "Define three tools for a research agent: search, open source, and summarize evidence.",
            "quiz": ("What records what has happened in a workflow?", ["state", "memory", "logs"]),
        },
        {
            "title": "Planning and Control Flow",
            "objective": "Understand linear chains, routers, loops, and supervisor patterns.",
            "fundamentals": [
                "Chains run fixed steps; routers choose a path; loops repeat until a condition is met.",
                "Supervisor patterns coordinate specialized workers but are harder to debug.",
                "Use the simplest control flow that can solve the task reliably.",
            ],
            "build": "Design a support workflow: classify issue -> retrieve docs -> draft answer -> verify citations.",
            "quiz": ("Which pattern chooses between multiple paths?", ["router", "routing"]),
        },
        {
            "title": "Guardrails and Observability",
            "objective": "Learn how to make agentic systems safer and easier to debug.",
            "fundamentals": [
                "Guardrails constrain tools, budgets, permissions, and output formats.",
                "Observability means logging prompts, tool calls, observations, costs, and failures.",
                "Human approval is useful for destructive actions or high-stakes decisions.",
            ],
            "build": "Add a rule that file writes require approval and every tool call is logged with inputs/outputs.",
            "quiz": ("What should destructive actions often require?", ["approval", "human approval"]),
        },
        {
            "title": "Building a Small Agent",
            "objective": "Learn a practical first agent architecture.",
            "fundamentals": [
                "Start with one goal, two or three tools, a max-steps limit, and clear success criteria.",
                "Keep tool schemas explicit so the model knows exactly what each tool can do.",
                "Evaluate the whole workflow with a harness, not just the final answer.",
            ],
            "build": "Build a CLI research agent with search/open/summarize tools and a five-step limit.",
            "quiz": ("What limit prevents an agent from looping forever?", ["max steps", "step limit", "budget"]),
        },
    ],
    "locallm": [
        {
            "title": "What Local LLMs Are",
            "objective": "Understand what runs locally and why you might choose it.",
            "fundamentals": [
                "A local LLM runs on your own machine instead of a cloud API.",
                "Benefits include privacy, offline use, lower marginal cost, and control over models.",
                "Tradeoffs include weaker models, hardware limits, setup work, and slower inference.",
            ],
            "build": "Install or open LM Studio, download a small instruct model, and run one chat locally.",
            "quiz": ("Name one benefit of a local LLM.", ["privacy", "offline", "cost", "control"]),
        },
        {
            "title": "Models, Quantization, and Context",
            "objective": "Learn the practical vocabulary for choosing a local model.",
            "fundamentals": [
                "Model size affects quality, memory use, and speed.",
                "Quantization compresses weights so models fit on consumer hardware.",
                "Context length controls how much prompt and history the model can consider.",
            ],
            "build": "Compare two local models by size, quantization, context length, and tokens per second.",
            "quiz": ("What does quantization help reduce?", ["memory", "size", "memory use"]),
        },
        {
            "title": "Serving a Local Model",
            "objective": "Understand how local apps connect to a local LLM server.",
            "fundamentals": [
                "Tools like LM Studio can expose an OpenAI-compatible HTTP endpoint.",
                "Your app sends messages to localhost and receives model completions.",
                "The endpoint, model name, timeout, and max tokens belong in configuration.",
            ],
            "build": "Start the LM Studio server and call `/v1/chat/completions` from a small script.",
            "quiz": ("Where does a local LLM server usually listen?", ["localhost", "local host", "127.0.0.1"]),
        },
        {
            "title": "Prompting and Tool Limits Locally",
            "objective": "Learn how local constraints change application design.",
            "fundamentals": [
                "Local models may need shorter prompts, clearer instructions, and smaller context.",
                "Some local models are weaker at tool calling or strict JSON than cloud models.",
                "Use validation, retries, and simpler schemas to compensate.",
            ],
            "build": "Create a prompt that asks for strict JSON, then validate and retry once if parsing fails.",
            "quiz": ("What should you do when local JSON output is unreliable?", ["validate", "retry", "validation"]),
        },
        {
            "title": "Building With Local LLMs",
            "objective": "Learn where local models fit into RAG, agents, and harnesses.",
            "fundamentals": [
                "Local models work well for drafts, classification, summarization, and private knowledge workflows.",
                "RAG can make smaller local models more useful by supplying focused context.",
                "Harnesses are essential because model quality varies widely across local models.",
            ],
            "build": "Build a local note-answering RAG prototype and evaluate it with 10 fixed questions.",
            "quiz": ("What technique can make a smaller local model more useful with private notes?", ["rag", "retrieval", "retrieval augmented generation"]),
        },
    ],
    "ml_basics": [
        {
            "title": "Supervised Learning Basics",
            "objective": "Understand the core training loop behind many ML systems.",
            "fundamentals": [
                "Supervised learning trains a model from labeled examples: inputs paired with target outputs.",
                "Training adjusts parameters to reduce loss on the training set.",
                "Validation data estimates whether the model generalizes beyond examples it memorized.",
            ],
            "build": "Define a toy spam classifier dataset with input text, label, train split, validation split, and metric.",
            "quiz": ("What data split estimates generalization during development?", ["validation", "validation set", "dev set"]),
        },
        {
            "title": "Loss, Metrics, and Baselines",
            "objective": "Learn how ML systems decide whether a model is improving.",
            "fundamentals": [
                "Loss is optimized during training; metrics express performance in business or task terms.",
                "Accuracy can hide failures on imbalanced data, so precision, recall, F1, ROC-AUC, or MAE may matter more.",
                "A baseline gives you a simple reference point before adding complexity.",
            ],
            "build": "Pick metrics for spam detection, fraud detection, price prediction, and support-ticket routing.",
            "quiz": ("What simple reference should you compare a new ML model against?", ["baseline", "a baseline"]),
        },
        {
            "title": "Overfitting and Generalization",
            "objective": "Understand why models can perform well in training and poorly in production.",
            "fundamentals": [
                "Overfitting means the model learns training quirks instead of reusable patterns.",
                "Generalization means the model works on new examples from the same real-world process.",
                "Regularization, more data, better splits, simpler models, and early stopping can reduce overfitting.",
            ],
            "build": "Sketch symptoms of overfitting by comparing training loss, validation loss, and test performance.",
            "quiz": ("What is it called when a model memorizes training quirks?", ["overfitting", "overfit"]),
        },
        {
            "title": "Data Leakage and Dataset Quality",
            "objective": "Learn one of the most common causes of misleading ML results.",
            "fundamentals": [
                "Data leakage occurs when training data includes information that would not be available at prediction time.",
                "Duplicates, bad labels, time leakage, target leakage, and biased sampling can ruin evaluation.",
                "Dataset quality often matters more than model complexity.",
            ],
            "build": "Review a hypothetical churn dataset and identify fields that might leak future information.",
            "quiz": ("What is it called when training uses information unavailable at prediction time?", ["data leakage", "leakage"]),
        },
    ],
    "data_engineering": [
        {
            "title": "Data Pipelines for AI",
            "objective": "Understand how raw data becomes usable training, retrieval, or evaluation data.",
            "fundamentals": [
                "AI systems depend on ingestion, parsing, cleaning, normalization, validation, and storage.",
                "Pipeline failures often show up as model failures later.",
                "Reliable pipelines are incremental, observable, replayable, and tested with bad inputs.",
            ],
            "build": "Design a pipeline that ingests PDFs, extracts text, validates metadata, chunks content, and stores records.",
            "quiz": ("What should a reliable data pipeline be able to do after a failure?", ["replay", "rerun", "resume"]),
        },
        {
            "title": "Labels, Features, and Ground Truth",
            "objective": "Learn how training and evaluation data get their meaning.",
            "fundamentals": [
                "Labels define what the model is supposed to learn or what an eval expects.",
                "Features are the input signals used by traditional ML models.",
                "Ground truth can be noisy, subjective, delayed, or expensive, so label quality must be measured.",
            ],
            "build": "Create labeling guidelines for classifying support tickets into billing, bug, account, or sales.",
            "quiz": ("What defines the target output for supervised learning?", ["label", "labels", "ground truth"]),
        },
        {
            "title": "Dataset Versioning and Lineage",
            "objective": "Understand how teams trace model behavior back to data changes.",
            "fundamentals": [
                "Dataset versioning records exactly which data went into training, evaluation, or indexing.",
                "Lineage tracks where data came from and which transformations changed it.",
                "Without lineage, debugging regressions becomes guesswork.",
            ],
            "build": "Define metadata for dataset version, source, transform version, timestamp, owner, and row count.",
            "quiz": ("What tracks where data came from and how it changed?", ["lineage", "data lineage"]),
        },
        {
            "title": "Data Quality Checks",
            "objective": "Learn the tests that prevent broken data from reaching models.",
            "fundamentals": [
                "Check schemas, null rates, duplicate rates, value ranges, distribution shifts, and permission constraints.",
                "RAG indexes need checks for empty chunks, bad encodings, missing source metadata, and stale documents.",
                "ML datasets need checks for label imbalance, leakage, duplicates across splits, and corrupted examples.",
            ],
            "build": "Write 10 validation checks for a document ingestion pipeline or classification dataset.",
            "quiz": ("What kind of examples across train/test splits can inflate model scores?", ["duplicates", "duplicate examples"]),
        },
    ],
    "transformers": [
        {
            "title": "Neural Networks in Plain Terms",
            "objective": "Understand the basic shape of deep learning before transformers.",
            "fundamentals": [
                "A neural network is a stack of parameterized transformations trained to reduce loss.",
                "Gradient descent updates parameters based on how much they contributed to error.",
                "Deep learning works well when there is enough data, compute, and structure to learn useful representations.",
            ],
            "build": "Draw input -> layers -> output -> loss -> gradient update for a classifier.",
            "quiz": ("What process updates model parameters to reduce loss?", ["gradient descent", "backpropagation", "training"]),
        },
        {
            "title": "Attention and Transformers",
            "objective": "Learn the key idea that made modern LLMs practical.",
            "fundamentals": [
                "Attention lets each token weigh information from other tokens in the context.",
                "Transformers stack attention and feed-forward layers to build contextual representations.",
                "This architecture scales well and supports parallel training better than older sequence models.",
            ],
            "build": "Explain how the word 'bank' changes meaning depending on nearby context.",
            "quiz": ("What mechanism lets tokens weigh other tokens in context?", ["attention", "self attention", "self-attention"]),
        },
        {
            "title": "Pretraining, Fine-Tuning, and Alignment",
            "objective": "Understand the main phases that produce useful AI assistants.",
            "fundamentals": [
                "Pretraining learns broad language patterns from large corpora.",
                "Fine-tuning adapts behavior to tasks, formats, or domains.",
                "Alignment methods improve helpfulness, safety, instruction following, and preference matching.",
            ],
            "build": "Classify examples as pretraining, supervised fine-tuning, preference tuning, or prompt engineering.",
            "quiz": ("Which phase learns broad language patterns from large corpora?", ["pretraining", "pre training"]),
        },
        {
            "title": "Fine-Tuning vs RAG vs Prompting",
            "objective": "Learn when to adapt the model and when to adapt the context.",
            "fundamentals": [
                "Prompting is best for quick behavior changes and low setup cost.",
                "RAG is best when answers need external or changing knowledge.",
                "Fine-tuning is best when you need repeated behavior, style, format, or task adaptation not solved by context alone.",
            ],
            "build": "Choose prompting, RAG, or fine-tuning for five scenarios and justify each choice.",
            "quiz": ("Which method is usually best for changing private or frequently updated knowledge?", ["rag", "retrieval"]),
        },
    ],
    "mlops": [
        {
            "title": "Serving AI Systems",
            "objective": "Understand what it means to deploy models and AI workflows.",
            "fundamentals": [
                "Serving turns a model or workflow into an API, batch job, CLI, or embedded app feature.",
                "Production systems need timeouts, retries, rate limits, fallbacks, and structured errors.",
                "Latency and cost are product constraints, not afterthoughts.",
            ],
            "build": "Design an API response shape for an AI endpoint including result, citations, latency, cost, and error fields.",
            "quiz": ("Name one production control for model API calls.", ["timeout", "retry", "rate limit", "fallback"]),
        },
        {
            "title": "Experiment Tracking and Versioning",
            "objective": "Learn how teams keep AI changes reproducible.",
            "fundamentals": [
                "Track datasets, prompts, model versions, hyperparameters, code commits, metrics, and eval results.",
                "Without versioning, you cannot explain why behavior changed.",
                "Prompt versions and retrieval index versions matter just like model versions.",
            ],
            "build": "Create a release checklist for a prompt/RAG change with versions and evaluation results.",
            "quiz": ("What do you need to explain why behavior changed?", ["versioning", "versions", "tracking"]),
        },
        {
            "title": "Monitoring and Drift",
            "objective": "Understand what to watch after deployment.",
            "fundamentals": [
                "Monitor latency, cost, errors, refusal rates, retrieval quality, user feedback, and task success.",
                "Data drift means production inputs differ from what the system was tested on.",
                "Silent quality regressions require sampled review, eval replay, and alerting.",
            ],
            "build": "Define five metrics for a production RAG assistant dashboard.",
            "quiz": ("What is it called when production inputs change from test data?", ["drift", "data drift"]),
        },
        {
            "title": "Human Review and Rollouts",
            "objective": "Learn how to ship AI features safely.",
            "fundamentals": [
                "Use staged rollouts, feature flags, shadow traffic, and human review for risky changes.",
                "High-stakes outputs may need approval before users see or act on them.",
                "Keep rollback paths simple because AI failures are often discovered from examples.",
            ],
            "build": "Plan a rollout for a customer-support AI feature from internal beta to full release.",
            "quiz": ("What lets you turn an AI feature off quickly?", ["feature flag", "rollback", "kill switch"]),
        },
    ],
    "safety": [
        {
            "title": "Threat Models for AI Apps",
            "objective": "Understand the main security risks unique to LLM applications.",
            "fundamentals": [
                "Prompt injection tries to override instructions or misuse connected tools.",
                "Data exfiltration tries to reveal secrets from prompts, files, tools, or retrieval context.",
                "Unsafe tool use can turn a text mistake into a real external action.",
            ],
            "build": "Write a threat model for a RAG assistant that can read private documents and send emails.",
            "quiz": ("What attack tries to override model instructions?", ["prompt injection", "injection"]),
        },
        {
            "title": "Permissions and Least Privilege",
            "objective": "Learn how to limit damage when AI systems call tools.",
            "fundamentals": [
                "Tools should have the narrowest permissions required for the task.",
                "Separate read-only tools from write/destructive tools.",
                "Require human approval for external side effects such as sending, deleting, buying, or publishing.",
            ],
            "build": "Classify tools in an agent as safe read-only, sensitive read, write, or destructive.",
            "quiz": ("What permission principle limits tool damage?", ["least privilege", "minimum privilege"]),
        },
        {
            "title": "Privacy and Data Governance",
            "objective": "Understand how data choices affect users, companies, and compliance.",
            "fundamentals": [
                "Do not send secrets, regulated data, or private user data to services that are not approved for that data.",
                "Log redaction and retention policies matter because prompts often contain sensitive context.",
                "RAG systems need access control so retrieval never exposes documents the user cannot see.",
            ],
            "build": "Design rules for what your AI tutor is allowed to log, retain, and send to cloud providers.",
            "quiz": ("What must RAG retrieval enforce for private documents?", ["access control", "permissions", "authorization"]),
        },
        {
            "title": "Bias, Reliability, and Responsible Use",
            "objective": "Learn practical engineering responsibilities around model behavior.",
            "fundamentals": [
                "Models can amplify bias from data, labels, prompts, and evaluation choices.",
                "Reliability means knowing when the system should answer, ask for clarification, refuse, or escalate.",
                "Responsible AI is implemented through product constraints, evaluation, monitoring, and user-facing transparency.",
            ],
            "build": "Add refusal/escalation rules for medical, legal, financial, and safety-critical questions.",
            "quiz": ("What should an AI system do when a task is high-stakes and uncertain?", ["escalate", "refuse", "ask for clarification"]),
        },
    ],
}


AI_AUDIT_APPENDIX = {}

AI_AUDIT_APPENDIX.update({
    "llm_fundamentals": [
        _ai_lesson(
            "Pretraining, SFT, and model families",
            "Understand how a raw foundation model becomes an assistant.",
            [
                "Pretraining learns broad language patterns from next-token prediction on massive corpora.",
                "Supervised fine-tuning adapts the base model to instruction-response pairs and domain tasks.",
                "Preference tuning and RLHF/GRPO push outputs toward helpful, safer, more preferred answers.",
                "Model families differ in quality, latency, context length, and deployment constraints.",
            ],
            "Map pretraining, SFT, and preference tuning to the right stage in a model lifecycle.",
            ("Which stage learns broad language patterns from large corpora?", ["pretraining"]),
            """
            base = pretrain(next_token_data)
            assistant = sft(base, instruction_pairs)
            aligned = preference_tune(assistant, ranked_answers)
            """,
        ),
        _ai_lesson(
            "Tokenization, context, and inference controls",
            "See how text becomes tokens and how sampling settings shape outputs.",
            [
                "Tokenization turns text into units such as BPE, SentencePiece, or WordPiece tokens.",
                "Context windows cap how much prompt and response history the model can attend to at once.",
                "Temperature, top-k, top-p, and repetition penalty control randomness and repetition.",
                "Long prompts cost more and can bury useful context in the middle of the window.",
            ],
            "Pick an inference setup for a concise assistant, a creative writer, and a code helper.",
            ("What parameter usually makes output more random?", ["temperature"]),
            """
            tokens = tokenizer.encode("explain vector search")
            logits = model(tokens, temperature=0.2, top_p=0.9)
            print(len(tokens), logits.sample())
            """,
        ),
        _ai_lesson(
            "Quantization and deployment tradeoffs",
            "Choose model sizes and numeric formats with the right latency-quality tradeoff.",
            [
                "Quantization compresses model weights to INT8, INT4, GPTQ, AWQ, or GGUF-style formats.",
                "Lower-bit models use less memory and can run on smaller hardware, but usually lose some quality.",
                "The right choice depends on privacy, cost, speed, and acceptable quality loss.",
                "Common families to know include GPT-4o, Claude, Llama, Mistral, Gemini, Qwen, and DeepSeek.",
            ],
            "Compare three deployment choices for a private assistant, a batch job, and a high-quality cloud workflow.",
            ("What is the main reason to quantize a model?", ["reduce memory", "reduce memory use", "fit hardware"]),
            """
            model = load_model("gguf", bits=4)
            print("lower memory, faster load, slight quality tradeoff")
            """,
        ),
    ],
    "prompting": [
        _ai_lesson(
            "Zero-shot, few-shot, and chain-of-thought",
            "Use examples and reasoning cues deliberately instead of hoping the model infers intent.",
            [
                "Zero-shot prompts rely on instructions alone.",
                "Few-shot prompts add examples that show the desired input-to-output pattern.",
                "Chain-of-thought prompting can improve reasoning on multi-step tasks.",
                "Self-consistency samples multiple reasoning paths and chooses the most stable answer.",
            ],
            "Rewrite one vague prompt three ways: zero-shot, few-shot, and reasoning-focused.",
            ("What does few-shot prompting add?", ["examples", "example pairs"]),
            """
            zero_shot = prompt("classify this ticket")
            few_shot = prompt("classify this ticket", examples=[...])
            cot = prompt("reason step by step, then answer")
            """,
        ),
        _ai_lesson(
            "System prompts, templates, and structured output",
            "Separate instructions, context, and output contracts so prompts stay reliable.",
            [
                "System prompts set role and policy, while user prompts carry the task request.",
                "Prompt templates keep variable injection consistent across repeated calls.",
                "Structured output can be JSON, XML, or a typed schema such as Pydantic.",
                "A good output contract defines fields, format, length, and refusal behavior.",
            ],
            "Turn a loose instruction into a role, context, and schema-based prompt.",
            ("What part of a prompt defines the response format?", ["output contract", "format", "schema"]),
            """
            system = "You are a concise tutor."
            user = "Return JSON with fields: answer, confidence, rationale."
            schema = {"answer": "string", "confidence": "number"}
            """,
        ),
        _ai_lesson(
            "ReAct, self-consistency, and injection defense",
            "Teach the model when to think, when to call tools, and how to resist hostile instructions.",
            [
                "ReAct interleaves reasoning and acting so the model can inspect results before continuing.",
                "Prompt injection tries to override instructions or manipulate tool use.",
                "Defensive prompting narrows tool authority and tells the model what not to trust.",
                "Majority voting and self-consistency help stabilize noisy answers.",
            ],
            "Write a prompt that uses tools only when needed and ignores untrusted instructions in retrieved text.",
            ("What attack tries to override the model's instructions?", ["prompt injection", "injection"]),
            """
            thought = plan(question)
            if need_tool(thought):
                result = call_tool(tool_schema)
            answer = synthesize(thought, result)
            """,
        ),
    ],
    "embeddings": [
        _ai_lesson(
            "Word, sentence, and document embeddings",
            "Understand how dense vectors represent meaning at different granularities.",
            [
                "Word embeddings capture local semantic relationships such as similarity and analogy.",
                "Sentence and document embeddings represent larger spans for retrieval and clustering.",
                "Dense vectors let semantically similar text sit near each other even when words differ.",
                "Embeddings are the backbone of vector search, RAG, recommendations, and deduplication.",
            ],
            "Explain why semantic search can find a relevant chunk that keyword search misses.",
            ("What does an embedding represent?", ["vector representation of meaning", "meaning vector", "dense vector"]),
            """
            query_vec = embed("how should I chunk documents?")
            doc_vec = embed("recursive chunking preserves headings")
            print(cosine(query_vec, doc_vec))
            """,
        ),
        _ai_lesson(
            "Similarity metrics and embedding model choices",
            "Choose the right metric and embedding model for the task you actually have.",
            [
                "Cosine similarity is common for semantic search; dot product and Euclidean distance appear in different stacks.",
                "Models such as Word2Vec, GloVe, sentence-transformers, E5, BGE, and CLIP cover different input types.",
                "Embedding dimensionality affects quality, cost, and index size.",
                "Batch embedding matters when you process large corpora or API-backed indexes.",
            ],
            "Decide which embedding family you would use for documents, code, and image-text retrieval.",
            ("Which metric is most common for semantic similarity?", ["cosine similarity", "cosine"]),
            """
            docs = embed_batch(chunks, batch_size=64)
            image_vec, text_vec = clip_embed(image, text)
            score = cosine(image_vec, text_vec)
            """,
        ),
    ],
    "ml_basics": [
        _ai_lesson(
            "Mathematical foundations for ML",
            "Cover the minimum math needed to read ML and AI engineering explanations confidently.",
            [
                "Vectors, matrices, dot products, and matrix multiplication are the language of model computations.",
                "Derivatives, gradients, and the chain rule explain how models learn from loss.",
                "Probability and Bayes' theorem describe uncertainty and conditional reasoning.",
                "Mean, variance, standard deviation, correlation, entropy, cross-entropy, and KL divergence show up in training and evaluation.",
            ],
            "Connect one math idea to a concrete ML use case such as loss gradients or similarity search.",
            ("What quantity tells gradient descent which way to change parameters?", ["gradient"]),
            """
            x = [1, 2, 3]
            w = [0.2, 0.5, 0.3]
            score = dot(x, w)
            grad = d_loss_d_w(score, target)
            """,
        ),
        _ai_lesson(
            "Core ML concepts and data splits",
            "Understand the basic training loop before choosing a model family.",
            [
                "Supervised learning uses labeled examples; unsupervised learning looks for structure without labels.",
                "Reinforcement learning learns from rewards and feedback rather than fixed labels.",
                "Training data, loss functions, optimizers, and learning rate form the core learning loop.",
                "Train/validation/test splits, cross-validation, and the bias-variance tradeoff protect against misleading metrics.",
            ],
            "Describe how you would split a small dataset and why the test set stays untouched.",
            ("Which split should stay untouched until the end?", ["test", "test set"]),
            """
            train, val, test = split(data, 0.7, 0.15, 0.15)
            model.fit(train.X, train.y)
            print(metric(model, val))
            """,
        ),
        _ai_lesson(
            "Classical supervised learning",
            "Learn the algorithm families that still matter in real ML systems.",
            [
                "Linear regression predicts continuous values, often with MSE as the training objective.",
                "Logistic regression maps features to class probabilities with a sigmoid decision boundary.",
                "Decision trees, random forests, and boosting methods capture nonlinear structure in tabular data.",
                "SVMs, k-nearest neighbors, and naive Bayes are still useful baselines and teaching tools.",
            ],
            "Pick one classical algorithm for regression, one for classification, and one for text.",
            ("Which algorithm is a common tabular baseline for classification?", ["logistic regression"]),
            """
            y_reg = linear_regression(X)
            y_cls = logistic_regression(X)
            tree = decision_tree.fit(X, y)
            """,
        ),
        _ai_lesson(
            "Unsupervised learning and anomaly detection",
            "See how clustering, dimensionality reduction, and outlier detection fit into AI workflows.",
            [
                "K-means and DBSCAN group similar examples without labels.",
                "PCA, t-SNE, and UMAP reduce dimensionality or reveal structure in high-dimensional data.",
                "Isolation forests and statistical methods help flag anomalies and unusual points.",
                "Unsupervised methods are useful when labels are missing or the goal is exploration.",
            ],
            "Choose an unsupervised method for clustering users, compressing embeddings, and finding outliers.",
            ("Which algorithm is commonly used for clustering?", ["k-means", "dbscan"]),
            """
            clusters = kmeans(X, k=4)
            low_dim = PCA(2).fit_transform(X)
            outliers = isolation_forest(X)
            """,
        ),
        _ai_lesson(
            "Evaluation metrics and model selection",
            "Choose metrics that actually match the problem and business goal.",
            [
                "Classification metrics include accuracy, precision, recall, F1, confusion matrix, ROC-AUC, and PR curves.",
                "Regression metrics include MSE, RMSE, MAE, and R^2.",
                "Class imbalance often requires oversampling, undersampling, SMOTE, or weighted loss.",
                "Comparing models should include confidence intervals or significance checks when decisions matter.",
            ],
            "Pick the right metric for spam filtering, churn, and price prediction.",
            ("Which metric is usually best for imbalanced binary classification?", ["f1", "precision recall", "pr auc"]),
            """
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            rmse = sqrt(mse(y, yhat))
            """,
        ),
        _ai_lesson(
            "Feature engineering and preprocessing",
            "Prepare data so simple models and deep models both get a fair shot.",
            [
                "Normalization, standardization, and scaling make numeric features comparable.",
                "Categorical variables often need one-hot, label, or target encoding.",
                "Missing data can be handled with imputation, deletion, or model-aware strategies.",
                "TF-IDF, bag-of-words, and EDA remain useful baselines before jumping to embeddings.",
            ],
            "Show how you would clean a mixed numeric/categorical dataset before training.",
            ("What is one common way to encode categorical variables?", ["one-hot", "label encoding", "target encoding"]),
            """
            X = standardize(X_num)
            X = one_hot(X_cat)
            X = impute_missing(X)
            """,
        ),
    ],
})

AI_AUDIT_APPENDIX.update({
    "transformers": [
        _ai_lesson(
            "Neural networks and deep learning foundations",
            "Understand the building blocks beneath modern LLMs.",
            [
                "Perceptrons and multi-layer perceptrons turn inputs into learned nonlinear features.",
                "Activations such as ReLU, sigmoid, tanh, and softmax make deep networks expressive.",
                "Backpropagation applies the chain rule to compute gradients layer by layer.",
                "Optimizers such as SGD, Adam, and AdamW turn gradients into parameter updates.",
            ],
            "Trace one forward pass and one backward pass through a tiny network.",
            ("What algorithm computes gradients through the network?", ["backpropagation", "backprop"]),
            """
            h = relu(W1 @ x + b1)
            yhat = softmax(W2 @ h + b2)
            loss.backward()
            """,
        ),
        _ai_lesson(
            "The transformer architecture",
            "Learn the core architecture that made modern LLMs practical.",
            [
                "Attention uses query, key, and value vectors to let tokens exchange information.",
                "Multi-head attention lets the model track several relationships at once.",
                "Positional encodings give the model a notion of token order.",
                "Decoder-only, encoder-only, and encoder-decoder families serve different tasks and training styles.",
            ],
            "Explain why attention beats a plain recurrent loop for large-context language modeling.",
            ("What vectors does attention use?", ["query key value", "q k v"]),
            """
            q, k, v = project(tokens)
            attn = softmax(q @ k.T / sqrt(d)) @ v
            """,
        ),
        _ai_lesson(
            "How large language models are trained",
            "Understand the full training story from pretraining to alignment.",
            [
                "Pretraining learns next-token prediction or masked language modeling from large corpora.",
                "Scaling laws describe how quality changes with data, compute, and parameter count.",
                "Instruction tuning and SFT convert a base model into a more useful assistant.",
                "RLHF and newer alignment methods improve preference following and safety.",
            ],
            "Explain how pretraining, SFT, and alignment differ in purpose and data shape.",
            ("Which stage usually uses instruction-response examples?", ["sft", "supervised fine-tuning"]),
            """
            base = pretrain(corpus)
            assistant = sft(base, instruction_pairs)
            aligned = rlhf_or_grpo(assistant)
            """,
        ),
        _ai_lesson(
            "Fine-tuning LLMs with PEFT",
            "Choose fine-tuning, prompting, or RAG with a production mindset.",
            [
                "Fine-tuning makes sense when the behavior should be repeated, specialized, or style-critical.",
                "PEFT dominates in practice because it adapts fewer parameters at lower cost.",
                "LoRA and QLoRA are the standard low-rank adaptation approaches most engineers should know.",
                "RAFT mixes retrieval and fine-tuning when both knowledge grounding and model adaptation matter.",
            ],
            "Pick one scenario where fine-tuning is better than prompting and one where RAG is better.",
            ("What does LoRA adapt?", ["low-rank adapters", "low rank adapters"]),
            """
            base = load_model("open-weights")
            adapt = lora(base, target_modules=["q_proj", "v_proj"])
            finetuned = qlora(base, rank=16)
            """,
        ),
    ],
    "rag": [
        _ai_lesson(
            "RAG architecture and why it exists",
            "Understand the core retrieve-augment-generate loop and where it fits.",
            [
                "RAG grounds an LLM in external evidence instead of relying only on model weights.",
                "The core loop is query, retrieve, augment, and generate.",
                "Naive, advanced, and modular RAG differ in how retrieval and orchestration are separated.",
                "RAG is useful when facts change, sources matter, or private data must stay outside model training.",
            ],
            "Compare RAG, fine-tuning, and long-context prompting for three different product needs.",
            ("What is the first step in the core RAG loop?", ["query"]),
            """
            q = user_question()
            chunks = retrieve(q)
            answer = generate(q, chunks)
            """,
        ),
        _ai_lesson(
            "Document ingestion, loaders, and chunking",
            "Turn raw documents into retrieval-ready chunks with useful metadata.",
            [
                "Loaders often need to handle PDF, HTML, Markdown, DOCX, CSV, and code files.",
                "Chunking can be fixed-size, recursive, sentence-based, or semantic.",
                "Metadata such as page number, section title, source, and timestamp make citations and filters work.",
                "Chunk size and overlap strongly affect retrieval quality and the lost-in-the-middle problem.",
            ],
            "Explain how you would split a long PDF into chunks without destroying headings and tables.",
            ("Why do RAG systems chunk documents?", ["fit context", "smaller retrieval units", "retrieval quality"]),
            """
            docs = load_pdf()
            chunks = chunk(docs, size=800, overlap=120)
            meta = {"page": 3, "source": "handbook"}
            """,
        ),
        _ai_lesson(
            "Embedding, indexing, and vector databases",
            "Store semantic representations so retrieval can scale beyond brute force.",
            [
                "Embedding models turn chunks into vectors and make semantic retrieval possible.",
                "Vector indexes and vector databases store vectors plus metadata for fast lookup and filtering.",
                "Approximate nearest-neighbor methods trade a little recall for major speed gains.",
                "Batch embedding, index choice, and dimensionality are cost and quality decisions, not afterthoughts.",
            ],
            "Describe what a vector DB stores that a normal relational DB does not optimize for.",
            ("Which structure speeds nearest-neighbor search?", ["vector index", "ann index", "hnsw", "ivf"]),
            """
            vecs = embed_batch(chunks)
            index = hnsw_upsert(vecs, metadata)
            print(index.search(query_vec))
            """,
        ),
        _ai_lesson(
            "Retrieval, reranking, and grounding",
            "Improve retrieval quality and keep the generated answer anchored to evidence.",
            [
                "Dense search, sparse search, and hybrid search solve different retrieval problems.",
                "Cross-encoder rerankers refine coarse retrieval candidates before generation.",
                "Prompt construction should separate instructions, question, and retrieved context clearly.",
                "Good grounding teaches the model to abstain when the context is insufficient.",
            ],
            "Write a retrieval stack that uses dense search, BM25, and reranking before generation.",
            ("What does hybrid search combine?", ["dense and sparse retrieval", "dense + sparse"]),
            """
            dense = vector_search(q)
            sparse = bm25(q)
            ranked = rerank(q, dense + sparse)
            """,
        ),
        _ai_lesson(
            "Advanced RAG, evaluation, and production",
            "Use advanced patterns and metrics to ship RAG responsibly.",
            [
                "GraphRAG, Self-reflective RAG, CRAG, RAPTOR, and Agentic RAG tackle harder retrieval problems.",
                "RAG evaluation tracks precision@k, recall@k, faithfulness, answer relevance, and context relevance.",
                "Production concerns include access control, incremental indexing, caching, latency, and observability.",
                "Agentic RAG uses query decomposition, validation, and specialized workers to improve hard queries.",
            ],
            "Name one advanced RAG pattern and one production concern you would monitor first.",
            ("Which RAG metric checks whether the answer follows the retrieved context?", ["faithfulness"]),
            """
            if not enough_context:
                ask_clarification()
            score = ragas(context, answer)
            log({"query": q, "score": score})
            """,
        ),
    ],
    "data_engineering": [
        _ai_lesson(
            "AI data pipelines",
            "See how raw inputs become training, retrieval, or evaluation data.",
            [
                "AI pipelines cover ingestion, parsing, cleaning, normalization, validation, and storage.",
                "Extraction can fail on tables, images, multi-column layouts, or malformed files.",
                "Incremental, observable, replayable pipelines are much easier to debug than ad hoc scripts.",
                "Pipeline quality strongly shapes model quality downstream.",
            ],
            "Sketch a pipeline that ingests PDFs, cleans text, and stores chunk records.",
            ("What should a reliable pipeline be able to do after a failure?", ["replay", "rerun", "resume"]),
            """
            raw = ingest(files)
            clean = normalize(raw)
            store(clean)
            """,
        ),
        _ai_lesson(
            "Labels, lineage, and versioning",
            "Keep track of what the model learned from and what changed over time.",
            [
                "Labels define target outputs for supervised learning or evaluation tasks.",
                "Ground truth can be noisy, delayed, or expensive, so labeling rules matter.",
                "Dataset versioning records exactly which data went into a model or index.",
                "Lineage tracks where the data came from and which transforms changed it.",
            ],
            "Define metadata you would attach to one dataset version and one transformed chunk set.",
            ("What tracks where data came from and how it changed?", ["lineage", "data lineage"]),
            """
            record = {"source": url, "version": "v3", "transform": "chunker-2"}
            audit_log(record)
            """,
        ),
        _ai_lesson(
            "Data quality and governance",
            "Add checks before broken data reaches models or retrieval indexes.",
            [
                "Validate schema, null rate, duplicate rate, ranges, and encoding before training or indexing.",
                "Check for leakage, duplicate examples across splits, and corrupted records.",
                "RAG systems need permissions and metadata checks so users cannot retrieve private material they should not see.",
                "Quality gates are much cheaper than debugging model behavior later.",
            ],
            "Write three quality checks for a document or tabular AI pipeline.",
            ("What kind of examples across train/test splits can inflate scores?", ["duplicates", "duplicate examples"]),
            """
            assert schema_ok(df)
            assert null_rate(df) < 0.01
            assert not leaked_rows(df)
            """,
        ),
    ],
})

AI_AUDIT_APPENDIX.update({
    "harnesses": [
        _ai_lesson(
            "Why evaluation matters",
            "Understand why AI engineering needs repeatable measurement.",
            [
                "Ad hoc testing makes results hard to compare and easy to fool yourself with.",
                "Evaluation should be a loop: measure, change, compare, and regressions-check.",
                "Benchmarks, online tests, and human review each answer different questions.",
                "Capability evals and safety evals should be separated, not blended together.",
            ],
            "Describe one AI change that should be measured before and after deployment.",
            ("Why should evaluation be repeatable?", ["reproducibility", "comparison", "regression detection"]),
            """
            before = run_eval(old_prompt)
            after = run_eval(new_prompt)
            compare(before, after)
            """,
        ),
        _ai_lesson(
            "Benchmarks and lm-evaluation-harness",
            "Know which benchmarks test what and how to run them in practice.",
            [
                "MMLU tests broad knowledge, HellaSwag tests commonsense, GSM8K tests grade-school math, and HumanEval tests code generation.",
                "IFEval and MT-Bench cover instruction following and multi-turn behavior.",
                "EleutherAI lm-evaluation-harness standardizes YAML tasks, model backends, and reporting.",
                "Writing a custom task and pinning config plus commit hash make benchmark runs reproducible.",
            ],
            "Pick one benchmark for knowledge, one for math, and one for code.",
            ("Which benchmark is commonly used for code generation?", ["humaneval"]),
            """
            lm_eval --model hf --tasks hellaswag,gsm8k --fewshot 5
            task = {"name": "custom_eval", "metrics": ["exact_match"]}
            """,
        ),
        _ai_lesson(
            "Metrics and LLM-as-judge",
            "Choose scoring methods that match the task and the amount of fuzziness involved.",
            [
                "Exact match and F1 work well for strict or extractive tasks.",
                "BLEU, ROUGE, METEOR, BERTScore, and pass@k cover different generation goals.",
                "LLM-as-judge is useful for subjective outputs but has biases like verbosity and position bias.",
                "Rubrics and reference answers make judge-based evals much more reliable.",
            ],
            "Decide which metric you would use for QA, summarization, and code generation.",
            ("What judge bias rewards longer answers?", ["verbosity bias"]),
            """
            score = judge(prompt, response, rubric)
            print({"f1": f1, "pass@k": pass_at_k, "judge": score})
            """,
        ),
        _ai_lesson(
            "RAG-specific evaluation and CI/CD tools",
            "Measure retrieval and grounding separately from the final response text.",
            [
                "RAGAS adds faithfulness, answer relevance, context precision, and context recall.",
                "Hallucination detection checks claims against retrieved evidence.",
                "DeepEval and Promptfoo make it easier to run AI tests inside CI/CD pipelines.",
                "Quality gates, dashboards, and synthetic test sets keep retrieval regressions visible.",
            ],
            "Write one test that checks retrieval and one that checks final-answer faithfulness.",
            ("Which metric checks how well retrieved context supports the answer?", ["faithfulness"]),
            """
            pytest -m eval
            promptfoo run
            record({"faithfulness": faith, "context_recall": recall})
            """,
        ),
        _ai_lesson(
            "Safety, red-teaming, and human evaluation",
            "Use adversarial testing and human review when automated metrics are not enough.",
            [
                "Safety evals include toxicity, stereotype, jailbreak, and harmful-output checks.",
                "Red-teaming intentionally probes failure modes and edge cases.",
                "Human evaluation needs rubrics, calibration, and inter-annotator agreement to be trusted.",
                "Some tasks should also enforce compliance and policy constraints such as GDPR or HIPAA.",
            ],
            "Design a small human-eval rubric for answer quality and safety.",
            ("What is one purpose of red-teaming?", ["find failure modes", "adversarial testing"]),
            """
            red_team(prompt)
            sample = annotate(pairwise_examples)
            report_kappa(sample)
            """,
        ),
    ],
    "agents": [
        _ai_lesson(
            "What makes AI agentic",
            "Understand the difference between a chatbot, a pipeline, and an agent.",
            [
                "An agent reasons, plans, acts, and observes outcomes in a loop.",
                "ReAct interleaves reasoning and acting so the model can inspect results.",
                "Agents are useful when task steps are open-ended, tool-heavy, or need adaptation.",
                "A simple prompt is still better when the workflow is small and predictable.",
            ],
            "Decide whether a task should be a prompt, pipeline, or agent.",
            ("What pattern interleaves reasoning and acting?", ["react", "reasoning and acting"]),
            """
            while not done:
                thought = plan(state)
                action = choose_tool(thought)
            """,
        ),
        _ai_lesson(
            "Tools and function calling",
            "Use schemas so the model can invoke tools reliably.",
            [
                "Tool definitions should include a name, a description, and a JSON schema for parameters.",
                "Function calling turns tool use into structured requests instead of free-form text guesses.",
                "Sequential and parallel tool calls each fit different workflows.",
                "Tool errors need retries, fallbacks, and clear failure handling.",
            ],
            "Design one tool schema for search and one for a database lookup.",
            ("What makes tool invocation reliable?", ["structured schema", "function calling", "json schema"]),
            """
            tool = {"name": "search", "parameters": {"query": "..."}}
            result = call_tool(tool)
            """,
        ),
        _ai_lesson(
            "MCP architecture and servers",
            "Connect AI systems to tools through the modern universal protocol.",
            [
                "MCP separates host, client, and server responsibilities over JSON-RPC 2.0.",
                "Tools, resources, prompts, and sampling are core MCP primitives.",
                "STDIO and Streamable HTTP cover local and remote transports.",
                "Building both a server and a client is part of practical AI engineering now.",
            ],
            "Explain how MCP differs from ad hoc tool wiring in one sentence.",
            ("What does MCP standardize?", ["tool connectivity", "ai-to-tool connectivity", "host client server messaging"]),
            """
            host -> client -> server
            tools = discover_tools(server)
            call(tool_name, args)
            """,
        ),
        _ai_lesson(
            "LangChain and LangGraph",
            "Use graph-based orchestration when an agent needs state and control flow.",
            [
                "LangChain covers prompts, chains, wrappers, and parsers.",
                "LangGraph adds nodes, edges, conditional routing, and durable state.",
                "Checkpointers, threads, and interrupt nodes make human-in-the-loop workflows possible.",
                "Subgraphs help you keep large workflows modular and debuggable.",
                "OpenAI Agents SDK, CrewAI, AutoGen, and smolagents are alternatives with different tradeoffs.",
            ],
            "Sketch one workflow that would be easier in LangGraph than in a single linear chain.",
            ("What LangGraph concept represents stateful routing?", ["nodes and edges", "graph", "conditional edges"]),
            """
            graph.add_node("plan", plan)
            graph.add_edge("plan", "tool")
            graph.add_conditional_edge("tool", router)
            """,
        ),
        _ai_lesson(
            "Memory and multi-agent systems",
            "Manage short-term and long-term memory, then coordinate several specialist agents.",
            [
                "Short-term memory holds the live conversation buffer and recent state.",
                "Long-term memory uses a vector store or database to recall past work.",
                "Multi-agent systems split work into roles such as planner, researcher, critic, and executor.",
                "Supervisor agents and handoffs keep specialization from turning into chaos.",
            ],
            "Describe one memory strategy and one role split for a research workflow.",
            ("Which memory store usually holds past interactions?", ["long-term memory", "vector store"]),
            """
            short_term.append(message)
            long_term = retrieve(query)
            next_agent = supervisor.route(task)
            """,
        ),
        _ai_lesson(
            "Agentic design patterns and production",
            "Ship agents that are observable, secure, and useful in real workflows.",
            [
                "Reflection, planning, routing, and tool augmentation are core agentic design patterns.",
                "Research agent, code agent, data analysis agent, RAG agent, browser agent, and workflow agent patterns are common applications.",
                "Observability tools such as LangSmith or LangFuse help debug loops and tool choices.",
                "Production agents need prompt-injection defense, permission scoping, retries, idempotency, and cost control.",
            ],
            "Pick one end-to-end agent project and list the tools, failure modes, and monitoring you would need.",
            ("What is one production safeguard for an agent?", ["permission scoping", "prompt injection defense", "idempotency"]),
            """
            planner -> researcher -> critic -> executor
            trace = langsmith.run(agent)
            enforce_permissions(tools)
            """,
        ),
    ],
})

for _module, _lessons in AI_AUDIT_APPENDIX.items():
    AI_PRINCIPLES_CURRICULUM[_module].extend(_lessons)


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    example_path = BASE / "config.example.json"
    if example_path.exists():
        with open(example_path) as f:
            return json.load(f)
    ui_box([f"No config.json found at {CONFIG_PATH}"], title="Configuration", color=ANSI.amber)
    sys.exit(1)


def load_profile() -> str:
    if PROFILE_PATH.exists():
        return PROFILE_PATH.read_text(encoding="utf-8")
    return "(No profile.md found. Create one for personalized analysis.)"


def load_deadlines() -> list:
    if DEADLINES_PATH.exists():
        with open(DEADLINES_PATH) as f:
            return json.load(f).get("deadlines", [])
    return []


def load_skills() -> dict:
    if SKILLS_PATH.exists():
        with open(SKILLS_PATH) as f:
            return json.load(f)
    return {}


# ── AnkiConnect ───────────────────────────────────────────────────────────

def _anki(action, params, cfg):
    try:
        r = requests.post(
            cfg["anki_connect_url"],
            json={"action": action, "version": 6, "params": params},
            timeout=10,
        )
        body = r.json()
        if body.get("error"):
            return None
        return body.get("result")
    except Exception:
        return None


def gather_anki(cfg) -> dict | None:
    version = _anki("version", {}, cfg)
    if version is None:
        return None

    due_ids = _anki("findCards", {"query": "is:due -is:learn"}, cfg) or []
    reviewed = _anki("getNumCardsReviewedToday", {}, cfg) or 0
    learning = len(_anki("findCards", {"query": "is:learn"}, cfg) or [])

    # Deck breakdown
    deck_names = _anki("deckNames", {}, cfg) or []
    decks = {}
    for d in deck_names:
        if d == "Default" and not _anki("findCards", {"query": f'deck:"{d}"'}, cfg):
            continue
        total = len(_anki("findCards", {"query": f'deck:"{d}"'}, cfg) or [])
        due = len(_anki("findCards", {"query": f'deck:"{d}" is:due'}, cfg) or [])
        if total > 0:
            decks[d] = {"total": total, "due": due}

    # Weak cards (leeches: high lapse count)
    leech_ids = _anki("findCards", {"query": "prop:lapses>3"}, cfg) or []
    weak_tags = {}
    if leech_ids:
        infos = _anki("cardsInfo", {"cards": leech_ids[:100]}, cfg) or []
        for card in infos:
            for tag in card.get("tags", []):
                weak_tags[tag] = weak_tags.get(tag, 0) + 1

    # Mature card count (interval > 21 days = well-learned)
    mature = len(_anki("findCards", {"query": "prop:ivl>21"}, cfg) or [])
    total_all = len(_anki("findCards", {"query": "deck:*"}, cfg) or [])

    return {
        "due": len(due_ids),
        "reviewed_today": reviewed,
        "learning": learning,
        "mature": mature,
        "total": total_all,
        "retention_approx": round(mature / total_all * 100, 1) if total_all else 0,
        "decks": decks,
        "weak_tags": sorted(weak_tags.items(), key=lambda x: -x[1])[:10],
        "leech_count": len(leech_ids),
    }


# ── Git Pulse ─────────────────────────────────────────────────────────────

def gather_git(cfg) -> list:
    repos = cfg.get("git_repos", [])
    results = []
    for repo in repos:
        path = os.path.expanduser(repo)
        if not os.path.isdir(os.path.join(path, ".git")):
            continue
        try:
            last = subprocess.run(
                ["git", "log", "-1", "--format=%ci|||%s"],
                cwd=path, capture_output=True, text=True, timeout=5,
            ).stdout.strip()
            week = subprocess.run(
                ["git", "rev-list", "--count", "--since=7.days", "HEAD"],
                cwd=path, capture_output=True, text=True, timeout=5,
            ).stdout.strip()
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=path, capture_output=True, text=True, timeout=5,
            ).stdout.strip()

            last_date, last_msg = "", ""
            if "|||" in last:
                parts = last.split("|||", 1)
                last_date = parts[0].strip()[:10]
                last_msg = parts[1].strip()

            days_since = 0
            if last_date:
                try:
                    ld = datetime.strptime(last_date, "%Y-%m-%d")
                    days_since = (datetime.now() - ld).days
                except ValueError:
                    pass

            results.append({
                "name": os.path.basename(path),
                "branch": branch or "main",
                "last_commit_date": last_date,
                "last_commit_msg": last_msg[:60],
                "week_commits": int(week) if week.isdigit() else 0,
                "days_since": days_since,
                "stale": days_since > 14,
            })
        except Exception:
            continue
    return results


# ── Calendar & Deadlines ──────────────────────────────────────────────────

def _read_apple_calendar(cfg) -> list:
    """Read upcoming events from Apple Calendar via osascript."""
    lookahead = cfg.get("calendar_lookahead_days", 30)
    script = f'''
tell application "Calendar"
    set output to ""
    set today to current date
    set future to today + {lookahead} * days
    repeat with cal in calendars
        set calName to name of cal
        try
            set evts to (every event of cal whose start date >= today and start date <= future)
            repeat with e in evts
                set n to summary of e
                set d to start date of e
                set yr to year of d as string
                set mo to text -2 thru -1 of ("0" & ((month of d as integer) as string))
                set dy to text -2 thru -1 of ("0" & ((day of d) as string))
                set hr to text -2 thru -1 of ("0" & ((hours of d) as string))
                set mn to text -2 thru -1 of ("0" & ((minutes of d) as string))
                set dateStr to yr & "-" & mo & "-" & dy & " " & hr & ":" & mn
                set nt to ""
                try
                    set nt to description of e
                end try
                if nt is missing value then set nt to ""
                set output to output & n & "|||" & dateStr & "|||" & calName & "|||" & nt & linefeed
            end repeat
        end try
    end repeat
    return output
end tell
'''
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return []

        events = []
        today = datetime.now().date()
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("|||")
            if len(parts) < 2:
                continue
            name = parts[0].strip()
            date_str = parts[1].strip()
            calendar = parts[2].strip() if len(parts) > 2 else ""
            notes = parts[3].strip() if len(parts) > 3 else ""

            try:
                event_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                event_date = event_dt.date()
            except ValueError:
                try:
                    event_date = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
                except ValueError:
                    continue

            days_left = (event_date - today).days
            events.append({
                "name": name,
                "date": date_str[:10],
                "time": date_str[11:] if len(date_str) > 10 else "",
                "calendar": calendar,
                "notes": notes,
                "days_left": days_left,
                "source": "calendar",
                "urgency": "overdue" if days_left < 0 else
                           "critical" if days_left <= 3 else
                           "soon" if days_left <= 7 else "normal",
            })
        return events
    except Exception:
        return []


def gather_deadlines(cfg) -> list:
    """Merge Apple Calendar events with manual deadlines.json entries."""
    # Calendar events
    cal_events = _read_apple_calendar(cfg)

    # Manual deadlines (fallback / supplemental)
    raw = load_deadlines()
    today = datetime.now().date()
    manual = []
    for d in raw:
        try:
            due = datetime.strptime(d["date"], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            continue
        days_left = (due - today).days
        if days_left < -7:
            continue
        manual.append({
            **d,
            "days_left": days_left,
            "source": "manual",
            "urgency": "overdue" if days_left < 0 else
                       "critical" if days_left <= 3 else
                       "soon" if days_left <= 7 else "normal",
        })

    all_events = cal_events + manual
    return sorted(all_events, key=lambda x: x["days_left"])


# ── Skills Gap ────────────────────────────────────────────────────────────

def gather_skills() -> dict:
    data = load_skills()
    if not data.get("skills"):
        return {}
    skills = []
    for name, vals in data["skills"].items():
        gap = vals["target"] - vals["level"]
        skills.append({
            "name": name,
            "level": vals["level"],
            "target": vals["target"],
            "gap": gap,
            "pct": round(vals["level"] / vals["target"] * 100) if vals["target"] else 100,
        })
    skills.sort(key=lambda x: -x["gap"])
    return {
        "target_role": data.get("target_role", ""),
        "skills": skills,
        "biggest_gaps": [s["name"] for s in skills if s["gap"] >= 2][:5],
    }


# ── API helpers ───────────────────────────────────────────────────────────

def _call_anthropic(system, user_msg, cfg, web_search=False, timeout=180):
    key = cfg.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return None
    payload = {
        "model": cfg.get("anthropic_model", "claude-sonnet-4-20250514"),
        "max_tokens": 16384,
        "system": system,
        "messages": [{"role": "user", "content": user_msg}],
    }
    if web_search:
        payload["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    r.raise_for_status()
    return "\n".join(
        b["text"] for b in r.json()["content"] if b.get("type") == "text"
    )


def _call_deepseek(system, user_msg, cfg, timeout=180):
    key = cfg.get("deepseek_api_key") or os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        return None
    r = requests.post(
        cfg.get("deepseek_endpoint", "https://api.deepseek.com/v1/chat/completions"),
        headers={
            "Authorization": f"Bearer {key}",
            "content-type": "application/json",
        },
        json={
            "model": cfg.get("deepseek_model", "deepseek-chat"),
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
            "temperature": 0.3,
            "max_tokens": 16384,
        },
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def _call_openai(system, user_msg, cfg, timeout=180):
    key = cfg.get("openai_api_key") or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return None
    r = requests.post(
        cfg.get("openai_endpoint", "https://api.openai.com/v1/chat/completions"),
        headers={
            "Authorization": f"Bearer {key}",
            "content-type": "application/json",
        },
        json={
            "model": cfg.get("openai_model", "gpt-4.1-mini"),
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
            "temperature": 0.3,
            "max_tokens": 4096,
        },
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def _call_local(system, user_msg, cfg, timeout=300):
    model = cfg.get("local_model", "")
    if not model:
        return None
    endpoint = cfg.get("local_endpoint", "http://localhost:1234/v1/chat/completions")
    r = requests.post(
        endpoint,
        headers={"content-type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
            "temperature": 0.3,
            "max_tokens": 16384,
        },
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


PROVIDER_LABELS = {
    "claude": "Claude",
    "openai": "OpenAI",
    "deepseek": "DeepSeek",
    "local": "Local (LM Studio)",
}


def _call_ai(system, user_msg, provider, cfg, web_search=False, timeout=180):
    """Route AI calls to the chosen provider."""
    if provider == "claude":
        return _call_anthropic(system, user_msg, cfg, web_search=web_search, timeout=timeout)
    elif provider == "openai":
        return _call_openai(system, user_msg, cfg, timeout=timeout)
    elif provider == "deepseek":
        return _call_deepseek(system, user_msg, cfg, timeout=timeout)
    elif provider == "local":
        return _call_local(system, user_msg, cfg, timeout=timeout)
    return None


def _parse_json_response(raw: str) -> dict | list | None:
    if not raw:
        return None
    text = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    decoder = json.JSONDecoder()
    for i, char in enumerate(text):
        if char not in "[{":
            continue
        try:
            parsed, _ = decoder.raw_decode(text[i:])
            return parsed
        except json.JSONDecodeError:
            continue
    # Try to find JSON object or array
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        i, j = text.find(start_char), text.rfind(end_char)
        if i != -1 and j != -1:
            try:
                return json.loads(text[i:j+1])
            except json.JSONDecodeError:
                fixed = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text[i:j+1])
                try:
                    return json.loads(fixed)
                except json.JSONDecodeError:
                    pass
    return None


def _escape(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _truncate(value, limit=220) -> str:
    text = re.sub(r"\s+", " ", "" if value is None else str(value)).strip()
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "..."


def _first_sentence(value, limit=180) -> str:
    text = re.sub(r"\s+", " ", "" if value is None else str(value)).strip()
    if not text:
        return ""
    match = re.search(r"(?<=[.!?])\s+", text)
    if match:
        text = text[:match.start()]
    return _truncate(text, limit)


# ── LeetCode practice catalog ─────────────────────────────────────────────

def load_leetcode_catalog() -> dict:
    if not LEETCODE_CATALOG_PATH.exists():
        return {"problems": [], "topics": [], "languages": ["python", "c", "java"]}
    with open(LEETCODE_CATALOG_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_leetcode_progress() -> dict:
    if LEETCODE_PROGRESS_PATH.exists():
        with open(LEETCODE_PROGRESS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {
        "completed_topics": {
            "python": [],
            "c": [],
            "java": [],
        },
        "completed_problems": {
            "python": [],
            "c": [],
            "java": [],
        },
    }


def save_leetcode_progress(progress: dict) -> None:
    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
    LEETCODE_PROGRESS_PATH.write_text(
        json.dumps(progress, indent=2) + "\n",
        encoding="utf-8",
    )


def _problem_key(problem: dict) -> tuple:
    difficulty_order = {"easy": 0, "medium": 1, "hard": 2}
    return (
        difficulty_order.get(problem.get("difficulty", ""), 9),
        problem.get("leetcode_number") or 99999,
        problem.get("title", ""),
    )


def _leetcode_problem_by_id(catalog: dict, problem_id: str) -> dict | None:
    needle = problem_id.strip().lower()
    for problem in catalog.get("problems", []):
        aliases = {
            str(problem.get("id", "")).lower(),
            str(problem.get("leetcode_number", "")).lower(),
            str(problem.get("slug", "")).lower(),
            str(problem.get("title", "")).lower(),
        }
        if needle in aliases:
            return problem
    return None


def _leetcode_is_unlocked(problem: dict, completed_topics: set[str]) -> bool:
    required = set(problem.get("prerequisite_topics", []))
    return required.issubset(completed_topics)


def _leetcode_status(problem: dict, language: str, progress: dict) -> str:
    completed = set(progress.get("completed_problems", {}).get(language, []))
    if problem.get("id") in completed:
        return "done"
    if language in problem.get("available_languages", []):
        return "local"
    return "catalog"


def _format_problem_line(problem: dict, language: str, progress: dict) -> str:
    topics = ", ".join(problem.get("topics", [])[:2])
    local = "local" if language in problem.get("available_languages", []) else "url"
    status = _leetcode_status(problem, language, progress)
    number = problem.get("leetcode_number") or "--"
    return (
        f"{problem['id']:<7} #{str(number):<4} "
        f"{problem['difficulty']:<6} {status:<7} {local:<5} "
        f"{problem['title']} [{topics}]"
    )


def _leetcode_filtered(args, catalog: dict, progress: dict) -> list[dict]:
    problems = catalog.get("problems", [])
    language = args.language
    completed_topics = set(progress.get("completed_topics", {}).get(language, []))
    completed_problems = set(progress.get("completed_problems", {}).get(language, []))

    if args.difficulty:
        problems = [p for p in problems if p.get("difficulty") == args.difficulty]
    if args.topic:
        problems = [p for p in problems if args.topic in p.get("topics", []) or args.topic in p.get("prerequisite_topics", [])]
    if args.unlocked:
        problems = [p for p in problems if _leetcode_is_unlocked(p, completed_topics)]
    if args.local_only:
        problems = [p for p in problems if language in p.get("available_languages", [])]
    if not args.include_done:
        problems = [p for p in problems if p.get("id") not in completed_problems]

    return sorted(problems, key=_problem_key)


def _read_local_problem(path: str) -> str:
    if not path:
        return ""
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def _extract_local_prompt(source: str) -> str:
    match = re.match(r'\s*"""(.*?)"""', source, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def handle_leetcode(args) -> None:
    catalog = load_leetcode_catalog()
    progress = load_leetcode_progress()
    language = getattr(args, "language", "python")

    if args.leetcode_cmd == "stats":
        problems = catalog.get("problems", [])
        done = set(progress.get("completed_problems", {}).get(language, []))
        completed_topics = progress.get("completed_topics", {}).get(language, [])
        local = sum(1 for p in problems if language in p.get("available_languages", []))
        print(f"  LeetCode catalog: {len(problems)} problems")
        print(f"  Language: {language}")
        print(f"  Local {language} solutions/stubs: {local}")
        print(f"  Completed problems: {len(done)}")
        print(f"  Completed topics: {', '.join(completed_topics) if completed_topics else '-'}")
        return

    if args.leetcode_cmd == "topics":
        completed = set(progress.get("completed_topics", {}).get(language, []))
        print(f"  Topics for {language}:")
        for topic in catalog.get("topics", []):
            mark = "✓" if topic in completed else " "
            print(f"  [{mark}] {topic}")
        return

    if args.leetcode_cmd == "topic-done":
        completed = progress.setdefault("completed_topics", {}).setdefault(language, [])
        changed = False
        for topic in args.topic:
            if topic not in completed:
                completed.append(topic)
                changed = True
        if changed:
            completed.sort()
            save_leetcode_progress(progress)
        print(f"  Completed topics for {language}: {', '.join(completed) if completed else '-'}")
        return

    if args.leetcode_cmd == "list":
        problems = _leetcode_filtered(args, catalog, progress)
        if args.limit:
            problems = problems[:args.limit]
        print(f"  Showing {len(problems)} problem(s) for {language}:")
        for problem in problems:
            print("  " + _format_problem_line(problem, language, progress))
        return

    if args.leetcode_cmd == "next":
        args.unlocked = True
        args.include_done = False
        args.local_only = False
        problems = _leetcode_filtered(args, catalog, progress)
        if not problems:
            print("  No unlocked unsolved problems yet. Mark more topics with `leetcode topic-done`.")
            return
        problem = problems[0]
        print("  Next problem:")
        print("  " + _format_problem_line(problem, language, progress))
        print(f"  {problem.get('url')}")
        if problem.get("local_path") and language in problem.get("available_languages", []):
            print(f"  Local file: {problem['local_path']}")
        return

    if args.leetcode_cmd == "show":
        problem = _leetcode_problem_by_id(catalog, args.problem)
        if not problem:
            print(f"  Problem not found: {args.problem}")
            return
        print(f"  {problem['id']} · #{problem.get('leetcode_number') or '--'} · {problem['title']} ({problem['difficulty']})")
        print(f"  URL: {problem.get('url')}")
        print(f"  Topics: {', '.join(problem.get('topics', []))}")
        print(f"  Required topics: {', '.join(problem.get('prerequisite_topics', [])) or '-'}")
        if problem.get("local_path"):
            print(f"  Local file: {problem['local_path']}")
            prompt = _extract_local_prompt(_read_local_problem(problem["local_path"]))
            if prompt:
                print("\n" + prompt)
        elif args.open:
            import webbrowser
            webbrowser.open(problem.get("url", ""))
        return

    if args.leetcode_cmd == "done":
        problem = _leetcode_problem_by_id(catalog, args.problem)
        if not problem:
            print(f"  Problem not found: {args.problem}")
            return
        completed = progress.setdefault("completed_problems", {}).setdefault(language, [])
        if problem["id"] not in completed:
            completed.append(problem["id"])
            completed.sort()
            save_leetcode_progress(progress)
        print(f"  Marked done for {language}: {problem['id']} {problem['title']}")
        return


# ── Interactive learning tutor ────────────────────────────────────────────

def build_learning_curriculum(language: str) -> list[dict]:
    lessons = []
    topics = list(LESSON_TOPICS) + list(AUDIT_LESSON_TOPICS.get(language, []))
    for i, (topic, title, objective) in enumerate(topics, 1):
        # Only show an example when one exists for this exact topic. Falling back
        # to an unrelated snippet (e.g. the variables example under "recursion")
        # is more confusing than showing none.
        example = EXAMPLE_SNIPPETS.get(language, {}).get(topic, "")
        quiz_q, answers = QUIZ_BY_TOPIC.get(topic, ("Type the main keyword or idea from this lesson.", [topic]))
        lessons.append({
            "day": i,
            "topic": topic,
            "title": title,
            "objective": objective,
            "quiz": quiz_q,
            "answers": answers,
            "example": example,
        })
    return lessons


def load_learning_progress() -> dict:
    if LEARNING_PROGRESS_PATH.exists():
        with open(LEARNING_PROGRESS_PATH, encoding="utf-8") as f:
            progress = json.load(f)
    else:
        progress = {
            "active_language": "",
            "active_track": "",
            "active_ai_module": "",
            "ai_provider": "",
            "local_model": "",
            "languages": {
                "python": {"completed_lessons": [], "completed_topics": [], "last_session": ""},
                "c": {"completed_lessons": [], "completed_topics": [], "last_session": ""},
                "java": {"completed_lessons": [], "completed_topics": [], "last_session": ""},
            },
            "ai_principles": {
                "llm_fundamentals": {"completed_lessons": [], "last_session": ""},
                "prompting": {"completed_lessons": [], "last_session": ""},
                "embeddings": {"completed_lessons": [], "last_session": ""},
                "rag": {"completed_lessons": [], "last_session": ""},
                "harnesses": {"completed_lessons": [], "last_session": ""},
                "agents": {"completed_lessons": [], "last_session": ""},
                "locallm": {"completed_lessons": [], "last_session": ""},
                "ml_basics": {"completed_lessons": [], "last_session": ""},
                "data_engineering": {"completed_lessons": [], "last_session": ""},
                "transformers": {"completed_lessons": [], "last_session": ""},
                "mlops": {"completed_lessons": [], "last_session": ""},
                "safety": {"completed_lessons": [], "last_session": ""},
            },
        }
    progress.setdefault("active_track", "")
    progress.setdefault("active_language", "")
    progress.setdefault("active_ai_module", "")
    progress.setdefault("ai_provider", "")
    progress.setdefault("local_model", "")
    progress.setdefault("theme", "dark")
    if "onboarding_complete" not in progress:
        progress["onboarding_complete"] = bool(progress.get("active_track"))
    languages = progress.setdefault("languages", {})
    for language in LEARN_LANGUAGES:
        languages.setdefault(language, {"completed_lessons": [], "completed_topics": [], "last_session": ""})
    ai_progress = progress.setdefault("ai_principles", {})
    for module in AI_MODULES:
        ai_progress.setdefault(module, {"completed_lessons": [], "last_session": ""})
    return progress


def save_learning_progress(progress: dict) -> None:
    PROGRESS_DIR.mkdir(parents=True, exist_ok=True)
    LEARNING_PROGRESS_PATH.write_text(
        json.dumps(progress, indent=2) + "\n",
        encoding="utf-8",
    )


def _prompt_choice(prompt: str, choices: dict[str, str], default: str | None = None) -> str:
    items = list(choices.items())
    lines = []
    for idx, (key, label) in enumerate(items, 1):
        suffix = "  default" if key == default else ""
        lines.append(f"[{idx}] {label}{suffix}")
    ui_box(lines, title=prompt.strip(), color=ANSI.cyan)
    while True:
        raw = ui_prompt()
        if not raw and default:
            return default
        if raw.isdigit():
            pick = int(raw)
            if 1 <= pick <= len(items):
                return items[pick - 1][0]
        if raw in choices:
            return raw
        ui_line("Pick one of: " + ", ".join(str(i) for i in range(1, len(items) + 1)), color=ANSI.amber)


def _normalise_answer(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _answer_matches(answer: str, accepted: list[str]) -> bool:
    got = _normalise_answer(answer)
    return any(got == _normalise_answer(a) or _normalise_answer(a) in got for a in accepted)


def _ensure_learning_language(progress: dict) -> str:
    language = progress.get("active_language")
    if language in LEARN_LANGUAGES:
        return language
    choice = _prompt_choice(
        "\nChoose a language to learn:",
        {"python": "Python", "c": "C", "java": "Java"},
        default="python",
    )
    progress["active_language"] = choice
    save_learning_progress(progress)
    return choice


def _ensure_learning_ai(progress: dict) -> str:
    provider = progress.get("ai_provider", "offline")
    if provider in LEARN_AI_PROVIDERS:
        return provider
    provider = _prompt_choice(
        "\nChoose AI assistance:",
        {"offline": "Offline only", "local": "Local AI (LM Studio)", "claude": "Claude", "openai": "OpenAI", "deepseek": "DeepSeek"},
        default="offline",
    )
    progress["ai_provider"] = provider
    save_learning_progress(progress)
    return provider


def _ensure_learning_track(progress: dict) -> str:
    track = progress.get("active_track")
    if track in LEARN_TRACKS:
        return track
    track = _prompt_choice(
        "\nChoose what you want to learn:",
        {"programming": "C, Python, or Java", "ai_principles": "Principles of AI"},
        default="programming",
    )
    progress["active_track"] = track
    save_learning_progress(progress)
    return track


def _ensure_ai_module(progress: dict) -> str:
    module = progress.get("active_ai_module")
    if module in AI_MODULES:
        return module
    module = _prompt_choice(
        "\nChoose a Principles of AI module:",
        AI_MODULES,
        default="rag",
    )
    progress["active_ai_module"] = module
    save_learning_progress(progress)
    return module


def _next_lesson(language: str, lang_progress: dict) -> dict | None:
    completed = set(lang_progress.get("completed_lessons", []))
    for lesson in build_learning_curriculum(language):
        if lesson["day"] not in completed:
            return lesson
    return None


def _ai_curriculum(module: str) -> list[dict]:
    lessons = []
    for i, lesson in enumerate(AI_PRINCIPLES_CURRICULUM[module], 1):
        lessons.append({"day": i, "module": module, **lesson})
    return lessons


def _next_ai_lesson(module: str, module_progress: dict) -> dict | None:
    completed = set(module_progress.get("completed_lessons", []))
    for lesson in _ai_curriculum(module):
        if lesson["day"] not in completed:
            return lesson
    return None


def _mark_topic_complete(language: str, topic: str, progress: dict) -> None:
    lang_progress = progress.setdefault("languages", {}).setdefault(
        language, {"completed_lessons": [], "completed_topics": [], "last_session": ""}
    )
    if topic not in lang_progress.setdefault("completed_topics", []):
        lang_progress["completed_topics"].append(topic)
        lang_progress["completed_topics"].sort()

    lc_progress = load_leetcode_progress()
    lc_topics = lc_progress.setdefault("completed_topics", {}).setdefault(language, [])
    topic_aliases = {
        "hash_maps": "arrays_hashing",
        "bitwise": "bit_manipulation",
        "c_bitwise_deep": "bit_manipulation",
        "java_bitwise_deep": "bit_manipulation",
        "python_bitwise_deep": "bit_manipulation",
    }
    mapped = topic_aliases.get(topic, topic)
    catalog_topics = set(load_leetcode_catalog().get("topics", []))
    if mapped in catalog_topics and mapped not in lc_topics:
        lc_topics.append(mapped)
        lc_topics.sort()
    save_leetcode_progress(lc_progress)


def _mark_ai_lesson_complete(module: str, lesson: dict, progress: dict) -> None:
    module_progress = progress.setdefault("ai_principles", {}).setdefault(
        module, {"completed_lessons": [], "last_session": ""}
    )
    if lesson["day"] not in module_progress.setdefault("completed_lessons", []):
        module_progress["completed_lessons"].append(lesson["day"])
        module_progress["completed_lessons"].sort()
    module_progress["last_session"] = datetime.now().strftime("%Y-%m-%d")
    save_learning_progress(progress)


def _mark_lesson_complete(language: str, lesson: dict, progress: dict) -> None:
    lang_progress = progress.setdefault("languages", {}).setdefault(
        language, {"completed_lessons": [], "completed_topics": [], "last_session": ""}
    )
    if lesson["day"] not in lang_progress.setdefault("completed_lessons", []):
        lang_progress["completed_lessons"].append(lesson["day"])
        lang_progress["completed_lessons"].sort()
    lang_progress["last_session"] = datetime.now().strftime("%Y-%m-%d")
    _mark_topic_complete(language, lesson["topic"], progress)
    save_learning_progress(progress)


def _unlocked_leetcode(language: str, limit: int = 5) -> list[dict]:
    catalog = load_leetcode_catalog()
    lc_progress = load_leetcode_progress()
    completed_topics = set(lc_progress.get("completed_topics", {}).get(language, []))
    completed = set(lc_progress.get("completed_problems", {}).get(language, []))
    problems = [
        p for p in catalog.get("problems", [])
        if p.get("id") not in completed and _leetcode_is_unlocked(p, completed_topics)
    ]
    return sorted(problems, key=_problem_key)[:limit]


def _provider_ready(provider: str, cfg: dict) -> bool:
    if provider == "offline":
        return True
    if provider == "local":
        return bool(cfg.get("local_model"))
    if provider == "claude":
        return bool(cfg.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY"))
    if provider == "openai":
        return bool(cfg.get("openai_api_key") or os.environ.get("OPENAI_API_KEY"))
    if provider == "deepseek":
        return bool(cfg.get("deepseek_api_key") or os.environ.get("DEEPSEEK_API_KEY"))
    return False


def _provider_model_key(provider: str) -> str:
    return AI_PROVIDER_MODEL_KEYS.get(provider, "")


def _raw_provider_model(provider: str, cfg: dict, progress: dict) -> str:
    key = _provider_model_key(provider)
    return "" if not key else str(progress.get(key) or cfg.get(key, "")).strip()


def _provider_model(provider: str, cfg: dict, progress: dict) -> str:
    model = _raw_provider_model(provider, cfg, progress)
    if provider == "deepseek":
        return _normalise_deepseek_model(model)
    return model


def _provider_model_display(provider: str, cfg: dict, progress: dict) -> str:
    model = _provider_model(provider, cfg, progress)
    if provider == "deepseek":
        return DEEPSEEK_MODELS.get(model, model)
    if provider in KNOWN_PROVIDER_MODELS:
        return KNOWN_PROVIDER_MODELS[provider].get(model, model)
    return model


def _provider_model_choices(provider: str, cfg: dict, progress: dict) -> dict[str, str]:
    if provider == "deepseek":
        models = _list_deepseek_models(cfg)
        return {
            model: f"{DEEPSEEK_MODELS.get(model, model)} ({model})"
            for model in models
        }
    if provider in KNOWN_PROVIDER_MODELS:
        return {
            model: f"{label} ({model})"
            for model, label in KNOWN_PROVIDER_MODELS[provider].items()
        }
    return {}


def _prompt_model_name(provider: str, cfg: dict, progress: dict) -> str:
    key = _provider_model_key(provider)
    if not key:
        return ""
    current = _provider_model(provider, cfg, progress)
    choices = _provider_model_choices(provider, cfg, progress)
    if not choices:
        return current
    default = current if current in choices else next(iter(choices))
    if current and current not in choices:
        ui_blank()
        ui_box(
            [f"Saved {LEARN_AI_PROVIDERS[provider]} model `{current}` is not in the available model list.",
             "Choose one of the supported IDs below."],
            title=f"{LEARN_AI_PROVIDERS[provider]} model",
            color=ANSI.amber,
        )
    model = _prompt_choice(f"\n{LEARN_AI_PROVIDERS[provider]} model:", choices, default=default)
    progress[key] = model
    return model


def _normalise_deepseek_model(model: str) -> str:
    model = model.strip()
    return DEEPSEEK_LEGACY_MODEL_ALIASES.get(model, model)


def _provider_alias_note(provider: str, cfg: dict, progress: dict) -> str:
    raw = _raw_provider_model(provider, cfg, progress)
    model = _provider_model(provider, cfg, progress)
    if provider == "deepseek" and raw and raw != model:
        return f"{raw} -> {model}"
    return "none" if model else ""


def _provider_identity_lines(provider: str, cfg: dict, progress: dict) -> list[str]:
    if provider == "offline":
        return ["AI: Offline only"]
    model_id = _provider_model(provider, cfg, progress)
    display = _provider_model_display(provider, cfg, progress)
    model_line = f"AI: {LEARN_AI_PROVIDERS[provider]} · Model ID: {model_id or '(none selected)'}"
    if display and display != model_id:
        model_line += f" · {display}"
    alias = _provider_alias_note(provider, cfg, progress)
    return [model_line, f"Alias: {alias or 'none'}"]


def _list_deepseek_models(cfg: dict) -> list[str]:
    key = cfg.get("deepseek_api_key") or os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        return list(DEEPSEEK_MODELS)
    endpoint = cfg.get("deepseek_endpoint", "https://api.deepseek.com/v1/chat/completions")
    base_url = endpoint.split("/v1/")[0].rstrip("/")
    try:
        response = requests.get(
            f"{base_url}/v1/models",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        models = [item.get("id", "") for item in data if item.get("id")]
        return models or list(DEEPSEEK_MODELS)
    except Exception:
        return list(DEEPSEEK_MODELS)


def _choose_deepseek_model(cfg: dict, progress: dict) -> str:
    key = "deepseek_model"
    current = _normalise_deepseek_model(_provider_model("deepseek", cfg, progress))
    choices = _provider_model_choices("deepseek", cfg, progress)
    default = current if current in choices else "deepseek-v4-flash"
    if current and current not in choices:
        ui_blank()
        ui_box(
            [f"Saved DeepSeek model `{current}` is not in the available model list.",
             "Choose one of the supported IDs below."],
            title="DeepSeek model",
            color=ANSI.amber,
        )
    model = _prompt_choice("\nDeepSeek model:", choices, default=default)
    progress[key] = model
    return model


def _configure_provider_model(provider: str, cfg: dict, progress: dict) -> None:
    if provider == "local":
        model = _choose_local_model(cfg, progress.get("local_model", ""))
        if model:
            progress["local_model"] = model
        return
    if provider == "deepseek":
        _choose_deepseek_model(cfg, progress)
        return
    if provider in ("claude", "openai"):
        _prompt_model_name(provider, cfg, progress)


def _ensure_provider_model_choice(provider: str, cfg: dict, progress: dict) -> None:
    if provider == "deepseek":
        current = _provider_model("deepseek", cfg, progress)
        if current not in _list_deepseek_models(cfg):
            _choose_deepseek_model(cfg, progress)
        elif _raw_provider_model("deepseek", cfg, progress) != current:
            progress["deepseek_model"] = current
    elif provider in ("claude", "openai"):
        current = _provider_model(provider, cfg, progress)
        allowed = KNOWN_PROVIDER_MODELS.get(provider, {})
        if not current or current not in allowed:
            _prompt_model_name(provider, cfg, progress)
    elif provider == "local" and not progress.get("local_model"):
        _learning_local_model(progress, cfg, prompt_if_missing=True)


def _apply_progress_models(cfg: dict, progress: dict) -> dict:
    merged = dict(cfg)
    for key in AI_PROVIDER_MODEL_KEYS.values():
        if progress.get(key):
            merged[key] = _normalise_deepseek_model(progress[key]) if key == "deepseek_model" else progress[key]
    return merged


def _choose_local_model(cfg: dict, current: str = "") -> str:
    """Let the learner pick (or change) the local model.

    Lists models from LM Studio's server when reachable, marks the current one,
    and only accepts numbered choices or Enter to keep the current choice.
    Returns the chosen model name (or current/"").
    """
    models = _list_lm_studio(cfg)
    ui_blank()
    if models:
        lines = [f"[{idx}] {model}{'  (current)' if model == current else ''}" for idx, model in enumerate(models, 1)]
        if current and current not in models:
            lines.append(f"Current: {current}  (not in the server's list)")
        lines.append("Pick a number, or press Enter to keep the current model.")
        ui_box(lines, title="Choose a local model", color=ANSI.cyan)
    else:
        ui_box(
            ["No models found from LM Studio's local server.",
             "Start LM Studio and load a model before selecting local AI.",
             f"Current model: {current or '(none)'}"],
            title="Choose a local model", color=ANSI.amber,
        )
    while True:
        raw = _read_line("> ").strip()
        if not raw:
            return current
        if raw.isdigit():
            if models and 1 <= int(raw) <= len(models):
                return models[int(raw) - 1]
            ui_line(f"Pick a number 1-{len(models)}.", color=ANSI.amber)
            continue
        ui_line("Model names must come from LM Studio's loaded model list.", color=ANSI.amber)


def _learning_local_model(progress: dict, cfg: dict, prompt_if_missing: bool = True) -> str:
    model = progress.get("local_model") or cfg.get("local_model", "")
    if model:
        return model
    if not prompt_if_missing:
        return ""
    model = _choose_local_model(cfg)
    if model:
        progress["local_model"] = model
        save_learning_progress(progress)
    else:
        ui_box(["No LM Studio models found.", "Start LM Studio's local server, then choose Settings again."], title="Local model", color=ANSI.amber)
    return model


def _prepare_ai_cfg(provider: str, cfg: dict, progress: dict) -> tuple[dict, str | None]:
    """Resolve config for a learning AI call. Returns (cfg, error_message_or_None)."""
    if provider == "offline":
        return cfg, "AI assistance is set to offline. Change AI settings from the Learn menu to use local or cloud help."
    local_cfg = _apply_progress_models(cfg, progress)
    if provider == "local":
        local_model = _learning_local_model(progress, cfg, prompt_if_missing=True)
        if not local_model:
            return local_cfg, "No local model is selected. Open Settings and choose a local model first."
        local_cfg["local_model"] = local_model
    if not _provider_ready(provider, local_cfg):
        return local_cfg, f"{LEARN_AI_PROVIDERS[provider]} is not ready. Check your model/API key, or switch AI settings."
    return local_cfg, None


def _learning_ai_response(provider: str, question: str, subject: str, cfg: dict, progress: dict, context: str = "") -> str:
    local_cfg, error = _prepare_ai_cfg(provider, cfg, progress)
    if error:
        return error
    system = (
        "You are a concise technical tutor for a beginner. "
        "Explain the idea, give one small practical example, and avoid doing the learner's exercise unless asked. "
        "Keep the answer under 180 words."
    )
    user_msg = f"Subject: {subject}\nContext: {context}\nQuestion: {question}"
    try:
        return _call_ai(system, user_msg, provider, local_cfg, timeout=120) or "No AI response."
    except Exception as exc:
        return f"AI request failed: {exc}"


def _grade_answer(provider: str, question: str, answer: str, accepted: list[str],
                  subject: str, cfg: dict, progress: dict, context: str = "") -> tuple[bool, str]:
    """Judge a learner's short answer.

    Hard accepted-answer matching runs first for trust and speed. A live AI
    provider is only used for ambiguous wording that the deterministic check
    could not accept.
    """
    if _answer_matches(answer, accepted):
        return True, "Hard check passed: matched the expected concept."

    local_cfg, error = _prepare_ai_cfg(provider, cfg, progress)
    if error:
        # Offline or provider not ready: fall back to keyword matching, no prose.
        return False, ""
    system = (
        "You are grading a beginner's short answer to a concept question. "
        "Decide whether the learner's answer is essentially correct, even if it is "
        "worded differently, partial, or uses synonyms, as long as the core idea is right. "
        "Return ONLY valid JSON, no markdown fences: "
        '{"correct": true or false, "feedback": "one or two sentences"}. '
        "If incorrect, the feedback should gently point toward the right idea without "
        "simply restating the reference answer verbatim. If correct, briefly affirm it."
    )
    user_msg = (
        f"Subject: {subject}\n"
        f"Context: {context}\n"
        f"Question: {question}\n"
        f"Reference correct answer(s): {', '.join(accepted)}\n"
        f"Learner's answer: {answer}"
    )
    try:
        raw = _call_ai(system, user_msg, provider, local_cfg, timeout=60)
        data = _parse_json_response(raw or "")
        if isinstance(data, dict) and "correct" in data:
            return bool(data["correct"]), str(data.get("feedback", "")).strip()
    except Exception:
        pass
    return _answer_matches(answer, accepted), ""


def _show_ai_feedback(response: str, title: str = "Tutor") -> None:
    ui_blank()
    ui_box(response.splitlines() or ["No response."], title=title, color=ANSI.cyan)
    ui_blank()
    ui_line("Press Enter to continue.", color=ANSI.dim)
    _read_line()


def _read_code_block(language: str | None = None) -> str:
    """In-app multi-line code editor with full arrow-key navigation.

    Uses prompt_toolkit so the learner can move up/down between lines and edit
    freely (with syntax highlighting when pygments is available). Falls back to
    a simple line reader when prompt_toolkit is missing or there is no terminal.
    """
    code = _read_code_block_ptk(language)
    return _read_code_block_inline(language) if code is None else code


def _read_code_block_ptk(language: str | None = None) -> str | None:
    """Framed multi-line code editor. Returns the code, or None if unusable.

    Draws a bordered box around the typing area (matching the rest of the UI)
    with line numbers and syntax highlighting, full arrow-key navigation, and
    Tab to indent.
    """
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        return None
    try:
        from prompt_toolkit.application import Application
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.layout import Layout
        from prompt_toolkit.layout.containers import HSplit, VSplit, Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.dimension import Dimension
        from prompt_toolkit.widgets import Frame, TextArea
    except ImportError:
        return None

    lexer = None
    try:  # syntax highlighting is a nice-to-have, not required
        from prompt_toolkit.lexers import PygmentsLexer
        from pygments.lexers import CLexer, JavaLexer, PythonLexer
        lex = {"python": PythonLexer, "c": CLexer, "java": JavaLexer}.get(language or "")
        if lex:
            lexer = PygmentsLexer(lex)
    except Exception:
        lexer = None

    lang_label = LEARN_LANGUAGES.get(language or "", "")
    box_width = min(84, _term_width() - 8)
    left = max(0, (shutil.get_terminal_size((96, 24)).columns - box_width) // 2)

    text_area = TextArea(
        multiline=True,
        line_numbers=True,
        scrollbar=True,
        wrap_lines=False,
        lexer=lexer,
        width=Dimension.exact(box_width - 2),
        height=Dimension(min=6, preferred=14),
    )

    result: dict[str, str | None] = {"text": ""}

    bindings = KeyBindings()

    @bindings.add("c-s")
    @bindings.add("escape", "enter")
    def _(event):
        result["text"] = text_area.text
        event.app.exit()

    @bindings.add("c-c")
    def _(event):
        result["text"] = None  # cancelled
        event.app.exit()

    @bindings.add("tab")
    def _(event):
        text_area.buffer.insert_text("    ")

    title = "Code editor" + (f" ({lang_label})" if lang_label else "")
    help_line = Window(
        FormattedTextControl(" Esc+Enter / Ctrl+S submit · Tab indent · arrows move · Ctrl+C cancel"),
        height=1, width=Dimension.exact(box_width),
    )
    body = VSplit([Window(width=Dimension.exact(left)), HSplit([Frame(text_area, title=title), help_line])])
    app: Application = Application(
        layout=Layout(body, focused_element=text_area),
        key_bindings=bindings,
        mouse_support=True,
        full_screen=False,
    )
    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        return ""
    text = result["text"]
    return "" if text is None else text.strip("\n")


def _read_code_block_inline(language: str | None = None) -> str:
    """Fallback line-by-line reader for when no editor/TTY is available.

    Enter inserts a new line; submission is an explicit command so writing code
    works the way users expect. Returns the typed code, or "" if cancelled/empty.
    """
    ui_blank()
    ui_box(
        [
            "Write your code below. Press Enter for a new line.",
            "Type :done on its own line (or Ctrl-D) to submit.",
            "Type :cancel to go back without submitting.",
        ],
        title="Code editor" + (f" ({LEARN_LANGUAGES[language]})" if language in LEARN_LANGUAGES else ""),
        color=ANSI.cyan,
    )
    lines: list[str] = []
    while True:
        try:
            line = input(f"{ANSI.dim}{len(lines) + 1:>3} | {ANSI.reset}")
        except EOFError:
            break
        stripped = line.strip()
        if stripped == ":done":
            break
        if stripped == ":cancel":
            return ""
        lines.append(line)
    return "\n".join(lines).strip("\n")


# A "lesson view" normalises programming and AI lessons into one shape so the
# teach -> practice -> auto-advance loop is written once for both tracks.

def _programming_lesson_view(language: str, lesson: dict) -> dict:
    note = LANGUAGE_NOTES[language]
    teach = [lesson["objective"]]
    explanation = LESSON_EXPLANATIONS.get(lesson["topic"])
    if explanation:
        teach += [""] + [f"- {point}" for point in explanation]
    teach += ["", f"In {LEARN_LANGUAGES[language]}: {note['syntax']}"]
    return {
        "title": f"Day {lesson['day']}: {lesson['title']} ({LEARN_LANGUAGES[language]})",
        "subject": LEARN_LANGUAGES[language],
        "context": lesson["title"],
        "topic": lesson["topic"],
        "teach": teach,
        "example": lesson.get("example", ""),
        "example_title": note["example_prefix"],
        "language": language,
        "quiz": lesson["quiz"],
        "answers": lesson["answers"],
        "build": PRACTICE_TASKS.get(
            lesson["topic"],
            f"Write a short {LEARN_LANGUAGES[language]} program that demonstrates {lesson['title'].lower()}.",
        ),
    }


def _ai_lesson_view(module: str, lesson: dict) -> dict:
    context_paragraphs = _ai_context_paragraphs(module, lesson)
    teach = [
        lesson["objective"],
        "",
        *context_paragraphs,
        "",
        "Key ideas:",
        *[f"- {item}" for item in lesson.get("fundamentals", [])],
    ]
    quiz, answers = lesson["quiz"]
    return {
        "title": f"{AI_MODULES[module]} - Lesson {lesson['day']}: {lesson['title']}",
        "subject": AI_MODULES[module],
        "context": lesson["title"],
        "teach": teach,
        "context_paragraphs": context_paragraphs,
        "example": "",
        "example_title": "Example",
        "language": None,
        "quiz": quiz,
        "answers": answers,
        "build": lesson.get("build", "Write down the smallest working version you could build."),
    }


def _ai_sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    return text if text.endswith((".", "!", "?", ":")) else f"{text}."


def _ai_context_paragraphs(module: str, lesson: dict) -> list[str]:
    module_label = AI_MODULES[module]
    fundamentals = [_ai_sentence(item) for item in lesson.get("fundamentals", []) if item.strip()]
    paragraphs = [
        (
            f"{lesson['title']} sits inside {module_label}. In practice, this topic is about learning how to explain "
            "the idea clearly, choose the right design choice, and spot where the concept stops being reliable."
        )
    ]
    if fundamentals:
        first = " ".join(fundamentals[:2])
        if first:
            paragraphs.append(first)
        rest = " ".join(fundamentals[2:])
        if rest:
            paragraphs.append(
                f"{rest} Put another way, the important part is not memorizing the term. "
                "It is knowing what changes in a real product, what tradeoff you are accepting, "
                "and what can go wrong if you ignore it."
            )
    else:
        paragraphs.append(
            "The central idea is easier to remember when you connect it to a real AI workflow, such as choosing a model, "
            "writing a prompt, retrieving supporting facts, or checking whether the output is trustworthy."
        )
    return paragraphs


def _teach_lesson(view: dict) -> None:
    ui_blank()
    ui_box(view["teach"], title=f"Stage 1 · Lecture · {view['title']}", color=ANSI.cyan)
    if view.get("example"):
        ui_blank()
        ui_box(view["example"].splitlines(), title=view["example_title"], color=ANSI.green)


def _quick_check(view: dict, progress: dict, cfg: dict, has_prev: bool = False) -> str:
    """Run the conceptual quick check.

    Returns 'correct', 'prev', or 'back'. Wrong answers stay in the question
    loop so the learner can reattempt before moving to the coding problem.
    """
    provider = progress.get("ai_provider", "offline")
    ui_blank()
    ui_box([view["quiz"]], title="Stage 2 · Question / answer", color=ANSI.amber)
    help_text = "Type your answer  ·  [a] ask the tutor  ·  [b] back"
    if has_prev:
        help_text += "  ·  [p] previous"
    ui_line(help_text, color=ANSI.dim)
    attempts = 0
    while True:
        answer = _read_line("> ").strip()
        cmd = answer.lower()
        if cmd in ("b", "back"):
            return "back"
        if cmd in ("p", "prev", "previous"):
            if has_prev:
                return "prev"
            ui_line("This is the first lesson.", color=ANSI.amber)
            continue
        if cmd in ("a", "ask"):
            ui_line("Ask your tutor:", color=ANSI.cyan)
            question = _read_line("> ").strip()
            if question:
                _show_ai_feedback(_learning_ai_response(provider, question, view["subject"], cfg, progress, context=view["context"]))
            ui_box([view["quiz"]], title="Stage 2 · Question / answer", color=ANSI.amber)
            ui_line(help_text, color=ANSI.dim)
            continue
        if not answer:
            continue
        attempts += 1
        correct, feedback = _grade_answer(provider, view["quiz"], answer, view["answers"], view["subject"], cfg, progress, view["context"])
        if correct:
            ui_line("Correct!", color=ANSI.green, bold=True)
            if feedback:
                ui_box(feedback.splitlines(), title="Tutor", color=ANSI.cyan)
            ui_line("Next: coding problem.", color=ANSI.dim)
            return "correct"
        if attempts == 1:
            # Let the learner try again before the tutor corrects them.
            ui_line("Not quite — give it another try.", color=ANSI.amber, bold=True)
            ui_line("Type [a] for a hint, or answer again.", color=ANSI.dim)
        else:
            ui_line("Not quite.", color=ANSI.amber, bold=True)
            if feedback:
                ui_box(feedback.splitlines(), title="Tutor", color=ANSI.cyan)
            else:
                # No tutor prose (offline, or AI grading fell back to matching):
                # reveal a correct answer so the learner is never stuck.
                ui_box([f"A correct answer is: {view['answers'][0]}.", "Review the lesson above, then try again."],
                       title="Answer", color=ANSI.amber)


def _has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL) for pattern in patterns)


def _output_patterns(language: str | None) -> list[str]:
    return {
        "python": [r"\bprint\s*\("],
        "c": [r"\bprintf\s*\("],
        "java": [r"System\.out\.print(?:ln)?\s*\("],
    }.get(language or "", [r"\bprint\s*\(", r"\bprintf\s*\(", r"System\.out\.print"])


def _programming_hard_review(view: dict, code: str) -> tuple[bool | None, str]:
    topic = view.get("topic", "")
    language = view.get("language")
    if not _has_any(code, _output_patterns(language)) and topic not in {"classes"}:
        return False, "Hard checks failed: include visible output so the result can be verified."
    if topic == "variables":
        assignments = re.findall(r"(?m)^\s*(?:[A-Za-z_]\w*\s+)?[A-Za-z_]\w*\s*=", code)
        if len(assignments) < 2:
            return False, "Hard checks failed: create at least two variables before printing."

    checks: dict[str, tuple[list[str], str]] = {
        "variables": (
            [r"(?m)^\s*(?:[A-Za-z_]\w*\s+)?[A-Za-z_]\w*\s*=", *_output_patterns(language)],
            "Hard checks passed: found variable assignment and output.",
        ),
        "types": (
            [r"[\"']10[\"']", r"\b(?:int|float|double|Integer\.parseInt|Double\.parseDouble|atoi|strtol)\b", r"\b5\b", *_output_patterns(language)],
            "Hard checks passed: found string-to-number conversion, addition, and output.",
        ),
        "input": (
            [r"\b(?:input|Scanner|scanf|fgets|BufferedReader)\b", r"\b(?:int|float|double|Integer\.parseInt|Double\.parseDouble|atoi|strtol)\b", *_output_patterns(language)],
            "Hard checks passed: found input, numeric conversion, and output.",
        ),
        "conditionals": (
            [r"\bif\b", r"\belse\b", r"(?:positive|negative|zero|>\s*0|<\s*0)", *_output_patterns(language)],
            "Hard checks passed: found branching logic for positive/negative/zero.",
        ),
        "loops": (
            [r"\b(?:for|while)\b", r"(?:1\s*(?:,|\.\.|;|<=)|range\s*\(\s*1\s*,\s*11\s*\))", *_output_patterns(language)],
            "Hard checks passed: found a loop over the required range and output.",
        ),
        "functions": (
            [r"\bsquare\b", r"\breturn\b", r"\b4\b", *_output_patterns(language)],
            "Hard checks passed: found square function, return value, call, and output.",
        ),
        "arrays": (
            [r"(?:\[|\{)\s*3\s*,\s*1\s*,\s*4\s*(?:\]|\})", r"\b(?:for|while|sum)\b", *_output_patterns(language)],
            "Hard checks passed: found the required collection, traversal or sum, and output.",
        ),
        "strings": (
            [r"[\"']hello[\"']", r"\b(?:len|length|strlen)\b", r"(?:\[0\]|charAt\s*\(\s*0\s*\))", *_output_patterns(language)],
            "Hard checks passed: found length and first-character handling.",
        ),
        "bitwise": (
            [r"(?:&|\||\^|<<|>>|~)", r"(?:READ|WRITE|EXEC|flag|mask)", *_output_patterns(language)],
            "Hard checks passed: found bitwise operators, flags or masks, and output.",
        ),
        "pseudocode": (
            [r"\b(?:for|while)\b", r"(?:1\s*;\s*.*<=\s*5|range\s*\(\s*1\s*,\s*6\s*\)|1\s+to\s+5)", r"(?:total|sum)", *_output_patterns(language)],
            "Hard checks passed: found translated pseudo-code loop, accumulator, and output.",
        ),
        "java_bitwise_deep": (
            [r"(?:&|\||\^|<<|>>|>>>|~)", r"(?:READ|WRITE|EXEC|flag|mask)", r"System\.out\.print"],
            "Hard checks passed: found Java bitwise operations, flags or masks, and output.",
        ),
        "java_random_testing": (
            [r"\b(?:Random|ThreadLocalRandom)\b", r"(?:42|seed)", r"\b(?:nextInt|nextDouble|shuffle)\b", r"System\.out\.print"],
            "Hard checks passed: found Java random generation, reproducibility, and output.",
        ),
        "java_benchmarking": (
            [r"System\.nanoTime\s*\(", r"(?:end\s*-|elapsed|duration|ms)", r"System\.out\.print"],
            "Hard checks passed: found Java nanoTime timing and output.",
        ),
        "c_command_line_args": (
            [r"\bargc\b", r"\bargv\b", r"(?:usage|fprintf\s*\(\s*stderr|printf)", r"\breturn\s+1\b|\bexit\s*\("],
            "Hard checks passed: found argc/argv validation and usage/error handling.",
        ),
        "c_file_io": (
            [r"\bfopen\s*\(", r"\bfgets\s*\(", r"\bfclose\s*\(", r"(?:NULL|!\s*\w+)"],
            "Hard checks passed: found fopen, fgets, fclose, and failure handling.",
        ),
        "c_function_pointers": (
            [r"\(\s*\*\s*\w+\s*\)|typedef\s+.*\(\s*\*", r"\[[^\]]*\]\s*=", r"\w+\s*\[[^\]]+\]\s*\("],
            "Hard checks passed: found function pointer declaration, dispatch array, and call.",
        ),
        "c_bitwise_deep": (
            [r"\b(?:uint32_t|unsigned)\b", r"(?:&|\||\^|<<|>>|~)", r"\bprintf\s*\("],
            "Hard checks passed: found unsigned bitwise operations and output.",
        ),
        "c_benchmarking": (
            [r"\bstruct\s+timespec\b", r"\bclock_gettime\s*\(", r"\bCLOCK_MONOTONIC\b", r"\bprintf\s*\("],
            "Hard checks passed: found clock_gettime timing and output.",
        ),
        "c_random_testing": (
            [r"\bsrand\s*\(", r"\brand\s*\(", r"(?:42|seed|time\s*\()", r"\bprintf\s*\("],
            "Hard checks passed: found C random generation, seeding, and output.",
        ),
        "c_hash_algorithms": (
            [r"\b(?:djb2|fnv|jenkins)\b", r"(?:<<|\^|\*)", r"\b(?:collision|collisions|printf)\b"],
            "Hard checks passed: found named hash algorithm logic and collision/output reporting.",
        ),
        "python_bitwise_deep": (
            [r"(?:&|\||\^|<<|>>|~)", r"(?:READ|WRITE|EXEC|flag|mask)", r"\bprint\s*\("],
            "Hard checks passed: found Python bitwise operations, flags or masks, and output.",
        ),
        "python_test_automation": (
            [r"\bsubprocess\.run\s*\(", r"\btimeout\s*=", r"\b(?:stdout|stderr|returncode)\b", r"\b(?:print|csv\.writer|DictWriter)\b"],
            "Hard checks passed: found subprocess automation, timeout, result inspection, and reporting.",
        ),
        "python_benchmarking": (
            [r"\b(?:timeit|perf_counter|process_time)\b", r"\b(?:repeat|timeit|start|elapsed)\b", r"\bprint\s*\("],
            "Hard checks passed: found Python timing API and output.",
        ),
        "python_random_testing": (
            [r"\brandom\.seed\s*\(", r"\brandom\.(?:randint|randrange|random|shuffle|sample|choices)\b", r"\b(?:assert|print)\b"],
            "Hard checks passed: found reproducible random generation and verification.",
        ),
        "python_graph_algorithms": (
            [r"\bheapq\b", r"\b(?:heappush|heappop)\b", r"\b(?:dist|distance|float\s*\(\s*[\"']inf)", r"\bprint\s*\("],
            "Hard checks passed: found heap-based graph algorithm logic and output.",
        ),
    }
    required = checks.get(topic)
    if not required:
        return None, "Hard checks could not fully verify this exercise; AI review is needed."
    patterns, success = required
    missing = [pattern for pattern in patterns if not _has_any(code, [pattern])]
    if missing:
        return False, "Hard checks failed: the submission is missing one or more required pieces for this exercise."
    return True, success


def _submission_hard_review(view: dict, code: str) -> tuple[bool | None, str]:
    cleaned = code.strip()
    if len(cleaned) < 12:
        return False, "Hard checks failed: the submission is too short to review."
    if re.search(r"\b(todo|placeholder|fix me|not sure)\b", cleaned, flags=re.IGNORECASE):
        return False, "Hard checks failed: remove placeholders before submitting."
    if view.get("language"):
        return _programming_hard_review(view, cleaned)
    if len(re.findall(r"\w+", cleaned)) < 8:
        return False, "Hard checks failed: include enough detail to evaluate the implementation."
    return None, "Hard checks passed basic completeness; AI review is needed for correctness."


def _ai_review_submission(view: dict, code: str, provider: str, cfg: dict, progress: dict) -> tuple[bool, str]:
    local_cfg, error = _prepare_ai_cfg(provider, cfg, progress)
    if error:
        return False, error

    lang_label = LEARN_LANGUAGES.get(view.get("language") or "", view["subject"])
    system = (
        "You are reviewing a beginner's coding or implementation exercise. "
        "Decide whether the submission satisfies the exercise goal. Be practical: "
        "minor style issues are okay, but missing core behavior, syntax that cannot plausibly run, "
        "or an answer that is only prose when code/design artifacts are required is not correct. "
        "Return ONLY valid JSON, no markdown fences: "
        '{"correct": true or false, "feedback": "two to four concise sentences with the next fix if incorrect"}'
    )
    user_msg = (
        f"Subject: {view['subject']}\n"
        f"Lesson context: {view['context']}\n"
        f"Exercise: {view['build']}\n"
        f"Submission type/language: {lang_label}\n\n"
        f"Submission:\n{code}"
    )
    try:
        raw = _call_ai(system, user_msg, provider, local_cfg, timeout=120)
        data = _parse_json_response(raw or "")
        if isinstance(data, dict) and "correct" in data:
            return bool(data["correct"]), str(data.get("feedback", "")).strip()
        return False, raw or "AI review did not return a usable result. Try again or change AI settings."
    except Exception as exc:
        return False, f"AI review failed: {exc}"


def _ai_feedback_after_hard_pass(view: dict, code: str, provider: str, cfg: dict, progress: dict) -> str:
    local_cfg, error = _prepare_ai_cfg(provider, cfg, progress)
    if error:
        return ""
    lang_label = LEARN_LANGUAGES.get(view.get("language") or "", view["subject"])
    system = (
        "You are a concise coding coach. The deterministic checks already passed, "
        "so do not change the correctness decision. Give one short improvement note, "
        "or say the solution is ready if there is nothing important to improve."
    )
    user_msg = f"Exercise: {view['build']}\nLanguage/type: {lang_label}\nSubmission:\n{code}"
    try:
        return _call_ai(system, user_msg, provider, local_cfg, timeout=60) or ""
    except Exception:
        return ""


def _review_code_submission(view: dict, code: str, progress: dict, cfg: dict) -> tuple[bool, str]:
    provider = progress.get("ai_provider", "offline")
    hard_result, hard_feedback = _submission_hard_review(view, code)
    if hard_result is False:
        return False, hard_feedback
    if hard_result is True:
        ai_note = _ai_feedback_after_hard_pass(view, code, provider, cfg, progress)
        feedback = hard_feedback + "\nNext: this lesson can advance."
        return True, feedback + (f"\nAI note: {ai_note}" if ai_note else "")
    return _ai_review_submission(view, code, provider, cfg, progress)


def _coding_practice(view: dict, progress: dict, cfg: dict, has_prev: bool = False) -> str:
    ui_blank()
    ui_box([view["build"]], title="Stage 3 · Coding problem", color=ANSI.cyan)
    prompt = "Press Enter to open the editor  ·  [b] back"
    if has_prev:
        prompt += "  ·  [p] previous"
    ui_line(prompt, color=ANSI.dim)
    cmd = _read_line("> ").strip().lower()
    if cmd in ("b", "back"):
        return "back"
    if cmd in ("p", "prev", "previous"):
        if has_prev:
            return "prev"
        ui_line("This is the first lesson.", color=ANSI.amber)
        return "retry"
    code = _read_code_block(view.get("language"))
    if not code.strip():
        ui_line("No code submitted.", color=ANSI.dim)
        return "retry"
    correct, feedback = _review_code_submission(view, code, progress, cfg)
    title = "Stage 4 · Review"
    color = ANSI.green if correct else ANSI.amber
    ui_blank()
    ui_box((feedback or ("Correct." if correct else "Not correct yet.")).splitlines(), title=title, color=color)
    if correct:
        ui_line("Next: lesson completion.", color=ANSI.dim)
        return "correct"
    ui_line("Press Enter to reattempt the coding problem.", color=ANSI.dim)
    _read_line()
    return "retry"


def _practice_lesson(view: dict, progress: dict, cfg: dict, has_prev: bool = False) -> str:
    """Sequential practice: question/answer, then coding problem with AI review."""
    while True:
        check_result = _quick_check(view, progress, cfg, has_prev=has_prev)
        if check_result in ("back", "prev"):
            return check_result
        while True:
            code_result = _coding_practice(view, progress, cfg, has_prev=has_prev)
            if code_result == "correct":
                return "complete"
            if code_result in ("back", "prev"):
                return code_result


def _lesson_session(progress, cfg, *, curriculum, completed_days, make_view,
                    practice_lesson, mark_complete, after_complete, show_all_done) -> None:
    """Shared teach -> practice loop with forward/backward lesson navigation.

    Tracks position by index so the learner can revisit earlier lessons, not
    just advance through the next unfinished one.
    """
    if not curriculum:
        return
    idx = next((i for i, lesson in enumerate(curriculum) if lesson["day"] not in completed_days), None)
    if idx is None:
        # Everything is done: show the summary, then drop in at the last lesson
        # so the learner can still page backward through what they finished.
        show_all_done()
        idx = len(curriculum) - 1
    while True:
        lesson = curriculum[idx]
        view = make_view(lesson)
        _teach_lesson(view)
        ui_blank()
        done = "  (completed)" if lesson["day"] in completed_days else ""
        ui_line(f"Lesson {idx + 1} of {len(curriculum)}{done}", color=ANSI.dim)
        nav = "Press Enter for Q&A  ·  [b] back to menu"
        if idx > 0:
            nav = "Press Enter for Q&A  ·  [p] previous lesson  ·  [b] back to menu"
        ui_line(nav, color=ANSI.dim)
        cmd = _read_line().strip().lower()
        if cmd in ("b", "back"):
            return
        if cmd in ("p", "prev", "previous"):
            if idx > 0:
                idx -= 1
            continue
        result = practice_lesson(view, progress, cfg, has_prev=idx > 0)
        if result == "back":
            return
        if result == "prev":
            if idx > 0:
                idx -= 1
            continue
        # result == "complete"
        mark_complete(lesson)
        completed_days.add(lesson["day"])
        ui_line(f"Marked complete: {lesson['title']}", color=ANSI.green, bold=True)
        after_complete()
        if idx < len(curriculum) - 1:
            idx += 1
            continue
        show_all_done()
        return


def _run_lesson(language: str, progress: dict, cfg: dict) -> None:
    """Teach -> practice -> navigate through the programming curriculum."""
    lang_progress = progress.setdefault("languages", {}).setdefault(
        language, {"completed_lessons": [], "completed_topics": [], "last_session": ""}
    )

    def show_all_done():
        ui_blank()
        ui_box([f"You completed every lesson in the {LEARN_LANGUAGES[language]} curriculum.",
                "Keep going with the unlocked LeetCode problems below."],
               title="Curriculum complete", color=ANSI.green)
        _print_unlocked_after_lesson(language)

    _lesson_session(
        progress, cfg,
        curriculum=build_learning_curriculum(language),
        completed_days=set(lang_progress.get("completed_lessons", [])),
        make_view=lambda lesson: _programming_lesson_view(language, lesson),
        practice_lesson=_practice_lesson,
        mark_complete=lambda lesson: _mark_lesson_complete(language, lesson, progress),
        after_complete=lambda: _print_unlocked_after_lesson(language),
        show_all_done=show_all_done,
    )


def _print_unlocked_after_lesson(language: str) -> None:
    problems = _unlocked_leetcode(language, limit=3)
    if not problems:
        ui_box(["No LeetCode problems unlocked yet. Keep going through the basics."], title="Practice", color=ANSI.dim)
        return
    lc_progress = load_leetcode_progress()
    ui_box([_format_problem_line(p, language, lc_progress) for p in problems], title="Unlocked practice", color=ANSI.green)


def _run_ai_lesson(module: str, progress: dict, cfg: dict) -> None:
    """Teach -> practice -> navigate through a Principles of AI module."""
    module_progress = progress.setdefault("ai_principles", {}).setdefault(
        module, {"completed_lessons": [], "last_session": ""}
    )

    def show_all_done():
        ui_blank()
        ui_box([f"You completed {AI_MODULES[module]}.",
                "Switch modules from Settings, or use Ask AI Tutor for deeper questions."],
               title="Module complete", color=ANSI.green)

    _lesson_session(
        progress, cfg,
        curriculum=_ai_curriculum(module),
        completed_days=set(module_progress.get("completed_lessons", [])),
        make_view=lambda lesson: _ai_lesson_view(module, lesson),
        practice_lesson=_practice_lesson,
        mark_complete=lambda lesson: _mark_ai_lesson_complete(module, lesson, progress),
        after_complete=lambda: None,
        show_all_done=show_all_done,
    )


def _show_learning_progress(language: str, progress: dict, cfg: dict) -> None:
    lang_progress = progress.get("languages", {}).get(language, {})
    completed = set(lang_progress.get("completed_lessons", []))
    curriculum = build_learning_curriculum(language)
    provider = progress.get("ai_provider", "offline")
    lines = [
        f"Lessons: {len(completed)}/{len(curriculum)}",
        "Completed topics: " + (", ".join(lang_progress.get("completed_topics", [])) or "-"),
        *_provider_identity_lines(provider, cfg, progress),
    ]
    next_lesson = _next_lesson(language, lang_progress)
    if next_lesson:
        lines.append(f"Next lesson: Day {next_lesson['day']} - {next_lesson['title']}")
    else:
        lines.append("Next lesson: curriculum complete")
    ui_blank()
    ui_box(lines, title=f"Progress: {LEARN_LANGUAGES[language]}", color=ANSI.cyan)
    unlocked = _unlocked_leetcode(language, limit=5)
    if unlocked:
        ui_blank()
        ui_box([_format_problem_line(p, language, load_leetcode_progress()) for p in unlocked], title="Unlocked LeetCode", color=ANSI.green)


def _show_ai_progress(module: str, progress: dict, cfg: dict) -> None:
    module_progress = progress.get("ai_principles", {}).get(module, {})
    completed = set(module_progress.get("completed_lessons", []))
    curriculum = _ai_curriculum(module)
    provider = progress.get("ai_provider", "offline")
    lines = [
        f"Lessons: {len(completed)}/{len(curriculum)}",
        *_provider_identity_lines(provider, cfg, progress),
    ]
    next_lesson = _next_ai_lesson(module, module_progress)
    if next_lesson:
        lines.append(f"Next lesson: {next_lesson['day']} - {next_lesson['title']}")
    else:
        lines.append("Next lesson: module complete")
    ui_blank()
    ui_box(lines, title=f"Progress: {AI_MODULES[module]}", color=ANSI.cyan)
    module_lines = []
    for key, label in AI_MODULES.items():
        mp = progress.get("ai_principles", {}).get(key, {})
        count = len(mp.get("completed_lessons", []))
        total = len(_ai_curriculum(key))
        mark = "*" if key == module else " "
        module_lines.append(f"{mark} {label}: {count}/{total}")
    ui_blank()
    ui_box(module_lines, title="All Principles of AI modules", color=ANSI.cyan)


def _practice_leetcode_interactive(language: str) -> None:
    problems = _unlocked_leetcode(language, limit=10)
    if not problems:
        ui_box(["No unlocked LeetCode problems yet. Finish more lessons first."], title="LeetCode practice", color=ANSI.amber)
        return
    lc_progress = load_leetcode_progress()
    ui_blank()
    ui_box([f"[{i}] {_format_problem_line(problem, language, lc_progress)}" for i, problem in enumerate(problems, 1)], title="Unlocked LeetCode practice", color=ANSI.green)
    ui_line("Pick a number to view, or press Enter to return.", color=ANSI.dim)
    raw = ui_prompt()
    if not raw:
        return
    try:
        problem = problems[int(raw) - 1]
    except (ValueError, IndexError):
        ui_line("Invalid pick.", color=ANSI.amber)
        return
    ui_blank()
    problem_lines = [problem.get("url", "")]
    if problem.get("local_path"):
        prompt = _extract_local_prompt(_read_local_problem(problem["local_path"]))
        if prompt:
            problem_lines += [""] + prompt.splitlines()
        problem_lines += ["", f"Local file: {problem['local_path']}"]
    ui_box(problem_lines, title=f"{problem['id']} - {problem['title']}", color=ANSI.cyan)
    ui_line("Mark complete for this language? [y/N]", color=ANSI.amber)
    done = ui_prompt()
    if done == "y":
        completed = lc_progress.setdefault("completed_problems", {}).setdefault(language, [])
        if problem["id"] not in completed:
            completed.append(problem["id"])
            completed.sort()
            save_leetcode_progress(lc_progress)
        ui_line("Marked complete.", color=ANSI.green, bold=True)


def _change_learning_settings(progress: dict, cfg: dict) -> tuple[str, str, str, str]:
    track = _prompt_choice(
        "\nLearning track:",
        {"programming": "Programming languages", "ai_principles": "Principles of AI"},
        default=progress.get("active_track") or "programming",
    )
    language = progress.get("active_language") or "python"
    module = progress.get("active_ai_module") or "rag"
    if track == "programming":
        language = _prompt_choice(
            "\nLanguage:",
            {"python": "Python", "c": "C", "java": "Java"},
            default=language,
        )
    else:
        module = _prompt_choice(
            "\nPrinciples of AI module:",
            AI_MODULES,
            default=module,
        )
    provider = _prompt_choice(
        "\nAI assistance:",
        {"offline": "Offline only", "local": "Local AI (LM Studio)", "claude": "Claude", "openai": "OpenAI", "deepseek": "DeepSeek"},
        default=progress.get("ai_provider", "offline"),
    )
    _configure_provider_model(provider, cfg, progress)
    theme = _prompt_choice(
        "\nColor theme (for terminal legibility):",
        {"dark": "Dark background", "light": "Light background"},
        default=progress.get("theme", "dark"),
    )
    progress["active_track"] = track
    progress["active_language"] = language
    progress["active_ai_module"] = module
    progress["ai_provider"] = provider
    progress["theme"] = theme
    apply_theme(theme)
    save_learning_progress(progress)
    return track, language, module, provider


def _active_progress_summary(track: str, language: str, module: str, progress: dict) -> str:
    if track == "programming":
        lang_progress = progress.get("languages", {}).get(language, {})
        completed = len(lang_progress.get("completed_lessons", []))
        total = len(build_learning_curriculum(language))
        return f"Track: Programming · {LEARN_LANGUAGES[language]} · {completed}/{total} lessons"
    module_progress = progress.get("ai_principles", {}).get(module, {})
    completed = len(module_progress.get("completed_lessons", []))
    total = len(_ai_curriculum(module))
    return f"Track: Principles of AI · {AI_MODULES[module]} · {completed}/{total} lessons"


def _active_next_label(track: str, language: str, module: str, progress: dict) -> str:
    if track == "programming":
        lang_progress = progress.get("languages", {}).get(language, {})
        lesson = _next_lesson(language, lang_progress)
        return f"Day {lesson['day']}: {lesson['title']}" if lesson else "curriculum complete"
    module_progress = progress.get("ai_principles", {}).get(module, {})
    lesson = _next_ai_lesson(module, module_progress)
    return f"Lesson {lesson['day']}: {lesson['title']}" if lesson else "module complete"


def _session_status_lines(
    track: str,
    language: str,
    module: str,
    provider: str,
    progress: dict,
    cfg: dict,
    *,
    stage: str,
    next_action: str,
) -> list[str]:
    return [
        f"Stage: {stage}",
        _active_progress_summary(track, language, module, progress),
        f"Current lesson: {_active_next_label(track, language, module, progress)}",
        *_provider_identity_lines(provider, cfg, progress),
        f"Next: {next_action}",
    ]


def _print_session_status(
    track: str,
    language: str,
    module: str,
    provider: str,
    progress: dict,
    cfg: dict,
    *,
    stage: str = "Home",
    next_action: str = "Enter to resume today's lesson",
) -> None:
    status_lines = _session_status_lines(
        track, language, module, provider, progress, cfg,
        stage=stage,
        next_action=next_action,
    )
    ui_blank()
    ui_box(status_lines, title="Session", color=ANSI.cyan)
    if provider != "offline" and not _provider_ready(provider, cfg):
        ui_box(["AI provider is selected but not ready.", "You can still learn offline or change settings."], title="Provider warning", color=ANSI.amber)


def _explicit_learning_args(args) -> bool:
    return bool(args and any(getattr(args, name, None) for name in ("track", "language", "module", "ai")))


def _learn_command_options(track: str) -> list[tuple[str, str, tuple[str, ...]]]:
    second = "LeetCode practice" if track == "programming" else "Module progress"
    return [
        ("lesson", "Resume today's lesson", ("1", "today", "start", "learn", "resume")),
        ("secondary", second, ("2", "leetcode", "practice", "module")),
        ("ask", "Ask AI tutor", ("3", "ai", "tutor", "question")),
        ("progress", "Progress", ("4", "stats", "status")),
        ("settings", "Settings", ("5", "config", "setup")),
        ("quit", "Quit", ("6", "q", "exit")),
    ]


def _resolve_home_command(raw: str, track: str) -> str:
    command = raw.strip().lower()
    if not command:
        return "lesson"
    if command in (":commands", "commands", "cmd", "menu", "?", "/"):
        return _command_palette("Commands", _learn_command_options(track))
    for key, _label, aliases in _learn_command_options(track):
        if command == key or command in aliases:
            return key
    return "ask"


def handle_learn(args=None) -> None:
    cfg = load_config()
    progress = load_learning_progress()
    if args and getattr(args, "theme", None):
        progress["theme"] = args.theme
    apply_theme(progress.get("theme", "dark"))
    print_learn_banner()

    if args and getattr(args, "track", None):
        progress["active_track"] = args.track
    if args and getattr(args, "language", None):
        progress["active_language"] = args.language
        progress["active_track"] = "programming"
    if args and getattr(args, "module", None):
        progress["active_ai_module"] = args.module
        progress["active_track"] = "ai_principles"
    if args and getattr(args, "ai", None):
        progress["ai_provider"] = args.ai

    if _explicit_learning_args(args):
        track = _ensure_learning_track(progress)
        language = _ensure_learning_language(progress) if track == "programming" else progress.get("active_language", "python")
        module = _ensure_ai_module(progress) if track == "ai_principles" else progress.get("active_ai_module", "rag")
        provider = _ensure_learning_ai(progress)
        _ensure_provider_model_choice(provider, cfg, progress)
        progress["onboarding_complete"] = True
    else:
        needs_onboarding = (
            not progress.get("onboarding_complete")
            or progress.get("active_track") not in LEARN_TRACKS
            or progress.get("ai_provider") not in LEARN_AI_PROVIDERS
        )
        if needs_onboarding:
            ui_blank()
            ui_line("Set up your first session", color=ANSI.green, bold=True)
            track, language, module, provider = _change_learning_settings(progress, cfg)
            progress["onboarding_complete"] = True
        else:
            track = _ensure_learning_track(progress)
            language = _ensure_learning_language(progress) if track == "programming" else progress.get("active_language", "python")
            module = _ensure_ai_module(progress) if track == "ai_principles" else progress.get("active_ai_module", "rag")
            provider = _ensure_learning_ai(progress)
            _ensure_provider_model_choice(provider, cfg, progress)
    save_learning_progress(progress)
    cfg = _apply_progress_models(cfg, progress)

    while True:
        _print_session_status(
            track, language, module, provider, progress, cfg,
            stage="Resume",
            next_action="Enter: resume lesson · Ctrl+P: commands · type: tutor question",
        )
        raw = _read_command_line()
        choice = _resolve_home_command(raw, track)
        if choice == "quit":
            ui_line("Saved. See you next session.", color=ANSI.green, bold=True)
            return
        if choice == "lesson":
            if track == "programming":
                _run_lesson(language, progress, cfg)
            else:
                _run_ai_lesson(module, progress, cfg)
        elif choice == "secondary":
            if track == "programming":
                _practice_leetcode_interactive(language)
            else:
                _show_ai_progress(module, progress, cfg)
        elif choice == "ask":
            ui_line("Ask your tutor:", color=ANSI.cyan)
            command_words = {":commands", "commands", "cmd", "menu", "?", "/", "ask", "ai", "tutor", "question", "3"}
            question = raw.strip() if raw.strip().lower() not in command_words else _read_line("> ").strip()
            if question:
                subject = LEARN_LANGUAGES[language] if track == "programming" else AI_MODULES[module]
                _show_ai_feedback(
                    _learning_ai_response(progress.get("ai_provider", "offline"), question, subject, cfg, progress),
                )
        elif choice == "progress":
            if track == "programming":
                _show_learning_progress(language, progress, cfg)
            else:
                _show_ai_progress(module, progress, cfg)
        elif choice == "settings":
            track, language, module, provider = _change_learning_settings(progress, cfg)
            progress["onboarding_complete"] = True
            save_learning_progress(progress)
            cfg = _apply_progress_models(cfg, progress)


# ── Web intelligence (one Claude call with web search) ────────────────────

INTEL_SYSTEM = """\
You are a research analyst preparing a daily intelligence summary for one specific person.
Return ONLY valid JSON (no markdown fences, no commentary).
Be factual, unbiased, and data-driven. No predictions. No hype.
Use supplied current context first. If a number, URL, salary, company, or date is not supported by the provided search/current context, use "--" or leave the URL empty.
"""

INTEL_PROMPT = """\
Research and provide current data for today's learning summary.
Use ONLY supplied current context and web search results. Do NOT use training data for prices, salaries, dates, or "current" claims.
Tailor career advice to the profile and local skill gaps. Ryu is targeting AI engineering, not ML research.

1. MARKET RECAP (last 24 hours):
   - S&P 500: last close, daily change %
   - NASDAQ composite: last close, daily change %
   - Bitcoin (BTC): current price USD, 24h change %
   - Solana (SOL): current price USD, 24h change %
   - Tesla (TSLA): last close, daily change %
   - Nvidia (NVDA): last close, daily change %
   - Apple (AAPL): last close, daily change %
   - Prefer VERIFIED MARKET QUOTES if supplied. Otherwise use --.
   - Notable macro events in one line.

2. AI ENGINEERING DEMAND (current):
   - Top 6-8 most useful skills/tools for this person right now, balancing market demand and their current gaps
   - For each: name, why employers want it, one concrete first step that fits their courses/projects
   - Avoid generic certificates unless the evidence strongly supports one.
   - Notable shifts vs 3-6 months ago

3. JOB MARKET (current):
   - Hiring trend: growing/flat/contracting
   - Mid-level AI engineer salary range (US)
   - Companies actively hiring
   - Remote vs hybrid vs onsite, only if supported by search results; otherwise "--"
   - Notable news

4. RESEARCH RADAR:
   - 5 recent AI/ML developments relevant to an aspiring AI engineer
   - CRITICAL: For each item, use ONLY a URL from the web search results. If no URL is available, set "url" to "". NEVER fabricate a URL.
   - Prefer engineering-practical items: evals, agents, RAG, deployment, tooling, model APIs.

Return ONLY valid JSON:
{
  "market": {
    "sp500": {"value": "5,400", "change": "+0.5%"},
    "nasdaq": {"value": "17,000", "change": "+0.8%"},
    "btc": {"price": "$104,000", "change_24h": "+2.1%"},
    "sol": {"price": "$170", "change_24h": "+3.0%"},
    "tsla": {"price": "$340", "change_24h": "+1.2%"},
    "nvda": {"price": "$135", "change_24h": "+0.9%"},
    "aapl": {"price": "$198", "change_24h": "-0.3%"},
    "notable": "one-line summary"
  },
  "ai_demand": {
    "top_skills": [
      {"name": "Python", "why": "reason", "start": "concrete first step"}
    ],
    "shifts": "paragraph on changes"
  },
  "job_market": {
    "trend": "growing",
    "salary_range": "$140k - $210k",
    "hot_companies": ["company1"],
    "remote_ratio": "35% remote, 45% hybrid, 20% onsite",
    "notable": "news"
  },
  "research": [
    {"title": "...", "summary": "...", "why": "...", "url": "real URL from search results or empty string"}
  ]
}
"""


def _ddg_search(queries, max_results=5) -> str:
    """Run DuckDuckGo searches, return compiled results as context."""
    try:
        from ddgs import DDGS
    except ImportError:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            return ""
    results = []
    with DDGS() as ddgs:
        for q in queries:
            try:
                hits = list(ddgs.text(q, max_results=max_results))
                for h in hits:
                    url = h.get("href", "")
                    title = h.get("title", "")
                    body = h.get("body", "")
                    results.append(f"[{q}] {title}: {body} (URL: {url})")
            except Exception:
                continue
    return "\n".join(results)


DDG_QUERIES = [
    "AI engineer hiring trends salary United States current",
    "AI engineering most in demand skills frameworks current",
    "latest AI ML research developments this week",
    "AI agent frameworks LangGraph AutoGen CrewAI current",
    "LLM evaluation RAG production best practices current",
]


QUOTE_SYMBOLS = {
    "sp500": {"symbol": "^GSPC", "label": "S&P 500", "price_key": "value", "change_key": "change"},
    "nasdaq": {"symbol": "^IXIC", "label": "NASDAQ", "price_key": "value", "change_key": "change"},
    "btc": {"symbol": "BTC-USD", "label": "BTC", "price_key": "price", "change_key": "change_24h"},
    "sol": {"symbol": "SOL-USD", "label": "SOL", "price_key": "price", "change_key": "change_24h"},
    "tsla": {"symbol": "TSLA", "label": "TSLA", "price_key": "price", "change_key": "change_24h"},
    "nvda": {"symbol": "NVDA", "label": "NVDA", "price_key": "price", "change_key": "change_24h"},
    "aapl": {"symbol": "AAPL", "label": "AAPL", "price_key": "price", "change_key": "change_24h"},
}


def _format_quote_price(value, currency="USD", index=False) -> str:
    if value is None:
        return "--"
    if index:
        return f"{float(value):,.2f}"
    prefix = "$" if currency == "USD" else f"{currency} "
    return f"{prefix}{float(value):,.2f}"


def _format_pct(value) -> str:
    if value is None:
        return "--"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def gather_market_quotes() -> dict:
    """Fetch quote data directly so market numbers are not delegated to the LLM."""
    market = {}
    headers = {"User-Agent": "language-ai-principles-cli/1.0"}
    for key, meta in QUOTE_SYMBOLS.items():
        symbol = meta["symbol"]
        try:
            r = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                params={"range": "5d", "interval": "1d"},
                headers=headers,
                timeout=10,
            )
            r.raise_for_status()
            result = r.json()["chart"]["result"][0]
            qmeta = result.get("meta", {})
            price = qmeta.get("regularMarketPrice")
            previous = qmeta.get("chartPreviousClose") or qmeta.get("previousClose")
            if price is None or previous in (None, 0):
                continue
            pct = (float(price) - float(previous)) / float(previous) * 100
            currency = qmeta.get("currency", "USD")
            item = {
                meta["price_key"]: _format_quote_price(
                    price, currency=currency, index=key in ("sp500", "nasdaq")
                ),
                meta["change_key"]: _format_pct(pct),
                "source": "Yahoo Finance",
            }
            as_of = qmeta.get("regularMarketTime")
            if as_of:
                item["as_of"] = datetime.fromtimestamp(as_of).strftime("%Y-%m-%d %H:%M")
            market[key] = item
        except Exception:
            continue
    if market:
        market["notable"] = "Quote data fetched directly; broader macro note is generated from search context when available."
    return market


def _merge_market_quotes(intel: dict | None, quotes: dict) -> dict | None:
    if not intel:
        intel = {}
    if quotes:
        existing = intel.get("market", {}) if isinstance(intel.get("market"), dict) else {}
        notable = existing.get("notable") or quotes.get("notable", "")
        merged = {**existing, **quotes}
        if notable:
            merged["notable"] = notable
        intel["market"] = merged
    return intel


def gather_web_intel(provider, cfg, search_ctx="", profile="", skills=None, market_quotes=None) -> dict | None:
    skills = skills or {}
    today = datetime.now().strftime("%Y-%m-%d")
    personal_context = f"""\
TODAY: {today}

PROFILE:
{profile}

LOCAL SKILL GAP DATA:
{json.dumps(skills, indent=2) if skills else "No local skill-gap data."}

VERIFIED MARKET QUOTES:
{json.dumps(market_quotes, indent=2) if market_quotes else "No direct quote data available; use -- for unavailable quote fields."}
"""
    try:
        prompt = f"{personal_context}\n\n{INTEL_PROMPT}"
        if provider == "claude":
            raw = _call_ai(INTEL_SYSTEM, prompt, provider, cfg,
                            web_search=True, timeout=300)
        else:
            if search_ctx:
                prompt += f"\n\nWEB SEARCH RESULTS (use these for current data):\n{search_ctx}"
            raw = _call_ai(INTEL_SYSTEM, prompt, provider, cfg, timeout=300)
        result = _parse_json_response(raw)
        return _merge_market_quotes(_sanitize_intel(result), market_quotes or {})
    except Exception as e:
        print(f"    Web intel error: {e}")
        return _merge_market_quotes(None, market_quotes or {})


VERIFY_SYSTEM = """\
You are a fact-checker verifying an AI-generated intelligence summary against raw web search results.

Rules:
1. Compare every price, percentage, and fact against the search results.
2. If a value in the summary contradicts the search results, CORRECT it.
3. If a research URL does NOT appear in the search results, set "url" to "".
4. If a value cannot be verified from the search results, keep it but add "(unverified)" after it.
5. NEVER return "not_specified". Use "--" if data is truly unavailable.
6. Return the CORRECTED data in the exact same JSON format. No commentary.
"""


def verify_intel(intel, search_ctx, provider, cfg) -> dict | None:
    """Verify web intelligence against raw DDG search results."""
    if not intel or not search_ctx:
        return intel

    user_msg = f"""GENERATED SUMMARY TO VERIFY:
{json.dumps(intel, indent=2)}

RAW WEB SEARCH RESULTS (ground truth):
{search_ctx}

Compare every claim against the search results. Fix anything that's wrong. Return corrected JSON."""

    try:
        raw = _call_ai(VERIFY_SYSTEM, user_msg, provider, cfg, timeout=180)
        result = _parse_json_response(raw)
        if isinstance(result, dict) and ("market" in result or "research" in result):
            return _sanitize_intel(result)
        return intel
    except Exception as e:
        print(f"    Verification error: {e}")
        return intel


def _sanitize_intel(data):
    """Clean 'not_specified' and similar junk from LLM output."""
    if not data or not isinstance(data, dict):
        return data
    # Clean market section
    mkt = data.get("market", {})
    for key, val in mkt.items():
        if isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, str) and ("not_specified" in v.lower() or "not specified" in v.lower()):
                    val[k] = "--"
        elif isinstance(val, str) and ("not_specified" in val.lower() or "not specified" in val.lower()):
            mkt[key] = ""
    # Clean job market
    jm = data.get("job_market", {})
    for k, v in jm.items():
        if isinstance(v, str) and ("not_specified" in v.lower() or "not specified" in v.lower()):
            jm[k] = "--"
    return data


# ── Study optimizer (AI) ──────────────────────────────────────────────────

OPTIMIZER_SYSTEM = """\
You are an expert academic operator and AI-engineering mentor.
Create today's plan from only the supplied profile, Anki analytics, deadlines, and skill gaps.

Rules:
- Prioritize deadlines inside 7 days, then high Anki due counts, then career skill gaps.
- Make every block concrete enough to execute without more planning.
- Include a deliverable or done condition for every block.
- Be tailored to Ryu's courses, projects, and AI engineering target.
- Do not recommend broad courses, certificates, or generic "learn X" tasks unless they are already in the supplied context.
- Keep the total realistic for one day: 90-240 minutes unless there are no urgent items.
- Say what to skip only in the summary, not as a standalone work block.

Return ONLY valid JSON:
{"plan": [{"topic": "...", "minutes": 45, "priority": "critical|high|medium", "reason": "...", "deliverable": "..."}], "summary": "..."}
"""


def generate_study_plan(anki_data, deadlines, profile, skills, provider, cfg) -> dict | None:
    user_msg = f"""STUDENT PROFILE:
{profile}

ANKI DATA:
{json.dumps(anki_data, indent=2) if anki_data else "Anki not available"}

UPCOMING DEADLINES:
{json.dumps(deadlines, indent=2) if deadlines else "No deadlines set"}

SKILL GAP DATA:
{json.dumps(skills, indent=2) if skills else "No skill-gap data"}

Generate today's study plan. Return only the JSON object."""

    try:
        raw = _call_ai(OPTIMIZER_SYSTEM, user_msg, provider, cfg)
        return _parse_json_response(raw)
    except Exception as e:
        print(f"    Study plan error: {e}")
        return None


# ── Final synthesis (AI) ──────────────────────────────────────────────────

SYNTHESIS_SYSTEM = """\
You are a strategic advisor writing an executive-quality daily learning summary for Ryu.
Given the complete daily data, identify the decisions that matter today.

Rules:
- 4-6 bullets, each one sentence.
- Every bullet must connect at least two supplied data points or explain a concrete tradeoff.
- Tailor to Ryu's AI engineering path, current MSCS courses, Anki load, and deadlines.
- Do not repeat the study plan line by line.
- Do not invent facts, numbers, deck names, companies, or deadlines.
- No motivational filler.
- End with one clear recommendation for what to prioritize today.

Return ONLY valid JSON:
{"bullets": [{"label": "Focus", "text": "insight"}], "recommendation": "what to do today"}
"""


def generate_synthesis(all_data, profile, provider, cfg) -> dict:
    user_msg = f"""STUDENT PROFILE:
{profile}

COMPLETE DAILY DATA:
{json.dumps(all_data, indent=2, default=str)}

Write the strategic summary as bullet points. End with one clear recommendation."""

    try:
        raw = _call_ai(SYNTHESIS_SYSTEM, user_msg, provider, cfg)
        result = _parse_json_response(raw)
        if isinstance(result, dict) and "bullets" in result:
            return result
        if isinstance(result, dict) and "synthesis" in result:
            return {"bullets": [result["synthesis"]], "recommendation": ""}
        return {}
    except Exception as e:
        print(f"    Synthesis error: {e}")
        return {}


# ── HTML renderer ─────────────────────────────────────────────────────────

REPORT_CSS = """
  :root {
    --bg: #f4f6f8;
    --panel: #ffffff;
    --panel-soft: #f9fafb;
    --ink: #172033;
    --muted: #667085;
    --faint: #98a2b3;
    --line: #d7dee8;
    --line-soft: #e7ebf0;
    --accent: #b42318;
    --accent-soft: #fff3f1;
    --teal: #007a7a;
    --green: #16803c;
    --amber: #b76e00;
    --red: #c02121;
    --code: #27364a;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--ink);
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.55;
    font-size: 15px;
  }
  .page {
    width: min(1120px, calc(100% - 32px));
    margin: 0 auto;
    padding: 32px 0 56px;
  }
  header {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 16px;
    align-items: end;
    padding: 18px 0 20px;
    border-bottom: 2px solid var(--ink);
    margin-bottom: 18px;
  }
  h1 {
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(1.55rem, 3vw, 2.35rem);
    font-weight: 700;
    letter-spacing: 0;
    line-height: 1;
    color: var(--ink);
  }
  .kicker, time, .card-label, th, .stat-label, .rec-label, footer {
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0;
  }
  .kicker {
    display: block;
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 8px;
  }
  time {
    color: var(--muted);
    font-size: 0.78rem;
    text-align: right;
  }
  .grid {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.65fr);
    gap: 16px;
    align-items: start;
  }
  .stack { display: grid; gap: 16px; }
  .card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 18px;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
  }
  .accent-border {
    border-top: 4px solid var(--accent);
    padding-top: 16px;
  }
  .card-label {
    color: var(--muted);
    font-size: 0.7rem;
    font-weight: 700;
    margin-bottom: 12px;
  }
  .synth-list {
    list-style: none;
    display: grid;
    gap: 10px;
  }
  .synth-list li {
    display: grid;
    grid-template-columns: 84px minmax(0, 1fr);
    gap: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--line-soft);
  }
  .synth-list li:last-child { border-bottom: 0; padding-bottom: 0; }
  .bullet-label {
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
  }
  .rec {
    margin-top: 14px;
    padding: 12px 14px;
    background: var(--accent-soft);
    border: 1px solid #ffd3cc;
    border-radius: 6px;
  }
  .rec-label {
    display: block;
    color: var(--accent);
    font-size: 0.68rem;
    font-weight: 700;
    margin-bottom: 4px;
  }
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(126px, 1fr));
    gap: 10px;
  }
  .stat-grid.three { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .stat {
    background: var(--panel-soft);
    border: 1px solid var(--line-soft);
    border-radius: 6px;
    padding: 12px;
    min-height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .stat-num {
    display: block;
    color: var(--ink);
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(1.1rem, 2vw, 1.45rem);
    font-weight: 700;
    line-height: 1.15;
    overflow-wrap: anywhere;
  }
  .stat-label {
    color: var(--muted);
    font-size: 0.62rem;
    font-weight: 700;
    margin-top: 8px;
  }
  .stat-sub {
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    margin-top: 4px;
    overflow-wrap: anywhere;
  }
  table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
  th {
    color: var(--muted);
    font-size: 0.65rem;
    font-weight: 700;
    text-align: left;
    padding: 8px;
    border-bottom: 1px solid var(--line);
  }
  td {
    vertical-align: top;
    padding: 10px 8px;
    border-bottom: 1px solid var(--line-soft);
  }
  tr:last-child td { border-bottom: 0; }
  tr.row-critical td { background: #fff1f1; }
  tr.row-soon td { background: #fff8e8; }
  code, .badge {
    background: #eef2f6;
    border: 1px solid #dce4ec;
    border-radius: 4px;
    color: var(--code);
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    padding: 1px 6px;
  }
  .badge { color: var(--muted); margin-left: 4px; }
  .dim { color: var(--muted); font-size: 0.88rem; }
  .muted { color: var(--muted); font-style: italic; }
  .red { color: var(--red); } .green { color: var(--green); }
  .cyan { color: var(--teal); } .yellow { color: var(--amber); }
  .plan-summary {
    color: var(--muted);
    font-size: 0.92rem;
    margin-bottom: 10px;
  }
  .priority {
    border-radius: 999px;
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    margin-bottom: 4px;
    padding: 2px 7px;
    text-transform: uppercase;
  }
  .priority-critical { background: #fff1f1; color: var(--red); }
  .priority-high { background: #fff8e8; color: var(--amber); }
  .priority-medium { background: #ecfdf5; color: var(--green); }
  .skill-card, .research-item {
    border-top: 1px solid var(--line-soft);
    padding: 12px 0;
  }
  .skill-card:first-child, .research-item:first-child { border-top: 0; padding-top: 0; }
  .skill-card:last-child, .research-item:last-child { padding-bottom: 0; }
  .skill-title, .research-title {
    color: var(--ink);
    font-weight: 700;
    margin-bottom: 4px;
  }
  .skill-meta {
    color: var(--teal);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    font-weight: 700;
  }
  .source {
    color: var(--teal);
    font-size: 0.78rem;
    text-decoration: none;
    white-space: nowrap;
  }
  .source:hover { text-decoration: underline; }
  footer {
    color: var(--muted);
    font-size: 0.64rem;
    margin-top: 22px;
    padding-top: 12px;
    border-top: 1px solid var(--line);
  }
  @media (max-width: 860px) {
    .grid { grid-template-columns: 1fr; }
    header { grid-template-columns: 1fr; }
    time { text-align: left; }
  }
  @media (max-width: 620px) {
    .page { width: min(100% - 20px, 1120px); padding-top: 18px; }
    .card { padding: 14px; }
    .stat-grid, .stat-grid.three { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .synth-list li { grid-template-columns: 1fr; gap: 4px; }
    table { display: block; overflow-x: auto; white-space: nowrap; }
    td:nth-child(3) { white-space: normal; min-width: 240px; }
  }
  @media print {
    body { background: #fff; }
    .page { width: 100%; padding: 0; }
    .card { box-shadow: none; break-inside: avoid; }
  }
"""

def render_html(data: dict, today: str) -> str:
    """Render all gathered data into a responsive HTML learning summary."""

    anki = data.get("anki")
    git = data.get("git", [])
    deadlines = data.get("deadlines", [])
    skills = data.get("skills", {})
    intel = data.get("intel") or {}
    plan = data.get("study_plan") or {}
    synthesis = data.get("synthesis", "")

    market = intel.get("market", {})
    ai_demand = intel.get("ai_demand", {})
    job_market = intel.get("job_market", {})
    research = intel.get("research", [])

    def synthesis_html():
        if not synthesis or not synthesis.get("bullets"):
            return ""
        bullets = ""
        for i, b in enumerate(synthesis.get("bullets", []), 1):
            if isinstance(b, dict):
                label = _escape(b.get("label") or f"Signal {i}")
                text = _escape(b.get("text") or "")
            else:
                label = f"Signal {i}"
                text = _escape(b)
            if text:
                bullets += f'<li><span class="bullet-label">{label}</span><span>{text}</span></li>'
        rec = synthesis.get("recommendation", "")
        rec_html = f'<div class="rec"><span class="rec-label">Recommendation</span>{_escape(rec)}</div>' if rec else ""
        return f'''<div class="card accent-border">
  <div class="card-label">STRATEGIC ANALYSIS</div>
  <ul class="synth-list">{bullets}</ul>
  {rec_html}
</div>'''

    def anki_html():
        if not anki:
            return '<div class="card"><div class="card-label">REVIEW QUEUE</div><p class="muted">Anki not running.</p></div>'
        weak = ", ".join(f'<code>{_escape(t)}</code> <span class="dim">({_escape(n)})</span>' for t, n in anki["weak_tags"]) if anki["weak_tags"] else '<span class="dim">none detected</span>'
        return f'''<div class="card">
  <div class="card-label">REVIEW QUEUE</div>
  <div class="stat-grid">
    <div class="stat"><span class="stat-num cyan">{_escape(anki["due"])}</span><span class="stat-label">TO REVIEW</span></div>
    <div class="stat"><span class="stat-num green">{_escape(anki["reviewed_today"])}</span><span class="stat-label">DONE TODAY</span></div>
    <div class="stat"><span class="stat-num">{_escape(anki["retention_approx"])}%</span><span class="stat-label">MATURITY</span></div>
    <div class="stat"><span class="stat-num red">{_escape(anki["leech_count"])}</span><span class="stat-label">LEECHES</span></div>
  </div>
  <p style="margin-top:0.8rem;font-size:0.8rem;">Weak spots: {weak}</p>
</div>'''

    def plan_html():
        if not plan or not plan.get("plan"):
            return ""
        items = ""
        for p in plan["plan"]:
            priority = _escape(str(p.get("priority", "medium")).lower())
            if priority not in ("critical", "high", "medium"):
                priority = "medium"
            deliverable = p.get("deliverable", "")
            rationale = _escape(p.get("reason", ""))
            if deliverable:
                rationale += f'<br><span class="dim"><strong>Done:</strong> {_escape(deliverable)}</span>'
            items += (
                f'<tr><td class="cyan">{_escape(p.get("minutes", "?"))} min</td>'
                f'<td><span class="priority priority-{priority}">{priority}</span><br>{_escape(p.get("topic", ""))}</td>'
                f'<td>{rationale}</td></tr>'
            )
        summary = plan.get("summary", "")
        return f'''<div class="card">
  <div class="card-label">STUDY PLAN</div>
  {f'<p class="plan-summary">{_escape(summary)}</p>' if summary else ''}
  <table><thead><tr><th>TIME</th><th>TOPIC</th><th>RATIONALE</th></tr></thead><tbody>{items}</tbody></table>
</div>'''

    def deadline_html():
        if not deadlines:
            return '<div class="card"><div class="card-label">CALENDAR</div><p class="muted">No events found.</p></div>'
        rows = ""
        for d in deadlines:
            u = d["urgency"]
            cls = "row-critical" if u in ("critical", "overdue") else "row-soon" if u == "soon" else ""
            label = f'{d["days_left"]}d' if d["days_left"] >= 0 else "OVERDUE"
            num_cls = "red" if u in ("critical", "overdue") else "yellow" if u == "soon" else "cyan"
            cal_badge = f' <span class="badge">{_escape(d["calendar"])}</span>' if d.get("calendar") else ""
            course_badge = f' <code>{_escape(d["course"])}</code>' if d.get("course") else ""
            time_str = d.get("time", "")
            notes = d.get("notes", "") or d.get("topics", "")
            rows += f'<tr class="{cls}"><td class="{num_cls}">{_escape(label)}</td><td>{_escape(d["name"])}{cal_badge}{course_badge}</td><td>{_escape(time_str)}</td><td class="dim">{_escape(notes)}</td></tr>'
        return f'''<div class="card">
  <div class="card-label">CALENDAR &mdash; UPCOMING</div>
  <table><thead><tr><th>IN</th><th>EVENT</th><th>TIME</th><th>NOTES</th></tr></thead><tbody>{rows}</tbody></table>
</div>'''

    def skills_html():
        if not skills or not skills.get("skills"):
            return ""
        rows = ""
        for s in skills.get("skills", [])[:6]:
            rows += f'''<div class="skill-card">
  <div class="skill-title">{_escape(s.get("name", ""))}</div>
  <div class="skill-meta">level {_escape(s.get("level", "?"))} / target {_escape(s.get("target", "?"))} &middot; gap {_escape(s.get("gap", "?"))}</div>
</div>'''
        target = skills.get("target_role", "target role")
        biggest = ", ".join(skills.get("biggest_gaps", [])[:5])
        return f'''<div class="card">
  <div class="card-label">LOCAL SKILL GAPS</div>
  <p class="dim" style="margin-bottom:10px;">For {_escape(target)}: {_escape(biggest) if biggest else "no major gaps listed"}.</p>
  {rows}
</div>'''

    def market_html():
        if not market:
            return '<div class="card"><div class="card-label">MARKET RECAP &mdash; 24H</div><p class="muted">No data.</p></div>'
        sp = market.get("sp500", {})
        nq = market.get("nasdaq", {})
        bt = market.get("btc", {})
        sl = market.get("sol", {})
        ts = market.get("tsla", {})
        nv = market.get("nvda", {})
        ap = market.get("aapl", {})
        return f'''<div class="card">
  <div class="card-label">MARKET RECAP &mdash; 24H</div>
  <div class="stat-grid">
    <div class="stat"><span class="stat-num">{_escape(sp.get("change", "N/A"))}</span><span class="stat-label">S&amp;P 500</span><span class="stat-sub">{_escape(sp.get("value", ""))}</span></div>
    <div class="stat"><span class="stat-num">{_escape(nq.get("change", "N/A"))}</span><span class="stat-label">NASDAQ</span><span class="stat-sub">{_escape(nq.get("value", ""))}</span></div>
    <div class="stat"><span class="stat-num">{_escape(bt.get("change_24h", "N/A"))}</span><span class="stat-label">BTC</span><span class="stat-sub">{_escape(bt.get("price", ""))}</span></div>
    <div class="stat"><span class="stat-num">{_escape(sl.get("change_24h", "N/A"))}</span><span class="stat-label">SOL</span><span class="stat-sub">{_escape(sl.get("price", ""))}</span></div>
    <div class="stat"><span class="stat-num">{_escape(ts.get("change_24h", "N/A"))}</span><span class="stat-label">TSLA</span><span class="stat-sub">{_escape(ts.get("price", ""))}</span></div>
    <div class="stat"><span class="stat-num">{_escape(nv.get("change_24h", "N/A"))}</span><span class="stat-label">NVDA</span><span class="stat-sub">{_escape(nv.get("price", ""))}</span></div>
    <div class="stat"><span class="stat-num">{_escape(ap.get("change_24h", "N/A"))}</span><span class="stat-label">AAPL</span><span class="stat-sub">{_escape(ap.get("price", ""))}</span></div>
  </div>
  {f'<p class="dim" style="margin-top:0.8rem;">{_escape(market.get("notable", ""))}</p>' if market.get("notable") else ''}
</div>'''

    def demand_html():
        if not ai_demand:
            return ""
        top = ai_demand.get("top_skills", [])
        if top and isinstance(top[0], dict):
            # New format with learning paths
            rows = ""
            for i, s in enumerate(top, 1):
                rows += f'''<div class="skill-card">
  <div class="skill-title">{i}. {_escape(s.get("name", ""))}</div>
  <p>{_escape(_first_sentence(s.get("why", ""), 180))}</p>
  <p class="dim" style="margin-top:4px;"><span class="green">Start:</span> {_escape(_truncate(s.get("start", ""), 180))}</p>
</div>'''
        else:
            # Fallback: old format (plain string list)
            rows = '<div class="pill-row">' + "".join(f'<span class="badge">{_escape(s)}</span>' for s in top) + '</div>'
        shifts = ai_demand.get("shifts", "")
        return f'''<div class="card">
  <div class="card-label">IN-DEMAND SKILLS &mdash; HOW TO START</div>
  {rows}
  {f'<p class="dim" style="margin-top:0.8rem;">{_escape(_truncate(shifts, 320))}</p>' if shifts else ''}
</div>'''

    def jobs_html():
        if not job_market:
            return ""
        hot = ", ".join(str(c) for c in job_market.get("hot_companies", []))
        return f'''<div class="card">
  <div class="card-label">JOB MARKET</div>
  <div class="stat-grid three">
    <div class="stat"><span class="stat-num cyan">{_escape(job_market.get("trend", "N/A"))}</span><span class="stat-label">HIRING TREND</span></div>
    <div class="stat"><span class="stat-num green">{_escape(job_market.get("salary_range", "N/A"))}</span><span class="stat-label">SALARY RANGE</span></div>
    <div class="stat"><span class="stat-num">{_escape(job_market.get("remote_ratio", "N/A"))}</span><span class="stat-label">REMOTE MIX</span></div>
  </div>
  {f'<p style="font-size:0.9rem;margin-top:0.8rem;">Active: <span class="cyan">{_escape(hot)}</span></p>' if hot else ''}
  {f'<p class="dim">{_escape(_truncate(job_market.get("notable", ""), 260))}</p>' if job_market.get("notable") else ''}
</div>'''

    def research_html():
        if not research:
            return ""
        items = ""
        for r in research:
            url = r.get("url", "")
            link = f' <a href="{_escape(url)}" target="_blank" class="source">source</a>' if url and url.startswith("http") else ""
            items += f'''<div class="research-item">
  <div class="research-title">{_escape(r.get("title", ""))}{link}</div>
  <p>{_escape(_truncate(r.get("summary", ""), 260))}</p>
  <p class="dim">{_escape(_truncate(r.get("why", ""), 220))}</p>
</div>'''
        return f'''<div class="card">
  <div class="card-label">RESEARCH RADAR</div>
  {items}
</div>'''

    main_col = "\n".join(filter(None, [
        synthesis_html(),
        plan_html(),
        deadline_html(),
        demand_html(),
        research_html(),
    ]))
    side_col = "\n".join(filter(None, [
        anki_html(),
        skills_html(),
        market_html(),
        jobs_html(),
    ]))
    body = f'<main class="grid"><section class="stack">{main_col}</section><aside class="stack">{side_col}</aside></main>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Learning Summary &mdash; {today}</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
{REPORT_CSS}
</style>
</head>
<body>
<div class="page">
<header>
  <div><span class="kicker">Daily Learning Summary</span><h1>Ryu Hemingway</h1></div>
  <time>{today}</time>
</header>
{body}
<footer>
  GENERATED BY LEARN.PY // PROVIDER: {_escape(data.get("synthesizer_used", "CLAUDE")).upper()}
</footer>
</div>
</body>
</html>'''


# ── CLI ───────────────────────────────────────────────────────────────────

def _list_lm_studio(cfg):
    base = cfg.get("local_endpoint", "http://localhost:1234/v1/chat/completions").rsplit("/v1/", 1)[0]
    try:
        r = requests.get(f"{base}/v1/models", timeout=10)
        r.raise_for_status()
        return [m.get("id", "?") for m in r.json().get("data", [])]
    except Exception:
        return []


def build_parser():
    p = argparse.ArgumentParser(
        description="Programming Fundamentals and AI learning CLI.",
        epilog="Run with no arguments for the interactive tutor.",
    )
    p.add_argument("-p", "--provider", choices=["claude", "openai", "deepseek", "local"],
                   help=argparse.SUPPRESS)
    p.add_argument("--no-open", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--output", help=argparse.SUPPRESS)
    p.add_argument("--list-models", action="store_true", help="Show LM Studio models")

    sub = p.add_subparsers(dest="command")

    learn = sub.add_parser("learn", help="Start the interactive programming tutor")
    learn.add_argument("--track", choices=["programming", "ai_principles"])
    learn.add_argument("-l", "--language", choices=["python", "c", "java"])
    learn.add_argument("--module", choices=list(AI_MODULES))
    learn.add_argument("--ai", choices=["offline", "local", "claude", "openai", "deepseek"],
                       help="AI helper mode for tutor explanations")
    learn.add_argument("--theme", choices=["light", "dark"], help="Color theme for terminal legibility")

    lc = sub.add_parser("leetcode", help="Practice from the local 200-problem LeetCode catalog")
    lc_sub = lc.add_subparsers(dest="leetcode_cmd", required=True)

    lc_stats = lc_sub.add_parser("stats", help="Show LeetCode catalog/progress stats")
    lc_stats.add_argument("-l", "--language", choices=["python", "c", "java"], default="python")

    lc_topics = lc_sub.add_parser("topics", help="List concept topics and completion state")
    lc_topics.add_argument("-l", "--language", choices=["python", "c", "java"], default="python")

    lc_topic_done = lc_sub.add_parser("topic-done", help="Mark concept topics complete for unlocks")
    lc_topic_done.add_argument("topic", nargs="+")
    lc_topic_done.add_argument("-l", "--language", choices=["python", "c", "java"], default="python")

    lc_list = lc_sub.add_parser("list", help="List LeetCode problems")
    lc_list.add_argument("-l", "--language", choices=["python", "c", "java"], default="python")
    lc_list.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    lc_list.add_argument("--topic")
    lc_list.add_argument("--unlocked", action="store_true", help="Only show problems unlocked by completed topics")
    lc_list.add_argument("--local-only", action="store_true", help="Only show problems with a local file for the language")
    lc_list.add_argument("--include-done", action="store_true", help="Include completed problems")
    lc_list.add_argument("--limit", type=int, default=25)

    lc_next = lc_sub.add_parser("next", help="Show the next unlocked unsolved problem")
    lc_next.add_argument("-l", "--language", choices=["python", "c", "java"], default="python")
    lc_next.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    lc_next.add_argument("--topic")
    lc_next.set_defaults(limit=1)

    lc_show = lc_sub.add_parser("show", help="Show one problem prompt and metadata")
    lc_show.add_argument("problem", help="Problem id, number, slug, or exact title")
    lc_show.add_argument("-l", "--language", choices=["python", "c", "java"], default="python")
    lc_show.add_argument("--open", action="store_true", help="Open the LeetCode URL when no local prompt exists")

    lc_done = lc_sub.add_parser("done", help="Mark a problem complete")
    lc_done.add_argument("problem", help="Problem id, number, slug, or exact title")
    lc_done.add_argument("-l", "--language", choices=["python", "c", "java"], default="python")
    return p


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    invoked_as = Path(sys.argv[0]).name.lower()
    tutor_flags = {"--track", "-l", "--language", "--module", "--ai", "--list-models", "-h", "--help"}
    full_cli_commands = {"learn", "leetcode"}
    if invoked_as in {"learn", "learn.py"} and (
        len(sys.argv) == 1
        or sys.argv[1] in tutor_flags
        or sys.argv[1] not in full_cli_commands
    ):
        p = argparse.ArgumentParser(description="Interactive programming tutor.")
        p.add_argument("--track", choices=["programming", "ai_principles"])
        p.add_argument("-l", "--language", choices=["python", "c", "java"])
        p.add_argument("--module", choices=list(AI_MODULES))
        p.add_argument("--ai", choices=["offline", "local", "claude", "openai", "deepseek"],
                       help="AI helper mode for tutor explanations")
        p.add_argument("--theme", choices=["light", "dark"], help="Color theme for terminal legibility")
        p.add_argument("--list-models", action="store_true", help="Show LM Studio models")
        args = p.parse_args()
        if args.list_models:
            cfg = load_config()
            models = _list_lm_studio(cfg)
            if models:
                ui_box([f"- {m}" for m in models], title="LM Studio models", color=ANSI.cyan)
            else:
                ui_box(["No models found. Is LM Studio running?"], title="LM Studio models", color=ANSI.amber)
            return
        handle_learn(args)
        return

    args = build_parser().parse_args()
    if args.list_models:
        cfg = load_config()
        models = _list_lm_studio(cfg)
        if models:
            ui_box([f"- {m}" for m in models], title="LM Studio models", color=ANSI.cyan)
        else:
            ui_box(["No models found. Is LM Studio running?"], title="LM Studio models", color=ANSI.amber)
        return
    if args.command is None:
        handle_learn(args)
        return
    if args.command == "learn":
        handle_learn(args)
        return
    if args.command == "leetcode":
        handle_leetcode(args)
        return


if __name__ == "__main__":
    main()
