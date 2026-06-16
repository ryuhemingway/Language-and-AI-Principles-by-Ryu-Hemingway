# Contributing

This is a small single-file CLI plus data and documentation.

Before opening a pull request:

1. Run `python3 -m py_compile learn.py`.
2. Run `python3 -m unittest discover -s tests`.
3. Start the tutor with `Learn --help`.
4. Avoid committing local config, progress, or generated HTML.
5. Keep lessons practical: each lesson should include fundamentals, a build
   practice, and a short quiz.

Curriculum data currently lives in `learn.py` so the app works without a
database or build step.
