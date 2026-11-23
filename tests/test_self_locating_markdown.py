"""Filesystem-content tests for the self-locating script-path convention."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
MARKER: str = "<!-- GEO-SCRIPT-RESOLUTION:v1 -->"
HARDCODED_ROOT: re.Pattern[str] = re.compile(r"\bpython3?\s+(?:geo/)?scripts/")

SCRIPT_INVOKING_FILES: frozenset[str] = frozenset(
    {
        "skills/geo/SKILL.md",
        "skills/geo-brand-mentions/SKILL.md",
        "skills/geo-report-pdf/SKILL.md",
        "skills/geo-report-pdf/references/cn.md",
        "skills/geo-schema/SKILL.md",
    }
)


def in_scope_markdown() -> list[Path]:
    files: list[Path] = [REPO_ROOT / "skills" / "geo" / "SKILL.md"]
    files.extend(sorted((REPO_ROOT / "skills").glob("geo-*/SKILL.md")))
    files.extend(sorted((REPO_ROOT / "skills").glob("geo-*/references/cn.md")))
    return files


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


@pytest.mark.parametrize("path", in_scope_markdown(), ids=rel)
def test_no_hardcoded_script_root_invocations(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    offenders = [line.strip() for line in text.splitlines() if HARDCODED_ROOT.search(line)]
    assert not offenders, f"{rel(path)} hardcodes a script root: {offenders}"


@pytest.mark.parametrize("name", sorted(SCRIPT_INVOKING_FILES))
def test_script_markdown_declares_resolution_convention(name: str) -> None:
    text = (REPO_ROOT / name).read_text(encoding="utf-8")
    assert MARKER in text, f"{name} missing convention marker {MARKER}"
    assert "GEO_SCRIPTS" in text, f"{name} does not use the GEO_SCRIPTS variable"
    assert "SKILL_DIR" in text, f"{name} does not anchor resolution to SKILL_DIR"


def test_orchestrator_documents_single_literal_script_path() -> None:
    text = (REPO_ROOT / "skills" / "geo" / "SKILL.md").read_text(encoding="utf-8")
    assert '"$SKILL_DIR/../geo/scripts"' in text
    assert "resolve_scripts.py" not in text


def test_canonical_script_root_exists() -> None:
    scripts = REPO_ROOT / "skills" / "geo" / "scripts"
    assert scripts.is_dir()
    assert (scripts / "fetch_page.py").is_file()


def test_region_resolver_uses_single_references_search_dir() -> None:
    text = (REPO_ROOT / "skills" / "geo" / "scripts" / "region_resolver.py").read_text(encoding="utf-8")
    assert re.search(r"""REGION_SEARCH_DIRS\s*=\s*\(\s*['"]\.\./references['"]\s*,?\s*\)""", text)


def test_cn_variants_manifest_uses_references_paths() -> None:
    text = (REPO_ROOT / "skills" / "geo" / "references" / "regions" / "cn-variants.json").read_text(encoding="utf-8")
    assert '"variant_file": "references/cn.md"' in text
    assert '"regions/cn/' not in text
    assert '"references/regions/cn/' in text


def test_no_resolve_scripts_helper_in_canonical_tree() -> None:
    assert not (REPO_ROOT / "geo" / "resolve_scripts.py").exists()
    assert not (REPO_ROOT / "skills" / "geo" / "scripts" / "resolve_scripts.py").exists()


def test_script_invoking_files_use_canonical_skills_paths() -> None:
    for name in sorted(SCRIPT_INVOKING_FILES):
        assert name.startswith("skills/"), name
        assert (REPO_ROOT / name).is_file(), name


# Dependency-error hints must point at the sibling bootstrap script and resolve
# it relative to __file__, so the hint works from any install root.
DEPENDENCY_HINT_SCRIPTS: frozenset[str] = frozenset(
    {
        "fetch_page.py",
        "citability_scorer.py",
        "brand_scanner.py",
        "llmstxt_generator.py",
        "generate_pdf_report.py",
    }
)
STALE_HINT: str = "pip install -r requirements.txt"
BOOTSTRAP_HINT: str = "bootstrap_env.sh"
SELF_LOCATION_PATTERN: str = "os.path.dirname(os.path.abspath(__file__))"


def test_dependency_error_hint_is_self_locating() -> None:
    for name in sorted(DEPENDENCY_HINT_SCRIPTS):
        path = REPO_ROOT / "skills" / "geo" / "scripts" / name
        text = path.read_text(encoding="utf-8")
        assert STALE_HINT not in text, f"{name} still shows stale '{STALE_HINT}' hint"
        assert BOOTSTRAP_HINT in text, f"{name} hint does not reference bootstrap_env.sh"
        assert SELF_LOCATION_PATTERN in text, f"{name} hint does not self-locate via __file__"
