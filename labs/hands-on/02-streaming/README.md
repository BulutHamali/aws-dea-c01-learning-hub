# Lab 2: Stream events, see throttling, and isolate a poison record

[Labs](../../README.md) · [Streaming](../../../topic-guides/streaming.md) · [Lambda](../../../topic-guides/lambda.md)

**Skills practiced:** 1.1.1, 1.1.7, 1.1.9, 1.1.10, 1.1.11 · **Time:** about 45 minutes · **Needs:** an AWS account, the AWS CLI, Python 3 with `boto3`

You will send events to a one-shard Kinesis stream with two consumers (Lambda and Firehose), overload the shard to see real throttling errors, then block the Lambda consumer with one malformed record and fix it with failure-handling settings.

## Cost and cleanup

- **Expected cost:** low if you tear down the same day. A provisioned shard is billed per shard-hour while the stream exists. Firehose and Lambda costs for a few thousand small records are minimal.
- **Free Tier:** Kinesis Data Streams and Firehose are not covered by the AWS Free Tier.
- **Pricing pages:** [Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/pricing/) · [Amazon Data Firehose](https://aws.amazon.com/firehose/pricing/) · [AWS Lambda](https://aws.amazon.com/lambda/pricing/)
- **The stream bills every hour it exists. Run the teardown step.**

## 1. Deploy with default retry behavior

```bash
export AWS_REGION=us-east-1
aws cloudformation deploy --stack-name dea-lab2 --template-file template.yaml \
  --capabilities CAPABILITY_IAM --parameter-overrides SafeMode=false
export STREAM=dea-lab2-events
```

## 2. Normal traffic reaches both consumers

```bash
python3 producer.py $STREAM normal
aws logs tail /aws/lambda/dea-lab2-consumer --since 5m
```

**Expected result:** log lines with `batch_size` and per-instrument counts. After about a minute, Firehose writes objects under `events/dt=YYYY-MM-DD/` in the archive bucket. Two consumers read the same records independently: that is fan-out.

## 3. Break it: overload one shard

```bash
python3 producer.py $STREAM burst
```

**Expected result:** `error codes: {'ProvisionedThroughputExceededException'}` and a large `failed=` count. One provisioned shard accepts up to 1,000 records/s or 1 MB/s. The script sends about 5,000 records per second.

**What to notice:** `PutRecords` succeeds as a call but reports failed entries individually. A real producer must retry only the failed entries with backoff. Fixes are more shards, on-demand mode, or a slower producer. See [fan-in, fan-out, and throughput](../../../topic-guides/streaming.md#fan-in-fan-out-and-throughput).

## 4. Break it: a poison record

```bash
python3 producer.py $STREAM poison
aws logs tail /aws/lambda/dea-lab2-consumer --since 5m --follow
```

**Expected result:** the function fails with `JSONDecodeError` again and again. The 50 good records behind the bad one are never processed. In the console, the function's `IteratorAge` metric keeps rising. With `MaximumRetryAttempts = -1`, Lambda retries until the record expires from the stream, 24 hours here.

## 5. Fix it

```bash
aws cloudformation deploy --stack-name dea-lab2 --template-file template.yaml \
  --capabilities CAPABILITY_IAM --parameter-overrides SafeMode=true
aws sqs receive-message --queue-url $(aws cloudformation describe-stacks --stack-name dea-lab2 \
  --query "Stacks[0].Outputs[?OutputKey=='FailedRecordsQueueUrl'].OutputValue" --output text)
```

**Expected result:** within a few minutes the logs show the good records processed. Bisecting splits the failing batch until the bad record is alone, two retries stop the loop, and the SQS queue receives a message describing the failed record's shard and sequence numbers.

**What to notice:** the on-failure destination receives metadata about the record, not the record itself. Use the sequence numbers to read it from the stream while it is still retained. That is why retention matters for replay. See [read a Kinesis stream with Lambda](../../../topic-guides/lambda.md#read-a-kinesis-stream-with-lambda).

## 6. Verify

- [ ] You saw `ProvisionedThroughputExceededException` in failed entries, not as a call error.
- [ ] The poison record blocked the shard with default settings.
- [ ] Safe mode let processing continue and sent failure details to SQS.
- [ ] Firehose archived the good records to S3.

## 7. Tear down

```bash
aws s3 rm s3://$(aws cloudformation describe-stacks --stack-name dea-lab2 \
  --query "Stacks[0].Outputs[?OutputKey=='ArchiveBucketName'].OutputValue" --output text) --recursive
aws cloudformation delete-stack --stack-name dea-lab2
aws cloudformation wait stack-delete-complete --stack-name dea-lab2
```
