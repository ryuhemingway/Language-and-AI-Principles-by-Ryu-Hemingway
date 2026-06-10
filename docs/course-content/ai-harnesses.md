# Evaluation harnesses Course Coverage

Total lessons: 10

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What a Harness Is

Objective: Understand harnesses as repeatable systems for running and judging AI behavior.

Concepts taught:
- A harness wraps a model, prompt, tool, or workflow so it can be tested repeatedly.
- It standardizes inputs, expected behavior, scoring, logging, and regression checks.
- Harnesses turn subjective demos into comparable engineering evidence.

Practice: Define a CSV/JSON test set with input, expected behavior, tags, and pass/fail criteria.

Quick check: What does a harness make repeatable?

## Lesson 2: Test Cases and Golden Sets

Objective: Learn how to build a useful set of examples before automating scores.

Concepts taught:
- Golden sets contain representative inputs and expected outcomes.
- Include normal cases, edge cases, adversarial cases, and examples from real failures.
- Tags help you see whether regressions cluster around retrieval, safety, formatting, or reasoning.

Practice: Create 20 test cases for one assistant task and tag each case by skill or risk.

Quick check: What should a golden set contain besides normal cases?

## Lesson 3: Scoring and Rubrics

Objective: Understand exact, heuristic, and judge-based scoring.

Concepts taught:
- Exact match works for structured outputs, unit tests, and known answers.
- Heuristic checks can validate citations, JSON schema, forbidden phrases, or required fields.
- LLM-as-judge can help with fuzzy answers, but needs rubrics and calibration.

Practice: Write a rubric with 0/1/2 scores for correctness, groundedness, and format compliance.

Quick check: What kind of scoring is best for strict JSON fields?

## Lesson 4: Building an Evaluation Harness

Objective: Learn the structure of a minimal AI eval harness.

Concepts taught:
- Runner: loops through test cases and calls the system under test.
- Scorer: grades each result using exact checks, rubrics, or judges.
- Reporter: saves results, failures, cost, latency, and diffs against prior runs.

Practice: Create `eval.py` that loads test cases, calls your app, scores outputs, and writes `results.json`.

Quick check: Name one core part of an eval harness.

## Lesson 5: Regression Testing AI Systems

Objective: Learn how harnesses protect prompts and workflows from silent degradation.

Concepts taught:
- AI changes can improve one behavior while breaking another.
- Regression runs compare current results to a previous baseline.
- Useful reports show failing examples first, not just aggregate scores.

Practice: Run the same test set before and after a prompt change and compare pass rate plus failed cases.

Quick check: What do regression runs compare against?

## Lesson 6: Why evaluation matters

Objective: Understand why AI engineering needs repeatable measurement.

Concepts taught:
- Ad hoc testing makes results hard to compare and easy to fool yourself with.
- Evaluation should be a loop: measure, change, compare, and regressions-check.
- Benchmarks, online tests, and human review each answer different questions.
- Capability evals and safety evals should be separated, not blended together.

Example:
```text
before = run_eval(old_prompt)
after = run_eval(new_prompt)
compare(before, after)
```

Practice: Describe one AI change that should be measured before and after deployment.

Quick check: Why should evaluation be repeatable?

## Lesson 7: Benchmarks and lm-evaluation-harness

Objective: Know which benchmarks test what and how to run them in practice.

Concepts taught:
- MMLU tests broad knowledge, HellaSwag tests commonsense, GSM8K tests grade-school math, and HumanEval tests code generation.
- IFEval and MT-Bench cover instruction following and multi-turn behavior.
- EleutherAI lm-evaluation-harness standardizes YAML tasks, model backends, and reporting.
- Writing a custom task and pinning config plus commit hash make benchmark runs reproducible.

Example:
```text
lm_eval --model hf --tasks hellaswag,gsm8k --fewshot 5
task = {"name": "custom_eval", "metrics": ["exact_match"]}
```

Practice: Pick one benchmark for knowledge, one for math, and one for code.

Quick check: Which benchmark is commonly used for code generation?

## Lesson 8: Metrics and LLM-as-judge

Objective: Choose scoring methods that match the task and the amount of fuzziness involved.

Concepts taught:
- Exact match and F1 work well for strict or extractive tasks.
- BLEU, ROUGE, METEOR, BERTScore, and pass@k cover different generation goals.
- LLM-as-judge is useful for subjective outputs but has biases like verbosity and position bias.
- Rubrics and reference answers make judge-based evals much more reliable.

Example:
```text
score = judge(prompt, response, rubric)
print({"f1": f1, "pass@k": pass_at_k, "judge": score})
```

Practice: Decide which metric you would use for QA, summarization, and code generation.

Quick check: What judge bias rewards longer answers?

## Lesson 9: RAG-specific evaluation and CI/CD tools

Objective: Measure retrieval and grounding separately from the final response text.

Concepts taught:
- RAGAS adds faithfulness, answer relevance, context precision, and context recall.
- Hallucination detection checks claims against retrieved evidence.
- DeepEval and Promptfoo make it easier to run AI tests inside CI/CD pipelines.
- Quality gates, dashboards, and synthetic test sets keep retrieval regressions visible.

Example:
```text
pytest -m eval
promptfoo run
record({"faithfulness": faith, "context_recall": recall})
```

Practice: Write one test that checks retrieval and one that checks final-answer faithfulness.

Quick check: Which metric checks how well retrieved context supports the answer?

## Lesson 10: Safety, red-teaming, and human evaluation

Objective: Use adversarial testing and human review when automated metrics are not enough.

Concepts taught:
- Safety evals include toxicity, stereotype, jailbreak, and harmful-output checks.
- Red-teaming intentionally probes failure modes and edge cases.
- Human evaluation needs rubrics, calibration, and inter-annotator agreement to be trusted.
- Some tasks should also enforce compliance and policy constraints such as GDPR or HIPAA.

Example:
```text
red_team(prompt)
sample = annotate(pairwise_examples)
report_kappa(sample)
```

Practice: Design a small human-eval rubric for answer quality and safety.

Quick check: What is one purpose of red-teaming?
