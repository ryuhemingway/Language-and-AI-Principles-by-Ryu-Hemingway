# AI deployment and MLOps Course Coverage

Total lessons: 4

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Serving AI Systems

Objective: Understand what it means to deploy models and AI workflows.

Concepts taught:
- Serving turns a model or workflow into an API, batch job, CLI, or embedded app feature.
- Production systems need timeouts, retries, rate limits, fallbacks, and structured errors.
- Latency and cost are product constraints, not afterthoughts.

Practice: Design an API response shape for an AI endpoint including result, citations, latency, cost, and error fields.

Quick check: Name one production control for model API calls.

## Lesson 2: Experiment Tracking and Versioning

Objective: Learn how teams keep AI changes reproducible.

Concepts taught:
- Track datasets, prompts, model versions, hyperparameters, code commits, metrics, and eval results.
- Without versioning, you cannot explain why behavior changed.
- Prompt versions and retrieval index versions matter just like model versions.

Practice: Create a release checklist for a prompt/RAG change with versions and evaluation results.

Quick check: What do you need to explain why behavior changed?

## Lesson 3: Monitoring and Drift

Objective: Understand what to watch after deployment.

Concepts taught:
- Monitor latency, cost, errors, refusal rates, retrieval quality, user feedback, and task success.
- Data drift means production inputs differ from what the system was tested on.
- Silent quality regressions require sampled review, eval replay, and alerting.

Practice: Define five metrics for a production RAG assistant dashboard.

Quick check: What is it called when production inputs change from test data?

## Lesson 4: Human Review and Rollouts

Objective: Learn how to ship AI features safely.

Concepts taught:
- Use staged rollouts, feature flags, shadow traffic, and human review for risky changes.
- High-stakes outputs may need approval before users see or act on them.
- Keep rollback paths simple because AI failures are often discovered from examples.

Practice: Plan a rollout for a customer-support AI feature from internal beta to full release.

Quick check: What lets you turn an AI feature off quickly?
