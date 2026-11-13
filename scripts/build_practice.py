#!/usr/bin/env python3
"""Build practice pages and the skill map from practice/source (stdlib only).

Usage:
  python3 scripts/build_practice.py          # write generated files and print stats
  python3 scripts/build_practice.py --check  # fail if generated files are stale or quality rules fail
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "practice" / "source"
LETTERS = "ABCDEF"
COUNT_WORDS = {2: "TWO", 3: "THREE"}
MAX_LONGEST_CORRECT = 0.30
DOMAIN_NAMES = {
    "1": "Data Ingestion and Transformation",
    "2": "Data Store Management",
    "3": "Data Operations and Support",
    "4": "Data Security and Governance",
}
SETS = {
    "timed": ("practice/timed-set.md", "practice/timed-answers.md", "Timed practice set", 64),
    "mock": ("practice/full-mock.md", "practice/full-mock-answers.md", "Full-length mock exam", 130),
}


@dataclass
class Skill:
    sid: str
    objective: str
    guide: str
    heading: str
    shared: str

    @property
    def canonical(self) -> str:
        """The first ID of a shared pair counts for both."""
        if self.shared and self.shared < self.sid:
            return self.shared
        return self.sid

    @property
    def link(self) -> str:
        return f"topic-guides/{self.guide}#{slug(self.heading)}"


@dataclass
class Question:
    qid: str
    qset: str
    primary: str
    secondary: list[str]
    answer: list[str]
    stem: str
    options: dict[str, tuple[str, str]] = field(default_factory=dict)
    explain: str = ""

    @property
    def domain(self) -> str:
        return self.primary.split(".")[0]


def slug(title: str) -> str:
    title = re.sub(r"<[^>]*>", "", title)
    return re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")


def load_skills() -> dict[str, Skill]:
    skills = {}
    for line in (SRC / "skills.tsv").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        parts += [""] * (5 - len(parts))
        sid, objective, guide, heading, shared = (p.strip() for p in parts[:5])
        skills[sid] = Skill(sid, objective, guide, heading, shared)
    return skills


def load_questions() -> list[Question]:
    questions = []
    for path in sorted(SRC.glob("*.txt")):
        for block in re.split(r"^=== ", path.read_text(encoding="utf-8"), flags=re.M)[1:]:
            lines = block.rstrip().splitlines()
            qid = lines[0].strip()
            fields: dict[str, str] = {}
            options: dict[str, tuple[str, str]] = {}
            key = None
            for raw in lines[1:]:
                match = re.match(r"^(set|primary|secondary|answer|stem|explain|[A-F]):\s?(.*)$", raw)
                if match:
                    key, value = match.groups()
                    if key in LETTERS:
                        options[key] = value
                    else:
                        fields[key] = value
                elif key:
                    if key in LETTERS:
                        options[key] += " " + raw.strip()
                    else:
                        fields[key] += " " + raw.strip()
            parsed = {}
            for letter, text in options.items():
                body, _, why = text.partition("||")
                parsed[letter] = (body.strip(), why.strip())
            questions.append(
                Question(
                    qid=qid,
                    qset=fields.get("set", "").strip(),
                    primary=fields.get("primary", "").strip(),
                    secondary=[s.strip() for s in fields.get("secondary", "").split(",") if s.strip()],
                    answer=[a.strip() for a in fields.get("answer", "").split(",") if a.strip()],
                    stem=fields.get("stem", "").strip(),
                    options=parsed,
                    explain=fields.get("explain", "").strip(),
                )
            )
    return questions


def validate(questions: list[Question], skills: dict[str, Skill]) -> list[str]:
    errors = []
    seen = set()
    for q in questions:
        where = f"{q.qid}:"
        if q.qid in seen:
            errors.append(f"{where} duplicate id")
        seen.add(q.qid)
        if q.qset not in (*SETS, "bank"):
            errors.append(f"{where} unknown set {q.qset!r}")
        for sid in [q.primary, *q.secondary]:
            if sid not in skills:
                errors.append(f"{where} unknown skill {sid!r}")
        if len(q.options) < 4:
            errors.append(f"{where} needs at least four options")
        expected = LETTERS[: len(q.options)]
        if "".join(sorted(q.options)) != expected:
            errors.append(f"{where} options must be lettered {expected}")
        if not q.answer or any(a not in q.options for a in q.answer):
            errors.append(f"{where} answer {q.answer} not among options")
        if len(q.answer) > 1 and len(q.options) < 5:
            errors.append(f"{where} multiple-response questions need five or more options")
        for letter, (body, why) in q.options.items():
            if not body or not why:
                errors.append(f"{where} option {letter} needs text and a rationale")
        if not q.stem or not q.explain:
            errors.append(f"{where} needs a stem and an explanation")
    return errors


def stats(questions: list[Question], skills: dict[str, Skill]) -> tuple[dict, list[str]]:
    problems = []
    singles = [q for q in questions if len(q.answer) == 1]
    longest = sum(
        1 for q in singles if max(q.options, key=lambda k: len(q.options[k][0])) == q.answer[0]
    )
    rate = longest / len(singles) if singles else 0
    if rate > MAX_LONGEST_CORRECT:
        problems.append(f"correct option is the longest in {rate:.0%} of single-answer questions")
    letters = Counter(a for q in questions for a in q.answer)
    primary = Counter(skills[q.primary].canonical for q in questions)
    appearances = Counter()
    for q in questions:
        for sid in {skills[s].canonical for s in [q.primary, *q.secondary]}:
            appearances[sid] += 1
    canon = sorted({s.canonical for s in skills.values()}, key=skill_key)
    for sid in canon:
        if primary[sid] < 1:
            problems.append(f"skill {sid} is not the primary skill of any question")
        if appearances[sid] < 2:
            problems.append(f"skill {sid} appears in fewer than two questions")
    return {
        "longest_rate": rate,
        "letters": letters,
        "primary": primary,
        "appearances": appearances,
        "objectives": len(canon),
    }, problems


def skill_key(sid: str) -> tuple[int, ...]:
    return tuple(int(p) for p in sid.split("."))


def tags(q: Question, skills: dict[str, Skill], prefix: str) -> str:
    def one(sid: str) -> str:
        s = skills[sid]
        return f"[{sid}]({prefix}{s.link})"

    text = f"Primary skill {one(q.primary)}"
    if q.secondary:
        text += " · also " + ", ".join(one(s) for s in q.secondary)
    return text


def prompt_block(q: Question, number: int) -> list[str]:
    out = [f"## Question {number}", "", q.stem]
    if len(q.answer) > 1:
        out[-1] += f" **Choose {COUNT_WORDS.get(len(q.answer), len(q.answer))}.**"
    out.append("")
    for letter, (body, _) in q.options.items():
        out.append(f"- **{letter}.** {body}")
    out.append("")
    return out


def answer_block(q: Question, number: int, skills: dict[str, Skill], prefix: str) -> list[str]:
    out = [f"## Question {number} · {', '.join(q.answer)}", "", tags(q, skills, prefix), "", q.explain, ""]
    for letter, (_, why) in q.options.items():
        mark = "Correct." if letter in q.answer else "Incorrect."
        out.append(f"- **{letter}.** {mark} {why}")
    out.append("")
    return out


def score_table(qs: list[Question]) -> list[str]:
    counts = Counter(q.domain for q in qs)
    out = ["| Domain | Questions | Score |", "|---|---:|---:|"]
    for d in "1234":
        out.append(f"| {d} · {DOMAIN_NAMES[d]} | {counts[d]} | / {counts[d]} |")
    out.append(f"| **Total** | **{len(qs)}** | **/ {len(qs)}** |")
    return out


def build_set(name: str, qs: list[Question], skills: dict[str, Skill]) -> dict[str, str]:
    qpath, apath, title, minutes = SETS[name]
    multi = sum(1 for q in qs if len(q.answer) > 1)
    qlines = [
        f"# {title}",
        "",
        "[Home](../README.md) · [Answers](" + Path(apath).name + ") · [Exam map](../EXAM-MAP.md) · [Study method](../learning-paths/study-method.md)",
        "",
        "<!-- Generated by scripts/build_practice.py from practice/source. Edit the source, then rebuild. -->",
        "",
        f"Set a timer for **{minutes} minutes** for {len(qs)} questions, the same two minutes per question as the real exam. "
        f"Choose one answer unless the question says otherwise. {multi} questions ask for more than one answer. "
        "Write down your answer and flag every guess before you open the answers.",
        "",
    ]
    alines = [
        f"# {title}: answers",
        "",
        "[Questions](" + Path(qpath).name + ") · [Exam map](../EXAM-MAP.md) · [Progress tracker](../CHECKLIST.md)",
        "",
        "<!-- Generated by scripts/build_practice.py from practice/source. Edit the source, then rebuild. -->",
        "",
        "Score one point for a fully correct answer. For multiple-response questions, every choice must match. "
        "Count correct guesses as review items. Each answer links the official skill and the guide section that teaches it.",
        "",
        *score_table(qs),
        "",
    ]
    for i, q in enumerate(qs, 1):
        qlines += prompt_block(q, i)
        alines += answer_block(q, i, skills, "../")
    return {qpath: "\n".join(qlines).rstrip() + "\n", apath: "\n".join(alines).rstrip() + "\n"}


def build_bank(qs: list[Question], skills: dict[str, Skill]) -> dict[str, str]:
    lines = [
        "# Supplemental question bank",
        "",
        "[Home](../README.md) · [Exam map](../EXAM-MAP.md) · [Timed set](timed-set.md) · [Full mock](full-mock.md)",
        "",
        "<!-- Generated by scripts/build_practice.py from practice/source. Edit the source, then rebuild. -->",
        "",
        "These questions cover skills that the timed set and the mock do not test as a primary skill, plus second questions for "
        "high-weight topics. Use them after you review a guide. Answers are hidden under each question.",
        "",
    ]
    for i, q in enumerate(qs, 1):
        lines += prompt_block(q, i)
        lines += ["<details>", "<summary>Show the answer</summary>", ""]
        lines += answer_block(q, i, skills, "../")[2:]
        lines += ["</details>", ""]
    return {"practice/question-bank.md": "\n".join(lines).rstrip() + "\n"}


def build_coverage(questions: list[Question], skills: dict[str, Skill], st: dict) -> dict[str, str]:
    where = defaultdict(list)
    names = {"timed": "Timed", "mock": "Mock", "bank": "Bank"}
    counters = Counter()
    for q in questions:
        counters[q.qset] += 1
        label = f"{names[q.qset]} {sum(1 for x in questions[: questions.index(q) + 1] if x.qset == q.qset)}"
        where[skills[q.primary].canonical].append(f"**{label}**")
        for s in q.secondary:
            where[skills[s].canonical].append(label)
    lines = [
        "| Skill | Objective | Teaching section | Practice (bold = primary) |",
        "|---|---|---|---|",
    ]
    for sid in sorted(skills, key=skill_key):
        s = skills[sid]
        canon = s.canonical
        practice = ", ".join(where[canon]) if canon == sid else f"Shared with {canon}: " + ", ".join(where[canon])
        lines.append(f"| {sid} | {s.objective} | [{s.heading}]({s.link}) | {practice} |")
    return {"__skill_table__": "\n".join(lines)}


def build_cards() -> dict[str, str]:
    import csv

    rows = list(csv.DictReader((ROOT / "practice" / "recall-cards.csv").open(encoding="utf-8")))
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        first = row["tags"].split()[0]
        groups[first].append(row)
    titles = {"domain1": "Domain 1 · Ingestion and transformation", "domain2": "Domain 2 · Data store management",
              "domain3": "Domain 3 · Operations and support", "domain4": "Domain 4 · Security and governance",
              "exam": "Exam scope"}
    lines = [
        "# Recall cards",
        "",
        "[Home](../README.md) · [Study method](../learning-paths/study-method.md) · [Anki CSV](recall-cards.csv)",
        "",
        "<!-- Generated by scripts/build_practice.py from practice/recall-cards.csv. Edit the CSV, then rebuild. -->",
        "",
        f"{len(rows)} cards. Cover the right column, say the answer aloud, and give an example. "
        "To use spaced repetition, import [recall-cards.csv](recall-cards.csv) into Anki or another flashcard app: "
        "the columns are front, back, and tags.",
        "",
    ]
    for key in ["domain1", "domain2", "domain3", "domain4", "exam"]:
        if key not in groups:
            continue
        lines += [f"## {titles[key]}", "", "| Prompt | Answer to check |", "|---|---|"]
        for row in groups[key]:
            lines.append(f"| {row['front']} | {row['back']} |")
        lines.append("")
    return {"practice/recall-cards.md": "\n".join(lines).rstrip() + "\n"}


def render_exam_map(table: str) -> str:
    path = ROOT / "EXAM-MAP.md"
    text = path.read_text(encoding="utf-8")
    start, end = "<!-- skill-table:start -->", "<!-- skill-table:end -->"
    if start not in text or end not in text:
        raise SystemExit("EXAM-MAP.md is missing the skill-table markers")
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    return f"{head}{start}\n{table}\n{end}{tail}"


def build() -> tuple[dict[str, str], dict, list[str]]:
    skills = load_skills()
    questions = load_questions()
    errors = validate(questions, skills)
    if errors:
        return {}, {}, errors
    st, problems = stats(questions, skills)
    files: dict[str, str] = {}
    for name in SETS:
        files.update(build_set(name, [q for q in questions if q.qset == name], skills))
    files.update(build_bank([q for q in questions if q.qset == "bank"], skills))
    files.update(build_cards())
    table = build_coverage(questions, skills, st)["__skill_table__"]
    files["EXAM-MAP.md"] = render_exam_map(table)
    st["sets"] = Counter(q.qset for q in questions)
    st["domains"] = {
        name: Counter(q.domain for q in questions if q.qset == name) for name in (*SETS, "bank")
    }
    return files, st, problems


def main(argv: list[str]) -> int:
    check = "--check" in argv
    files, st, problems = build()
    if not files:
        print("\n".join(problems))
        return 1
    stale = []
    for rel, content in files.items():
        path = ROOT / rel
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(rel)
        else:
            path.write_text(content, encoding="utf-8")
    print(f"Questions per set: {dict(st['sets'])}")
    for name, counts in st["domains"].items():
        print(f"  {name}: " + ", ".join(f"D{d}={counts[d]}" for d in "1234"))
    print(f"Correct option is the longest: {st['longest_rate']:.0%} of single-answer questions")
    print("Answer letters: " + ", ".join(f"{k}={v}" for k, v in sorted(st["letters"].items())))
    print(f"Objectives covered as primary: {sum(1 for v in st['primary'].values() if v)} of {st['objectives']}")
    for p in problems:
        print(f"PROBLEM: {p}")
    for rel in stale:
        print(f"STALE: {rel} (run python3 scripts/build_practice.py)")
    return 1 if (problems or stale) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
