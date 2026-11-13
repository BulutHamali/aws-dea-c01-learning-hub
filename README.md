# AWS DEA-C01 Learning Hub

A practical study path for **AWS Certified Data Engineer – Associate (DEA-C01)**. Learn how data moves through AWS, why you would choose one service over another, and how to diagnose a pipeline when it fails.

## Choose your path

| If you have… | Start here | What to focus on |
|---|---|---|
| Four weeks | [Four-week plan](learning-paths/4-week-plan.md) | Follow the weekly path through 24 guides and practice every week |
| One to two weeks | [Diagnostic](practice/diagnostic.md) and [topic index](topic-guides/README.md) | Review the guides tied to your weakest answers |
| A few days | [Decision guides](decision-guides/README.md) | Explain what requirement makes each service the best fit |
| A study session today | [Pipeline challenges](practice/pipeline-challenges.md) | Write your reasoning before revealing the answer |

New to data engineering? [Start here](START-HERE.md). Coming from SAA-C03? Begin with [Glue](topic-guides/glue.md), [Athena](topic-guides/athena.md), and [Redshift](topic-guides/redshift.md), then try the [batch workshop](labs/README.md#workshop-1--design-a-sequencing-metrics-lake).

## Study by exam domain

| Domain | Scored weight | Start with |
|---|---:|---|
| Data Ingestion and Transformation | 34% | [Streaming](topic-guides/streaming.md), [Glue](topic-guides/glue.md), [Orchestration](topic-guides/orchestration.md) |
| Data Store Management | 26% | [S3](topic-guides/s3.md), [File formats and table layout](topic-guides/file-layout.md), [Database selection](topic-guides/databases.md) |
| Data Operations and Support | 22% | [Monitoring](topic-guides/monitoring.md), [Data quality and recovery](topic-guides/data-quality.md), [Athena](topic-guides/athena.md) |
| Data Security and Governance | 18% | [IAM and encryption](topic-guides/security.md), [Lake Formation and auditing](topic-guides/governance.md) |

See the [full exam map](EXAM-MAP.md) and the [official AWS exam guide](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01.html).

## Learn, practice, and check your readiness

| Learn | Practice | Check |
|---|---|---|
| [Glossary and first pipeline](START-HERE.md) | [Six pipeline challenges](practice/pipeline-challenges.md) | [Eight-question diagnostic](practice/diagnostic.md) |
| [Visual decision maps](decision-guides/visual-maps.md) | [Three workshops with expected results](labs/README.md) | [32-question timed practice set](practice/timed-set.md) |
| [Task-by-task exam map](EXAM-MAP.md#task-by-task-study-map) | [20 recall cards](practice/recall-cards.md) | [Progress tracker](CHECKLIST.md) |

## How to study

1. Read a topic guide. Explain the service and its inputs and outputs from memory.
2. Compare it with the closest alternative. Name the one constraint that changes your decision.
3. Solve a scenario. Include how you would monitor the pipeline and rerun a failed batch.
4. Record your misses in the [progress tracker](CHECKLIST.md) and retry them two days later.

The [workshops](labs/README.md) use fictional datasets and can be completed without an AWS account. The diagnostic and challenges use original practice scenarios. This is an independent study resource. Use AWS documentation to verify feature availability, limits, pricing, and exam scope.

For a daily session template, spaced review, and exam pacing, see the [study method](learning-paths/study-method.md).

## Sources and attribution

The [official AWS DEA-C01 exam guide](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01.html) determines the study objectives. The [AWS SAA-C03 Learning Hub](https://github.com/BulutHamali/aws-saa-c03-learning-hub) informed the study structure. [Laura Galera’s notes](https://github.com/lauragalera/aws-data-engineer-associate-notes), accessed through [BulutHamali’s fork](https://github.com/BulutHamali/aws-data-engineer-associate-notes), were an initial reference for the first version. Each topic guide links to relevant AWS documentation.
