# Data preparation, analysis, visualization, and sampling

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

The same dataset passes through different hands. A data engineer cleans it, an analyst explores it, and a manager reads a dashboard. Pick the tool by who is doing the work and whether they write code.

| Who and what | First tool to evaluate |
|---|---|
| Analyst cleans data visually, no code | AWS Glue DataBrew |
| Data scientist prepares features for ML | SageMaker Data Wrangler, now part of SageMaker Canvas |
| Team prepares data inside a shared data and AI workspace | SageMaker Unified Studio (Visual ETL, notebooks, query editor) |
| Engineer runs repeated distributed transforms | Glue Spark ETL or EMR |
| Ad hoc SQL over the lake | Athena, or the Redshift query editor for warehouse tables |
| Explore with PySpark in a notebook | Athena for Apache Spark, or Glue interactive sessions |
| Publish dashboards to business users | Amazon QuickSight, now AWS Quick Sight |
| Search and visualize operational events | OpenSearch Service with OpenSearch Dashboards |

## DataBrew recipes and Unified Studio preparation

**DataBrew** works in four steps:

1. A **dataset** points at data in S3, a Data Catalog table, or a JDBC source.
2. A **project** shows a sample in a grid where you click transforms such as "remove duplicates", "split column", or "fill missing values". DataBrew offers more than 250 of them.
3. The steps you click are saved as a **recipe**, a reusable list of transforms.
4. A **recipe job** applies the recipe to the full dataset on a schedule and writes the output to S3.

**SageMaker Unified Studio** brings data and AI tools into one project workspace. Use Visual ETL for drag-and-drop pipelines that run on Glue, the query editor for SQL against Athena or Redshift, and notebooks for Python. Projects share data through SageMaker Catalog subscriptions. See [Unified Studio](catalog-and-unified-studio.md).

## Profile, validate, and correct a batch

| Tool | How it verifies and cleans data |
|---|---|
| DataBrew profile job | Column statistics, missing values, outliers, and correlations, plus data quality rules |
| Glue Data Quality | DQDL rules inside pipelines. See [data quality](data-quality.md) |
| Athena SQL | Count nulls, duplicates, and out-of-range values |
| Lambda | Validate a small file or manifest when it arrives |
| Jupyter notebooks | Explore and fix with pandas or PySpark |
| QuickSight | Spot anomalies visually in charts |
| SageMaker Data Wrangler | Data quality and insights report for ML datasets |

## QuickSight dashboards and DataBrew profiling

AWS renamed QuickSight to Amazon Quick Sight and then AWS Quick Sight in November 2026. The exam guide still says QuickSight, and the features are the same.

**QuickSight** connects to Athena, Redshift, RDS, S3, and other sources.

- **SPICE** is QuickSight's in-memory engine. Import data into SPICE for fast dashboards and to avoid hitting the source on every view. Schedule refreshes to keep it current.
- **Direct query** reads the source each time. Choose it when data must be current to the minute and the source can handle the load.
- Row-level security in a dataset limits which rows each reader sees.

DataBrew also shows value distributions and correlation charts during profiling, which is a quick visual check before data reaches a dashboard.

## Athena for Apache Spark notebook workflow

1. Create a Spark-enabled workgroup in Athena.
2. Open a notebook. A session starts in seconds without a cluster.
3. Read Data Catalog tables with PySpark, explore, and write results back to S3.
4. Sessions end automatically after idle time, and you pay only for the compute used.

Use it for exploration that is awkward in SQL, such as complex Python logic. Use Glue or EMR for production jobs.

## Random and stratified sampling

A **sample** is a subset used to check or explore data without reading all of it.

| Method | How | Good for | Risk |
|---|---|---|---|
| Simple random | Every row has the same chance | Quick estimates on uniform data | Misses rare groups |
| Stratified | Sample separately within each group, such as each supplier | Making sure small groups are represented | Need to know the groups first |
| Systematic | Every 100th row | Simple to run on ordered data | Biased if the data has a repeating pattern |
| Time-based | The most recent window | Freshness checks | Ignores older problems |

A random 1% sample of a file where one small supplier sends 0.5% of rows may contain none of that supplier's rows. Stratify by supplier, or validate required fields on every row and sample only for expensive checks. Report the denominator: "checked 12,000 of 1.2 million rows".

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| DataBrew transformations | More than 250 prebuilt | No-code cleaning covers most common tasks | [What is DataBrew?](https://docs.aws.amazon.com/databrew/latest/dg/what-is.html) |
| DataBrew output | Recipe job results are written to S3 | Plan a downstream catalog step | [What is DataBrew?](https://docs.aws.amazon.com/databrew/latest/dg/what-is.html) |
| Data Wrangler location | Data preparation in SageMaker Canvas | Recognize both names in answer options | [Data preparation in Canvas](https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-data-prep.html) |

## Common mistake

Using DataBrew as a scheduler for a large multi-step production pipeline. Recipe jobs fit data preparation. Orchestrate the full pipeline with Step Functions or MWAA.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| DataBrew vs. Glue ETL | Visual, no-code preparation vs. code-based distributed jobs |
| DataBrew vs. Data Wrangler | General data preparation vs. ML feature preparation |
| SPICE vs. direct query | Fast cached dashboards vs. always-current data |
| Random vs. stratified sampling | Uniform data vs. groups of very different sizes |

**Exam cues:** "Without writing code" → DataBrew. "Business dashboards" → QuickSight. "Explore with Spark in a notebook, serverless" → Athena for Apache Spark. "Small supplier missing from sample" → stratified sampling.

## Try it

A no-code analyst team must profile a supplier feed weekly, apply the same cleaning steps every time, and publish a dashboard for managers.

<details>
<summary>Show the reasoning</summary>

Build the cleaning steps once in a DataBrew project and save them as a recipe. Schedule a recipe job and a profile job. Catalog the S3 output and point a QuickSight dataset at it through Athena, imported into SPICE with a scheduled refresh.

</details>

## AWS documentation

- [AWS Glue DataBrew](https://docs.aws.amazon.com/databrew/latest/dg/what-is.html)
- [Athena for Apache Spark](https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark.html)
- [QuickSight data sources](https://docs.aws.amazon.com/quicksight/latest/user/supported-data-sources.html)
- [SageMaker Data Wrangler](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html)

*Last verified against AWS documentation: November 2026.*
