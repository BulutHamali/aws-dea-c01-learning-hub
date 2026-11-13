# Timed DEA-C01 practice set

[Home](../README.md) · [Exam map](../EXAM-MAP.md#task-by-task-study-map) · [Study method](../learning-paths/study-method.md)

Set a timer for **64 minutes**. Record your answers and flag guesses. Select one answer unless a question says **Choose TWO**. The questions are original and ordered across mixed domains.

## Question 1

A weather company needs three independent applications to consume the same event feed. An application recovering from an outage must be able to reread retained events.

- **A.** Data Firehose by itself
- **B.** Kinesis Data Streams
- **C.** One standard SQS queue shared by all readers
- **D.** Separate SQS queues subscribed to one SNS topic

## Question 2

Analysts query historic tables from Redshift. Archived records should stay in S3 but must join to local warehouse tables.

- **A.** COPY all archive files into Redshift
- **B.** Use Redshift federation to query the S3 files
- **C.** Query S3 with Athena and keep the local Redshift tables available only inside Redshift
- **D.** Use Redshift Spectrum

## Question 3

A report must show every daily row per sensor plus the average of its current and six preceding daily readings. Each sensor has one row per date with no gaps. Which SQL approach preserves the detail rows?

- **A.** GROUP BY sensor and calculate AVG(reading)
- **B.** Use a single AVG across the entire table
- **C.** Use AVG over a window partitioned by sensor and ordered by date, with a frame from six preceding rows to the current row
- **D.** Use ROW_NUMBER and filter to one row per sensor

## Question 4

A Glue job can start, but it times out reaching a private RDS instance. The job role and database credentials were validated.

- **A.** Grant Athena access to the catalog
- **B.** Rewrite the S3 objects as Parquet
- **C.** Rotate credentials without inspecting connectivity
- **D.** Verify subnet reachability, security groups, and DNS

## Question 5

An API limits callers to 40 requests per second and sometimes returns HTTP 429. The pipeline has already written a page but crashes before saving its next token. **Choose TWO.**

- **A.** Use bounded backoff with jitter and honor Retry-After
- **B.** Retry every rejected call immediately
- **C.** Use a deterministic output key and save progress after durable storage
- **D.** Advance the checkpoint before persisting the page
- **E.** Discard every page that was throttled

## Question 6

A document search prototype compares every embedding and is too slow. The team can tolerate approximate results and wants to evaluate a graph-based index.

- **A.** Add a date partition only
- **B.** Evaluate HNSW and measure latency and recall
- **C.** Use exact equality on vector values
- **D.** Use IVF solely because it is graph-based

## Question 7

A no-code data team wants to profile columns and record reusable visual cleaning steps before publishing a prepared dataset.

- **A.** Use AWS Glue DataBrew profiles and recipes
- **B.** Use a Glue crawler as the cleaning engine
- **C.** Use S3 Glacier transitions to clean values
- **D.** Write a Spark ETL job with custom profiling code

## Question 8

A group should query approved columns in a governed S3 lake through Athena. It currently has raw S3 read access. **Choose TWO.**

- **A.** Grant the group wider S3 access
- **B.** Grant column-scoped access through Lake Formation for the table
- **C.** Remove direct raw-object access for the restricted role
- **D.** Give the role the broadest managed policy
- **E.** Enable S3 Versioning only

## Question 9

A database must continue accepting writes while the team copies its existing tables and then forwards inserts, updates, and deletes to a supported target.

- **A.** Use DataSync on the database installation directory
- **B.** Use a Glue crawler to read each changed row
- **C.** Schedule a complete export each hour
- **D.** Run DMS full load plus CDC

## Question 10

An S3 analytical table requires daily row corrections and the ability to query a previous committed version.

- **A.** Use a supported Iceberg table with snapshot retention
- **B.** Query a directory of Parquet files through a conventional external table
- **C.** Use S3 lifecycle transitions alone
- **D.** Add a crawler schedule

## Question 11

An existing team maintains Airflow DAGs and operators. It wants to run those DAGs on AWS and retain its Airflow backfill workflow.

- **A.** Rewrite the DAGs as SNS subscriptions
- **B.** Use an S3 Lifecycle rule
- **C.** Store the DAG files in the Glue Data Catalog
- **D.** Use Amazon MWAA

## Question 12

A cross-account role has been granted S3 read access, but the dataset uses a customer-managed KMS key in the owner account. The error is KMS AccessDenied.

- **A.** Add more S3 ListBucket permissions
- **B.** Disable TLS
- **C.** Authorize cross-account key use in the key policy and grant applicable decrypt permission to the role
- **D.** Grant database SELECT privileges

## Question 13

Daily flat files are too large for one worker. The team wants serverless joins, row validation, and output to partitioned Parquet.

- **A.** Run a Glue Spark ETL job
- **B.** Run a Glue crawler only
- **C.** Run each entire day in one Lambda invocation
- **D.** Configure Firehose record conversion directly on the arriving files

## Question 14

A date-based Athena-only table has predictable S3 paths. The team wants dates queryable without registering each new partition.

- **A.** Use a separate Schema Registry per day
- **B.** Use a Glue bookmark to update the table
- **C.** Set up partition projection and validate the path template
- **D.** Schedule a crawler every day after the files arrive

## Question 15

An Athena query usually filters one day and selects two fields from a large CSV dataset. The team can redesign the layout. **Choose TWO.**

- **A.** Partition by an appropriately sized date key used in predicates
- **B.** Partition by a unique event ID
- **C.** Select every column
- **D.** Write a columnar format such as Parquet
- **E.** Turn on S3 replication as the scan optimization

## Question 16

Approved support analysts may view the last four digits of an identifier. Another role must see its full value in the same Redshift table.

- **A.** Use Redshift dynamic data masking with role-scoped policy
- **B.** Rewrite all identifiers in the source table to constants
- **C.** Use SSE-KMS alone
- **D.** Configure S3 retention

## Question 17

A Spark workload requires a custom node daemon and explicit control over the worker instance fleet.

- **A.** Use a Glue crawler
- **B.** Use EMR Serverless
- **C.** Use EMR on EC2 with bootstrap configuration
- **D.** Use AWS Glue Spark with additional Python libraries

## Question 18

Business users need to find a trustworthy “daily revenue” dataset, see its owner and definition, and request access through a team workspace.

- **A.** Run a crawler every hour
- **B.** Use CloudWatch Logs Insights
- **C.** Create an S3 lifecycle rule
- **D.** Publish the asset in SageMaker Catalog and use a project subscription workflow

## Question 19

A nightly Redshift load fails because an input field cannot be converted to the target type. The operator needs the filename and column.

- **A.** Inspect SYS_QUERY_HISTORY only
- **B.** Inspect the query execution plan
- **C.** Inspect SYS_LOAD_ERROR_DETAIL for the COPY query
- **D.** Inspect only the Glue Data Catalog table owner

## Question 20

An auditor asks which principal read a specific S3 object last week. Which record should the team look for, assuming collection was configured?

- **A.** A Glue job bookmark
- **B.** A lifecycle transition record alone
- **C.** An AWS Budget alert
- **D.** A CloudTrail S3 data event for GetObject

## Question 21

Free-text maintenance reports must become a structured table. An LLM extracts fields from reports with variable phrasing. How should the team handle extracted values?

- **A.** Accept every well-formed response
- **B.** Change KMS keys to improve field accuracy
- **C.** Index the original text and assume required fields exist
- **D.** Validate types and values, test against labeled reports, and route uncertain outputs for review

## Question 22

A Redshift analyst must write a query result to S3 so another team can process it. Which command moves the data in the required direction?

- **A.** UNLOAD
- **B.** COPY
- **C.** MERGE
- **D.** VACUUM

## Question 23

A job reports success, but yesterday’s dashboard is stale. The expected date does not appear in the output.

- **A.** Increase compute across every stage
- **B.** Check source arrival, input and output counts, catalog visibility, and refresh time
- **C.** Delete the pipeline checkpoint immediately
- **D.** Enable KMS key rotation

## Question 24

A team suspects S3 datasets contain PII and must keep backups inside approved Regions. **Choose TWO.**

- **A.** Enable unrestricted cross-Region replication
- **B.** Use Macie findings to identify likely sensitive S3 data
- **C.** Use a Glue bookmark to enforce data residency
- **D.** Apply only a bucket encryption rule
- **E.** Review and constrain replication and backup destinations and monitor configuration

## Question 25

A file arrival starts validation, a Glue job, and notification if the job ultimately fails. The team wants explicit branches and retry policies.

- **A.** Use an EventBridge rule alone
- **B.** Route the arrival event to Step Functions
- **C.** Use SNS alone
- **D.** Invoke Glue directly on each arrival and configure an alarm

## Question 26

The raw archive must keep prior object versions for recovery and move older noncurrent versions into cheaper storage. **Choose TWO.**

- **A.** Expire every current and noncurrent object immediately
- **B.** Enable S3 Versioning
- **C.** Use Transfer Acceleration
- **D.** Use an S3 access point per day
- **E.** Set a noncurrent version transition rule

## Question 27

A random sample across a large combined feed misses a small supplier’s malformed values. The supplier must be represented in recurring samples.

- **A.** Stratify the sample by supplier and validate each group
- **B.** Sample the largest supplier only
- **C.** Increase compression
- **D.** Remove supplier IDs before drawing the sample

## Question 28

Two independent applications must receive every notification. One must buffer the messages during outages.

- **A.** Use an SNS topic with separate SQS queues
- **B.** Use one queue shared between both consumers
- **C.** Publish to one SNS topic with two direct Lambda subscriptions
- **D.** Use a crawler to find pending messages

## Question 29

A DynamoDB API always fetches the latest measurements for one device by a known ID. Which primary key design supports a Query by device and a sort condition by time?

- **A.** Partition by timestamp and omit the device ID
- **B.** Partition by device ID and sort by timestamp with an appropriate tie-breaker
- **C.** Use a random partition key for each record with no secondary index
- **D.** Use the measurement value as the partition key

## Question 30

A Lambda function consumes SQS batches. One malformed message keeps causing nine successful records to be processed again. **Choose TWO.**

- **A.** Always return an error for the whole batch
- **B.** Enable and return partial batch failures
- **C.** Disable retries by deleting every failed message
- **D.** Make successful writes idempotent by record key
- **E.** Increase memory until the malformed message becomes valid

## Question 31

A team recreates its test pipeline manually and frequently misses permissions and alarms. It needs consistent deployment and reviewable changes.

- **A.** Export CloudWatch logs after deploying
- **B.** Save screenshots of the consoles
- **C.** Define resources in IaC and validate changes in CI
- **D.** Recreate the roles manually in each environment

## Question 32

One Lambda must cap its concurrency to protect a downstream database. Another needs lower cold-start latency for a scheduled spike. **Choose TWO.**

- **A.** Use reserved concurrency to cap the first function
- **B.** Use larger ephemeral storage for the first function
- **C.** Move the database password to an environment variable
- **D.** Increase the first function’s timeout as the sole fix
- **E.** Configure provisioned concurrency for the second function’s relevant version or alias

When the timer ends, open the [answer key and review links](timed-answers.md).
