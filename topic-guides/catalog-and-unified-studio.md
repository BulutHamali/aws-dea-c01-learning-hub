# Technical catalogs, business catalogs, and SageMaker Unified Studio

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

A library has two kinds of records. The shelf record says where a book is and what format it is in. The reader's guide says what the book is about, who wrote it, and how to borrow it. In AWS, the **technical catalog** (Glue Data Catalog) is the shelf record for query engines. The **business catalog** (Amazon SageMaker Catalog) is the reader's guide for people.

## Glue Data Catalog and Hive metastore

| Component | Role |
|---|---|
| AWS Glue Data Catalog | Technical table definitions: location, schema, format, partitions. Used by Athena, Redshift Spectrum, EMR, and Glue |
| Apache Hive metastore | The open-source equivalent. EMR can use the Glue Data Catalog as its Hive metastore so engines share one catalog |
| Amazon SageMaker Catalog | Business metadata, glossary terms, ownership, discovery, and access requests |

See [catalog](catalog.md) for crawlers and partitions.

## SageMaker Unified Studio terms

**SageMaker Unified Studio** is a single workspace for data and AI work. SageMaker Catalog is built in. The exam guide names these pieces:

| Term | Meaning |
|---|---|
| Domain | The top-level organizing entity that connects assets, users, and projects. One per enterprise or one per business unit |
| Domain unit | A grouping inside a domain for a business unit or team. Domain unit owners receive delegated authority to set policies |
| Authorization policies | Set on domain units. Control who can create domain units and projects, join projects, or create glossaries and metadata forms |
| Project profile | A template for projects, made of blueprints |
| Blueprint | Defines which tools a project can use, such as a lakehouse database or EMR Serverless |
| Project | A workspace and permission boundary for a team's code, queries, notebooks, and data |
| Asset | A table, view, dashboard, or file registered in the catalog |
| Business glossary | Shared business terms, such as "Read count: the number of sequencing reads passing filter" |
| Metadata form | Required fields a publisher fills in, such as owner, sensitivity, and refresh schedule |

## Domains, domain units, and projects

A lab organization sets up one domain. It creates domain units for `Sequencing`, `Clinical`, and `Analytics`. The `Sequencing` domain unit owner allows only members of that unit to create projects with the lakehouse project profile. Each team works inside its own project, which keeps its data and permissions separate.

## Publish an asset and approve subscriptions

1. A producer project brings a Glue table into its **inventory**.
2. The owner adds a description, glossary terms, and metadata form values, then **publishes** the asset to the catalog.
3. A consumer in another project searches, finds the asset, and submits a **subscription request** with a reason.
4. The producer **approves** or rejects it.

## Project subscriptions and fulfillment

When a subscription to a managed Glue Data Catalog asset is approved, SageMaker Unified Studio grants access through AWS Lake Formation on the producer's behalf. The table then appears in the subscriber project's catalog, and members query it with Athena, Redshift, or Spark. Requirements:

- The Glue table must be managed by Lake Formation.
- The publishing project's role needs grantable `DESCRIBE` and `SELECT` permissions on the table.

A subscription can later be revoked, which removes the grant. Approval in the catalog and effective access to the data must both happen. If the table is not Lake Formation managed, someone must grant access by other means.

## Catalog lineage and SageMaker ML Lineage Tracking

SageMaker Unified Studio captures lineage automatically from Glue, Redshift, Visual ETL, and notebooks, and it accepts OpenLineage events from other tools. SageMaker ML Lineage Tracking traces ML training artifacts. See [data modeling](data-modeling.md#catalog-lineage-and-sagemaker-ml-lineage-tracking).

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Managed Glue asset fulfillment | Access granted through Lake Formation on approval | The table must be Lake Formation managed | [Grant access to Glue assets](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/grant-access-to-glue-asset.html) |
| Unsupported for managed Glue assets | LF-TBAC grant method, cross-Region sharing | Expect manual steps in those cases | [Grant access to Glue assets](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/grant-access-to-glue-asset.html) |
| Project creation | Each project comes from a project profile, a collection of blueprints | Admins control which tools teams get | [Unified Studio concepts](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/adminguide/concepts.html) |

## Common mistake

Expecting a crawler to fill in business meaning. A crawler infers column names and types. The data owner must write definitions, ownership, and glossary terms.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Glue Data Catalog vs. SageMaker Catalog | Metadata for engines vs. meaning, ownership, and access requests for people |
| Domain vs. domain unit vs. project | Whole organization vs. business unit with delegated policies vs. team workspace |
| Project profile vs. blueprint | A template of tools vs. one tool configuration |
| Subscription approval vs. Lake Formation grant | The business decision vs. the technical permission |

**Exam cues:** "Business users discover datasets and request access" → SageMaker Catalog. "Delegate administration to business units" → domain units. "Team workspace with scoped permissions" → project.

## Try it

People can find a "monthly runs" dataset but disagree on how failed runs are counted. A clinical team wants access but has no process to request it.

<details>
<summary>Show the reasoning</summary>

Have the owner add a glossary term and description defining failed runs, attach a metadata form with owner and sensitivity, and publish the asset in SageMaker Catalog. The clinical team subscribes from its project. On approval, access is granted through Lake Formation.

</details>

## AWS documentation

- [SageMaker Unified Studio concepts](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/adminguide/concepts.html)
- [Domain units and authorization policies](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/adminguide/domain-units.html)
- [Publish assets](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/publishing-data-asset.html)
- [Approve and manage access](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/catalog-iam-manage-access.html)

*Last verified against AWS documentation: November 2026.*
