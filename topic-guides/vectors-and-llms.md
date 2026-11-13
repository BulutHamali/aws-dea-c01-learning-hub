# Vectors, indexes, and LLMs in data pipelines

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

An **embedding** is a list of numbers produced from a record, such as a paragraph. Similar content often lies near other content in the embedding space. A vector index helps find nearby records. Unlike a product ID lookup, a similarity search usually ranks several candidates.

| Concept | Mental model | Decision |
|---|---|---|
| Exact nearest neighbors | Compare the query to every candidate | Useful as a baseline on small sets |
| HNSW | Navigate a graph of nearby vectors | Tune memory, build time, latency, and retrieval recall |
| IVF or IVFFlat | Group vectors into clusters and search selected clusters | Probe more clusters when retrieval recall matters more than latency |
| Metadata filtering | Limit results by fields such as region or dataset | Use access controls as well as filters when records have different permissions |

A document pipeline can split text into chunks, generate embeddings, and store the vectors with document IDs and permissions metadata. Amazon Bedrock Knowledge Bases can manage supported ingestion and retrieval workflows. Aurora PostgreSQL with pgvector and OpenSearch are examples of systems that can support vector search, depending on configuration. Keep query and stored embeddings compatible. A model or dimension change can require re-embedding and reindexing.

**When to integrate an LLM.** Consider one for extracting fields from messy free text. Validate the returned schema, route ambiguous outputs for review, and compare quality against labeled examples. A deterministic parser remains appropriate for a stable structured input. Focus your exam preparation on pipeline integration and data handling.

<details>
<summary>Recall check</summary>

A search feature returns similar safety manuals but misses documents with an exact model number. Evaluate hybrid retrieval that combines keyword matching and vector similarity. Measure recall on representative queries before changing index settings.

</details>

[AWS vector database decision guide](https://docs.aws.amazon.com/decision-guides/latest/decision-guides/vector-database-guide.html) · [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
