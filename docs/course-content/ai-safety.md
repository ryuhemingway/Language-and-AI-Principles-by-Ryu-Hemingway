# AI safety, governance, and reliability Course Coverage

Total lessons: 4

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Threat Models for AI Apps

Objective: Understand the main security risks unique to LLM applications.

Concepts taught:
- Prompt injection tries to override instructions or misuse connected tools.
- Data exfiltration tries to reveal secrets from prompts, files, tools, or retrieval context.
- Unsafe tool use can turn a text mistake into a real external action.

Practice: Write a threat model for a RAG assistant that can read private documents and send emails.

Quick check: What attack tries to override model instructions?

## Lesson 2: Permissions and Least Privilege

Objective: Learn how to limit damage when AI systems call tools.

Concepts taught:
- Tools should have the narrowest permissions required for the task.
- Separate read-only tools from write/destructive tools.
- Require human approval for external side effects such as sending, deleting, buying, or publishing.

Practice: Classify tools in an agent as safe read-only, sensitive read, write, or destructive.

Quick check: What permission principle limits tool damage?

## Lesson 3: Privacy and Data Governance

Objective: Understand how data choices affect users, companies, and compliance.

Concepts taught:
- Do not send secrets, regulated data, or private user data to services that are not approved for that data.
- Log redaction and retention policies matter because prompts often contain sensitive context.
- RAG systems need access control so retrieval never exposes documents the user cannot see.

Practice: Design rules for what your AI tutor is allowed to log, retain, and send to cloud providers.

Quick check: What must RAG retrieval enforce for private documents?

## Lesson 4: Bias, Reliability, and Responsible Use

Objective: Learn practical engineering responsibilities around model behavior.

Concepts taught:
- Models can amplify bias from data, labels, prompts, and evaluation choices.
- Reliability means knowing when the system should answer, ask for clarification, refuse, or escalate.
- Responsible AI is implemented through product constraints, evaluation, monitoring, and user-facing transparency.

Practice: Add refusal/escalation rules for medical, legal, financial, and safety-critical questions.

Quick check: What should an AI system do when a task is high-stakes and uncertain?
