# Amazon Redshift loads, table design, access paths, and locks

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Amazon Redshift is a columnar analytical warehouse. Picture a stockroom. `COPY` brings boxes in from Amazon S3. Redshift Spectrum lets you inspect boxes that stay outside. `UNLOAD` ships query results back to S3. Table design decides where each box sits so joins don't have to carry boxes between rooms.

## COPY, staging, and UNLOAD

Use one `COPY` command that points at many files. Redshift splits the work across slices, the parallel units inside each node. Many separate `COPY` commands into one table load serially and run slower.

1. Land the batch in S3. Give Redshift an IAM role that can read the prefix and decrypt any KMS key.
2. `COPY` into a staging table. Use a manifest when you must load an exact list of files and fail if one is missing.
3. Check row counts and duplicates by business key in staging.
4. `MERGE` into the target inside one transaction, then record the batch as complete.
5. If a run fails after step 2, truncate staging and rerun. The target stays untouched until the merge commits.

```sql
COPY stage_runs
FROM 's3://lab-lake/curated/runs/run_date=2026-01-01/'
IAM_ROLE 'arn:aws:iam::111122223333:role/RedshiftLoad'
FORMAT AS PARQUET;

MERGE INTO runs USING stage_runs s ON runs.run_id = s.run_id
WHEN MATCHED THEN UPDATE SET reads = s.reads
WHEN NOT MATCHED THEN INSERT VALUES (s.run_id, s.run_date, s.instrument, s.reads);
```

`UNLOAD` writes query results to S3 in parallel. Choose `FORMAT AS PARQUET` and `PARTITION BY` when other engines will read the output.

When `COPY` fails, query `SYS_LOAD_ERROR_DETAIL` for the file, line, column, and reason. Query `SYS_QUERY_HISTORY` for status and timing of any query.

## Spectrum, federation, and materialized views

| Need | Feature | Notes |
|---|---|---|
| Join warehouse tables with large S3 data that should stay in S3 | Redshift Spectrum external tables | Uses the Glue Data Catalog. Partition and use columnar formats to limit scanned bytes |
| Query live rows in an operational database | Federated query | RDS and Aurora, PostgreSQL and MySQL editions. Adds load to the source |
| Make Kinesis or MSK records queryable with low latency, no S3 staging | Streaming ingestion into a materialized view | Refresh pulls new records from the stream |
| Speed up a repeated dashboard aggregation | Materialized view | Stores precomputed results. `AUTO REFRESH YES` refreshes when resources allow. Redshift can rewrite queries to use it automatically |
| Give another account or workgroup live read access without copying | Data sharing | Producers grant a datashare. Consumers query current data |

Firehose delivery to Redshift writes to S3 first and then runs `COPY`. Streaming ingestion skips that intermediate staging step.

## Table design: distribution and sort keys

**Distribution** decides which slice stores each row. Moving rows between slices during a join is expensive.

| Style | Use when |
|---|---|
| `AUTO` (default) | You have no strong reason to choose. Redshift starts small tables as `ALL` and can switch to `KEY` or `EVEN` as they grow |
| `KEY` | Two large tables are joined often on the same column. Distribute both on it so matching rows sit together |
| `ALL` | A slow-changing table must be joined from every slice. Storage multiplies by the number of nodes |
| `EVEN` | The table rarely joins, or no column distributes evenly |

**Skew** happens when a distribution key has a few very common values. One slice then does most of the work. Check row counts per slice before adding nodes.

**Sort keys** store rows in order so range filters, such as a date range, skip blocks. Prefer `SORTKEY AUTO` or a compound sort key that starts with the most common filter column. Run `ANALYZE` after large loads and let automatic vacuum reclaim space, or run `VACUUM` after heavy deletes.

## Redshift and RDS transactions, locks, and contention

A **lock** stops two sessions from changing the same thing in conflicting ways.

- New Redshift provisioned clusters and serverless workgroups default to **snapshot isolation**. Two transactions that update different rows can both commit.
- With **serializable isolation**, concurrent transactions that conflict fail with error `1023`. Retry the losing transaction or serialize writers.
- `LOCK table_name` inside a transaction takes an ACCESS EXCLUSIVE lock. Other sessions' reads and writes wait until the transaction ends. Use it to force two loaders into a single file line.
- `DROP TABLE` and `TRUNCATE` take exclusive locks and block reads.
- To find a blocker, query `STV_LOCKS` and `SVV_TRANSACTIONS`. End a stuck session with `PG_TERMINATE_BACKEND(pid)` only after confirming it is safe, because its open transaction rolls back.

In Amazon RDS and Aurora, the database engine handles row locks. `SELECT ... FOR UPDATE` locks the rows a job is about to change. Long transactions hold locks longer and raise deadlock risk. Keep load transactions short and access tables in the same order in every job.

## Serverless and provisioned cost and scaling

| Choose | When |
|---|---|
| Redshift Serverless | Spiky or intermittent use, and you want no cluster management. You set base and max capacity in Redshift Processing Units (RPUs) and pay for compute while queries run |
| Provisioned RA3 cluster | Steady, predictable load where reserved pricing and node-level control pay off. Concurrency scaling adds capacity for bursts of queries |

Workload management (WLM) assigns queries to queues so a heavy ETL job cannot starve dashboard queries. Automatic WLM is the default.

## Database roles, grants, and schema access

Grant SQL privileges to roles, then roles to users. Grant `USAGE` on a schema plus `SELECT` on its tables. Use role-based access control for groups of analysts, row-level security policies to filter rows, and [dynamic data masking](privacy-and-audit.md#hide-values-at-query-time) to hide column values at query time.

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| COPY input files that cannot be split (for example gzip CSV) | Split into files close in size, 1 MB to 1 GB after compression, in a multiple of the slice count | Keeps every slice busy during the load | [Loading from multiple files](https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-use-multiple-files.html) |
| Automatic splitting | Uncompressed CSV and columnar files of 128 MB or larger are split automatically | Small Parquet files are not split, so file count matters | [Loading from multiple files](https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-use-multiple-files.html) |
| Default isolation for new clusters and workgroups | Snapshot isolation | Conflict behavior differs from older serializable clusters | [Isolation levels](https://docs.aws.amazon.com/redshift/latest/dg/c_serial_isolation.html) |
| Serverless base capacity | 128 RPUs by default. Adjustable from 4 RPUs up to 512 (1,024 in some Regions) | Lower base for small dev workloads, raise for heavy concurrency | [Serverless capacity](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-capacity.html) |
| Federated query sources | RDS and Aurora for PostgreSQL and MySQL | Any other source needs a different access path | [Federated queries](https://docs.aws.amazon.com/redshift/latest/dg/federated-overview.html) |

## Common mistake

Adding nodes to fix a slow join. If one slice holds most rows because of a skewed distribution key, more nodes leave that slice just as slow. Fix the key first.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Spectrum vs. federated query vs. Athena | S3 data from Redshift SQL, live RDS or Aurora rows from Redshift SQL, or S3 data without a warehouse |
| Streaming ingestion vs. Firehose to Redshift | No S3 staging and lowest latency, or managed delivery through S3 and COPY |
| Materialized view vs. view | Stored, refreshed results vs. a saved query that runs every time |
| Data sharing vs. UNLOAD and COPY | Live read access with no copy vs. a separate copy |
| `KEY` vs. `ALL` distribution | Two large joined tables vs. a small, slow-changing table needed everywhere |

**Exam cues:** "Without moving the data" from Redshift → Spectrum or federated query. "Error 1023" → serializable conflict. "Another team's account, live data" → data sharing. "Dashboards repeat the same aggregation" → materialized view.

## Try it

Two nightly loaders write to the same `runs` table. Sometimes one fails with a serializable isolation error. A dashboard also runs the same daily aggregation hundreds of times.

<details>
<summary>Show the reasoning</summary>

Serialize the loaders: take `LOCK runs` at the start of each load transaction, or move both into one orchestrated step with retry. Create a materialized view for the daily aggregation with auto refresh. Verify that the loaders stop failing and the dashboard query plan reads the view.

</details>

## AWS documentation

- [COPY command](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html)
- [MERGE](https://docs.aws.amazon.com/redshift/latest/dg/r_MERGE.html)
- [Choosing a distribution style](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html)
- [LOCK](https://docs.aws.amazon.com/redshift/latest/dg/r_LOCK.html)
- [Materialized views](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-overview.html)
- [Streaming ingestion](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-streaming-ingestion.html)
- [Data sharing](https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html)

*Last verified against AWS documentation: November 2026.*
