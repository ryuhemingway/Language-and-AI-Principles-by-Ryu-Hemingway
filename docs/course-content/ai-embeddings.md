# Embeddings and vector search Course Coverage

Total lessons: 6

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What Embeddings Represent

Objective: Understand embeddings as numeric representations of semantic similarity.

Context:
What Embeddings Represent sits inside Embeddings and vector search. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

An embedding maps text, images, or other content into a vector. Nearby vectors often represent similar meaning, even when exact words differ.

Embeddings are useful for search, clustering, deduplication, recommendations, and RAG. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- An embedding maps text, images, or other content into a vector.
- Nearby vectors often represent similar meaning, even when exact words differ.
- Embeddings are useful for search, clustering, deduplication, recommendations, and RAG.

Quick check: What does an embedding convert text into?

Coding problem: Write five pairs of queries/documents where keyword search might miss the semantic match.


## Lesson 2: Vector Databases and Indexes

Objective: Learn why vector indexes exist and what metadata adds.

Context:
Vector Databases and Indexes sits inside Embeddings and vector search. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

A vector index makes nearest-neighbor search fast over many embeddings. Vector databases store vectors plus metadata and sometimes original text.

Metadata filters let you restrict search by source, tenant, date, permission, language, or document type. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- A vector index makes nearest-neighbor search fast over many embeddings.
- Vector databases store vectors plus metadata and sometimes original text.
- Metadata filters let you restrict search by source, tenant, date, permission, language, or document type.

Quick check: What helps restrict vector search by source or permissions?

Coding problem: Design a vector record schema with id, text, embedding, source, timestamp, and permissions.


## Lesson 3: Similarity, Recall, and Precision

Objective: Understand retrieval quality tradeoffs.

Context:
Similarity, Recall, and Precision sits inside Embeddings and vector search. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Recall means the right item appears somewhere in retrieved results. Precision means retrieved results are mostly relevant.

Top-k, chunk size, filters, hybrid search, and reranking all affect recall and precision. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Recall means the right item appears somewhere in retrieved results.
- Precision means retrieved results are mostly relevant.
- Top-k, chunk size, filters, hybrid search, and reranking all affect recall and precision.

Quick check: What means the right result appears in the retrieved set?

Coding problem: Create 10 search queries and label which chunks should appear in the top 5 results.


## Lesson 4: Reranking and Hybrid Search

Objective: Learn how production retrieval improves beyond plain vector search.

Context:
Reranking and Hybrid Search sits inside Embeddings and vector search. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Hybrid search combines keyword and vector retrieval. Rerankers rescore candidate chunks for the specific query after broad retrieval.

These steps often improve retrieval for exact names, numbers, code identifiers, and ambiguous queries. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Hybrid search combines keyword and vector retrieval.
- Rerankers rescore candidate chunks for the specific query after broad retrieval.
- These steps often improve retrieval for exact names, numbers, code identifiers, and ambiguous queries.

Quick check: What combines keyword and vector retrieval?

Coding problem: Plan a two-stage search: retrieve 30 candidates, rerank them, then send the top 5 to the model.


## Lesson 5: Word, sentence, and document embeddings

Objective: Understand how dense vectors represent meaning at different granularities.

Context:
Word, sentence, and document embeddings sits inside Embeddings and vector search. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Word embeddings capture local semantic relationships such as similarity and analogy. Sentence and document embeddings represent larger spans for retrieval and clustering.

Dense vectors let semantically similar text sit near each other even when words differ. Embeddings are the backbone of vector search, RAG, recommendations, and deduplication. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Word embeddings capture local semantic relationships such as similarity and analogy.
- Sentence and document embeddings represent larger spans for retrieval and clustering.
- Dense vectors let semantically similar text sit near each other even when words differ.
- Embeddings are the backbone of vector search, RAG, recommendations, and deduplication.

Quick check: What does an embedding represent?

Coding problem: Explain why semantic search can find a relevant chunk that keyword search misses.


## Lesson 6: Similarity metrics and embedding model choices

Objective: Choose the right metric and embedding model for the task you actually have.

Context:
Similarity metrics and embedding model choices sits inside Embeddings and vector search. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Cosine similarity is common for semantic search; dot product and Euclidean distance appear in different stacks. Models such as Word2Vec, GloVe, sentence-transformers, E5, BGE, and CLIP cover different input types.

Embedding dimensionality affects quality, cost, and index size. Batch embedding matters when you process large corpora or API-backed indexes. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Cosine similarity is common for semantic search; dot product and Euclidean distance appear in different stacks.
- Models such as Word2Vec, GloVe, sentence-transformers, E5, BGE, and CLIP cover different input types.
- Embedding dimensionality affects quality, cost, and index size.
- Batch embedding matters when you process large corpora or API-backed indexes.

Quick check: Which metric is most common for semantic similarity?

Coding problem: Decide which embedding family you would use for documents, code, and image-text retrieval.
