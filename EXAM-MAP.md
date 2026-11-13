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

## Task-by-task study map

This map follows the AWS exam guide’s task numbering. The descriptions below are study objectives in plain language.

| Task | What you should be able to explain | Study material |
|---|---|---|
| 1.1 | Ingest files, database changes, API pages, or streaming events. Handle replay, fan-out, and rate limits | [Data movement](topic-guides/data-movement.md), [Streaming](topic-guides/streaming.md), [API ingestion](topic-guides/pipeline-engineering.md), [Lambda stream consumers](topic-guides/lambda.md#read-a-kinesis-stream-with-lambda) |
| 1.2 | Choose a processing engine and validate data. Recognize when an LLM fits unstructured input | [Glue](topic-guides/glue.md), [EMR](topic-guides/emr.md), [Vectors and LLMs](topic-guides/vectors-and-llms.md) |
| 1.3 | Schedule work, route events, retry failed steps, and notify operators | [Orchestration](topic-guides/orchestration.md), [Pipeline engineering](topic-guides/pipeline-engineering.md) |
| 1.4 | Design code for distributed processing, test changes, manage Lambda capacity, and deploy repeatably | [Pipeline engineering](topic-guides/pipeline-engineering.md), [Lambda capacity](topic-guides/lambda.md#reserved-and-provisioned-concurrency), [SQL](topic-guides/sql-patterns.md) |
| 2.1 | Choose storage by workload. Understand federated access, open table formats, and vector indexes | [Databases](topic-guides/databases.md), [Redshift](topic-guides/redshift.md), [Iceberg](topic-guides/iceberg.md), [Vector indexes](topic-guides/vectors-and-llms.md) |
| 2.2 | Keep table metadata in sync and distinguish technical and business catalogs | [Catalog](topic-guides/catalog.md), [Unified Studio](topic-guides/catalog-and-unified-studio.md) |
| 2.3 | Load, unload, transition, retain, expire, and recover data | [S3](topic-guides/s3.md), [Redshift](topic-guides/redshift.md), [Databases](topic-guides/databases.md) |
| 2.4 | Model data at the right grain, handle schema change, and establish lineage | [Modeling](topic-guides/data-modeling.md), [File layout](topic-guides/file-layout.md), [Vectors](topic-guides/vectors-and-llms.md) |
| 3.1 | Automate processing and troubleshoot scheduled or event-triggered jobs | [Orchestration](topic-guides/orchestration.md), [Pipeline engineering](topic-guides/pipeline-engineering.md), [Lambda](topic-guides/lambda.md), [Data preparation](topic-guides/analysis-and-data-prep.md) |
| 3.2 | Choose a tool for SQL, interactive exploration, or visualization | [Athena](topic-guides/athena.md), [Redshift](topic-guides/redshift.md), [Analysis](topic-guides/analysis-and-data-prep.md) |
| 3.3 | Diagnose lag, performance, and failed loads using logs and metrics | [Monitoring](topic-guides/monitoring.md), [Redshift](topic-guides/redshift.md), [Audit](topic-guides/privacy-and-audit.md) |
| 3.4 | Detect missing or inconsistent records, choose a sampling method, and account for skew | [Data quality](topic-guides/data-quality.md), [Data preparation](topic-guides/analysis-and-data-prep.md), [EMR](topic-guides/emr.md) |
| 4.1 | Identify the execution principal and diagnose credential or network problems | [IAM and network access](topic-guides/security.md), [Unified Studio](topic-guides/catalog-and-unified-studio.md) |
| 4.2 | Enforce least privilege at AWS, catalog, and database layers | [Security](topic-guides/security.md), [Lake Formation](topic-guides/governance.md) |
| 4.3 | Apply encryption, cross-account key permissions, and masking | [Security](topic-guides/security.md), [Privacy](topic-guides/privacy-and-audit.md) |
| 4.4 | Collect and query the right audit evidence | [Privacy and audit](topic-guides/privacy-and-audit.md), [Monitoring](topic-guides/monitoring.md) |
| 4.5 | Govern sharing, classify sensitive data, and keep it in approved locations | [Governance](topic-guides/governance.md), [Unified Studio](topic-guides/catalog-and-unified-studio.md), [Privacy](topic-guides/privacy-and-audit.md) |

[Official certification page](https://aws.amazon.com/certification/certified-data-engineer-associate/) · [Official exam guide PDF](https://docs.aws.amazon.com/pdfs/aws-certification/latest/data-engineer-associate-01/data-engineer-associate-01.pdf)

## Ingestion and orchestration skills

| Skills | Section |
|---|---|
| 1.1.1 | [Consumer integrations and source selection](topic-guides/streaming.md#consumer-integrations-and-source-selection) |
| 1.1.2 | [Batch ingestion by source and destination](topic-guides/data-movement.md#batch-ingestion-by-source-and-destination) |
| 1.1.3 | [Manifests and incremental loads](topic-guides/data-movement.md#manifests-and-incremental-loads) |
| 1.1.5 | [Schedules, time zones, and backfills](topic-guides/orchestration.md#schedules-time-zones-and-backfills) |
| 1.1.6 | [S3 events and EventBridge routing](topic-guides/orchestration.md#s3-events-and-eventbridge-routing) |
| 1.1.7 | [Read a Kinesis stream with Lambda](topic-guides/lambda.md#read-a-kinesis-stream-with-lambda) |
| 1.1.10 | [Fan-in, fan-out, and throughput](topic-guides/streaming.md#fan-in-fan-out-and-throughput) |
| 1.1.11 | [Retention, checkpoints, and replay](topic-guides/streaming.md#retention-checkpoints-and-replay) |
| 1.1.12 | [Event-time state and stateless transforms](topic-guides/streaming.md#event-time-state-and-stateless-transforms) |
| 1.2.2 / 2.2.5 | [Glue connections, networking, and credentials](topic-guides/glue.md#glue-connections-networking-and-credentials) |
| 1.2.4 | [Glue worker, execution, and scaling choices](topic-guides/glue.md#numbers-and-defaults) |
| 1.2.3 / 1.2.7 | [Joining sources, schema alignment, and skew](topic-guides/glue.md#joining-sources-schema-alignment-and-skew) |
| 1.3.1 / 3.1.1 | [Step Functions, Glue workflows, and Airflow](topic-guides/orchestration.md#step-functions-glue-workflows-and-airflow) |
| 1.3.2 | [Queues, backpressure, retries, and recovery](topic-guides/orchestration.md#queues-backpressure-retries-and-recovery) |
| 1.3.3 | [Service integrations and execution history](topic-guides/orchestration.md#service-integrations-and-execution-history) |
| 1.4.2 | [Reserved and provisioned concurrency](topic-guides/lambda.md#reserved-and-provisioned-concurrency) |
| 1.4.7 | [Temporary and shared storage](topic-guides/lambda.md#temporary-and-shared-storage) |
| 3.1.2 | [Debug task failures in Step Functions and MWAA](topic-guides/orchestration.md#debug-task-failures-in-step-functions-and-mwaa) |
| 3.1.8 | [Choose Lambda for a data pipeline](topic-guides/lambda.md#choose-lambda-for-a-data-pipeline) |
| 3.1.9 | [EventBridge Rules, Scheduler, and Pipes](topic-guides/orchestration.md#eventbridge-rules-scheduler-and-pipes) |

## Shared exam objectives

Keep both official skill IDs when looking up the exam guide. Each pair shares a teaching destination and counts once toward practice coverage.

| Official skill IDs | Shared teaching destination |
|---|---|
| 1.3.4 / 3.3.3 | [Alerts, buffers, and failed deliveries](topic-guides/orchestration.md#alerts-buffers-and-failed-deliveries) |
| 1.4.5 / 1.4.8 | [Infrastructure as code](topic-guides/pipeline-engineering.md#how-the-pieces-fit) |
| 3.3.5 / 4.4.1 | [CloudTrail evidence](topic-guides/privacy-and-audit.md#choose-the-right-evidence) |
| 3.3.7 / 4.4.2 | [CloudWatch application logs](topic-guides/monitoring.md#how-to-decide) |
| 3.3.8 / 4.4.4 | [Log analysis](topic-guides/privacy-and-audit.md#choose-the-right-evidence) |
