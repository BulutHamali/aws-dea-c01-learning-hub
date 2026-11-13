# AWS Glue jobs, crawlers, and development tools

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Think of a library. A crawler inspects new arrivals and updates the index. The Data Catalog holds that index. An extract, transform, and load (ETL) job opens the boxes, checks their contents, and repackages them.

## How to decide

| Requirement | Glue feature | What you configure |
|---|---|---|
| Query files through Athena | Data Catalog table | File location, schema, and partitions. A crawler can discover metadata, or the pipeline can register it explicitly. |
| Convert daily files, validate rows, or join large tables | Spark ETL job | Input sources, transformation code, worker type, output layout, and retry behavior. |
| Apply Spark transforms as events arrive | Streaming ETL job | Stream source, micro-batch window, checkpoint location, and output sink. |
| Develop interactively | Interactive Sessions | A managed Spark runtime for iterative code in a notebook or integrated development environment. |
| Create or monitor an ETL job visually | Glue Studio | Visual or script authoring and run monitoring. Studio notebooks can use Interactive Sessions. |

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| G.1X worker | 1 data processing unit (DPU), 4 virtual CPUs, 16 GB memory | Start here for ordinary distributed transformations. | [Glue worker types](https://docs.aws.amazon.com/glue/latest/dg/worker-types.html) |
| G.2X worker | 2 DPUs, 8 virtual CPUs, 32 GB memory | More capacity per worker can help larger joins, but inspect skew before scaling. | [Glue worker types](https://docs.aws.amazon.com/glue/latest/dg/worker-types.html) |
| R.1X worker | 1 memory-optimized DPU, 4 virtual CPUs, 32 GB memory | Choose more memory per CPU when individual workers are memory-bound. | [Glue worker types](https://docs.aws.amazon.com/glue/latest/dg/worker-types.html) |
| Flex execution | Glue 3.0 or later with the `glueetl` command | Use for non-urgent Spark batch jobs that tolerate variable startup and completion times. Use Standard for deadlines. | [Glue Job API and execution classes](https://docs.aws.amazon.com/glue/latest/webapi/API_Job.html) |
| Auto Scaling | Available for eligible workloads on Glue 3.0 or later | Configure an upper worker count. Glue can vary workers with demand during the job. | [Glue Auto Scaling](https://docs.aws.amazon.com/glue/latest/dg/auto-scaling.html) |
| Streaming micro-batch window | 100 seconds by default, configurable | Shorter windows can publish sooner if processing keeps pace. Monitor backlog and sink writes. | [Glue streaming ETL](https://docs.aws.amazon.com/glue/latest/dg/add-job-streaming.html) |

## Glue connections, networking, and credentials

A Glue connection supplies information for reaching a data source, such as a Java Database Connectivity (JDBC) endpoint. A catalog table describes the data the engine reads. For a private database, configure the virtual private cloud (VPC), subnet, and security groups. Check routes, available addresses, Domain Name System (DNS) resolution, and reachability to the database and the other services used by the job. Glue uses network interfaces with private addresses for this connection.

Use the job’s execution role to access data and retrieve any secret it needs. Give the database user only the privileges required to read or write the relevant tables. If a connection test times out, inspect the network path before changing credentials. If the database rejects authentication, inspect the stored credentials and database grants.

## Joining sources, schema alignment, and skew

A Spark DataFrame has a defined schema. A Glue DynamicFrame can represent inconsistent types as choice types. If the sequencing instruments send `reads` as either a number or text, use `ResolveChoice` to resolve the ambiguity before you publish a typed table. Keep rows that fail validation in quarantine so operators can repair them.

| Transform | Use it when |
|---|---|
| `ResolveChoice` | A field contains more than one type. Choose a rule such as casting to a target type or preserving alternative representations. |
| `ApplyMapping` | You need an explicit mapping of field names and types from the source schema to the output. |
| `Relationalize` | You need to flatten nested records and represent nested arrays as related tables. |

Align identifiers and types before joining. Filter early, select the fields you need, and inspect the largest Spark partitions. If one instrument owns most of the records and one task runs much longer than others, investigate key skew. Changing the worker count alone may leave that oversized partition in place.

## Bookmarks, checkpoints, and backfills

For a batch job on a bookmark-compatible source, enable bookmarks, initialize the job with `job.init()`, keep a stable transformation context for the source, and call `job.commit()` after successful output. Glue saves the bookmark state at commit. If the job dies after writing output and before committing, it can reread input on the next run. Make publication safe to repeat.

For streaming, Glue tracks progress in a checkpoint. When restarting, keep the checkpoint path unless you intend to change replay behavior. If you reset a bookmark or replay a stream interval, use a separate output path or replace or merge the affected output safely.

## Common mistake

A crawler that finishes successfully only confirms a metadata operation completed. If a new partition is missing, inspect the data location and catalog. If the files themselves contain the wrong values, inspect the transformation and quality checks.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Crawler vs. job vs. partition projection | Use a crawler to discover metadata, a job to change data, and Athena partition projection when Athena can calculate predictable paths from rules. |

**Exam cues:** Incremental batch input, continuously running Spark, schema inference, or interactive ETL development. Use the stated requirements to decide.

## Try it

The lab receives daily files. A schema change sends an integer measurement as a string. A job wrote output before failing and the following run duplicated rows.

<details>
<summary>Show the reasoning</summary>

Use a Glue Spark job with explicit type handling and validation. Quarantine invalid values, write curated Parquet, and update the catalog metadata. Commit the input bookmark after publication. Use a stable batch identifier and safe replacement or merge so a rerun after partial success yields the same dataset.

</details>

## AWS documentation

- [Glue JDBC connections in a VPC](https://docs.aws.amazon.com/glue/latest/dg/connection-JDBC-VPC.html)
- [Tracking processed data with bookmarks](https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html)
- [DynamicFrame transforms and schema operations](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
- [Glue Interactive Sessions](https://docs.aws.amazon.com/glue/latest/dg/interactive-sessions.html)

*Last verified against AWS documentation: November 2026.*
