#!/usr/bin/env python3
"""Scripted terminal smoke tests for Learn.

The tests run the real CLI with piped input and isolated progress/config files.
They intentionally avoid live model calls so CI stays deterministic.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEARN = ROOT / "learn.py"


def _write_test_config(path: Path, overrides: dict | None = None) -> None:
    example = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))
    example.update({
        "anthropic_api_key": "",
        "openai_api_key": "",
        "deepseek_api_key": "",
        "local_model": "",
    })
    if overrides:
        example.update(overrides)
    path.write_text(json.dumps(example, indent=2) + "\n", encoding="utf-8")


def make_env(tmp_path: Path, config_overrides: dict | None = None) -> dict[str, str]:
    config_path = tmp_path / "config.json"
    progress_dir = tmp_path / "progress"
    progress_dir.mkdir(exist_ok=True)
    _write_test_config(config_path, config_overrides)
    return {
        **os.environ,
        "NO_COLOR": "1",
        "LEARN_CONFIG_PATH": str(config_path),
        "LEARN_PROGRESS_DIR": str(progress_dir),
        "COLUMNS": "120",
    }


def run_process(name: str, args: list[str], stdin: str, expected: list[str], env: dict[str, str],
                absent: list[str] | None = None) -> str:
    proc = subprocess.run(
        [sys.executable, str(LEARN), *args],
        input=stdin,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env=env,
        timeout=30,
    )
    output = proc.stdout + proc.stderr
    if proc.returncode != 0:
        raise AssertionError(f"{name} exited {proc.returncode}\n{output}")
    missing = [needle for needle in expected if needle not in output]
    if missing:
        raise AssertionError(f"{name} missing expected text: {missing}\n{output}")
    forbidden = [needle for needle in (absent or []) if needle in output]
    if forbidden:
        raise AssertionError(f"{name} contained forbidden text: {forbidden}\n{output}")
    print(f"ok {name}")
    return output


def run_case(
    name: str,
    args: list[str],
    stdin: str,
    expected: list[str],
    absent: list[str] | None = None,
    config_overrides: dict | None = None,
) -> str:
    with tempfile.TemporaryDirectory(prefix=f"learn-smoke-{name}-") as tmp:
        return run_process(
            name,
            args,
            stdin,
            expected,
            make_env(Path(tmp), config_overrides=config_overrides),
            absent=absent,
        )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="learn-smoke-resume-") as tmp:
        env = make_env(Path(tmp))
        run_process(
            "startup-onboarding",
            ["learn"],
            "1\n1\n1\n1\nq\n",
            [
                "Set up your first session",
                "Stage: Resume",
                "Track: Programming",
                "AI: Offline only",
                "Saved. See you next session.",
            ],
            env,
        )
        run_process(
            "resume-without-onboarding",
            ["learn"],
            "q\n",
            ["Stage: Resume", "Current lesson: Day 1", "Saved. See you next session."],
            env,
            absent=["Set up your first session"],
        )
    run_case(
        "command-palette",
        ["learn", "--track", "programming", "--language", "python", "--ai", "offline"],
        "?\n6\n",
        ["Commands", "Resume today's lesson", "Settings", "Quit"],
    )
    run_case(
        "settings-flow",
        ["learn", "--track", "programming", "--language", "python", "--ai", "offline"],
        "settings\n1\n2\n1\n1\nq\n",
        ["Learning track:", "Language:", "Track: Programming · C", "Saved. See you next session."],
    )
    run_case(
        "deepseek-model-picker",
        ["learn", "--track", "programming", "--language", "python", "--ai", "deepseek"],
        "1\nq\n",
        [
            "Saved DeepSeek model",
            "DeepSeek model",
            "DeepSeek V4 Flash (deepseek-v4-flash)",
            "Alias: none",
            "AI: DeepSeek · Model ID: deepseek-v4-flash",
            "Stage: Resume",
            "Saved. See you next session.",
        ],
        config_overrides={"deepseek_model": "deepseek-legacy-beta"},
    )
    run_case(
        "lesson-question-code-review",
        ["learn", "--track", "programming", "--language", "python", "--ai", "offline"],
        "\n\nstore a value\n\nname = \"Alex\"\nage = 21\nprint(name, age)\n:done\nb\nq\n",
        [
            "Stage 1 · Lecture",
            "Stage 2 · Question / answer",
            "Correct!",
            "Stage 3 · Coding problem",
            "Stage 4 · Review",
            "Hard checks passed",
            "Marked complete",
        ],
    )
    run_case(
        "ai-rag-concept-check",
        ["learn", "--track", "ai_principles", "--module", "rag", "--ai", "offline"],
        "\nrelevant context\nRAG helps when facts are fresh or private and need citations.\nb\nq\n",
        [
            "Stage 1 · Lecture",
            "Stage 2 · Question / answer",
            "Correct!",
            "Stage 3 · Concept check",
            "When is RAG a better choice than prompting alone?",
            "Good concept check.",
            "Marked complete",
        ],
        absent=[
            "Stage 3 · Coding problem",
            "Code editor",
            "Sketch a pipeline",
        ],
    )


if __name__ == "__main__":
    main()
