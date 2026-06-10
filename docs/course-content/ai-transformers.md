# Neural nets, transformers, and LLMs Course Coverage

Total lessons: 8

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Neural Networks in Plain Terms

Objective: Understand the basic shape of deep learning before transformers.

Concepts taught:
- A neural network is a stack of parameterized transformations trained to reduce loss.
- Gradient descent updates parameters based on how much they contributed to error.
- Deep learning works well when there is enough data, compute, and structure to learn useful representations.

Practice: Draw input -> layers -> output -> loss -> gradient update for a classifier.

Quick check: What process updates model parameters to reduce loss?

## Lesson 2: Attention and Transformers

Objective: Learn the key idea that made modern LLMs practical.

Concepts taught:
- Attention lets each token weigh information from other tokens in the context.
- Transformers stack attention and feed-forward layers to build contextual representations.
- This architecture scales well and supports parallel training better than older sequence models.

Practice: Explain how the word 'bank' changes meaning depending on nearby context.

Quick check: What mechanism lets tokens weigh other tokens in context?

## Lesson 3: Pretraining, Fine-Tuning, and Alignment

Objective: Understand the main phases that produce useful AI assistants.

Concepts taught:
- Pretraining learns broad language patterns from large corpora.
- Fine-tuning adapts behavior to tasks, formats, or domains.
- Alignment methods improve helpfulness, safety, instruction following, and preference matching.

Practice: Classify examples as pretraining, supervised fine-tuning, preference tuning, or prompt engineering.

Quick check: Which phase learns broad language patterns from large corpora?

## Lesson 4: Fine-Tuning vs RAG vs Prompting

Objective: Learn when to adapt the model and when to adapt the context.

Concepts taught:
- Prompting is best for quick behavior changes and low setup cost.
- RAG is best when answers need external or changing knowledge.
- Fine-tuning is best when you need repeated behavior, style, format, or task adaptation not solved by context alone.

Practice: Choose prompting, RAG, or fine-tuning for five scenarios and justify each choice.

Quick check: Which method is usually best for changing private or frequently updated knowledge?

## Lesson 5: Neural networks and deep learning foundations

Objective: Understand the building blocks beneath modern LLMs.

Concepts taught:
- Perceptrons and multi-layer perceptrons turn inputs into learned nonlinear features.
- Activations such as ReLU, sigmoid, tanh, and softmax make deep networks expressive.
- Backpropagation applies the chain rule to compute gradients layer by layer.
- Optimizers such as SGD, Adam, and AdamW turn gradients into parameter updates.

Example:
```text
h = relu(W1 @ x + b1)
yhat = softmax(W2 @ h + b2)
loss.backward()
```

Practice: Trace one forward pass and one backward pass through a tiny network.

Quick check: What algorithm computes gradients through the network?

## Lesson 6: The transformer architecture

Objective: Learn the core architecture that made modern LLMs practical.

Concepts taught:
- Attention uses query, key, and value vectors to let tokens exchange information.
- Multi-head attention lets the model track several relationships at once.
- Positional encodings give the model a notion of token order.
- Decoder-only, encoder-only, and encoder-decoder families serve different tasks and training styles.

Example:
```text
q, k, v = project(tokens)
attn = softmax(q @ k.T / sqrt(d)) @ v
```

Practice: Explain why attention beats a plain recurrent loop for large-context language modeling.

Quick check: What vectors does attention use?

## Lesson 7: How large language models are trained

Objective: Understand the full training story from pretraining to alignment.

Concepts taught:
- Pretraining learns next-token prediction or masked language modeling from large corpora.
- Scaling laws describe how quality changes with data, compute, and parameter count.
- Instruction tuning and SFT convert a base model into a more useful assistant.
- RLHF and newer alignment methods improve preference following and safety.

Example:
```text
base = pretrain(corpus)
assistant = sft(base, instruction_pairs)
aligned = rlhf_or_grpo(assistant)
```

Practice: Explain how pretraining, SFT, and alignment differ in purpose and data shape.

Quick check: Which stage usually uses instruction-response examples?

## Lesson 8: Fine-tuning LLMs with PEFT

Objective: Choose fine-tuning, prompting, or RAG with a production mindset.

Concepts taught:
- Fine-tuning makes sense when the behavior should be repeated, specialized, or style-critical.
- PEFT dominates in practice because it adapts fewer parameters at lower cost.
- LoRA and QLoRA are the standard low-rank adaptation approaches most engineers should know.
- RAFT mixes retrieval and fine-tuning when both knowledge grounding and model adaptation matter.

Example:
```text
base = load_model("open-weights")
adapt = lora(base, target_modules=["q_proj", "v_proj"])
finetuned = qlora(base, rank=16)
```

Practice: Pick one scenario where fine-tuning is better than prompting and one where RAG is better.

Quick check: What does LoRA adapt?
