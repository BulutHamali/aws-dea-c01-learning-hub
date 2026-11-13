# Study method and exam-day practice

[Home](../README.md) · [Four-week plan](4-week-plan.md) · [Timed practice](../practice/timed-set.md)

## A 35-minute session

| Time | Activity | What you produce |
|---|---|---|
| 5 min | Recall yesterday’s material before opening a guide | A rough diagram or two service differences |
| 10 min | Read one guide and trace the worked example | One sentence about each service’s job |
| 10 min | Solve a new scenario with the answer hidden | Your choice and the requirement that decides it |
| 10 min | Compare your reasoning and schedule a retry | An error-log entry and a specific retry prompt |

Retry misses after roughly two days and a week. Mix similar services across sessions once you understand them individually. For example, alternate an Athena question with a Redshift Spectrum question and say what makes the second one different. Use the [recall cards](../practice/recall-cards.md) for short sessions.

## Read scenario questions in three passes

1. **Read the requested outcome.** Do they need a replayable source, lower scan cost, finer access, or easier operations?
2. **Underline constraints.** Look for the input type, required latency, replay, current tooling, operational burden, and recovery. For “choose two,” make sure both choices satisfy the same design.
3. **Test the plausible answers.** Ask where the data lives, what actually reads or writes it, and how the choice meets the strongest constraint. If you have to assume an extra component, compare that effort with the other options.

## Simulate the test

AWS lists 65 questions in 130 minutes, with single- and multiple-response questions. Fifteen of the 65 are unscored, and you cannot tell which. Use the [32-question timed set](../practice/timed-set.md) in 64 minutes midway through your plan and the [65-question full mock](../practice/full-mock.md) in 130 minutes near the end. AWS reports a scaled score, so use your practice percentage to find weak areas. Reserve time to review flagged questions, and answer every question because there is no penalty for guessing.

Before booking or sitting the exam, take the official AWS practice material where available. Use this hub's [skill map](../EXAM-MAP.md#skill-by-skill-map) to revisit the objectives behind your misses.

[Official AWS exam overview and preparation](https://aws.amazon.com/certification/certified-data-engineer-associate/)
