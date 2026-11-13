# Four-week study plan

[Home](../README.md) · [Six-week plan](6-week-plan.md) · [Progress tracker](../CHECKLIST.md) · [Study method](study-method.md)

Four 60-minute sessions per week, two guides per session at most. Spend the first half reading and the second half recalling, comparing, or solving the guide's "Try it" scenario. Take the [diagnostic](../practice/diagnostic.md) first and move extra time to the domains where you missed two or more prompts.

| Week | Session 1 | Session 2 | Session 3 | Session 4 |
|---|---|---|---|---|
| 1 · Ingest and transform | [Streaming](../topic-guides/streaming.md), [Lambda](../topic-guides/lambda.md) | [Data movement](../topic-guides/data-movement.md), [APIs and SDKs](../topic-guides/apis-and-sdks.md) | [Glue](../topic-guides/glue.md), [EMR](../topic-guides/emr.md) | [Orchestration](../topic-guides/orchestration.md), [Programming concepts](../topic-guides/pipeline-engineering.md) |
| 2 · Store and model | [Deployment](../topic-guides/deployment.md), [File layout](../topic-guides/file-layout.md) | [S3](../topic-guides/s3.md), [Databases](../topic-guides/databases.md) | [Redshift](../topic-guides/redshift.md), [Catalog](../topic-guides/catalog.md) | [Iceberg](../topic-guides/iceberg.md), [Data modeling](../topic-guides/data-modeling.md) |
| 3 · Operate and recover | [Vectors and LLMs](../topic-guides/vectors-and-llms.md), [Athena](../topic-guides/athena.md) | [Monitoring](../topic-guides/monitoring.md), [Data quality](../topic-guides/data-quality.md) | [SQL patterns](../topic-guides/sql-patterns.md), [Analysis and prep](../topic-guides/analysis-and-data-prep.md) | [Timed set](../practice/timed-set.md), then review every miss |
| 4 · Secure and review | [Security](../topic-guides/security.md), [Networking](../topic-guides/networking.md) | [Governance](../topic-guides/governance.md), [Privacy and audit](../topic-guides/privacy-and-audit.md) | [Unified Studio](../topic-guides/catalog-and-unified-studio.md), [Service recognition](../topic-guides/service-recognition.md) | [Full mock](../practice/full-mock.md) under exam timing |

## Checkpoints

| End of week | You should be able to |
|---|---|
| 1 | Explain how to replay a stream after an outage, and how to retry an API safely after a crash |
| 2 | Pick a storage class from a retrieval deadline, and design a Redshift load that can be rerun |
| 3 | Trace a missing partition end to end, and write a window function from memory |
| 4 | Fix a cross-account KMS denial, and explain why Lake Formation filters need S3 access removed |

## Hands-on

If you have an AWS sandbox account, add one lab per week: [lab 2](../labs/hands-on/02-streaming/README.md) in week 1, [lab 1](../labs/hands-on/01-batch-lake/README.md) and [lab 3](../labs/hands-on/03-redshift-load/README.md) in weeks 2 and 3, and [labs 4 and 5](../labs/README.md#hands-on-labs) in week 4. Without an account, do the [paper workshops](../labs/README.md#paper-workshops).

After each session, write one distinction from memory, such as "a crawler updates metadata; a job transforms rows." Use the [recall cards](../practice/recall-cards.md) on days without a session. Finish with the [question bank](../practice/question-bank.md) for any skill the mock showed as weak, then try AWS's official practice exam.
