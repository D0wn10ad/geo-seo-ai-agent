"""Invariants for the canonical command surface after wrapper consolidation.

The 21 `geo/commands/` wrappers were deleted. The orchestrator skill table in
`skills/geo/SKILL.md` is now the canonical command source, and no wrapper
directory should exist.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = ROOT / "skills" / "geo" / "SKILL.md"
README = ROOT / "README.md"
LEGACY_WRAPPERS_DIR = ROOT / "geo" / "commands"

EXPECTED_NAMES = {
    "audit", "brands", "citability", "compare", "compete", "content",
    "crawlers", "distribute", "llmstxt", "matrix", "page", "pipeline",
    "platforms", "proposal", "prospect", "quick", "report-pdf", "report",
    "schema", "technical", "update",
}

TABLE_ONLY_COMMANDS = {"help"}


def command_table_names(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"^\|\s*`/geo\s+([a-z][a-z0-9-]*)", text, re.MULTILINE))


def test_orchestrator_table_lists_all_21_commands():
    assert ORCHESTRATOR.is_file(), f"missing orchestrator {ORCHESTRATOR}"
    names = command_table_names(ORCHESTRATOR)
    assert names == EXPECTED_NAMES
    assert len(names) == 21


def test_no_geo_commands_wrapper_directory():
    assert not LEGACY_WRAPPERS_DIR.exists(), f"legacy wrapper dir still present: {LEGACY_WRAPPERS_DIR}"


def test_readme_command_table_matches_orchestrator():
    readme = command_table_names(README)
    orchestrator = command_table_names(ORCHESTRATOR)
    assert len(readme) == 22, readme
    assert readme - TABLE_ONLY_COMMANDS == EXPECTED_NAMES
    assert orchestrator == EXPECTED_NAMES


def test_no_unknown_command_names_in_orchestrator():
    names = command_table_names(ORCHESTRATOR)
    assert names - EXPECTED_NAMES == set()
    assert EXPECTED_NAMES - names == set()
