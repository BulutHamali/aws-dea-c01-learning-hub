# Topic guides

[Home](../README.md) · [Exam map](../EXAM-MAP.md) · [Decision guides](../decision-guides/README.md)

Every guide follows the same shape: the core idea in plain words, decision tables, a **Numbers and defaults** table with an AWS source on every row (where the topic has numbers), a common mistake, a **Commonly confused** table, exam cues, a worked "Try it" scenario, and the date it was last checked against AWS documentation.

## Domain 1 · Data Ingestion and Transformation (34%)

| Guide | What you will learn |
|---|---|
| [Streaming with Kinesis, Firehose, MSK, and Flink](streaming.md) | Shard limits, fan-out, retention and replay, stateful windows |
| [Data movement and database CDC](data-movement.md) | DMS full load and CDC, DataSync, Transfer Family, AppFlow, manifests |
| [AWS Glue jobs, crawlers, and development tools](glue.md) | Worker types, Flex, connections, DynamicFrames, bookmarks |
| [Lambda for data pipelines](lambda.md) | Kinesis and SQS event sources, failure handling, concurrency, storage |
| [Orchestration with EventBridge, Step Functions, and MWAA](orchestration.md) | Schedules, events, Pipes, retries, alerts, debugging workflows |
| [Amazon EMR, distributed processing, and skew](emr.md) | Engine choice, node types and Spot, Spark logs, skew fixes |
| [APIs, SDKs, throttling, and resumable ingestion](apis-and-sdks.md) | Pagination, 429 handling, SDK paginators and retries, data APIs |
| [Testing, infrastructure as code, and CI/CD](deployment.md) | CloudFormation, CDK, SAM gradual deployments, pipelines |
| [Programming concepts for data engineers](pipeline-engineering.md) | Languages, batching and pushdown, containers, data structures |

## Domain 2 · Data Store Management (26%)

| Guide | What you will learn |
|---|---|
| [Amazon S3 storage classes, lifecycle, retention, and recovery](s3.md) | Storage class minimums, restore tiers, Object Lock, replication and RTC |
| [Choose a data store from the access pattern](databases.md) | DynamoDB keys and limits, MemoryDB, DocumentDB, Keyspaces, TTL |
| [Amazon Redshift loads, table design, access paths, and locks](redshift.md) | COPY and MERGE, distribution, Spectrum, materialized views, locks |
| [File formats, partitions, compaction, and data shape](file-layout.md) | Parquet, partitioning, bucketing, small files, volume, velocity, variety |
| [Glue Data Catalog, crawlers, and partition sync](catalog.md) | Crawler policies, partition projection, Schema Registry |
| [Apache Iceberg, open table formats, and Amazon S3 Tables](iceberg.md) | Snapshots, time travel, OPTIMIZE and VACUUM, managed maintenance |
| [Data modeling, schema evolution, conversion, and lineage](data-modeling.md) | Grain, star schemas, safe schema changes, DMS Schema Conversion, lineage |
| [Vectors, indexes, and LLMs in data pipelines](vectors-and-llms.md) | Chunking, HNSW vs. IVF, vector stores, validating LLM output |

## Domain 3 · Data Operations and Support (22%)

| Guide | What you will learn |
|---|---|
| [Amazon Athena queries, cost control, and federation](athena.md) | Bytes scanned, CTAS limits, workgroup controls, federated queries |
| [Monitor, log, and troubleshoot data pipelines](monitoring.md) | Freshness alarms, EventBridge alerts, log retention, log analysis tools |
| [Data quality, quarantine, and safe recovery](data-quality.md) | DQDL rules, quarantine, reconciliation, idempotent reruns |
| [SQL for validation, deduplication, analysis, and loading](sql-patterns.md) | Windows, pivots, duplicates, views, tested SQL examples |
| [Data preparation, analysis, visualization, and sampling](analysis-and-data-prep.md) | DataBrew, Unified Studio, QuickSight SPICE, Spark notebooks, sampling |

## Domain 4 · Data Security and Governance (18%)

| Guide | What you will learn |
|---|---|
| [IAM, KMS, credentials, and encryption](security.md) | Role trust, least privilege, Secrets Manager, KMS across accounts, S3 encryption |
| [Networking for data pipelines](networking.md) | Security groups, NAT allowlists, gateway and interface endpoints, shared responsibility |
| [Lake Formation, access models, sharing, and PII discovery](governance.md) | Data filters, LF-Tags and ABAC, Macie, datashares, governance patterns |
| [Masking, encryption in transit, residency, and audit evidence](privacy-and-audit.md) | Masking and tokenization, Region controls, CloudTrail and Config evidence |
| [Technical catalogs, business catalogs, and SageMaker Unified Studio](catalog-and-unified-studio.md) | Domains, domain units, projects, subscriptions and fulfillment |
| [Recognition-level services](service-recognition.md) | Amazon Q, Kendra, Data Exchange, Direct Connect, and 2026 name changes |
