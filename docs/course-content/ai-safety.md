# AI safety, governance, and reliability Course Coverage

Total lessons: 7

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

Concept check: In one sentence, explain how this idea matters in a real AI system: Threat Models for AI Apps.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Permissions and Least Privilege.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Privacy and Data Governance.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Bias, Reliability, and Responsible Use.


## Lesson 5: Prompt injection defenses

Objective: Design systems that treat retrieved or user-supplied text as untrusted evidence.

Context:
Prompt injection defenses sits inside AI safety, governance, and reliability. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Prompt injection often hides instructions inside user text, retrieved documents, web pages, or tool outputs. Defenses separate trusted instructions from untrusted evidence and explicitly limit what context can authorize.

Tool calls should validate arguments, permission scopes, and user intent before taking action. Good safety reviews test indirect injection, exfiltration attempts, and instructions that conflict with system policy. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Prompt injection often hides instructions inside user text, retrieved documents, web pages, or tool outputs.
- Defenses separate trusted instructions from untrusted evidence and explicitly limit what context can authorize.
- Tool calls should validate arguments, permission scopes, and user intent before taking action.
- Good safety reviews test indirect injection, exfiltration attempts, and instructions that conflict with system policy.

Quick check: What should retrieved text be treated as before tool use?

Concept check: In one sentence, explain how this idea matters in a real AI system: Prompt injection defenses.


## Lesson 6: Safety evaluation and incident response

Objective: Prepare for harmful outputs with repeatable tests and operational response.

Context:
Safety evaluation and incident response sits inside AI safety, governance, and reliability. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Safety evals should include jailbreaks, harmful instructions, privacy leaks, bias, and high-stakes uncertainty. Incident response starts with severity, containment, user impact, root cause, and corrective actions.

Red-team findings become regression tests so old failures do not return silently. Post-incident reviews should update prompts, tools, data filters, monitoring, and escalation paths. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Safety evals should include jailbreaks, harmful instructions, privacy leaks, bias, and high-stakes uncertainty.
- Incident response starts with severity, containment, user impact, root cause, and corrective actions.
- Red-team findings become regression tests so old failures do not return silently.
- Post-incident reviews should update prompts, tools, data filters, monitoring, and escalation paths.

Quick check: What testing practice turns discovered failures into future checks?

Concept check: In one sentence, explain how this idea matters in a real AI system: Safety evaluation and incident response.


## Lesson 7: Privacy-by-design controls

Objective: Build privacy controls into data flow instead of adding them after launch.

Context:
Privacy-by-design controls sits inside AI safety, governance, and reliability. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Data minimization collects only what the AI feature needs for a clear purpose. Redaction and tokenization reduce exposure before logs, prompts, and analytics are stored.

Retention limits and deletion workflows must cover prompts, files, embeddings, cached answers, and eval traces. Access reviews keep sensitive learner data available only to the people and systems that need it. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Data minimization collects only what the AI feature needs for a clear purpose.
- Redaction and tokenization reduce exposure before logs, prompts, and analytics are stored.
- Retention limits and deletion workflows must cover prompts, files, embeddings, cached answers, and eval traces.
- Access reviews keep sensitive learner data available only to the people and systems that need it.

Quick check: What principle says to collect only the data the feature needs?

Concept check: In one sentence, explain how this idea matters in a real AI system: Privacy-by-design controls.
