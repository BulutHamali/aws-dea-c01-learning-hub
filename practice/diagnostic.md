# DEA-C01 diagnostic

[Home](../README.md) · [Progress tracker](../CHECKLIST.md)

Take ten minutes. For each prompt, write the service or action and one reason. Mark low-confidence answers even if they turn out to be correct.

1. Two applications must independently consume the same AWS-native event stream. One needs to replay last night’s events. Which ingestion layer fits?
2. A batch job reran after a bookmark reset. Analysts now see duplicate results. What should you check first?
3. Athena queries usually select two columns from raw CSV and filter on collection day. Which two layout changes would you test?
4. An Athena-only table writes dates to a consistent S3 prefix and the catalog partitions are expensive to maintain. What could remove per-date registration?
5. A Redshift COPY command failed on a malformed input field. Where do you find the file and column involved?
6. A Glue job reports success, but the latest day in the dashboard is missing. What evidence do you gather first?
7. A role can list a bucket, but GetObject on an SSE-KMS object reports a KMS denial. Which access layer do you investigate?
8. Analysts must query a curated table but can see only approved columns. Which service can enforce the table access, and which alternate path should you check?

<details>
<summary>Answers and review links</summary>

1. Kinesis Data Streams with a retention window covering last night. Firehose can be a delivery consumer. [Streaming](../topic-guides/streaming.md)
2. Inspect existing output. Resetting an input bookmark does not clear the sink. [Glue](../topic-guides/glue.md)
3. Convert to a columnar format such as Parquet and partition by a commonly filtered date at an appropriate granularity. Compare bytes scanned. [File layout](../topic-guides/file-layout.md)
4. Configure partition projection with a matching date range and S3 location pattern. Check whether sparse partitions make it inefficient. [Catalog](../topic-guides/catalog.md)
5. Look at SYS_LOAD_ERROR_DETAIL for the affected COPY query ID. [Redshift](../topic-guides/redshift.md)
6. Trace the missing partition from source arrival through job input/output counts, published files, catalog, and dashboard refresh. [Monitoring](../topic-guides/monitoring.md)
7. Check applicable decrypt authorization for the executing role and the relevant key policy. [Security](../topic-guides/security.md)
8. Use Lake Formation with an integrated query engine and review direct S3 access that could bypass the table controls. [Governance](../topic-guides/governance.md)

</details>
