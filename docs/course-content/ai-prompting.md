# Prompt engineering Course Coverage

Total lessons: 7

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Instructions, Context, and Output Contracts

Objective: Learn the three parts every reliable prompt needs.

Concepts taught:
- Instructions define the role, goal, constraints, and decision rules.
- Context supplies task-specific facts the model should use.
- The output contract defines format, fields, tone, length, and refusal behavior.

Practice: Rewrite a vague prompt into sections: task, constraints, context, output format, and examples.

Quick check: What part of a prompt defines the response format?

## Lesson 2: Few-Shot Examples

Objective: Understand when examples beat abstract instructions.

Concepts taught:
- Few-shot examples show the model exactly how inputs should map to outputs.
- Examples are especially useful for style, classification boundaries, and structured extraction.
- Bad or inconsistent examples can teach the wrong behavior.

Practice: Write three input/output examples for classifying support tickets by urgency.

Quick check: What do few-shot examples demonstrate?

## Lesson 3: Context Management

Objective: Learn how to keep prompts focused as applications grow.

Concepts taught:
- Do not send everything; send the smallest relevant context that supports the task.
- Summarize or retrieve old conversation history instead of blindly appending it forever.
- Separate durable instructions from volatile user data and retrieved facts.

Practice: Design a memory policy for a tutor: what to keep, summarize, retrieve, and discard.

Quick check: What kind of context should you prefer in a model prompt?

## Lesson 4: Prompt Debugging

Objective: Learn how to improve prompts systematically.

Concepts taught:
- Change one thing at a time and test against fixed examples.
- Prompt failures often come from missing constraints, ambiguous terms, conflicting instructions, or weak examples.
- A prompt is production code: version it, evaluate it, and review changes.

Practice: Take one failing prompt output and write a hypothesis, prompt change, and expected improvement.

Quick check: What should stay fixed while debugging prompt changes?

## Lesson 5: Zero-shot, few-shot, and chain-of-thought

Objective: Use examples and reasoning cues deliberately instead of hoping the model infers intent.

Concepts taught:
- Zero-shot prompts rely on instructions alone.
- Few-shot prompts add examples that show the desired input-to-output pattern.
- Chain-of-thought prompting can improve reasoning on multi-step tasks.
- Self-consistency samples multiple reasoning paths and chooses the most stable answer.

Example:
```text
zero_shot = prompt("classify this ticket")
few_shot = prompt("classify this ticket", examples=[...])
cot = prompt("reason step by step, then answer")
```

Practice: Rewrite one vague prompt three ways: zero-shot, few-shot, and reasoning-focused.

Quick check: What does few-shot prompting add?

## Lesson 6: System prompts, templates, and structured output

Objective: Separate instructions, context, and output contracts so prompts stay reliable.

Concepts taught:
- System prompts set role and policy, while user prompts carry the task request.
- Prompt templates keep variable injection consistent across repeated calls.
- Structured output can be JSON, XML, or a typed schema such as Pydantic.
- A good output contract defines fields, format, length, and refusal behavior.

Example:
```text
system = "You are a concise tutor."
user = "Return JSON with fields: answer, confidence, rationale."
schema = {"answer": "string", "confidence": "number"}
```

Practice: Turn a loose instruction into a role, context, and schema-based prompt.

Quick check: What part of a prompt defines the response format?

## Lesson 7: ReAct, self-consistency, and injection defense

Objective: Teach the model when to think, when to call tools, and how to resist hostile instructions.

Concepts taught:
- ReAct interleaves reasoning and acting so the model can inspect results before continuing.
- Prompt injection tries to override instructions or manipulate tool use.
- Defensive prompting narrows tool authority and tells the model what not to trust.
- Majority voting and self-consistency help stabilize noisy answers.

Example:
```text
thought = plan(question)
if need_tool(thought):
    result = call_tool(tool_schema)
answer = synthesize(thought, result)
```

Practice: Write a prompt that uses tools only when needed and ignores untrusted instructions in retrieved text.

Quick check: What attack tries to override the model's instructions?
