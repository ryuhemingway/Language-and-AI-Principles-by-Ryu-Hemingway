# Local LLMs Course Coverage

Total lessons: 8

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

Concept check: In one sentence, explain how this idea matters in a real AI system: What Local LLMs Are.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Models, Quantization, and Context.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Serving a Local Model.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Prompting and Tool Limits Locally.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Building With Local LLMs.


## Lesson 6: Local model serving stacks

Objective: Understand the moving parts in a private local LLM workflow.

Context:
Local model serving stacks sits inside Local LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Local serving usually combines a model file, runtime, tokenizer, context settings, and an OpenAI-compatible HTTP endpoint. Tools such as LM Studio, Ollama, llama.cpp, vLLM, and text-generation-inference make different tradeoffs in UX, throughput, and hardware support.

GGUF, GPTQ, AWQ, and other formats affect memory use, loading speed, and model compatibility. A local app should surface endpoint, model, context length, and hardware limits clearly so failures are diagnosable. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Local serving usually combines a model file, runtime, tokenizer, context settings, and an OpenAI-compatible HTTP endpoint.
- Tools such as LM Studio, Ollama, llama.cpp, vLLM, and text-generation-inference make different tradeoffs in UX, throughput, and hardware support.
- GGUF, GPTQ, AWQ, and other formats affect memory use, loading speed, and model compatibility.
- A local app should surface endpoint, model, context length, and hardware limits clearly so failures are diagnosable.

Quick check: What endpoint style do many local model servers mimic?

Concept check: In one sentence, explain how this idea matters in a real AI system: Local model serving stacks.


## Lesson 7: Hardware, context, and throughput planning

Objective: Estimate whether a local model can fit and respond fast enough.

Context:
Hardware, context, and throughput planning sits inside Local LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Model size, quantization, context length, KV cache, and batch size all consume memory. GPU VRAM usually determines the largest fast model, while CPU/RAM fallback trades speed for accessibility.

Long contexts can fail even when the model loads because the KV cache grows during inference. Throughput planning should consider tokens per second, concurrent users, streaming, and timeout behavior. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Model size, quantization, context length, KV cache, and batch size all consume memory.
- GPU VRAM usually determines the largest fast model, while CPU/RAM fallback trades speed for accessibility.
- Long contexts can fail even when the model loads because the KV cache grows during inference.
- Throughput planning should consider tokens per second, concurrent users, streaming, and timeout behavior.

Quick check: What cache grows as context length increases during inference?

Concept check: In one sentence, explain how this idea matters in a real AI system: Hardware, context, and throughput planning.


## Lesson 8: Private offline evaluation

Objective: Test local models without sending learner data to cloud services.

Context:
Private offline evaluation sits inside Local LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Offline evaluation should use local prompts, local answer keys, and saved synthetic cases when real data is sensitive. Small local models need tighter rubrics because they may be weaker judges than frontier cloud models.

Regression sets catch quality drops after changing a model file, quantization, prompt, or context size. Logs should redact learner submissions when the goal is privacy-preserving local assistance. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Offline evaluation should use local prompts, local answer keys, and saved synthetic cases when real data is sensitive.
- Small local models need tighter rubrics because they may be weaker judges than frontier cloud models.
- Regression sets catch quality drops after changing a model file, quantization, prompt, or context size.
- Logs should redact learner submissions when the goal is privacy-preserving local assistance.

Quick check: What kind of test set catches quality drops after changing a local model?

Concept check: In one sentence, explain how this idea matters in a real AI system: Private offline evaluation.
