"""Post-migration artifact checks for the pinned npx skill-distribution flow.

Pins the distributed-tree observable after the legacy git-clone/copy/rewrite
updater is removed: no legacy updater identifiers survive in `geo/` or
`skills/`, and `skills/geo-update/SKILL.md` documents pinned npx update
semantics for this fork.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_IDENTIFIERS = (
    "update_toolkit.py",
    "clone_or_pull_repo",
    "copy_tree",
    "copy_files",
    "patch_installed_markdown",
    "rewrite_runtime_markdown",
    "--runtime-python",
    "--runtime-scripts-root",
)
TEXT_SUFFIXES = {".md", ".sh", ".py", ".txt", ".yaml", ".yml", ".json"}
DISTRIBUTED_DIRS = ("geo", "skills")
UPDATE_SKILL = ROOT / "skills" / "geo-update" / "SKILL.md"


def _distributed_files():
    for subdir in DISTRIBUTED_DIRS:
        for path in (ROOT / subdir).rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path


def test_legacy_updater_file_is_absent():
    assert not (ROOT / "geo" / "scripts" / "update_toolkit.py").exists()


def test_distributed_tree_has_no_legacy_updater_identifiers():
    offenders = []
    for path in _distributed_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for identifier in LEGACY_IDENTIFIERS:
            if identifier in text:
                offenders.append(f"{path.relative_to(ROOT)}:{identifier}")
    assert offenders == [], f"legacy updater identifiers remain: {offenders}"


def test_geo_update_documents_pinned_npx_check_and_update():
    text = UPDATE_SKILL.read_text(encoding="utf-8")
    assert "skills check" in text
    assert "skills update" in text
    assert "skills@1.9.0" in text
    assert "D0wn10ad/geo-seo-ai-agent" in text


def test_geo_update_has_no_stale_upstream_claim():
    text = UPDATE_SKILL.read_text(encoding="utf-8")
    assert "zubair-trabzada" not in text
