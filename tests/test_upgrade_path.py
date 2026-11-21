"""Upgrade path regression tests for legacy -> npx migration.

Proves the documented contract:
- an in-place npx-style add overwrites a stale same-named skill directory
  (models installer cleanAndCreateDirectory: rm -rf then recreate), while
- legacy-only artifacts outside that directory (old .venv, legacy agents/*.md)
  are NOT auto-removed by the add, and
- ~/.geo-prospects/ stand-ins remain intact in both Path A (uninstall-first)
  and Path B (in-place add + manual legacy cleanup).
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNINSTALL = ROOT / "uninstall.sh"
PINNED_ADD = (
    "npx skills@1.9.0 add -a claude-code -a opencode -y "
    "https://github.com/D0wn10ad/geo-seo-ai-agent.git"
)


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _clean_and_create_directory(path: Path) -> None:
    """Mirror vercel-labs/skills src/installer.ts cleanAndCreateDirectory."""
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True, exist_ok=True)


def _run_uninstall(cwd: Path, home: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["XDG_CONFIG_HOME"] = str(home / ".config")
    env["XDG_CACHE_HOME"] = str(home / ".cache")
    return subprocess.run(
        ["bash", str(UNINSTALL)],
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def test_inplace_add_overwrites_skill_dir_but_not_legacy_artifacts(tmp_path: Path) -> None:
    """Path B: add refreshes same-named skill dir; legacy artifacts survive."""
    home = tmp_path / "home"
    install = tmp_path / "install"
    skills_root = install / ".agents" / "skills"
    skill_dir = skills_root / "geo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("stale skill content\n", encoding="utf-8")
    (skill_dir / "old_extra.txt").write_text("stale extra\n", encoding="utf-8")

    legacy_venv = home / ".claude" / "skills" / "geo" / ".venv" / "pyvenv.cfg"
    legacy_venv.parent.mkdir(parents=True)
    legacy_venv.write_text("legacy venv sentinel\n", encoding="utf-8")
    legacy_agent = home / ".claude" / "agents" / "geo-audit.md"
    legacy_agent.parent.mkdir(parents=True)
    legacy_agent.write_text("legacy agent sentinel\n", encoding="utf-8")
    stale_cmd = home / ".config" / "opencode" / "commands" / "geo-audit.md"
    stale_cmd.parent.mkdir(parents=True)
    stale_cmd.write_text("stale command wrapper\n", encoding="utf-8")
    prospects = home / ".geo-prospects" / "prospects.json"
    prospects.parent.mkdir(parents=True)
    prospects.write_text('{"sentinel": "keep"}\n', encoding="utf-8")
    prospects_sha = _sha256(prospects)

    # In-place npx-style add replaces ONLY the managed skill directory.
    _clean_and_create_directory(skill_dir)
    (skill_dir / "SKILL.md").write_text("fresh skill content\n", encoding="utf-8")

    assert (skill_dir / "SKILL.md").read_text(encoding="utf-8") == "fresh skill content\n"
    assert not (skill_dir / "old_extra.txt").exists(), "stale file must be removed by overwrite"
    assert legacy_venv.exists(), "legacy .venv is outside skill dir; add must not remove it"
    assert legacy_agent.exists(), "legacy agents/*.md must not be auto-removed by add"
    assert stale_cmd.exists(), "stale opencode command wrapper must survive until manual cleanup"
    assert prospects.exists() and _sha256(prospects) == prospects_sha

    # Manual cleanup checklist (documented Path B follow-up) removes legacy-only artifacts.
    shutil.rmtree(home / ".claude" / "skills" / "geo" / ".venv")
    legacy_agent.unlink()
    stale_cmd.unlink()
    assert not legacy_venv.exists()
    assert not legacy_agent.exists()
    assert not stale_cmd.exists()
    assert prospects.exists() and _sha256(prospects) == prospects_sha, "cleanup must preserve prospects"


def test_path_a_uninstall_then_add_preserves_prospects(tmp_path: Path) -> None:
    """Path A: uninstall.sh legacy cleanup removes legacy artifacts, keeps prospects."""
    home = tmp_path / "home"
    cwd = tmp_path / "elsewhere"
    cwd.mkdir()
    legacy_skill = home / ".claude" / "skills" / "geo" / "SKILL.md"
    legacy_skill.parent.mkdir(parents=True)
    legacy_skill.write_text("legacy\n", encoding="utf-8")
    legacy_venv = home / ".claude" / "skills" / "geo" / ".venv" / "pyvenv.cfg"
    legacy_venv.parent.mkdir(parents=True)
    legacy_venv.write_text("venv\n", encoding="utf-8")
    legacy_agent = home / ".claude" / "agents" / "geo-audit.md"
    legacy_agent.parent.mkdir(parents=True)
    legacy_agent.write_text("agent\n", encoding="utf-8")
    prospects = home / ".geo-prospects" / "prospects.json"
    prospects.parent.mkdir(parents=True)
    prospects.write_text('{"keep": true}\n', encoding="utf-8")
    prospects_sha = _sha256(prospects)

    proc = _run_uninstall(cwd, home)

    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "Legacy artifacts removed" in proc.stdout
    assert not legacy_skill.exists()
    assert not legacy_venv.exists()
    assert not legacy_agent.exists()
    assert prospects.exists() and _sha256(prospects) == prospects_sha

    # After cleanup, a fresh pinned add would install into a clean state (command documented).
    assert PINNED_ADD  # sanity: pinned command constant defined for doc checks


def test_upgrade_docs_document_both_paths_and_preserve_prospects() -> None:
    readme = _read("README.md")
    getting_started = _read("docs/getting-started.md")
    combined = readme + "\n" + getting_started

    assert "## Upgrading an older install" in readme
    assert "Upgrading an older install" in getting_started

    # Path A (recommended): uninstall first, then pinned add, then bootstrap, then verify.
    for text in (readme, getting_started):
        assert "bash uninstall.sh" in text
        assert PINNED_ADD in text
        assert "bootstrap_env.sh" in text

    # Path B (in-place): add overwrites skill dirs, then manual cleanup checklist.
    assert "Path B" in readme or "in-place" in readme.lower()
    assert "legacy `.venv`" in readme or "legacy .venv" in readme or "`.venv`" in readme
    assert "agents/*.md" in readme or "geo-*.md" in readme
    assert ".opencode/commands" in readme or "command wrappers" in readme.lower()

    # Prospects preserved in both paths and uninstall is not a hard prerequisite.
    lower = combined.lower()
    assert "~/.geo-prospects/" in combined
    assert "preserv" in lower
    assert "hard prerequisite" not in lower
    assert "strictly required" not in lower
    assert "mandatory uninstall" not in lower
