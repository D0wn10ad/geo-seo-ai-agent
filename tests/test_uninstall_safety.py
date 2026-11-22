"""Artifact-based safety checks for the npx-aware legacy-cleanup uninstaller.

Todo 15 (npx-skills-migration). These tests read ``uninstall.sh`` as text and
pin the safety contract of the retained legacy-cleanup fallback:

* npx-managed installs are handled via the pinned ``npx skills@1.9.0 remove``
  command, never by shell deletion of npx-owned artifacts.
* shell ``rm`` is restricted to legacy artifacts and is symlink-safe (a symlink
  link is removed, never its resolved target).
* the npx cache, the lock/manifest, symlink targets, and ``~/.geo-prospects/``
  are never passed to ``rm``.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNINSTALL = ROOT / "uninstall.sh"


def _lines():
    return UNINSTALL.read_text(encoding="utf-8").splitlines()


def _text():
    return "\n".join(_lines())


def test_uninstall_script_is_retained():
    assert UNINSTALL.is_file()


def test_references_pinned_npx_remove_command():
    assert "npx skills@1.9.0 remove" in _text()


def test_detects_npx_managed_install_signals():
    text = _text()
    assert "skills-lock.json" in text
    assert ".agents/skills" in text


def test_never_uses_readlink_f():
    # readlink -f resolves a symlink to its target; feeding that to rm would
    # delete a target outside the skill dir (the QA failure scenario).
    assert "readlink -f" not in _text()


def test_no_rm_line_uses_readlink_or_command_substitution():
    for line in _lines():
        if re.search(r"\brm\b", line):
            assert "readlink" not in line, f"rm line references readlink: {line}"
            assert "$(" not in line, f"rm line uses command substitution: {line}"


def test_geo_prospects_is_never_passed_to_rm():
    for line in _lines():
        if ".geo-prospects" in line:
            assert not re.search(r"\brm\b", line), f"rm touches geo-prospects: {line}"


def test_npx_cache_path_is_never_rmd():
    for line in _lines():
        if "rm" in line:
            assert "_npx" not in line, f"rm touches npx cache: {line}"
            assert "npm" not in line, f"rm touches npm path: {line}"


def test_symlink_guard_exists():
    assert any("[ -L" in line or "-L \"$" in line for line in _lines())


def test_symlink_guard_precedes_any_rm_rf():
    lines = _lines()
    guard = next((i for i, line in enumerate(lines) if "[ -L" in line), None)
    rms = [i for i, line in enumerate(lines) if "rm -rf" in line]
    assert guard is not None, "no symlink guard found"
    assert rms, "no legacy rm -rf found"
    assert guard < min(rms), "a rm -rf appears before the symlink guard"


def test_script_distinguishes_npx_managed_from_legacy_paths():
    text = _text()
    lowered = text.lower()
    assert "npx-managed" in lowered or "npx managed" in lowered
    assert "legacy" in lowered
    assert "npx" in lowered
