# Monitor and troubleshoot data pipelines

[Topic index](README.md) · [Home](../README.md)

## The idea

A healthy pipeline delivers complete data on time. Track freshness, throughput, and failures so a technically successful job cannot hide a missing dataset.

## How to decide

| Concept | When it matters |
|---|---|
| **Metrics and alarms** | CloudWatch metrics show trends and support alarms. Compare source lag, output freshness, and failures against a baseline. |
| **Logs** | Use execution logs and correlation IDs to identify the input, run, and stage that failed. |
| **Warehouse diagnostics** | Use Redshift SYS_QUERY_HISTORY for status and timing and SYS_LOAD_ERROR_DETAIL for COPY errors. Inspect plans when a query succeeds slowly. |
| **Cost** | Use Cost Explorer for spend trends and AWS Budgets for threshold alerts. Correlate a spike with pipeline metrics, such as an increase in Athena bytes scanned. |

## Common mistake

A green job status can coincide with empty output. Compare row counts, late-arrival rates, and the timestamp of the most recent complete partition.

## Try it

Analysts say yesterday’s dashboard is stale. The Glue job completed and the warehouse is reachable.

<details>
<summary>Show the reasoning</summary>

Trace one expected partition end to end. Compare source arrival, job input/output counts, catalog metadata, load status, and dashboard refresh time.

</details>

## AWS documentation

- [AWS documentation · WhatIsCloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [AWS documentation · SYS_QUERY_HISTORY](https://docs.aws.amazon.com/redshift/latest/dg/SYS_QUERY_HISTORY.html)
- [AWS documentation · SYS_LOAD_ERROR_DETAIL](https://docs.aws.amazon.com/redshift/latest/dg/SYS_LOAD_ERROR_DETAIL.html)
