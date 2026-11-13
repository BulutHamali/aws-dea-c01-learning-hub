# IAM, KMS, credentials, and network access

[Topic index](README.md) · [Home](../README.md)

## The idea

Follow the identity that actually executes the operation. A successful launch from your console only proves that your identity could start the job.

## How to decide

| Concept | When it matters |
|---|---|
| **IAM** | The execution role needs permission for the APIs it calls. Resource policies and explicit denies also affect access. |
| **KMS** | A role reading SSE-KMS data needs applicable decrypt authorization. Cross-account access can also require a key policy that authorizes the external account or role. |
| **Secrets Manager** | Store and rotate supported database credentials outside the job code. Grant the execution role access to the specific secret. |
| **Network path** | Verify route and endpoint reachability, security groups, and DNS for private sources. Use TLS to protect traffic in transit. |

## Common mistake

A read of an SSE-KMS S3 object can fail after S3 permissions are granted. Confirm authorization for the actual KMS key and inspect CloudTrail when available.

## Try it

A Glue job can list objects in S3, but reading encrypted files fails with a KMS access error.

<details>
<summary>Show the reasoning</summary>

Check the job role and key policy for the specific key protecting the objects. Grant the required decrypt authorization at the appropriate scope.

</details>

## AWS documentation

- [AWS documentation · reference_policies_evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [AWS documentation · key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)
- [AWS documentation · intro](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
