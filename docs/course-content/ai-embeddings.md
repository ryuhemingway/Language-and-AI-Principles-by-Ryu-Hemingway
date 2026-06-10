# Embeddings and vector search Course Coverage

Total lessons: 6

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What Embeddings Represent

Objective: Understand embeddings as numeric representations of semantic similarity.

Concepts taught:
- An embedding maps text, images, or other content into a vector.
- Nearby vectors often represent similar meaning, even when exact words differ.
- Embeddings are useful for search, clustering, deduplication, recommendations, and RAG.

Practice: Write five pairs of queries/documents where keyword search might miss the semantic match.

Quick check: What does an embedding convert text into?

## Lesson 2: Vector Databases and Indexes

Objective: Learn why vector indexes exist and what metadata adds.

Concepts taught:
- A vector index makes nearest-neighbor search fast over many embeddings.
- Vector databases store vectors plus metadata and sometimes original text.
- Metadata filters let you restrict search by source, tenant, date, permission, language, or document type.

Practice: Design a vector record schema with id, text, embedding, source, timestamp, and permissions.

Quick check: What helps restrict vector search by source or permissions?

## Lesson 3: Similarity, Recall, and Precision

Objective: Understand retrieval quality tradeoffs.

Concepts taught:
- Recall means the right item appears somewhere in retrieved results.
- Precision means retrieved results are mostly relevant.
- Top-k, chunk size, filters, hybrid search, and reranking all affect recall and precision.

Practice: Create 10 search queries and label which chunks should appear in the top 5 results.

Quick check: What means the right result appears in the retrieved set?

## Lesson 4: Reranking and Hybrid Search

Objective: Learn how production retrieval improves beyond plain vector search.

Concepts taught:
- Hybrid search combines keyword and vector retrieval.
- Rerankers rescore candidate chunks for the specific query after broad retrieval.
- These steps often improve retrieval for exact names, numbers, code identifiers, and ambiguous queries.

Practice: Plan a two-stage search: retrieve 30 candidates, rerank them, then send the top 5 to the model.

Quick check: What combines keyword and vector retrieval?

## Lesson 5: Word, sentence, and document embeddings

Objective: Understand how dense vectors represent meaning at different granularities.

Concepts taught:
- Word embeddings capture local semantic relationships such as similarity and analogy.
- Sentence and document embeddings represent larger spans for retrieval and clustering.
- Dense vectors let semantically similar text sit near each other even when words differ.
- Embeddings are the backbone of vector search, RAG, recommendations, and deduplication.

Example:
```text
query_vec = embed("how should I chunk documents?")
doc_vec = embed("recursive chunking preserves headings")
print(cosine(query_vec, doc_vec))
```

Practice: Explain why semantic search can find a relevant chunk that keyword search misses.

Quick check: What does an embedding represent?

## Lesson 6: Similarity metrics and embedding model choices

Objective: Choose the right metric and embedding model for the task you actually have.

Concepts taught:
- Cosine similarity is common for semantic search; dot product and Euclidean distance appear in different stacks.
- Models such as Word2Vec, GloVe, sentence-transformers, E5, BGE, and CLIP cover different input types.
- Embedding dimensionality affects quality, cost, and index size.
- Batch embedding matters when you process large corpora or API-backed indexes.

Example:
```text
docs = embed_batch(chunks, batch_size=64)
image_vec, text_vec = clip_embed(image, text)
score = cosine(image_vec, text_vec)
```

Practice: Decide which embedding family you would use for documents, code, and image-text retrieval.

Quick check: Which metric is most common for semantic similarity?
