"""Guard the factual claims corrected in Wave B (plan task 17).

Asserts internal consistency between docs and the measured repo surface, NOT
hardcoded literals: if a script legitimately grows/shrinks, the doc must track
it. Would have failed before Wave B (941 vs 943 lines, 7 vs 8 scripts, and an
affirmative CI status-check claim).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _pdf_report_line_count():
    return len(
        (ROOT / "skills" / "geo" / "scripts" / "generate_pdf_report.py")
        .read_text(encoding="utf-8")
        .splitlines()
    )


def _script_count():
    return len(list((ROOT / "skills" / "geo" / "scripts").rglob("*.py")))


def test_agents_md_pdf_report_line_count_matches_actual():
    """AGENTS.md's stated line count for generate_pdf_report.py == measured length."""
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    m = re.search(
        r"generate_pdf_report\.py`\s*[—-]\s*(\d+)\s*lines", text
    )
    assert m, "AGENTS.md line-count claim for generate_pdf_report.py not found"
    claimed = int(m.group(1))
    assert claimed == _pdf_report_line_count(), (
        f"AGENTS.md claims {claimed} lines; file is {_pdf_report_line_count()}"
    )


def test_skills_and_agents_script_count_matches_actual():
    """docs/skills-and-agents.md script count == number of .py files (incl webapp/app.py)."""
    text = (ROOT / "docs" / "skills-and-agents.md").read_text(encoding="utf-8")
    m = re.search(r"(\d+)\s+Python helper scripts", text)
    assert m, "script-count claim not found in docs/skills-and-agents.md"
    claimed = int(m.group(1))
    actual = _script_count()
    assert claimed == actual, (
        f"docs/skills-and-agents.md claims {claimed} scripts; found {actual}"
    )
    # The nested webapp/app.py must be among the counted scripts.
    assert (ROOT / "skills" / "geo" / "scripts" / "webapp" / "app.py").exists()


def test_no_affirmative_ci_status_check_claim():
    """CONTRIBUTING.md and faq.md must not claim CI status checks exist.

    Every 'status check(s)' mention must be negated ('no CI status checks'),
    matching the corrected no-CI reality of this fork.
    """
    for rel in ("CONTRIBUTING.md", "docs/faq.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        low = text.lower()
        mentions = list(re.finditer(r"status checks?", low))
        assert mentions, f"{rel}: expected an explicit 'no CI status checks' statement"
        for m in mentions:
            prefix = low[max(0, m.start() - 24):m.start()]
            assert re.search(r"\bno\s+(ci\s+)?$", prefix), (
                f"{rel}: unnegated status-check claim near: "
                f"...{low[max(0, m.start() - 40):m.end() + 40]}..."
            )
