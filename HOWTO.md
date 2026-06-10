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

The app saves progress locally in `data/learning_progress.json`.

## 3. Programming Track

```bash
Learn --track programming --language python
Learn --track programming --language c
Learn --track programming --language java
```

Each lesson includes:

- Concept explanation
- Language-specific example
- Practice target
- Quiz
- Optional AI tutor help
- LeetCode unlocks after prerequisites are complete

## 4. Principles of AI Track

```bash
Learn --track ai_principles --module rag
Learn --track ai_principles --module agents
Learn --track ai_principles --module mlops
```

Each module includes fundamentals, build practice, quizzes, and optional AI
assistance.

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

## 6. LeetCode Practice

```bash
brief leetcode stats
brief leetcode list --unlocked
brief leetcode next
brief leetcode show 1
brief leetcode done 1
```

## 7. Daily Brief

```bash
brief
brief -p claude
brief -p openai
brief -p deepseek
brief -p local
brief --no-open
```

The daily brief reads local context, generates an HTML briefing, and saves it to
`output/`.

