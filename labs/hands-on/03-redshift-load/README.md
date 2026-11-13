# Lab 3: Load Redshift safely with COPY, staging, and MERGE

[Labs](../../README.md) · [Redshift](../../../topic-guides/redshift.md) · [SQL patterns](../../../topic-guides/sql-patterns.md)

**Skills practiced:** 2.3.1, 2.1.6, 3.2.3, 3.2.5, 3.4.1 · **Time:** about 45 minutes · **Needs:** an AWS account, the AWS CLI, access to Redshift Query Editor v2 in the console

You will load a first batch, plant a bad row in a second batch, read the exact error in `SYS_LOAD_ERROR_DETAIL`, fix it, and apply the batch with a staging table and `MERGE` so a rerun cannot duplicate rows.

## Cost and cleanup

- **Expected cost:** low if you finish and tear down the same day. Redshift Serverless charges for compute in RPU-hours while queries run, and this lab sets a small base capacity of 8 RPUs. Storage for a few rows is negligible.
- **Free Tier:** check whether your account has a Redshift Serverless trial credit.
- **Pricing page:** [Amazon Redshift pricing](https://aws.amazon.com/redshift/pricing/)
- **Networking note:** the workgroup uses your default VPC. It needs subnets in at least two Availability Zones with free IP addresses.

## 1. Deploy and upload data

```bash
export AWS_REGION=us-east-1
aws cloudformation deploy --stack-name dea-lab3 --template-file template.yaml --capabilities CAPABILITY_IAM
export BUCKET=$(aws cloudformation describe-stacks --stack-name dea-lab3 \
  --query "Stacks[0].Outputs[?OutputKey=='DataBucketName'].OutputValue" --output text)
aws s3 cp runs-batch-1.csv s3://$BUCKET/batch-1/
aws s3 cp runs-batch-2.csv s3://$BUCKET/batch-2/
```

Open **Redshift Query Editor v2**, connect to workgroup `dea-lab3-wg`, database `lab`, with your federated identity or the admin secret.

## 2. Create tables and load the first batch

```sql
CREATE TABLE runs (run_id VARCHAR(10), run_date DATE, instrument VARCHAR(20), reads INTEGER);
CREATE TABLE stage_runs (LIKE runs);

COPY runs FROM 's3://<DataBucketName>/batch-1/'
IAM_ROLE default FORMAT AS CSV IGNOREHEADER 1;

SELECT * FROM runs ORDER BY run_id;
```

**Expected result:** R01 with 180 and R03 with 500.

## 3. Break it: a bad row in batch 2

```sql
COPY stage_runs FROM 's3://<DataBucketName>/batch-2/'
IAM_ROLE default FORMAT AS CSV IGNOREHEADER 1;
```

**Expected result:** the COPY fails with "Load into table 'stage_runs' failed. Check 'sys_load_error_detail' system table for details."

```sql
SELECT file_name, line_number, column_name, error_message
FROM sys_load_error_detail ORDER BY start_time DESC LIMIT 5;
```

**Expected result:** the line that holds R04, column `reads`, with an invalid integer error for the value `low`. COPY loads nothing from a failed batch by default, so `stage_runs` is still empty.

## 4. Fix the source and stage again

```bash
aws s3 rm s3://$BUCKET/batch-2/ --recursive
aws s3 cp runs-batch-2-fixed.csv s3://$BUCKET/batch-2/
```

```sql
TRUNCATE stage_runs;
COPY stage_runs FROM 's3://<DataBucketName>/batch-2/'
IAM_ROLE default FORMAT AS CSV IGNOREHEADER 1;

-- Check the grain before merging: one row per run_id
SELECT run_id, COUNT(*) FROM stage_runs GROUP BY run_id HAVING COUNT(*) > 1;
```

`MAXERROR` can let a COPY skip a few bad rows instead, but then you must handle the rejected rows yourself. Fixing the source keeps the batch complete.

## 5. Merge, then rerun the merge

```sql
MERGE INTO runs USING stage_runs s ON runs.run_id = s.run_id
WHEN MATCHED THEN UPDATE SET run_date = s.run_date, instrument = s.instrument, reads = s.reads
WHEN NOT MATCHED THEN INSERT VALUES (s.run_id, s.run_date, s.instrument, s.reads);

SELECT * FROM runs ORDER BY run_id;
```

Run the `MERGE` a second time, then the `SELECT`.

**Expected result:** both times, five rows: R01 200, R02 150, R03 500, R04 90, R05 320. A plain `INSERT INTO runs SELECT * FROM stage_runs` run twice would have duplicated R01, R02, R04, and R05.

## 6. Optional: see a lock wait

Open a second editor tab. In tab 1 run `BEGIN; LOCK runs;` and do not commit. In tab 2 run `SELECT COUNT(*) FROM runs;`. Tab 2 waits. In tab 1 run `COMMIT;` and tab 2 completes. This is how an explicit lock serializes two loaders. See [locks](../../../topic-guides/redshift.md#redshift-and-rds-transactions-locks-and-contention).

## 7. Verify

- [ ] You found the file, line, column, and reason in `SYS_LOAD_ERROR_DETAIL`.
- [ ] The failed COPY loaded nothing.
- [ ] Rerunning `MERGE` left five rows.

## 8. Tear down

```bash
aws s3 rm s3://$BUCKET --recursive
aws cloudformation delete-stack --stack-name dea-lab3
aws cloudformation wait stack-delete-complete --stack-name dea-lab3
```

Deleting the namespace deletes its data. Take a snapshot first if you want to keep anything.
