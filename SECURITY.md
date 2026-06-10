# Security

Do not commit real API keys or personal profile data.

This repository intentionally ignores:

- `config.json`
- `profile.md`
- `deadlines.json`
- `skills.json`
- generated `output/`
- saved progress files

Use `config.example.json` as the public template and keep real credentials in
your local `config.json` or environment variables.

Supported environment variables:

- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `DEEPSEEK_API_KEY`

If you accidentally committed a key, revoke it in the provider dashboard before
removing it from Git history.

