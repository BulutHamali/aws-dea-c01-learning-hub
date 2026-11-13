# IAM, KMS, credentials, and encryption

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

A badge identifies who is at the door. The door's access list decides whether that badge can enter. A locked cabinet inside still needs its own key. In AWS those layers are **identity** (who is calling), **permissions** (IAM, resource, and Lake Formation policies), and **key authorization** (AWS KMS).

Always follow the identity that actually runs the operation. If you start a Glue job from the console, your identity started it, but the job's **execution role** reads the data. A successful launch proves nothing about the role's access.

## Identity types and endpoint access

| Identity | Use for |
|---|---|
| IAM user | Avoid for people. Use only where no role-based option exists |
| IAM group | Attach policies to many users at once. Groups cannot be principals in policies |
| IAM role | Temporary credentials for services, applications, and federated people. The default for everything in a pipeline |
| IAM Identity Center user | Human sign-in across accounts with temporary credentials |
| Service-linked role | A role a service creates and manages for itself |

## Trust and permission policies by caller

A role has two policies:

- The **trust policy** says who may assume the role, such as `glue.amazonaws.com` or `lambda.amazonaws.com`.
- The **permission policy** says what the role may do once assumed.

| Caller | Role setup |
|---|---|
| Glue job | Trust `glue.amazonaws.com`. Allow S3 paths, catalog tables, secrets, and KMS keys the job uses |
| Lambda function | Execution role trusting `lambda.amazonaws.com`. Add stream or queue read permissions for event source mappings |
| API Gateway calling AWS services | A role API Gateway assumes for direct integrations |
| AWS CLI on a laptop | Assume a role through IAM Identity Center rather than storing access keys |
| CloudFormation | A service role so stacks deploy with that role's permissions instead of the caller's |

## Read an access failure in order

1. **Which principal?** Check the role in the error message or in CloudTrail.
2. **Can it assume the role?** Check the trust policy.
3. **Is the action allowed?** Check identity policies, resource policies (bucket, key, secret), permission boundaries, service control policies (SCPs), and VPC endpoint policies. An explicit `Deny` anywhere wins.
4. **Is there a Lake Formation grant?** For governed catalog tables.
5. **Can it use the KMS key?** For encrypted objects, secrets, and logs.
6. **Is it a timeout instead of AccessDenied?** That is a network problem. See [networking](networking.md).

## Build a scoped policy from required operations

AWS managed policies are broad. Write a custom policy when a job needs only specific actions on specific resources.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": ["s3:GetObject"],
     "Resource": "arn:aws:s3:::lab-raw/runs/*"},
    {"Effect": "Allow", "Action": ["s3:PutObject"],
     "Resource": "arn:aws:s3:::lab-curated/runs/*"},
    {"Effect": "Allow", "Action": ["s3:ListBucket"],
     "Resource": ["arn:aws:s3:::lab-raw", "arn:aws:s3:::lab-curated"],
     "Condition": {"StringLike": {"s3:prefix": ["runs/*"]}}},
    {"Effect": "Allow", "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
     "Resource": "arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"}
  ]
}
```

## Least-privilege policy examples and tests

- Start from the actions the job calls. CloudTrail or IAM Access Analyzer policy generation can list what a role actually used.
- Scope `Resource` to bucket prefixes and key ARNs, not `*`.
- Use conditions such as `aws:SourceVpce` or `aws:SecureTransport`.
- Test with the IAM policy simulator, then run the job and check for denies.
- Remove unused permissions with IAM Access Analyzer's unused access findings.

## Secrets Manager and Parameter Store

| Need | Choose |
|---|---|
| Database password with automatic rotation | AWS Secrets Manager. Built-in rotation for RDS, Aurora, Redshift, and DocumentDB |
| API key or OAuth secret you rotate yourself | Secrets Manager with a rotation Lambda function |
| Configuration values, such as a bucket name or feature flag | Systems Manager Parameter Store, standard parameters |
| A small secret without rotation, at low cost | Parameter Store `SecureString`, encrypted with KMS |

Grant the execution role `secretsmanager:GetSecretValue` on the specific secret ARN, and decrypt on its KMS key if it uses a customer managed key.

## KMS keys, grants, and policies

| Key type | Who controls the key policy | Cross-account use |
|---|---|---|
| AWS owned key | AWS, not visible in your account | No |
| AWS managed key (`aws/s3`, `aws/glue`) | AWS. You cannot edit it | No |
| Customer managed key | You | Yes, by editing the key policy |

Every KMS key has a **key policy**. It decides who *can* use the key. IAM policies then decide who *does*. **Grants** give temporary, narrow permissions, often created by AWS services on your behalf.

S3 **Bucket Keys** reduce the number of calls S3 makes to KMS for SSE-KMS objects, which lowers cost and avoids KMS request throttling.

## Cross-account encrypted object access

The lab's sequencing account (111122223333) shares an SSE-KMS bucket with the analytics account (444455556666).

1. **Bucket policy** in the owner account allows the analytics role `s3:GetObject`.
2. **Key policy** on the customer managed key allows the analytics account or role `kms:Decrypt`.
3. **IAM policy** in the analytics account allows its role `s3:GetObject` on the bucket and `kms:Decrypt` on the key ARN.

All three are required. Objects encrypted with the AWS managed `aws/s3` key cannot be read cross-account, because you cannot edit that key's policy. Re-encrypt with a customer managed key.

## S3 encryption modes

| Mode | Who manages keys | Use when |
|---|---|---|
| SSE-S3 | S3 | Default for all new uploads since January 2023. No KMS cost |
| SSE-KMS | KMS key you or AWS manage | You need key-level access control, audit of key use in CloudTrail, or cross-account sharing |
| DSSE-KMS | KMS, with two layers of encryption | Compliance requires dual-layer encryption |
| SSE-C | You supply the key with every request | You must keep keys outside AWS |
| Client-side encryption | You encrypt before upload | Data must be encrypted before it leaves your environment |

See [privacy and audit](privacy-and-audit.md#tls-client-side-encryption-and-s3-encryption-modes) for encryption in transit.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| S3 default encryption | All new object uploads use SSE-S3 since January 5, 2023, and it cannot be disabled | "Enable encryption" alone is not the answer to a key-control requirement | [Default encryption FAQ](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-encryption-faq.html) |
| Cross-account KMS | Requires both the key policy (owner account) and an IAM policy (caller account) | Neither alone is enough | [Key policies for other accounts](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html) |
| Policy evaluation | An explicit deny overrides any allow | Check SCPs and boundaries when an allow seems to be ignored | [Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) |

## Common mistake

Granting more S3 permissions when the error is a KMS denial. The role can already reach the object. It cannot decrypt it.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Trust policy vs. permission policy | Who can assume the role vs. what the role can do |
| Secrets Manager vs. Parameter Store | Built-in rotation vs. low-cost config and simple secrets |
| AWS managed vs. customer managed KMS key | No policy control vs. full control including cross-account |
| SSE-KMS vs. SSE-C vs. client-side | AWS-held keys with audit vs. you send keys per request vs. you encrypt before upload |

**Exam cues:** "Rotate database credentials automatically" → Secrets Manager. "Another account can't decrypt" → key policy plus caller IAM policy, customer managed key. "Managed policy too broad" → custom least-privilege policy.

## Try it

A Glue job in the analytics account lists objects in the sequencing account's bucket but fails to read them with `AccessDeniedException` from KMS. The objects use SSE-KMS with the `aws/s3` key.

<details>
<summary>Show the reasoning</summary>

The AWS managed key's policy cannot be edited to allow another account. Re-encrypt the objects with a customer managed key, add the analytics role to its key policy for `kms:Decrypt`, and give the role a matching IAM policy. Verify with a test read and check CloudTrail for the KMS call.

</details>

## AWS documentation

- [IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [KMS key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)
- [Allowing users in other accounts to use a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html)
- [Secrets Manager rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [S3 server-side encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html)

*Last verified against AWS documentation: November 2026.*
