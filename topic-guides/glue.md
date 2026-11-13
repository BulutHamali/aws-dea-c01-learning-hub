# AWS Glue jobs, crawlers, and development tools

[Topic index](README.md) · [Home](../README.md)

## The idea

Glue brings together several tools for preparing data. Follow the input and output to identify which tool you need.

## How to decide

| Concept | When it matters |
|---|---|
| **Job** | Run ETL logic. Spark ETL fits distributed joins and format conversion. Glue streaming ETL processes records in micro-batches. |
| **Crawler and Data Catalog** | A crawler infers metadata such as schema and partitions. The catalog stores that metadata for services such as Athena. |
| **Glue Studio and Interactive Sessions** | Studio provides authoring and monitoring interfaces, including a visual editor. Interactive Sessions provide a managed runtime for iterative code development in notebooks or compatible IDEs. |
| **Bookmarks and checkpoints** | Supported batch sources can use bookmarks to track processed input. Streaming jobs track progress through checkpoints. Design output writes to tolerate replay. |

## Common mistake

Resetting a bookmark can reprocess old inputs. Existing target files remain, so plan a separate output location or replace the affected data safely.

## Try it

Daily CSV files must become partitioned Parquet after unit normalization and invalid-row checks.

<details>
<summary>Show the reasoning</summary>

Use a Glue ETL job for the transformation. Update the curated table metadata explicitly or with a crawler. Use bookmarks if the batch source supports them and make the sink safe to rerun.

</details>

## AWS documentation

- [AWS documentation · what is glue](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
- [AWS documentation · monitor continuations](https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html)
- [AWS documentation · add job streaming](https://docs.aws.amazon.com/glue/latest/dg/add-job-streaming.html)
