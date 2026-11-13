# Lab 4: Restrict rows and columns with Lake Formation, then close the bypass

[Labs](../../README.md) · [Governance](../../../topic-guides/governance.md) · [Security](../../../topic-guides/security.md)

**Skills practiced:** 4.2.4, 4.2.5, 4.3.1, 4.2.6 · **Time:** about 45 minutes · **Needs:** an AWS account where you may become a Lake Formation administrator, the AWS CLI

A contractor role must see only Cincinnati rows and no donor identifiers. You will create a Lake Formation cell-level filter, prove it works in Athena, then show how direct S3 access bypasses it and remove that path.

> Use a sandbox account. Lake Formation settings apply account-wide in a Region. Do not change data lake settings in an account other teams rely on.

## Cost and cleanup

- **Expected cost:** very low. Lake Formation permissions have no charge. A few Athena queries over kilobytes and tiny S3 storage.
- **Pricing pages:** [Lake Formation](https://aws.amazon.com/lake-formation/pricing/) · [Amazon Athena](https://aws.amazon.com/athena/pricing/)

## 1. Deploy and upload fictional data

```bash
export AWS_REGION=us-east-1
aws cloudformation deploy --stack-name dea-lab4 --template-file template.yaml \
  --capabilities CAPABILITY_NAMED_IAM --parameter-overrides ContractorRawAccess=true
export ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export BUCKET=dea-lab4-data-$ACCOUNT-$AWS_REGION
export CONTRACTOR=arn:aws:iam::$ACCOUNT:role/dea-lab4-contractor
export ANALYST=arn:aws:iam::$ACCOUNT:role/dea-lab4-full-analyst
aws s3 cp donor-runs.csv s3://$BUCKET/donors/
```

## 2. Make yourself a Lake Formation administrator

In the Lake Formation console, open **Administrative roles and tasks** and add your current IAM role or user as a data lake administrator. The console adds you to the existing list. The CLI command `put-data-lake-settings` replaces the whole list, so avoid it unless you include existing admins.

## 3. Hand the table to Lake Formation

```bash
# Let Lake Formation vend credentials for this S3 path
aws lakeformation register-resource --use-service-linked-role \
  --resource-arn arn:aws:s3:::$BUCKET/donors

# Stop the legacy "IAM decides" default for this table
aws lakeformation revoke-permissions \
  --principal DataLakePrincipalIdentifier=IAM_ALLOWED_PRINCIPALS --permissions ALL \
  --resource '{"Table":{"DatabaseName":"dea_lab4_db","Name":"donor_runs"}}'
```

If the revoke returns "not found", new tables in your account already default to Lake Formation permissions. Continue.

## 4. Create the filter and grant access

```bash
aws lakeformation create-data-cells-filter --table-data '{
  "TableCatalogId":"'$ACCOUNT'","DatabaseName":"dea_lab4_db","TableName":"donor_runs",
  "Name":"cincinnati_no_ids",
  "RowFilter":{"FilterExpression":"site = '"'"'cincinnati'"'"'"},
  "ColumnWildcard":{"ExcludedColumnNames":["donor_name","donor_phone"]}}'

for ROLE in $CONTRACTOR $ANALYST; do
  aws lakeformation grant-permissions --principal DataLakePrincipalIdentifier=$ROLE \
    --permissions DESCRIBE --resource '{"Database":{"Name":"dea_lab4_db"}}'
done

aws lakeformation grant-permissions --principal DataLakePrincipalIdentifier=$CONTRACTOR \
  --permissions SELECT --resource '{"DataCellsFilter":{"TableCatalogId":"'$ACCOUNT'",
  "DatabaseName":"dea_lab4_db","TableName":"donor_runs","Name":"cincinnati_no_ids"}}'

aws lakeformation grant-permissions --principal DataLakePrincipalIdentifier=$ANALYST \
  --permissions SELECT --resource '{"Table":{"DatabaseName":"dea_lab4_db","Name":"donor_runs"}}'
```

## 5. Test as each role

```bash
as_role () {   # usage: as_role ROLE_ARN command...
  CREDS=$(aws sts assume-role --role-arn "$1" --role-session-name lab4 --query Credentials --output json)
  shift
  AWS_ACCESS_KEY_ID=$(echo $CREDS | python3 -c 'import json,sys;print(json.load(sys.stdin)["AccessKeyId"])') \
  AWS_SECRET_ACCESS_KEY=$(echo $CREDS | python3 -c 'import json,sys;print(json.load(sys.stdin)["SecretAccessKey"])') \
  AWS_SESSION_TOKEN=$(echo $CREDS | python3 -c 'import json,sys;print(json.load(sys.stdin)["SessionToken"])') \
  "$@"
}

for ROLE in $ANALYST $CONTRACTOR; do
  QID=$(as_role $ROLE aws athena start-query-execution --work-group dea-lab4-wg \
    --query-string "SELECT * FROM dea_lab4_db.donor_runs" --output text --query QueryExecutionId)
  sleep 5
  echo "== $ROLE"
  as_role $ROLE aws athena get-query-results --query-execution-id $QID --output text | head -8
done
```

**Expected result:** the full analyst sees four rows with names and phones. The contractor sees two Cincinnati rows with only `site`, `run_id`, and `reads`.

## 6. Break it: the S3 bypass

```bash
as_role $CONTRACTOR aws s3 cp s3://$BUCKET/donors/donor-runs.csv -
```

**Expected result:** the full file prints, including every donor name. The contractor's IAM policy allows `s3:GetObject`, and reading S3 directly never asks Lake Formation. This is the most common governance mistake in exam scenarios.

## 7. Fix it

```bash
aws cloudformation deploy --stack-name dea-lab4 --template-file template.yaml \
  --capabilities CAPABILITY_NAMED_IAM --parameter-overrides ContractorRawAccess=false
as_role $CONTRACTOR aws s3 cp s3://$BUCKET/donors/donor-runs.csv -
```

**Expected result:** `AccessDenied` on the direct read. Rerun step 5: the contractor's filtered Athena query still works, because Athena reads through Lake Formation's temporary credentials.

## 8. Verify

- [ ] The contractor sees only Cincinnati rows and no identifier columns in Athena.
- [ ] Direct S3 reads exposed everything until the IAM permission was removed.
- [ ] After the fix, Athena works and direct reads fail.

## 9. Tear down

```bash
aws lakeformation delete-data-cells-filter --table-catalog-id $ACCOUNT \
  --database-name dea_lab4_db --table-name donor_runs --name cincinnati_no_ids
aws lakeformation deregister-resource --resource-arn arn:aws:s3:::$BUCKET/donors
aws s3 rm s3://$BUCKET --recursive
aws s3 rm s3://dea-lab4-athena-$ACCOUNT-$AWS_REGION --recursive
aws cloudformation delete-stack --stack-name dea-lab4
aws cloudformation wait stack-delete-complete --stack-name dea-lab4
```

Remove yourself as a data lake administrator in the console if you added yourself only for this lab.
