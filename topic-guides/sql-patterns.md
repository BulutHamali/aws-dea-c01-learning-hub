# SQL for validation, deduplication, analysis, and loading

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Start every query by stating the grain: what one row represents. If one row is one run per day, then every join and aggregation must either keep that grain or change it on purpose. Most wrong numbers come from a join that silently multiplied rows.

All examples below use this table and run in SQLite, Athena, and Redshift with at most small syntax changes.

```sql
CREATE TABLE runs (run_date TEXT, run_id TEXT, instrument TEXT, reads INTEGER);
INSERT INTO runs VALUES
  ('2026-01-01','R01','inst-a',200), ('2026-01-01','R02','inst-b',150),
  ('2026-01-02','R03','inst-a',500), ('2026-01-02','R04','inst-b',100),
  ('2026-01-03','R05','inst-a',300), ('2026-01-03','R05','inst-a',300);
```

## Worked aggregation, window, and pivot queries

**Aggregation** collapses rows into one row per group.

```sql
SELECT instrument, SUM(reads) AS total_reads
FROM runs GROUP BY instrument;
```

**Rolling average** keeps every detail row and adds a calculation over neighbouring rows. That is what a window function does.

```sql
SELECT run_date, instrument, reads,
       AVG(reads) OVER (PARTITION BY instrument ORDER BY run_date
                        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_3_rows
FROM runs;
```

`ROWS BETWEEN 2 PRECEDING` counts rows, not days. If dates can be missing, build a complete date list first or use a date-based range where the engine supports it.

**Pivot** turns category values into columns. Conditional aggregation works in every engine.

```sql
SELECT run_date,
       SUM(CASE WHEN instrument = 'inst-a' THEN reads ELSE 0 END) AS inst_a,
       SUM(CASE WHEN instrument = 'inst-b' THEN reads ELSE 0 END) AS inst_b
FROM runs GROUP BY run_date ORDER BY run_date;
```

## Find gaps and duplicates

```sql
-- Duplicates at the stated grain: one row per run_id per day
SELECT run_date, run_id, COUNT(*) AS n
FROM runs GROUP BY run_date, run_id HAVING COUNT(*) > 1;

-- Compare source and target counts per day
SELECT s.run_date, s.n AS source_rows, COALESCE(t.n, 0) AS target_rows
FROM (SELECT run_date, COUNT(*) n FROM runs GROUP BY run_date) s
LEFT JOIN (SELECT run_date, COUNT(*) n FROM runs GROUP BY run_date) t
  ON s.run_date = t.run_date
WHERE s.n <> COALESCE(t.n, 0);
```

The first query returns `2026-01-03, R05, 2`. In a real pipeline the second query compares a source table with a target table. Here both sides read `runs`, so it returns nothing.

## Deduplicate and merge

Keep the latest version of each key with `ROW_NUMBER`. Add a tie-breaker, such as a source sequence number, so two rows with the same timestamp still rank deterministically.

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY run_date, run_id
                               ORDER BY reads DESC) AS rn
  FROM runs
)
SELECT run_date, run_id, instrument, reads FROM ranked WHERE rn = 1;
```

Then apply the clean batch to the target with `MERGE` in Redshift or an Iceberg table, or an upsert in other engines. See [Workshop 2](../labs/README.md#workshop-2-recover-a-partially-loaded-batch) and [Redshift loads](redshift.md#copy-staging-and-unload).

## Athena and Redshift queries and views

| Object | What it stores | Use it when |
|---|---|---|
| View | Only the query text. Runs against base data each time | You want one shared definition and always-current results |
| Materialized view (Redshift) | Stored results, refreshed on demand or automatically | The same expensive aggregation runs often |
| CTAS table (Athena) | New files written from a query | You want a converted or pre-aggregated copy in S3 |

```sql
CREATE VIEW daily_reads AS
SELECT run_date, instrument, SUM(reads) AS reads
FROM runs GROUP BY run_date, instrument;
```

## Pattern matching

Use `LIKE 'R0%'` for simple wildcards. Use the engine's regular expression function for exact patterns: `regexp_like(run_id, '^R[0-9]{2}$')` in Athena, `run_id ~ '^R[0-9]{2}$'` in Redshift.

## Common mistake

A one-to-many join multiplies rows. Joining runs to a samples table with five samples per run makes `SUM(reads)` five times too large. Aggregate first, then join.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| `GROUP BY` vs. window function | Collapse rows vs. keep rows and add a calculation |
| `ROW_NUMBER` vs. `RANK` | Exactly one row per key vs. ties share a rank |
| `ROWS` vs. `RANGE` frame | Count physical rows vs. compare ordering values |
| View vs. materialized view | Always current but recomputed vs. stored and refreshed |

**Exam cues:** "Keep detail rows and add a moving average" → window function. "Keep the latest record per key" → `ROW_NUMBER` with a tie-breaker. "Turn categories into columns" → pivot.

## Try it

A file contains several updates per sample, including two with the same event timestamp. The report also needs a seven-day moving average of reads per instrument.

<details>
<summary>Show the reasoning</summary>

Rank updates by event time and then a source sequence number, keep rank 1 per sample, and merge that into the target. For the moving average, use `AVG(reads) OVER (PARTITION BY instrument ORDER BY run_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` over one row per instrument per day, with missing days filled.

</details>

## AWS documentation

- [Redshift window functions](https://docs.aws.amazon.com/redshift/latest/dg/c_Window_functions.html)
- [Redshift ROW_NUMBER](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_ROW_NUMBER.html)
- [Redshift MERGE](https://docs.aws.amazon.com/redshift/latest/dg/r_MERGE.html)
- [Athena SQL reference](https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html)

*Last verified against AWS documentation: November 2026.*
