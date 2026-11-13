# Service decisions

[Home](../README.md) · [Pipeline challenges](../practice/pipeline-challenges.md)

Read the workload first. Identify its source, latency, required transformations, access pattern, and recovery needs. Then choose the simplest combination that satisfies those constraints.

| Requirement | Start with | What changes the decision |
|---|---|---|
| Multiple consumers need independent replay | [Kinesis Data Streams](../topic-guides/streaming.md) | Existing Kafka clients and connectors favor MSK |
| Deliver events to S3 with managed buffering | [Amazon Data Firehose](../topic-guides/streaming.md) | Stateful event-time joins or windows favor a stream processor |
| Make Kinesis events queryable in Redshift without S3 staging | [Redshift streaming ingestion](../topic-guides/redshift.md) | For archived batches already in S3, use COPY |
| Capture live changes from a supported database | [AWS DMS](../topic-guides/data-movement.md) | A file share migration favors DataSync. A partner SFTP endpoint favors Transfer Family |
| Convert and validate daily files | [AWS Glue ETL](../topic-guides/glue.md) | Custom software on cluster nodes can favor EMR on EC2 |
| Discover new partitions for a cataloged table | [Crawler or explicit partition registration](../topic-guides/catalog.md) | A predictable path used only by Athena can favor partition projection |
| Run SQL over S3 | [Athena](../topic-guides/athena.md) | If readers already query through Redshift and need joins with warehouse tables, consider Spectrum |
| Orchestrate several AWS services with explicit error branches | [Step Functions](../topic-guides/orchestration.md) | An existing Airflow DAG estate favors MWAA |
| Restrict which columns groups can query in a governed lake | [Lake Formation](../topic-guides/governance.md) | KMS controls key use. Macie can discover sensitive content |
| Find out who read an S3 object | [CloudTrail data events](../topic-guides/governance.md) | To alert on late pipeline output, publish a CloudWatch metric |
| Keep records for years while lowering storage costs | [S3 Lifecycle](../topic-guides/s3.md) | Retrieval deadlines determine the archive class. Deletion protection requires a separate retention control |

## Compare newer exam topics

| Requirement | First choice | Boundary to remember |
|---|---|---|
| Keep history of committed analytical table changes on S3 | [Iceberg](../topic-guides/iceberg.md) | Parquet is the file format. Iceberg tracks table state |
| Publish ownership and dataset definitions for business users | [SageMaker Catalog](../topic-guides/catalog-and-unified-studio.md) | Glue Data Catalog holds technical metadata for query engines |
| Find items similar in meaning across a large collection | [Vector search](../topic-guides/vectors-and-llms.md) | Evaluate latency and retrieval recall together |
| Track resource settings over time | [AWS Config](../topic-guides/privacy-and-audit.md) | CloudTrail records API activity. CloudWatch Logs stores application logs |

Follow the branching examples in the [visual decision maps](visual-maps.md).
