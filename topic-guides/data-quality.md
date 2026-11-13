# Data quality, quarantine, and safe recovery

[Topic index](README.md) · [Home](../README.md)

## The idea

A quality gate defines the conditions a dataset must meet before it becomes visible to downstream readers.

## How to decide

| Concept | When it matters |
|---|---|
| **Rules** | Check required values, uniqueness, ranges, volume, and freshness. AWS Glue Data Quality can evaluate rules expressed in DQDL. |
| **Quarantine** | Record the rejected row, the reason, and its source batch so the team can diagnose and reprocess it. |
| **Idempotent output** | Use a deterministic batch identifier, replace a complete partition safely, or merge by stable business keys. |
| **Backfill** | Choose a bounded interval, verify what was already published, and rerun using a clear overwrite or merge strategy. |

## Common mistake

If a job wrote some files before failing, rerunning with random output names can duplicate data. Record successful publication after the data is ready.

## Try it

A nightly load fails after writing some records. The source input can be replayed.

<details>
<summary>Show the reasoning</summary>

Stage and validate the full batch, then publish it using an idempotent merge or controlled partition replacement. Verify counts and keys after rerun.

</details>

## AWS documentation

- [AWS documentation · glue data quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html)
- [AWS documentation · dqdl](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html)
