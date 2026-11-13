# Testing, infrastructure as code, and CI/CD for data pipelines

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

A pipeline you built by clicking in the console works once. A pipeline defined in code can be reviewed, tested, rebuilt in another account, and rolled back. **Infrastructure as code (IaC)** describes the buckets, roles, jobs, and workflows in files. **CI/CD** (continuous integration and continuous delivery) tests and deploys those files automatically on every change.

## Engineering practices for data pipelines

| Practice | In a data pipeline |
|---|---|
| Version control | Keep job scripts, SQL, DQDL rules, and templates in Git |
| Unit tests | Test transformation functions on small fixed inputs, such as "negative reads go to quarantine" |
| Integration tests | Run the job on a small sample in a test account and check row counts and schema |
| Data tests | Glue Data Quality rules on real batches. See [data quality](data-quality.md) |
| Logging | Structured logs with a correlation ID per batch. See [monitoring](monitoring.md) |
| Monitoring | Freshness, volume, and failure alarms |
| Configuration | Pass dates, paths, and environment names as job arguments, not hard-coded values |

## Infrastructure as code and deployment review

| Tool | What you write | Notes |
|---|---|---|
| AWS CloudFormation | YAML or JSON templates | AWS's native IaC. Deploys a **stack** of resources together and rolls back on failure |
| AWS CDK | Code in Python, TypeScript, Java, and other languages | `cdk synth` produces a CloudFormation template. Reuse patterns as constructs |
| AWS SAM | A CloudFormation extension with short syntax for serverless resources | Lambda, Step Functions, API Gateway, DynamoDB |

Safe deployment habits:

- Create a **change set** to preview what a stack update will add, modify, or replace before running it.
- Turn on **drift detection** to find resources someone changed by hand.
- Use separate roles: a deployment role that creates resources, and narrow execution roles that jobs run as.
- Deploy the same template to dev, test, and prod with different parameters.

## CloudFormation stacks and CDK synthesis

```yaml
Resources:
  CurateRunsJob:
    Type: AWS::Glue::Job
    Properties:
      Name: curate-runs
      Role: !GetAtt GlueJobRole.Arn
      GlueVersion: "5.0"
      WorkerType: G.1X
      NumberOfWorkers: 5
      Command:
        Name: glueetl
        ScriptLocation: s3://lab-artifacts/jobs/curate_runs.py
      DefaultArguments:
        "--job-bookmark-option": job-bookmark-enable
```

The same job in CDK is a few lines of Python that `cdk synth` turns into a template like the one above. The deployed resource is identical either way.

## SAM package, deploy, and rollback

1. `sam build` prepares function code and dependencies.
2. `sam deploy --guided` packages the code to S3 and deploys the CloudFormation stack. Later runs reuse the saved settings.
3. For gradual Lambda releases, set `AutoPublishAlias` and a `DeploymentPreference`. SAM then uses CodeDeploy to shift traffic.

| Deployment type | Behavior |
|---|---|
| `Canary10Percent5Minutes` | 10% of traffic first, the rest after 5 minutes |
| `Linear10PercentEvery1Minute` | Equal 10% steps every minute |
| `AllAtOnce` | Switch all traffic immediately |

Add CloudWatch alarms to the deployment preference. If an alarm fires during the shift, CodeDeploy rolls back automatically. `PreTraffic` and `PostTraffic` hooks run validation functions.

## Continuous integration and delivery

A typical pipeline for a Glue job:

1. A pull request triggers AWS CodeBuild or GitHub Actions to lint code, run unit tests, and validate the template.
2. After merge, AWS CodePipeline deploys the stack to a test account.
3. An integration test runs the job on a sample batch and checks Glue Data Quality results.
4. A manual approval or passing tests promote the same artifact to production.
5. If production checks fail, redeploy the previous version.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| SAM gradual deployment | Uses CodeDeploy with Canary, Linear, or AllAtOnce traffic shifting | Recognize the rollout options in answers | [SAM gradual deployments](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html) |
| First gradual deployment | Needs an existing version to shift from, so it takes two deployments | The first release is effectively all at once | [SAM gradual deployments](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html) |
| IaC examples named in the exam guide | CloudFormation and CDK (skill 1.4.8) | Expect both in answer options | [Exam guide domain 1](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/data-engineer-associate-01-domain1.html) |
| Services removed from scope in v1.1 | AWS Cloud9 and AWS CodeCommit | Don't build answers around them | [Exam guide revisions](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/dea-01-revisions.html) |

## Common mistake

Fixing a production job directly in the console. The next stack deployment overwrites the fix, and drift detection flags the difference. Change the template instead.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| CloudFormation vs. CDK | Declarative templates vs. general-purpose code that generates templates |
| SAM vs. CloudFormation | Short serverless syntax and local tooling vs. any AWS resource in full syntax |
| Change set vs. drift detection | Preview a planned change vs. find unplanned manual changes |
| Canary vs. linear deployment | Two steps vs. equal steps over time |

**Exam cues:** "Repeatable across accounts" → IaC. "Serverless pipeline with Lambda and Step Functions" → SAM. "Roll back automatically on errors" → SAM deployment preference with alarms.

## Try it

A team recreates its Glue jobs and IAM roles by hand in each account, and environments drift apart. A Lambda function update recently broke production for an hour.

<details>
<summary>Show the reasoning</summary>

Define jobs, roles, and functions in CloudFormation, CDK, or SAM in Git. Validate and test in CI, deploy the same template to each account, and use change sets before updates. For Lambda, use SAM `AutoPublishAlias` with a canary deployment preference and error alarms so a bad release rolls back.

</details>

## AWS documentation

- [What is AWS CloudFormation?](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [What is AWS SAM?](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html)

*Last verified against AWS documentation: November 2026.*
