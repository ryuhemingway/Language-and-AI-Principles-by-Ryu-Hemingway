# AI deployment and MLOps Course Coverage

Total lessons: 4

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Serving AI Systems

Objective: Understand what it means to deploy models and AI workflows.

Context:
Serving AI Systems sits inside AI deployment and MLOps. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Serving turns a model or workflow into an API, batch job, CLI, or embedded app feature. Production systems need timeouts, retries, rate limits, fallbacks, and structured errors.

Latency and cost are product constraints, not afterthoughts. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Serving turns a model or workflow into an API, batch job, CLI, or embedded app feature.
- Production systems need timeouts, retries, rate limits, fallbacks, and structured errors.
- Latency and cost are product constraints, not afterthoughts.

Quick check: Name one production control for model API calls.

Coding problem: Design an API response shape for an AI endpoint including result, citations, latency, cost, and error fields.


## Lesson 2: Experiment Tracking and Versioning

Objective: Learn how teams keep AI changes reproducible.

Context:
Experiment Tracking and Versioning sits inside AI deployment and MLOps. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Track datasets, prompts, model versions, hyperparameters, code commits, metrics, and eval results. Without versioning, you cannot explain why behavior changed.

Prompt versions and retrieval index versions matter just like model versions. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Track datasets, prompts, model versions, hyperparameters, code commits, metrics, and eval results.
- Without versioning, you cannot explain why behavior changed.
- Prompt versions and retrieval index versions matter just like model versions.

Quick check: What do you need to explain why behavior changed?

Coding problem: Create a release checklist for a prompt/RAG change with versions and evaluation results.


## Lesson 3: Monitoring and Drift

Objective: Understand what to watch after deployment.

Context:
Monitoring and Drift sits inside AI deployment and MLOps. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Monitor latency, cost, errors, refusal rates, retrieval quality, user feedback, and task success. Data drift means production inputs differ from what the system was tested on.

Silent quality regressions require sampled review, eval replay, and alerting. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Monitor latency, cost, errors, refusal rates, retrieval quality, user feedback, and task success.
- Data drift means production inputs differ from what the system was tested on.
- Silent quality regressions require sampled review, eval replay, and alerting.

Quick check: What is it called when production inputs change from test data?

Coding problem: Define five metrics for a production RAG assistant dashboard.


## Lesson 4: Human Review and Rollouts

Objective: Learn how to ship AI features safely.

Context:
Human Review and Rollouts sits inside AI deployment and MLOps. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Use staged rollouts, feature flags, shadow traffic, and human review for risky changes. High-stakes outputs may need approval before users see or act on them.

Keep rollback paths simple because AI failures are often discovered from examples. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Use staged rollouts, feature flags, shadow traffic, and human review for risky changes.
- High-stakes outputs may need approval before users see or act on them.
- Keep rollback paths simple because AI failures are often discovered from examples.

Quick check: What lets you turn an AI feature off quickly?

Coding problem: Plan a rollout for a customer-support AI feature from internal beta to full release.
