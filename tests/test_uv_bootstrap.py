"""TDD for Todo 11: vendored Astral uv skill + pinned idempotent installer.

Baseline characterization records the pre-migration state observed on HEAD
ca2c67b0da4cc7325489e030bc599bea5bba1d77: no skills/uv/SKILL.md, no pinned
installer helper, and install.sh carrying only the raw unpinned hint.

The behaviour tests below fail first, then pass once the vendored skill and the
guarded installer are added. All PATH-sensitive tests use an isolated scratch
bin so the system uv at ~/.local/bin/uv cannot satisfy the presence guard.
"""

import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDORED_SKILL = ROOT / "skills" / "uv" / "SKILL.md"
INSTALLER = ROOT / "geo" / "scripts" / "install_uv.sh"
INSTALL_SH = ROOT / "install.sh"

EXPECTED_PIN = "0.13.9"
UPSTREAM_URL = (
    "https://raw.githubusercontent.com/astral-sh/agent-plugins/main/"
    "plugins/astral/skills/uv/SKILL.md"
)
UPSTREAM_SHA256 = "96dcc38d6dd80deb2f54ee82a3a15987d6441cdb234452fbc4d43499c3461287"

PRE_MIGRATION_ABSENCE = {
    "skills/uv/SKILL.md": False,
    "geo/scripts/install_uv.sh": False,
}


def test_baseline_pre_migration_absence_snapshot():
    assert PRE_MIGRATION_ABSENCE == {
        "skills/uv/SKILL.md": False,
        "geo/scripts/install_uv.sh": False,
    }


def test_baseline_install_sh_carries_only_unpinned_hint():
    text = INSTALL_SH.read_text(encoding="utf-8")
    assert "curl -LsSf https://astral.sh/uv/install.sh | sh" in text
    assert "install_uv.sh" not in text
    assert "UV_VERSION" not in text
    assert "astral.sh/uv/0." not in text
    assert "astral.sh/uv/$" not in text


def test_vendored_skill_has_frontmatter_and_intact_upstream_teaching():
    assert VENDORED_SKILL.is_file(), f"missing vendored skill {VENDORED_SKILL}"
    text = VENDORED_SKILL.read_text(encoding="utf-8")
    assert text.startswith("---\n"), text[:80]
    frontmatter = text.split("---\n", 2)[1]
    assert re.search(r"^name:\s*uv\s*$", frontmatter, re.MULTILINE), frontmatter
    assert re.search(r"^description:\s*\S", frontmatter, re.MULTILINE), frontmatter
    assert "Bootstrap (this fork)" in text
    assert UPSTREAM_URL in text
    assert UPSTREAM_SHA256 in text
    assert f"UV_VERSION=\"{EXPECTED_PIN}\"" in text
    assert "uv run script.py" in text
    assert "uv pip compile" in text
    assert "https://docs.astral.sh/uv/llms.txt" in text


def test_installer_helper_exists_executable_pinned_and_guarded():
    assert INSTALLER.is_file(), f"missing helper {INSTALLER}"
    assert os.stat(INSTALLER).st_mode & 0o111, "helper is not executable"
    src = INSTALLER.read_text(encoding="utf-8")
    assert "set -euo pipefail" in src
    assert f'UV_VERSION="{EXPECTED_PIN}"' in src
    assert f'"https://astral.sh/uv/${{UV_VERSION}}/install.sh"' in src
    assert "command -v uv" in src
    assert "uv --version" in src
    assert "UV_VERSION=" in src
    assert "latest" not in src.lower()
    assert "pipefail" in src


def _make_env(bin_dir):
    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}/usr/bin:/bin"
    env.pop("UV_VERSION", None)
    return env


def _write_fake_uv(bin_dir, output):
    uv = bin_dir / "uv"
    uv.write_text("#!/bin/sh\nprintf '%s\\n' " + shlex.quote(output) + "\n")
    uv.chmod(0o755)
    return uv


def _write_curl_stub(bin_dir, log, *, mode):
    if mode == "install":
        fake_uv = bin_dir / "uv"
        body = (
            "cat > " + shlex.quote(str(fake_uv)) + " <<'STUBEOF'\n"
            "#!/bin/sh\n"
            f'echo "uv {EXPECTED_PIN} (stub)"\n'
            "STUBEOF\n"
            "chmod +x " + shlex.quote(str(fake_uv)) + "\n"
            "exit 0\n"
        )
    else:
        body = 'echo "STUB_CURL_MUST_NOT_RUN" >&2\nexit 99\n'
    script = (
        "#!/bin/sh\n"
        f'printf "ARGS=%s\\n" "$*" >> "{log}"\n'
        f'printf "UV_VERSION=%s\\n" "${{UV_VERSION-<unset>}}" >> "{log}"\n'
        + body
    )
    curl = bin_dir / "curl"
    curl.write_text(script)
    curl.chmod(0o755)
    return curl


def _run_installer(env):
    return subprocess.run(
        ["bash", str(INSTALLER)],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_guard_is_genuine_noop_when_uv_present_at_other_version():
    with tempfile.TemporaryDirectory(prefix="task11-noop-") as raw:
        root = Path(raw)
        bin_dir = root / "bin"
        bin_dir.mkdir()
        log = root / "curl.log"
        uv = _write_fake_uv(bin_dir, "uv 0.0.1")
        _write_curl_stub(bin_dir, log, mode="fail")
        before = (uv.read_bytes(), uv.stat().st_mtime_ns)

        proc = _run_installer(_make_env(bin_dir))

        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        assert "already present" in proc.stdout.lower(), proc.stdout
        assert "no-op" in proc.stdout.lower(), proc.stdout
        assert not log.exists(), f"curl was called: {log.read_text()}"
        assert (uv.read_bytes(), uv.stat().st_mtime_ns) == before
        assert uv.read_text().strip() == "#!/bin/sh\nprintf '%s\\n' 'uv 0.0.1'"


def test_guard_noop_with_weird_or_empty_version_output():
    for output in ("", "totally-not-a-version", "uv 9999.99.99"):
        with tempfile.TemporaryDirectory(prefix="task11-malformed-") as raw:
            root = Path(raw)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            log = root / "curl.log"
            uv = _write_fake_uv(bin_dir, output)
            _write_curl_stub(bin_dir, log, mode="fail")
            before = (uv.read_bytes(), uv.stat().st_mtime_ns)

            proc = _run_installer(_make_env(bin_dir))

            assert proc.returncode == 0, (output, proc.stdout, proc.stderr)
            assert "no-op" in proc.stdout.lower(), (output, proc.stdout)
            assert not log.exists(), (output, log.read_text())
            assert (uv.read_bytes(), uv.stat().st_mtime_ns) == before


def test_absent_uv_installs_pinned_version_and_second_run_is_noop():
    with tempfile.TemporaryDirectory(prefix="task11-happy-") as raw:
        root = Path(raw)
        bin_dir = root / "bin"
        bin_dir.mkdir()
        log = root / "curl.log"
        _write_curl_stub(bin_dir, log, mode="install")
        env = _make_env(bin_dir)

        first = _run_installer(env)

        assert first.returncode == 0, (first.stdout, first.stderr)
        assert log.exists(), "stub curl was never called"
        logged = log.read_text(encoding="utf-8")
        assert f"UV_VERSION={EXPECTED_PIN}" in logged, logged
        assert f"https://astral.sh/uv/{EXPECTED_PIN}/install.sh" in logged, logged
        assert f"-LsSf https://astral.sh/uv/{EXPECTED_PIN}/install.sh" in logged, logged
        uv = bin_dir / "uv"
        assert uv.is_file() and os.access(uv, os.X_OK)
        installed = subprocess.run(
            [str(uv), "--version"], env=env, capture_output=True, text=True, timeout=10
        )
        assert EXPECTED_PIN in installed.stdout, installed.stdout

        state_before = (log.read_bytes(), uv.read_bytes(), uv.stat().st_mtime_ns)
        second = _run_installer(env)

        assert second.returncode == 0, (second.stdout, second.stderr)
        assert "already present" in second.stdout.lower(), second.stdout
        assert (log.read_bytes(), uv.read_bytes(), uv.stat().st_mtime_ns) == state_before
