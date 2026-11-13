# Batch ingestion and database change capture

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Start with what the producer already has. A live database has transaction logs. A file server has directories. A partner may be ready to upload files through an agreed protocol. These are different starting points even when all three land in the same data lake.

## Batch ingestion by source and destination

| Starting point | Use | Why |
|---|---|---|
| Existing database rows plus new writes | AWS Database Migration Service (AWS DMS), full load plus change data capture (CDC) | Copy the initial dataset, then apply changes from the source logs. |
| Existing files on a network file share | AWS DataSync | Schedule, filter, transfer, and verify the selected files. |
| External partner initiates uploads | AWS Transfer Family | Give the partner a managed endpoint such as Secure File Transfer Protocol (SFTP) and scope its landing path. |
| Data in an application with an Amazon AppFlow connector | AppFlow | Configure the connector, object mapping, schedule, and destination. |
| A scheduled export already in Amazon Simple Storage Service (Amazon S3) | AWS Glue for transformation or Redshift COPY for warehouse load | The files are already landed. Choose the next service by whether the job changes the records or loads them into a table. |
| Bulk data constrained by available network capacity | AWS Data Transfer Terminal or a partner offline option. Snowball Edge is no longer available to new customers | Compare the network transfer time with DataSync or Direct Connect first. See [service recognition](service-recognition.md#offline-transfers-and-private-connectivity). |
| Repeated private transfers from a data center | AWS Direct Connect when dedicated connectivity is required | The connection supplies the path. DataSync or another data service still moves the files. |

## Numbers and defaults

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| DMS `MaxFullLoadSubTasks` | 8 by default, configurable up to 49 | Sets parallel tables or segments for full load. Raising it increases resource demand. | [DMS full-load task settings](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.FullLoad.html) |
| DMS `ParallelLoadThreads` | 0 by default. Supported settings depend on the target. | It multiplies full-load parallelism when set. Tune it together with the subtask count. | [DMS full-load task settings](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.FullLoad.html) |
| DMS `TransactionConsistencyTimeout` | 600 seconds by default, configurable | For full load plus CDC, DMS can start loading after this wait even if transactions remain open. A full-load-only task starts immediately. | [DMS full-load task settings](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.FullLoad.html) |
| DataSync Basic mode throughput ceiling per task | 10 Gbps for agent-based transfers or 5 Gbps for transfers without an agent. These quotas are not adjustable. | These are ceilings, not promised speeds. Source and network capacity can lower actual throughput. | [DataSync quotas](https://docs.aws.amazon.com/datasync/latest/userguide/datasync-limits.html) |
| DataSync Enhanced mode manifest | Up to 20 GB per manifest file. This quota is not adjustable. | Split an oversized inventory before running a manifest-based transfer. | [DataSync quotas](https://docs.aws.amazon.com/datasync/latest/userguide/datasync-limits.html) |

## Manifests and incremental loads

A manifest identifies the files a batch should include. It gives the operator a stable input set for validation and retries. Organize landing files by source and batch date, preserve the original bytes, and publish a ready marker or manifest after uploads complete. A consumer that starts from the first file-arrival event can otherwise read an incomplete batch.

For a batch that already exists in S3, assign a batch identifier. Count input files and expected rows, stage the output, and publish a successful status only after validation. Use a key-based merge or replace the affected output partition safely if the batch must be rerun. For DataSync, choose the task mode based on endpoints and transfer size. Use transfer verification and configure destination deletion behavior intentionally before synchronizing.

## Diagnose replication lag

1. Confirm the source and target engines are supported for your migration mode. Configure source logs and retention before starting CDC.
2. Full load seeds target tables. CDC reads logged changes and forwards them to the target. Decide whether to create, truncate, or preserve target tables before running full load.
3. Compare `CDCLatencySource` and `CDCLatencyTarget`. If both rise together, inspect capture and the source first, including long transactions. If target latency rises while source latency is low, inspect the target write path, capacity, and blocking.
4. Before cutover, reconcile row counts and representative records, confirm replication has caught up, and plan how to stop or redirect source writes.

## Common mistake

More replication capacity may not fix an uncommitted source transaction or a target-side lock. Inspect which stage owns the delay before changing task settings. A migration task also needs a separate schema assessment when the database engines differ. See [data modeling and schema conversion](data-modeling.md#compatible-and-breaking-schema-changes).

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| DMS vs. DataSync vs. Transfer Family | Use DMS for database log changes, DataSync for existing files, and Transfer Family when a partner needs an upload endpoint. |

**Exam cues:** Full load plus ongoing changes, verify file copies, or partner-initiated SFTP. Use the stated requirements to decide.

## Try it

A sequencing facility has archived files on a network file share and an active database recording run status. Partners will later upload files using SFTP. The application must stay online during its database migration.

<details>
<summary>Show the reasoning</summary>

Use DataSync to copy the file share, Transfer Family for partner-initiated uploads, and DMS full load plus CDC for the live database. Validate each path independently. If DMS capture is current but application of changes is delayed, inspect the target before increasing source read capacity.

</details>

## AWS documentation

- [DMS ongoing change replication](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html)
- [DMS monitoring metrics](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Monitoring.html)
- [DMS data validation](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Validating.html)
- [DataSync task modes](https://docs.aws.amazon.com/datasync/latest/userguide/choosing-task-mode.html)
- [Transfer Family protocols and storage options](https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html)
- [Amazon AppFlow](https://docs.aws.amazon.com/appflow/latest/userguide/what-is-appflow.html)
- [Snowball Edge availability change](https://docs.aws.amazon.com/snowball/latest/developer-guide/snowball-edge-availability-change.html)
- [AWS Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)

*Last verified against AWS documentation: November 2026.*
