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
| `deepseek_model` | DeepSeek model name |
| `deepseek_endpoint` | DeepSeek API endpoint |
| `local_endpoint` | LM Studio local endpoint |
| `local_model` | Optional default local model |

## Environment Variables

You can avoid storing keys in `config.json` by using:

```bash
export ANTHROPIC_API_KEY="..."
export OPENAI_API_KEY="..."
export DEEPSEEK_API_KEY="..."
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

