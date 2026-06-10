# AI data engineering Course Coverage

Total lessons: 7

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: Data Pipelines for AI

Objective: Understand how raw data becomes usable training, retrieval, or evaluation data.

Concepts taught:
- AI systems depend on ingestion, parsing, cleaning, normalization, validation, and storage.
- Pipeline failures often show up as model failures later.
- Reliable pipelines are incremental, observable, replayable, and tested with bad inputs.

Practice: Design a pipeline that ingests PDFs, extracts text, validates metadata, chunks content, and stores records.

Quick check: What should a reliable data pipeline be able to do after a failure?

## Lesson 2: Labels, Features, and Ground Truth

Objective: Learn how training and evaluation data get their meaning.

Concepts taught:
- Labels define what the model is supposed to learn or what an eval expects.
- Features are the input signals used by traditional ML models.
- Ground truth can be noisy, subjective, delayed, or expensive, so label quality must be measured.

Practice: Create labeling guidelines for classifying support tickets into billing, bug, account, or sales.

Quick check: What defines the target output for supervised learning?

## Lesson 3: Dataset Versioning and Lineage

Objective: Understand how teams trace model behavior back to data changes.

Concepts taught:
- Dataset versioning records exactly which data went into training, evaluation, or indexing.
- Lineage tracks where data came from and which transformations changed it.
- Without lineage, debugging regressions becomes guesswork.

Practice: Define metadata for dataset version, source, transform version, timestamp, owner, and row count.

Quick check: What tracks where data came from and how it changed?

## Lesson 4: Data Quality Checks

Objective: Learn the tests that prevent broken data from reaching models.

Concepts taught:
- Check schemas, null rates, duplicate rates, value ranges, distribution shifts, and permission constraints.
- RAG indexes need checks for empty chunks, bad encodings, missing source metadata, and stale documents.
- ML datasets need checks for label imbalance, leakage, duplicates across splits, and corrupted examples.

Practice: Write 10 validation checks for a document ingestion pipeline or classification dataset.

Quick check: What kind of examples across train/test splits can inflate model scores?

## Lesson 5: AI data pipelines

Objective: See how raw inputs become training, retrieval, or evaluation data.

Concepts taught:
- AI pipelines cover ingestion, parsing, cleaning, normalization, validation, and storage.
- Extraction can fail on tables, images, multi-column layouts, or malformed files.
- Incremental, observable, replayable pipelines are much easier to debug than ad hoc scripts.
- Pipeline quality strongly shapes model quality downstream.

Example:
```text
raw = ingest(files)
clean = normalize(raw)
store(clean)
```

Practice: Sketch a pipeline that ingests PDFs, cleans text, and stores chunk records.

Quick check: What should a reliable pipeline be able to do after a failure?

## Lesson 6: Labels, lineage, and versioning

Objective: Keep track of what the model learned from and what changed over time.

Concepts taught:
- Labels define target outputs for supervised learning or evaluation tasks.
- Ground truth can be noisy, delayed, or expensive, so labeling rules matter.
- Dataset versioning records exactly which data went into a model or index.
- Lineage tracks where the data came from and which transforms changed it.

Example:
```text
record = {"source": url, "version": "v3", "transform": "chunker-2"}
audit_log(record)
```

Practice: Define metadata you would attach to one dataset version and one transformed chunk set.

Quick check: What tracks where data came from and how it changed?

## Lesson 7: Data quality and governance

Objective: Add checks before broken data reaches models or retrieval indexes.

Concepts taught:
- Validate schema, null rate, duplicate rate, ranges, and encoding before training or indexing.
- Check for leakage, duplicate examples across splits, and corrupted records.
- RAG systems need permissions and metadata checks so users cannot retrieve private material they should not see.
- Quality gates are much cheaper than debugging model behavior later.

Example:
```text
assert schema_ok(df)
assert null_rate(df) < 0.01
assert not leaked_rows(df)
```

Practice: Write three quality checks for a document or tabular AI pipeline.

Quick check: What kind of examples across train/test splits can inflate scores?
