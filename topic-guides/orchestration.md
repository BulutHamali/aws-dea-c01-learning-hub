# Orchestration with EventBridge, Step Functions, and MWAA

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

An orchestrator decides when a step runs, what it waits for, and where failures go. An event router decides who receives an event. A queue holds work for a consumer. A pipeline can use all three.

## Step Functions, Glue workflows, and Airflow

| Requirement | Use | Deciding condition |
|---|---|---|
| Branch or retry across AWS services | AWS Step Functions | Use states and service integrations for explicit sequencing. With the Glue `.sync` integration in a Standard workflow, a step waits for the job result. |
| Chain Glue jobs and crawlers | AWS Glue Workflows | Use Glue triggers and dependencies when the pipeline lives within Glue. |
| Keep existing Apache Airflow directed acyclic graphs (DAGs) | Amazon Managed Workflows for Apache Airflow (Amazon MWAA) | Use existing operators, dependency graphs, and backfill conventions. |

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Standard workflow duration | Up to one year. Standard is the default type when the type is omitted. | Use for long-running or auditable workflows and run-a-job integrations. | [Choosing a Step Functions workflow type](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html) |
| Express workflow duration | Up to five minutes | Use for short, high-volume work. Design asynchronous Express tasks for at-least-once execution. | [Choosing a Step Functions workflow type](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html) |
| Standard execution history | Available for up to 90 days after completion | Keep longer-lived evidence in your own logs when required. | [Choosing a Step Functions workflow type](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html) |
| Step Functions state or task payload | 256 KiB maximum for relevant task, state, and execution input or output | Put the dataset in storage and pass its location, job ID, or batch ID. | [Step Functions service quotas](https://docs.aws.amazon.com/step-functions/latest/dg/service-quotas.html) |
| EventBridge rule target retries | Defaults of up to 24 hours and up to 185 attempts for retriable delivery errors. Set the target retry policy to adjust it. | Configure a dead-letter queue if you need to retain failed deliveries. | [EventBridge delivery retries](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html) |
| EventBridge Scheduler target retry bounds | At most 24 hours of event age and 185 retries | Configure the schedule’s policy separately from any EventBridge rule and the workflow itself. | [Scheduling Step Functions executions](https://docs.aws.amazon.com/step-functions/latest/dg/using-eventbridge-scheduler.html) |

## EventBridge Rules, Scheduler, and Pipes

- **Rules** match events on an event bus and route matches to configured targets.
- **Scheduler** runs a target once or on a recurring schedule. Use a calendar expression and time zone when a local business time matters.
- **Pipes** connect a source such as an Amazon Simple Queue Service (Amazon SQS) queue or Kinesis stream to one target. Use optional filters and enrichment for that path. Use a bus when several independent targets need to react to the same event.

## Schedules, time zones, and backfills

A schedule is a trigger. The processing date should still be an explicit parameter. If today’s run reprocesses yesterday’s data, pass yesterday’s date and the same logical batch identifier. Decide whether missed dates need manual backfill or Airflow catchup. Use a bounded range and confirm which destinations can accept safe replacement.

## S3 events and EventBridge routing

Use a narrow rule for the input bucket, event type, and raw input prefix. Prevent a loop by keeping output outside that input filter. Amazon Simple Storage Service (Amazon S3) event notifications can arrive more than once. Deduplicate with an identity that represents the same input, such as the bucket, key, and version when bucket versioning supplies one. A duplicate trigger should reach a safe write path.

## Queues, backpressure, retries, and recovery

If arrivals outpace the consumer, use a queue to absorb bursts and set a processing limit that protects the sink. Pass stable batch identifiers to tasks. Retry transient failures with a bounded policy. Treat a deterministic data error as a validation or quarantine problem. Replaying a failed batch should produce the same published result.

## Alerts, buffers, and failed deliveries

Use Amazon Simple Notification Service (Amazon SNS) to notify subscribers, and SQS to hold work until a consumer can process it. For an alarm, route the CloudWatch alarm action to SNS and include enough context for the operator to locate the run. A dead-letter queue (DLQ) preserves failed deliveries for diagnosis and controlled replay.

## Service integrations and execution history

For a failed pipeline, determine whether the event reached the target. A rule target DLQ concerns **delivery**. After a workflow starts, use execution history to locate the failed state. Inspect the processing service’s logs for the actual error. A successful delivery does not prove the transformation succeeded.

## Debug task failures in Step Functions and MWAA

In Step Functions, inspect state input, the service integration error, and the retry or catch policy. In Airflow, inspect the DAG run, the task instance logs, and the failed dependency. Rerun the smallest safe unit with the original batch identifier and verify output before marking recovery complete.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| EventBridge rule vs. Step Functions vs. SQS | Use a rule to deliver events, Step Functions for multi-step execution and failure branches, and SQS to hold work for a consumer. |

**Exam cues:** Wait for job completion, fan out an event, filter and enrich a single route, or retry target delivery. Use the stated requirements to decide.

## Try it

A raw data upload starts validation and a Glue transformation. The job can run beyond Express duration. An operator needs a notification if the transformation fails and a separate record if the start event cannot be delivered.

<details>
<summary>Show the reasoning</summary>

Route the arrival event to a Standard Step Functions workflow. Wait for Glue with the run-a-job integration, then publish a notification from the workflow’s failure path. Configure an EventBridge target DLQ for failed delivery and use a stable input identity to protect against duplicate arrivals.

</details>

## AWS documentation

- [EventBridge Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html)
- [EventBridge Scheduler schedule types](https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html)
- [S3 event notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html)
- [Step Functions integration with Glue](https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html)
- [Handling Step Functions errors](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
- [What is Amazon MWAA?](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html)
