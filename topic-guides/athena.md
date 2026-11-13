# Athena queries, cost, and workgroups

[Topic index](README.md) · [Home](../README.md)

## The idea

Athena lets you use SQL over S3 datasets and can query supported external sources through connectors. Query performance depends heavily on how the data is laid out.

## How to decide

| Concept | When it matters |
|---|---|
| **Partition pruning** | Filter the partition column directly so Athena can skip unrelated paths. |
| **Column pruning** | Use Parquet or ORC and select the columns you need. Check bytes scanned on representative queries. |
| **CTAS** | Create a new table from a SELECT query. It can reshape data and write it in a different file format or layout. |
| **Workgroups** | Group queries and control settings such as results location and data usage limits. Protect the S3 results location separately. |

## Common mistake

When query time rises, inspect the execution statistics and files before raising quotas. A poorly chosen filter may still scan many partitions.

## Try it

A weekly analysis reads only run ID, date, and yield, yet scans the whole raw CSV dataset.

<details>
<summary>Show the reasoning</summary>

Create a curated Parquet table with a partition scheme that matches common filters. Select only the needed columns and compare scanned bytes using the same analytical query.

</details>

## AWS documentation

- [AWS documentation · what is](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)
- [AWS documentation · ctas](https://docs.aws.amazon.com/athena/latest/ug/ctas.html)
- [AWS documentation · workgroups manage queries control costs](https://docs.aws.amazon.com/athena/latest/ug/workgroups-manage-queries-control-costs.html)
