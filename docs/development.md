# Development

## Run Locally

```bash
python3 -m pip install -r requirements.txt
python3 learn.py --help
python3 learn.py learn --help
```

## Install Launchers

```bash
bash scripts/install.sh
```

This creates:

```text
~/.local/bin/Learn
~/.local/bin/learn
```

## Verification

```bash
python3 -m py_compile learn.py
python3 -m unittest discover -s tests
python3 learn.py --help
python3 learn.py leetcode stats
```

## Adding Lessons

Programming lessons are controlled by:

- `LESSON_TOPICS`
- `EXAMPLE_SNIPPETS`
- `QUIZ_BY_TOPIC`

Principles of AI lessons are controlled by:

- `AI_MODULES`
- `AI_PRINCIPLES_CURRICULUM`

Each Principles of AI lesson should include:

- `title`
- `objective`
- `fundamentals`
- `build`
- `quiz`
