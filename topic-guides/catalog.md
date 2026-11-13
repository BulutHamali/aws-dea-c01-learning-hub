# Glue Data Catalog, crawlers, and partition sync

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Files in S3 are just bytes. The **catalog** tells a query engine where a table lives, which columns it has, how to parse its files, and which partitions exist. If the files exist but the catalog does not know about them, the query returns nothing. Data and metadata are separate layers.

## Read a cataloged dataset

The AWS Glue Data Catalog is a technical catalog. Athena, Redshift Spectrum, EMR, and Glue jobs all read table definitions from it. A table entry holds:

- the S3 location
- columns and types
- the format and serializer/deserializer (SerDe) that parses files
- the partition keys and partition locations

Lake Formation can control who may read each table, column, or row. See [governance](governance.md).

## Crawler discovery and schema change policy

A **crawler** scans an S3 path or a JDBC source, infers the schema, and creates or updates tables and partitions.

| Setting | What it controls | Safe default for a curated table |
|---|---|---|
| Schema change policy, update behavior | Whether a changed schema updates the table or only logs the change | Log changes, then update the table through a reviewed process |
| Schema change policy, delete behavior | What happens when source objects disappear | Log or mark deprecated instead of deleting tables |
| Recrawl policy | Crawl everything again, or only new folders | Crawl new folders only, for append-only data |
| Table grouping | Whether similar folders merge into one table | Set an explicit table level so date folders don't become separate tables |
| Schedule | When the crawler runs | After data lands, or replace the crawler with explicit partition registration |

Crawlers infer. If two files in one folder disagree on a column type, the crawler may create a table you did not expect. For curated data where you control the schema, define the table yourself and register partitions from the pipeline.

## Registration, repair, and partition projection

| Method | How it works | Fits |
|---|---|---|
| Crawler | Discovers new partitions on a schedule or after an event | Unpredictable folders and schema discovery |
| `ALTER TABLE ADD PARTITION` or the Glue API from the pipeline | The job registers the partition it just wrote | Controlled pipelines. New data is visible immediately after the job |
| `MSCK REPAIR TABLE` | Athena lists S3 and adds Hive-style `key=value` folders | Occasional repair. Slow for many partitions and does not handle non-Hive paths |
| Partition projection | Athena computes partition locations from rules in table properties, with no catalog partitions | Predictable paths such as dates, for Athena-only tables |
| Partition indexes | Glue indexes partition keys to speed partition lookups | Tables with very many partitions |

With partition projection enabled, Athena ignores partitions registered in the catalog for that table. Other engines, such as Redshift Spectrum and EMR, do not use projection.

## Glue Data Catalog and Hive metastore

Apache Hive metastore is the open-source metadata service that Spark, Hive, and Presto use. EMR clusters can use the Glue Data Catalog as their metastore, so Athena and EMR share one set of table definitions. A self-managed Hive metastore on Amazon RDS is the alternative when you need full control. See [business catalogs](catalog-and-unified-studio.md) for SageMaker Catalog.

## Schema Registry

The AWS Glue Schema Registry stores versions of event schemas for streams such as Kinesis and MSK. Producers and consumers validate records against a registered version. A compatibility mode, such as `BACKWARD`, rejects changes that would break existing consumers.

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Projection and registered partitions | When projection is enabled, Athena ignores registered partition metadata for that table | Do not mix the two and expect both to work | [Partition projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html) |
| Partition key type for pushdown | `STRING` | Non-string keys can stop filter pushdown into Glue | [Athena data optimization](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html) |
| Projection over a wide range with no filter | Can require one S3 list per possible value | A query without a partition filter can be very slow | [Athena data optimization](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html) |

## Common mistake

Running a crawler every hour on a table whose path is fully predictable. It costs time and can change the schema unexpectedly. Partition projection or explicit registration is cheaper and deterministic.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Crawler vs. partition projection | Unknown structure vs. predictable path used only by Athena |
| `MSCK REPAIR TABLE` vs. `ALTER TABLE ADD PARTITION` | Bulk repair of Hive-style folders vs. registering a known partition |
| Glue Data Catalog vs. Schema Registry | Table metadata for queries vs. event schema versions for streams |
| Glue Data Catalog vs. SageMaker Catalog | Technical metadata vs. business meaning, ownership, and access requests |

**Exam cues:** "New partitions not showing in Athena" → registration, repair, or projection. "Least operational overhead" with predictable date paths → partition projection. "Prevent breaking changes to stream records" → Schema Registry compatibility.

## Try it

An Athena-only table receives a new folder each day at `s3://lab-lake/curated/runs/run_date=YYYY-MM-DD/`. A crawler runs hourly and once split the table into hundreds of tables.

<details>
<summary>Show the reasoning</summary>

Define the table explicitly and enable partition projection with a date range and a storage location template. Stop the crawler. Query a known date and confirm with `EXPLAIN` that only that prefix is read.

</details>

## AWS documentation

- [Glue Data Catalog and crawlers](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html)
- [Crawler schema change policy](https://docs.aws.amazon.com/glue/latest/dg/crawler-configuration.html)
- [Athena partition projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html)
- [Glue partition indexes](https://docs.aws.amazon.com/glue/latest/dg/partition-indexes.html)
- [Glue Schema Registry](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html)

*Last verified against AWS documentation: November 2026.*
