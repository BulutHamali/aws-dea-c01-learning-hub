# Data preparation, analysis, and visualization

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

The same dataset can go through several tools. Decide whether the person needs to inspect it, clean it, answer an analytical question, or deliver a dashboard.

| Work | First option to evaluate |
|---|---|
| Profile columns and design visual data-cleaning steps | AWS Glue DataBrew recipes and profile jobs |
| Repeated distributed joins and format conversion | Glue Spark ETL or EMR |
| Ad hoc SQL over a lake | Athena |
| Explore data with Spark in a notebook | Athena for Apache Spark or a suitable Glue interactive environment |
| Publish a BI dashboard | Amazon QuickSight. Evaluate SPICE import for dashboard performance or direct query when source freshness and connector behavior fit |
| Search and visualize operational events | OpenSearch for indexed search. Use CloudWatch Logs Insights for interactive queries over logs already in CloudWatch |

Use grouped aggregation to collapse records into one row per group. A window function computes a rolling average while preserving row detail. A pivot puts category values into columns. A view saves a logical query; a materialized view stores computed results with a refresh strategy.

**Quality example.** A random 1% sample may miss rare errors in a small supplier feed. Stratify across suppliers or validate the required fields across the entire batch. Report the validation denominator and include rejected counts.

[AWS Glue DataBrew](https://docs.aws.amazon.com/databrew/latest/dg/what-is.html) · [Athena for Apache Spark](https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark.html) · [QuickSight data sources](https://docs.aws.amazon.com/quicksight/latest/user/supported-data-sources.html)
