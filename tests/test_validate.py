"""Exercise malformed package inputs and portable link boundaries."""

import tempfile
import unittest
from pathlib import Path

from scripts.validate import (
    validate_cases, validate_frontmatter, validate_links, validate_repository,
)


class PackageValidationTests(unittest.TestCase):
    """Protect package discovery and local resource resolution."""

    def test_valid_frontmatter(self) -> None:
        """Accept required metadata and string-valued optional metadata."""
        contents = (
            '---\nname: example\ndescription: Design systems\nmetadata:\n  version: "1"\n---\n'
        )
        self.assertEqual(validate_frontmatter(contents, "example"), [])

    def test_invalid_frontmatter(self) -> None:
        """Reject malformed YAML, wrong identity, missing text, and typed metadata."""
        cases = [
            "No frontmatter", "---\n[\n---\n", "---\n- item\n---\n",
            "---\nname: other\ndescription: Design systems\n---\n",
            "---\nname: Example\ndescription: Design systems\n---\n",
            "---\nname: example\n---\n",
            "---\nname: example\ndescription: 3\n---\n",
            "---\nname: example\ndescription: Design\nmetadata:\n  version: 1\n---\n",
        ]
        for contents in cases:
            with self.subTest(contents=contents):
                self.assertTrue(validate_frontmatter(contents, "example"))

    def test_local_links_and_fenced_examples(self) -> None:
        """Accept portable resources and ignore external links and fenced examples."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "reference.md").write_text("A reference", encoding="utf-8")
            document = root / "SKILL.md"
            document.write_text(
                '[local](reference.md#section) [web](https://example.com) [anchor](#a)\n'
                '```md\n[example](missing.md)\n```\n', encoding="utf-8",
            )
            self.assertEqual(validate_links(document, root), [])

    def test_missing_and_escaping_links(self) -> None:
        """Detect missing files, parent escapes, absolute links, and symlink escapes."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "package"
            package.mkdir()
            outside = root / "outside.md"
            outside.write_text("Outside", encoding="utf-8")
            (package / "escape.md").symlink_to(outside)
            document = package / "SKILL.md"
            document.write_text(
                f"[missing](missing.md) [parent](../outside.md) "
                f"[absolute]({outside}) [symlink](escape.md)\n", encoding="utf-8",
            )
            self.assertEqual(len(validate_links(document, package)), 4)

    def test_evaluation_inputs(self) -> None:
        """Accept usable prompts and reject duplicates, blank prompts, and invalid IDs."""
        case = {"id": "booking", "prompt": "Design a booking system"}
        self.assertEqual(validate_cases({"version": 1, "cases": [case]}), [])
        for data in (
            None, {}, {"version": 1, "cases": []},
            {"version": 1, "cases": [case, case]},
            {"version": 1, "cases": [{"id": "../bad", "prompt": " "}]},
            {"version": 1, "cases": [None]},
        ):
            with self.subTest(data=data):
                self.assertTrue(validate_cases(data))

    def test_missing_required_files(self) -> None:
        """Report incomplete packages without raising a file-reading exception."""
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(validate_repository(Path(directory)))

    def test_invalid_function_arguments(self) -> None:
        """Fail clearly when callers supply invalid paths or contents."""
        with self.assertRaises(ValueError):
            validate_frontmatter(None, "example")
        with self.assertRaises(ValueError):
            validate_links("SKILL.md", Path("."))
        with self.assertRaises(ValueError):
            validate_repository(Path("/nonexistent-design-skill-validation-root"))


if __name__ == "__main__":
    unittest.main()
