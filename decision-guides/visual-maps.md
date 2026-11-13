# Visual decision maps

[Home](../README.md) · [Service decisions](README.md)

## Choose the ingestion layer

```mermaid
flowchart TD
    A["What is arriving?"] --> B["Database changes"]
    A --> C["Continuous events"]
    A --> D["Existing files"]
    B --> E["DMS full load and CDC"]
    C --> F{"Independent readers or replay?"}
    F -->|Yes| G["Kinesis Data Streams or MSK"]
    F -->|Delivery only| H["Data Firehose"]
    D -->|Storage migration| I["DataSync"]
    D -->|Partner SFTP uploads| J["Transfer Family"]
```

An existing stream can feed Firehose and a stateful processor at the same time. Use [streaming](../topic-guides/streaming.md) and [data movement](../topic-guides/data-movement.md) to compare the edges of each choice.

## Diagnose a missing partition

```mermaid
flowchart TD
    A{"Did the source object arrive?"} -->|No| B["Investigate the producer"]
    A -->|Yes| C{"Did the job publish curated files?"}
    C -->|No| D["Check run logs and quality rejects"]
    C -->|Yes| E{"Does the table point to the right path?"}
    E -->|No| F["Repair catalog or projection settings"]
    E -->|Yes| G["Check filters, grants, and dashboard refresh"]
```

Trace one missing day or batch all the way through. [Monitoring guide](../topic-guides/monitoring.md)

## Trace access to a governed table

```mermaid
flowchart TD
    A["Analyst assumes an IAM role"] --> B["Query engine checks API permissions"]
    B --> C["Lake Formation checks table grants"]
    C --> D["Engine reads the authorized S3 data"]
    D --> E["Key policy permits applicable KMS use"]
    B --> F["Engine writes query results to S3"]
```

The exact credential and key path depends on the service integration. Test the analyst role and verify that direct reads of the raw objects follow the intended policy. [IAM guide](../topic-guides/security.md) · [Governance guide](../topic-guides/governance.md)
