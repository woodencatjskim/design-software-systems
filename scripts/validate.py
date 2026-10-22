"""Validate this repository's portable skill package and basic documentation links."""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

SKILL_NAME = "design-software-systems"
FRONTMATTER_FIELDS = {
    "name", "description", "license", "compatibility", "metadata", "allowed-tools",
}
LINK_PATTERN = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")


def validate_frontmatter(text: str, directory_name: str) -> list[str]:
    """Check required discovery metadata and the entrypoint size.

    Args:
        text: Complete SKILL.md contents.
        directory_name: Name of its containing directory.

    Returns:
        Actionable errors, or an empty list for valid metadata.
    """
    if not isinstance(text, str) or not isinstance(directory_name, str) or not directory_name:
        raise ValueError("Skill contents and a nonempty directory name must be strings")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        return ["SKILL.md must begin with a YAML frontmatter block"]
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        return [f"Invalid frontmatter YAML: {error}"]
    if not isinstance(metadata, dict):
        return ["Frontmatter must be a mapping"]
    errors = []
    name = metadata.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("name must contain lowercase ASCII letters/digits separated by hyphens")
    elif len(name) > 64 or name != directory_name:
        errors.append("name must match its directory and be at most 64 characters")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("description must be a nonempty string of at most 1024 characters")
    if set(metadata) - FRONTMATTER_FIELDS:
        errors.append("Frontmatter contains unsupported fields")
    extra = metadata.get("metadata", {})
    if not isinstance(extra, dict) or any(
        not isinstance(key, str) or not isinstance(value, str) for key, value in extra.items()
    ):
        errors.append("metadata must map strings to strings")
    if len(text.splitlines()) > 500:
        errors.append("Keep SKILL.md within the repository's 500-line entrypoint limit")
    return errors


def validate_links(document: Path, boundary: Path) -> list[str]:
    """Check basic inline local Markdown links, including symlink escapes.

    Args:
        document: Existing Markdown file to inspect.
        boundary: Directory that all its local links must stay inside.

    Returns:
        Missing or unsafe link errors. External URLs and anchors are not checked.
    """
    if not isinstance(document, Path) or not isinstance(boundary, Path):
        raise ValueError("document and boundary must be pathlib Paths")
    errors = []
    fence = None
    for line_number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
        # Examples inside fenced code are literal text rather than navigation.
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        for match in LINK_PATTERN.finditer(line):
            target = match.group(1).split(' "', 1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            local_path = Path(unquote(parsed.path))
            resolved = (document.parent / local_path).resolve()
            location = f"{document.name}:{line_number}"
            if local_path.is_absolute() or not resolved.is_relative_to(boundary.resolve()):
                errors.append(f"{location}: local link leaves package boundary: {target}")
            elif not resolved.exists():
                errors.append(f"{location}: missing local link: {target}")
    return errors


def validate_cases(data: object) -> list[str]:
    """Check evaluation input structure without scoring answer wording.

    Args:
        data: Parsed evaluation JSON.

    Returns:
        Schema and duplicate identifier errors.
    """
    if not isinstance(data, dict) or data.get("version") != 1:
        return ["Evaluation data must be an object with version 1"]
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        return ["Evaluation cases must be a nonempty list"]
    errors = []
    identifiers = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"Case {index} must be an object")
            continue
        identifier = case.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9-]+", identifier):
            errors.append(f"Case {index} needs a safe, nonempty identifier")
        elif identifier in identifiers:
            errors.append(f"Duplicate case identifier: {identifier}")
        else:
            identifiers.add(identifier)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"Case {index} needs a nonempty prompt")
    return errors


def validate_repository(root: Path) -> list[str]:
    """Validate required files, package metadata, links, and evaluation inputs.

    Args:
        root: Existing repository directory.

    Returns:
        All discovered errors, including file and parsing failures.
    """
    if not isinstance(root, Path) or not root.is_dir():
        raise ValueError("root must be an existing repository directory")
    skill = root / "skills" / SKILL_NAME
    required = [
        root / "LICENSE", root / "README.md", root / "README.ko.md",
        root / "evals/prompts.json", skill / "SKILL.md", skill / "LICENSE",
        skill / "agents/openai.yaml",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.is_file()]
    if missing:
        return [f"Missing required file: {path}" for path in missing]
    try:
        errors = validate_frontmatter((skill / "SKILL.md").read_text(encoding="utf-8"), SKILL_NAME)
        if (root / "LICENSE").read_bytes() != (skill / "LICENSE").read_bytes():
            errors.append("Installed skill LICENSE differs from repository LICENSE")
        interface = yaml.safe_load((skill / "agents/openai.yaml").read_text(encoding="utf-8"))
        interface = interface.get("interface") if isinstance(interface, dict) else None
        if not isinstance(interface, dict) or any(
            not isinstance(interface.get(key), str) or not interface[key].strip()
            for key in ("display_name", "short_description", "default_prompt")
        ):
            errors.append("openai.yaml needs nonempty interface strings")
        case_text = (root / "evals/prompts.json").read_text(encoding="utf-8")
        errors.extend(validate_cases(json.loads(case_text)))
        # Scan only published documentation; do not traverse agent caches or dependencies.
        documents = list(root.glob("*.md"))
        for folder in ("skills", "docs", "examples", "evals"):
            documents.extend((root / folder).rglob("*.md"))
        for document in documents:
            boundary = skill if document.is_relative_to(skill) else root
            errors.extend(validate_links(document, boundary))
        return errors
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as error:
        return [f"Cannot validate repository files: {error}"]


def main() -> int:
    """Run repository validation.

    Returns:
        Zero for success or one for invalid files or arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = validate_repository(args.root.resolve())
    except ValueError as error:
        errors = [str(error)]
    for error in errors:
        print(f"ERROR: {error}")
    if not errors:
        print("PASS: package metadata, local links, license, and evaluation input structure")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
