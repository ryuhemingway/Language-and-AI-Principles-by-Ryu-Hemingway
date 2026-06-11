# How To Use Programming Fundamentals and AI

## 1. Install

```bash
python3 -m pip install -r requirements.txt
bash scripts/install.sh
```

If needed, add the launcher directory to your shell path:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 2. Start Learning

```bash
Learn
```

On first launch, choose:

1. Programming languages or Principles of AI
2. A language or AI module
3. Offline, local AI, or cloud AI
4. The exact model when the provider supports model selection
5. A terminal color theme

The app saves progress locally in `data/learning_progress.json`.
After setup, relaunching `Learn` shows a resume header with your active track,
next lesson, AI provider, exact model ID, and the next action. Press Enter to
continue, or press Ctrl+P to open commands.

### What It Looks Like

Resume screen and main input:

![Resume screen with compact session header](docs/assets/learn-home.svg)

First-run setup, settings, and exact model selection:

![First-run setup and model settings](docs/assets/learn-onboarding-settings.svg)

Available courses and modules:

![Programming and Principles of AI course map](docs/assets/learn-course-map.svg)

Lesson and language-specific example:

![Lecture and language-specific example](docs/assets/learn-programming-lesson.svg)

Question, coding problem, and deterministic review:

![Question answer, coding problem, and hard-check review](docs/assets/learn-qa-code-review.svg)

Command discovery with Ctrl+P:

![Ctrl+P command palette](docs/assets/learn-command-palette.svg)

Animated walkthrough:

![Animated terminal walkthrough](docs/assets/learn-demo-walkthrough.svg)

## 3. Programming Track

```bash
Learn --track programming --language python
Learn --track programming --language c
Learn --track programming --language java
```

Each lesson includes:

- Concept explanation
- Language-specific example
- Question/answer quick check
- Coding problem
- Deterministic hard checks before optional AI review
- Optional AI tutor help
- LeetCode unlocks after prerequisites are complete

## 4. Principles of AI Track

```bash
Learn --track ai_principles --module rag
Learn --track ai_principles --module agents
Learn --track ai_principles --module mlops
```

Each module follows the same flow: lecture, question/answer, coding or design
problem, review, then next lesson.

## 5. AI Assistance

Offline mode always works:

```bash
Learn --ai offline
```

Local LM mode uses LM Studio:

```bash
Learn --ai local
```

Cloud mode uses API keys:

```bash
Learn --ai claude
Learn --ai openai
Learn --ai deepseek
```

DeepSeek model selection is constrained to valid known IDs:

- `deepseek-v4-flash`
- `deepseek-v4-pro`

The session header shows the provider, exact model ID, and whether an alias was
normalized.

## 6. LeetCode Practice

```bash
Learn leetcode stats
Learn leetcode list --unlocked
Learn leetcode next
Learn leetcode show 1
Learn leetcode done 1
```

## 7. Resume Later

Progress is saved locally. Start the app again with:

```bash
Learn
```

Then continue the active track, switch tracks from Settings, or use direct
commands such as:

```bash
Learn --track ai_principles --module rag
Learn --track programming --language java
```

## 8. Commands and Tests

Press Ctrl+P from the home prompt to discover secondary actions.

For a quick project demo:

```bash
bash scripts/demo.sh
```

For development checks:

```bash
python3 scripts/terminal_smoke.py
bash scripts/check_generated_docs.sh
```
