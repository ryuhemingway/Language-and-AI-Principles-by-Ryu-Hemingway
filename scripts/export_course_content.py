#!/usr/bin/env python3
"""Export complete PROGRAM course coverage docs from the runtime curriculum."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import learn  # noqa: E402


OUT_DIR = ROOT / "docs" / "course-content"


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def fence(text: str, language: str = "text") -> list[str]:
    return [f"```{language}", text.rstrip(), "```"]


def write_doc(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def programming_doc(language: str) -> tuple[str, int]:
    label = learn.LEARN_LANGUAGES[language]
    lessons = learn.build_learning_curriculum(language)
    filename = f"programming-{language}.md"
    code_lang = {"python": "python", "c": "c", "java": "java"}[language]

    lines = [
        f"# {label} Programming Course Coverage",
        "",
        f"Total lessons: {len(lessons)}",
        "",
        "This file is generated from `learn.py` and mirrors the CLI lesson order.",
        "",
    ]

    for lesson in lessons:
        topic = lesson["topic"]
        lines += [
            f"## Day {lesson['day']}: {lesson['title']}",
            "",
            f"Objective: {lesson['objective']}",
            "",
            "Concepts taught:",
        ]
        for item in learn.LESSON_EXPLANATIONS.get(topic, []):
            lines.append(f"- {item}")

        example = lesson.get("example", "")
        if example:
            lines += ["", "Example:", *fence(example, code_lang)]

        lines += [
            "",
            f"Practice: {learn.PRACTICE_TASKS.get(topic, '')}",
            "",
            f"Quick check: {lesson['quiz']}",
            "",
        ]

    write_doc(OUT_DIR / filename, lines)
    return filename, len(lessons)


def ai_doc(module: str) -> tuple[str, int]:
    title = learn.AI_MODULES[module]
    lessons = learn._ai_curriculum(module)
    filename = f"ai-{slug(module)}.md"

    lines = [
        f"# {title} Course Coverage",
        "",
        f"Total lessons: {len(lessons)}",
        "",
        "This file is generated from `learn.py` and mirrors the CLI lesson order.",
        "",
    ]

    for lesson in lessons:
        view = learn._ai_lesson_view(module, lesson)
        lines += [
            f"## Lesson {lesson['day']}: {lesson['title']}",
            "",
            f"Objective: {lesson['objective']}",
            "",
            "Context:",
        ]
        for paragraph in view.get("context_paragraphs", []):
            lines += [paragraph, ""]

        lines += ["Key ideas:"]
        for item in lesson.get("fundamentals", []):
            lines.append(f"- {item}")

        quiz, _answers = lesson["quiz"]
        lines += [
            "",
            f"Quick check: {quiz}",
            "",
            f"Coding problem: {lesson.get('build', '')}",
            "",
        ]
        lines.append("")

    write_doc(OUT_DIR / filename, lines)
    return filename, len(lessons)


def index_doc(programming: list[tuple[str, int]], ai: list[tuple[str, str, int]]) -> None:
    lines = [
        "# PROGRAM Course Content Coverage",
        "",
        "These files list the content covered by every PROGRAM course from beginning to end.",
        "They are generated from the same `learn.py` curriculum data used by the terminal app.",
        "",
        "## Programming Courses",
        "",
    ]
    for filename, count in programming:
        label = filename.removeprefix("programming-").removesuffix(".md")
        lines.append(f"- [{label.title()}]({filename}) - {count} lessons")

    lines += ["", "## AI Courses", ""]
    for module, filename, count in ai:
        lines.append(f"- [{learn.AI_MODULES[module]}]({filename}) - {count} lessons")

    lines += [
        "",
        "## Regeneration",
        "",
        "Run this command after editing curriculum data:",
        "",
        "```bash",
        "python3 scripts/export_course_content.py",
        "```",
        "",
    ]
    write_doc(OUT_DIR / "README.md", lines)


def main() -> None:
    programming = [programming_doc(language) for language in learn.LEARN_LANGUAGES]
    ai = []
    for module in learn.AI_MODULES:
        filename, count = ai_doc(module)
        ai.append((module, filename, count))
    index_doc(programming, ai)
    print(f"Wrote course content docs to {OUT_DIR}")


if __name__ == "__main__":
    main()
