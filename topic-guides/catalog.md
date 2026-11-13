# Glue Data Catalog and schema management

[Topic index](README.md) · [Home](../README.md)

## The idea

The catalog tells a query engine where a table lives, which columns it has, and how to interpret its files.

## How to decide

| Concept | When it matters |
|---|---|
| **Crawler** | Discover schema and partitions from data. Configure crawler targets and schema-change behavior deliberately. |
| **Explicit catalog updates** | Create a table or add partitions from a controlled schema or pipeline when you need predictable metadata changes. |
| **Partition projection** | Athena can compute partition locations from rules such as dates and a path template. Athena ignores registered partition metadata for a table when projection is enabled. |
| **Schema Registry** | Track and validate event schema versions in supported producers and consumers. Use compatibility rules to manage changes over time. |

## Common mistake

Check the S3 path, schema, partition visibility, and query engine before concluding that data is missing. Projection can waste time on empty locations when partitions are sparse.

## Try it

An Athena-only table gets a daily partition under a predictable date path. The team wants new dates visible without daily crawler runs.

<details>
<summary>Show the reasoning</summary>

Evaluate Athena partition projection. Define the date range and location pattern, then query a known date and verify that it reads the expected prefix.

</details>

## AWS documentation

- [AWS documentation · catalog and crawler](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html)
- [AWS documentation · partition projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html)
- [AWS documentation · schema registry](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html)
