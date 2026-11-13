# Vectors, indexes, and LLMs in data pipelines

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

An **embedding** is a list of numbers produced from a piece of content, such as a paragraph of a lab protocol. Content with similar meaning gets numbers that are close together. A **vector index** finds the nearest embeddings to a query quickly. Unlike a lookup by ID, a similarity search returns a ranked list of candidates.

The exam stays at the data engineering level: how documents become vectors, where vectors are stored, which index type fits, and how to use a large language model (LLM) safely inside a pipeline.

## Chunking, embeddings, and Bedrock Knowledge Bases

**Vectorization** turns documents into searchable vectors:

1. **Extract** text from source files, such as PDFs in S3.
2. **Chunk** the text into pieces small enough to embed and retrieve.
3. **Embed** each chunk with an embedding model, such as Amazon Titan Text Embeddings.
4. **Store** each vector with its chunk text, document ID, and permission metadata.
5. **Retrieve** the nearest chunks for a question, filtered by metadata, and pass them to an LLM. This is **retrieval-augmented generation (RAG)**.

**Amazon Bedrock Knowledge Bases** manage steps 1 to 5 for documents in S3 and other sources.

| Chunking strategy | Behavior |
|---|---|
| Default | About 300 tokens per chunk, keeping whole sentences |
| Fixed-size | You set maximum tokens and overlap percentage |
| Hierarchical | Small child chunks for precise matching, replaced by larger parent chunks at retrieval for context |
| Semantic | Splits by meaning using a foundation model. Costs more |
| None | Each document is one chunk |

Query and stored embeddings must come from the same model with the same dimension. Changing the model means re-embedding and reindexing everything.

## HNSW and IVF trade-offs

| Index | How it works | Tune | Trade-off |
|---|---|---|---|
| Exact (flat) | Compare the query with every vector | Nothing | Perfect recall, slow on large sets. Good as a baseline |
| HNSW (Hierarchical Navigable Small World) | Navigates a layered graph of neighbouring vectors | `m` (links per node), `ef_construction` (build quality), `ef_search` (search breadth) | Fast and accurate queries, more memory, slower builds |
| IVF / IVFFlat (inverted file) | Groups vectors into clusters, then searches only the closest clusters | Number of lists (clusters), number of probes | Faster builds and less memory. Needs training data. Probing more clusters raises recall but slows queries |

**Recall** here means the share of the true nearest neighbours the index actually returns. Approximate indexes trade some recall for speed.

## Where to store vectors

| Store | Fits |
|---|---|
| Aurora PostgreSQL with pgvector | Vectors next to relational data. Supports HNSW (pgvector 0.5.0+) and IVFFlat. Bedrock Knowledge Bases can use it |
| Amazon OpenSearch Service or Serverless | Large-scale search that combines keyword and vector matching (hybrid search) |
| Amazon S3 Vectors | Low-cost storage of large vector sets in S3 vector buckets |
| Amazon MemoryDB | Very low latency vector search in memory |
| Neptune Analytics | Graph plus vector search (GraphRAG) |

## LLM extraction and output validation

Consider an LLM when input is messy free text, such as instrument notes, and you need structured fields. Keep a deterministic parser for stable structured input.

1. Call the model, for example through Amazon Bedrock from a Lambda function or Glue job, with a prompt that requests a fixed JSON schema.
2. **Validate** every response: correct JSON, required fields present, types and ranges valid.
3. Route failures and low-confidence results to a review queue instead of publishing them.
4. Measure accuracy against a labeled sample before and after prompt or model changes.
5. Watch cost and throttling. Batch requests where possible.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Bedrock default chunking | About 300 tokens, sentence-aware | Know what you get without configuration | [Knowledge Base chunking](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html) |
| pgvector HNSW support on Aurora | pgvector 0.5.0 or higher | Older versions only offer IVFFlat or exact search | [Aurora as a Knowledge Base](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html) |
| Knowledge Base vector stores | OpenSearch Serverless and managed clusters, S3 Vectors, Aurora PostgreSQL, Neptune Analytics, and third-party stores | Pick the store, then match the embedding dimension | [Knowledge Base setup](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html) |

## Common mistake

Searching only by vector similarity when users type exact part numbers. Similar meaning does not mean the same identifier. Use hybrid search that combines keyword and vector matching.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| HNSW vs. IVF | Best query speed and recall with more memory vs. faster builds and less memory |
| Embedding vs. index | The numbers for one item vs. the structure that searches many |
| Metadata filter vs. access control | Narrows results vs. enforces who may see them. Use both |
| LLM vs. deterministic parser | Messy free text vs. stable structured input |

**Exam cues:** "Graph-based index" → HNSW. "Cluster-based index" → IVF. "Managed chunking and embedding of S3 documents" → Bedrock Knowledge Bases. "Vectors alongside relational data" → Aurora PostgreSQL with pgvector.

## Try it

A search over 5 million protocol chunks compares every vector and takes several seconds. The team accepts approximate results, has plenty of memory, and wants the best recall at low latency.

<details>
<summary>Show the reasoning</summary>

Build an HNSW index and tune `ef_search` while measuring recall against exact results on a test set. HNSW fits because memory is available and query latency matters more than build time.

</details>

## AWS documentation

- [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Knowledge Base chunking](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html)
- [Aurora PostgreSQL as a vector store](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html)
- [AWS vector database decision guide](https://docs.aws.amazon.com/decision-guides/latest/decision-guides/vector-database-guide.html)

*Last verified against AWS documentation: November 2026.*
