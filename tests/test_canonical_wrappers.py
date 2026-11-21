"""Characterization + invariants for canonical OpenCode command wrappers.

Pins the observable that the generator used to emit: 21 wrappers from
_GEO_COMMANDS, each with description frontmatter and a non-empty body. After the
canonical-wrapper migration the same observable is pinned against the committed
files in geo/commands/ using an in-test replica of the generator's exact byte
format (the generator itself is intentionally gone).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "geo" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from update_toolkit import _GEO_COMMANDS  # noqa: E402

WRAPPERS_DIR = ROOT / "geo" / "commands"
UPDATER = SCRIPTS / "update_toolkit.py"
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


def render(description: str, body: str) -> str:
    """Byte-exact replica of generate_opencode_commands' output format."""
    return (
        "---\n"
        f'description: "{description}"\n'
        "---\n"
        "\n"
        f"{body}\n"
    )


def wrapper_names(root: Path = ROOT) -> set[str]:
    directory = root / "geo" / "commands"
    return {p.stem[len("geo-"):] for p in directory.glob("geo-*.md") if p.is_file()}


def command_table_names(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"^\|\s*`/geo\s+([a-z][a-z0-9-]*)", text, re.MULTILINE))


def test_generator_spec_yields_21_wrappers_with_frontmatter_and_body():
    assert set(_GEO_COMMANDS) == EXPECTED_NAMES
    for name, (description, body) in _GEO_COMMANDS.items():
        text = render(description, body)
        assert text.startswith('---\ndescription: "')
        assert "\n---\n\n" in text
        assert text.split("\n---\n\n", 1)[1].strip()


def test_canonical_wrapper_dir_has_exactly_21_files():
    assert WRAPPERS_DIR.is_dir(), f"missing canonical wrapper dir {WRAPPERS_DIR}"
    files = sorted(p.name for p in WRAPPERS_DIR.glob("geo-*.md") if p.is_file())
    assert files == sorted(f"geo-{name}.md" for name in EXPECTED_NAMES)


def test_committed_wrappers_byte_identical_to_generator_spec():
    for name, (description, body) in _GEO_COMMANDS.items():
        path = WRAPPERS_DIR / f"geo-{name}.md"
        assert path.is_file(), f"missing committed wrapper {path}"
        assert path.read_text(encoding="utf-8") == render(description, body)


def test_generation_stripped_from_updater():
    src = UPDATER.read_text(encoding="utf-8")
    assert "def generate_opencode_commands" not in src
    assert "generate_opencode_commands(" not in src
    assert "def generate_opencode_agents" not in src
    assert "generate_opencode_agents(" not in src


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
