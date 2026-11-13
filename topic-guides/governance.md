# Lake Formation, Macie, and CloudTrail

[Topic index](README.md) · [Home](../README.md)

## The idea

Governance answers who can see the data, what they can see, and how you can review what happened later.

## How to decide

| Concept | When it matters |
|---|---|
| **Lake Formation** | Grant access to catalog resources and apply supported column or row filters for integrated query engines. Review IAM permissions and how the location is registered. |
| **LF-tags** | Assign tags to catalog resources and grant permissions by tag expressions when many datasets share classifications. |
| **Macie** | Discover sensitive data in eligible S3 objects and surface findings for investigation. |
| **CloudTrail** | Audit AWS API activity. Configure S3 data events if you need an audit record of object-level API calls. |

## Common mistake

If analysts can read raw S3 objects directly, table-level restrictions may leave a second access path. Review bucket access alongside catalog and Lake Formation grants.

## Try it

Two analyst groups use Athena. One can see all fields, and the other must see only de-identified fields.

<details>
<summary>Show the reasoning</summary>

Use Lake Formation grants or filters for the governed table and restrict alternate access to raw objects. Test both personas and review object-level logging needs.

</details>

## AWS documentation

- [AWS documentation · what is lake formation](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html)
- [AWS documentation · what is macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [AWS documentation · logging data events with cloudtrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)
