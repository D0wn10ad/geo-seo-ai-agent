"""TDD for Todo 13: prune unused deps and drop playwright installer branches.

Fails first on the unpruned tree (requirements.txt still carries playwright,
Pillow and validators; installer, README and docs still mention Playwright),
then passes once the pruning edits land. Asserts observable outcomes in the
scoped distribution surface, not implementation details.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "requirements.txt"

KEEP_DEPS = {
    "beautifulsoup4>=4.12.0,<5.0.0",
    "requests>=2.34.2,<3.0.0",
    "lxml>=6.1.1,<7.0.0",
    "urllib3>=2.7.0,<3.0.0",
    "reportlab>=4.4.0,<5.0.0",
    "flask>=3.1.3,<4.0.0",
    "rich>=13.0.0,<14.0.0",
}
DROPPED_NAMES = ("playwright", "pillow", "validators")
TEXT_SUFFIXES = {".md", ".sh", ".py", ".txt", ".yaml", ".yml", ".json"}


def _scoped_surface():
    files = [ROOT / "README.md"]
    for subdir in ("skills", "docs"):
        files.extend(
            p for p in (ROOT / subdir).rglob("*")
            if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES
        )
    return files


def test_requirements_has_exactly_the_seven_keep_deps():
    lines = [
        line.strip()
        for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert set(lines) == KEEP_DEPS


def test_requirements_has_no_dropped_deps():
    text = REQUIREMENTS.read_text(encoding="utf-8").lower()
    for name in DROPPED_NAMES:
        assert name not in text, f"{name} still in requirements.txt"


def test_scoped_surface_has_no_playwright_references():
    offenders = [
        str(path.relative_to(ROOT))
        for path in _scoped_surface()
        if "playwright" in path.read_text(encoding="utf-8", errors="ignore").lower()
    ]
    assert offenders == [], f"playwright references remain in: {offenders}"


def test_scoped_surface_has_no_validator_or_pillow_install_references():
    offenders = []
    for path in _scoped_surface():
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for name in ("validators", "pillow"):
            if name in text:
                offenders.append(f"{path.relative_to(ROOT)}:{name}")
    assert offenders == [], f"dropped dep references remain in: {offenders}"


def test_ssr_rendered_dom_step_is_retained():
    text = (ROOT / "skills" / "geo-technical" / "SKILL.md").read_text(encoding="utf-8")
    assert "Compare the raw HTML" in text
    assert "rendered DOM" in text
