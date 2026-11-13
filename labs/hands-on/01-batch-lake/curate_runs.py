"""Glue ETL job for DEA-C01 lab 1.

Reads the raw runs table from the Glue Data Catalog, sends invalid rows to quarantine
with a reason, and writes valid rows as Parquet partitioned by run_date. Each run
overwrites only the partitions it writes, so a rerun of the same dates is idempotent.
"""

import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F

args = getResolvedOptions(
    sys.argv, ["JOB_NAME", "DATABASE", "SOURCE_TABLE", "CURATED_PATH", "QUARANTINE_PATH"]
)

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

raw = glue_context.create_dynamic_frame.from_catalog(
    database=args["DATABASE"], table_name=args["SOURCE_TABLE"]
).toDF()

# The crawler may infer reads as a string if any value is not numeric.
typed = raw.withColumn("reads_num", F.col("reads").cast("long"))

reason = (
    F.when(F.col("run_id").isNull() | (F.trim(F.col("run_id")) == ""), F.lit("missing run_id"))
    .when(F.col("reads_num").isNull(), F.lit("reads not numeric"))
    .when(F.col("reads_num") < 0, F.lit("negative reads"))
)
checked = typed.withColumn("reject_reason", reason)

valid = (
    checked.filter(F.col("reject_reason").isNull())
    .select("run_date", "run_id", "instrument", F.col("reads_num").alias("reads"))
    .dropDuplicates(["run_date", "run_id"])
)
rejected = checked.filter(F.col("reject_reason").isNotNull()).withColumn(
    "rejected_at", F.current_timestamp()
)

valid.write.mode("overwrite").partitionBy("run_date").parquet(args["CURATED_PATH"])
rejected.write.mode("append").json(args["QUARANTINE_PATH"])

print(f"input={raw.count()} valid={valid.count()} rejected={rejected.count()}")
job.commit()
