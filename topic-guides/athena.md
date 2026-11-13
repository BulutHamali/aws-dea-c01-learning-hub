# Amazon Athena queries, cost control, and federation

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Amazon Athena runs SQL directly over files in S3 with no servers to manage. It reads table definitions from the Glue Data Catalog and charges for the bytes each query scans. That one fact drives most Athena answers: anything that reduces bytes scanned makes queries both faster and cheaper.

## Run a query and inspect its output

1. Choose a **workgroup**. It sets the S3 location for results, encryption, and limits.
2. Run the query. Athena writes the result file and a metadata file to the results location.
3. Read the query statistics: data scanned, run time, and queue time. Use `EXPLAIN` to confirm which partitions are read.

```sql
EXPLAIN SELECT instrument, SUM(reads)
FROM curated.runs
WHERE run_date = '2026-01-01'
GROUP BY instrument;
```

If the plan lists every partition, the filter is not pruning. Check that the filter uses the partition column directly, without wrapping it in a function.

## Reduce bytes scanned

| Technique | Effect |
|---|---|
| Convert CSV or JSON to Parquet or ORC | Reads only the needed columns, compressed |
| Partition on filtered columns | Skips whole folders |
| Select named columns, not `SELECT *` | Fewer columns read from columnar files |
| Compact small files | Less per-file overhead |
| Partition projection | Faster planning with no partition lookups in the catalog |
| Query result reuse | Returns a recent cached result for an identical query instead of scanning again |

See [file layout](file-layout.md) and [catalog](catalog.md).

## CTAS, INSERT INTO, and views

- `CREATE TABLE AS SELECT` (CTAS) writes query results as a new table, in any supported format and partitioning. It is a quick way to convert raw CSV to curated Parquet.
- `INSERT INTO` appends results to an existing table.
- Both can write at most 100 partitions per query. Split larger backfills into several statements with non-overlapping filters.
- A view saves a query definition and scans the underlying data every time it runs.

## Workgroups and cost control

| Control | Behavior |
|---|---|
| Per-query data usage limit | Athena cancels any query that scans more than the threshold |
| Workgroup data usage alert | Sends an Amazon SNS alarm when the workgroup's total crosses a threshold. It does not cancel queries |
| Enforce workgroup settings | Clients cannot override the result location, encryption, or expected bucket owner |
| Separate workgroups per team | Separate cost tracking, limits, and IAM permissions |

Protect the results bucket. Results can contain the same sensitive data as the source.

## Federated queries and Spark notebooks

**Athena federated query** reads sources outside S3, such as DynamoDB, RDS, CloudWatch Logs, or other databases, through data source connectors that run as Lambda functions. Use it for occasional joins across sources. For heavy repeated queries, copy the data into S3 instead.

**Athena for Apache Spark** runs PySpark in notebooks with fast startup, for exploration that needs more than SQL. See [analysis and data prep](analysis-and-data-prep.md).

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| CTAS and INSERT INTO partitions | 100 per query | Larger writes fail with `HIVE_TOO_MANY_OPEN_PARTITIONS` | [CTAS and INSERT INTO](https://docs.aws.amazon.com/athena/latest/ug/ctas-insert-into.html) |
| Query string length | 262,144 bytes, not adjustable | Very long generated SQL must be split or replaced with a table | [Athena quotas](https://docs.aws.amazon.com/athena/latest/ug/service-limits.html) |
| DML query timeout | Adjustable, up to 240 minutes | Long queries may need a quota increase or a different engine | [Athena quotas](https://docs.aws.amazon.com/athena/latest/ug/service-limits.html) |
| Workgroup threshold types | Per-query limit cancels. Workgroup limit alerts | Only the per-query limit stops a runaway query | [Workgroup cost controls](https://docs.aws.amazon.com/athena/latest/ug/workgroups-manage-queries-control-costs.html) |

## Common mistake

Raising quotas when queries get slower. Check `EXPLAIN` and bytes scanned first. A filter on a non-partition column, or thousands of small files, scans far more than needed.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Athena vs. Redshift Spectrum | SQL over S3 with no warehouse vs. Redshift SQL that joins S3 data with warehouse tables |
| Per-query limit vs. workgroup alert | Stop a query vs. notify about total use |
| CTAS vs. view | Writes new files vs. stores a query |
| Federated query vs. copying data to S3 | Occasional access to live sources vs. repeated heavy analysis |

**Exam cues:** "Serverless SQL on S3" → Athena. "Limit cost per team" → workgroups with data usage controls. "Query DynamoDB and S3 together in SQL" → federated query.

## Try it

A weekly report reads run ID, date, and reads from a raw CSV dataset and scans everything. One analyst's ad hoc query scanned 40 TB by mistake.

<details>
<summary>Show the reasoning</summary>

Create a curated Parquet table partitioned by date with CTAS, in batches of up to 100 partitions. Select only the needed columns. Put analysts in a workgroup with a per-query data usage limit. Compare bytes scanned before and after.

</details>

## AWS documentation

- [What is Amazon Athena?](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)
- [CTAS](https://docs.aws.amazon.com/athena/latest/ug/ctas.html)
- [Workgroup cost controls](https://docs.aws.amazon.com/athena/latest/ug/workgroups-manage-queries-control-costs.html)
- [Federated query](https://docs.aws.amazon.com/athena/latest/ug/connect-to-a-data-source.html)
- [Query result reuse](https://docs.aws.amazon.com/athena/latest/ug/reusing-query-results.html)

*Last verified against AWS documentation: November 2026.*
