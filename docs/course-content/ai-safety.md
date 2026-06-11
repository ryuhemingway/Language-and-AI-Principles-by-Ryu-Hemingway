# AI safety, governance, and reliability Course Coverage

Total lessons: 4

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Threat Models for AI Apps

Objective: Understand the main security risks unique to LLM applications.

Context:
Threat Models for AI Apps sits inside AI safety, governance, and reliability. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Prompt injection tries to override instructions or misuse connected tools. Data exfiltration tries to reveal secrets from prompts, files, tools, or retrieval context.

Unsafe tool use can turn a text mistake into a real external action. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Prompt injection tries to override instructions or misuse connected tools.
- Data exfiltration tries to reveal secrets from prompts, files, tools, or retrieval context.
- Unsafe tool use can turn a text mistake into a real external action.

Quick check: What attack tries to override model instructions?

Coding problem: Write a threat model for a RAG assistant that can read private documents and send emails.


## Lesson 2: Permissions and Least Privilege

Objective: Learn how to limit damage when AI systems call tools.

Context:
Permissions and Least Privilege sits inside AI safety, governance, and reliability. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Tools should have the narrowest permissions required for the task. Separate read-only tools from write/destructive tools.

Require human approval for external side effects such as sending, deleting, buying, or publishing. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Tools should have the narrowest permissions required for the task.
- Separate read-only tools from write/destructive tools.
- Require human approval for external side effects such as sending, deleting, buying, or publishing.

Quick check: What permission principle limits tool damage?

Coding problem: Classify tools in an agent as safe read-only, sensitive read, write, or destructive.


## Lesson 3: Privacy and Data Governance

Objective: Understand how data choices affect users, companies, and compliance.

Context:
Privacy and Data Governance sits inside AI safety, governance, and reliability. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Do not send secrets, regulated data, or private user data to services that are not approved for that data. Log redaction and retention policies matter because prompts often contain sensitive context.

RAG systems need access control so retrieval never exposes documents the user cannot see. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Do not send secrets, regulated data, or private user data to services that are not approved for that data.
- Log redaction and retention policies matter because prompts often contain sensitive context.
- RAG systems need access control so retrieval never exposes documents the user cannot see.

Quick check: What must RAG retrieval enforce for private documents?

Coding problem: Design rules for what your AI tutor is allowed to log, retain, and send to cloud providers.


## Lesson 4: Bias, Reliability, and Responsible Use

Objective: Learn practical engineering responsibilities around model behavior.

Context:
Bias, Reliability, and Responsible Use sits inside AI safety, governance, and reliability. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Models can amplify bias from data, labels, prompts, and evaluation choices. Reliability means knowing when the system should answer, ask for clarification, refuse, or escalate.

Responsible AI is implemented through product constraints, evaluation, monitoring, and user-facing transparency. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Models can amplify bias from data, labels, prompts, and evaluation choices.
- Reliability means knowing when the system should answer, ask for clarification, refuse, or escalate.
- Responsible AI is implemented through product constraints, evaluation, monitoring, and user-facing transparency.

Quick check: What should an AI system do when a task is high-stakes and uncertain?

Coding problem: Add refusal/escalation rules for medical, legal, financial, and safety-critical questions.
