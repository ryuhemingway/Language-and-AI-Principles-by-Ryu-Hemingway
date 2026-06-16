# Cloud API Keys

Cloud AI assistance is optional. Offline and local LM modes work without cloud
keys.

## Anthropic Claude

1. Go to the [Anthropic Console](https://console.anthropic.com/).
2. Open API keys.
3. Create a key.
4. Add it to your shell or `config.json`.

Environment variable:

```bash
export ANTHROPIC_API_KEY="your_key_here"
```

Config field:

```json
{
  "anthropic_api_key": "your_key_here",
  "anthropic_model": "claude-sonnet-4-20250514"
}
```

Official docs:

- [Anthropic Console](https://console.anthropic.com/)
- [Anthropic API docs](https://docs.anthropic.com/)

Anthropic model IDs are date-coded and can change. Keep
`anthropic_model` aligned with the current Anthropic docs for your account.

## OpenAI

1. Go to the [OpenAI Platform](https://platform.openai.com/).
2. Open API keys.
3. Create a new secret key.
4. Add it to your shell or `config.json`.

Environment variable:

```bash
export OPENAI_API_KEY="your_key_here"
```

Config fields:

```json
{
  "openai_api_key": "your_key_here",
  "openai_model": "gpt-4.1-mini",
  "openai_endpoint": "https://api.openai.com/v1/chat/completions"
}
```

Official docs:

- [OpenAI Platform](https://platform.openai.com/)
- [OpenAI API documentation](https://platform.openai.com/docs)
- [OpenAI API keys](https://platform.openai.com/api-keys)

OpenAI model availability changes over time. Verify the current model list
before changing production configs.

## DeepSeek

1. Go to the [DeepSeek Platform](https://platform.deepseek.com/).
2. Open API keys.
3. Create a key.
4. Add it to your shell or `config.json`.

Environment variable:

```bash
export DEEPSEEK_API_KEY="your_key_here"
```

Config fields:

```json
{
  "deepseek_api_key": "your_key_here",
  "deepseek_model": "deepseek-v4-flash",
  "deepseek_endpoint": "https://api.deepseek.com/v1/chat/completions"
}
```

The Learn setup flow only allows supported DeepSeek choices:

- `deepseek-v4-flash`
- `deepseek-v4-pro`

Legacy aliases such as `deepseek-chat` are normalized and shown in the session
header so you know the exact model ID being used.

Official docs:

- [DeepSeek Platform](https://platform.deepseek.com/)
- [DeepSeek API docs](https://api-docs.deepseek.com/)

## Key Safety

- Never commit keys.
- Prefer environment variables for shared machines.
- Revoke keys immediately if they are exposed.
- Use separate keys for development and production.
