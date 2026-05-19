"""Tests for update_toolkit.py — cross-platform installer/updater.

Touch points tested:
  - Platform detection (claude-code, opencode, both, none)
  - --all-platforms override
  - --target and --upstream flags
  - Sub-skills path correctness (regression: skills/skills/ bug)
  - Agent installation per platform
  - OpenCode command installation
  - Git clone vs pull behavior
  - Missing source directory handling
  - copy_tree and copy_files edge cases
"""

import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, call, ANY

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from update_toolkit import (
    platform_info,
    detect_platforms,
    clone_or_pull_repo,
    copy_tree,
    copy_files,
    install_for_platform,
    install_all_platforms,
    parse_args,
    main,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def repo(tmp_path):
    """Create a minimal mock repository structure."""
    r = tmp_path / "repo"

    (r / "geo" / "SKILL.md").mkdir(parents=True)

    for name in ["geo-audit", "geo-citability", "geo-crawlers"]:
        d = r / "skills" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"# {name}")

    plat = r / "platform"
    plat.mkdir()
    (plat / "SKILL.md").write_text("# platform")
    (plat / "TOOL-MAP.md").write_text("# tool map")

    (r / "scripts").mkdir(parents=True)
    (r / "scripts" / "fetch_page.py").write_text("print('ok')")
    (r / "docs").mkdir(parents=True)
    (r / "docs" / "README.md").write_text("# docs")

    (r / "agents").mkdir(parents=True)
    (r / "agents" / "geo-content.md").write_text("# agent")
    (r / "agents" / "geo-schema.md").write_text("# schema agent")

    oa = r / ".opencode" / "agents"
    oa.mkdir(parents=True)
    (oa / "geo-content.md").write_text("# oc agent")
    oc = r / ".opencode" / "commands"
    oc.mkdir(parents=True)
    (oc / "geo-audit.md").write_text("# oc command")

    return r


# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------

class TestPlatformDetection:
    def test_detect_both(self):
        with (
            patch("update_toolkit.HOME", MagicMock()),
            patch("update_toolkit.XDG_CONFIG", MagicMock()),
        ):
            with patch.object(Path, "is_dir", return_value=True):
                with patch.object(Path, "is_file", return_value=True):
                    result = detect_platforms()
        assert "claude-code" in result
        assert "opencode" in result

    def test_detect_only_claude(self):
        with patch.object(Path, "is_dir", side_effect=[True, False]):
            with patch.object(Path, "is_file", return_value=False):
                result = detect_platforms()
        assert result == ["claude-code"]

    def test_detect_only_opencode(self):
        with patch.object(Path, "is_dir", side_effect=[False, False]):
            with patch.object(Path, "is_file", return_value=True):
                result = detect_platforms()
        assert result == ["opencode"]

    def test_detect_none(self):
        with patch.object(Path, "is_dir", return_value=False):
            with patch.object(Path, "is_file", return_value=False):
                result = detect_platforms()
        assert result == []


# ---------------------------------------------------------------------------
# clone_or_pull_repo
# ---------------------------------------------------------------------------

class TestCloneOrPullRepo:
    def test_clone_new_repo(self, tmp_path):
        target = tmp_path / "new-repo"
        with patch("update_toolkit.subprocess.run") as mock_run:
            result = clone_or_pull_repo("https://example.com/repo.git", target)
        assert result == target
        mock_run.assert_called_once_with(
            ["git", "clone", "https://example.com/repo.git", str(target)],
            check=True,
        )

    def test_pull_existing_repo(self, tmp_path):
        target = tmp_path / "existing-repo"
        target.mkdir()
        with patch("update_toolkit.subprocess.run") as mock_run:
            result = clone_or_pull_repo("https://example.com/repo.git", target)
        assert result == target
        mock_run.assert_called_once_with(
            ["git", "pull", "--ff-only"],
            cwd=target,
            check=False,
        )


# ---------------------------------------------------------------------------
# copy_tree
# ---------------------------------------------------------------------------

class TestCopyTree:
    def test_copies_directory(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "file.txt").write_text("hello")
        dst = tmp_path / "dst" / "sub"
        copy_tree(src, dst, "Test")
        assert dst.exists()
        assert (dst / "file.txt").read_text() == "hello"

    def test_replaces_existing_dst(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "file.txt").write_text("new")
        dst = tmp_path / "dst"
        dst.mkdir()
        (dst / "old.txt").write_text("old")
        copy_tree(src, dst, "Test")
        assert not (dst / "old.txt").exists()

    def test_skip_missing_src(self, tmp_path, capsys):
        src = tmp_path / "nonexistent"
        dst = tmp_path / "dst"
        copy_tree(src, dst, "Missing")
        captured = capsys.readouterr()
        assert "SKIP: Missing" in captured.out
        assert not dst.exists()


# ---------------------------------------------------------------------------
# copy_files
# ---------------------------------------------------------------------------

class TestCopyFiles:
    def test_copies_matching_files(self, tmp_path):
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "a.md").write_text("a")
        (src_dir / "b.md").write_text("b")
        (src_dir / "c.py").write_text("c")
        dst_dir = tmp_path / "dst"
        copy_files(src_dir, dst_dir, "*.md", "Markdown files")
        assert (dst_dir / "a.md").exists()
        assert (dst_dir / "b.md").exists()
        assert not (dst_dir / "c.py").exists()

    def test_skip_missing_src_dir(self, tmp_path, capsys):
        src_dir = tmp_path / "nonexistent"
        dst_dir = tmp_path / "dst"
        copy_files(src_dir, dst_dir, "*.md", "Missing")
        captured = capsys.readouterr()
        assert "SKIP: Missing" in captured.out


# ---------------------------------------------------------------------------
# install_for_platform — CRITICAL: sub-skills path correctness
# ---------------------------------------------------------------------------

class TestInstallForPlatform:
    """These tests verify the fix for the skills/skills/ path bug."""

    def test_sub_skills_go_to_skills_dst_directly(self, repo, tmp_path):
        """Each sub-skill dir must be a direct child of skills_dst,
        NOT nested under skills_dst/skills/."""
        skills_dst = tmp_path / "skills"
        agents_dst = tmp_path / "agents"

        with (
            patch("update_toolkit.CLAUDE_SKILLS", skills_dst),
            patch("update_toolkit.CLAUDE_AGENTS", agents_dst),
            patch("update_toolkit.OPENCODE_AGENTS", tmp_path / "oc-agents"),
            patch("update_toolkit.OPENCODE_COMMANDS", tmp_path / "oc-commands"),
        ):
            install_for_platform(repo, "claude-code")

        # Sub-skills directly under skills_dst/
        assert (skills_dst / "geo-audit").is_dir()
        assert (skills_dst / "geo-citability").is_dir()
        assert (skills_dst / "geo-crawlers").is_dir()

        # NOT under skills_dst/skills/ (the old bug)
        assert not (skills_dst / "skills").exists()

    def test_claude_agents_copied(self, repo, tmp_path):
        skills_dst = tmp_path / "skills"
        agents_dst = tmp_path / "agents"

        with (
            patch("update_toolkit.CLAUDE_SKILLS", skills_dst),
            patch("update_toolkit.CLAUDE_AGENTS", agents_dst),
        ):
            install_for_platform(repo, "claude-code")

        assert (agents_dst / "geo-content.md").exists()
        assert (agents_dst / "geo-schema.md").exists()

    def test_opencode_agents_copied(self, repo, tmp_path):
        skills_dst = tmp_path / "skills"
        oc_agents = tmp_path / "oc-agents"
        oc_commands = tmp_path / "oc-commands"

        with (
            patch("update_toolkit.CLAUDE_SKILLS", skills_dst),
            patch("update_toolkit.OPENCODE_AGENTS", oc_agents),
            patch("update_toolkit.OPENCODE_COMMANDS", oc_commands),
        ):
            install_for_platform(repo, "opencode")

        assert (oc_agents / "geo-content.md").exists()
        assert (oc_commands / "geo-audit.md").exists()

    def test_platform_adapter_copied(self, repo, tmp_path):
        skills_dst = tmp_path / "skills"

        with (
            patch("update_toolkit.CLAUDE_SKILLS", skills_dst),
            patch("update_toolkit.CLAUDE_AGENTS", tmp_path / "agents"),
        ):
            install_for_platform(repo, "claude-code")

        assert (skills_dst / "platform" / "SKILL.md").exists()
        assert (skills_dst / "platform" / "TOOL-MAP.md").exists()

    def test_scripts_and_docs_copied(self, repo, tmp_path):
        skills_dst = tmp_path / "skills"

        with (
            patch("update_toolkit.CLAUDE_SKILLS", skills_dst),
            patch("update_toolkit.CLAUDE_AGENTS", tmp_path / "agents"),
        ):
            install_for_platform(repo, "claude-code")

        assert (skills_dst / "scripts" / "fetch_page.py").exists()
        assert (skills_dst / "docs" / "README.md").exists()

    def test_opencode_no_claude_agents(self, repo, tmp_path):
        """OpenCode install must NOT install to claude agent dir."""
        skills_dst = tmp_path / "skills"
        claude_agents = tmp_path / "claude-agents"

        with (
            patch("update_toolkit.CLAUDE_SKILLS", skills_dst),
            patch("update_toolkit.CLAUDE_AGENTS", claude_agents),
            patch("update_toolkit.OPENCODE_AGENTS", tmp_path / "oc-agents"),
            patch("update_toolkit.OPENCODE_COMMANDS", tmp_path / "oc-commands"),
        ):
            install_for_platform(repo, "opencode")

        assert not (claude_agents / "geo-content.md").exists()

    def test_claude_code_no_opencode_commands(self, repo, tmp_path):
        """Claude Code install must NOT install OpenCode commands."""
        skills_dst = tmp_path / "skills"
        oc_commands = tmp_path / "oc-commands"

        with (
            patch("update_toolkit.CLAUDE_SKILLS", skills_dst),
            patch("update_toolkit.CLAUDE_AGENTS", tmp_path / "agents"),
            patch("update_toolkit.OPENCODE_COMMANDS", oc_commands),
        ):
            install_for_platform(repo, "claude-code")

        assert not oc_commands.exists()

    def test_unknown_platform_prints_warning(self, repo, capsys):
        install_for_platform(repo, "some-other-ai")
        captured = capsys.readouterr()
        assert "Unknown platform" in captured.out


# ---------------------------------------------------------------------------
# install_all_platforms
# ---------------------------------------------------------------------------

class TestInstallAllPlatforms:
    def test_installs_each_platform(self, repo):
        platforms = ["claude-code", "opencode"]
        with patch("update_toolkit.install_for_platform") as mock_install:
            install_all_platforms(repo, platforms)
        mock_install.assert_has_calls([
            call(repo, "claude-code"),
            call(repo, "opencode"),
        ])

    def test_no_platforms_no_error(self, repo):
        with patch("update_toolkit.install_for_platform") as mock_install:
            install_all_platforms(repo, [])
        mock_install.assert_not_called()


# ---------------------------------------------------------------------------
# main() integration via parse_args
# ---------------------------------------------------------------------------

class TestMain:
    def test_all_platforms_flag_overrides_detection(self):
        test_args = ["prog", "--all-platforms"]
        with (
            patch.object(sys, "argv", test_args),
            patch("update_toolkit.detect_platforms", return_value=[]),
            patch("update_toolkit.clone_or_pull_repo"),
            patch("update_toolkit.install_all_platforms") as mock_install,
            patch("update_toolkit.tempfile.TemporaryDirectory") as mock_tmp,
        ):
            mock_tmp.return_value.__enter__.return_value = "/tmp/geo-seo-xxx"
            main()

        # Should install for both despite detect_platforms returning []
        args, _ = mock_install.call_args
        assert mock_install.called
        # The platforms were overridden to ["claude-code", "opencode"]

    def test_no_platforms_exits(self):
        test_args = ["prog"]
        with (
            patch.object(sys, "argv", test_args),
            patch("update_toolkit.detect_platforms", return_value=[]),
        ):
            with pytest.raises(SystemExit):
                main()

    def test_upstream_flag_passed_to_clone(self):
        test_args = ["prog", "--upstream", "https://example.com/fork.git", "--target", "/tmp/test-target"]
        with (
            patch.object(sys, "argv", test_args),
            patch("update_toolkit.detect_platforms", return_value=["claude-code"]),
            patch("update_toolkit.clone_or_pull_repo") as mock_clone,
            patch("update_toolkit.install_all_platforms"),
        ):
            main()

        mock_clone.assert_called_once_with(
            "https://example.com/fork.git",
            Path("/tmp/test-target"),
        )

    def test_target_skip_pull_if_not_exists(self, tmp_path):
        """When --target is given and dir doesn't exist, clone is called."""
        target = tmp_path / "fresh-target"
        test_args = ["prog", "--target", str(target)]
        with (
            patch.object(sys, "argv", test_args),
            patch("update_toolkit.detect_platforms", return_value=["claude-code"]),
            patch("update_toolkit.clone_or_pull_repo") as mock_clone,
            patch("update_toolkit.install_all_platforms"),
        ):
            main()

        assert mock_clone.called


# ---------------------------------------------------------------------------
# copy_tree edge cases
# ---------------------------------------------------------------------------

class TestCopyTreeEdgeCases:
    def test_src_is_file_not_dir(self, tmp_path, capsys):
        src = tmp_path / "file.txt"
        src.write_text("data")
        dst = tmp_path / "dst"
        copy_tree(src, dst, "FileSrc")
        captured = capsys.readouterr()
        assert "SKIP: FileSrc" in captured.out
        assert not dst.exists()

    def test_dst_parent_created(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "x.txt").write_text("x")
        dst = tmp_path / "a" / "b" / "c"
        copy_tree(src, dst, "Deep path")
        assert dst.is_dir()
        assert (dst / "x.txt").exists()

    def test_repo_url_constant(self):
        from update_toolkit import REPO_URL
        assert "D0wn10ad" in REPO_URL
        assert "geo-seo-ai-agent" in REPO_URL
