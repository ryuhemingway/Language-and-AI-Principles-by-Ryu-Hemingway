# LLM fundamentals Course Coverage

Total lessons: 7

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What LLMs Are Good At

Objective: Understand the practical capabilities and limits of large language models.

Concepts taught:
- LLMs predict useful continuations from context; they are not databases, calculators, or proof engines by default.
- They are strong at language transformation, summarization, drafting, classification, code assistance, and pattern completion.
- They are weak when the task requires fresh facts, exact arithmetic, hidden state, strict guarantees, or unsupported private data.

Practice: List five tasks in one app and classify each as good for an LLM, needing tools, or better solved with normal code.

Quick check: What do LLMs primarily use to produce an answer at request time?

## Lesson 2: Tokens, Context Windows, and Cost

Objective: Learn the units that determine latency, cost, and what the model can see.

Concepts taught:
- Text is processed as tokens, not characters or words exactly.
- The context window is the maximum prompt plus output size the model can handle.
- Long prompts increase cost and latency, and can reduce answer quality if they contain irrelevant context.

Practice: Estimate the token budget for a support assistant: system prompt, conversation history, retrieved docs, and answer.

Quick check: What grows when you send a longer prompt to a paid model API?

## Lesson 3: Structured Output and Tool Calling

Objective: Understand how models connect to software systems safely.

Concepts taught:
- Structured outputs make model responses easier to validate and consume in code.
- Tool calling lets a model request a narrow external action instead of pretending it knows the result.
- Schemas, validation, retries, and fallbacks are required because models can still produce invalid outputs.

Practice: Design a JSON schema for a task classifier with fields: category, priority, confidence, and rationale.

Quick check: What should you do before trusting model-generated JSON?

## Lesson 4: Choosing Models

Objective: Learn how to pick models based on task requirements instead of hype.

Concepts taught:
- Match the model to the task: reasoning, coding, extraction, latency, context length, privacy, and cost all matter.
- Small fast models are often enough for classification and extraction; stronger models help with complex reasoning.
- Use evaluation harnesses to compare models on your own tasks before switching production traffic.

Practice: Create a comparison table for three models with cost, latency, context length, quality, and deployment constraints.

Quick check: What should you use to compare models on your own workload?

## Lesson 5: Pretraining, SFT, and model families

Objective: Understand how a raw foundation model becomes an assistant.

Concepts taught:
- Pretraining learns broad language patterns from next-token prediction on massive corpora.
- Supervised fine-tuning adapts the base model to instruction-response pairs and domain tasks.
- Preference tuning and RLHF/GRPO push outputs toward helpful, safer, more preferred answers.
- Model families differ in quality, latency, context length, and deployment constraints.

Example:
```text
base = pretrain(next_token_data)
assistant = sft(base, instruction_pairs)
aligned = preference_tune(assistant, ranked_answers)
```

Practice: Map pretraining, SFT, and preference tuning to the right stage in a model lifecycle.

Quick check: Which stage learns broad language patterns from large corpora?

## Lesson 6: Tokenization, context, and inference controls

Objective: See how text becomes tokens and how sampling settings shape outputs.

Concepts taught:
- Tokenization turns text into units such as BPE, SentencePiece, or WordPiece tokens.
- Context windows cap how much prompt and response history the model can attend to at once.
- Temperature, top-k, top-p, and repetition penalty control randomness and repetition.
- Long prompts cost more and can bury useful context in the middle of the window.

Example:
```text
tokens = tokenizer.encode("explain vector search")
logits = model(tokens, temperature=0.2, top_p=0.9)
print(len(tokens), logits.sample())
```

Practice: Pick an inference setup for a concise assistant, a creative writer, and a code helper.

Quick check: What parameter usually makes output more random?

## Lesson 7: Quantization and deployment tradeoffs

Objective: Choose model sizes and numeric formats with the right latency-quality tradeoff.

Concepts taught:
- Quantization compresses model weights to INT8, INT4, GPTQ, AWQ, or GGUF-style formats.
- Lower-bit models use less memory and can run on smaller hardware, but usually lose some quality.
- The right choice depends on privacy, cost, speed, and acceptable quality loss.
- Common families to know include GPT-4o, Claude, Llama, Mistral, Gemini, Qwen, and DeepSeek.

Example:
```text
model = load_model("gguf", bits=4)
print("lower memory, faster load, slight quality tradeoff")
```

Practice: Compare three deployment choices for a private assistant, a batch job, and a high-quality cloud workflow.

Quick check: What is the main reason to quantize a model?
