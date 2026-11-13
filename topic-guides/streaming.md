# Streaming with Kinesis, Firehose, MSK, and Flink

[Topic index](README.md) · [Home](../README.md)

## The idea

Think of Kinesis as a DVR that several viewers can rewind independently. Firehose behaves like a delivery truck that leaves when a buffer fills or a delivery timer expires. Flink is the analyst counting events over time.

A stream keeps events moving while producers and consumers run independently. Start by asking whether you need a replayable source, a delivery service, or a processor.

## How to decide

| Concept | When it matters |
|---|---|
| **Kinesis Data Streams** | Retain events for independent consumers and replay. Records sharing a partition key are routed to the same shard. Plan for duplicates and hot keys. |
| **DynamoDB Streams** | Consume changes to items in a DynamoDB table. Use a suitable consumer such as Lambda to react to updates. |
| **Amazon Data Firehose** | Buffer records and deliver them to a supported destination such as S3. Use built-in delivery and optional transformations when you mainly need a managed sink. |
| **Amazon MSK** | Use managed Kafka when producers, consumers, or connectors already depend on the Kafka ecosystem. |
| **Managed Service for Apache Flink** | Use stateful event-time windows, joins, or aggregation. A processor reads a stream and maintains computation state. |

## Ordering, fan-out, and lag

Kinesis uses the partition key to route records. If one device produces most of the traffic, using device ID as the key can concentrate load on a shard. Consider whether the application needs the original ordering before spreading one key across multiple keys.

With shared-throughput consumers, readers share shard read capacity. Enhanced fan-out gives registered Kinesis consumers dedicated read throughput per shard. If one application still lags, check its processing time and downstream writes. More read throughput cannot fix a slow sink.

A Flink window uses state to compute results over several events. A stateless field rename can handle each event independently. For late events, define whether the pipeline accepts them, updates results, or sends them to a separate path.

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
