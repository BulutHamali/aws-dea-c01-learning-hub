# File formats, partitions, compaction, and data shape

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Picture a filing cabinet with one drawer per day. A date filter opens only the drawers it needs. That is **partition pruning**. Inside each drawer, a columnar file lets you pull out the `reads` column without reading every description field. That is **column pruning**. The bytes a query reads depend on the file format, the partition filter, and the size and number of files.

## Volume, velocity, and variety

Engineers describe data with three words. They change which tools fit.

| Term | Plain meaning | Lab example | Design effect |
|---|---|---|---|
| Volume | How much data | 2 TB of reads per year | Columnar formats, partitioning, and distributed engines |
| Velocity | How fast it arrives | 2,400 instrument events per second | Streams and micro-batches instead of nightly files |
| Variety | How varied its shape is | CSV run sheets, JSON events, PDF protocols | Structured data fits tables. Semi-structured JSON needs schema handling. Unstructured text needs extraction or an LLM |

## From raw CSV to partitioned Parquet

| Format | Use it for | Weakness |
|---|---|---|
| CSV | Landing data from partners and instruments | Every query reads every column. No types |
| JSON | Nested, flexible events | Large and slow to scan. Schema can drift silently |
| Apache Parquet | Analytics in Athena, Redshift Spectrum, Spark | Columnar, typed, compressed, with min and max statistics per row group |
| Apache ORC | Analytics in Hive-oriented stacks | Similar strengths to Parquet |
| Apache Avro | Row-based records with an embedded schema, common in streaming | Not columnar, so analytical scans read whole rows |

To convert, use a Glue ETL job, an Athena `CREATE TABLE AS SELECT` (CTAS) query, or Firehose record format conversion for streams. Athena CTAS and `INSERT INTO` can write at most 100 partitions per query. For more, run several `INSERT INTO` statements with non-overlapping filters.

## File layout, pruning, compression, and index trade-offs

**Partitioning** splits files into folders by a column such as `run_date=2026-01-01/`. Partition by what queries filter on, at the granularity they filter at. If queries look at days, don't partition by hour. A partition key with millions of values, such as sample ID, creates huge numbers of tiny files.

**Bucketing** groups rows with the same value of a high-cardinality column into the same file. It helps queries that look up single values, such as one sample ID.

**Sorting** inside files lets engines skip row groups using min and max statistics. Sorting by timestamp can replace an hourly partition.

**Compression** reduces bytes scanned, and Athena charges for bytes scanned before decompression. Gzip text files cannot be split, so one large gzip file is read by one worker. Parquet compresses each column inside a splittable file.

**Small files** hurt every engine. Each file adds open and list overhead. Compact many small files into fewer large ones, with a scheduled Glue job, Athena CTAS, or Iceberg `OPTIMIZE`.

## Worked estimate

A year of telemetry has 360 daily files of equal size with 12 equal columns. A report reads 2 columns for the last 30 days.

- Unpartitioned CSV: reads 100%.
- Partitioned CSV: 30/360 ≈ 8.3%.
- Partitioned Parquet: 30/360 × 2/12 ≈ 1.4%.

Real numbers differ because of compression and column widths. Measure with Athena query statistics. See [Workshop 3](../labs/README.md#workshop-3-estimate-what-a-query-can-skip).

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Athena CTAS and INSERT INTO partition limit | 100 partitions per query | Larger backfills need several statements | [CTAS and INSERT INTO](https://docs.aws.amazon.com/athena/latest/ug/ctas-insert-into.html) |
| Files per partition | More than 1,000 files in one partition needs several S3 list calls and slows planning | Compact before adding compute | [Athena data optimization](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html) |
| Parquet row group default | 128 MB (ORC stripe 64 MB). AWS advises against going smaller | Tiny row groups lose the benefit of columnar statistics | [Athena data optimization](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html) |
| S3 request rate | 5,500 GET requests per second per partitioned prefix | Very hot prefixes can throttle large parallel scans | [Athena data optimization](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html) |
| Partition key type for Glue filter pushdown | `STRING` | Other types can stop Athena from pruning in the catalog | [Athena data optimization](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html) |

## Common mistake

Partitioning by a unique ID. Each partition holds a few rows, the file count explodes, and every query pays planning overhead. Keep high-cardinality IDs as columns, or bucket them.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Partitioning vs. bucketing | Low-cardinality filter column vs. high-cardinality single-value lookups |
| Parquet vs. Avro | Columnar analytics vs. row records with schema in streams |
| Partition pruning vs. column pruning | Skips files vs. skips columns inside files |
| Gzip CSV vs. Parquet with compression | Not splittable vs. splittable and columnar |

**Exam cues:** "Reduce data scanned" → columnar format plus partitions on filtered columns. "Many small files" → compaction. "Queries filter on a single customer ID" → bucketing or sorting, not partitioning.

## Try it

Analysts query three columns from a large dataset and always filter by collection month. A streaming job writes thousands of 50 KB files per day.

<details>
<summary>Show the reasoning</summary>

Write Parquet partitioned by month. Add a compaction step that rewrites each day's small files into a few large files. Keep sample IDs as columns. Compare bytes scanned before and after with the same query.

</details>

## AWS documentation

- [Athena data optimization techniques](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html)
- [Athena CTAS](https://docs.aws.amazon.com/athena/latest/ug/ctas.html)
- [Firehose record format conversion](https://docs.aws.amazon.com/firehose/latest/dev/record-format-conversion.html)

*Last verified against AWS documentation: November 2026.*
