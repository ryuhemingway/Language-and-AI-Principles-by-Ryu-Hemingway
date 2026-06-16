# RAG Fundamentals

RAG means retrieval-augmented generation. It retrieves relevant external
context before asking a model to answer.

## Principles Included

- What RAG solves
- Document ingestion
- Chunking
- Metadata
- Embeddings
- Vector search
- Prompt assembly
- Grounding and citations
- RAG evaluation and failure modes

## Why It Matters

RAG is one of the most practical AI engineering patterns because it lets models
use private, current, or domain-specific information without retraining.

## Build Practice

Build two scripts:

- `ingest.py`: load files, chunk text, embed chunks, save index
- `ask.py`: embed a question, retrieve chunks, assemble prompt, answer

