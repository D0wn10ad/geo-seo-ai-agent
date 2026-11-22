from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOC_FILES = ["README.md", "docs/*.md"]

PINNED_ADD = (
    "npx skills@1.9.0 add -a claude-code -a opencode -y "
    "https://github.com/D0wn10ad/geo-seo-ai-agent.git"
)


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def _docs_text():
    parts = [_read("README.md")]
    parts.extend(p.read_text(encoding="utf-8") for p in sorted((ROOT / "docs").glob("*.md")))
    return "\n".join(parts)


def _quick_start():
    text = _read("README.md")
    return text[text.index("## Quick Start"):text.index("## Commands")]


def test_readme_quick_start_uses_pinned_npx_add():
    assert PINNED_ADD in _quick_start()


def test_readme_quick_start_has_no_curl_installer_default():
    section = _quick_start()
    assert "curl -fsSL" not in section
    assert "install.sh | bash" not in section


def test_legacy_installers_are_explicitly_labeled():
    readme = _read("README.md")
    assert "uninstall.sh" in readme
    assert "legacy" in readme.lower()


def test_getting_started_has_no_stale_upstream_install_paths():
    text = _read("docs/getting-started.md")
    assert "zubair-trabzada/geo-seo-claude/main/install" not in text
    assert "git clone https://github.com/zubair-trabzada/geo-seo-claude.git" not in text


@pytest.mark.parametrize("rel", ["README.md"] + [str(p.relative_to(ROOT)) for p in sorted((ROOT / "docs").glob("*.md"))])
def test_no_doc_references_deleted_update_toolkit(rel):
    assert "update_toolkit.py" not in _read(rel)


def test_pinning_and_check_update_documented():
    text = _docs_text()
    assert "npx skills@1.9.0 check" in text
    assert "npx skills@1.9.0 update" in text
    assert "pin" in text.lower()


def test_uv_bootstrap_documented():
    text = _read("docs/getting-started.md")
    assert "skills/geo/scripts/bootstrap_env.sh" in text
    assert "skills/geo/scripts/install_uv.sh" in text
    assert "Python 3.10+" in text


def test_os_support_documented():
    text = _docs_text()
    for token in ("macOS", "Linux", "Windows", "Git Bash"):
        assert token in text


def test_legacy_uninstall_fallback_documented():
    text = _docs_text()
    assert "npx skills@1.9.0 remove" in text
    assert "legacy" in text.lower()


def test_no_offline_airgap_or_playwright_claims():
    text = _docs_text().lower()
    for token in ("offline", "air-gap", "airgap", "playwright"):
        assert token not in text


def test_python_version_is_3_10_plus():
    text = _docs_text()
    assert "Python 3.10+" in text
    assert "Python 3.8+" not in text
    assert "Python 3.9+" not in text


def test_no_git_required_for_installer_claim():
    section = _quick_start()
    assert "Required for installer" not in section


def test_gitignore_ignores_local_npx_install_artifacts():
    text = _read(".gitignore")
    assert "skills-lock.json" in text
    assert ".agents/" in text
    assert "*.pdf" in text


def test_legitimate_fork_attributions_are_kept():
    readme = _read("README.md")
    assert "This is a fork of [zubair-trabzada/geo-seo-claude]" in readme
    assert "Original work © 2026 Zubair Trabzada" in readme
    assert "zubair-trabzada/geo-seo-claude" in _read("FORK_CHANGELOG.md")
