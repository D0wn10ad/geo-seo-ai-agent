"""Regression guard for the root AGENTS.md after the pinned-npx migration.

F2-02: the legacy deploy-time updater and its suite were deleted, while the
root AGENTS.md kept describing them as active tooling. ``test_npx_docs.py``
only scans README.md + docs/*.md, so the root document was an unguarded blind
spot. These assertions pin the root document to the committed npx-first layout.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"

DELETED_TOOLING = ("update_toolkit.py", "test_update_toolkit.py")
REMOVAL_MARKERS = ("removed", "deleted", "retired", "no longer", "dropped", "absent")


def _agents_text():
    if not AGENTS.is_file():
        pytest.fail(f"missing root AGENTS.md at {AGENTS}")
    return AGENTS.read_text(encoding="utf-8")


def _numbered_lines():
    return list(enumerate(_agents_text().splitlines(), 1))


def test_npx_first_reality_is_true_on_disk():
    wrappers = sorted((ROOT / "geo" / "commands").glob("geo-*.md"))
    assert len(wrappers) == 21, f"expected 21 committed wrappers, found {len(wrappers)}"
    assert not (ROOT / "geo" / "scripts" / "update_toolkit.py").exists()
    assert not (ROOT / "tests" / "test_update_toolkit.py").exists()


def test_agents_md_documents_pinned_npx_add():
    assert "npx skills@1.9.0 add" in _agents_text()


@pytest.mark.parametrize("token", DELETED_TOOLING)
def test_deleted_tooling_is_not_described_as_active(token):
    offenders = []
    for line_no, line in _numbered_lines():
        if token not in line:
            continue
        if not any(marker in line.lower() for marker in REMOVAL_MARKERS):
            offenders.append(f"AGENTS.md:{line_no}: {line.strip()}")
    assert offenders == [], (
        f"{token} is described as current tooling without a removal marker:\n"
        + "\n".join(offenders)
    )


def test_opencode_is_not_claimed_missing_or_updater_generated():
    offenders = []
    for line_no, line in _numbered_lines():
        low = line.lower()
        if ".opencode/" not in low:
            continue
        if "does not exist" in low or "generated at deploy time by" in low:
            offenders.append(f"AGENTS.md:{line_no}: {line.strip()}")
    assert offenders == [], "stale .opencode/ claim:\n" + "\n".join(offenders)


def test_opencode_is_described_as_local_deploy_artifact():
    text = _agents_text()
    assert ".opencode/" in text
    assert "deploy artifact" in text.lower()


def test_canonical_wrappers_are_documented_as_committed():
    text = _agents_text()
    assert "geo/commands/" in text
    assert "geo/commands/geo-*.md" in text


def test_legacy_installers_are_documented_as_retired():
    text = _agents_text()
    assert "LEGACY" in text
    assert "install.sh" in text
    assert "install-win.sh" in text


def test_uv_bootstrap_is_documented():
    text = _agents_text()
    assert "bootstrap_env.sh" in text
    assert "install_uv.sh" in text
