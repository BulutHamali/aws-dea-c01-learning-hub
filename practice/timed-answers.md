# Timed practice answers

[Question set](timed-set.md) · [Exam map](../EXAM-MAP.md#task-by-task-study-map)

Give yourself one point for a fully correct response. For Choose TWO, both selections must match. Count guesses as review items even if you chose correctly. Record the task number and your reasoning in the [progress tracker](../CHECKLIST.md).

| Domain | Questions | Score |
|---|---:|---:|
| 1 · Ingestion and transformation | 11 | / 11 |
| 2 · Data store management | 8 | / 8 |
| 3 · Operations and support | 7 | / 7 |
| 4 · Security and governance | 6 | / 6 |

## Question 1 · B

Task 1.1. Replay is the deciding requirement. [Review the guide](../topic-guides/streaming.md)

- **A.** It delivers to supported destinations and does not supply independent stream offsets.
- **B.** Independent consumers can reread retained records within the configured window.
- **C.** Consumers compete for messages in the same queue.
- **D.** This handles fan-out, but a consumer cannot rewind messages it already deleted.

## Question 2 · D

Task 2.1. Keep archived files external while querying from Redshift. [Review the guide](../topic-guides/redshift.md)

- **A.** This materializes them as warehouse data.
- **B.** Federation targets supported remote operational databases.
- **C.** Athena can query the archive but this design does not give Redshift a local-to-external SQL join.
- **D.** External tables support SQL on S3 from Redshift.

## Question 3 · C

Task 3.2. Use a window to calculate across rows while preserving their grain. [Review the guide](../topic-guides/analysis-and-data-prep.md)

- **A.** This collapses each sensor into a single row.
- **B.** This mixes sensors and loses the moving window.
- **C.** This calculates the rolling average for each sensor without collapsing rows.
- **D.** This removes the detail rows instead of averaging them.

## Question 4 · D

Task 4.1. A timeout points toward the network path. [Review the guide](../topic-guides/security.md)

- **A.** That does not open the database path.
- **B.** Object layout is unrelated to JDBC connectivity.
- **C.** This overlooks the reported timeout and verified credentials.
- **D.** These determine whether the job can reach the private endpoint.

## Question 5 · A, C

Task 1.1. Control the retry rate and make the sink safe to replay. [Review the guide](../topic-guides/pipeline-engineering.md)

- **A.** This reduces synchronized retries and respects the provider’s signal.
- **B.** Immediate retries can worsen throttling.
- **C.** A retry can reread a page without creating an extra output.
- **D.** A crash can lose data.
- **E.** This creates gaps.

## Question 6 · B

Task 2.1. The requirement names approximate nearest-neighbor search with a graph. [Review the guide](../topic-guides/vectors-and-llms.md)

- **A.** It may filter data but does not create a vector graph.
- **B.** HNSW uses a graph and gives tunable search trade-offs.
- **C.** It does not find nearby values.
- **D.** IVF narrows search by clusters.

## Question 7 · A

Task 3.1. The requirement is interactive profiling and preparation. [Review the guide](../topic-guides/analysis-and-data-prep.md)

- **A.** Profiles show characteristics and recipes capture transformations.
- **B.** A crawler discovers metadata.
- **C.** A lifecycle rule does not rewrite fields.
- **D.** It can perform these operations, but it misses the stated visual, no-code workflow.

## Question 8 · B, C

Task 4.2. Enforce the table policy and close the alternate access path. [Review the guide](../topic-guides/governance.md)

- **A.** It expands the alternate path.
- **B.** A supported query engine can enforce the grants.
- **C.** This prevents the role from bypassing the table restriction via S3.
- **D.** That conflicts with least privilege.
- **E.** Versioning preserves history.

## Question 9 · D

Task 1.1. The input is a live database change log. [Review the guide](../topic-guides/data-movement.md)

- **A.** Copying files does not provide supported logical CDC.
- **B.** Crawlers discover metadata.
- **C.** Full exports do not provide the requested continuous capture.
- **D.** It covers the initial copy and ongoing database changes for supported endpoints.

## Question 10 · A

Task 2.1. Versioned table metadata is central. [Review the guide](../topic-guides/iceberg.md)

- **A.** It supports table snapshots and compatible row-level operations.
- **B.** Parquet is suitable storage, but the conventional table does not maintain committed snapshots or row-level changes.
- **C.** Transitions do not maintain committed table states.
- **D.** Discovery does not supply snapshots.

## Question 11 · D

Task 3.1. Keep the existing orchestration model. [Review the guide](../topic-guides/orchestration.md)

- **A.** Subscriptions do not represent dependencies and backfills.
- **B.** It is unrelated to workflow execution.
- **C.** The catalog stores data metadata.
- **D.** It provides managed Apache Airflow.

## Question 12 · C

Task 4.3. Both accounts’ KMS authorization matter. [Review the guide](../topic-guides/security.md)

- **A.** Listing does not authorize decrypt.
- **B.** Transport changes cannot fix key authorization.
- **C.** This addresses authorization for the specific key and caller.
- **D.** The failure occurs in KMS.

## Question 13 · A

Task 1.2. The workload calls for distributed transformation. [Review the guide](../topic-guides/glue.md)

- **A.** It can distribute joins and write the validated output layout.
- **B.** It does not rewrite data.
- **C.** One function is a poor fit for the stated workload.
- **D.** Firehose can convert supported stream records, but it does not run the distributed joins across these existing daily files.

## Question 14 · C

Task 2.2. Athena can calculate partition paths. [Review the guide](../topic-guides/catalog.md)

- **A.** Event schemas do not manage Athena partitions.
- **B.** Bookmarks track job progress.
- **C.** Athena derives locations from the rules.
- **D.** A crawler can discover dates, but this design still registers the partitions.

## Question 15 · A, D

Task 3.2. Reduce both the set of files and the columns read. [Review the guide](../topic-guides/file-layout.md)

- **A.** Athena can prune unrelated partition paths.
- **B.** High cardinality can create many tiny partitions.
- **C.** That increases data accessed.
- **D.** Compatible scans can read selected columns.
- **E.** Copies do not reduce the bytes the query reads.

## Question 16 · A

Task 4.3. The display depends on the querying role. [Review the guide](../topic-guides/privacy-and-audit.md)

- **A.** It changes what authorized queries reveal.
- **B.** The privileged role would lose the full values.
- **C.** Authorized decryption does not mask columns.
- **D.** Retention controls deletion.

## Question 17 · C

Task 1.2. The team needs node-level control. [Review the guide](../topic-guides/emr.md)

- **A.** It only discovers metadata.
- **B.** It abstracts the worker fleet.
- **C.** This gives control over cluster setup and nodes.
- **D.** Dependency packaging does not give you control to install a daemon on the underlying worker nodes.

## Question 18 · D

Task 2.2. The requirement includes business context and subscriptions. [Review the guide](../topic-guides/catalog-and-unified-studio.md)

- **A.** It updates technical metadata.
- **B.** It searches application logs.
- **C.** It handles object retention and transitions.
- **D.** This supports discovery and access requests with business context.

## Question 19 · C

Task 3.3. Use a diagnostic view specific to load errors. [Review the guide](../topic-guides/monitoring.md)

- **A.** It can show status and timing but is not the dedicated view for per-file and per-column COPY details.
- **B.** The plan is useful for performance analysis, but it does not identify the malformed field in a COPY input file.
- **C.** It exposes load-error fields including filename and column.
- **D.** Ownership does not show the conversion error.

## Question 20 · D

Task 4.4. This is an object-level API action. [Review the guide](../topic-guides/privacy-and-audit.md)

- **A.** It tracks input progress.
- **B.** It does not identify an object reader.
- **C.** It tracks spend.
- **D.** It records object-level activity when enabled.

## Question 21 · D

Task 1.2. Treat model output as input requiring validation. [Review the guide](../topic-guides/vectors-and-llms.md)

- **A.** A valid structure can still contain incorrect values.
- **B.** Encryption does not affect extraction quality.
- **C.** Indexing does not validate the extraction contract.
- **D.** This manages errors and measures quality.

## Question 22 · A

Task 2.3. The data flows from Redshift to S3. [Review the guide](../topic-guides/redshift.md)

- **A.** It exports query results to S3.
- **B.** It loads from supported sources into Redshift.
- **C.** It applies staged changes to a target table.
- **D.** It performs table maintenance.

## Question 23 · B

Task 3.3. Trace one known batch from arrival to consumption. [Review the guide](../topic-guides/monitoring.md)

- **A.** There is no evidence that compute caused the problem.
- **B.** This isolates where the date was lost.
- **C.** That changes recovery state before identifying the cause.
- **D.** It does not diagnose the stale date.

## Question 24 · B, E

Task 4.5. Identify sensitive data and enforce the approved storage locations. [Review the guide](../topic-guides/privacy-and-audit.md)

- **A.** This can copy data to disallowed Regions.
- **B.** The findings guide investigation and classification.
- **C.** A bookmark tracks job input progress.
- **D.** Encryption protects data at rest, but it does not enforce the locations of replicas or backups.
- **E.** This addresses where durable copies can land.

## Question 25 · B

Task 1.3. Separate event routing from execution state. [Review the guide](../topic-guides/orchestration.md)

- **A.** Routing events does not model all workflow branches.
- **B.** The workflow can run the steps, retry, and handle failures.
- **C.** A notification topic does not track workflow state.
- **D.** This starts one job, while the requested design needs an explicit validation step and workflow-level failure handling.

## Question 26 · B, E

Task 2.3. Protect old versions and manage their lifecycle separately. [Review the guide](../topic-guides/s3.md)

- **A.** This defeats the recovery requirement.
- **B.** It keeps versions that can support recovery.
- **C.** It addresses transfer paths.
- **D.** It does not retain earlier versions.
- **E.** It can transition older versions based on the configured policy.

## Question 27 · A

Task 3.4. The sampling design should represent small groups. [Review the guide](../topic-guides/data-quality.md)

- **A.** This avoids letting the largest supplier dominate every sample.
- **B.** That leaves the known gap.
- **C.** Compression does not select records.
- **D.** This removes the field needed to stratify.

## Question 28 · A

Task 1.3. Each consumer needs a separate delivery path. [Review the guide](../topic-guides/pipeline-engineering.md)

- **A.** Each subscriber has its own buffer and acknowledgment state.
- **B.** Messages can be processed by either consumer rather than both.
- **C.** This provides fan-out, but it does not give the outage-prone consumer its own SQS backlog and redrive controls.
- **D.** A crawler is a metadata tool.

## Question 29 · B

Task 2.4. Put related readings together with a sortable timestamp. [Review the guide](../topic-guides/databases.md)

- **A.** The device query cannot target one key.
- **B.** This groups a device’s readings and supports ordered range queries.
- **C.** The device query would require a scan.
- **D.** The request knows the device, not the value.

## Question 30 · B, D

Task 1.4. Isolate the failed item and protect successful writes. [Review the guide](../topic-guides/pipeline-engineering.md)

- **A.** All messages can become eligible for retry.
- **B.** The function can identify which records need a retry.
- **C.** This loses the failed input and evidence.
- **D.** Duplicate delivery or a retry does not duplicate results.
- **E.** Memory does not fix invalid data.

## Question 31 · C

Task 1.4. Put infrastructure and validation in version control. [Review the guide](../topic-guides/pipeline-engineering.md)

- **A.** This records output but cannot reproduce resources.
- **B.** Screenshots do not apply the configuration.
- **C.** The deployment is repeatable and changes can be reviewed.
- **D.** The original drift remains.

## Question 32 · A, E

Task 1.4. Capacity caps and pre-initialization serve different needs. [Review the guide](../topic-guides/pipeline-engineering.md)

- **A.** Reserved concurrency sets a function-level ceiling.
- **B.** Disk capacity does not cap invocations.
- **C.** Credentials do not control concurrency.
- **D.** Longer timeouts do not set the concurrency limit.
- **E.** It pre-initializes execution environments.
