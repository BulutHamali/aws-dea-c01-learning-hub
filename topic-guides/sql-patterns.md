# SQL for validation, deduplication, and loading

[Topic index](README.md) · [Home](../README.md)

## The idea

Start by stating the grain of the dataset. If one row should represent one event, every join and merge should preserve or intentionally change that grain.

## How to decide

| Concept | When it matters |
|---|---|
| **GROUP BY and HAVING** | Count rows per key to detect duplicates and compare source and target volumes by date or batch. |
| **ROW_NUMBER** | Rank rows within a business key to keep the latest version. Add a deterministic tie-breaker when timestamps can match. |
| **Staging and MERGE** | Validate the incoming batch, deduplicate it, and apply inserts or updates to the target by its business key. |
| **LIKE and regular expressions** | Use LIKE for wildcard matching. Use the engine’s regex function when you need explicit patterns, such as validating a fixed set of characters. |

## Common mistake

A one-to-many join can multiply records even when both source tables look reasonable. Check row counts and keys before and after the join.

## Try it

A file contains multiple updates per sample, including two updates with the same event timestamp.

<details>
<summary>Show the reasoning</summary>

Rank by event time and a stable secondary field such as source sequence. Keep rank 1 per sample in staging and merge the result.

</details>

## AWS documentation

- [AWS documentation · r_WF_ROW_NUMBER](https://docs.aws.amazon.com/redshift/latest/dg/r_WF_ROW_NUMBER.html)
- [AWS documentation · r_MERGE](https://docs.aws.amazon.com/redshift/latest/dg/r_MERGE.html)
