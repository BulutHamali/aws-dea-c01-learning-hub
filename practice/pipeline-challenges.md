# Pipeline challenges

[Home](../README.md) · [Decision guides](../decision-guides/README.md)

For each original scenario, identify the deciding requirement, sketch the data path, and choose one observable success signal.

## 1. A replayable event feed

A sensor emits readings continuously. One consumer detects anomalies and may replay readings after an outage. A second delivers a long-term copy to S3. The team wants managed delivery and can tolerate buffering in the archive path.

<details>
<summary>Show reasoning</summary>

Use Kinesis Data Streams with retention sized for recovery. Attach the anomaly consumer and a Firehose delivery stream reading Kinesis. Watch consumer lag and S3 delivery freshness independently. Firehose alone addresses archival delivery, while the anomaly consumer needs independent replay.

</details>

## 2. A slow scan over quality metrics

Analysts query three fields from raw CSV files in S3 and nearly always filter by run date. Data arrives daily. The team can maintain one extra table.

<details>
<summary>Show reasoning</summary>

Use Glue ETL or Athena CTAS for conversion to a curated Parquet dataset. Choose date granularity based on filter patterns and file sizes. Use Athena to compare bytes scanned and validate that the result matches the raw query. JSON preserves flexible structure, but it offers little benefit for these repeated narrow scans.

</details>

## 3. A warehouse batch with corrections

Every night a supplier sends updated rows for existing products alongside new products. A previous import job crashed halfway through a retry and inserted duplicates.

<details>
<summary>Show reasoning</summary>

COPY files into a Redshift staging table. Validate expected fields and retain one input version per product ID using a deterministic ordering. MERGE by product ID and record the completed batch. Replaying the same normalized batch should leave the same product rows. Appending directly with COPY would leave corrections and prior values together.

</details>

## 4. A lab partner’s restricted dataset

An external research group may query anonymized measurements in Athena. Internal staff need full columns. Existing analyst roles have access to raw S3 paths.

<details>
<summary>Show reasoning</summary>

Apply Lake Formation permissions to the governed dataset and narrow direct raw-object access. Test as both roles. Include permissions for the Athena results path and any applicable KMS keys. Encryption alone does not distinguish which columns each authorized group can query.

</details>

## 5. A stalled streaming job

A Glue streaming job reads from a Kinesis stream. Downstream data is ten minutes behind. The job recently restarted and the team proposes deleting its checkpoint.

<details>
<summary>Show reasoning</summary>

Compare consumer lag, input rate, processing time per micro-batch, and sink writes. Inspect logs for throttling, data skew, or sink failures. Preserve the checkpoint until you have a recovery plan. Replaying from a changed start point can duplicate or skip records depending on configuration and retention.

</details>

## 6. Database changes with an object archive

A supported transactional database must keep serving users while the analytics team receives an initial snapshot and ongoing changes. Reporting can tolerate a modest lag.

<details>
<summary>Show reasoning</summary>

Consider DMS full load plus CDC to a supported target. Confirm source logging and retention, monitor latency, and reconcile source and target. Schedule file movement with DataSync only if your source is already materialized as files. The task here begins with database change capture.

</details>
