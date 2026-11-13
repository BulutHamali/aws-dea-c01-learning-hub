#!/usr/bin/env python3
"""Validate repository navigation, coverage, and guide structure (stdlib only).

Checks relative link targets and heading anchors, that every topic guide is in the
topic index and the study plans, that guides keep the standard sections, and that
Markdown prose has no em dashes (house style). It does not fetch external URLs or
verify the technical truth of study material.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")
HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
REQUIRED_SECTIONS = ("## Common mistake", "## Commonly confused", "## Try it", "## AWS documentation")
PLANS = ("learning-paths/4-week-plan.md", "learning-paths/6-week-plan.md")


def prose(text: str) -> str:
    """Drop fenced code blocks so sample links and headings are ignored."""
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is None:
            if match:
                fence = match.group(1)
            else:
                lines.append(line)
        elif match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
            fence = None
    return "\n".join(lines)


def anchors(text: str) -> set[str]:
    found: set[str] = set()
    for title in HEADING.findall(prose(text)):
        title = re.sub(r"!?\[([^]]*)\]\([^)]*\)", r"\1", title)
        title = re.sub(r"<[^>]*>", "", title)
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in found:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        found.add(candidate)
    return found


def markdown_files(root: Path) -> list[Path]:
    return [p for p in sorted(root.rglob("*.md")) if ".git" not in p.relative_to(root).parts]


def check_links(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors = []
    for source in markdown_files(root):
        for raw in LINK.findall(prose(source.read_text(encoding="utf-8"))):
            target = raw.strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            destination = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            label = str(source.relative_to(root))
            if not destination.is_relative_to(root):
                errors.append(f"{label}: link escapes repository: {target}")
            elif not destination.exists():
                errors.append(f"{label}: missing link target: {target}")
            elif parsed.fragment and destination.suffix == ".md":
                if unquote(parsed.fragment) not in anchors(destination.read_text(encoding="utf-8")):
                    errors.append(f"{label}: missing heading anchor: {target}")
    return errors


def guides(root: Path) -> list[Path]:
    return [g for g in sorted((root / "topic-guides").glob("*.md")) if g.name != "README.md"]


def linked(source: Path) -> set[str]:
    return {urlsplit(l.strip("<>")).path for l in LINK.findall(prose(source.read_text(encoding="utf-8")))}


def check_index(root: Path = ROOT) -> list[str]:
    index = root / "topic-guides/README.md"
    if not index.is_file():
        return ["Missing topic index"]
    targets = linked(index)
    return [f"Topic index omits guide: {g.name}" for g in guides(root) if g.name not in targets]


def check_plans(root: Path = ROOT) -> list[str]:
    errors = []
    for rel in PLANS:
        plan = root / rel
        if not plan.is_file():
            errors.append(f"Missing study plan: {rel}")
            continue
        targets = linked(plan)
        errors += [
            f"{rel} omits topic guide: {g.name}"
            for g in guides(root)
            if f"../topic-guides/{g.name}" not in targets
        ]
    return errors


def check_structure(root: Path = ROOT) -> list[str]:
    errors = []
    for guide in guides(root):
        text = prose(guide.read_text(encoding="utf-8"))
        for section in REQUIRED_SECTIONS:
            if not re.search(rf"^{re.escape(section)}\s*$", text, re.MULTILINE):
                errors.append(f"{guide.name}: missing section '{section}'")
        if "Last verified against AWS documentation" not in text:
            errors.append(f"{guide.name}: missing 'Last verified' line")
    return errors


def check_style(root: Path = ROOT) -> list[str]:
    errors = []
    for source in markdown_files(root):
        for number, line in enumerate(prose(source.read_text(encoding="utf-8")).splitlines(), 1):
            if "—" in line:
                errors.append(f"{source.relative_to(root)}:{number}: em dash in prose")
    return errors


def main() -> int:
    errors = check_links() + check_index() + check_plans() + check_structure() + check_style()
    if errors:
        print("Repository checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository checks passed: links, anchors, index and plan coverage, guide structure, style.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
