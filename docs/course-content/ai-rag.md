# Retrieval-augmented generation Course Coverage

Total lessons: 11

This file is generated from `learn.py` and mirrors the CLI lesson order.

## Lesson 1: What RAG Solves

Objective: Understand why retrieval-augmented generation exists and when it beats prompting alone.

Context:
What RAG Solves sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

LLMs answer from model weights plus prompt context; they do not automatically know your private files. RAG retrieves relevant external context first, then asks the model to answer using that context.

It is helpful for fresher facts, private knowledge, citations, and reducing unsupported answers. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- LLMs answer from model weights plus prompt context; they do not automatically know your private files.
- RAG retrieves relevant external context first, then asks the model to answer using that context.
- It is helpful for fresher facts, private knowledge, citations, and reducing unsupported answers.

Quick check: What does the retrieval step add to the model prompt?

Concept check: When is RAG a better choice than prompting alone?


## Lesson 2: Documents, Chunks, and Metadata

Objective: Learn how source material becomes searchable retrieval units.

Context:
Documents, Chunks, and Metadata sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Documents are split into chunks because whole files are usually too large and too broad. Good chunks preserve meaning: headings, section boundaries, code blocks, and source metadata matter.

Metadata such as filename, URL, date, owner, and topic helps filtering and citation. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Documents are split into chunks because whole files are usually too large and too broad.
- Good chunks preserve meaning: headings, section boundaries, code blocks, and source metadata matter.
- Metadata such as filename, URL, date, owner, and topic helps filtering and citation.

Quick check: Why do RAG systems chunk documents?

Concept check: In one sentence, explain how this idea matters in a real AI system: Documents, Chunks, and Metadata.


## Lesson 3: Embeddings and Vector Search

Objective: Understand how semantic retrieval finds similar meaning instead of exact words only.

Context:
Embeddings and Vector Search sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

An embedding converts text into a vector that represents semantic meaning. Vector search compares vectors to find chunks near the user question.

Keyword search and vector search are complementary; hybrid retrieval often works better than either alone. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- An embedding converts text into a vector that represents semantic meaning.
- Vector search compares vectors to find chunks near the user question.
- Keyword search and vector search are complementary; hybrid retrieval often works better than either alone.

Quick check: What does an embedding represent?

Concept check: In one sentence, explain how this idea matters in a real AI system: Embeddings and Vector Search.


## Lesson 4: Prompt Assembly and Grounding

Objective: Learn how retrieved passages are turned into a grounded answer prompt.

Context:
Prompt Assembly and Grounding sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

The prompt should separate instructions, user question, and retrieved context. Grounding means the answer should be based on supplied context, not unsupported guesses.

Citations work best when each chunk keeps stable source metadata. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- The prompt should separate instructions, user question, and retrieved context.
- Grounding means the answer should be based on supplied context, not unsupported guesses.
- Citations work best when each chunk keeps stable source metadata.

Quick check: What should a grounded RAG answer be based on?

Concept check: In one sentence, explain how this idea matters in a real AI system: Prompt Assembly and Grounding.


## Lesson 5: Building a Minimal RAG App

Objective: Understand the smallest working RAG implementation you can build yourself.

Context:
Building a Minimal RAG App sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Indexing path: load files, chunk text, embed chunks, store vectors and metadata. Query path: embed question, retrieve chunks, assemble prompt, call model, return answer.

Start with a local JSON/SQLite store before adding a production vector database. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Indexing path: load files, chunk text, embed chunks, store vectors and metadata.
- Query path: embed question, retrieve chunks, assemble prompt, call model, return answer.
- Start with a local JSON/SQLite store before adding a production vector database.

Quick check: Name one file/script in a minimal RAG project.

Concept check: In one sentence, explain how this idea matters in a real AI system: Building a Minimal RAG App.


## Lesson 6: RAG Quality and Failure Modes

Objective: Learn how RAG fails and how to measure whether it is improving.

Context:
RAG Quality and Failure Modes sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Bad chunking, weak retrieval, stale data, and vague questions can all produce bad answers. Evaluate retrieval separately from generation: did the right evidence appear in top results?

Track answer correctness, citation support, refusal behavior, and latency. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Bad chunking, weak retrieval, stale data, and vague questions can all produce bad answers.
- Evaluate retrieval separately from generation: did the right evidence appear in top results?
- Track answer correctness, citation support, refusal behavior, and latency.

Quick check: What should you evaluate separately from generation?

Concept check: In one sentence, explain how this idea matters in a real AI system: RAG Quality and Failure Modes.


## Lesson 7: RAG architecture and why it exists

Objective: Understand the core retrieve-augment-generate loop and where it fits.

Context:
RAG architecture and why it exists sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

RAG grounds an LLM in external evidence instead of relying only on model weights. The core loop is query, retrieve, augment, and generate.

Naive, advanced, and modular RAG differ in how retrieval and orchestration are separated. RAG is useful when facts change, sources matter, or private data must stay outside model training. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- RAG grounds an LLM in external evidence instead of relying only on model weights.
- The core loop is query, retrieve, augment, and generate.
- Naive, advanced, and modular RAG differ in how retrieval and orchestration are separated.
- RAG is useful when facts change, sources matter, or private data must stay outside model training.

Quick check: What is the first step in the core RAG loop?

Concept check: In one sentence, explain how this idea matters in a real AI system: RAG architecture and why it exists.


## Lesson 8: Document ingestion, loaders, and chunking

Objective: Turn raw documents into retrieval-ready chunks with useful metadata.

Context:
Document ingestion, loaders, and chunking sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Loaders often need to handle PDF, HTML, Markdown, DOCX, CSV, and code files. Chunking can be fixed-size, recursive, sentence-based, or semantic.

Metadata such as page number, section title, source, and timestamp make citations and filters work. Chunk size and overlap strongly affect retrieval quality and the lost-in-the-middle problem. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Loaders often need to handle PDF, HTML, Markdown, DOCX, CSV, and code files.
- Chunking can be fixed-size, recursive, sentence-based, or semantic.
- Metadata such as page number, section title, source, and timestamp make citations and filters work.
- Chunk size and overlap strongly affect retrieval quality and the lost-in-the-middle problem.

Quick check: What chunk field helps citations and filters work?

Concept check: In one sentence, explain how this idea matters in a real AI system: Document ingestion, loaders, and chunking.


## Lesson 9: Embedding, indexing, and vector databases

Objective: Store semantic representations so retrieval can scale beyond brute force.

Context:
Embedding, indexing, and vector databases sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Embedding models turn chunks into vectors and make semantic retrieval possible. Vector indexes and vector databases store vectors plus metadata for fast lookup and filtering.

Approximate nearest-neighbor methods trade a little recall for major speed gains. Batch embedding, index choice, and dimensionality are cost and quality decisions, not afterthoughts. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Embedding models turn chunks into vectors and make semantic retrieval possible.
- Vector indexes and vector databases store vectors plus metadata for fast lookup and filtering.
- Approximate nearest-neighbor methods trade a little recall for major speed gains.
- Batch embedding, index choice, and dimensionality are cost and quality decisions, not afterthoughts.

Quick check: Which structure speeds nearest-neighbor search?

Concept check: In one sentence, explain how this idea matters in a real AI system: Embedding, indexing, and vector databases.


## Lesson 10: Retrieval, reranking, and grounding

Objective: Improve retrieval quality and keep the generated answer anchored to evidence.

Context:
Retrieval, reranking, and grounding sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

Dense search, sparse search, and hybrid search solve different retrieval problems. Cross-encoder rerankers refine coarse retrieval candidates before generation.

Prompt construction should separate instructions, question, and retrieved context clearly. Good grounding teaches the model to abstain when the context is insufficient. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- Dense search, sparse search, and hybrid search solve different retrieval problems.
- Cross-encoder rerankers refine coarse retrieval candidates before generation.
- Prompt construction should separate instructions, question, and retrieved context clearly.
- Good grounding teaches the model to abstain when the context is insufficient.

Quick check: What does hybrid search combine?

Concept check: In one sentence, explain how this idea matters in a real AI system: Retrieval, reranking, and grounding.


## Lesson 11: Advanced RAG, evaluation, and production

Objective: Use advanced patterns and metrics to ship RAG responsibly.

Context:
Advanced RAG, evaluation, and production sits inside Retrieval-augmented generation. In practice, this topic is about learning how to explain the idea clearly, choose the right design choice, and spot where the concept stops being reliable.

GraphRAG, Self-reflective RAG, CRAG, RAPTOR, and Agentic RAG tackle harder retrieval problems. RAG evaluation tracks precision@k, recall@k, faithfulness, answer relevance, and context relevance.

Production concerns include access control, incremental indexing, caching, latency, and observability. Agentic RAG uses query decomposition, validation, and specialized workers to improve hard queries. Put another way, the important part is not memorizing the term. It is knowing what changes in a real product, what tradeoff you are accepting, and what can go wrong if you ignore it.

Key ideas:
- GraphRAG, Self-reflective RAG, CRAG, RAPTOR, and Agentic RAG tackle harder retrieval problems.
- RAG evaluation tracks precision@k, recall@k, faithfulness, answer relevance, and context relevance.
- Production concerns include access control, incremental indexing, caching, latency, and observability.
- Agentic RAG uses query decomposition, validation, and specialized workers to improve hard queries.

Quick check: Which RAG metric checks whether the answer follows the retrieved context?

Concept check: In one sentence, explain how this idea matters in a real AI system: Advanced RAG, evaluation, and production.
