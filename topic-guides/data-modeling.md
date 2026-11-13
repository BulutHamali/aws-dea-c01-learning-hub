# Data modeling, schema evolution, and lineage

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

**Start with the grain.** “One row per product per day” tells you how to aggregate, which keys should be unique, and when a join will duplicate rows.

## One workload, three models

| Reader | Model | Example |
|---|---|---|
| Order application | Normalize transactions and enforce relational constraints | Store order lines separately from customer records. Update a customer address in one place |
| Warehouse analyst | Use a fact table for measurable events and dimensions for descriptive context | Order-line facts join to product and date dimensions for daily totals |
| Low-latency API | Design keys around known requests | DynamoDB partition key `DEVICE#123` and sort key `READING#2026-04-01T10:00` support recent readings for one device |

For Redshift, evaluate distribution for join data movement and skew, sort order for selective scans, and encoding for compression. Start with automatic table optimization where appropriate and inspect real query plans and workloads before tuning manually. For DynamoDB, a secondary index supports a different access pattern and adds write and storage overhead.

## Make schema changes safe

1. Define old and new contracts. Adding an optional column is often easier to roll out than renaming a field or changing its type.
2. Update readers to tolerate both formats if the two will coexist. Version the schema and validate a representative batch.
3. Backfill if readers require history in the new shape. Publish the new version after validation.
4. Track lineage from source to output, including job version and run ID, so a broken dashboard can be traced to an input and transformation.

An engine migration may also require schema conversion for incompatible types or procedures. DMS schema conversion or AWS SCT can assess and convert supported objects. Moving rows and converting schemas are distinct parts of the migration.

<details>
<summary>Recall check</summary>

A report joins customers to orders and order lines. Summing the order total after joining to lines multiplies orders with multiple lines. Aggregate at the correct grain first, or use line-level amounts for a line-grain query.

</details>

[Redshift table design](https://docs.aws.amazon.com/redshift/latest/dg/c_designing-tables-best-practices.html) · [DynamoDB data modeling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql.html) · [DMS schema conversion](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_SchemaConversion.html)
