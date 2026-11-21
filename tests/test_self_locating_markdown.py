"""Filesystem-content tests for the self-locating script-path convention."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
MARKER: str = "<!-- GEO-SCRIPT-RESOLUTION:v1 -->"
HELPER: Path = REPO_ROOT / "geo" / "resolve_scripts.py"
HARDCODED_ROOT: re.Pattern[str] = re.compile(r"\bpython3?\s+(?:geo/)?scripts/")

FALLBACK_TOKENS: tuple[str, ...] = (
    '"$SKILL_DIR/scripts"',
    '"$SKILL_DIR/../geo/scripts"',
    '"$SKILL_DIR/../../geo/scripts"',
    '"$SKILL_DIR/../../../.claude/skills/geo/scripts"',
)

SCRIPT_INVOKING_FILES: frozenset[str] = frozenset(
    {
        "geo/SKILL.md",
        "skills/geo-brand-mentions/SKILL.md",
        "skills/geo-report-pdf/SKILL.md",
        "skills/geo-report-pdf/SKILL.cn.md",
        "skills/geo-schema/SKILL.md",
    }
)


def in_scope_markdown() -> list[Path]:
    files: list[Path] = [REPO_ROOT / "geo" / "SKILL.md"]
    files.extend(sorted((REPO_ROOT / "skills").glob("geo-*/SKILL.md")))
    files.extend(sorted((REPO_ROOT / "skills").glob("geo-*/SKILL.cn.md")))
    return files


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def run_helper(skill_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HELPER), str(skill_dir)],
        capture_output=True,
        text=True,
        check=False,
    )


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


def test_orchestrator_documents_ordered_fallback_list() -> None:
    text = (REPO_ROOT / "geo" / "SKILL.md").read_text(encoding="utf-8")
    missing = [token for token in FALLBACK_TOKENS if token not in text]
    assert not missing, f"geo/SKILL.md is missing fallback candidates: {missing}"


def test_helper_resolves_source_tree_layout() -> None:
    result = run_helper(REPO_ROOT / "skills" / "geo-schema")
    assert result.returncode == 0, result.stderr
    resolved = Path(result.stdout.strip())
    assert resolved.is_dir(), f"resolved path is not a directory: {resolved}"
    assert (resolved / "fetch_page.py").is_file()
    assert resolved.resolve() == (REPO_ROOT / "geo" / "scripts").resolve()


def test_helper_resolves_npx_installed_layout(tmp_path: Path) -> None:
    agents = tmp_path / ".agents" / "skills"
    scripts = agents / "geo" / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "fetch_page.py").write_text("# stub\n", encoding="utf-8")
    (agents / "geo-schema").mkdir(parents=True)

    result = run_helper(agents / "geo-schema")

    assert result.returncode == 0, result.stderr
    assert Path(result.stdout.strip()).resolve() == scripts.resolve()


@pytest.mark.skipif(os.name == "nt", reason="POSIX symlinks required")
def test_helper_resolves_claude_symlink_view(tmp_path: Path) -> None:
    agents = tmp_path / ".agents" / "skills"
    scripts = agents / "geo" / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "fetch_page.py").write_text("# stub\n", encoding="utf-8")
    (agents / "geo-schema").mkdir(parents=True)
    claude = tmp_path / ".claude" / "skills"
    claude.mkdir(parents=True)
    (claude / "geo").symlink_to(agents / "geo", target_is_directory=True)
    (claude / "geo-schema").symlink_to(agents / "geo-schema", target_is_directory=True)

    result = run_helper(claude / "geo-schema")

    assert result.returncode == 0, result.stderr
    resolved = Path(result.stdout.strip())
    assert (resolved / "fetch_page.py").is_file()
    assert resolved.resolve() == scripts.resolve()


@pytest.mark.skipif(os.name == "nt", reason="POSIX symlinks required")
def test_helper_resolves_canonical_claude_path(tmp_path: Path) -> None:
    agents = tmp_path / ".agents" / "skills"
    (agents / "geo-schema").mkdir(parents=True)
    claude = tmp_path / ".claude" / "skills"
    scripts = claude / "geo" / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "fetch_page.py").write_text("# stub\n", encoding="utf-8")
    (claude / "geo-schema").mkdir(parents=True)

    result = run_helper(agents / "geo-schema")

    assert result.returncode == 0, result.stderr
    assert Path(result.stdout.strip()).resolve() == scripts.resolve()


def test_helper_fails_closed_when_no_candidate_exists(tmp_path: Path) -> None:
    result = run_helper(tmp_path / "unrelated-skill")
    assert result.returncode != 0
    assert "GEO scripts root not found" in result.stderr
