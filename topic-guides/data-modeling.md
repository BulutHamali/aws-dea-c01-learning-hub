# Data modeling, schema evolution, conversion, and lineage

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

**Start with the grain.** The grain is what one row represents, such as "one sequencing run per day". It tells you how to aggregate, which keys must be unique, and when a join will multiply rows. Every modeling decision follows from the grain and from how the data will be read.

## Grain, keys, sort order, and governed schemas

The same lab data needs three different models for three readers.

| Reader | Model | Example |
|---|---|---|
| Lab application in RDS | Normalized tables with constraints | `runs`, `samples`, and `instruments` tables. An instrument rename changes one row |
| Analyst in Redshift | Star schema: a fact table of measurable events and dimension tables of context | `fact_run_reads` joins `dim_instrument` and `dim_date` for daily totals |
| Status API in DynamoDB | Keys built for the known request | `PK = SAMPLE#S42`, `SK = STATUS#2026-04-01T10:00` returns the latest statuses for one sample |
| Governed lake in Lake Formation | Catalog tables with columns grouped by sensitivity | Keep identifiers in separate columns so column filters can hide them |

**Facts and dimensions.** A fact table holds numbers you add up, such as read counts, at a stated grain. A dimension describes them, such as instrument model or date. When a dimension value changes over time, a **slowly changing dimension type 2** keeps history by adding a new row with valid-from and valid-to dates instead of overwriting.

**Redshift.** Choose distribution keys from the most common large join and sort keys from the most common range filter. See [Redshift table design](redshift.md#table-design-distribution-and-sort-keys).

**DynamoDB.** List every access pattern first, then design keys and secondary indexes to serve them. Single-table design stores several entity types in one table with prefixed keys. See [databases](databases.md#keys-indexes-and-warehouse-layout).

## Compatible and breaking schema changes

| Change | Usually safe? | What to do |
|---|---|---|
| Add an optional column | Yes | Readers ignore it until they use it. Backfill if history needs a value |
| Widen a type, such as int to bigint | Often | Confirm every engine supports the promotion |
| Rename a column | Breaks name-based readers | Iceberg renames by column ID safely. For plain Parquet, add the new column and keep the old one for a transition period |
| Change a type, such as number to text | Breaks readers | Version the dataset, migrate readers, then backfill |
| Remove a column | Breaks readers that use it | Announce, deprecate, then drop |

A safe rollout: define old and new contracts, make readers tolerate both, validate a sample batch, backfill if needed, then switch. For streams, register schemas in the Glue Schema Registry with a compatibility mode so producers cannot publish breaking changes.

## DMS Schema Conversion and manual action items

Moving to a different database engine has two parts. **Schema conversion** translates tables, views, stored procedures, and types. **Data migration** moves the rows.

- **AWS DMS Schema Conversion** runs inside AWS Database Migration Service. It assesses the source, converts supported objects, and lists *action items* for code it cannot convert automatically.
- **AWS Schema Conversion Tool (AWS SCT)** is the older desktop tool for the same job. The exam guide still names it as an example. Version 1.1 removed it from the list of in-scope services, so lead with DMS Schema Conversion.
- After conversion, use DMS full load plus change data capture (CDC) to move and sync rows. See [data movement](data-movement.md).

## Catalog lineage and SageMaker ML Lineage Tracking

**Lineage** is the record of where data came from and what changed it. When a dashboard breaks, lineage tells you which input and which job version to check.

| Tool | Tracks | Use when |
|---|---|---|
| SageMaker Catalog lineage (in SageMaker Unified Studio) | Data assets and the jobs that transform them. Captured automatically from AWS Glue, Amazon Redshift, Visual ETL, and notebooks. OpenLineage-compatible APIs accept events from other tools | You need dataset-to-dataset lineage for analytics pipelines |
| Amazon SageMaker ML Lineage Tracking | ML workflow entities: datasets, processing and training jobs, models, and endpoints | You need to trace which data trained which model |
| Your own run metadata | Job version, run ID, input partitions, and row counts written alongside outputs | Every pipeline, as a minimum |

Lineage versions with each event, so you can compare a job's inputs before and after a change.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| SageMaker Unified Studio lineage format | OpenLineage-compatible | Lets non-AWS tools publish lineage events into the same graph | [Data lineage support](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/datazone-data-lineage-support.html) |
| Automatic lineage sources | AWS Glue, Amazon Redshift, Visual ETL, notebooks | Other tools need API or OpenLineage integration | [Data lineage support](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/datazone-data-lineage-support.html) |
| AWS SCT exam scope | Removed from in-scope services in exam guide v1.1 | Expect DMS Schema Conversion in answers | [Exam guide revisions](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/dea-01-revisions.html) |

## Common mistake

Summing an order total after joining orders to order lines. Each order repeats once per line, so the total multiplies. Aggregate at the right grain first, or sum line-level amounts.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Normalized vs. star schema | Fast safe updates vs. fast analytical reads |
| DMS Schema Conversion vs. DMS replication | Translate structure and code vs. move and sync rows |
| SageMaker Catalog lineage vs. ML Lineage Tracking | Data pipeline lineage vs. model training lineage |
| SCD type 1 vs. type 2 | Overwrite the value vs. keep history in new rows |

**Exam cues:** "Heterogeneous migration", "stored procedures" → DMS Schema Conversion. "Which dataset trained this model" → ML Lineage Tracking. "Trace a broken dashboard back to its source" → catalog lineage.

## Try it

A lab moves from Oracle to Aurora PostgreSQL. It has hundreds of stored procedures. Analysts later want to know which raw files fed each curated table.

<details>
<summary>Show the reasoning</summary>

Assess and convert the schema with DMS Schema Conversion and resolve its action items by hand. Migrate rows with DMS full load plus CDC, then cut over. Capture lineage automatically by running transforms in Glue connected to SageMaker Unified Studio, and record run IDs with outputs.

</details>

## AWS documentation

- [Redshift table design best practices](https://docs.aws.amazon.com/redshift/latest/dg/c_designing-tables-best-practices.html)
- [DynamoDB data modeling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql.html)
- [DMS Schema Conversion](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_SchemaConversion.html)
- [SageMaker Unified Studio data lineage](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/datazone-data-lineage-support.html)
- [SageMaker ML Lineage Tracking](https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html)

*Last verified against AWS documentation: November 2026.*
