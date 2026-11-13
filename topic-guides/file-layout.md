# File formats, partitions, and compaction

[Topic index](README.md) · [Home](../README.md)

## The idea

Picture a cabinet with one drawer per day. A date filter selects drawers. Inside, a columnar layout lets you pull the measurement values without reading every description field.

The bytes a query has to read depend on the file format, the partition filter, and the size and number of files.

## How to decide

| Concept | When it matters |
|---|---|
| **CSV and JSON** | Useful for interchange and raw landing. JSON can preserve nested structure. Large analytical scans often read many irrelevant fields. |
| **Parquet and ORC** | Columnar formats that let compatible query engines skip unneeded columns. Select a format supported by your readers. |
| **Partitions** | Group records by frequently filtered values such as run date. Balance pruning against the number of directories and files. |
| **Compaction and table formats** | Compact tiny objects into fewer files. A table format such as Apache Iceberg can add snapshots and row-level changes where the engine supports them. |

## Common mistake

Thousands of tiny Parquet files can still produce slow queries. Reduce file count and verify that partition predicates prune the expected data.

## Try it

Analysts repeatedly query three columns from a large dataset and always filter by collection month.

<details>
<summary>Show the reasoning</summary>

Write Parquet, partition by month if it produces sensible partition sizes, and compare bytes scanned before and after. Keep high-cardinality sample IDs as columns.

</details>

## AWS documentation

- [AWS documentation · performance tuning data optimization techniques](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html)
- [AWS documentation · querying iceberg](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg.html)
