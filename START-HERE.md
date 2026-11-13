# Start here

[Home](README.md) · [Topic index](topic-guides/README.md) · [Diagnostic](practice/diagnostic.md)

A data pipeline moves data from where it is produced to where people can use it. Picture a lab that receives one CSV per sequencing run. The lab stores the original files, checks that each sample has a run ID, and publishes a cleaned table that analysts can query.

```mermaid
flowchart TD
    A["CSV files arrive in S3"] --> B["Glue validates and transforms rows"]
    B --> C["Valid rows go to curated Parquet"]
    B --> D["Invalid rows go to quarantine"]
    C --> E["Athena queries through the Glue Data Catalog"]
```

| Term | In the lab example |
|---|---|
| Batch | Process a group of files together, such as all runs from yesterday |
| Stream | Process a continuing flow of events as they arrive |
| ETL | Extract data, transform it in a processing engine, then load the result |
| ELT | Load data first, then transform it in the destination |
| Data lake | Store source and curated datasets in an object store such as S3 |
| Warehouse | Store and query structured analytical tables in a system such as Redshift |
| Catalog | Describe where the data lives, what columns it has, and how to read it |
| Partition | Group rows by a value such as run date so a query can skip unrelated files |
| CDC | Capture inserts, updates, and deletes from a source database over time |
| Idempotency | Rerun the same work and reach the same final result |
| Backfill | Reprocess a past period to fill a gap or apply a correction |
| Schema drift | A source changes its fields or types, such as an integer arriving as text |

Know basic SQL filters, joins, aggregation, and window functions. If AWS is new to you, learn what an S3 bucket, IAM role, and CloudWatch log group do before starting the first week.

**Recall check.** If the curated Parquet objects exist in S3 but Athena has no table definition, which layer is missing? The metadata layer. The data and its catalog entry are separate.

Next → [Four-week plan](learning-paths/4-week-plan.md)
