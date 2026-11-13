# Technical catalogs, business catalogs, and Unified Studio

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

A technical catalog resembles a library’s location and format record. A business catalog adds a description of what a dataset means, who owns it, and how teams request access.

| Component | Role |
|---|---|
| AWS Glue Data Catalog | Technical table definitions, schema, locations and partitions for compatible engines |
| Apache Hive metastore | Technical metadata service for compatible compute engines. Glue Data Catalog can serve as a metastore for supported workloads |
| Amazon SageMaker Catalog | Business-facing asset discovery, publication, and access subscription workflows |
| SageMaker Unified Studio domain | Administrative boundary for organized data and AI work |
| Domain unit | Organizational grouping that can delegate responsibilities within a domain |
| Project | Workspace for a team’s members and assets, with permissions scoped to its work |
| Lineage | Trace where a dataset came from and the transformations that produced it |

**Worked example.** A data engineer registers a cleaned table in Glue so Athena can interpret its files. The owner publishes the asset with a description and owner in the business catalog. A different team finds it and requests access through a project. The approved workflow must still arrange effective access to the underlying data.

<details>
<summary>Recall check</summary>

People can find a “monthly returns” dataset, but it is unclear how refunds are counted. Improve business metadata with definitions, ownership, and lineage. A crawler can infer technical structure, but the owner must supply the business meaning.

</details>

[Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html) · [SageMaker Unified Studio](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/what-is-sagemaker-unified-studio.html)
