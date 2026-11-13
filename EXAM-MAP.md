# DEA-C01 exam map

[Home](README.md) · [Topic index](topic-guides/README.md)

The percentages are shares of scored content. AWS maintains the task statements and current service list in its [official DEA-C01 exam guide](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01.html).

| Domain | Weight | Practice these decisions |
|---|---:|---|
| 1. Data Ingestion and Transformation | 34% | Choose batch, streaming, or CDC ingestion. Select a transformation engine. Coordinate retries and dependencies. [Streaming](topic-guides/streaming.md) · [Glue](topic-guides/glue.md) · [EMR](topic-guides/emr.md) · [Data movement](topic-guides/data-movement.md) · [Orchestration](topic-guides/orchestration.md) |
| 2. Data Store Management | 26% | Choose a store from the access pattern. Design data layout, catalog metadata, and retention. [S3](topic-guides/s3.md) · [File layout](topic-guides/file-layout.md) · [Databases](topic-guides/databases.md) · [Catalog](topic-guides/catalog.md) · [Redshift](topic-guides/redshift.md) |
| 3. Data Operations and Support | 22% | Automate recovery, query data, isolate failures, and measure quality. [Athena](topic-guides/athena.md) · [Monitoring](topic-guides/monitoring.md) · [Data quality](topic-guides/data-quality.md) · [SQL patterns](topic-guides/sql-patterns.md) |
| 4. Data Security and Governance | 18% | Identify the executing role, protect data and keys, control access, and audit activity. [Security](topic-guides/security.md) · [Governance](topic-guides/governance.md) |

Practice tasks often cross domains. A failed Athena query can involve a missing partition, missing S3 access, or a missing KMS grant. Start with the actual error and identify which layer produced it.
