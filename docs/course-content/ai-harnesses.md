# Evaluation harnesses Course Coverage

Total lessons: 10

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What a Harness Is

Objective: Understand harnesses as repeatable systems for running and judging AI behavior.

Context:
What a Harness Is sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

A harness wraps a model, prompt, tool, or workflow so it can be tested repeatedly. It standardizes inputs, expected behavior, scoring, logging, and regression checks.

Harnesses turn subjective demos into comparable engineering evidence. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- A harness wraps a model, prompt, tool, or workflow so it can be tested repeatedly.
- It standardizes inputs, expected behavior, scoring, logging, and regression checks.
- Harnesses turn subjective demos into comparable engineering evidence.

Quick check: What does a harness make repeatable?

Concept check: In one sentence, explain how this idea matters in a real AI system: What a Harness Is.


## Lesson 2: Test Cases and Golden Sets

Objective: Learn how to build a useful set of examples before automating scores.

Context:
Test Cases and Golden Sets sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Golden sets contain representative inputs and expected outcomes. Include normal cases, edge cases, adversarial cases, and examples from real failures.

Tags help you see whether regressions cluster around retrieval, safety, formatting, or reasoning. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Golden sets contain representative inputs and expected outcomes.
- Include normal cases, edge cases, adversarial cases, and examples from real failures.
- Tags help you see whether regressions cluster around retrieval, safety, formatting, or reasoning.

Quick check: What should a golden set contain besides normal cases?

Concept check: In one sentence, explain how this idea matters in a real AI system: Test Cases and Golden Sets.


## Lesson 3: Scoring and Rubrics

Objective: Understand exact, heuristic, and judge-based scoring.

Context:
Scoring and Rubrics sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Exact match works for structured outputs, unit tests, and known answers. Heuristic checks can validate citations, JSON schema, forbidden phrases, or required fields.

LLM-as-judge can help with fuzzy answers, but needs rubrics and calibration. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Exact match works for structured outputs, unit tests, and known answers.
- Heuristic checks can validate citations, JSON schema, forbidden phrases, or required fields.
- LLM-as-judge can help with fuzzy answers, but needs rubrics and calibration.

Quick check: What kind of scoring is best for strict JSON fields?

Concept check: In one sentence, explain how this idea matters in a real AI system: Scoring and Rubrics.


## Lesson 4: Building an Evaluation Harness

Objective: Learn the structure of a minimal AI eval harness.

Context:
Building an Evaluation Harness sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Runner: loops through test cases and calls the system under test. Scorer: grades each result using exact checks, rubrics, or judges.

Reporter: saves results, failures, cost, latency, and diffs against prior runs. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Runner: loops through test cases and calls the system under test.
- Scorer: grades each result using exact checks, rubrics, or judges.
- Reporter: saves results, failures, cost, latency, and diffs against prior runs.

Quick check: Name one core part of an eval harness.

Concept check: In one sentence, explain how this idea matters in a real AI system: Building an Evaluation Harness.


## Lesson 5: Regression Testing AI Systems

Objective: Learn how harnesses protect prompts and workflows from silent degradation.

Context:
Regression Testing AI Systems sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

AI changes can improve one behavior while breaking another. Regression runs compare current results to a previous baseline.

Useful reports show failing examples first, not just aggregate scores. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- AI changes can improve one behavior while breaking another.
- Regression runs compare current results to a previous baseline.
- Useful reports show failing examples first, not just aggregate scores.

Quick check: What do regression runs compare against?

Concept check: In one sentence, explain how this idea matters in a real AI system: Regression Testing AI Systems.


## Lesson 6: Why evaluation matters

Objective: Understand why AI engineering needs repeatable measurement.

Context:
Why evaluation matters sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Ad hoc testing makes results hard to compare and easy to fool yourself with. Evaluation should be a loop: measure, change, compare, and regressions-check.

Benchmarks, online tests, and human review each answer different questions. Capability evals and safety evals should be separated, not blended together. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Ad hoc testing makes results hard to compare and easy to fool yourself with.
- Evaluation should be a loop: measure, change, compare, and regressions-check.
- Benchmarks, online tests, and human review each answer different questions.
- Capability evals and safety evals should be separated, not blended together.

Quick check: Why should evaluation be repeatable?

Concept check: In one sentence, explain how this idea matters in a real AI system: Why evaluation matters.


## Lesson 7: Benchmarks and lm-evaluation-harness

Objective: Know which benchmarks test what and how to run them in practice.

Context:
Benchmarks and lm-evaluation-harness sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

MMLU tests broad knowledge, HellaSwag tests commonsense, GSM8K tests grade-school math, and HumanEval tests code generation. IFEval and MT-Bench cover instruction following and multi-turn behavior.

EleutherAI lm-evaluation-harness standardizes YAML tasks, model backends, and reporting. Writing a custom task and pinning config plus commit hash make benchmark runs reproducible. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- MMLU tests broad knowledge, HellaSwag tests commonsense, GSM8K tests grade-school math, and HumanEval tests code generation.
- IFEval and MT-Bench cover instruction following and multi-turn behavior.
- EleutherAI lm-evaluation-harness standardizes YAML tasks, model backends, and reporting.
- Writing a custom task and pinning config plus commit hash make benchmark runs reproducible.

Quick check: Which benchmark is commonly used for code generation?

Concept check: In one sentence, explain how this idea matters in a real AI system: Benchmarks and lm-evaluation-harness.


## Lesson 8: Metrics and LLM-as-judge

Objective: Choose scoring methods that match the task and the amount of fuzziness involved.

Context:
Metrics and LLM-as-judge sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Exact match and F1 work well for strict or extractive tasks. BLEU, ROUGE, METEOR, BERTScore, and pass@k cover different generation goals.

LLM-as-judge is useful for subjective outputs but has biases like verbosity and position bias. Rubrics and reference answers make judge-based evals much more reliable. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Exact match and F1 work well for strict or extractive tasks.
- BLEU, ROUGE, METEOR, BERTScore, and pass@k cover different generation goals.
- LLM-as-judge is useful for subjective outputs but has biases like verbosity and position bias.
- Rubrics and reference answers make judge-based evals much more reliable.

Quick check: What judge bias rewards longer answers?

Concept check: In one sentence, explain how this idea matters in a real AI system: Metrics and LLM-as-judge.


## Lesson 9: RAG-specific evaluation and CI/CD tools

Objective: Measure retrieval and grounding separately from the final response text.

Context:
RAG-specific evaluation and CI/CD tools sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

RAGAS adds faithfulness, answer relevance, context precision, and context recall. Hallucination detection checks claims against retrieved evidence.

DeepEval and Promptfoo make it easier to run AI tests inside CI/CD pipelines. Quality gates, dashboards, and synthetic test sets keep retrieval regressions visible. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- RAGAS adds faithfulness, answer relevance, context precision, and context recall.
- Hallucination detection checks claims against retrieved evidence.
- DeepEval and Promptfoo make it easier to run AI tests inside CI/CD pipelines.
- Quality gates, dashboards, and synthetic test sets keep retrieval regressions visible.

Quick check: Which metric checks how well retrieved context supports the answer?

Concept check: In one sentence, explain how this idea matters in a real AI system: RAG-specific evaluation and CI/CD tools.


## Lesson 10: Safety, red-teaming, and human evaluation

Objective: Use adversarial testing and human review when automated metrics are not enough.

Context:
Safety, red-teaming, and human evaluation sits inside Evaluation harnesses. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Safety evals include toxicity, stereotype, jailbreak, and harmful-output checks. Red-teaming intentionally probes failure modes and edge cases.

Human evaluation needs rubrics, calibration, and inter-annotator agreement to be trusted. Some tasks should also enforce compliance and policy constraints such as GDPR or HIPAA. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Safety evals include toxicity, stereotype, jailbreak, and harmful-output checks.
- Red-teaming intentionally probes failure modes and edge cases.
- Human evaluation needs rubrics, calibration, and inter-annotator agreement to be trusted.
- Some tasks should also enforce compliance and policy constraints such as GDPR or HIPAA.

Quick check: What is one purpose of red-teaming?

Concept check: In one sentence, explain how this idea matters in a real AI system: Safety, red-teaming, and human evaluation.
