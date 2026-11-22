"""Executable, artifact-based checks for the npx-aware legacy uninstaller.

The sibling ``test_uninstall_safety.py`` pins source-text properties of
``uninstall.sh``. A logic regression can keep every one of those assertions green
while changing runtime behaviour, so this module executes the real script inside
isolated sandboxes and observes the filesystem outcomes that matter: npx-managed
installs delete nothing, and legacy cleanup removes only legacy artifacts.

Set ``GEO_UNINSTALL_SH`` to execute an alternate script (used by the mutation
proof in the task evidence); it defaults to the repository's ``uninstall.sh``.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNINSTALL = Path(os.environ.get("GEO_UNINSTALL_SH", str(ROOT / "uninstall.sh")))
PINNED_REMOVE = "npx skills@1.9.0 remove"


def _run(script: Path, cwd: Path, home: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["XDG_CONFIG_HOME"] = str(home / ".config")
    env["XDG_CACHE_HOME"] = str(home / ".cache")
    return subprocess.run(
        ["bash", str(script)],
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def _preserved_sentinels(tmp_path: Path) -> tuple[Path, list[Path]]:
    home = tmp_path / "home"
    cache = home / ".cache" / "geo-seo-ai-agent" / "venv" / "pyvenv.cfg"
    prospects = home / ".geo-prospects" / "prospects.json"
    cache.parent.mkdir(parents=True)
    prospects.parent.mkdir(parents=True)
    cache.write_text("venv sentinel\n", encoding="utf-8")
    prospects.write_text("prospects sentinel\n", encoding="utf-8")
    return home, [cache, prospects]


def test_npx_mode_deletes_nothing_and_guides_to_pinned_remove(tmp_path: Path) -> None:
    home, preserved = _preserved_sentinels(tmp_path)
    install = tmp_path / "install"
    agents = install / ".agents" / "skills" / "geo"
    agents.mkdir(parents=True)
    skill = agents / "SKILL.md"
    skill.write_text("npx skill sentinel\n", encoding="utf-8")
    lock = install / "skills-lock.json"
    lock.write_text("{}\n", encoding="utf-8")
    claude = install / ".claude" / "skills"
    claude.mkdir(parents=True)
    link = claude / "geo"
    link.symlink_to(agents, target_is_directory=True)
    legacy = home / ".claude" / "skills" / "geo-legacy" / "SKILL.md"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("legacy sentinel\n", encoding="utf-8")

    proc = _run(UNINSTALL, install, home)

    assert proc.returncode == 0, proc.stderr
    assert "Detected an npx-managed install" in proc.stdout
    assert PINNED_REMOVE in proc.stdout
    assert "deletes nothing" in proc.stdout
    assert "No shell removal performed" in proc.stdout
    for path in [lock, skill, link, legacy, *preserved]:
        assert path.exists(), f"npx mode deleted {path}"


def test_npx_mode_detected_via_claude_symlink_alone(tmp_path: Path) -> None:
    home, preserved = _preserved_sentinels(tmp_path)
    cwd = tmp_path / "elsewhere"
    cwd.mkdir()
    target = home / ".agents" / "skills" / "geo"
    target.mkdir(parents=True)
    (target / "SKILL.md").write_text("target sentinel\n", encoding="utf-8")
    links = home / ".claude" / "skills"
    links.mkdir(parents=True)
    link = links / "geo"
    link.symlink_to("../../.agents/skills/geo", target_is_directory=True)

    proc = _run(UNINSTALL, cwd, home)

    assert proc.returncode == 0, proc.stderr
    assert "Detected an npx-managed install" in proc.stdout
    assert PINNED_REMOVE in proc.stdout
    for path in [link, target / "SKILL.md", *preserved]:
        assert path.exists(), f"npx mode deleted {path}"


def test_legacy_mode_removes_only_legacy_artifacts_and_preserves_data(tmp_path: Path) -> None:
    home, preserved = _preserved_sentinels(tmp_path)
    cwd = tmp_path / "elsewhere"
    cwd.mkdir()
    legacy_skill = home / ".claude" / "skills" / "geo" / "SKILL.md"
    legacy_skill.parent.mkdir(parents=True)
    legacy_skill.write_text("legacy\n", encoding="utf-8")
    legacy_agent = home / ".claude" / "agents" / "geo-audit.md"
    legacy_agent.parent.mkdir(parents=True)
    legacy_agent.write_text("legacy\n", encoding="utf-8")
    opencode_agent = home / ".config" / "opencode" / "agents" / "geo-audit.md"
    opencode_agent.parent.mkdir(parents=True)
    opencode_agent.write_text("legacy\n", encoding="utf-8")
    opencode_command = home / ".config" / "opencode" / "commands" / "geo-audit.md"
    opencode_command.parent.mkdir(parents=True)
    opencode_command.write_text("legacy\n", encoding="utf-8")
    target_dir = tmp_path / "external-target" / "geo-real"
    target_dir.mkdir(parents=True)
    target_file = target_dir / "SKILL.md"
    target_file.write_text("must survive\n", encoding="utf-8")
    link = home / ".claude" / "skills" / "geo-audit"
    link.symlink_to(target_dir, target_is_directory=True)

    proc = _run(UNINSTALL, cwd, home)

    assert proc.returncode == 0, proc.stderr
    assert "Legacy artifacts removed" in proc.stdout
    assert "Detected an npx-managed install" not in proc.stdout
    for path in (legacy_skill, legacy_agent, opencode_agent, opencode_command, link):
        assert not path.exists(), f"legacy artifact survived: {path}"
    for path in [target_file, *preserved]:
        assert path.exists(), f"cleanup deleted a protected path: {path}"
