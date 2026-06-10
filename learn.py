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
CONFIG_PATH = BASE / "config.json"
PROFILE_PATH = BASE / "profile.md"
DEADLINES_PATH = BASE / "deadlines.json"
SKILLS_PATH = BASE / "skills.json"
OUTPUT_DIR = BASE / "output"
DATA_DIR = BASE / "data"
LEETCODE_CATALOG_PATH = DATA_DIR / "leetcode_catalog.json"
LEETCODE_PROGRESS_PATH = DATA_DIR / "leetcode_progress.json"
LEARNING_PROGRESS_PATH = DATA_DIR / "learning_progress.json"


ANSI_ENABLED = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


class ANSI:
    reset = "\033[0m" if ANSI_ENABLED else ""
    bold = "\033[1m" if ANSI_ENABLED else ""
    dim = "\033[2m" if ANSI_ENABLED else ""
    cyan = "\033[36m" if ANSI_ENABLED else ""
    green = "\033[32m" if ANSI_ENABLED else ""
    amber = "\033[33m" if ANSI_ENABLED else ""
    red = "\033[31m" if ANSI_ENABLED else ""
    magenta = "\033[35m" if ANSI_ENABLED else ""


def _term_width() -> int:
    return max(72, min(110, shutil.get_terminal_size((96, 24)).columns))


def _strip_ansi(text: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", text)


def _display_len(text: str) -> int:
    return len(_strip_ansi(text))


def _center_text(text: str, width: int | None = None) -> str:
    width = width or _term_width()
    visible = _display_len(text)
    if visible >= width:
        return text
    return " " * ((width - visible) // 2) + text


def ui_line(text: str = "", color: str = "", bold: bool = False) -> None:
    prefix = (ANSI.bold if bold else "") + color
    print(_center_text(f"{prefix}{text}{ANSI.reset}" if prefix else text))


def ui_blank() -> None:
    print()


def ui_rule(char: str = "─", color: str = ANSI.dim) -> None:
    ui_line(char * min(84, _term_width() - 8), color=color)


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
    ui_box([f"[{i}] {option}" for i, option in enumerate(options, 1)], title=title, color=ANSI.magenta)


def ui_prompt() -> str:
    return input(_center_text(f"{ANSI.green}> {ANSI.reset}")).strip().lower()


def print_learn_banner() -> None:
    ui_blank()
    art = [
        "██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗",
        "██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║",
        "██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║",
        "██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║",
        "██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║",
        "╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝",
    ]
    for line in art:
        ui_line(line, color=ANSI.cyan, bold=True)
    ui_blank()
    ui_line("Programming Fundamentals and AI - By Ryu Hemingway", color=ANSI.green, bold=True)
    ui_line("Learn programming, AI systems, and LeetCode practice from one terminal.", color=ANSI.dim)
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


LEARN_TRACKS = {
    "programming": "Programming languages",
    "ai_principles": "Principles of AI",
}


AI_MODULES = {
    "llm_fundamentals": "LLM and model API fundamentals",
    "prompting": "Prompt and context engineering",
    "embeddings": "Embeddings and vector databases",
    "rag": "RAG fundamentals",
    "harnesses": "Harnesses and evaluation",
    "agents": "Agentic workflows",
    "locallm": "Local LLM fundamentals",
    "ml_basics": "Machine learning fundamentals",
    "data_engineering": "AI data engineering",
    "transformers": "Transformers and deep learning basics",
    "mlops": "AI deployment and MLOps",
    "safety": "AI safety, security, and privacy",
}


LESSON_TOPICS = [
    ("variables", "Variables and output", "Store values, name them clearly, and print results."),
    ("types", "Types and conversions", "Recognize numbers, text, booleans, and basic casts."),
    ("input", "Input and simple programs", "Read user input and turn it into useful values."),
    ("conditionals", "Conditionals", "Use if/else logic to make decisions."),
    ("loops", "Loops", "Repeat work with for/while loops and trace loop state."),
    ("functions", "Functions and methods", "Package logic into reusable units with parameters and returns."),
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


EXAMPLE_SNIPPETS = {
    "python": {
        "variables": 'name = "Ryu"\nscore = 10\nprint(name, score)',
        "conditionals": 'age = 20\nif age >= 18:\n    print("adult")\nelse:\n    print("minor")',
        "loops": 'for n in range(1, 6):\n    print(n)',
        "functions": 'def add(a, b):\n    return a + b\n\nprint(add(2, 3))',
        "arrays": 'nums = [3, 1, 4]\nfor n in nums:\n    print(n)',
        "strings": 'word = "level"\nprint(word == word[::-1])',
        "hash_maps": 'counts = {}\nfor ch in "banana":\n    counts[ch] = counts.get(ch, 0) + 1\nprint(counts)',
        "classes": 'class Counter:\n    def __init__(self):\n        self.value = 0\n    def inc(self):\n        self.value += 1',
    },
    "c": {
        "variables": '#include <stdio.h>\nint main(void) {\n    int score = 10;\n    printf("%d\\n", score);\n    return 0;\n}',
        "conditionals": '#include <stdio.h>\nint main(void) {\n    int age = 20;\n    if (age >= 18) printf("adult\\n");\n    else printf("minor\\n");\n    return 0;\n}',
        "loops": '#include <stdio.h>\nint main(void) {\n    for (int n = 1; n <= 5; n++) printf("%d\\n", n);\n    return 0;\n}',
        "functions": '#include <stdio.h>\nint add(int a, int b) { return a + b; }\nint main(void) {\n    printf("%d\\n", add(2, 3));\n    return 0;\n}',
        "arrays": '#include <stdio.h>\nint main(void) {\n    int nums[] = {3, 1, 4};\n    for (int i = 0; i < 3; i++) printf("%d\\n", nums[i]);\n    return 0;\n}',
        "strings": '#include <stdio.h>\n#include <string.h>\nint main(void) {\n    char word[] = "level";\n    printf("%zu\\n", strlen(word));\n    return 0;\n}',
        "hash_maps": 'C has no built-in hash map. Start with arrays/counting tables for small key ranges, then learn structs plus a hash table implementation.',
        "classes": 'C has structs, not classes. Use a struct for data and functions that receive a pointer to that struct.',
    },
    "java": {
        "variables": 'public class Main {\n    public static void main(String[] args) {\n        int score = 10;\n        System.out.println(score);\n    }\n}',
        "conditionals": 'public class Main {\n    public static void main(String[] args) {\n        int age = 20;\n        if (age >= 18) System.out.println("adult");\n        else System.out.println("minor");\n    }\n}',
        "loops": 'public class Main {\n    public static void main(String[] args) {\n        for (int n = 1; n <= 5; n++) System.out.println(n);\n    }\n}',
        "functions": 'public class Main {\n    static int add(int a, int b) { return a + b; }\n    public static void main(String[] args) {\n        System.out.println(add(2, 3));\n    }\n}',
        "arrays": 'public class Main {\n    public static void main(String[] args) {\n        int[] nums = {3, 1, 4};\n        for (int n : nums) System.out.println(n);\n    }\n}',
        "strings": 'public class Main {\n    public static void main(String[] args) {\n        String word = "level";\n        System.out.println(word.length());\n    }\n}',
        "hash_maps": 'import java.util.*;\npublic class Main {\n    public static void main(String[] args) {\n        Map<Character, Integer> counts = new HashMap<>();\n        for (char ch : "banana".toCharArray()) counts.put(ch, counts.getOrDefault(ch, 0) + 1);\n        System.out.println(counts);\n    }\n}',
        "classes": 'class Counter {\n    int value = 0;\n    void inc() { value++; }\n}',
    },
}


QUIZ_BY_TOPIC = {
    "variables": ("What is the main purpose of a variable?", ["store a value", "store values", "remember a value"]),
    "types": ("Why do types matter?", ["they define what operations are valid", "valid operations", "memory and operations"]),
    "input": ("What should you usually do before using numeric input?", ["convert it", "parse it", "cast it"]),
    "conditionals": ("Which construct lets code choose between branches?", ["if", "if else", "if/else"]),
    "loops": ("What do loops help you avoid writing repeatedly?", ["duplicate code", "repeated code", "repetition"]),
    "functions": ("What keyword returns a value from a function/method?", ["return"]),
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
    DATA_DIR.mkdir(parents=True, exist_ok=True)
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
    for i, (topic, title, objective) in enumerate(LESSON_TOPICS, 1):
        example = EXAMPLE_SNIPPETS.get(language, {}).get(topic)
        if not example:
            example = EXAMPLE_SNIPPETS.get(language, {}).get("variables", "")
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
    languages = progress.setdefault("languages", {})
    for language in LEARN_LANGUAGES:
        languages.setdefault(language, {"completed_lessons": [], "completed_topics": [], "last_session": ""})
    ai_progress = progress.setdefault("ai_principles", {})
    for module in AI_MODULES:
        ai_progress.setdefault(module, {"completed_lessons": [], "last_session": ""})
    return progress


def save_learning_progress(progress: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
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
    ui_box(lines, title=prompt.strip(), color=ANSI.magenta)
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
    mapped = topic
    if topic == "hash_maps":
        mapped = "arrays_hashing"
    if mapped not in lc_topics:
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


def _choose_local_model(cfg: dict, current: str = "") -> str:
    models = _list_lm_studio(cfg)
    if not models:
        return ""
    if current in models:
        return current
    ui_blank()
    ui_box(
        [f"[{idx}] {model}{'  default' if model == current else ''}" for idx, model in enumerate(models, 1)],
        title="Choose a local model",
        color=ANSI.cyan,
    )
    while True:
        raw = ui_prompt()
        if not raw and current in models:
            return current
        if raw.isdigit():
            pick = int(raw)
            if 1 <= pick <= len(models):
                return models[pick - 1]
        ui_line("Pick a number from the list.", color=ANSI.amber)


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


def _learning_ai_response(provider: str, question: str, subject: str, cfg: dict, progress: dict, context: str = "") -> str:
    if provider == "offline":
        return "AI assistance is set to offline. Change AI settings from the Learn menu to use local or cloud help."
    local_cfg = dict(cfg)
    if provider == "local":
        local_model = _learning_local_model(progress, cfg, prompt_if_missing=True)
        if not local_model:
            return "No local model is selected. Open Settings and choose a local model first."
        local_cfg["local_model"] = local_model
    if not _provider_ready(provider, local_cfg):
        return f"{LEARN_AI_PROVIDERS[provider]} is not ready. Check your model/API key, or switch AI settings."
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


def _show_ai_feedback(response: str, next_hint: str) -> None:
    ui_blank()
    ui_box(response.splitlines() or ["No response."], title="Tutor feedback", color=ANSI.cyan)
    ui_blank()
    ui_box([next_hint, "Press Enter to continue."], title="Next step", color=ANSI.green)
    input(_center_text(f"{ANSI.green}> {ANSI.reset}"))


def _print_lesson(language: str, lesson: dict) -> None:
    note = LANGUAGE_NOTES[language]
    ui_blank()
    ui_box(
        [
            lesson["objective"],
            "",
            note["syntax"],
        ],
        title=f"Day {lesson['day']}: {lesson['title']} ({LEARN_LANGUAGES[language]})",
        color=ANSI.cyan,
    )
    ui_blank()
    ui_box(lesson["example"].splitlines(), title=note["example_prefix"], color=ANSI.green)
    ui_blank()
    ui_box(
        [f"Explain {lesson['topic'].replace('_', ' ')} in your own words, then write or trace a tiny example."],
        title="Practice target",
        color=ANSI.magenta,
    )


def _run_lesson(language: str, progress: dict, cfg: dict) -> None:
    lang_progress = progress.setdefault("languages", {}).setdefault(
        language, {"completed_lessons": [], "completed_topics": [], "last_session": ""}
    )
    lesson = _next_lesson(language, lang_progress)
    if not lesson:
        print("\nYou completed the current curriculum for this language.")
        problems = _unlocked_leetcode(language, limit=10)
        if problems:
            print("Next: keep working through unlocked LeetCode problems.")
            for p in problems:
                print("  " + _format_problem_line(p, language, load_leetcode_progress()))
        return

    _print_lesson(language, lesson)
    while True:
        ui_menu("Lesson options", ["Quiz", "Ask AI", "Skip and mark complete", "Back"])
        choice = ui_prompt()
        if choice in ("4", "b", "back"):
            return
        if choice in ("2", "a", "ask"):
            provider = progress.get("ai_provider", "offline")
            ui_line("Ask your tutor:", color=ANSI.cyan)
            question = input(_center_text(f"{ANSI.green}> {ANSI.reset}")).strip()
            if question:
                _show_ai_feedback(
                    _learning_ai_response(provider, question, LEARN_LANGUAGES[language], cfg, progress, context=lesson["title"]),
                    "Next: press Enter, then choose 1 to retry the quiz, 2 to ask for another hint, 3 to skip, or 4 to go back.",
                )
            continue
        if choice in ("3", "s", "skip"):
            _mark_lesson_complete(language, lesson, progress)
            ui_line(f"Marked complete: {lesson['title']}", color=ANSI.green, bold=True)
            _print_unlocked_after_lesson(language)
            return
        if choice in ("1", "q", "quiz", ""):
            ui_blank()
            ui_box([lesson["quiz"]], title="Quick check", color=ANSI.amber)
            answer = input(_center_text(f"{ANSI.green}> {ANSI.reset}")).strip()
            if _answer_matches(answer, lesson["answers"]):
                ui_line("Correct.", color=ANSI.green, bold=True)
                _mark_lesson_complete(language, lesson, progress)
                _print_unlocked_after_lesson(language)
                return
            ui_line("Not quite.", color=ANSI.amber, bold=True)
            provider = progress.get("ai_provider", "offline")
            if provider != "offline":
                _show_ai_feedback(
                    _learning_ai_response(
                        provider,
                        f"The learner answered '{answer}' to: {lesson['quiz']}. Explain the correction.",
                        LEARN_LANGUAGES[language],
                        cfg,
                        progress,
                        context=lesson["title"],
                    ),
                    "Next: press Enter, then choose 1 to try the quiz again or 2 to ask for another hint.",
                )
            else:
                ui_box(["Review the example, then choose 1 to try the quiz again."], title="Next step", color=ANSI.amber)


def _print_unlocked_after_lesson(language: str) -> None:
    problems = _unlocked_leetcode(language, limit=3)
    if not problems:
        ui_box(["No LeetCode problems unlocked yet. Keep going through the basics."], title="Practice", color=ANSI.dim)
        return
    lc_progress = load_leetcode_progress()
    ui_box([_format_problem_line(p, language, lc_progress) for p in problems], title="Unlocked practice", color=ANSI.green)


def _print_ai_lesson(module: str, lesson: dict) -> None:
    ui_blank()
    ui_box(
        [lesson["objective"], ""] + [f"- {item}" for item in lesson.get("fundamentals", [])],
        title=f"{AI_MODULES[module]} - Lesson {lesson['day']}: {lesson['title']}",
        color=ANSI.cyan,
    )
    ui_blank()
    ui_box([lesson.get("build", "Write down the smallest working version you could build.")], title="Build practice", color=ANSI.green)


def _run_ai_lesson(module: str, progress: dict, cfg: dict) -> None:
    module_progress = progress.setdefault("ai_principles", {}).setdefault(
        module, {"completed_lessons": [], "last_session": ""}
    )
    lesson = _next_ai_lesson(module, module_progress)
    if not lesson:
        ui_box([f"You completed {AI_MODULES[module]}.", "Use Ask AI Tutor for deeper questions, or switch modules from Settings."], title="Module complete", color=ANSI.green)
        return

    _print_ai_lesson(module, lesson)
    while True:
        ui_menu("Lesson options", ["Quiz", "Ask AI", "Skip and mark complete", "Back"])
        choice = ui_prompt()
        if choice in ("4", "b", "back"):
            return
        if choice in ("2", "a", "ask"):
            provider = progress.get("ai_provider", "offline")
            ui_line("Ask your tutor:", color=ANSI.cyan)
            question = input(_center_text(f"{ANSI.green}> {ANSI.reset}")).strip()
            if question:
                _show_ai_feedback(
                    _learning_ai_response(provider, question, AI_MODULES[module], cfg, progress, context=lesson["title"]),
                    "Next: press Enter, then choose 1 to retry the module quiz, 2 to ask again, 3 to skip, or 4 to go back.",
                )
            continue
        if choice in ("3", "s", "skip"):
            _mark_ai_lesson_complete(module, lesson, progress)
            ui_line(f"Marked complete: {lesson['title']}", color=ANSI.green, bold=True)
            return
        if choice in ("1", "q", "quiz", ""):
            quiz, answers = lesson["quiz"]
            ui_blank()
            ui_box([quiz], title="Quick check", color=ANSI.amber)
            answer = input(_center_text(f"{ANSI.green}> {ANSI.reset}")).strip()
            if _answer_matches(answer, answers):
                ui_line("Correct.", color=ANSI.green, bold=True)
                _mark_ai_lesson_complete(module, lesson, progress)
                return
            ui_line("Not quite.", color=ANSI.amber, bold=True)
            provider = progress.get("ai_provider", "offline")
            if provider != "offline":
                _show_ai_feedback(
                    _learning_ai_response(
                        provider,
                        f"The learner answered '{answer}' to: {quiz}. Explain the correction.",
                        AI_MODULES[module],
                        cfg,
                        progress,
                        context=lesson["title"],
                    ),
                    "Next: press Enter, then choose 1 to try the quiz again or 2 to ask for another hint.",
                )
            else:
                ui_box(["Review the fundamentals, then choose 1 to try the quiz again."], title="Next step", color=ANSI.amber)


def _show_learning_progress(language: str, progress: dict) -> None:
    lang_progress = progress.get("languages", {}).get(language, {})
    completed = set(lang_progress.get("completed_lessons", []))
    curriculum = build_learning_curriculum(language)
    lines = [
        f"Lessons: {len(completed)}/{len(curriculum)}",
        f"AI: {LEARN_AI_PROVIDERS.get(progress.get('ai_provider', 'offline'), 'Offline only')}",
        "Completed topics: " + (", ".join(lang_progress.get("completed_topics", [])) or "-"),
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


def _show_ai_progress(module: str, progress: dict) -> None:
    module_progress = progress.get("ai_principles", {}).get(module, {})
    completed = set(module_progress.get("completed_lessons", []))
    curriculum = _ai_curriculum(module)
    lines = [
        f"Lessons: {len(completed)}/{len(curriculum)}",
        f"AI: {LEARN_AI_PROVIDERS.get(progress.get('ai_provider', 'offline'), 'Offline only')}",
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
    ui_box(module_lines, title="All Principles of AI modules", color=ANSI.magenta)


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
    if provider == "local":
        model = _choose_local_model(cfg, progress.get("local_model", ""))
        if model:
            progress["local_model"] = model
    progress["active_track"] = track
    progress["active_language"] = language
    progress["active_ai_module"] = module
    progress["ai_provider"] = provider
    save_learning_progress(progress)
    return track, language, module, provider


def handle_learn(args=None) -> None:
    cfg = load_config()
    progress = load_learning_progress()
    print_learn_banner()

    if args and getattr(args, "track", None):
        progress["active_track"] = args.track
    if args and getattr(args, "language", None):
        progress["active_language"] = args.language
        progress["active_track"] = progress.get("active_track") or "programming"
    if args and getattr(args, "module", None):
        progress["active_ai_module"] = args.module
        progress["active_track"] = progress.get("active_track") or "ai_principles"
    if args and getattr(args, "ai", None):
        progress["ai_provider"] = args.ai
    save_learning_progress(progress)

    track = _ensure_learning_track(progress)
    language = _ensure_learning_language(progress) if track == "programming" else progress.get("active_language", "python")
    module = _ensure_ai_module(progress) if track == "ai_principles" else progress.get("active_ai_module", "rag")
    provider = _ensure_learning_ai(progress)
    if provider == "local" and not progress.get("local_model"):
        _learning_local_model(progress, cfg, prompt_if_missing=True)
    if provider == "local" and progress.get("local_model"):
        cfg["local_model"] = progress["local_model"]

    status_lines = [f"Track: {LEARN_TRACKS[track]}"]
    if track == "programming":
        status_lines.append(f"Language: {LEARN_LANGUAGES[language]}")
    else:
        status_lines.append(f"Module: {AI_MODULES[module]}")
    status_lines.append(f"AI help: {LEARN_AI_PROVIDERS[provider]}")
    if provider == "local" and progress.get("local_model"):
        status_lines.append(f"Local model: {progress['local_model']}")
    ui_box(status_lines, title="Session", color=ANSI.cyan)
    if provider != "offline" and not _provider_ready(provider, cfg):
        ui_box(["AI provider is selected but not ready.", "You can still learn offline or change settings."], title="Provider warning", color=ANSI.amber)

    while True:
        options = ["Today's lesson"]
        if track == "programming":
            options.append("LeetCode practice")
        else:
            options.append("Module progress")
        options += ["Ask AI tutor", "Progress", "Settings", "Quit"]
        ui_blank()
        ui_menu("Command palette", options)
        choice = ui_prompt()
        if choice in ("6", "q", "quit", "exit"):
            ui_line("Saved. See you next session.", color=ANSI.green, bold=True)
            return
        if choice in ("1", "lesson", ""):
            if track == "programming":
                _run_lesson(language, progress, cfg)
            else:
                _run_ai_lesson(module, progress, cfg)
        elif choice in ("2", "leetcode", "practice"):
            if track == "programming":
                _practice_leetcode_interactive(language)
            else:
                _show_ai_progress(module, progress)
        elif choice in ("3", "ask"):
            ui_line("Ask your tutor:", color=ANSI.cyan)
            question = input(_center_text(f"{ANSI.green}> {ANSI.reset}")).strip()
            if question:
                subject = LEARN_LANGUAGES[language] if track == "programming" else AI_MODULES[module]
                _show_ai_feedback(
                    _learning_ai_response(progress.get("ai_provider", "offline"), question, subject, cfg, progress),
                    "Next: press Enter to return to the main menu.",
                )
        elif choice in ("4", "progress"):
            if track == "programming":
                _show_learning_progress(language, progress)
            else:
                _show_ai_progress(module, progress)
        elif choice in ("5", "settings"):
            track, language, module, provider = _change_learning_settings(progress, cfg)
            if provider == "local" and not progress.get("local_model"):
                _learning_local_model(progress, cfg, prompt_if_missing=True)
            if provider == "local" and progress.get("local_model"):
                cfg["local_model"] = progress["local_model"]
        else:
            ui_line("Pick 1, 2, 3, 4, 5, or 6.", color=ANSI.amber)


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
