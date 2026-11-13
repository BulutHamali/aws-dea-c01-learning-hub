"""Exercise the repository checks with broken fixtures, not only happy paths."""

import tempfile
import unittest
from pathlib import Path

from check_repository import anchors, check_index, check_links, check_plans, check_structure, check_style

GOOD_GUIDE = (
    "# G\n## Common mistake\n## Commonly confused\n## Try it\n## AWS documentation\n"
    "*Last verified against AWS documentation: November 2026.*\n"
)


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, text):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def test_missing_target(self):
        self.write("README.md", "[missing](missing.md)")
        self.assertIn("missing link target", check_links(self.root)[0])

    def test_missing_fragment(self):
        self.write("README.md", "# Existing\n[missing](#absent)")
        self.assertIn("missing heading anchor", check_links(self.root)[0])

    def test_valid_cross_file_fragment_with_punctuation(self):
        self.write("README.md", "[ok](guide.md#copy-staging-and-unload)")
        self.write("guide.md", "## COPY, staging, and UNLOAD\n")
        self.assertEqual(check_links(self.root), [])

    def test_escape_is_rejected(self):
        self.write("README.md", "[escape](../outside.md)")
        self.assertIn("escapes repository", check_links(self.root)[0])

    def test_external_and_fenced_examples_are_ignored(self):
        self.write("README.md", "[web](https://example.org/a#b)\n```md\n[example](missing.md)\n```\n")
        self.assertEqual(check_links(self.root), [])

    def test_duplicate_headings(self):
        self.assertEqual(anchors("## Hello\n## Hello\n```md\n## Fake\n```\n"), {"hello", "hello-1"})

    def test_index_omission(self):
        self.write("topic-guides/README.md", "# Index")
        self.write("topic-guides/s3.md", GOOD_GUIDE)
        self.assertEqual(check_index(self.root), ["Topic index omits guide: s3.md"])

    def test_plan_omission(self):
        self.write("topic-guides/s3.md", GOOD_GUIDE)
        self.write("learning-paths/4-week-plan.md", "[S3](../topic-guides/s3.md)")
        self.write("learning-paths/6-week-plan.md", "# Plan")
        self.assertEqual(check_plans(self.root), ["learning-paths/6-week-plan.md omits topic guide: s3.md"])

    def test_structure(self):
        self.write("topic-guides/s3.md", GOOD_GUIDE)
        self.write("topic-guides/bad.md", "# Bad\n## Try it\n")
        errors = check_structure(self.root)
        self.assertTrue(all(e.startswith("bad.md") for e in errors))
        self.assertIn("bad.md: missing 'Last verified' line", errors)

    def test_em_dash_in_prose_but_not_code(self):
        self.write("README.md", "Plain text — here\n```\ncode — ok\n```\n")
        self.assertEqual(len(check_style(self.root)), 1)


if __name__ == "__main__":
    unittest.main()
