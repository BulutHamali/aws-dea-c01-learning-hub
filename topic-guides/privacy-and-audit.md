# Masking, encryption in transit, residency, and audit evidence

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Privacy controls answer "who can see the real values?" Residency controls answer "where are copies allowed to live?" Audit controls answer "what happened, and can we prove it?" Each needs a different tool.

## Dynamic masking, redaction, and tokenization

| Technique | What it does | Reversible? | AWS example |
|---|---|---|---|
| Masking | Shows a partial or replaced value at query time, such as `XXX-XX-1234` | The stored value is unchanged | Redshift dynamic data masking policies attached to roles |
| Redaction | Removes the value from a published copy | No | Glue or DataBrew transform drops or blanks the column |
| Tokenization | Replaces an identifier with a token. A secured lookup maps tokens back | Yes, with access to the lookup | Custom Lambda or Glue step with a protected mapping table |
| Hashing | One-way transform that still lets you join on equal values | No | `sha2(donor_id || salt, 256)` in a Glue job |
| Anonymization | Removes or generalizes enough fields that a person cannot be identified | No | Drop names, generalize birth date to year |

Removing direct identifiers is not always enough. Combinations such as birth date, ZIP code, and sex can re-identify people. Generalize or remove those too when policy requires anonymization.

## Hide values at query time

**Redshift dynamic data masking** attaches a masking policy to a column for specific roles. Analysts in `support_role` see the last four digits. Auditors see the full value. The data on disk does not change.

**Lake Formation column filters** hide whole columns. **Restricted views** in Athena or Redshift expose only safe columns.

## TLS, client-side encryption, and S3 encryption modes

| Need | Control |
|---|---|
| Encrypt in transit | TLS on every connection. Require it with the bucket policy condition `aws:SecureTransport = false` → Deny |
| Encrypt in transit to databases | Force SSL on RDS (`rds.force_ssl`) or Redshift (`require_ssl`) |
| Encrypt *before* transit | Client-side encryption with the AWS Encryption SDK or the Amazon S3 encryption client, so data leaves your environment already encrypted |
| Encrypt at rest | SSE-S3 by default, SSE-KMS for key control. See [security](security.md#s3-encryption-modes) |

```json
{"Effect": "Deny", "Principal": "*", "Action": "s3:*",
 "Resource": ["arn:aws:s3:::lab-curated", "arn:aws:s3:::lab-curated/*"],
 "Condition": {"Bool": {"aws:SecureTransport": "false"}}}
```

## Regional controls for replication and backups

To keep data and every copy in approved Regions:

- **Service control policies (SCPs)** in AWS Organizations deny actions outside approved Regions with the `aws:RequestedRegion` condition.
- **S3 replication** rules point only to buckets in approved Regions. Review them in AWS Config.
- **AWS Backup** copy rules send cross-Region copies only to approved vaults.
- **AWS Control Tower** Region deny controls apply the same restriction across a landing zone.
- **AWS Config rules** flag non-compliant resources, such as a bucket created in the wrong Region.

## Data residency, sovereignty, and exception reviews

**Data residency** is where data is stored. **Data sovereignty** is the stronger idea that data is subject to the laws of the place it is stored, and its access and control must follow those laws. To maintain sovereignty: keep data and backups in the required Region, keep encryption keys in the same jurisdiction (customer managed KMS keys in that Region), restrict who can access it from elsewhere, and document and review every exception.

## Audit evidence, scope, and retention

| Question | Evidence | Notes |
|---|---|---|
| Who changed a bucket policy or started a job? | CloudTrail management events | On by default. 90 days in Event history. Create a trail to keep longer in S3 |
| Who read this S3 object? | CloudTrail data events | Off by default and charged. Enable for the buckets that need it |
| Why did the job fail? | CloudWatch Logs application logs | Set retention. See [monitoring](monitoring.md#cloudwatch-log-groups-retention-and-queries) |
| What did this resource look like last month? | AWS Config configuration history | Records configuration changes for supported resources |
| Which requests reached this bucket? | S3 server access logs | Best-effort delivery. CloudTrail data events are more complete for audit |

## CloudTrail event categories and selectors

- **Management events:** control-plane actions such as `CreateBucket` or `PutBucketPolicy`.
- **Data events:** data-plane actions such as `GetObject`, `PutObject`, Lambda `Invoke`, or DynamoDB item reads. High volume.
- **Insights events:** unusual API call rates or error rates.
- **Advanced event selectors** limit data events to specific buckets, prefixes, or event names to control cost.

Store trails in a dedicated log bucket in a separate security account, with S3 Object Lock and log file validation turned on so tampering is detectable.

## CloudTrail Lake and account availability

CloudTrail Lake stores events in event data stores you can query with SQL. **AWS closed CloudTrail Lake to new customers on May 31, 2026.** Existing customers can keep using it. AWS recommends Amazon CloudWatch for new centralized queries of CloudTrail data. The exam guide still names CloudTrail Lake (skill 4.4.3), so know what it does: centralized, SQL-queryable, long-retention storage of CloudTrail events across accounts and Regions.

## Query audit logs in Athena, Logs Insights, or OpenSearch

| Logs live in | Query with |
|---|---|
| S3 (CloudTrail trail, S3 access logs, VPC Flow Logs) | Athena, with partition projection on date |
| CloudWatch Logs | CloudWatch Logs Insights |
| Indexed for search and dashboards | OpenSearch Service |
| Very large S3 archives that need heavy processing | EMR with Spark |

**Worked example.** Someone downloaded a donor file last week, and cross-Region replication was turned on for the same bucket. Query CloudTrail data events in Athena for `GetObject` on the key to find the caller. Query management events for `PutBucketReplication`. Check AWS Config history for when the replication configuration changed.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| CloudTrail Lake | Closed to new customers on May 31, 2026. Existing customers keep access | Expect CloudWatch for new centralized CloudTrail analysis | [CloudTrail Lake availability change](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-service-availability-change.html) |
| CloudTrail Event history | Last 90 days of management events | Create a trail for longer retention | [CloudTrail Event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html) |
| Data events | Not logged by default | "Who read the object" needs data events enabled beforehand | [Logging data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html) |

## Common mistake

Expecting CloudTrail to show who read an object last month when data events were never enabled. Management events don't include object reads.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| CloudTrail vs. AWS Config | Who did what, when vs. what a resource's configuration was over time |
| Management vs. data events | Control-plane changes vs. object and item reads and writes |
| Masking vs. tokenization | Hide at query time vs. replace with a reversible token |
| In transit vs. before transit | TLS on the connection vs. client-side encryption of the payload |
| Residency vs. sovereignty | Where data sits vs. which laws and controls govern it |

**Exam cues:** "Who accessed the object" → CloudTrail data events. "Configuration changes" → AWS Config. "Prevent backups to other Regions" → SCP with `aws:RequestedRegion` and Backup copy rules. "Show last four digits only" → dynamic data masking.

## Try it

Support analysts in Redshift must see only the last four digits of donor phone numbers. Auditors need the full value. Compliance requires that no copy of donor data leaves `eu-central-1`.

<details>
<summary>Show the reasoning</summary>

Attach a Redshift dynamic data masking policy to the phone column for the support role, and a full-access policy for auditors. Apply an SCP that denies actions outside `eu-central-1`, keep KMS keys in that Region, restrict replication and Backup copies to it, and monitor with AWS Config.

</details>

## AWS documentation

- [Redshift dynamic data masking](https://docs.aws.amazon.com/redshift/latest/dg/t_ddm.html)
- [AWS Encryption SDK](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/introduction.html)
- [CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)
- [CloudTrail Lake availability change](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-service-availability-change.html)
- [What is AWS Config?](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
- [SCP examples for Region restriction](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples_general.html)

*Last verified against AWS documentation: November 2026.*
