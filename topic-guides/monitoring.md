# Monitor, log, and troubleshoot data pipelines

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

A healthy pipeline delivers complete data on time. A green "SUCCEEDED" status is not the same thing. A job can succeed while reading zero files. Monitor three things for every dataset:

- **Freshness:** how old is the newest complete partition?
- **Volume:** did roughly the expected number of rows arrive?
- **Failures:** did any step fail, retry, or send records to quarantine?

## Correlation IDs, freshness, and alarms

Give each batch a **correlation ID**, such as `run_date=2026-01-01/attempt=2`. Write it into every log line, output path, and metric. When a dashboard is stale, you can search for one ID across every service.

Publish custom metrics such as `RowsPublished` and `MinutesSinceLastPartition`. A CloudWatch alarm on `MinutesSinceLastPartition > 90` catches a missing dataset even when no job reported an error.

## CloudWatch alarms and SNS notifications

| Signal | Where it comes from | Typical action |
|---|---|---|
| Glue job `FAILED`, `TIMEOUT`, or `STOPPED` | EventBridge event "Glue Job State Change" | Rule sends to SNS or starts a recovery workflow |
| Glue crawler `Failed` | EventBridge event "Glue Crawler State Change" | Notify the owner |
| Step Functions execution failed | EventBridge execution status event | Notify and link the execution history |
| Metric over a threshold | CloudWatch alarm | Alarm action publishes to an SNS topic |
| Error pattern in logs | Metric filter on a log group, then an alarm | Count matching lines as a metric |

SNS delivers to email, SMS, Lambda, SQS, or HTTPS endpoints. See [alerts in orchestration](orchestration.md#alerts-buffers-and-failed-deliveries).

## Lag, skew, scan volume, and query queues

| Symptom | Check first | Likely fix |
|---|---|---|
| Stream consumer falls behind | `GetRecords.IteratorAgeMilliseconds` for Kinesis, consumer duration, sink latency | Enhanced fan-out, more parallelism, or fix the slow sink. See [streaming](streaming.md) |
| One Spark task runs far longer than the others | Spark UI stage timeline and shuffle read size per task | Fix data skew. See [EMR](emr.md#diagnose-and-mitigate-partition-and-join-skew) |
| Athena query is slow or expensive | Bytes scanned and `EXPLAIN` | Partitions, Parquet, compaction |
| Redshift queries wait | Queue time in `SYS_QUERY_HISTORY` and WLM queue metrics | Separate queues, concurrency scaling, or tune the query |
| Lambda throttles | `Throttles` and `ConcurrentExecutions` metrics | Raise or reserve concurrency, or slow the source |
| DynamoDB throttles | Throttled request metrics, Contributor Insights | Fix the hot key or raise capacity |

## CloudWatch log groups, retention, and queries

Application logs go to **log groups** in CloudWatch Logs. Glue, Lambda, Step Functions, MWAA, and EMR Serverless can all write there.

- **Retention:** log groups keep data forever by default. Set a retention period on every log group, from one day up to ten years.
- **Log class:** choose Standard or Essentials (formerly Infrequent Access) when you create the group. Essentials costs less but has no metric filters, subscription filters, or Live Tail. You cannot change the class later.
- **Automation:** set retention in infrastructure as code so new groups are not left at "never expire".
- **Encryption:** associate a KMS key with a log group for customer-managed encryption.

## Logs Insights, Athena, EMR, and OpenSearch

| Log volume and need | Tool |
|---|---|
| Interactive search across recent CloudWatch log groups | CloudWatch Logs Insights |
| SQL over logs archived in S3, such as CloudTrail or S3 access logs | Athena |
| Very large volumes of application logs that need custom processing | EMR with Spark over logs in S3 |
| Full-text search, dashboards, and near real-time log analytics | Amazon OpenSearch Service, fed by a subscription filter or Firehose |
| Stream logs out of CloudWatch as they arrive | Subscription filter to Kinesis, Firehose, Lambda, or OpenSearch |

## S3 log archive and distributed processing with EMR

To audit very large log volumes, deliver logs to S3 with Firehose or a subscription filter, partition by date, and convert to Parquet. Query with Athena for ad hoc questions or run an EMR Spark job for heavy aggregation across months.

## Cost monitoring

Use Cost Explorer for spend trends and AWS Budgets for threshold alerts. Correlate a cost spike with a pipeline metric, such as a jump in Athena bytes scanned after someone dropped a partition filter.

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Default log retention | Never expire | Logs grow forever unless you set retention | [Working with log groups](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html) |
| Subscription filters per log group | Up to 5 | Plan fan-out of logs to several destinations | [Subscriptions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Subscriptions.html) |
| Essentials log class | No metric filters, subscription filters, or Live Tail. Class is fixed at creation | Do not use it for logs that drive alarms | [Log classes](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html) |
| Glue job state events | `SUCCEEDED`, `FAILED`, `TIMEOUT`, `STOPPED` | Match these in an EventBridge rule for alerts | [Glue with EventBridge](https://docs.aws.amazon.com/glue/latest/dg/automating-awsglue-with-cloudwatch-events.html) |

## Common mistake

Alerting only on job failures. A job that succeeds with empty input never fires an alarm. Alarm on freshness and row counts too.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| CloudWatch Logs vs. CloudTrail | Application log lines vs. AWS API calls |
| Logs Insights vs. Athena | Query logs in CloudWatch vs. query logs archived in S3 |
| Metric filter vs. subscription filter | Turn log lines into a metric vs. stream log lines to another service |
| Standard vs. Essentials log class | Full features vs. lower cost without filters |

**Exam cues:** "Notify when a Glue job fails" → EventBridge rule plus SNS. "Logs kept forever, rising cost" → retention policy. "Stream logs to OpenSearch" → subscription filter.

## Try it

Analysts say yesterday's dashboard is stale. The Glue job shows `SUCCEEDED` and the warehouse is reachable.

<details>
<summary>Show the reasoning</summary>

Follow the correlation ID end to end: source arrival in S3, job input and output row counts, the curated partition, catalog registration, the warehouse load, and dashboard refresh time. Add a freshness alarm so the next gap pages someone before analysts notice.

</details>

## AWS documentation

- [What is Amazon CloudWatch?](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
- [Glue events in EventBridge](https://docs.aws.amazon.com/glue/latest/dg/automating-awsglue-with-cloudwatch-events.html)
- [SYS_QUERY_HISTORY](https://docs.aws.amazon.com/redshift/latest/dg/SYS_QUERY_HISTORY.html)

*Last verified against AWS documentation: November 2026.*
