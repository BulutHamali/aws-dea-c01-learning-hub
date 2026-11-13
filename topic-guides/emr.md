# Amazon EMR and distributed processing

[Topic index](README.md) · [Home](../README.md)

## The idea

EMR runs big-data frameworks such as Spark. Choose the deployment mode based on the control and infrastructure your team needs.

## How to decide

| Concept | When it matters |
|---|---|
| **Glue Spark** | Use a managed integration service when jobs mostly clean, join, or convert datasets and already use Glue metadata or connections. |
| **EMR Serverless** | Run supported Spark or Hive workloads without managing a cluster. Consider it for intermittent jobs that fit the runtime. |
| **EMR on EC2** | Choose cluster-level control when you need custom software, bootstrap steps, instance choices, or a persistent cluster. |
| **EMR on EKS** | Run supported workloads on Kubernetes when you already operate EKS and want to share its operational model. |

## Common mistake

Adding workers may leave one slow partition untouched. Look at Spark stage timings, shuffle size, and skew before scaling.

## Try it

A migrated Spark job requires a custom daemon installed on worker nodes at startup and explicit control over the instance fleet.

<details>
<summary>Show the reasoning</summary>

Start with EMR on EC2. The requirements point to control over cluster software and nodes.

</details>

## AWS documentation

- [AWS documentation · emr what is emr](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)
- [AWS documentation · emr serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html)
- [AWS documentation · emr eks](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/emr-eks.html)
