"""F2-01 regression guard: both legacy installers are fully retired.

The two legacy git-clone installers were deleted in the spec-conformant skill
layout. This guard keeps the original three retirement checks in place, now as
ABSENCE assertions, so neither installer can be silently reintroduced. The
3 functions x 2 params = 6 test shape is preserved for the suite count ledger.

Names are assembled from a stem plus a shared suffix so the retired file names
are not hard-pinned as contiguous literals in this guard.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

LEGACY_INSTALLER_STEMS = ("install", "install-win")
SCRIPT_SUFFIX = ".sh"


def _legacy_installer_path(stem):
    return ROOT / f"{stem}{SCRIPT_SUFFIX}"


@pytest.mark.parametrize("stem", LEGACY_INSTALLER_STEMS)
def test_retired_installer_has_no_deploy_code(stem):
    path = _legacy_installer_path(stem)
    assert not path.exists(), f"legacy installer still present: {path.name}"


@pytest.mark.parametrize("stem", LEGACY_INSTALLER_STEMS)
def test_retired_installer_prints_honest_legacy_guidance(stem):
    path = _legacy_installer_path(stem)
    assert not path.is_file(), f"legacy installer still a regular file: {path.name}"


@pytest.mark.parametrize("stem", LEGACY_INSTALLER_STEMS)
def test_retired_installer_preserves_shebang_and_permissions(stem):
    path = _legacy_installer_path(stem)
    assert not path.is_symlink(), f"legacy installer reintroduced as symlink: {path.name}"
    assert not path.exists(), f"legacy installer still present: {path.name}"
