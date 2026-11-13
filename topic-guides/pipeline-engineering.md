# APIs and reliable deployments

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

A pipeline is a series of handoffs. At each handoff, know what has arrived, what is durable, and what can safely be repeated. Think of a numbered receipt for a parcel. If delivery times out, the receipt lets you check whether the parcel was accepted before sending it again.

## How the pieces fit

| Requirement | Design choice | What to check |
|---|---|---|
| Read all pages of a partner API | Follow the returned pagination token and checkpoint progress after the page has been stored durably | Handle HTTP 429 with bounded exponential backoff and jitter. Honor Retry-After where provided |
| Fan out an announcement | Publish to SNS or route matching events through EventBridge | Each consumer that needs buffering can have its own SQS queue |
| Execute heavy containerized jobs | Use AWS Batch for queued compute or a managed Spark engine for distributed data processing | Right-size CPU, memory and partitions. An ECR repository stores images. ECS and EKS run container workloads |
| Make deployments repeatable | Define resources in CloudFormation, CDK or SAM and version them in Git | Validate changes in CI, test a small batch, separate deployment and execution roles, and plan rollback |

## Follow one failure

An API gives you page 8, your pipeline writes it to S3, then crashes before saving the token. On restart it may fetch page 8 again. Write to a deterministic destination tied to the batch and page identity, or deduplicate by a stable record key. If the token advances before durable storage, page 8 can be lost.

Use streaming or distributed processing when the input cannot fit into the memory or runtime of a single process. A hash map is useful for bounded key lookups. A graph represents relationships. A tree represents a hierarchy. Avoid collecting a distributed dataset onto one Spark driver just to perform a lookup.

For event processing, see [Lambda for data pipelines](lambda.md). For queues, notifications, and retries, see [orchestration](orchestration.md).

[AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) · [AWS Batch](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html)
