# Neural nets, transformers, and LLMs Course Coverage

Total lessons: 8

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Neural Networks in Plain Terms

Objective: Understand the basic shape of deep learning before transformers.

Context:
Neural Networks in Plain Terms sits inside Neural nets, transformers, and LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

A neural network is a stack of parameterized transformations trained to reduce loss. Gradient descent updates parameters based on how much they contributed to error.

Deep learning works well when there is enough data, compute, and structure to learn useful representations. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- A neural network is a stack of parameterized transformations trained to reduce loss.
- Gradient descent updates parameters based on how much they contributed to error.
- Deep learning works well when there is enough data, compute, and structure to learn useful representations.

Quick check: What process updates model parameters to reduce loss?

Coding problem: Draw input -> layers -> output -> loss -> gradient update for a classifier.


## Lesson 2: Attention and Transformers

Objective: Learn the key idea that made modern LLMs practical.

Context:
Attention and Transformers sits inside Neural nets, transformers, and LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Attention lets each token weigh information from other tokens in the context. Transformers stack attention and feed-forward layers to build contextual representations.

This architecture scales well and supports parallel training better than older sequence models. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Attention lets each token weigh information from other tokens in the context.
- Transformers stack attention and feed-forward layers to build contextual representations.
- This architecture scales well and supports parallel training better than older sequence models.

Quick check: What mechanism lets tokens weigh other tokens in context?

Coding problem: Explain how the word 'bank' changes meaning depending on nearby context.


## Lesson 3: Pretraining, Fine-Tuning, and Alignment

Objective: Understand the main phases that produce useful AI assistants.

Context:
Pretraining, Fine-Tuning, and Alignment sits inside Neural nets, transformers, and LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Pretraining learns broad language patterns from large corpora. Fine-tuning adapts behavior to tasks, formats, or domains.

Alignment methods improve helpfulness, safety, instruction following, and preference matching. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Pretraining learns broad language patterns from large corpora.
- Fine-tuning adapts behavior to tasks, formats, or domains.
- Alignment methods improve helpfulness, safety, instruction following, and preference matching.

Quick check: Which phase learns broad language patterns from large corpora?

Coding problem: Classify examples as pretraining, supervised fine-tuning, preference tuning, or prompt engineering.


## Lesson 4: Fine-Tuning vs RAG vs Prompting

Objective: Learn when to adapt the model and when to adapt the context.

Context:
Fine-Tuning vs RAG vs Prompting sits inside Neural nets, transformers, and LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Prompting is best for quick behavior changes and low setup cost. RAG is best when answers need external or changing knowledge.

Fine-tuning is best when you need repeated behavior, style, format, or task adaptation not solved by context alone. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Prompting is best for quick behavior changes and low setup cost.
- RAG is best when answers need external or changing knowledge.
- Fine-tuning is best when you need repeated behavior, style, format, or task adaptation not solved by context alone.

Quick check: Which method is usually best for changing private or frequently updated knowledge?

Coding problem: Choose prompting, RAG, or fine-tuning for five scenarios and justify each choice.


## Lesson 5: Neural networks and deep learning foundations

Objective: Understand the building blocks beneath modern LLMs.

Context:
Neural networks and deep learning foundations sits inside Neural nets, transformers, and LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Perceptrons and multi-layer perceptrons turn inputs into learned nonlinear features. Activations such as ReLU, sigmoid, tanh, and softmax make deep networks expressive.

Backpropagation applies the chain rule to compute gradients layer by layer. Optimizers such as SGD, Adam, and AdamW turn gradients into parameter updates. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Perceptrons and multi-layer perceptrons turn inputs into learned nonlinear features.
- Activations such as ReLU, sigmoid, tanh, and softmax make deep networks expressive.
- Backpropagation applies the chain rule to compute gradients layer by layer.
- Optimizers such as SGD, Adam, and AdamW turn gradients into parameter updates.

Quick check: What algorithm computes gradients through the network?

Coding problem: Trace one forward pass and one backward pass through a tiny network.


## Lesson 6: The transformer architecture

Objective: Learn the core architecture that made modern LLMs practical.

Context:
The transformer architecture sits inside Neural nets, transformers, and LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Attention uses query, key, and value vectors to let tokens exchange information. Multi-head attention lets the model track several relationships at once.

Positional encodings give the model a notion of token order. Decoder-only, encoder-only, and encoder-decoder families serve different tasks and training styles. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Attention uses query, key, and value vectors to let tokens exchange information.
- Multi-head attention lets the model track several relationships at once.
- Positional encodings give the model a notion of token order.
- Decoder-only, encoder-only, and encoder-decoder families serve different tasks and training styles.

Quick check: What vectors does attention use?

Coding problem: Explain why attention beats a plain recurrent loop for large-context language modeling.


## Lesson 7: How large language models are trained

Objective: Understand the full training story from pretraining to alignment.

Context:
How large language models are trained sits inside Neural nets, transformers, and LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Pretraining learns next-token prediction or masked language modeling from large corpora. Scaling laws describe how quality changes with data, compute, and parameter count.

Instruction tuning and SFT convert a base model into a more useful assistant. RLHF and newer alignment methods improve preference following and safety. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Pretraining learns next-token prediction or masked language modeling from large corpora.
- Scaling laws describe how quality changes with data, compute, and parameter count.
- Instruction tuning and SFT convert a base model into a more useful assistant.
- RLHF and newer alignment methods improve preference following and safety.

Quick check: Which stage usually uses instruction-response examples?

Coding problem: Explain how pretraining, SFT, and alignment differ in purpose and data shape.


## Lesson 8: Fine-tuning LLMs with PEFT

Objective: Choose fine-tuning, prompting, or RAG with a production mindset.

Context:
Fine-tuning LLMs with PEFT sits inside Neural nets, transformers, and LLMs. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Fine-tuning makes sense when the behavior should be repeated, specialized, or style-critical. PEFT dominates in practice because it adapts fewer parameters at lower cost.

LoRA and QLoRA are the standard low-rank adaptation approaches most engineers should know. RAFT mixes retrieval and fine-tuning when both knowledge grounding and model adaptation matter. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Fine-tuning makes sense when the behavior should be repeated, specialized, or style-critical.
- PEFT dominates in practice because it adapts fewer parameters at lower cost.
- LoRA and QLoRA are the standard low-rank adaptation approaches most engineers should know.
- RAFT mixes retrieval and fine-tuning when both knowledge grounding and model adaptation matter.

Quick check: What does LoRA adapt?

Coding problem: Pick one scenario where fine-tuning is better than prompting and one where RAG is better.
