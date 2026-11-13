# Amazon EMR, distributed processing, and skew

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Distributed computing splits one big job across many machines. Each worker processes its own chunk, called a **partition**, then workers exchange data when they need to group or join by a key. That exchange is the **shuffle**, and it is usually the slowest step. Amazon EMR runs open-source engines such as Apache Spark, Hive, Presto, and Flink on clusters AWS manages for you.

## Distributed processing, shuffle, and workers

| Term | Plain meaning |
|---|---|
| Driver | The process that plans the job and hands out tasks |
| Executor or worker | A process that runs tasks on one chunk of data |
| Partition | One chunk of data processed by one task |
| Shuffle | Moving rows between workers so all rows with the same key meet on one worker |
| Narrow transformation | Each output partition needs one input partition, such as a filter. No shuffle |
| Wide transformation | Needs rows from many partitions, such as `groupBy` or a join. Causes a shuffle |

Avoid `collect()` on a large dataset. It pulls every row to the driver, which runs out of memory.

## Transformation engine decisions

| Requirement | First choice | Why |
|---|---|---|
| Serverless Spark ETL that uses the Glue Data Catalog and connections | AWS Glue | Least operational work for typical ETL |
| Spark or Hive jobs that run intermittently, without cluster management | EMR Serverless | Pay while the job runs. Pre-initialized capacity reduces startup time |
| Custom software on nodes, bootstrap actions, specific instance types, or a long-running cluster | EMR on EC2 | Full control of nodes and configuration |
| Your organization already runs Amazon EKS | EMR on EKS | Spark jobs share the Kubernetes platform |
| Small, short transformations per event | AWS Lambda | No cluster at all. Limited to 15 minutes |
| SQL transformations inside the warehouse (ELT) | Amazon Redshift | The data is already there |

## Operational choices on EMR on EC2

| Node type | Role | Spot safe? |
|---|---|---|
| Primary | Manages the cluster | No |
| Core | Runs tasks and stores HDFS data | Risky, because losing a node loses HDFS blocks |
| Task | Runs tasks only, no HDFS | Yes, the usual place for Spot Instances |

- **Instance groups** use one instance type per group. **Instance fleets** allow up to five instance types per fleet with a mix of On-Demand and Spot, which improves the chance of getting Spot capacity.
- **Managed scaling** adds and removes core and task capacity between a minimum and maximum you set. It works with YARN applications such as Spark and Hive.
- Store data in S3, not HDFS, so you can terminate transient clusters after each job.

## Spark execution stages, logs, and failure isolation

When an EMR or Glue Spark job fails or runs slowly:

1. Open the Spark UI or the persistent Spark History Server. Find the slowest stage.
2. Compare task durations inside that stage. One task far slower than the rest means skew.
3. Check executor logs for `OutOfMemoryError`, `Container killed by YARN`, or S3 throttling (`503 Slow Down`).
4. EMR writes cluster and step logs to S3 when you configure a log location. Glue writes to CloudWatch Logs.
5. Rerun failed steps only for the affected partitions when the output is written idempotently.

## Diagnose and mitigate partition and join skew

**Skew** means a few keys hold most of the rows. One worker gets a huge partition while the others sit idle. Adding workers does not help that one worker.

| Technique | How it helps |
|---|---|
| Adaptive Query Execution (AQE) skew join | Spark 3 splits oversized join partitions automatically at run time |
| Broadcast join | Ships a small table to every worker so the big table needs no shuffle |
| Salting | Adds a random suffix to a hot key so its rows spread across several partitions, then aggregates twice |
| Filter or pre-aggregate early | Shrinks data before the shuffle |
| Repartition on a better key | Spreads rows more evenly before writing |

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Instance types per instance fleet | Up to 5 | More types raise the chance of Spot capacity | [EMR managed scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html) |
| Managed scaling scope | Core and task nodes. The primary node does not scale | Size the primary node correctly at launch | [EMR managed scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html) |
| Managed scaling applications | YARN-based, such as Spark, Hive, Flink. Not Presto or HBase | Choose another scaling approach for non-YARN apps | [EMR managed scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html) |
| Lambda maximum run time | 15 minutes | Large transforms need Glue or EMR | [Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html) |

## Common mistake

Doubling the cluster when one task is slow. Check the stage's task times. If one key holds most rows, fix the skew instead.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Glue vs. EMR Serverless vs. EMR on EC2 | Least operations with Glue integration, serverless open-source runtime, or full node control |
| Core vs. task nodes | Stores HDFS data vs. compute only, safe for Spot |
| Instance groups vs. fleets | One type per group vs. up to five types with Spot diversity |
| Broadcast join vs. salting | One side is small vs. both sides large with a hot key |

**Exam cues:** "Custom software installed at startup" → EMR on EC2 with bootstrap actions. "Reduce cost of interruptible compute" → Spot task nodes. "One task runs much longer" → skew.

## Try it

A Spark join of reads to instruments takes two hours. One task runs for 110 minutes while others finish in two. The instruments table is 20 MB.

<details>
<summary>Show the reasoning</summary>

The single long task shows skew on the join key. Broadcast the 20 MB instruments table so the large table needs no shuffle, and enable AQE skew join for other joins. Verify in the Spark UI that task times even out.

</details>

## AWS documentation

- [What is Amazon EMR?](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)
- [EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html)
- [EMR on EKS](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/emr-eks.html)
- [EMR managed scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html)

*Last verified against AWS documentation: November 2026.*
