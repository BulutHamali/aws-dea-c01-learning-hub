# Programming concepts for data engineers

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

The exam does not ask you to write code, but it expects you to recognize which language, data structure, compute option, and coding habit fits a job. This guide covers those concepts. APIs and SDKs are in [APIs and SDKs](apis-and-sdks.md), testing and IaC in [deployment](deployment.md), and Lambda in [Lambda](lambda.md).

## SQL, Python, and Spark workload choices

| Language or framework | Use it for |
|---|---|
| SQL | Filters, joins, aggregations, and merges in Athena and Redshift |
| Python | Glue jobs, Lambda functions, SDK automation, and data validation |
| PySpark or Scala with Spark | Distributed transformations on Glue or EMR |
| Java | Kinesis Client Library consumers, Flink applications |
| R | Statistical analysis, less common in pipelines |
| Bash and PowerShell | Scripts that move files, run CLI commands, or bootstrap EMR nodes |

Push work to where the data is. A SQL aggregation inside Redshift beats pulling millions of rows into Python.

## Batching, parallelism, and pushdown

Ways to reduce runtime for ingestion and transformation code:

| Technique | Example |
|---|---|
| Batch requests | `PutRecords` sends up to 500 records per call instead of one `PutRecord` each |
| Parallelize independent work | Process each date partition in a separate task |
| Predicate pushdown | Filter at the source so less data is read. Glue `push_down_predicate` reads only matching partitions |
| Column pruning | Select only needed columns from Parquet |
| Avoid row-by-row loops | Use vectorized DataFrame operations or set-based SQL |
| Reuse connections and clients | Create SDK clients and database connections outside the Lambda handler |
| Cache small lookups | Broadcast a small reference table in Spark |

## Container sizing and deployment choices

| Requirement | Service |
|---|---|
| Queue of containerized batch jobs with managed scheduling | AWS Batch |
| Long-running containerized services | Amazon ECS, on AWS Fargate for no server management |
| Organization standardized on Kubernetes | Amazon EKS |
| Store container images | Amazon Elastic Container Registry (ECR) |

To optimize containers for performance, right-size CPU and memory to what the task actually uses, use Fargate Spot or EC2 Spot for interruptible batch work, and keep images small so tasks start faster.

## Distributed computing

When data doesn't fit on one machine or one process takes too long, split it into partitions and process them in parallel on many workers. The cost is coordination: shuffles, stragglers, and partial failures. See [EMR and distributed processing](emr.md#distributed-processing-shuffle-and-workers).

## Maps, trees, and graphs

| Structure | What it is | Data engineering example |
|---|---|---|
| Hash map (dictionary) | Key to value lookup in roughly constant time | Look up an instrument's model by ID while processing records |
| Array or list | Ordered sequence | A batch of records to write |
| Queue | First in, first out | SQS buffering work between steps |
| Tree | Hierarchy with one parent per node | Folder structures, B-tree database indexes, JSON documents |
| Graph | Nodes connected by edges, any shape | Lineage of datasets and jobs, task dependencies in an Airflow DAG (directed acyclic graph) |

Algorithms to recognize: sorting (needed before merge joins and for sort keys), hashing (distributing rows to partitions and shards), and graph traversal (finding everything downstream of a broken dataset).

## Common mistake

Collecting a large distributed dataset onto the Spark driver to do a lookup in a Python dictionary. The driver runs out of memory. Join or broadcast instead.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| AWS Batch vs. ECS | Queued jobs that finish vs. services that keep running |
| Tree vs. graph | One parent per node vs. any connections |
| Pushdown vs. post-filter | Filter while reading vs. read everything, then filter |

**Exam cues:** "Containerized batch jobs" → AWS Batch. "Dependencies between tasks" → DAG, a graph. "Reduce runtime" → batch calls, parallelize, push filters down.

## Try it

A Python script calls `PutRecord` once per event and loops over rows one at a time. It falls behind as volume grows.

<details>
<summary>Show the reasoning</summary>

Send events with `PutRecords` in batches, retry only the failed entries, and process rows with vectorized operations. If volume keeps growing, move the transform to Glue or Flink.

</details>

## AWS documentation

- [AWS Batch](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html)
- [Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [Glue pushdown predicates](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-partitions.html)
- [Kinesis PutRecords](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecords.html)

*Last verified against AWS documentation: November 2026.*
