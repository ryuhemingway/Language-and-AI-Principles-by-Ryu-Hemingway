# Prompt engineering Course Coverage

Total lessons: 7

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Instructions, Context, and Output Contracts

Objective: Learn the three parts every reliable prompt needs.

Context:
Instructions, Context, and Output Contracts sits inside Prompt engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Instructions define the role, goal, constraints, and decision rules. Context supplies task-specific facts the model should use.

The output contract defines format, fields, tone, length, and refusal behavior. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Instructions define the role, goal, constraints, and decision rules.
- Context supplies task-specific facts the model should use.
- The output contract defines format, fields, tone, length, and refusal behavior.

Quick check: What part of a prompt defines the response format?

Concept check: In one sentence, explain how this idea matters in a real AI system: Instructions, Context, and Output Contracts.


## Lesson 2: Few-Shot Examples

Objective: Understand when examples beat abstract instructions.

Context:
Few-Shot Examples sits inside Prompt engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Few-shot examples show the model exactly how inputs should map to outputs. Examples are especially useful for style, classification boundaries, and structured extraction.

Bad or inconsistent examples can teach the wrong behavior. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Few-shot examples show the model exactly how inputs should map to outputs.
- Examples are especially useful for style, classification boundaries, and structured extraction.
- Bad or inconsistent examples can teach the wrong behavior.

Quick check: What do few-shot examples demonstrate?

Concept check: In one sentence, explain how this idea matters in a real AI system: Few-Shot Examples.


## Lesson 3: Context Management

Objective: Learn how to keep prompts focused as applications grow.

Context:
Context Management sits inside Prompt engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Do not send everything; send the smallest relevant context that supports the task. Summarize or retrieve old conversation history instead of blindly appending it forever.

Separate durable instructions from volatile user data and retrieved facts. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Do not send everything; send the smallest relevant context that supports the task.
- Summarize or retrieve old conversation history instead of blindly appending it forever.
- Separate durable instructions from volatile user data and retrieved facts.

Quick check: What kind of context should you prefer in a model prompt?

Concept check: In one sentence, explain how this idea matters in a real AI system: Context Management.


## Lesson 4: Prompt Debugging

Objective: Learn how to improve prompts systematically.

Context:
Prompt Debugging sits inside Prompt engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Change one thing at a time and test against fixed examples. Prompt failures often come from missing constraints, ambiguous terms, conflicting instructions, or weak examples.

A prompt is production code: version it, evaluate it, and review changes. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Change one thing at a time and test against fixed examples.
- Prompt failures often come from missing constraints, ambiguous terms, conflicting instructions, or weak examples.
- A prompt is production code: version it, evaluate it, and review changes.

Quick check: What should stay fixed while debugging prompt changes?

Concept check: In one sentence, explain how this idea matters in a real AI system: Prompt Debugging.


## Lesson 5: Zero-shot, few-shot, and chain-of-thought

Objective: Use examples and reasoning cues deliberately instead of hoping the model infers intent.

Context:
Zero-shot, few-shot, and chain-of-thought sits inside Prompt engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Zero-shot prompts rely on instructions alone. Few-shot prompts add examples that show the desired input-to-output pattern.

Chain-of-thought prompting can improve reasoning on multi-step tasks. Self-consistency samples multiple reasoning paths and chooses the most stable answer. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Zero-shot prompts rely on instructions alone.
- Few-shot prompts add examples that show the desired input-to-output pattern.
- Chain-of-thought prompting can improve reasoning on multi-step tasks.
- Self-consistency samples multiple reasoning paths and chooses the most stable answer.

Quick check: What does few-shot prompting add?

Concept check: In one sentence, explain how this idea matters in a real AI system: Zero-shot, few-shot, and chain-of-thought.


## Lesson 6: System prompts, templates, and structured output

Objective: Separate instructions, context, and output contracts so prompts stay reliable.

Context:
System prompts, templates, and structured output sits inside Prompt engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

System prompts set role and policy, while user prompts carry the task request. Prompt templates keep variable injection consistent across repeated calls.

Structured output can be JSON, XML, or a typed schema such as Pydantic. A good output contract defines fields, format, length, and refusal behavior. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- System prompts set role and policy, while user prompts carry the task request.
- Prompt templates keep variable injection consistent across repeated calls.
- Structured output can be JSON, XML, or a typed schema such as Pydantic.
- A good output contract defines fields, format, length, and refusal behavior.

Quick check: What keeps variable insertion consistent across repeated prompts?

Concept check: In one sentence, explain how this idea matters in a real AI system: System prompts, templates, and structured output.


## Lesson 7: ReAct, self-consistency, and injection defense

Objective: Teach the model when to think, when to call tools, and how to resist hostile instructions.

Context:
ReAct, self-consistency, and injection defense sits inside Prompt engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

ReAct interleaves reasoning and acting so the model can inspect results before continuing. Prompt injection tries to override instructions or manipulate tool use.

Defensive prompting narrows tool authority and tells the model what not to trust. Majority voting and self-consistency help stabilize noisy answers. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- ReAct interleaves reasoning and acting so the model can inspect results before continuing.
- Prompt injection tries to override instructions or manipulate tool use.
- Defensive prompting narrows tool authority and tells the model what not to trust.
- Majority voting and self-consistency help stabilize noisy answers.

Quick check: What narrows tool authority when retrieved text may be hostile?

Concept check: In one sentence, explain how this idea matters in a real AI system: ReAct, self-consistency, and injection defense.
