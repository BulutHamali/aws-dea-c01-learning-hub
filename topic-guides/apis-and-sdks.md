# APIs, SDKs, throttling, and resumable ingestion

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Pipelines talk to services through APIs, either a partner's HTTP API or AWS service APIs called from code through a software development kit (SDK). Every API has limits. A good client reads in pages, saves progress only after data is safe, backs off when told to slow down, and can restart without losing or duplicating data.

## API pagination and resumable ingestion

A paginated API returns one page and a token for the next page.

1. Request page 1. Store the records durably, for example as `s3://lab-raw/partner/batch=2026-01-01/page=0001.json`.
2. Only after the write succeeds, save the next-page token to a checkpoint store such as DynamoDB.
3. On restart, read the checkpoint and continue from the saved token.

If the job crashes after writing page 8 but before saving the token, it fetches page 8 again. Because the output key is deterministic, the rewrite replaces the same object instead of creating a duplicate. If the token were saved *before* the write, a crash would skip page 8 forever.

## Throttle signals and bounded retries

| Source | Throttle signal | Response |
|---|---|---|
| Partner HTTP API | HTTP 429, often with a `Retry-After` header | Wait at least `Retry-After`, then retry with capped exponential backoff and jitter |
| Amazon API Gateway (your own API) | HTTP 429 when account, stage, or usage plan limits are exceeded | Clients back off. Raise limits or add a usage plan per client |
| DynamoDB | `ProvisionedThroughputExceededException` or `ThrottlingException` | SDK retries. Fix hot keys or capacity. See [databases](databases.md#throttling-and-hot-keys) |
| Kinesis Data Streams | `ProvisionedThroughputExceededException` on writes or reads | Retry failed records from `PutRecords`, spread partition keys, add shards. See [streaming](streaming.md#fan-in-fan-out-and-throughput) |
| Amazon RDS | Connection limit reached or slow queries | Pool connections with RDS Proxy, cap concurrency, batch writes |
| Any AWS API | `ThrottlingException`, `TooManyRequestsException`, `SlowDown` | Use the SDK's retry modes and lower request rate |

**Backoff with jitter** means wait longer after each failure, with a random spread so many clients don't retry in lockstep. **Bounded** means cap the number of retries and send what still fails to a dead-letter queue for review.

## AWS SDK clients, pagination, and errors

Use the AWS SDK for Python (Boto3) or another SDK to call AWS from code.

```python
import boto3
from botocore.config import Config

s3 = boto3.client("s3", config=Config(retries={"mode": "standard"}))
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket="lab-raw", Prefix="runs/2026-01-01/"):
    for obj in page.get("Contents", []):
        print(obj["Key"], obj["Size"])

glue = boto3.client("glue")
run = glue.start_job_run(JobName="curate-runs", Arguments={"--run_date": "2026-01-01"})
```

| SDK feature | Why it matters |
|---|---|
| Paginators | List calls return limited results per page. Paginators fetch every page for you |
| Waiters | Poll until a resource reaches a state, such as a table becoming active |
| Retry modes | Standard mode retries with exponential backoff and jitter. Adaptive mode adds a client-side rate limiter for a single heavily throttled resource |
| Credentials | Let the SDK use the execution role. Never hard-code keys |
| Error codes | Catch the service error code, such as `EntityNotFoundException`, and decide whether a retry can help |

## API timeouts, pagination, authentication, and checkpoints

Keeping a partner API client healthy over months:

- Set connect and read timeouts so a hung call fails instead of blocking the job.
- Store API keys or OAuth client secrets in Secrets Manager and rotate them.
- Log the request ID, page token, and response status for every page.
- Alert when the record count per run drops sharply or the API schema changes.
- Watch for token expiry in long runs and refresh before it expires.

For SaaS sources with a supported connector, such as Salesforce, Amazon AppFlow avoids writing the client at all. See [data movement](data-movement.md).

## API Gateway, Lambda, and DynamoDB serving

To make curated data available to other systems through an API:

| Requirement | Design |
|---|---|
| Low-latency lookups by key | API Gateway → Lambda → DynamoDB |
| SQL-style queries over a warehouse | Redshift Data API, called from Lambda behind API Gateway |
| Bulk datasets for other teams | Share the S3 location or a Redshift datashare instead of an API |
| Rate limits per consumer | API Gateway usage plans with API keys |
| Fewer moving parts for direct reads | API Gateway direct service integration with DynamoDB |

The Redshift Data API runs SQL over HTTPS without managing database connections, which suits Lambda.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| API Gateway throttle response | HTTP 429 Too Many Requests | Clients must treat 429 as "slow down", not as a failure | [API Gateway throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html) |
| Usage plan limits | Per-client throttles cannot exceed the account limits | A usage plan divides capacity, it does not add any | [API Gateway throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html) |
| SDK retry modes | Standard (backoff with jitter), adaptive (adds client-side rate limiting), legacy | Pick adaptive only for one heavily throttled resource | [SDK retry behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html) |

## Common mistake

Retrying every 429 immediately in a tight loop. That makes throttling worse and can get the client blocked. Honor `Retry-After` and back off.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Write first, then checkpoint vs. checkpoint first | No data loss vs. possible lost pages |
| Standard vs. adaptive retry mode | General default vs. one resource that throttles often |
| AppFlow vs. custom API client | Supported SaaS connector vs. any other API |
| Redshift Data API vs. JDBC | HTTPS calls without connections vs. persistent drivers |

**Exam cues:** "HTTP 429" → backoff with jitter and `Retry-After`. "Crash between pages" → deterministic output key and checkpoint after write. "Expose data to partners with rate limits" → API Gateway with usage plans.

## Try it

A partner API allows 40 requests per second and returns 429 with `Retry-After`. A Lambda pipeline crashed after writing page 120 but before saving its next token.

<details>
<summary>Show the reasoning</summary>

On restart, resume from the last saved token, which re-fetches page 120 and overwrites the same deterministic S3 key. Throttle the client below 40 requests per second, honor `Retry-After`, and retry with capped exponential backoff and jitter. Save the token only after each page write succeeds.

</details>

## AWS documentation

- [Boto3 paginators](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html)
- [SDK retry behavior](https://docs.aws.amazon.com/sdkref/latest/guide/feature-retry-behavior.html)
- [API Gateway throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
- [Redshift Data API](https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html)

*Last verified against AWS documentation: November 2026.*
