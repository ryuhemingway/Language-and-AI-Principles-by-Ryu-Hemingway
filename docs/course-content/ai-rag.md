# Retrieval-augmented generation Course Coverage

Total lessons: 11

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What RAG Solves

Objective: Understand why retrieval-augmented generation exists and when it beats prompting alone.

Concepts taught:
- LLMs answer from model weights plus prompt context; they do not automatically know your private files.
- RAG retrieves relevant external context first, then asks the model to answer using that context.
- It is helpful for fresher facts, private knowledge, citations, and reducing unsupported answers.

Practice: Sketch a pipeline: user question -> retrieve matching notes -> place top passages in prompt -> generate answer with citations.

Quick check: What does the retrieval step add to the model prompt?

## Lesson 2: Documents, Chunks, and Metadata

Objective: Learn how source material becomes searchable retrieval units.

Concepts taught:
- Documents are split into chunks because whole files are usually too large and too broad.
- Good chunks preserve meaning: headings, section boundaries, code blocks, and source metadata matter.
- Metadata such as filename, URL, date, owner, and topic helps filtering and citation.

Practice: Take one article, split it into 300-800 token chunks, and attach source/title/page metadata to each chunk.

Quick check: Why do RAG systems chunk documents?

## Lesson 3: Embeddings and Vector Search

Objective: Understand how semantic retrieval finds similar meaning instead of exact words only.

Concepts taught:
- An embedding converts text into a vector that represents semantic meaning.
- Vector search compares vectors to find chunks near the user question.
- Keyword search and vector search are complementary; hybrid retrieval often works better than either alone.

Practice: Embed chunks, store vectors in a vector index, embed the question, then retrieve the nearest chunks.

Quick check: What does an embedding represent?

## Lesson 4: Prompt Assembly and Grounding

Objective: Learn how retrieved passages are turned into a grounded answer prompt.

Concepts taught:
- The prompt should separate instructions, user question, and retrieved context.
- Grounding means the answer should be based on supplied context, not unsupported guesses.
- Citations work best when each chunk keeps stable source metadata.

Practice: Write a prompt template with: role, rules, context block, question, and citation requirement.

Quick check: What should a grounded RAG answer be based on?

## Lesson 5: Building a Minimal RAG App

Objective: Understand the smallest working RAG implementation you can build yourself.

Concepts taught:
- Indexing path: load files, chunk text, embed chunks, store vectors and metadata.
- Query path: embed question, retrieve chunks, assemble prompt, call model, return answer.
- Start with a local JSON/SQLite store before adding a production vector database.

Practice: Create `ingest.py` and `ask.py`: one builds the index, the other retrieves context and calls local/cloud AI.

Quick check: Name one file/script in a minimal RAG project.

## Lesson 6: RAG Quality and Failure Modes

Objective: Learn how RAG fails and how to measure whether it is improving.

Concepts taught:
- Bad chunking, weak retrieval, stale data, and vague questions can all produce bad answers.
- Evaluate retrieval separately from generation: did the right evidence appear in top results?
- Track answer correctness, citation support, refusal behavior, and latency.

Practice: Create 10 question/expected-source pairs and check whether your retriever returns the right chunks.

Quick check: What should you evaluate separately from generation?

## Lesson 7: RAG architecture and why it exists

Objective: Understand the core retrieve-augment-generate loop and where it fits.

Concepts taught:
- RAG grounds an LLM in external evidence instead of relying only on model weights.
- The core loop is query, retrieve, augment, and generate.
- Naive, advanced, and modular RAG differ in how retrieval and orchestration are separated.
- RAG is useful when facts change, sources matter, or private data must stay outside model training.

Example:
```text
q = user_question()
chunks = retrieve(q)
answer = generate(q, chunks)
```

Practice: Compare RAG, fine-tuning, and long-context prompting for three different product needs.

Quick check: What is the first step in the core RAG loop?

## Lesson 8: Document ingestion, loaders, and chunking

Objective: Turn raw documents into retrieval-ready chunks with useful metadata.

Concepts taught:
- Loaders often need to handle PDF, HTML, Markdown, DOCX, CSV, and code files.
- Chunking can be fixed-size, recursive, sentence-based, or semantic.
- Metadata such as page number, section title, source, and timestamp make citations and filters work.
- Chunk size and overlap strongly affect retrieval quality and the lost-in-the-middle problem.

Example:
```text
docs = load_pdf()
chunks = chunk(docs, size=800, overlap=120)
meta = {"page": 3, "source": "handbook"}
```

Practice: Explain how you would split a long PDF into chunks without destroying headings and tables.

Quick check: Why do RAG systems chunk documents?

## Lesson 9: Embedding, indexing, and vector databases

Objective: Store semantic representations so retrieval can scale beyond brute force.

Concepts taught:
- Embedding models turn chunks into vectors and make semantic retrieval possible.
- Vector indexes and vector databases store vectors plus metadata for fast lookup and filtering.
- Approximate nearest-neighbor methods trade a little recall for major speed gains.
- Batch embedding, index choice, and dimensionality are cost and quality decisions, not afterthoughts.

Example:
```text
vecs = embed_batch(chunks)
index = hnsw_upsert(vecs, metadata)
print(index.search(query_vec))
```

Practice: Describe what a vector DB stores that a normal relational DB does not optimize for.

Quick check: Which structure speeds nearest-neighbor search?

## Lesson 10: Retrieval, reranking, and grounding

Objective: Improve retrieval quality and keep the generated answer anchored to evidence.

Concepts taught:
- Dense search, sparse search, and hybrid search solve different retrieval problems.
- Cross-encoder rerankers refine coarse retrieval candidates before generation.
- Prompt construction should separate instructions, question, and retrieved context clearly.
- Good grounding teaches the model to abstain when the context is insufficient.

Example:
```text
dense = vector_search(q)
sparse = bm25(q)
ranked = rerank(q, dense + sparse)
```

Practice: Write a retrieval stack that uses dense search, BM25, and reranking before generation.

Quick check: What does hybrid search combine?

## Lesson 11: Advanced RAG, evaluation, and production

Objective: Use advanced patterns and metrics to ship RAG responsibly.

Concepts taught:
- GraphRAG, Self-reflective RAG, CRAG, RAPTOR, and Agentic RAG tackle harder retrieval problems.
- RAG evaluation tracks precision@k, recall@k, faithfulness, answer relevance, and context relevance.
- Production concerns include access control, incremental indexing, caching, latency, and observability.
- Agentic RAG uses query decomposition, validation, and specialized workers to improve hard queries.

Example:
```text
if not enough_context:
    ask_clarification()
score = ragas(context, answer)
log({"query": q, "score": score})
```

Practice: Name one advanced RAG pattern and one production concern you would monitor first.

Quick check: Which RAG metric checks whether the answer follows the retrieved context?
