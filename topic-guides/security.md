# IAM, KMS, credentials, and network access

[Topic index](README.md) · [Home](../README.md)

## The idea

A badge identifies who is at the door. The door’s access list decides whether the badge can enter, and a locked cabinet inside still needs its own key. Map those layers to identity, data permissions, and KMS key authorization.

Follow the identity that actually executes the operation. A successful launch from your console only proves that your identity could start the job.

## How to decide

| Concept | When it matters |
|---|---|
| **IAM** | The execution role needs permission for the APIs it calls. Resource policies and explicit denies also affect access. |
| **KMS** | A role reading SSE-KMS data needs applicable decrypt authorization. Cross-account access can also require a key policy that authorizes the external account or role. |
| **Secrets Manager** | Store and rotate supported database credentials outside the job code. Grant the execution role access to the specific secret. |
| **Network path** | Verify route and endpoint reachability, security groups, and DNS for private sources. Use TLS to protect traffic in transit. |

## Read an access failure in order

1. Confirm the principal and its role trust relationship. A role needs to be assumable by the intended service or caller.
2. Check the API and resource authorization, including relevant explicit denies, endpoint policies, and bucket policies. Confirm any necessary table grants.
3. Verify KMS permissions when customer-managed keys protect data or secrets.
4. For network timeouts, test routes, endpoint reachability, security groups, and DNS. Look for a connection error before widening access.

Use database roles and grants for SQL privileges. Secrets Manager can manage supported credential rotation. Parameter Store can hold configuration values and SecureString parameters. Decide who can read each secret or parameter and which key is used.

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
