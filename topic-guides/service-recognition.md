# Recognition-level services: assistants, search, licensed data, and transfer

[Topic index](README.md) · [Exam map](../EXAM-MAP.md)

## The idea

Some in-scope services appear on the exam only as answer options you must recognize. You need to know what each one does and when it is the right pick, not how to configure it in depth. Several of these services were renamed or closed to new customers in 2025 and 2026. The exam guide uses the older names, so learn both.

## Assistant, search, and licensed data

| Service | What it does | Pick it when |
|---|---|---|
| Amazon Q | Generative AI assistants. Amazon Q Developer helps write and explain code, including SQL and Glue scripts. Generative BI features help analysts build dashboards and ask questions in plain language | A stem asks for natural-language help writing code or queries, or plain-language questions over dashboards |
| Amazon Kendra | Machine learning-powered enterprise search across documents, with connectors to sources such as S3, SharePoint, and Salesforce | Employees need to search and get answers from many document repositories |
| AWS Data Exchange | Find, subscribe to, and receive third-party data, or share your own through data grants. Data sets can be files, APIs, Redshift data, S3 data access, or Lake Formation data | You need licensed external data, such as weather or market data, delivered into AWS without building delivery pipelines |
| Amazon Bedrock | Managed access to foundation models and Knowledge Bases | LLM steps in pipelines and RAG. See [vectors and LLMs](vectors-and-llms.md) |

**Name and availability changes to know**

- Amazon Q Developer in the AWS Management Console is now called the **AWS assistant** (November 2026).
- **Amazon Q Business** is no longer open to new customers. AWS recommends Amazon Quick, now **AWS Quick**, for similar capabilities.
- Amazon QuickSight became Amazon Quick Sight and then **AWS Quick Sight** (November 2026). Dashboards, datasets, and SPICE work the same.

## Offline transfers and private connectivity

| Service | What it does | Note |
|---|---|---|
| AWS Snowball Edge | Physical device shipped to you for offline transfer of large datasets | **No longer available to new customers.** AWS points new customers to DataSync for online transfer and AWS Data Transfer Terminals for physical transfer |
| AWS Direct Connect | A dedicated private network link from your data center to AWS | Steady, high-volume transfers with consistent latency. Takes time to provision |
| AWS Site-to-Site VPN | Encrypted tunnel over the internet | Faster to set up than Direct Connect, less predictable throughput |
| AWS DataSync | Online transfer between file systems, object stores, and S3 | See [data movement](data-movement.md) |
| AWS Transfer Family | Managed SFTP, FTPS, FTP, and AS2 endpoints in front of S3 or EFS | Partners upload with protocols they already use |

**Rule of thumb for moving a large one-time dataset:** if the network can move it in an acceptable time, use DataSync over the network or Direct Connect. Older material says "use Snowball if it would take more than a week over the network". Treat that as legacy for new customers and evaluate Data Transfer Terminals or partners instead.

## Numbers and facts

| Fact | Value | Why it matters | AWS source |
|---|---|---|---|
| Data Exchange data set types | Files, API, Amazon Redshift, Amazon S3, AWS Lake Formation (preview) | Recognize how licensed data arrives | [What is AWS Data Exchange?](https://docs.aws.amazon.com/data-exchange/latest/userguide/what-is.html) |
| Snowball Edge | No longer available to new customers | Expect DataSync or Data Transfer Terminal for new migrations | [Snowball Edge availability change](https://docs.aws.amazon.com/snowball/latest/developer-guide/snowball-edge-availability-change.html) |
| Amazon Q Business | No longer open to new customers | Exam options may still list it | [Q Business availability change](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/qbusiness-availability-change.html) |
| Q Developer in the console | Renamed the AWS assistant, November 5, 2026 | Same capability, new name | [What's New announcement](https://aws.amazon.com/about-aws/whats-new/2026/11/q-developer-renamed-aws-assistant/) |
| QuickSight | Now AWS Quick Sight, November 9, 2026 | Same BI features, new name | [What's New announcement](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-quick-aws-quick/) |
| v1.1 in-scope additions | Aurora, Amazon Q, Bedrock, Kendra, Data Exchange, S3 Tables | These names can appear as answers | [Exam guide revisions](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/dea-01-revisions.html) |

## Common mistake

Choosing a service only because its name sounds right. Amazon Q, Kendra, and Bedrock can all "answer questions". Ask what the input is (code, company documents, or your own pipeline data) and whether you need a ready-made assistant or a building block.

## Commonly confused

| Choices | Deciding requirement |
|---|---|
| Kendra vs. OpenSearch | Ready-made enterprise document search vs. a search engine you build indexes and queries on |
| Data Exchange vs. Lake Formation sharing | Licensed or external data products vs. sharing your own tables between accounts |
| Direct Connect vs. VPN | Dedicated consistent link vs. quick encrypted tunnel over the internet |
| Amazon Q vs. Bedrock | Ready-made assistants vs. models you build into your own pipeline |

**Exam cues:** "Subscribe to third-party data" → Data Exchange. "Search across company documents" → Kendra. "Natural-language help writing SQL" → Amazon Q. "Dedicated private connection" → Direct Connect.

## Try it

A lab wants daily weather data from a commercial provider in its S3 lake, analysts want to ask questions of dashboards in plain English, and researchers want to search 20 years of protocols stored in SharePoint.

<details>
<summary>Show the reasoning</summary>

Subscribe to the weather product in AWS Data Exchange and export revisions to S3 automatically. Use the generative BI features in AWS Quick Sight for plain-language dashboard questions. Index the SharePoint protocols with Amazon Kendra.

</details>

## AWS documentation

- [What is Amazon Kendra?](https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html)
- [What is AWS Data Exchange?](https://docs.aws.amazon.com/data-exchange/latest/userguide/what-is.html)
- [What is Amazon Q Developer?](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html)
- [What is AWS Direct Connect?](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)

*Last verified against AWS documentation: November 2026.*
