"""F2-01 regression guard: both legacy installers are fully retired.

Characterize-then-replace. Written against the pre-fix tree where install.sh
and install-win.sh still clone a repo, pip-install requirements, build venvs
and print a false "Installation Complete!" banner for skills they never
deployed. These tests must FAIL on that tree and PASS once both scripts are
reduced to honest LEGACY signpost guidance only.
"""

import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ("install.sh", "install-win.sh")

# Observed at baseline (pre-fix); preserved exactly by the retirement change.
BASELINE_MODES = {"install.sh": 0o755, "install-win.sh": 0o644}

FORBIDDEN_PATTERNS = {
    "git clone": r"git\s+clone",
    "git pull": r"git\s+pull",
    "pip install": r"pip3?\s+install",
    "stdlib venv creation": r"-m\s+venv",
    "uv venv creation": r"\buv\s+venv\b",
    "virtualenv creation": r"\bvirtualenv\b",
    "legacy venv paths": r"VENV_DIR|VENV_PY|\.venv",
    "pip bootstrap": r"get-pip\.py|ensurepip",
    "copy_tree": r"copy_tree",
    "deleted deploy helper": r"update_toolkit\.py",
    "false success banner": r"Installation Complete!",
}

REQUIRED_PATTERNS = {
    "LEGACY marker": r"\bLEGACY\b",
    "pinned npx install guidance": r"npx\s+skills@1\.9\.0\s+add",
    "legacy cleanup guidance": r"bash\s+uninstall\.sh",
    "no-deploy honesty": r"no longer deploy|does not deploy|no longer distribute",
    "prospects directory reference": r"\.geo-prospects",
    "preservation statement": r"preserv",
}


@pytest.mark.parametrize("name", SCRIPTS)
def test_retired_installer_has_no_deploy_code(name):
    src = (ROOT / name).read_text(encoding="utf-8")
    for label, pattern in FORBIDDEN_PATTERNS.items():
        assert not re.search(pattern, src, re.IGNORECASE), (
            f"{name} still contains forbidden {label} ({pattern!r})"
        )


@pytest.mark.parametrize("name", SCRIPTS)
def test_retired_installer_prints_honest_legacy_guidance(name):
    src = (ROOT / name).read_text(encoding="utf-8")
    for label, pattern in REQUIRED_PATTERNS.items():
        assert re.search(pattern, src, re.IGNORECASE), (
            f"{name} is missing required {label} ({pattern!r})"
        )


@pytest.mark.parametrize("name", SCRIPTS)
def test_retired_installer_preserves_shebang_and_permissions(name):
    path = ROOT / name
    src = path.read_text(encoding="utf-8")
    assert src.startswith("#!/usr/bin/env bash"), f"{name} lost its bash shebang"
    actual = os.stat(path).st_mode & 0o777
    assert actual == BASELINE_MODES[name], (
        f"{name} permissions changed: {actual:o} != {BASELINE_MODES[name]:o}"
    )
