# Lambda for data pipelines

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## Choose Lambda for a data pipeline

Use AWS Lambda for short, event-driven work such as validating an object manifest, normalizing a stream record, or starting a Glue job. Send large distributed joins and file rewrites to Glue or Amazon EMR. Pass a storage location or batch ID into the function when the data is large.

| If you need to… | Use |
|---|---|
| Validate a manifest after upload | Lambda triggered by an object event or the workflow that owns the batch |
| Process Kinesis or queue records in batches | Lambda event source mapping with retry and failure settings for that source |
| Wait for a long data-processing job | A Step Functions service integration that waits for the job |
| Run a distributed join | Glue Spark or EMR, using Lambda only to initiate work if needed |

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Standard Lambda function timeout | Up to 900 seconds (15 minutes) | Break work into bounded units or use a job service. Lambda Managed Instances have separate invocation limits. | [Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html) |
| Function temporary storage | 512 MB by default, configurable up to 10,240 MB | Size scratch space for the largest working file. Keep durable results outside `/tmp`. | [Lambda ephemeral storage](https://docs.aws.amazon.com/lambda/latest/dg/configuration-ephemeral-storage.html) |
| Kinesis event source batch size | 100 records by default, configurable up to 10,000, subject to payload size | Larger batches amortize invocation overhead but take longer to process. | [Kinesis event source mapping parameters](https://docs.aws.amazon.com/lambda/latest/dg/services-kinesis-parameters.html) |
| Kinesis `ParallelizationFactor` | 1 by default, configurable up to 10 batches per shard | Raise it when processing capacity is the bottleneck and the sink can absorb concurrency. | [Kinesis event source mapping parameters](https://docs.aws.amazon.com/lambda/latest/dg/services-kinesis-parameters.html) |
| Amazon Simple Queue Service (Amazon SQS) visibility guidance | At least six times the function timeout, plus the configured batching window | This is an AWS recommendation. Lambda requires the function timeout to be no greater than queue visibility. | [SQS event source configuration](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html) |
| Standard versus first-in, first-out (FIFO) queue batch limits | Up to 10,000 records for a standard queue and 10 for a FIFO queue, subject to payload size | A standard queue batch size above 10 requires a batching window of at least one second. | [SQS event source configuration](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html) |

## Read a Kinesis stream with Lambda

An event source mapping polls a stream or reads through enhanced fan-out and passes records to the function in batches. Give the execution role access to read the stream. Choose `TRIM_HORIZON` to start at the oldest retained data, `LATEST` to start with new data, or `AT_TIMESTAMP` to start from a specified time. AWS recommends `TRIM_HORIZON` or `AT_TIMESTAMP` when you must avoid missing records during mapping creation or updates.

A failed invocation can hold up later records on the affected shard. Use bounded retries, a maximum record age, a failure destination, and idempotent writes. `BisectBatchOnFunctionError` splits an erroring batch so a poison record is easier to isolate. With partial batch responses, Lambda resumes from the lowest sequence number reported as failed and can invoke later records again. Follow the source-specific response format.

If lag rises, check the function’s error rate and duration, stream read capacity, and sink latency. Increase shard parallelization only when the workload and destination can handle the additional concurrency. See [stream throughput](streaming.md#fan-in-fan-out-and-throughput).

## Reserved and provisioned concurrency

**Reserved concurrency** sets aside concurrency and caps how much the function can use. Apply it when many invocations could overload a downstream database. An SQS event source mapping can also set a maximum concurrency so one queue does not consume all the function’s capacity.

**Provisioned concurrency** pre-initializes environments for a function version or alias. Use it to reduce cold-start latency when an endpoint has predictable demand. Capacity limits and pre-initialization address different requirements.

## Temporary and shared storage

Use `/tmp` for scratch data such as a decompressed working file. Use Amazon Elastic File System (Amazon EFS) if several environments need a shared mounted file system and the function can reach its mount targets from the configured network. Store durable batch progress in a service such as DynamoDB or Amazon S3 so it survives replacement of an execution environment.

## Queue retries and duplicate writes

When an SQS invocation fails, messages can become visible again after the visibility timeout. Enable `ReportBatchItemFailures` to report only failed messages. For a FIFO queue, stop after the first failure and return failed and unprocessed items to preserve ordering. Configure the queue’s redrive policy to send persistently failing messages to a dead-letter queue. Use a stable record key at the sink to handle duplicate delivery.

## Common mistake

Turning on provisioned concurrency to protect a database from too many connections. Provisioned concurrency makes more environments ready, which can push even more load downstream. Reserved concurrency, an SQS maximum concurrency setting, or RDS Proxy limits the load.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Reserved vs. provisioned concurrency | Use reserved concurrency to protect capacity and cap a function. Use provisioned concurrency to reduce initialization latency. |

**Exam cues:** Cold starts, database connection limits, partial batch failure, or shared file system. Use the stated requirements to decide.

## Try it

A lab uses Lambda to read instrument events and write validated rows to a database. Invalid records stall progress. After retry, some valid rows are duplicated, and the database sees too many simultaneous writes.

<details>
<summary>Show the reasoning</summary>

Use bounded retry and an on-failure destination on the Kinesis event source mapping. Enable failure isolation where it fits and deduplicate using the instrument event ID. Use reserved concurrency to protect the database, then verify lag and database connection metrics. Provisioned concurrency helps startup latency and does not provide the database protection requirement.

</details>

## AWS documentation

- [Using Lambda with Kinesis](https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html)
- [Kinesis partial batch responses](https://docs.aws.amazon.com/lambda/latest/dg/services-kinesis-batchfailurereporting.html)
- [Lambda concurrency](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html)
- [SQS error handling and partial batch responses](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html)
- [Lambda file system access](https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem.html)

*Last verified against AWS documentation: November 2026.*
