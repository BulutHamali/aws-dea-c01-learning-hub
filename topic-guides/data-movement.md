# Data movement and database CDC

[Topic index](README.md) · [Home](../README.md)

## The idea

Start with the shape of what needs to move. Database changes, existing files, and incoming partner uploads require different interfaces.

## How to decide

| Concept | When it matters |
|---|---|
| **AWS DMS** | Use full load plus change data capture when a supported database needs an initial copy and ongoing changes. Confirm source log configuration and retention. |
| **AWS DataSync** | Move files or objects between supported storage systems on a schedule. Use it for a directory tree already sitting on a file share. |
| **AWS Transfer Family** | Offer a managed file-transfer endpoint when a partner sends files over a protocol such as SFTP. |
| **Amazon AppFlow** | Move records between supported SaaS applications and AWS without writing your own connector. |

## Common mistake

Replication lag can increase if the source changes faster than the target applies changes. Keep source logs long enough to recover from interruptions.

## Try it

An on-premises SQL database must remain online while a target database is populated and brought up to date before cutover.

<details>
<summary>Show the reasoning</summary>

Use AWS DMS full load plus CDC for supported endpoints. Monitor source and target latency and reconcile records before cutover.

</details>

## AWS documentation

- [AWS documentation · CHAP_Introduction](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html)
- [AWS documentation · what is datasync](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html)
- [AWS documentation · what is aws transfer family](https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html)
