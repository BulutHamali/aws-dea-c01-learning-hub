# Data quality, quarantine, and safe recovery

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

A **quality gate** is a set of checks a batch must pass before readers can see it. Bad rows go to quarantine with a reason. Good rows are published in one step. If the job fails halfway, readers still see yesterday's complete data, not a half-written batch.

## Validate, quarantine, and reconcile rows

Run checks while processing:

| Check | Example |
|---|---|
| Completeness | `run_id` is never empty |
| Validity | `reads >= 0` and `instrument` is in the known list |
| Uniqueness | One row per `run_id` per day |
| Volume | Today's row count is within 30% of the recent average |
| Freshness | The newest `run_date` is yesterday or today |
| Referential integrity | Every `instrument` exists in the instrument dimension |

Write rejected rows to `quarantine/` with the rule that failed, the source file, and the batch ID. Then reconcile: `input rows = published rows + quarantined rows`. If the numbers don't add up, rows were lost.

## Glue DQDL and DataBrew rule sets

**AWS Glue Data Quality** checks data with rules written in Data Quality Definition Language (DQDL). You can run it in a Glue ETL job, in a Glue Studio visual job, or against a Data Catalog table.

```text
Rules = [
    IsComplete "run_id",
    IsUnique "run_id",
    ColumnValues "reads" >= 0,
    RowCount between min(last(7)) - 1000 and max(last(7)) + 1000
]
Analyzers = [
    Completeness "instrument"
]
```

- Rules pass or fail. A job can stop or route failing records based on the result.
- **Analyzers** collect statistics without passing or failing, for trend monitoring.
- `DetectAnomalies` and dynamic rules such as `min(last(7))` compare against recent runs instead of a fixed number.
- `ReferentialIntegrity` checks that values exist in a reference dataset, such as every instrument in the instrument list.

**AWS Glue DataBrew** offers data quality rulesets and profile jobs in a visual tool, for teams that prefer point-and-click.

## Profile drift and reconcile counts

To investigate inconsistent data:

1. Run a profile (DataBrew profile job or Glue Data Quality analyzers) on a good day and a bad day.
2. Compare null rates, distinct counts, min and max values, and type mismatches.
3. Compare source and target counts per key and per day with SQL. See [SQL patterns](sql-patterns.md#find-gaps-and-duplicates).
4. Check whether the source changed its schema. A column arriving as text instead of a number is a common cause.

## Idempotent publishing and backfills

**Idempotent** means running the same work twice gives the same final result.

- Write to a path tied to the batch, such as `run_date=2026-01-01/`, and replace the whole partition at the end.
- Or `MERGE` by a stable business key so a repeat updates instead of duplicating.
- Or use an Iceberg table, where each write commits atomically.
- Record a completion marker only after the data is fully written.

For a **backfill**, pick a bounded date range, check what was already published, and rerun with the same overwrite or merge strategy.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| DQDL rule format | `<RuleType> <Parameter> <Expression>`, inside `Rules = [ ]` | Recognize valid DQDL in answer options | [DQDL reference](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html) |
| Composite rules | Combine rules with `and` and `or`, each in parentheses | Express "either condition is fine" checks | [DQDL reference](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html) |
| Analyzers | Gather statistics without pass or fail. Not supported for Data Catalog evaluations | Use for monitoring trends | [DQDL reference](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html) |
| DataBrew transformations | More than 250 prebuilt | No-code cleaning for analysts | [What is DataBrew?](https://docs.aws.amazon.com/databrew/latest/dg/what-is.html) |

## Common mistake

Rerunning a failed job that writes files with random names. The rerun adds a second copy of every row that was written before the failure.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Glue Data Quality vs. DataBrew | Rules in code inside pipelines vs. visual rules and profiling for analysts |
| Rule vs. analyzer | Pass or fail vs. statistics only |
| Quarantine vs. drop | Keep bad rows for repair vs. lose them |

**Exam cues:** "Check for empty fields during processing" → Glue Data Quality rules in the job. "Profile data without code" → DataBrew. "Rerun without duplicates" → idempotent write.

## Try it

A nightly load fails after writing 60% of its files. The source can be replayed. Some rows have negative read counts.

<details>
<summary>Show the reasoning</summary>

Add DQDL rules such as `ColumnValues "reads" >= 0` and route failing rows to quarantine. Stage the full batch, then replace the partition or `MERGE` by run ID so the rerun does not duplicate rows. Reconcile input, published, and quarantined counts.

</details>

## AWS documentation

- [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html)
- [DQDL reference](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html)
- [DataBrew data quality rules](https://docs.aws.amazon.com/databrew/latest/dg/profile.data-quality-rules.html)

*Last verified against AWS documentation: November 2026.*
