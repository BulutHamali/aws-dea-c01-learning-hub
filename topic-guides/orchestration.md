# Orchestration with EventBridge, Step Functions, and MWAA

[Topic index](README.md) · [Home](../README.md)

## The idea

Orchestration decides what runs next and what happens after failure. Jobs do the processing and events tell the system when work may be needed.

## How to decide

| Concept | When it matters |
|---|---|
| **EventBridge** | Route events that match rules or use EventBridge Scheduler to initiate work at a defined time. |
| **Step Functions** | Model a workflow with states, branching, and explicit retry or catch paths. Start the processing services from the workflow. |
| **AWS Glue Workflows** | Coordinate a Glue-centered chain of triggers, crawlers, and jobs. |
| **Amazon MWAA** | Run Apache Airflow DAGs when your team already uses Airflow operators, schedules, and backfills. |

## Common mistake

S3 event notifications can arrive more than once. Use a stable file identity and make the write path idempotent before adding retries.

## Try it

A new file must trigger validation, a Glue job, and an alert on permanent failure.

<details>
<summary>Show the reasoning</summary>

Route the event to a Step Functions workflow. Keep the execution identity stable for the same logical batch and record processing state in a durable store.

</details>

## AWS documentation

- [AWS documentation · eb what is](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [AWS documentation · welcome](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [AWS documentation · what is mwaa](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html)
