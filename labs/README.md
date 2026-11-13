# Pipeline workshops

[Home](../README.md) · [Topic index](../topic-guides/README.md)

Use the sample inputs to work through the design on paper. Workshop 2 also includes SQL you can run locally with SQLite.

## Workshop 1 — Design a sequencing metrics lake

A fictional sequencing facility lands a daily CSV. Each row is supposed to have a unique run ID per day and a nonnegative read count.

| run_date | run_id | instrument | reads |
|---|---|---|---:|
| 2026-01-01 | R01 | inst-a | 200 |
| 2026-01-01 | R02 | inst-b | -3 |
| 2026-01-02 | R03 | inst-a | 500 |

1. Sketch S3 locations for original files, curated data, and invalid rows.
2. Choose the component that validates rows and writes Parquet, and identify how Athena discovers the schema.
3. Design a query that sums reads per instrument for January 1. Explain which files and columns the engine can skip.
4. Specify what happens if January 1 is processed twice and how you alert when January 2 has no curated output.

<details>
<summary>Expected result</summary>

Keep the incoming file in raw storage. Glue ETL sends R02 to quarantine and writes valid rows to curated Parquet under a date-based partition scheme. Catalog the curated table. Filtering the January 1 partition and grouping by instrument yields inst-a with 200 reads. For a rerun, use a controlled partition replacement or a table format that supports atomic changes. Track successful publication and alert on stale data.

</details>

## Workshop 2 — Recover a partially loaded batch

The target already contains the first update from a failed attempt. Run the setup and the UPSERT block, then run the UPSERT block again. SQLite’s conflict clause models the key-based update. In Redshift, use a staging table with MERGE.

```sql
CREATE TABLE target (id TEXT PRIMARY KEY, reads INTEGER);
CREATE TABLE stage (id TEXT, reads INTEGER, source_seq INTEGER);
INSERT INTO target VALUES ('R01', 180), ('R03', 500);
INSERT INTO stage VALUES ('R01', 180, 1), ('R01', 200, 2), ('R02', 300, 3);
```

```sql
-- UPSERT block
WITH ranked AS (
    SELECT id, reads,
           ROW_NUMBER() OVER (PARTITION BY id ORDER BY source_seq DESC) AS rn
    FROM stage
)
INSERT INTO target (id, reads)
SELECT id, reads FROM ranked WHERE rn = 1
ON CONFLICT(id) DO UPDATE SET reads = excluded.reads;

SELECT id, reads FROM target ORDER BY id;
```

<details>
<summary>Expected result</summary>

Both executions return R01 with 200, R02 with 300, and R03 with 500. The ranking ensures one input row per target key. The upsert adds missing IDs and updates existing IDs. If older batches can arrive after newer batches, store a source version on the target and condition updates on it.

</details>

## Workshop 3 — Estimate what a query can skip

A year of daily telemetry is stored in S3. For this exercise, assume 360 days, one equal-sized file per day, and 12 equally sized columns. A report reads two columns and asks for the most recent 30 days. Assume an engine can prune the unused dates and columns and ignore compression and metadata overhead.

1. Estimate how much data the report reads from unpartitioned CSV.
2. Estimate the proportion read with date partitions and CSV files.
3. Estimate the proportion read after converting the partitioned table to Parquet.
4. Explain why the same factors would be harder to estimate for production data.

<details>
<summary>Expected result</summary>

The simplified baseline reads 100% of the data. Date pruning reduces the scan to 30/360, about 8.3%. Column pruning reduces that to 30/360 × 2/12, about 1.4% of the original logical data in this model. Actual scanned bytes depend on compression, column widths, file layout, query predicates, and engine behavior. Use Athena query statistics to measure the difference on equivalent queries.

</details>
