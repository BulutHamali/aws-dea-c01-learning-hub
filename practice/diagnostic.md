# DEA-C01 diagnostic

[Home](../README.md) · [Progress tracker](../CHECKLIST.md) · [Exam map](../EXAM-MAP.md)

Take 20 minutes. There are no answer options. For each prompt, write the service or setting you would choose **and the one requirement that decides it**. Then mark your confidence: sure, unsure, or guess. Open the answers only after you finish all twelve.

Each prompt hides a trap that the real exam uses. If you fall for one, study the linked section before the four-week plan's matching week.

## Domain 1 · Ingestion and transformation

1. Two applications read the same instrument stream. After a 30-hour outage, one must reprocess everything it missed. Which service and which setting?
2. A Glue job that reads from RDS fails with a timeout. The password was verified from a bastion host. What do you check first, and why not the password?
3. A Lambda function writing to Aurora opens thousands of connections during spikes. Its own latency is fine. Which Lambda setting, and which similar-sounding setting would not help?

## Domain 2 · Data store management

4. Regulators require that nobody, including administrators, can delete raw files for seven years. Name both features you must enable.
5. A table receives daily row corrections, and auditors must query it as it was 60 days ago. Which table format, and what maintenance setting could silently break the audit?
6. A DynamoDB table in on-demand mode throttles writes while total traffic is far below the table limit. What is the cause, and what is the fix?

## Domain 3 · Operations and support

7. A Glue job reports SUCCEEDED, but yesterday's partition is missing from the dashboard. List the evidence you collect, in order.
8. An Athena workgroup must stop any single query from scanning more than 1 TB. Which control, and which similar control would not stop the query?
9. One Spark task in a join stage runs 50 times longer than the others. What is the cause, and why does adding nodes not help?

## Domain 4 · Security and governance

10. A Glue job in account B can list objects in account A's bucket but gets a KMS AccessDenied when reading them. The objects use the `aws/s3` key. What must change?
11. Contractors may query only their site's rows and no identifier columns through Athena. They currently have `s3:GetObject` on the bucket. Name both steps.
12. Security asks who read a donor file last month. CloudTrail has only default settings. What can you find, and what should have been enabled?

<details>
<summary>Answers and review links</summary>

1. **Kinesis Data Streams with retention above 30 hours.** The trap: the default retention is 24 hours, so default settings lose six hours. [Streaming](../topic-guides/streaming.md#retention-checkpoints-and-replay)
2. **Security groups, routes, and DNS**, including Glue's self-referencing rule. A bad password fails fast with an authentication error. A timeout means packets never arrived. [Networking](../topic-guides/networking.md#security-groups-for-private-database-access)
3. **Reserved concurrency** caps simultaneous invocations. Provisioned concurrency reduces cold starts and does not cap anything. RDS Proxy is another valid fix. [Lambda](../topic-guides/lambda.md#reserved-and-provisioned-concurrency)
4. **S3 Versioning and Object Lock in compliance mode.** Governance mode can be bypassed, and lifecycle expiration does not prevent deletion. [S3](../topic-guides/s3.md#deletion-object-lock-and-legal-holds)
5. **Apache Iceberg with `MERGE` and time travel.** A short snapshot retention for `VACUUM` deletes the snapshots auditors need. [Iceberg](../topic-guides/iceberg.md#iceberg-maintenance-and-amazon-s3-tables)
6. **A hot partition key.** One key exceeds the per-partition limit of 1,000 write units per second. Spread it with write sharding or a better key. More table capacity does not help. [Databases](../topic-guides/databases.md#throttling-and-hot-keys)
7. **Source arrival in S3, job input and output row counts, the curated partition files, catalog registration, then dashboard refresh.** Then add a freshness alarm. [Monitoring](../topic-guides/monitoring.md#correlation-ids-freshness-and-alarms)
8. **The per-query data usage control** cancels the query. The workgroup-wide control only sends an alert. [Athena](../topic-guides/athena.md#workgroups-and-cost-control)
9. **Data skew.** The hot key lives in one partition processed by one task, so more nodes leave that task just as slow. Use AQE skew joins, salting, or a broadcast join if one side is small. [EMR](../topic-guides/emr.md#diagnose-and-mitigate-partition-and-join-skew)
10. **Re-encrypt with a customer managed key**, allow account B's role in its key policy, and add `kms:Decrypt` to the role's IAM policy. The `aws/s3` key policy cannot be edited. [Security](../topic-guides/security.md#cross-account-encrypted-object-access)
11. **A Lake Formation cell-level data filter, and removal of direct S3 access.** Without the second step, contractors read the files and skip the filter. [Governance](../topic-guides/governance.md#lake-formation-grants-across-query-engines)
12. **Nothing about the read.** Default CloudTrail records management events only. Object reads need CloudTrail data events enabled beforehand. [Privacy and audit](../topic-guides/privacy-and-audit.md#audit-evidence-scope-and-retention)

</details>

Score yourself by domain. Two or more misses in a domain means start that domain's week with the guides linked above. Then continue with the [four-week plan](../learning-paths/4-week-plan.md).
