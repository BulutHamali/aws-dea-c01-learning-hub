# Lab 5: Diagnose a KMS AccessDenied and fix it the right way

[Labs](../../README.md) · [Security](../../../topic-guides/security.md) · [Privacy and audit](../../../topic-guides/privacy-and-audit.md)

**Skills practiced:** 4.3.2, 4.3.3, 4.3.4, 3.3.5, 4.2.6 · **Time:** about 30 minutes · **Needs:** an AWS account and the AWS CLI

A role that can list and get objects still cannot read them, because the objects are encrypted with a customer managed KMS key. You will reproduce the error, find it in CloudTrail, fix it with the smallest permission, and see how the fix changes across accounts.

## Cost and cleanup

- **Expected cost:** very low. A customer managed KMS key has a monthly charge prorated by the hour, plus tiny per-request charges. S3 Bucket Keys reduce KMS requests.
- **Pricing pages:** [AWS KMS](https://aws.amazon.com/kms/pricing/) · [Amazon S3](https://aws.amazon.com/s3/pricing/)
- KMS keys cannot be deleted immediately. Teardown schedules deletion with a 7-day waiting period.

## 1. Deploy without decrypt permission

```bash
export AWS_REGION=us-east-1
aws cloudformation deploy --stack-name dea-lab5 --template-file template.yaml \
  --capabilities CAPABILITY_NAMED_IAM --parameter-overrides GrantDecrypt=false
export ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export BUCKET=dea-lab5-data-$ACCOUNT-$AWS_REGION
export READER=arn:aws:iam::$ACCOUNT:role/dea-lab5-reader
echo "run_id,reads" > sample.csv && echo "R01,200" >> sample.csv
aws s3 cp sample.csv s3://$BUCKET/runs/sample.csv
aws s3api head-object --bucket $BUCKET --key runs/sample.csv \
  --query "[ServerSideEncryption, SSEKMSKeyId, BucketKeyEnabled]"
```

**Expected result:** `aws:kms`, the lab key's ARN, and `true` for Bucket Keys.

Reuse the `as_role` helper from [lab 4](../04-lake-formation/README.md#5-test-as-each-role) to run commands as the reader role.

## 2. Break it: list works, read fails

```bash
as_role $READER aws s3 ls s3://$BUCKET/runs/
as_role $READER aws s3 cp s3://$BUCKET/runs/sample.csv -
```

**Expected result:** the list succeeds. The read fails with `AccessDenied` mentioning `kms:Decrypt`. S3 permissions are fine. The role cannot use the key.

## 3. Find the evidence in CloudTrail

```bash
aws cloudtrail lookup-events --max-results 5 \
  --lookup-attributes AttributeKey=EventName,AttributeValue=Decrypt \
  --query "Events[].CloudTrailEvent" --output text | python3 -m json.tool | grep -E '"(errorCode|arn|eventSource)"'
```

**Expected result:** a `Decrypt` event from `kms.amazonaws.com` with `errorCode: AccessDenied` and the reader role's session ARN. KMS calls are management events, so they appear in Event history with default settings. Events can take a few minutes to appear.

## 4. Fix it with the smallest permission

```bash
aws cloudformation deploy --stack-name dea-lab5 --template-file template.yaml \
  --capabilities CAPABILITY_NAMED_IAM --parameter-overrides GrantDecrypt=true
as_role $READER aws s3 cp s3://$BUCKET/runs/sample.csv -
```

**Expected result:** the file prints. The role now has `kms:Decrypt` on this one key ARN, not `kms:*` and not `Resource: "*"`.

**Why an IAM policy was enough here:** the key policy's first statement trusts this account's root principal, which lets IAM policies in this account grant use of the key.

## 5. Think it through: the cross-account version

If the reader role lived in another account, the IAM change alone would fail. You would also add a key policy statement allowing that account or role to call `kms:Decrypt`, and a bucket policy statement allowing it `s3:GetObject`. If the objects used the AWS managed `aws/s3` key, no fix would be possible without re-encrypting, because you cannot edit that key's policy. See [cross-account encrypted object access](../../../topic-guides/security.md#cross-account-encrypted-object-access).

## 6. Bonus: encryption in transit

The bucket policy denies any request where `aws:SecureTransport` is false. The AWS CLI always uses HTTPS, so every command above passed. A client calling the plain HTTP endpoint would be refused. See [encryption in transit](../../../topic-guides/privacy-and-audit.md#tls-client-side-encryption-and-s3-encryption-modes).

## 7. Verify

- [ ] You saw `ListBucket` succeed and `GetObject` fail on the same role.
- [ ] CloudTrail showed the failed `Decrypt` with the role's identity.
- [ ] One `kms:Decrypt` statement on one key fixed the read.
- [ ] You can explain the extra key policy statement needed across accounts.

## 8. Tear down

```bash
export KEY=$(aws cloudformation describe-stacks --stack-name dea-lab5 \
  --query "Stacks[0].Outputs[?OutputKey=='KeyArn'].OutputValue" --output text)
aws s3 rm s3://$BUCKET --recursive
aws cloudformation delete-stack --stack-name dea-lab5
aws cloudformation wait stack-delete-complete --stack-name dea-lab5
aws kms describe-key --key-id $KEY --query "KeyMetadata.KeyState"
```

CloudFormation schedules the key for deletion with the 7-day window set in the template, so the last command should show `PendingDeletion`.
