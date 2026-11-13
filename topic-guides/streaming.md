# Streaming with Kinesis, Firehose, MSK, and Flink

[Topic index](README.md) · [Home](../README.md)

## The idea

A stream keeps events moving while producers and consumers run independently. Start by asking whether you need a replayable source, a delivery service, or a processor.

## How to decide

| Concept | When it matters |
|---|---|
| **Kinesis Data Streams** | Retain events for independent consumers and replay. Records sharing a partition key are routed to the same shard. Plan for duplicates and hot keys. |
| **Amazon Data Firehose** | Buffer records and deliver them to a supported destination such as S3. Use built-in delivery and optional transformations when you mainly need a managed sink. |
| **Amazon MSK** | Use managed Kafka when producers, consumers, or connectors already depend on the Kafka ecosystem. |
| **Managed Service for Apache Flink** | Use stateful event-time windows, joins, or aggregation. A processor reads a stream and maintains computation state. |

## Common mistake

Treat a stream and a delivery destination as separate decisions. Multiple independent consumers can read Kinesis while Firehose writes an archival S3 copy.

## Try it

Instrument events must feed both a live alerting service and an S3 archive. The alerting service needs to reprocess yesterday’s events.

<details>
<summary>Show the reasoning</summary>

Put events in Kinesis Data Streams, size retention for the replay window, and attach an alerting consumer plus Firehose for archival delivery.

</details>

## AWS documentation

- [AWS documentation · introduction](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)
- [AWS documentation · what is this service](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html)
- [AWS documentation · what is](https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html)
