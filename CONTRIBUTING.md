# Contributing

Start with a focused issue or pull request. Use the **Fact check** issue template for outdated or wrong claims and the **Learning content request** template for new material.

## Content rules

- Explain the requirement that drives each choice. Define acronyms on first use in each page.
- Every number, limit, default, or quota needs an AWS source link in the same table row or sentence. Say when a quota is adjustable or varies by Region. Never add a number you could not verify.
- Avoid hedge words such as "consider" or "where appropriate" unless you name the condition that decides.
- Write original scenarios. Keep recalled exam questions and copied commercial practice questions out of the repository.
- Use fictional records only. Lab data must not contain real people's information.
- House style: plain English, short sentences, no em dashes.
- Update the "Last verified" line at the bottom of any guide you fact-check.

## Practice questions

Questions live in `practice/source/*.txt`, one block per question:

```text
=== M66
set: mock            # timed, mock, or bank
primary: 2.3.5       # exactly one official skill ID
secondary: 2.3.4     # optional, comma-separated
answer: B            # or "A, D" for multiple response (needs 5+ options)
stem: Scenario text...
A: Option text || Why it is wrong
B: Option text || Why it is right
C: ...
D: ...
explain: The deciding requirement in one or two sentences.
```

Then run `python3 scripts/build_practice.py`. It regenerates the timed set, mock, bank, recall cards, and the skill table in `EXAM-MAP.md`, and it fails if:

- any of the 115 distinct objectives is not the primary skill of some question, or appears in fewer than two;
- the correct option is the longest one in more than 30% of single-answer questions.

Write distractors that would partly work. Keep option lengths similar.

## Checks to run before a pull request

```bash
python3 scripts/check_repository.py
python3 scripts/build_practice.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
cfn-lint labs/hands-on/*/template.yaml   # if you changed a lab template
```

Continuous integration runs the same checks plus an external link check on every pull request and weekly.
