# AWS DEA-C01 Learning Hub

A practical study path for **AWS Certified Data Engineer – Associate (DEA-C01)**, aligned to exam guide version 1.1 (December 2025). Learn how data moves through AWS, why you would choose one service over another, the numbers that decide exam answers, and how to diagnose a pipeline when it fails.

[![Repository quality](https://github.com/BulutHamali/aws-dea-c01-learning-hub/actions/workflows/quality.yml/badge.svg)](https://github.com/BulutHamali/aws-dea-c01-learning-hub/actions/workflows/quality.yml)

## Choose your path

| If you have… | Start here | What to focus on |
|---|---|---|
| Six weeks and a full-time job | [Six-week plan](learning-paths/6-week-plan.md) | Three short weekday sessions and one weekend lab or practice block |
| Four weeks | [Four-week plan](learning-paths/4-week-plan.md) | Sixteen sessions, two guides at most per session |
| One to two weeks | [Diagnostic](practice/diagnostic.md) and [topic index](topic-guides/README.md) | Study the guides behind your diagnostic misses, then take the [full mock](practice/full-mock.md) |
| A few days | [Decision guides](decision-guides/README.md) and [recall cards](practice/recall-cards.md) | The service choices and numbers you are most likely to confuse |

New to data engineering? [Start here](START-HERE.md). Coming from SAA-C03? Begin with [Glue](topic-guides/glue.md), [Athena](topic-guides/athena.md), and [Redshift](topic-guides/redshift.md), then try [lab 1](labs/hands-on/01-batch-lake/README.md).

## The exam at a glance

65 questions (50 scored, 15 unscored) in 130 minutes. Passing score 720 out of 1,000.

| Domain | Weight | Guides |
|---|---:|---|
| 1. Data Ingestion and Transformation | 34% | [9 guides](topic-guides/README.md#domain-1--data-ingestion-and-transformation-34): streaming, Lambda, data movement, Glue, EMR, orchestration, APIs, deployment, programming |
| 2. Data Store Management | 26% | [8 guides](topic-guides/README.md#domain-2--data-store-management-26): S3, databases, Redshift, file layout, catalog, Iceberg, modeling, vectors |
| 3. Data Operations and Support | 22% | [5 guides](topic-guides/README.md#domain-3--data-operations-and-support-22): Athena, monitoring, data quality, SQL, analysis |
| 4. Data Security and Governance | 18% | [6 guides](topic-guides/README.md#domain-4--data-security-and-governance-18): security, networking, governance, privacy and audit, Unified Studio, service recognition |

The [exam map](EXAM-MAP.md) links all 120 official skills to the section that teaches each one and the questions that test it.

## Learn, practice, and check your readiness

| Learn | Practice | Check |
|---|---|---|
| [28 topic guides](topic-guides/README.md) with sourced numbers tables | [5 hands-on AWS labs](labs/README.md#hands-on-labs) with CloudFormation and teardown | [12-prompt diagnostic](practice/diagnostic.md) |
| [Glossary and first pipeline](START-HERE.md) | [3 paper workshops](labs/README.md#paper-workshops) and [6 pipeline challenges](practice/pipeline-challenges.md) | [32-question timed set](practice/timed-set.md) |
| [Visual decision maps](decision-guides/visual-maps.md) | [98 recall cards](practice/recall-cards.md), also as an [Anki CSV](practice/recall-cards.csv) | [65-question full mock](practice/full-mock.md) |
| [Skill-by-skill exam map](EXAM-MAP.md#skill-by-skill-map) | [38-question supplemental bank](practice/question-bank.md) | [Progress tracker](CHECKLIST.md) |

Every one of the 115 distinct exam objectives is the primary target of at least one practice question and appears in at least two. Answer explanations say why each wrong option loses, and link the guide section to review.

## How to study

1. Read a topic guide. Explain the service and its inputs and outputs from memory.
2. Compare it with the closest alternative using the guide's **Commonly confused** table. Name the one requirement that changes your decision.
3. Solve the guide's "Try it" scenario, including how you would monitor the pipeline and rerun a failed batch.
4. Record your misses in the [progress tracker](CHECKLIST.md) and retry them two days later.

For a session template, spaced review, and exam pacing, see the [study method](learning-paths/study-method.md).

## How this hub stays accurate

- Every number in a **Numbers and defaults** table links the AWS page it came from, and each guide shows when it was last checked.
- Service changes from 2026 are reflected, such as CloudTrail Lake and Amazon Q Business closing to new customers, Snowball Edge no longer being offered to new customers, and QuickSight becoming AWS Quick Sight.
- Continuous integration checks every link and heading anchor, rebuilds the practice pages to confirm they are current, enforces skill coverage and answer-length balance, and lints the lab templates. See [CONTRIBUTING](CONTRIBUTING.md).

This is an independent study resource, not affiliated with AWS. Practice questions are original. Verify feature availability, limits, and prices in AWS documentation for your Region.

## Sources and attribution

The [official AWS DEA-C01 exam guide](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/data-engineer-associate-01.html) determines the study objectives. The [AWS SAA-C03 Learning Hub](https://github.com/BulutHamali/aws-saa-c03-learning-hub) and the [AWS MLA Learning Hub](https://github.com/BulutHamali/aws-mla-learning-hub) informed the structure. [Laura Galera's notes](https://github.com/lauragalera/aws-data-engineer-associate-notes), accessed through [BulutHamali's fork](https://github.com/BulutHamali/aws-data-engineer-associate-notes), were an initial reference for the first version. Each topic guide links the AWS documentation it relies on.

## License

Content is licensed under [CC BY 4.0](LICENSE). You may share and adapt it, including commercially, with credit to Bulut Hamali and a link to this repository.
