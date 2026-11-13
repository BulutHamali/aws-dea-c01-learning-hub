# Streaming with Kinesis, Firehose, MSK, and Flink

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Think of a stream as a recording that several viewers can rewind independently. Producers append events while consumers keep their own place. Amazon Kinesis Data Streams is the recording. Amazon Data Firehose delivers copies to a destination, and Apache Flink computes results across the events.

## Consumer integrations and source selection

| Need | Use | Design consequence |
|---|---|---|
| Independent readers and replay | Kinesis Data Streams | Each consumer maintains progress. Size retention for the recovery window. |
| Managed delivery to Amazon Simple Storage Service (Amazon S3) | Amazon Data Firehose | Delivery is buffered. Check destination-specific behavior before promising low latency. |
| Existing Kafka producers, connectors, and consumer groups | Amazon Managed Streaming for Apache Kafka (Amazon MSK) | Preserve the Kafka interface and offset model. |
| React to DynamoDB item changes | DynamoDB Streams with a Lambda event source mapping | The source is the table’s change feed. Use the item identity and sequence in downstream processing. |
| Short per-event validation | [AWS Lambda](lambda.md#read-a-kinesis-stream-with-lambda) | Keep writes safe to repeat and configure failed-record handling. |
| Event-time joins and windows | Amazon Managed Service for Apache Flink | Keep state across events. Define how late events affect published results. |

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Provisioned shard sustained write capacity | Up to 1 MB/s or 1,000 records/s per shard, whichever binds first | Size for both record count and bytes. This is sustained capacity. Kinesis documents burst capacity for intermittent large records separately. | [Kinesis quotas](https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html) |
| Shared read bandwidth | Up to 2 MB/s per shard across shared readers | Another consumer can slow a reader on the same shard. | [Enhanced fan-out](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html) |
| Enhanced fan-out bandwidth | Up to 2 MB/s per shard for each registered consumer | Give a latency-sensitive reader independent bandwidth. | [Enhanced fan-out](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html) |
| Stream retention | 24 hours by default, configurable up to 365 days | An expired record cannot be replayed from this stream. | [Kinesis record retention](https://docs.aws.amazon.com/streams/latest/dev/kinesis-extended-retention.html) |
| New on-demand stream baseline | 4 MB/s writes and 8 MB/s reads by default. Scaling ceilings vary by Region. | Use on-demand when traffic is variable and confirm the Region’s limits. | [Kinesis quotas](https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html) |
| Firehose buffering hints | Generic API defaults are 300 seconds and 5 MiB. Check the destination-specific configuration. | These are configurable hints. They are not an end-to-end delivery guarantee. | [Firehose BufferingHints](https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html) |

## Fan-in, fan-out, and throughput

**Fan-in** combines several producers into one stream. **Fan-out** lets independent consumers read the same events. Use a partition key that distributes traffic while preserving the ordering your application needs. Kinesis routes records with the same key together. Splitting a hot instrument key can distribute load, but changes the ordering boundary. Resharding alone leaves a single hot key concentrated.

Suppose the lab produces 2,400 events/s and 1.8 MB/s across evenly distributed keys. Divide each load by the sustained per-shard limit above and round up. The record rate needs three shards and the byte rate needs two. Start with three as the theoretical minimum, then allow room for traffic spikes and uneven keys. If one key alone exceeds a shard’s sustained write capacity, revisit the key or rate-limit that producer.

Check write throttles first if events never enter the stream. With `PutRecords`, inspect individual results and retry failed records with bounded backoff and jitter. Use stable event IDs downstream because uncertain retries can duplicate an event. If the records are already in the stream and a reader is falling behind, compare lag, read contention, consumer processing duration, and sink latency. Enhanced fan-out addresses shared reads. A slow database needs a database-side fix or a bounded consumer.

## Retention, checkpoints, and replay

Retention determines how far back data is available. A checkpoint determines where a consumer resumes. An archive is a separate source for data older than stream retention. On recovery, choose the starting position, confirm the records are still retained, and replay into an idempotent sink or an isolated output. Starting from an earlier position may repeat already published events. In Kafka, use consumer-group offsets and check broker retention before resetting an offset.

## Event-time state and stateless transforms

A stateless transform renames a field using the current record alone. A stateful calculation keeps information across records, such as the count of alerts per instrument within an event-time window. Event time comes from the record. Processing time comes from the consumer. Delays can make these disagree. When late readings matter, define the window, how long to wait for late arrivals, and whether you will update a previous result.

## Common mistake

Firehose delivery and replay solve different requirements. Feed Firehose from Kinesis when the archive needs managed delivery and another application needs its own replay position.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Kinesis vs. Firehose vs. MSK | Use Kinesis for AWS-native replay, Firehose for managed buffered delivery, and MSK for Kafka compatibility. |

**Exam cues:** Independent replay, retained records, dedicated consumer bandwidth, or existing Kafka clients. Use the stated requirements to decide.

## Try it

The lab writes telemetry to a stream and archives it in S3. The alerting reader falls behind during a daily spike. Its sink is healthy, but shared read capacity is exhausted. Recovery requires replay after a two-day outage.

<details>
<summary>Show the reasoning</summary>

Keep Kinesis Data Streams for replay. Configure retention beyond two days, register the alerting reader for enhanced fan-out, and keep Firehose for delivery. Verify that lag falls and that rerunning a retained interval does not duplicate alerts.

</details>

## AWS documentation

- [Kinesis Data Streams concepts](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html)
- [Kinesis PutRecords request and response](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecords.html)
- [What is Amazon Data Firehose?](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html)
- [What is Managed Service for Apache Flink?](https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html)
