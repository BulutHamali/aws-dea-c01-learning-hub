# Choose a data store from the access pattern

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Before naming a database, write down the most important read and the most important write. Include the latency target, how evenly the keys spread, and whether the queries are known in advance. The access pattern picks the store. The brand name of the store comes last.

## Cost, latency, and operational trade-offs

| Access pattern | First choice | Why |
|---|---|---|
| Transactions with joins, constraints, and an existing SQL engine | Amazon RDS or Amazon Aurora | Relational integrity. Aurora adds storage that grows automatically and fast replicas |
| Known key lookups at any scale with single-digit millisecond latency | Amazon DynamoDB | No servers to manage. Performance depends on key design |
| Microsecond reads from a durable in-memory primary database | Amazon MemoryDB | Stores data in memory with a Multi-AZ transaction log, compatible with Valkey and Redis OSS |
| A cache in front of another database | Amazon ElastiCache | Speeds reads. The source of truth stays elsewhere |
| Aggregations and joins over years of history | Amazon Redshift, or Athena over S3 | Columnar storage for scans, not single-row lookups |
| Full-text search and log analytics | Amazon OpenSearch Service | Inverted indexes and relevance scoring. Also supports vector search |
| Relationship traversal such as "samples linked to the same donor" | Amazon Neptune | Graph queries |
| JSON documents with a MongoDB-compatible API | Amazon DocumentDB | Keeps existing MongoDB drivers and queries |
| Wide-column workloads already written for Apache Cassandra | Amazon Keyspaces | Serverless and Cassandra Query Language (CQL) compatible |

Mixing workloads in one store usually fails. If a dashboard scans years of data while an API fetches one sample status by key, serve the API from DynamoDB and the dashboard from Redshift or Athena.

## Keys, indexes, and warehouse layout

**DynamoDB** stores items in partitions chosen by a hash of the partition key. The sort key orders items within one partition key.

- Design keys from the queries. `PK = DEVICE#123`, `SK = READING#2026-04-01T10:00` returns recent readings for one device with one `Query`.
- A **global secondary index (GSI)** supports a different access pattern with its own keys. It is eventually consistent and can be added anytime.
- A **local secondary index (LSI)** keeps the same partition key with a different sort key. It must be created with the table.
- A **hot key** receives far more traffic than others. Spread it by adding a suffix (write sharding) or by redesigning the key. Use CloudWatch Contributor Insights to find which keys are hot.

For **Redshift**, choose distribution and sort keys from join and filter patterns. See [Redshift table design](redshift.md#table-design-distribution-and-sort-keys).

## MemoryDB, ElastiCache, DynamoDB, and vector stores

| Requirement | Choose | Reason |
|---|---|---|
| Fastest key/value reads, and the data must survive node failure | MemoryDB | Durable primary database with microsecond reads |
| Reduce load on an existing database by caching hot results | ElastiCache | A cache can be rebuilt from the source |
| Key/value at large scale with less focus on microsecond latency | DynamoDB | Managed scaling with single-digit millisecond responses |
| Similarity search over embeddings near relational data | Aurora PostgreSQL with pgvector and an HNSW index | Keeps vectors next to the rows they describe |
| Similarity search plus keyword search at scale | OpenSearch Service | Hybrid keyword and vector retrieval |

See [vectors and LLMs](vectors-and-llms.md) for index types.

## Time to Live and recovery

DynamoDB **Time to Live (TTL)** deletes an item after the epoch timestamp in a chosen attribute passes.

- Deletion happens typically within a few days, not at the exact second. Filter expired items out of reads.
- TTL deletes do not consume write capacity in the table's Region.
- TTL deletes appear in DynamoDB Streams marked as service deletions, so a consumer can archive them to S3.
- Point-in-time recovery restores the table to any second in the recovery window, as a new table.

## Throttling and hot keys

Throttling means a request was rejected because a limit was hit. In DynamoDB, the response is a `ProvisionedThroughputExceededException` or `ThrottlingException`. The AWS SDKs retry with exponential backoff, but retries do not fix a hot key. Check which limit applies:

- **Table limit:** raise provisioned capacity or use on-demand mode.
- **Partition limit:** one key receives more than a partition can serve. Spread the key.

For RDS, the limit is often connections. Cap Lambda concurrency or use Amazon RDS Proxy to pool connections.

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| DynamoDB per-partition capacity | 3,000 read units and 1,000 write units per second | A single hot key cannot exceed this, whatever the table setting | [Partition key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) |
| Read and write unit sizes | 1 read unit = one strongly consistent read of up to 4 KB per second. 1 write unit = one write of up to 1 KB per second | Large items consume several units per request | [Partition key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) |
| Secondary indexes per table | 20 GSIs (default, adjustable) and 5 LSIs | LSIs must be planned at table creation | [DynamoDB quotas](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html) |
| Maximum item size | 400 KB including attribute names | Store large payloads in S3 and keep a pointer in DynamoDB | [Large items and attributes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-use-s3-too.html) |
| TTL deletion timing | Typically within a few days of expiry | Do not rely on TTL for exact-time deletion | [How TTL works](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/howitworks-ttl.html) |
| MemoryDB latency | Microsecond reads, single-digit millisecond writes | Separates MemoryDB from DynamoDB in latency-driven stems | [What is MemoryDB](https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html) |

## Common mistake

Adding a GSI to make a hot key cooler. The GSI has its own partitions and its own hot-key problem if it uses the same skewed value.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| MemoryDB vs. ElastiCache | Durable primary database vs. disposable cache |
| DynamoDB vs. MemoryDB | Millisecond managed scale vs. microsecond in-memory reads |
| GSI vs. LSI | New partition key anytime vs. same partition key, defined at creation |
| DocumentDB vs. DynamoDB | MongoDB compatibility vs. native key-value design |
| Keyspaces vs. DynamoDB | Existing Cassandra code vs. new key-value design |

**Exam cues:** "Microsecond" and "durable" → MemoryDB. "MongoDB drivers" → DocumentDB. "Cassandra" → Keyspaces. "Graph" or "relationships" → Neptune. "Hot partition" → key redesign or write sharding.

## Try it

An instrument status API reads one record by sample ID at very high request rates and needs microsecond responses. The records must survive node failures. A nightly job also compares status history across years.

<details>
<summary>Show the reasoning</summary>

Serve the API from MemoryDB because it is a durable, in-memory primary database. Archive status changes to S3 and query history with Athena or Redshift. A cache alone would not meet the durability requirement.

</details>

## AWS documentation

- [DynamoDB partition key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
- [DynamoDB Time to Live](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/howitworks-ttl.html)
- [CloudWatch Contributor Insights for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights.html)
- [What is Amazon MemoryDB?](https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html)
- [What is Amazon RDS?](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)

*Last verified against AWS documentation: November 2026.*
