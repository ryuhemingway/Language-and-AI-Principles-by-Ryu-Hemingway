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
