# Masking, privacy, and audit evidence

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## Choose a control for the risk

| Need | Control | Example |
|---|---|---|
| Protect data in transit | TLS and policies enforcing secure requests | Require HTTPS to S3 |
| Protect stored data | Server-side encryption and scoped key authorization | SSE-KMS for an S3 dataset that needs customer-managed key control. DSSE-KMS applies two server-side encryption layers |
| Hide values at query time | Dynamic masking or restricted views in a supported engine | Customer-service analysts see only the last four digits |
| Share an edited copy | Transform or remove identifiers in the published dataset | Substitute test values in an ETL or DataBrew workflow |
| Discover possible sensitive fields | Macie for eligible S3 objects | Review findings before deciding what to quarantine or restrict |
| Keep data in approved Regions | Review storage, replication, backups, sharing, and policy exceptions | Restrict cross-Region copies and verify configuration over time |

Masking hides values. Tokenization replaces an identifier with a token that can often be linked back with controlled access. Removing direct identifiers may leave re-identification risk through combinations of fields. Apply the privacy rule that fits the dataset and the intended recipients.

## Choose the right evidence

- **CloudTrail** records AWS API activity. Enable relevant data events for operations such as S3 object reads.
- **CloudWatch Logs** stores application logs, including job errors and correlation IDs.
- **AWS Config** records supported resource configuration changes and evaluates configured rules.
- **Athena or Logs Insights** can query logs in their supported locations. Protect the audit destination and set retention. The AWS guide also references CloudTrail Lake. Verify current availability for your account before planning a deployment.

**Scenario.** A team needs to determine who downloaded an object and when cross-Region replication was enabled. Query retained S3 data events for the download, then inspect CloudTrail management events and AWS Config history for the configuration change.

[S3 encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html) · [Redshift dynamic data masking](https://docs.aws.amazon.com/redshift/latest/dg/t_ddm.html) · [CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html) · [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
