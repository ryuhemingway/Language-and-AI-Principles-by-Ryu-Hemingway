# Local LLMs Course Coverage

Total lessons: 5

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What Local LLMs Are

Objective: Understand what runs locally and why you might choose it.

Concepts taught:
- A local LLM runs on your own machine instead of a cloud API.
- Benefits include privacy, offline use, lower marginal cost, and control over models.
- Tradeoffs include weaker models, hardware limits, setup work, and slower inference.

Practice: Install or open LM Studio, download a small instruct model, and run one chat locally.

Quick check: Name one benefit of a local LLM.

## Lesson 2: Models, Quantization, and Context

Objective: Learn the practical vocabulary for choosing a local model.

Concepts taught:
- Model size affects quality, memory use, and speed.
- Quantization compresses weights so models fit on consumer hardware.
- Context length controls how much prompt and history the model can consider.

Practice: Compare two local models by size, quantization, context length, and tokens per second.

Quick check: What does quantization help reduce?

## Lesson 3: Serving a Local Model

Objective: Understand how local apps connect to a local LLM server.

Concepts taught:
- Tools like LM Studio can expose an OpenAI-compatible HTTP endpoint.
- Your app sends messages to localhost and receives model completions.
- The endpoint, model name, timeout, and max tokens belong in configuration.

Practice: Start the LM Studio server and call `/v1/chat/completions` from a small script.

Quick check: Where does a local LLM server usually listen?

## Lesson 4: Prompting and Tool Limits Locally

Objective: Learn how local constraints change application design.

Concepts taught:
- Local models may need shorter prompts, clearer instructions, and smaller context.
- Some local models are weaker at tool calling or strict JSON than cloud models.
- Use validation, retries, and simpler schemas to compensate.

Practice: Create a prompt that asks for strict JSON, then validate and retry once if parsing fails.

Quick check: What should you do when local JSON output is unreliable?

## Lesson 5: Building With Local LLMs

Objective: Learn where local models fit into RAG, agents, and harnesses.

Concepts taught:
- Local models work well for drafts, classification, summarization, and private knowledge workflows.
- RAG can make smaller local models more useful by supplying focused context.
- Harnesses are essential because model quality varies widely across local models.

Practice: Build a local note-answering RAG prototype and evaluate it with 10 fixed questions.

Quick check: What technique can make a smaller local model more useful with private notes?
