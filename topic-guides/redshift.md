# Redshift loads, Spectrum, and streaming ingestion

[Topic index](README.md) · [Home](../README.md)

## The idea

Think of the warehouse as a working stockroom. COPY brings boxes in from S3. Spectrum lets you inspect a box while it stays in external storage. UNLOAD sends query results back to S3.

Redshift is an analytical warehouse. Decide whether data should live in a warehouse table, remain in S3, or arrive through a live stream.

## How to decide

| Concept | When it matters |
|---|---|
| **COPY from S3** | Bulk load files into a Redshift table. For incremental updates, load to a staging table, check key uniqueness and quality, then merge. |
| **Redshift Spectrum** | Query external data in S3 from Redshift and join with local warehouse data where appropriate. |
| **Streaming ingestion** | Ingest supported Kinesis or MSK streams into a materialized view for low-latency access. Firehose delivery to Redshift uses S3 staging and COPY. |
| **Federated queries** | Query supported operational databases such as RDS or Aurora from Redshift. Consider source load and latency. |
| **UNLOAD** | Write query results to S3. Choose the output layout and file format for downstream readers. |
| **Data sharing** | Share live Redshift data with authorized consumers using a datashare. Redshift Serverless or provisioned deployments can participate where supported. |

## Follow a warehouse load

1. Write the batch to a known S3 location. Use an appropriate IAM role for Redshift to read the files.
2. COPY the batch into a staging table. Inspect load errors and reject or correct bad input.
3. Check row counts, deduplicate by business key, and MERGE into the target in a controlled transaction.
4. Verify target counts or keys and record the completed batch. Rerun safely from staging if publication fails.

For repeated analytical joins, inspect distribution and skew before adding capacity. For an infrequent workload with variable demand, compare Redshift Serverless with provisioned options using actual performance and cost requirements.

## Common mistake

Use SYS_LOAD_ERROR_DETAIL to inspect COPY failures and SYS_QUERY_HISTORY for query status and timing. Check key uniqueness before merging a batch with multiple records for the same target row.

## Try it

Your warehouse needs fresh device readings directly from an existing Kinesis stream, with no S3 staging step.

<details>
<summary>Show the reasoning</summary>

Use Redshift streaming ingestion. For a nightly backfill from archived S3 files, use COPY and a staging table.

</details>

## AWS documentation

- [AWS documentation · r_COPY](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html)
- [AWS documentation · c spectrum overview](https://docs.aws.amazon.com/redshift/latest/dg/c-spectrum-overview.html)
- [AWS documentation · materialized view streaming ingestion](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion.html)
- [AWS documentation · datashare overview](https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html)
