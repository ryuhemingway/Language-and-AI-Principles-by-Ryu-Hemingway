#!/usr/bin/env python3
"""Generate README/HOWTO terminal screenshots as SVG assets."""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"

COLORS = {
    "bg": "#111820",
    "panel": "#141d24",
    "chrome": "#26323b",
    "cyan": "#55f6ff",
    "green": "#8cff8c",
    "amber": "#f7e86a",
    "dim": "#9aa1aa",
    "white": "#e8edf2",
}

FONT = "JetBrains Mono, SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace"
FONT_SIZE = 22
LINE_HEIGHT = 31
WIDTH = 1600
X = 48
Y = 78


Line = str | tuple[str, str]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_lines(lines: list[Line], x: int = X, y: int = Y) -> str:
    out: list[str] = []
    for idx, line in enumerate(lines):
        text, color = line if isinstance(line, tuple) else (line, "white")
        out.append(
            f'<text x="{x}" y="{y + idx * LINE_HEIGHT}" fill="{COLORS[color]}" '
            f'font-family="{FONT}" font-size="{FONT_SIZE}">{esc(text)}</text>'
        )
    return "\n".join(out)


def write_svg(name: str, lines: list[Line], *, width: int = WIDTH) -> None:
    height = Y + len(lines) * LINE_HEIGHT + 46
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(name)}">
  <rect width="{width}" height="{height}" rx="18" fill="{COLORS["bg"]}"/>
  <rect x="0" y="0" width="{width}" height="42" rx="18" fill="{COLORS["panel"]}"/>
  <circle cx="28" cy="21" r="7" fill="#ff5f57"/>
  <circle cx="52" cy="21" r="7" fill="#febc2e"/>
  <circle cx="76" cy="21" r="7" fill="#28c840"/>
  {render_lines(lines)}
</svg>
'''
    (OUT / name).write_text(svg, encoding="utf-8")


def write_animated_svg() -> None:
    frames: list[list[Line]] = [
        [
            ("AI ENGINEERING", "cyan"),
            ("Programming, ML, RAG, evals, and agentic systems - By Ryu Hemingway", "green"),
            ("", "white"),
            ("╭──────────────────────────── Learning track ────────────────────────────╮", "cyan"),
            ("│ [1] Programming languages  default                                      │", "cyan"),
            ("│ [2] Principles of AI                                                    │", "cyan"),
            ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
            ("╭──────────────────────────────── Input ─────────────────────────────────╮", "green"),
            ("│ > 1                                                                    │", "green"),
            ("╰────────────────────────────────────────────────────────────────────────╯", "green"),
        ],
        [
            ("AI ENGINEERING", "cyan"),
            ("╭──────────────────────────────── Session ────────────────────────────────╮", "cyan"),
            ("│ Stage: Resume                                                           │", "cyan"),
            ("│ Track: Programming · Java · 4/40 lessons                                │", "cyan"),
            ("│ Current lesson: Day 5: Loops                                            │", "cyan"),
            ("│ AI: DeepSeek · Model ID: deepseek-v4-flash · DeepSeek V4 Flash          │", "cyan"),
            ("│ Alias: none                                                             │", "cyan"),
            ("│ Next: Enter: resume lesson · Ctrl+P: commands · type: tutor question    │", "cyan"),
            ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ],
        [
            ("╭──────────────────── Stage 1 · Lecture · Day 5: Loops (Java) ───────────╮", "cyan"),
            ("│ Repeat work with for/while loops and trace loop state.                  │", "cyan"),
            ("│ - A loop repeats a block of code so you do not copy-paste lines.        │", "cyan"),
            ("│ - Use for when you know the count; while repeats until false.           │", "cyan"),
            ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
            ("", "white"),
            ("╭────────────────────────────── Java example ─────────────────────────────╮", "green"),
            ("│ for (int n = 1; n <= 5; n++)                                            │", "green"),
            ("│     System.out.println(n);                                              │", "green"),
            ("╰────────────────────────────────────────────────────────────────────────╯", "green"),
        ],
        [
            ("╭──────────────────────── Stage 4 · Review ───────────────────────────────╮", "green"),
            ("│ Hard checks passed: found a loop over the required range and output.    │", "green"),
            ("│ Next: this lesson can advance.                                          │", "green"),
            ("╰────────────────────────────────────────────────────────────────────────╯", "green"),
            ("", "white"),
            ("Marked complete: Loops", "green"),
            ("Next: lesson completion.", "dim"),
        ],
    ]
    height = Y + 10 * LINE_HEIGHT + 46
    frame_svgs = []
    dur = "12s"
    ranges = [
        "1;1;0;0;0",
        "0;1;1;0;0",
        "0;0;1;1;0",
        "0;0;0;1;1",
    ]
    key_times = [
        "0;0.20;0.25;0.95;1",
        "0;0.25;0.45;0.50;1",
        "0;0.50;0.70;0.75;1",
        "0;0.75;0.95;1;1",
    ]
    for frame, values, times in zip(frames, ranges, key_times):
        frame_svgs.append(
            f'<g opacity="0">\n{render_lines(frame)}\n'
            f'<animate attributeName="opacity" values="{values}" keyTimes="{times}" '
            f'dur="{dur}" repeatCount="indefinite"/>\n</g>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Animated Learn terminal walkthrough">
  <rect width="{WIDTH}" height="{height}" rx="18" fill="{COLORS["bg"]}"/>
  <rect x="0" y="0" width="{WIDTH}" height="42" rx="18" fill="{COLORS["panel"]}"/>
  <circle cx="28" cy="21" r="7" fill="#ff5f57"/>
  <circle cx="52" cy="21" r="7" fill="#febc2e"/>
  <circle cx="76" cy="21" r="7" fill="#28c840"/>
  {"".join(frame_svgs)}
</svg>
'''
    (OUT / "learn-demo-walkthrough.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_svg("learn-home.svg", [
        ("AI ENGINEERING", "cyan"),
        ("Programming, ML, RAG, evals, and agentic systems - By Ryu Hemingway", "green"),
        ("Learn programming foundations and applied AI engineering from one terminal.", "dim"),
        ("────────────────────────────────────────────────────────────────────────────", "dim"),
        ("", "white"),
        ("╭──────────────────────────────── Session ────────────────────────────────╮", "cyan"),
        ("│ Stage: Resume                                                           │", "cyan"),
        ("│ Track: Programming · Java · 4/40 lessons                                │", "cyan"),
        ("│ Current lesson: Day 5: Loops                                            │", "cyan"),
        ("│ AI: DeepSeek · Model ID: deepseek-v4-flash · DeepSeek V4 Flash          │", "cyan"),
        ("│ Alias: none                                                             │", "cyan"),
        ("│ Next: Enter: resume lesson · Ctrl+P: commands · type: tutor question    │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ("", "white"),
        ("╭──────────────────────────────── Command ────────────────────────────────╮", "green"),
        ("│ >                                                                      │", "green"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "green"),
        ("Enter: today's lesson | Ctrl+P: commands | type a tutor question", "dim"),
    ])

    write_svg("learn-onboarding-settings.svg", [
        ("Set up your first session", "green"),
        ("", "white"),
        ("╭──────────────────────────── Learning track ────────────────────────────╮", "cyan"),
        ("│ [1] Programming languages  default                                      │", "cyan"),
        ("│ [2] Principles of AI                                                    │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ("╭──────────────────────────────── Language ──────────────────────────────╮", "cyan"),
        ("│ [1] Python  default                                                     │", "cyan"),
        ("│ [2] C                                                                   │", "cyan"),
        ("│ [3] Java                                                                │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ("╭────────────────────────────── AI assistance ───────────────────────────╮", "cyan"),
        ("│ [1] Offline only                                                        │", "cyan"),
        ("│ [2] Local AI (LM Studio)                                                │", "cyan"),
        ("│ [3] Claude  [4] OpenAI  [5] DeepSeek                                    │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ("╭────────────────────────────── DeepSeek model ──────────────────────────╮", "cyan"),
        ("│ [1] DeepSeek V4 Flash (deepseek-v4-flash)  default                      │", "cyan"),
        ("│ [2] DeepSeek V4 Pro (deepseek-v4-pro)                                   │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
    ])

    write_svg("learn-course-map.svg", [
        ("What you can learn", "green"),
        ("", "white"),
        ("╭────────────────────────── Programming languages ───────────────────────╮", "cyan"),
        ("│ Python · C · Java                                                       │", "cyan"),
        ("│ Variables, types, input, conditionals, loops, functions, arrays         │", "cyan"),
        ("│ Strings, hash maps, stacks, two pointers, sliding windows               │", "cyan"),
        ("│ Binary search, classes, linked lists, recursion, trees, graphs          │", "cyan"),
        ("│ Dynamic programming, heaps, matrices, design problems                   │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ("", "white"),
        ("╭──────────────────────────── Principles of AI ──────────────────────────╮", "cyan"),
        ("│ LLM fundamentals · Prompting · Embeddings · RAG · Eval harnesses        │", "cyan"),
        ("│ Agents · Local LLMs · ML basics · Data engineering · Transformers       │", "cyan"),
        ("│ MLOps · Safety, governance, and reliability                             │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
    ])

    write_svg("learn-programming-lesson.svg", [
        ("╭──────────────────── Stage 1 · Lecture · Day 5: Loops (Java) ───────────╮", "cyan"),
        ("│ Repeat work with for/while loops and trace loop state.                  │", "cyan"),
        ("│                                                                        │", "cyan"),
        ("│ - A loop repeats a block of code so you do not copy-paste lines.        │", "cyan"),
        ("│ - Use a 'for' loop when you know how many times or walk a collection.   │", "cyan"),
        ("│ - Use 'while' to repeat until a condition turns false.                  │", "cyan"),
        ("│ - Make sure the loop can end, or it runs forever.                       │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ("", "white"),
        ("╭────────────────────────────── Java example ─────────────────────────────╮", "green"),
        ("│ public class Main {                                                     │", "green"),
        ("│     public static void main(String[] args) {                            │", "green"),
        ("│         for (int n = 1; n <= 5; n++)                                    │", "green"),
        ("│             System.out.println(n);                                      │", "green"),
        ("│     }                                                                   │", "green"),
        ("│ }                                                                       │", "green"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "green"),
    ])

    write_svg("learn-qa-code-review.svg", [
        ("╭──────────────────────── Stage 2 · Question / answer ───────────────────╮", "amber"),
        ("│ What do loops help you avoid writing repeatedly?                        │", "amber"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "amber"),
        ("Type your answer · [a] ask the tutor · [b] back · [p] previous", "dim"),
        ("╭──────────────────────────────── Input ─────────────────────────────────╮", "green"),
        ("│ > helps avoid repeatedly writing the same code                          │", "green"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "green"),
        ("Correct!  Next: coding problem.", "green"),
        ("", "white"),
        ("╭────────────────────────── Stage 3 · Coding problem ────────────────────╮", "cyan"),
        ("│ Use a loop to print the numbers 1 through 10, each on its own line.     │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ("", "white"),
        ("╭──────────────────────────── Stage 4 · Review ──────────────────────────╮", "green"),
        ("│ Hard checks passed: found a loop over the required range and output.    │", "green"),
        ("│ Next: this lesson can advance.                                          │", "green"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "green"),
    ])

    write_svg("learn-command-palette.svg", [
        ("╭──────────────────────────────── Commands ──────────────────────────────╮", "cyan"),
        ("│ [1] Resume today's lesson                                               │", "cyan"),
        ("│ [2] LeetCode practice                                                   │", "cyan"),
        ("│ [3] Ask AI tutor                                                        │", "cyan"),
        ("│ [4] Progress                                                            │", "cyan"),
        ("│ [5] Settings                                                            │", "cyan"),
        ("│ [6] Quit                                                                │", "cyan"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "cyan"),
        ("╭──────────────────────────────── Input ─────────────────────────────────╮", "green"),
        ("│ > settings                                                              │", "green"),
        ("╰────────────────────────────────────────────────────────────────────────╯", "green"),
    ])

    write_animated_svg()
    print(f"Wrote docs media to {OUT}")


if __name__ == "__main__":
    main()
