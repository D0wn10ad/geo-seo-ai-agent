"""TDD for Todo 12: single idempotent checksum-keyed uv env/deps bootstrap.

Baseline characterization records state observed before this change and pins
behaviour that must survive it. The failing-first tests below assert observable
outcomes (artifacts, call logs, sentinel contents, exit codes) rather than
mock-call bookkeeping, and pass once the bootstrap and hint edits are in place.

Every PATH-sensitive probe uses an isolated scratch bin so the real uv at
~/.local/bin/uv cannot satisfy or defeat a guard.
"""

import hashlib
import os
import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "skills" / "geo" / "scripts" / "bootstrap_env.sh"
INSTALL_UV = ROOT / "skills" / "geo" / "scripts" / "install_uv.sh"
REQUIREMENTS = ROOT / "requirements.txt"
PDF_SKILL = ROOT / "skills" / "geo-report-pdf" / "SKILL.md"
PDF_SKILL_CN = ROOT / "skills" / "geo-report-pdf" / "references" / "cn.md"

PRE_BOOTSTRAP_OBSERVATION = {
    "skills/geo/scripts/bootstrap_env.sh exists": True,
    "geo-report-pdf/SKILL.md bare 'pip install reportlab' hints": 0,
    "geo-report-pdf/references/cn.md bare 'pip install reportlab[ttfont]' hints": 0,
}


def test_baseline_pre_bootstrap_observation_snapshot():
    assert PRE_BOOTSTRAP_OBSERVATION == {
        "skills/geo/scripts/bootstrap_env.sh exists": True,
        "geo-report-pdf/SKILL.md bare 'pip install reportlab' hints": 0,
        "geo-report-pdf/references/cn.md bare 'pip install reportlab[ttfont]' hints": 0,
    }


def test_baseline_requirements_file_is_stable_bootstrap_input():
    text = REQUIREMENTS.read_text(encoding="utf-8")
    assert "reportlab>=4.4.0,<5.0.0" in text
    assert "requests>=2.34.2,<3.0.0" in text
    assert "flask>=3.1.3,<4.0.0" in text


def test_baseline_install_uv_guard_survives():
    with _scratch("task12-survive-") as root:
        bin_dir = root / "bin"
        bin_dir.mkdir()
        (bin_dir / "uv").write_text("#!/bin/sh\nprintf 'uv 0.13.9\\n'\n")
        (bin_dir / "uv").chmod(0o755)
        curl_log = root / "curl.log"
        curl = bin_dir / "curl"
        curl.write_text(
            "#!/bin/sh\nprintf 'CURL_CALLED\\n' >> " + shlex.quote(str(curl_log)) + "\nexit 99\n"
        )
        curl.chmod(0o755)
        proc = subprocess.run(
            ["bash", str(INSTALL_UV)],
            env=_isolated_env(bin_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        assert "no-op" in proc.stdout.lower()
        assert not curl_log.exists()


class _scratch:
    def __init__(self, prefix):
        import tempfile

        self._tmp = tempfile.TemporaryDirectory(prefix=prefix)

    def __enter__(self):
        return Path(self._tmp.name)

    def __exit__(self, *_exc):
        self._tmp.cleanup()


def _isolated_env(bin_dir, **extra):
    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}/usr/bin:/bin"
    env["HOME"] = str(bin_dir.parent / "home")
    env.pop("GEO_CACHE_DIR", None)
    env.pop("XDG_CACHE_HOME", None)
    env.update(extra)
    return env


def _write_fake_uv(bin_dir, call_log, marker):
    uv = bin_dir / "uv"
    uv.write_text(
        "#!/bin/sh\n"
        f'printf "%s\\n" "$*" >> "{call_log}"\n'
        'case "$1" in\n'
        "  venv)\n"
        '    mkdir -p "$2/bin"\n'
        '    printf "#!/bin/sh\\nprintf \'stub venv python\\n\'\\n" > "$2/bin/python3"\n'
        '    chmod +x "$2/bin/python3"\n'
        "    ;;\n"
        "  pip)\n"
        f'    : > "{marker}"\n'
        "    ;;\n"
        "  *)\n"
        '    printf "unexpected uv args: %s\\n" "$*" >&2\n'
        "    exit 2\n"
        "    ;;\n"
        "esac\n"
        "exit 0\n"
    )
    uv.chmod(0o755)
    return uv


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _run_bootstrap(requirements, env):
    return subprocess.run(
        ["bash", str(BOOTSTRAP), str(requirements)] if BOOTSTRAP.exists() else ["bash", "-c", "exit 127"],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _assert_fresh_observables(root, requirements, proc):
    call_log = root / "uv-calls.log"
    marker = root / "install.marker"
    cache = root / "cache"
    venv_py = cache / "venv" / "bin" / "python3"
    sentinel = cache / ".env-bootstrap-sentinel"

    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert venv_py.is_file() and os.access(venv_py, os.X_OK), "venv interpreter missing"
    assert marker.exists(), "install marker missing"
    lines = call_log.read_text(encoding="utf-8").splitlines()
    assert sum(line.startswith("venv ") for line in lines) == 1, lines
    assert sum(line.startswith("pip install ") for line in lines) == 1, lines
    expected_sha = _sha(requirements)
    assert sentinel.read_text(encoding="utf-8").strip() == expected_sha
    assert f"{venv_py}" in proc.stdout, proc.stdout
    return lines, sentinel


def test_bootstrap_script_exists_executable_and_meets_spec():
    assert BOOTSTRAP.is_file(), f"missing {BOOTSTRAP}"
    assert os.stat(BOOTSTRAP).st_mode & 0o111, "bootstrap is not executable"
    src = BOOTSTRAP.read_text(encoding="utf-8")
    assert src.startswith("#!/usr/bin/env bash\n")
    assert "set -euo pipefail" in src
    assert "requirements.txt" in src
    assert "sha256sum" in src and "shasum" in src
    assert "XDG_CACHE_HOME" in src and "GEO_CACHE_DIR" in src
    assert "SENTINEL" in src and "VENV_DIR" in src
    assert "no-op" in src
    assert "uv venv" in src and "uv pip install" in src and "--python" in src
    assert "install_uv.sh" in src
    bare_pip = [ln for ln in src.splitlines() if "pip install" in ln and not ln.lstrip().startswith("uv ")]
    assert bare_pip == [], bare_pip


def test_report_pdf_hints_are_venv_targeted():
    text = PDF_SKILL.read_text(encoding="utf-8")
    assert "pip install reportlab" not in text
    assert "bootstrap_env.sh" in text
    assert "uv pip install --python" in text
    assert "reportlab" in text


def test_report_pdf_cn_hint_is_venv_targeted():
    text = PDF_SKILL_CN.read_text(encoding="utf-8")
    assert "pip install reportlab[ttfont]" not in text
    assert "uv pip install --python" in text
    assert "reportlab[ttfont]" in text


def test_bootstrap_is_idempotent_and_checksum_keyed():
    with _scratch("task12-happy-") as root:
        bin_dir = root / "bin"
        bin_dir.mkdir()
        requirements = root / "requirements.txt"
        requirements.write_text("rich>=13.0.0,<14.0.0\n", encoding="utf-8")
        call_log = root / "uv-calls.log"
        marker = root / "install.marker"
        _write_fake_uv(bin_dir, call_log, marker)
        cache = root / "cache"
        env = _isolated_env(bin_dir, GEO_CACHE_DIR=str(cache))

        first = _run_bootstrap(requirements, env)
        lines, sentinel = _assert_fresh_observables(root, requirements, first)

        second = _run_bootstrap(requirements, env)
        assert second.returncode == 0, (second.stdout, second.stderr)
        assert call_log.read_text(encoding="utf-8").splitlines() == lines
        assert "no-op" in second.stdout.lower(), second.stdout
        assert sentinel.read_text(encoding="utf-8").strip() == _sha(requirements)

        requirements.write_text(
            "rich>=13.0.0,<14.0.0\n# checksum changed\n", encoding="utf-8"
        )
        third = _run_bootstrap(requirements, env)
        assert third.returncode == 0, (third.stdout, third.stderr)
        grown = call_log.read_text(encoding="utf-8").splitlines()
        assert len(grown) == len(lines) + 2, grown
        assert sum(line.startswith("pip install ") for line in grown) == 2, grown
        assert sentinel.read_text(encoding="utf-8").strip() == _sha(requirements)


def test_stale_venv_python_triggers_rerun():
    with _scratch("task12-stale-") as root:
        bin_dir = root / "bin"
        bin_dir.mkdir()
        requirements = root / "requirements.txt"
        requirements.write_text("rich>=13.0.0,<14.0.0\n", encoding="utf-8")
        call_log = root / "uv-calls.log"
        marker = root / "install.marker"
        _write_fake_uv(bin_dir, call_log, marker)
        cache = root / "cache"
        env = _isolated_env(bin_dir, GEO_CACHE_DIR=str(cache))

        first = _run_bootstrap(requirements, env)
        lines, _sentinel = _assert_fresh_observables(root, requirements, first)

        (cache / "venv" / "bin" / "python3").unlink()
        second = _run_bootstrap(requirements, env)
        assert second.returncode == 0, (second.stdout, second.stderr)
        grown = call_log.read_text(encoding="utf-8").splitlines()
        assert len(grown) == len(lines) + 2, grown
        assert (cache / "venv" / "bin" / "python3").is_file()


def test_missing_requirements_errors_without_sentinel():
    with _scratch("task12-missing-") as root:
        bin_dir = root / "bin"
        bin_dir.mkdir()
        _write_fake_uv(bin_dir, root / "uv-calls.log", root / "install.marker")
        cache = root / "cache"
        env = _isolated_env(bin_dir, GEO_CACHE_DIR=str(cache))
        missing = root / "does-not-exist.txt"

        proc = _run_bootstrap(missing, env)

        assert proc.returncode != 0
        assert "requirements" in (proc.stdout + proc.stderr).lower()
        assert not (cache / ".env-bootstrap-sentinel").exists()
        assert not (root / "uv-calls.log").exists()


def test_absent_uv_errors_with_installer_hint():
    with _scratch("task12-nouv-") as root:
        bin_dir = root / "bin"
        bin_dir.mkdir()
        requirements = root / "requirements.txt"
        requirements.write_text("rich>=13.0.0,<14.0.0\n", encoding="utf-8")
        cache = root / "cache"
        env = _isolated_env(bin_dir, GEO_CACHE_DIR=str(cache))

        proc = _run_bootstrap(requirements, env)

        assert proc.returncode != 0
        assert "install_uv.sh" in (proc.stdout + proc.stderr)
        assert not (cache / ".env-bootstrap-sentinel").exists()


def test_bootstrap_no_arg_resolves_requirements_sibling_of_script():
    """No-arg bootstrap must default to a requirements.txt beside the script.

    Self-contained: copies bootstrap_env.sh into a fresh temp tree, places a
    valid requirements.txt as its SIBLING, stubs uv via a fake bin on PATH, and
    points XDG_CACHE_HOME at a temp cache. It deliberately does NOT reference
    the module-level REQUIREMENTS constant (owned by a separate change).
    """
    with _scratch("task2-noarg-") as root:
        bin_dir = root / "bin"
        bin_dir.mkdir()

        # Nest the script two levels deep so the OLD default (../..) resolves
        # to <root>/requirements.txt, which we intentionally do NOT create.
        script_dir = root / "nested" / "scripts"
        script_dir.mkdir(parents=True)
        copied_bootstrap = script_dir / "bootstrap_env.sh"
        copied_bootstrap.write_text(
            BOOTSTRAP.read_text(encoding="utf-8"), encoding="utf-8"
        )

        requirements = script_dir / "requirements.txt"
        requirements.write_text("rich>=13.0.0,<14.0.0\n", encoding="utf-8")

        call_log = root / "uv-calls.log"
        marker = root / "install.marker"
        _write_fake_uv(bin_dir, call_log, marker)
        cache = root / "cache"
        env = _isolated_env(bin_dir, XDG_CACHE_HOME=str(cache))

        proc = subprocess.run(
            ["bash", str(copied_bootstrap)],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        lines = call_log.read_text(encoding="utf-8").splitlines()
        assert any(
            line.startswith("pip install ") and str(requirements) in line
            for line in lines
        ), lines
        assert marker.exists(), "pip install was not invoked"
        sentinel = cache / "geo-seo-ai-agent" / ".env-bootstrap-sentinel"
        assert sentinel.read_text(encoding="utf-8").strip() == _sha(requirements)
