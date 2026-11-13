# Topic guides

[Home](../README.md) · [Exam map](../EXAM-MAP.md) · [Decision guides](../decision-guides/README.md)

| Topic | What you will learn |
|---|---|
| [Streaming with Kinesis, Firehose, MSK, and Flink](streaming.md) | A stream keeps events moving while producers and consumers run independently. Start by asking whether you need a replayable source, a delivery service, or a processor. |
| [Data movement and database CDC](data-movement.md) | Start with the shape of what needs to move. Database changes, existing files, and incoming partner uploads require different interfaces. |
| [AWS Glue jobs, crawlers, and development tools](glue.md) | Glue brings together several tools for preparing data. Follow the input and output to identify which tool you need. |
| [Amazon EMR and distributed processing](emr.md) | EMR runs big-data frameworks such as Spark. Choose the deployment mode based on the control and infrastructure your team needs. |
| [Orchestration with EventBridge, Step Functions, and MWAA](orchestration.md) | Orchestration decides what runs next and what happens after failure. Jobs do the processing and events tell the system when work may be needed. |
| [Amazon S3 lifecycle, replication, and lake storage](s3.md) | S3 stores data objects under keys. Use the key layout to make the stages of the pipeline visible, such as raw/, curated/, and quarantine/. |
| [File formats, partitions, and compaction](file-layout.md) | The bytes a query has to read depend on the file format, the partition filter, and the size and number of files. |
| [Glue Data Catalog and schema management](catalog.md) | The catalog tells a query engine where a table lives, which columns it has, and how to interpret its files. |
| [Athena queries, cost, and workgroups](athena.md) | Athena lets you use SQL over S3 datasets and can query supported external sources through connectors. Query performance depends heavily on how the data is laid out. |
| [Redshift loads, Spectrum, and streaming ingestion](redshift.md) | Redshift is an analytical warehouse. Decide whether data should live in a warehouse table, remain in S3, or arrive through a live stream. |
| [Choose a database from the access pattern](databases.md) | Describe the most important read and write before choosing a data store. Include latency, key distribution, and whether queries are known in advance. |
| [Monitor and troubleshoot data pipelines](monitoring.md) | A healthy pipeline delivers complete data on time. Track freshness, throughput, and failures so a technically successful job cannot hide a missing dataset. |
| [Data quality, quarantine, and safe recovery](data-quality.md) | A quality gate defines the conditions a dataset must meet before it becomes visible to downstream readers. |
| [SQL for validation, deduplication, and loading](sql-patterns.md) | Start by stating the grain of the dataset. If one row should represent one event, every join and merge should preserve or intentionally change that grain. |
| [IAM, KMS, credentials, and network access](security.md) | Follow the identity that actually executes the operation. A successful launch from your console only proves that your identity could start the job. |
| [Lake Formation, Macie, and CloudTrail](governance.md) | Governance answers who can see the data, what they can see, and how you can review what happened later. |
| [APIs and deployment fundamentals](pipeline-engineering.md) | Pagination, throttling, distributed processing, and repeatable deployments |
| [Data modeling and schema evolution](data-modeling.md) | Grain, warehouse facts, DynamoDB keys, migration, and lineage |
| [Iceberg](iceberg.md) | Snapshots, compaction, partition evolution, and retention |
| [Vectors and LLMs](vectors-and-llms.md) | Embeddings, index choices, and document processing |
| [Business catalogs and Unified Studio](catalog-and-unified-studio.md) | Asset discovery, domains, domain units, and projects |
| [Analysis and data preparation](analysis-and-data-prep.md) | DataBrew, visualizations, SQL, and sampling |
| [Privacy and audit](privacy-and-audit.md) | Masking, key controls, data residency, and audit evidence |
| [Lambda for data pipelines](lambda.md) | Stream consumers, queue failures, concurrency, and storage |
