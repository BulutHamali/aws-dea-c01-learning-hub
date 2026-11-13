# Lake Formation, access models, sharing, and PII discovery

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Governance answers three questions: who can see the data, which parts of it they can see, and how others can get access safely. IAM controls who can call AWS APIs. AWS Lake Formation adds database-style permissions on catalog tables, down to columns, rows, and cells. Amazon Macie finds sensitive data so you know what to protect.

## Lake Formation grants across query engines

Lake Formation manages permissions for tables in the Glue Data Catalog. Integrated engines, such as Athena, Redshift Spectrum, EMR, and Glue, check those grants before reading the underlying S3 data.

1. **Register** the S3 location with Lake Formation so it can hand out temporary credentials for that path.
2. **Grant** `SELECT`, `INSERT`, `DESCRIBE`, and other permissions on databases, tables, or columns to IAM roles, users, or SAML groups.
3. **Remove** broad S3 access from analyst roles so they cannot bypass Lake Formation by reading files directly.

**Data filters** narrow a `SELECT` grant:

| Filter level | Example |
|---|---|
| Column | Analysts see `run_id`, `reads`, not `donor_name` |
| Row | A regional lab sees only rows where `site = 'cincinnati'` |
| Cell | Row and column filters combined: one site, without identifiers |

Filters apply only to reads.

**Hybrid access mode** lets you turn on Lake Formation permissions for some users while others keep using IAM and S3 policies, so you can migrate gradually.

## RBAC, IAM ABAC, and LF-tags

| Model | How access is decided | Fits |
|---|---|---|
| Role-based (RBAC) | Permissions attach to roles such as `lab-analyst` | Small, stable sets of jobs |
| Tag-based in Lake Formation (LF-TBAC) | Tag databases, tables, and columns with LF-Tags such as `sensitivity=pii`. Grant roles access to tag expressions | Many tables that share classifications. New tables inherit access when tagged |
| Attribute-based in IAM (ABAC) | Policy conditions compare principal tags with resource tags, such as `aws:PrincipalTag/project` = `aws:ResourceTag/project` | Many projects or teams without writing a policy per project |

```json
{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "*",
 "Condition": {"StringEquals": {"s3:ExistingObjectTag/project": "${aws:PrincipalTag/project}"}}}
```

Choose the model from the business need: a few fixed roles → RBAC. Thousands of tables by classification → LF-Tags. Fast-growing teams and projects → ABAC.

## Macie discovery and Lake Formation access

**Amazon Macie** scans S3 objects for sensitive data such as names, addresses, and credentials.

- **Managed data identifiers** detect common types such as credit card numbers or passport numbers.
- **Custom data identifiers** use regular expressions you define, such as a lab's donor ID format `DNR-[0-9]{6}`.
- **Automated sensitive data discovery** samples buckets continuously. **Sensitive data discovery jobs** scan chosen buckets on demand or on a schedule.
- Findings go to EventBridge and Security Hub so a workflow can react.

**PII workflow with Lake Formation:** Macie finds donor names in a curated table's files. Tag the affected columns with `sensitivity=pii` LF-Tags. Only roles granted that tag can read them. Everyone else gets a column-filtered view.

## Redshift datashares and Lake Formation sharing

| Share | How | Notes |
|---|---|---|
| Redshift to Redshift, same or other account | Producer creates a datashare and grants `USAGE` to a consumer namespace or account | Live data, no copy. Cross-account shares need authorization by the producer account and association by the consumer |
| Lake Formation tables to another account | Grant table or LF-Tag permissions to the external account. AWS Resource Access Manager (RAM) carries the share | Consumer creates resource links to query |
| Datasets to external subscribers | AWS Data Exchange | Licensed third-party data. See [service recognition](service-recognition.md) |
| Business users find and request data | SageMaker Catalog subscriptions | See [Unified Studio](catalog-and-unified-studio.md) |

## Central governance, delegated ownership, and sharing

A **governance framework** decides who owns data and who sets the rules.

| Pattern | How it works | Trade-off |
|---|---|---|
| Centralized | One platform team owns the lake, the catalog, and all grants | Consistent, but a bottleneck |
| Decentralized (data mesh) | Domain teams own and publish their data as products | Fast, but needs shared standards |
| Federated (hub and spoke) | Domains own data. A central account holds the catalog and governance rules. Producers share into it and consumers subscribe | Common AWS pattern with Lake Formation or SageMaker Catalog |

Sharing patterns to recognize: in-place sharing (Lake Formation, Redshift datashares) avoids copies. Copy-based sharing (UNLOAD, replication) duplicates data and governance work.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Lake Formation filter levels | Column, row, and cell | Pick the narrowest filter that meets the requirement | [Data filtering](https://docs.aws.amazon.com/lake-formation/latest/dg/data-filtering.html) |
| Filtered permissions | Only `SELECT` can carry a filter | Filters do not restrict writes | [Data filtering](https://docs.aws.amazon.com/lake-formation/latest/dg/data-filtering.html) |
| Engines enforcing row and column security | Athena, EMR, Redshift Spectrum, among others | Direct S3 reads bypass Lake Formation | [Data filtering](https://docs.aws.amazon.com/lake-formation/latest/dg/data-filtering.html) |

## Common mistake

Adding Lake Formation column filters while analysts still have `s3:GetObject` on the raw bucket. They can read the full files directly and skip the filter.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Lake Formation vs. IAM | Table, column, and row permissions vs. API and object permissions |
| LF-Tags vs. IAM ABAC | Tag-based catalog permissions vs. tag-matching conditions in IAM policies |
| Macie vs. Lake Formation | Find sensitive data vs. control access to it |
| Datashare vs. Lake Formation cross-account | Redshift live data vs. catalog tables on S3 |

**Exam cues:** "Column-level or row-level access in Athena" → Lake Formation data filters. "Hundreds of tables, classify once" → LF-Tags. "Find PII in S3" → Macie. "Share Redshift data with another account without copying" → datashare.

## Try it

An external research group may query only de-identified columns of a curated table in Athena. Internal staff see everything. Existing analyst roles have read access to the raw S3 path.

<details>
<summary>Show the reasoning</summary>

Register the location with Lake Formation, tag identifier columns with an LF-Tag, and grant the external group's role `SELECT` excluding those columns. Share cross-account through Lake Formation. Remove direct S3 read access from analyst roles. Test as both roles, including Athena result bucket and KMS permissions.

</details>

## AWS documentation

- [What is Lake Formation?](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html)
- [Lake Formation data filtering](https://docs.aws.amazon.com/lake-formation/latest/dg/data-filtering.html)
- [Lake Formation tag-based access control](https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html)
- [IAM ABAC](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html)
- [What is Amazon Macie?](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [Redshift data sharing](https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html)

*Last verified against AWS documentation: November 2026.*
