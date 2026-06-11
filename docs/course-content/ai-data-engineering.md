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

Coding problem: Design a pipeline that ingests PDFs, extracts text, validates metadata, chunks content, and stores records.


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

Coding problem: Create labeling guidelines for classifying support tickets into billing, bug, account, or sales.


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

Coding problem: Define metadata for dataset version, source, transform version, timestamp, owner, and row count.


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

Coding problem: Write 10 validation checks for a document ingestion pipeline or classification dataset.


## Lesson 5: AI data pipelines

Objective: See how raw inputs become training, retrieval, or evaluation data.

Context:
AI data pipelines sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

AI pipelines cover ingestion, parsing, cleaning, normalization, validation, and storage. Extraction can fail on tables, images, multi-column layouts, or malformed files.

Incremental, observable, replayable pipelines are much easier to debug than ad hoc scripts. Pipeline quality strongly shapes model quality downstream. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- AI pipelines cover ingestion, parsing, cleaning, normalization, validation, and storage.
- Extraction can fail on tables, images, multi-column layouts, or malformed files.
- Incremental, observable, replayable pipelines are much easier to debug than ad hoc scripts.
- Pipeline quality strongly shapes model quality downstream.

Quick check: What should a reliable pipeline be able to do after a failure?

Coding problem: Sketch a pipeline that ingests PDFs, cleans text, and stores chunk records.


## Lesson 6: Labels, lineage, and versioning

Objective: Keep track of what the model learned from and what changed over time.

Context:
Labels, lineage, and versioning sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Labels define target outputs for supervised learning or evaluation tasks. Ground truth can be noisy, delayed, or expensive, so labeling rules matter.

Dataset versioning records exactly which data went into a model or index. Lineage tracks where the data came from and which transforms changed it. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Labels define target outputs for supervised learning or evaluation tasks.
- Ground truth can be noisy, delayed, or expensive, so labeling rules matter.
- Dataset versioning records exactly which data went into a model or index.
- Lineage tracks where the data came from and which transforms changed it.

Quick check: What tracks where data came from and how it changed?

Coding problem: Define metadata you would attach to one dataset version and one transformed chunk set.


## Lesson 7: Data quality and governance

Objective: Add checks before broken data reaches models or retrieval indexes.

Context:
Data quality and governance sits inside AI data engineering. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Validate schema, null rate, duplicate rate, ranges, and encoding before training or indexing. Check for leakage, duplicate examples across splits, and corrupted records.

RAG systems need permissions and metadata checks so users cannot retrieve private material they should not see. Quality gates are much cheaper than debugging model behavior later. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Validate schema, null rate, duplicate rate, ranges, and encoding before training or indexing.
- Check for leakage, duplicate examples across splits, and corrupted records.
- RAG systems need permissions and metadata checks so users cannot retrieve private material they should not see.
- Quality gates are much cheaper than debugging model behavior later.

Quick check: What kind of examples across train/test splits can inflate scores?

Coding problem: Write three quality checks for a document or tabular AI pipeline.
