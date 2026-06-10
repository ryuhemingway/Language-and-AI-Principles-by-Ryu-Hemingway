# Running Local LMs

Local AI mode is useful when you want offline/private help or want to avoid
cloud token costs. The app currently targets LM Studio's OpenAI-compatible local
server.

## LM Studio

1. Download LM Studio from [lmstudio.ai](https://lmstudio.ai/).
2. Download an instruct/chat model.
3. Start the local server.
4. Confirm the endpoint:

```text
http://localhost:1234/v1/chat/completions
```

Then run:

```bash
Learn --ai local
```

The app will show available LM Studio models and let you pick one by number.
That choice is saved in `data/learning_progress.json`.

Official docs:

- [LM Studio](https://lmstudio.ai/)
- [LM Studio local server docs](https://lmstudio.ai/docs/app/api)

## Ollama

Ollama is another popular local model runner. Download it from
[ollama.com](https://ollama.com/).

Example:

```bash
ollama pull llama3.1
ollama run llama3.1
```

Ollama has its own API. This app is currently wired for LM Studio's
OpenAI-compatible `/v1/chat/completions` endpoint. To use Ollama directly, add
an adapter or expose an OpenAI-compatible endpoint in front of Ollama.

Official docs:

- [Ollama](https://ollama.com/)
- [Ollama API docs](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Choosing a Local Model

For a tutoring app, prefer:

- Instruct/chat-tuned models
- Enough context length for lesson + question
- Fast enough responses for interactive use
- Models that follow JSON/format instructions reasonably well

Local models are excellent for explanations, brainstorming, and private notes.
Cloud models are usually stronger for complex reasoning and code review.

