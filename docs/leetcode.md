# LeetCode Practice

The app includes a 200-problem LeetCode catalog.

```bash
Learn leetcode stats
Learn leetcode list --unlocked
Learn leetcode next
Learn leetcode show 1
Learn leetcode done 1
```

## How Unlocks Work

Programming lessons mark concept topics complete. LeetCode problems have
prerequisites such as:

- loops
- arrays
- hash maps
- binary search
- recursion
- trees
- graphs
- dynamic programming

When prerequisites are complete, problems appear in `Learn leetcode next` and
inside the interactive tutor.

## Problem Sources

The catalog currently ships as 200 curated LeetCode URL entries. A problem is
shown as local only when its catalog entry includes a readable local prompt or
starter file path for the selected language.

Use `Learn leetcode show <id-or-number>` to view the catalog metadata and URL.
If a future entry includes a local prompt file, the same command prints that
prompt directly.

The catalog lives at:

```text
data/leetcode_catalog.json
```

Progress lives at:

```text
data/leetcode_progress.json
```

Reset saved practice state with:

```bash
Learn reset-progress --leetcode-only
```
