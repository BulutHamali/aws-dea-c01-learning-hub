# Lab 1: Build a small batch lake with Glue, Athena, and a quality gate

[Labs](../../README.md) · [Glue](../../../topic-guides/glue.md) · [Catalog](../../../topic-guides/catalog.md) · [Athena](../../../topic-guides/athena.md)

**Skills practiced:** 1.2.6, 2.2.3, 2.2.4, 3.1.7, 3.4.1 · **Time:** about 60 minutes · **Needs:** an AWS account, the AWS CLI, permission to create IAM roles

You will land raw CSV files, catalog them with a crawler, run a Glue job that quarantines bad rows and writes partitioned Parquet, query it in Athena through partition projection, and watch a workgroup limit stop an oversized query.

## Cost and cleanup

- **Expected cost:** low if you finish and tear down the same day. You pay for two short Glue runs (Flex execution, two G.1X workers), one crawler run, a few Athena queries over kilobytes, and tiny S3 storage.
- **Free Tier:** Glue jobs and crawlers are not covered by the AWS Free Tier. Check your account's Free Tier or credits page.
- **Pricing pages:** [AWS Glue](https://aws.amazon.com/glue/pricing/) · [Amazon Athena](https://aws.amazon.com/athena/pricing/) · [Amazon S3](https://aws.amazon.com/s3/pricing/)
- **Always run the teardown step at the end.**

## 1. Deploy

```bash
export AWS_REGION=us-east-1
aws cloudformation deploy --stack-name dea-lab1 \
  --template-file template.yaml --capabilities CAPABILITY_IAM

aws cloudformation describe-stacks --stack-name dea-lab1 \
  --query "Stacks[0].Outputs" --output table
export RAW=$(aws cloudformation describe-stacks --stack-name dea-lab1 --query "Stacks[0].Outputs[?OutputKey=='RawBucketName'].OutputValue" --output text)
export CURATED=$(aws cloudformation describe-stacks --stack-name dea-lab1 --query "Stacks[0].Outputs[?OutputKey=='CuratedBucketName'].OutputValue" --output text)
```

## 2. Land raw files and catalog them

```bash
aws s3 cp runs-2026-01-01.csv s3://$RAW/runs/
aws s3 cp runs-2026-01-02.csv s3://$RAW/runs/
aws s3 cp curate_runs.py s3://$RAW/scripts/
aws glue start-crawler --name dea-lab1-raw-runs
aws glue get-crawler --name dea-lab1-raw-runs --query "Crawler.State"   # repeat until READY
aws glue get-table --database-name dea_lab1_db --name raw_runs \
  --query "Table.StorageDescriptor.Columns"
```

**Look at:** the type the crawler inferred for `reads`. Row R04 contains `abc`, so it is likely `string`. This is why the job casts and validates instead of trusting inferred types.

## 3. Run the quality gate

```bash
aws glue start-job-run --job-name dea-lab1-curate-runs
aws glue get-job-runs --job-name dea-lab1-curate-runs --query "JobRuns[0].JobRunState"   # repeat until SUCCEEDED
aws s3 ls s3://$CURATED/runs/ --recursive
aws s3 ls s3://$CURATED/quarantine/runs/ --recursive
```

**Expected result:** two partitions, `run_date=2026-01-01/` and `run_date=2026-01-02/`. The job log in CloudWatch shows `input=8 valid=4 rejected=3`. The missing row is the duplicate R06, removed by `dropDuplicates`. Reconcile: 8 input = 4 valid + 3 rejected + 1 duplicate.

## 4. Query through partition projection

Open the Athena console, switch to the `dea-lab1-analysts` workgroup, and run this, replacing the bucket name:

```sql
CREATE EXTERNAL TABLE dea_lab1_db.runs (
  run_id string, instrument string, reads bigint)
PARTITIONED BY (run_date string)
STORED AS PARQUET
LOCATION 's3://<CuratedBucketName>/runs/'
TBLPROPERTIES (
  'projection.enabled'='true',
  'projection.run_date.type'='date',
  'projection.run_date.format'='yyyy-MM-dd',
  'projection.run_date.range'='2026-01-01,NOW',
  'storage.location.template'='s3://<CuratedBucketName>/runs/run_date=${run_date}/');

SELECT instrument, SUM(reads) AS reads
FROM dea_lab1_db.runs WHERE run_date = '2026-01-01' GROUP BY instrument;
```

**Expected result:** `inst-a` with 550. No crawler or `MSCK REPAIR TABLE` was needed for the curated table. Run `EXPLAIN` on the query and confirm only the `2026-01-01` partition is listed.

## 5. Break it: an idempotent rerun

Run the job again (step 3) and then rerun the `SELECT`.

**Expected result:** still 550. The job uses dynamic partition overwrite, so it replaces only the partitions it writes. Now imagine the job wrote files with append mode instead: the total would double. That is the exam's "rerun created duplicates" scenario. See [idempotent publishing](../../../topic-guides/data-quality.md#idempotent-publishing-and-backfills).

## 6. Break it: the workgroup scan limit

The workgroup cancels any query that scans more than 1 GB. The lab data is only kilobytes, so no query here will hit the limit. Inspect the setting and the scanned bytes instead:

```bash
aws athena get-work-group --work-group dea-lab1-analysts \
  --query "WorkGroup.Configuration.BytesScannedCutoffPerQuery"
aws athena list-query-executions --work-group dea-lab1-analysts --max-items 1
# Use the returned ID:
aws athena get-query-execution --query-execution-id <id> \
  --query "QueryExecution.Statistics.DataScannedInBytes"
```

**What to notice:** this is the per-query control that cancels queries. A workgroup-wide data usage alert would only notify you. See [Athena workgroups](../../../topic-guides/athena.md#workgroups-and-cost-control).

## 7. Verify

- [ ] Curated data is partitioned by `run_date` and stored as Parquet.
- [ ] Three rejected rows are in `quarantine/` with a reason.
- [ ] A rerun did not change the totals.
- [ ] The curated table works with no registered partitions.

## 8. Tear down

```bash
for b in $RAW $CURATED $(aws cloudformation describe-stacks --stack-name dea-lab1 --query "Stacks[0].Outputs[?OutputKey=='AthenaResultsBucketName'].OutputValue" --output text); do
  aws s3 rm s3://$b --recursive
done
aws glue delete-table --database-name dea_lab1_db --name runs
aws cloudformation delete-stack --stack-name dea-lab1
aws cloudformation wait stack-delete-complete --stack-name dea-lab1
```

Buckets must be empty before CloudFormation can delete them, which is why the loop runs first.
