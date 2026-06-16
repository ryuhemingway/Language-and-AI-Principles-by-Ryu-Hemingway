# Configuration

The app reads `config.json` from the repository root. Do not commit this file.

Start from the template:

```bash
cp config.example.json config.json
```

## Provider Fields

| Field | Purpose |
| --- | --- |
| `anthropic_api_key` | Claude/Anthropic API key |
| `anthropic_model` | Claude model name |
| `openai_api_key` | OpenAI API key |
| `openai_model` | OpenAI model name |
| `openai_endpoint` | OpenAI chat completions endpoint |
| `deepseek_api_key` | DeepSeek API key |
| `deepseek_model` | DeepSeek model ID, usually `deepseek-v4-flash` or `deepseek-v4-pro` |
| `deepseek_endpoint` | DeepSeek API endpoint |
| `local_endpoint` | LM Studio local endpoint |
| `local_model` | Optional default local model |
| `anki_connect_url` | URL for a local AnkiConnect server used by study planning features |
| `calendar_lookahead_days` | Number of days the optimizer should scan for upcoming deadlines |
| `git_repos` | Optional local repository paths to include in project/status analysis |
| `synthesizer` | Preferred AI provider for synthesis tasks such as plans or reports |
| `open_browser` | Whether commands that produce local reports may open them in a browser |

Model IDs change over time. The template uses example model IDs for supported
providers, but provider docs should be checked before choosing defaults for a
new setup.

## Environment Variables

You can avoid storing keys in `config.json` by using:

```bash
export ANTHROPIC_API_KEY="..."
export OPENAI_API_KEY="..."
export DEEPSEEK_API_KEY="..."
```

For tests or demos, you can isolate local files:

```bash
export LEARN_CONFIG_PATH="/tmp/learn-config.json"
export LEARN_PROGRESS_DIR="/tmp/learn-progress"
```

## Local Files

These files are intentionally ignored by Git:

- `config.json`
- `profile.md`
- `deadlines.json`
- `skills.json`
- `output/`
- `data/learning_progress.json`
- `data/leetcode_progress.json`

## Progress

Learning progress is saved locally:

```text
data/learning_progress.json
data/leetcode_progress.json
```

Delete those files only if you want to reset progress.

The app also stores `onboarding_complete` so first launch can show setup once
and later launches can resume the active lesson directly.
