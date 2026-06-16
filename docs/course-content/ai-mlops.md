# AI deployment and MLOps Course Coverage

Total lessons: 7

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

Concept check: In one sentence, explain how this idea matters in a real AI system: Serving AI Systems.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Experiment Tracking and Versioning.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Monitoring and Drift.


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

Concept check: In one sentence, explain how this idea matters in a real AI system: Human Review and Rollouts.


## Lesson 5: Model packaging and promotion

Objective: Move models from experiment to production with traceable artifacts.

Context:
Model packaging and promotion sits inside AI deployment and MLOps. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Packaging should record code version, model weights, tokenizer, dependency versions, config, and evaluation results. A model registry tracks candidates, approvals, owners, and promotion state such as staging or production.

Promotion gates should compare the candidate against a baseline before traffic changes. Rollback is easier when every deployed model has immutable artifact IDs and documented serving requirements. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Packaging should record code version, model weights, tokenizer, dependency versions, config, and evaluation results.
- A model registry tracks candidates, approvals, owners, and promotion state such as staging or production.
- Promotion gates should compare the candidate against a baseline before traffic changes.
- Rollback is easier when every deployed model has immutable artifact IDs and documented serving requirements.

Quick check: What system tracks model artifacts and promotion state?

Concept check: In one sentence, explain how this idea matters in a real AI system: Model packaging and promotion.


## Lesson 6: Monitoring drift and feedback loops

Objective: Watch deployed AI systems for changing data and changing behavior.

Context:
Monitoring drift and feedback loops sits inside AI deployment and MLOps. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Data drift means production inputs stop looking like training or evaluation inputs. Concept drift means the relationship between inputs and desired outputs changes.

Feedback loops can reinforce model mistakes when generated outputs become future training or ranking data. Monitoring should connect latency, cost, quality, safety incidents, and user feedback to deployment decisions. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Data drift means production inputs stop looking like training or evaluation inputs.
- Concept drift means the relationship between inputs and desired outputs changes.
- Feedback loops can reinforce model mistakes when generated outputs become future training or ranking data.
- Monitoring should connect latency, cost, quality, safety incidents, and user feedback to deployment decisions.

Quick check: What drift means production inputs changed distribution?

Concept check: In one sentence, explain how this idea matters in a real AI system: Monitoring drift and feedback loops.


## Lesson 7: Canary releases and rollback

Objective: Deploy AI changes gradually so failures affect fewer users.

Context:
Canary releases and rollback sits inside AI deployment and MLOps. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

A canary sends a small percentage of traffic to a candidate model, prompt, retriever, or agent workflow. Shadow traffic runs a candidate without showing its answer to users, which makes comparison safer.

Rollback criteria should be explicit before launch: quality drop, latency spike, cost spike, or safety incident. Feature flags make it possible to disable a model, prompt, tool, or retrieval path without redeploying code. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- A canary sends a small percentage of traffic to a candidate model, prompt, retriever, or agent workflow.
- Shadow traffic runs a candidate without showing its answer to users, which makes comparison safer.
- Rollback criteria should be explicit before launch: quality drop, latency spike, cost spike, or safety incident.
- Feature flags make it possible to disable a model, prompt, tool, or retrieval path without redeploying code.

Quick check: What release sends a small slice of traffic to a candidate first?

Concept check: In one sentence, explain how this idea matters in a real AI system: Canary releases and rollback.
