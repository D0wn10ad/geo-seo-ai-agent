"""Guard for Wave-A triggering-description quality.

Locks in the what+when ("Use when ...") third-person description form applied to
the 14 skills rewritten in Wave A, while leaving the 9 untouched skills exempt
(they still legitimately use second person / other phrasing). The skill list is
derived from the tree, not hardcoded, so adding a skill does not break the test.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# Exactly the 14 skills whose descriptions were rewritten in Wave A (tasks 6-8).
WAVE_A_EDITED = {
    "geo-audit",
    "geo-citability",
    "geo-content",
    "geo-schema",
    "geo-technical",
    "geo-crawlers",
    "geo-ai-visibility",
    "geo-report",
    "geo-report-pdf",
    "geo-brand-mentions",
    "geo-platform-analysis",
    "geo-platform-optimizer",
    "geo-llmstxt",
    "geo-update",
}

SKILL_FILES = sorted((ROOT / "skills").glob("*/SKILL.md"))
FIRST_SECOND_PERSON = re.compile(r"\b(I|you|your|You)\b")


def _frontmatter_lines(path):
    """Return the raw lines of the leading YAML frontmatter block."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return []


def _description(path):
    """Extract the description value from frontmatter (inline or block scalar).

    The venv that runs pytest has no PyYAML, so parse the small frontmatter
    subset by hand: inline `description: text`, folded/literal `description: >`
    / `|`, and bare `description:` followed by indented lines.
    """
    block = _frontmatter_lines(path)
    for i, line in enumerate(block):
        if not line.startswith("description:"):
            continue
        inline = line[len("description:") :].strip()
        if inline and inline not in (">", "|", ">-", "|-", ">+", "|+"):
            return inline
        parts = []
        for j in range(i + 1, len(block)):
            nxt = block[j]
            if nxt.strip() == "":
                continue
            if nxt[0].isspace():
                parts.append(nxt.strip())
            else:
                break
        return " ".join(parts)
    return None


def test_skill_files_discovered():
    """Sanity: discovery works and the edited set is a subset of the tree."""
    names = {p.parent.name for p in SKILL_FILES}
    assert SKILL_FILES, "no skills/*/SKILL.md found"
    assert WAVE_A_EDITED <= names, f"edited skills missing from tree: {WAVE_A_EDITED - names}"


@pytest.mark.parametrize("path", SKILL_FILES, ids=lambda p: p.parent.name)
def test_description_present_and_well_formed(path):
    """Applies to ALL skills: present, <=1024 chars, no angle brackets."""
    desc = _description(path)
    assert desc, f"{path.parent.name}: missing description"
    assert len(desc) <= 1024, f"{path.parent.name}: description too long ({len(desc)})"
    assert "<" not in desc and ">" not in desc, f"{path.parent.name}: angle bracket in description"


@pytest.mark.parametrize(
    "path", [p for p in SKILL_FILES if p.parent.name in WAVE_A_EDITED],
    ids=lambda p: p.parent.name,
)
def test_wave_a_description_has_use_when_and_third_person(path):
    """Applies ONLY to the 14 Wave-A-edited skills."""
    desc = _description(path)
    assert desc, f"{path.parent.name}: missing description"
    assert "Use when" in desc, f"{path.parent.name}: missing 'Use when' clause"
    assert FIRST_SECOND_PERSON.search(desc) is None, (
        f"{path.parent.name}: first/second-person wording in description"
    )
