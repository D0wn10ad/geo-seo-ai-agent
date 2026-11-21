"""Invariants for the committed canonical OpenCode command wrappers.

The updater that used to generate these wrappers is gone. The 21 files in
`geo/commands/` are now the canonical source, so the surviving contract is:
all 21 exist, are well-formed, match the documented command tables, and contain
no unknown wrapper names.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPERS_DIR = ROOT / "geo" / "commands"
ORCHESTRATOR = ROOT / "geo" / "SKILL.md"
README = ROOT / "README.md"

EXPECTED_NAMES = {
    "audit", "brands", "citability", "compare", "compete", "content",
    "crawlers", "distribute", "llmstxt", "matrix", "page", "pipeline",
    "platforms", "proposal", "prospect", "quick", "report-pdf", "report",
    "schema", "technical", "update",
}

# /geo help is a dispatcher-only command (no wrapper); quick/page are the two
# known no-SKILL.md commands, but both DO have canonical wrappers.
TABLE_ONLY_COMMANDS = {"help"}


def wrapper_names(root: Path = ROOT) -> set[str]:
    directory = root / "geo" / "commands"
    return {p.stem[len("geo-"):] for p in directory.glob("geo-*.md") if p.is_file()}


def command_table_names(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"^\|\s*`/geo\s+([a-z][a-z0-9-]*)", text, re.MULTILINE))


def test_canonical_wrapper_dir_has_exactly_21_files():
    assert WRAPPERS_DIR.is_dir(), f"missing canonical wrapper dir {WRAPPERS_DIR}"
    files = sorted(p.name for p in WRAPPERS_DIR.glob("geo-*.md") if p.is_file())
    assert files == sorted(f"geo-{name}.md" for name in EXPECTED_NAMES)


def test_committed_wrappers_have_frontmatter_and_nonempty_body():
    for name in sorted(EXPECTED_NAMES):
        path = WRAPPERS_DIR / f"geo-{name}.md"
        assert path.is_file(), f"missing committed wrapper {path}"
        text = path.read_text(encoding="utf-8")
        assert text.startswith('---\ndescription: "'), path
        assert "\n---\n\n" in text, path
        body = text.split("\n---\n\n", 1)[1]
        assert body.strip(), f"empty wrapper body: {path}"


def test_wrapper_set_matches_command_tables():
    readme = command_table_names(README)
    orchestrator = command_table_names(ORCHESTRATOR)
    assert len(readme) == 22, readme
    assert readme - TABLE_ONLY_COMMANDS == EXPECTED_NAMES
    assert orchestrator == EXPECTED_NAMES
    assert wrapper_names() == EXPECTED_NAMES


def test_no_unknown_wrapper_names():
    assert WRAPPERS_DIR.is_dir(), f"missing canonical wrapper dir {WRAPPERS_DIR}"
    assert wrapper_names() - EXPECTED_NAMES == set()
