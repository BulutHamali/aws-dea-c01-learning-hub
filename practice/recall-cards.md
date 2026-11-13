# Recall cards

[Home](../README.md) · [Study method](../learning-paths/study-method.md)

Cover the right column. Say the answer aloud and give an example. Mark guesses and return to those cards later.

| Prompt | Answer to check |
|---|---|
| Which tool changes the rows and which discovers the table definition? | Glue ETL changes rows. A crawler discovers metadata for the Glue Data Catalog |
| Why can resetting a Glue bookmark create duplicates? | It can reread earlier inputs. The destination still contains previous output |
| What state helps a Glue streaming job resume? | The streaming checkpoint tracks progress |
| What separates Kinesis from Firehose? | Kinesis Data Streams retains records for consumers to read or replay. Firehose delivers records to a destination |
| Why use a Flink window? | It groups events over time for a stateful calculation such as a rolling count |
| EventBridge, SQS, or Step Functions? | EventBridge routes or schedules. SQS buffers. Step Functions runs a workflow with explicit states |
| What makes a stream’s hot shard possible? | Uneven keys can route disproportionate traffic to one shard |
| Which store for order transactions, device lookups, and historical reporting? | RDS/Aurora for relational transactions, DynamoDB for key-based lookups, Redshift for analytical warehouse queries |
| What do partitioning and Parquet save separately? | Partition filters can skip groups of files. Columnar reads can skip unneeded columns |
| What does Iceberg add? | Table-level metadata, snapshots, and supported evolution or updates over the data files |
| What is the first sentence to say when modeling a fact table? | “One row represents …” State its grain before choosing keys |
| Glue Data Catalog versus SageMaker Catalog? | Technical schema and location versus business-facing discovery, ownership, and access workflow |
| When do Athena, Spectrum, and federated queries fit? | Athena for direct lake queries, Spectrum for Redshift SQL over S3, federation for supported remote operational sources |
| COPY, UNLOAD, or MERGE? | COPY loads into Redshift, UNLOAD exports results to S3, MERGE applies staged changes by key |
| Where do you look for a malformed Redshift COPY field? | SYS_LOAD_ERROR_DETAIL |
| What’s the difference between lag and freshness? | Lag is the backlog or delay in consumption. Freshness is how current the usable output is |
| Who ran GetObject, why did a job fail, and what resource configuration changed? | CloudTrail data events, application logs in CloudWatch, and AWS Config history respectively |
| Why can an S3 read fail even after GetObject is allowed? | The caller may lack key permissions for SSE-KMS, or another policy layer can deny the request |
| Lake Formation, KMS, or Macie? | Lake Formation governs supported data access, KMS controls key usage, and Macie discovers sensitive S3 data |
| What problem do HNSW and IVF solve? | Approximate similarity search over vectors. HNSW navigates a graph and IVF narrows search to selected clusters |
