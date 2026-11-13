# Choose a database from the access pattern

[Topic index](README.md) · [Home](../README.md)

## The idea

Describe the most important read and write before choosing a data store. Include latency, key distribution, and whether queries are known in advance.

## How to decide

| Concept | When it matters |
|---|---|
| **RDS and Aurora** | Serve transactional workloads that need relational constraints, joins, or an existing SQL engine. |
| **DynamoDB** | Serve predictable key-based access at low latency. Choose partition and sort keys based on actual queries and traffic distribution. |
| **Redshift** | Run analytical aggregations and repeated joins over warehouse tables. |
| **Specialized stores** | Consider OpenSearch for text search and Neptune for graph traversal when that access pattern is central to the workload. |

## Common mistake

DynamoDB throttling can be concentrated on a hot key. Inspect throttling metrics and use Contributor Insights where appropriate to identify frequently accessed or throttled keys.

## Try it

A dashboard analyzes years of measurements, while an API fetches one sample status by a known key.

<details>
<summary>Show the reasoning</summary>

Separate the workloads when their requirements warrant it. Use a key-based store for serving sample status and a warehouse or S3 query layer for historical analytics.

</details>

## AWS documentation

- [AWS documentation · bp partition key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
- [AWS documentation · contributorinsights](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights.html)
- [AWS documentation · Welcome](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
