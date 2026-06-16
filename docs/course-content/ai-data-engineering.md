# AI data engineering Course Coverage

Total lessons: 7

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Data Pipelines for AI

Objective: Understand how raw data becomes usable training, retrieval, or evaluation data.

Context:
Data Pipelines for AI sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

AI systems depend on ingestion, parsing, cleaning, normalization, validation, and storage. Pipeline failures often show up as model failures later.

Reliable pipelines are incremental, observable, replayable, and tested with bad inputs. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- AI systems depend on ingestion, parsing, cleaning, normalization, validation, and storage.
- Pipeline failures often show up as model failures later.
- Reliable pipelines are incremental, observable, replayable, and tested with bad inputs.

Quick check: What should a reliable data pipeline be able to do after a failure?

Concept check: In one sentence, explain how this idea matters in a real AI system: Data Pipelines for AI.


## Lesson 2: Labels, Features, and Ground Truth

Objective: Learn how training and evaluation data get their meaning.

Context:
Labels, Features, and Ground Truth sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Labels define what the model is supposed to learn or what an eval expects. Features are the input signals used by traditional ML models.

Ground truth can be noisy, subjective, delayed, or expensive, so label quality must be measured. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Labels define what the model is supposed to learn or what an eval expects.
- Features are the input signals used by traditional ML models.
- Ground truth can be noisy, subjective, delayed, or expensive, so label quality must be measured.

Quick check: What defines the target output for supervised learning?

Concept check: In one sentence, explain how this idea matters in a real AI system: Labels, Features, and Ground Truth.


## Lesson 3: Dataset Versioning and Lineage

Objective: Understand how teams trace model behavior back to data changes.

Context:
Dataset Versioning and Lineage sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Dataset versioning records exactly which data went into training, evaluation, or indexing. Lineage tracks where data came from and which transformations changed it.

Without lineage, debugging regressions becomes guesswork. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Dataset versioning records exactly which data went into training, evaluation, or indexing.
- Lineage tracks where data came from and which transformations changed it.
- Without lineage, debugging regressions becomes guesswork.

Quick check: What tracks where data came from and how it changed?

Concept check: In one sentence, explain how this idea matters in a real AI system: Dataset Versioning and Lineage.


## Lesson 4: Data Quality Checks

Objective: Learn the tests that prevent broken data from reaching models.

Context:
Data Quality Checks sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Check schemas, null rates, duplicate rates, value ranges, distribution shifts, and permission constraints. RAG indexes need checks for empty chunks, bad encodings, missing source metadata, and stale documents.

ML datasets need checks for label imbalance, leakage, duplicates across splits, and corrupted examples. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Check schemas, null rates, duplicate rates, value ranges, distribution shifts, and permission constraints.
- RAG indexes need checks for empty chunks, bad encodings, missing source metadata, and stale documents.
- ML datasets need checks for label imbalance, leakage, duplicates across splits, and corrupted examples.

Quick check: What kind of examples across train/test splits can inflate model scores?

Concept check: In one sentence, explain how this idea matters in a real AI system: Data Quality Checks.


## Lesson 5: Orchestration, backfills, and recovery

Objective: Operate AI data jobs when schedules, failures, and historical repairs matter.

Context:
Orchestration, backfills, and recovery sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Orchestrators such as Airflow, Dagster, and Prefect make dependencies, schedules, retries, and ownership explicit. Idempotent tasks can be rerun safely without duplicating records, chunks, embeddings, or labels.

Backfills repair historical data after a parser, chunker, schema, or model choice changes. Checkpoints and run metadata let teams resume failed AI data jobs without guessing what already finished. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Orchestrators such as Airflow, Dagster, and Prefect make dependencies, schedules, retries, and ownership explicit.
- Idempotent tasks can be rerun safely without duplicating records, chunks, embeddings, or labels.
- Backfills repair historical data after a parser, chunker, schema, or model choice changes.
- Checkpoints and run metadata let teams resume failed AI data jobs without guessing what already finished.

Quick check: What kind of task can be rerun safely without duplicating outputs?

Concept check: In one sentence, explain how this idea matters in a real AI system: Orchestration, backfills, and recovery.


## Lesson 6: Data contracts and schema evolution

Objective: Prevent producer changes from silently breaking AI consumers.

Context:
Data contracts and schema evolution sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

A data contract states expected fields, types, semantics, freshness, and ownership for a dataset. Schema evolution needs compatibility rules so adding, renaming, or deleting fields does not break training or retrieval jobs.

Consumer-driven tests catch breaking changes before downstream feature stores, indexes, or eval sets drift. Deprecation windows give AI systems time to migrate prompts, parsers, embeddings, and dashboards. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- A data contract states expected fields, types, semantics, freshness, and ownership for a dataset.
- Schema evolution needs compatibility rules so adding, renaming, or deleting fields does not break training or retrieval jobs.
- Consumer-driven tests catch breaking changes before downstream feature stores, indexes, or eval sets drift.
- Deprecation windows give AI systems time to migrate prompts, parsers, embeddings, and dashboards.

Quick check: What states the expected fields and meaning of a dataset?

Concept check: In one sentence, explain how this idea matters in a real AI system: Data contracts and schema evolution.


## Lesson 7: Access, retention, and deletion workflows

Objective: Engineer data governance into retrieval and training systems.

Context:
Access, retention, and deletion workflows sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Access checks must happen before retrieval, not after a model has already seen private context. Retention policies decide how long raw documents, transformed chunks, labels, logs, and embeddings may stay available.

Deletion workflows must remove derived artifacts such as chunks, vectors, cached answers, and eval rows. Governance metadata should travel with records so every consumer can enforce policy consistently. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Access checks must happen before retrieval, not after a model has already seen private context.
- Retention policies decide how long raw documents, transformed chunks, labels, logs, and embeddings may stay available.
- Deletion workflows must remove derived artifacts such as chunks, vectors, cached answers, and eval rows.
- Governance metadata should travel with records so every consumer can enforce policy consistently.

Quick check: What derived artifact must be deleted when a source document is removed?

Concept check: In one sentence, explain how this idea matters in a real AI system: Access, retention, and deletion workflows.
