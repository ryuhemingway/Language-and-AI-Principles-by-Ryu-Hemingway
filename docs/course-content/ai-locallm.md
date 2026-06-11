# Local LLMs Course Coverage

Total lessons: 5

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What Local LLMs Are

Objective: Understand what runs locally and why you might choose it.

Context:
What Local LLMs Are sits inside Local LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

A local LLM runs on your own machine instead of a cloud API. Benefits include privacy, offline use, lower marginal cost, and control over models.

Tradeoffs include weaker models, hardware limits, setup work, and slower inference. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- A local LLM runs on your own machine instead of a cloud API.
- Benefits include privacy, offline use, lower marginal cost, and control over models.
- Tradeoffs include weaker models, hardware limits, setup work, and slower inference.

Quick check: Name one benefit of a local LLM.

Coding problem: Install or open LM Studio, download a small instruct model, and run one chat locally.


## Lesson 2: Models, Quantization, and Context

Objective: Learn the practical vocabulary for choosing a local model.

Context:
Models, Quantization, and Context sits inside Local LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Model size affects quality, memory use, and speed. Quantization compresses weights so models fit on consumer hardware.

Context length controls how much prompt and history the model can consider. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Model size affects quality, memory use, and speed.
- Quantization compresses weights so models fit on consumer hardware.
- Context length controls how much prompt and history the model can consider.

Quick check: What does quantization help reduce?

Coding problem: Compare two local models by size, quantization, context length, and tokens per second.


## Lesson 3: Serving a Local Model

Objective: Understand how local apps connect to a local LLM server.

Context:
Serving a Local Model sits inside Local LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Tools like LM Studio can expose an OpenAI-compatible HTTP endpoint. Your app sends messages to localhost and receives model completions.

The endpoint, model name, timeout, and max tokens belong in configuration. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Tools like LM Studio can expose an OpenAI-compatible HTTP endpoint.
- Your app sends messages to localhost and receives model completions.
- The endpoint, model name, timeout, and max tokens belong in configuration.

Quick check: Where does a local LLM server usually listen?

Coding problem: Start the LM Studio server and call `/v1/chat/completions` from a small script.


## Lesson 4: Prompting and Tool Limits Locally

Objective: Learn how local constraints change application design.

Context:
Prompting and Tool Limits Locally sits inside Local LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Local models may need shorter prompts, clearer instructions, and smaller context. Some local models are weaker at tool calling or strict JSON than cloud models.

Use validation, retries, and simpler schemas to compensate. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Local models may need shorter prompts, clearer instructions, and smaller context.
- Some local models are weaker at tool calling or strict JSON than cloud models.
- Use validation, retries, and simpler schemas to compensate.

Quick check: What should you do when local JSON output is unreliable?

Coding problem: Create a prompt that asks for strict JSON, then validate and retry once if parsing fails.


## Lesson 5: Building With Local LLMs

Objective: Learn where local models fit into RAG, agents, and harnesses.

Context:
Building With Local LLMs sits inside Local LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Local models work well for drafts, classification, summarization, and private knowledge workflows. RAG can make smaller local models more useful by supplying focused context.

Harnesses are essential because model quality varies widely across local models. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Local models work well for drafts, classification, summarization, and private knowledge workflows.
- RAG can make smaller local models more useful by supplying focused context.
- Harnesses are essential because model quality varies widely across local models.

Quick check: What technique can make a smaller local model more useful with private notes?

Coding problem: Build a local note-answering RAG prototype and evaluate it with 10 fixed questions.
