# Four-week study plan

[Home](../README.md) · [Progress tracker](../CHECKLIST.md)

Aim for four 35–45 minute sessions per week. Spend the first half reading and the second half recalling, comparing, or solving a scenario. Take the [diagnostic](../practice/diagnostic.md) first and adjust the time you spend on each area.

| Week | Sessions 1–2 | Sessions 3–4 | Checkpoint |
|---|---|---|---|
| 1 · Ingest and transform | [Streaming](../topic-guides/streaming.md), [Data movement](../topic-guides/data-movement.md), [Glue](../topic-guides/glue.md) | [EMR](../topic-guides/emr.md) and [Orchestration](../topic-guides/orchestration.md) | Explain how you would capture changes from a database and independently replay an event stream |
| 2 · Store and query | [S3](../topic-guides/s3.md), [File layout](../topic-guides/file-layout.md), [Catalog](../topic-guides/catalog.md) | [Athena](../topic-guides/athena.md), [Redshift](../topic-guides/redshift.md), [Databases](../topic-guides/databases.md) | Complete the [batch workshop](../labs/README.md#workshop-1--design-a-sequencing-metrics-lake) and explain what Athena can skip reading |
| 3 · Operate and recover | [Monitoring](../topic-guides/monitoring.md), [Data quality](../topic-guides/data-quality.md) | [SQL patterns](../topic-guides/sql-patterns.md) and the [recovery workshop](../labs/README.md#workshop-2--recover-a-partially-loaded-batch) | Describe how to retry a partial load without duplicating rows |
| 4 · Secure and review | [Security](../topic-guides/security.md), [Governance](../topic-guides/governance.md) | [Decision guides](../decision-guides/README.md) and [pipeline challenges](../practice/pipeline-challenges.md) | Redo missed scenarios without opening the answers |

After each session, record one distinction from memory, such as “a crawler updates metadata; a job transforms rows.” If you have one week, compress each row into one or two study sessions and prioritize your diagnostic misses.
