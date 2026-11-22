from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_DIRS = {".git", ".omo", ".venv", "tests", "agents", "__pycache__"}
EXCLUDED_FILES = {ROOT / "skills" / "geo-update" / "SKILL.md"}
SCANNED_SUFFIXES = {".md", ".sh", ".py"}


def source_files():
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in SCANNED_SUFFIXES:
            continue
        if EXCLUDED_DIRS.intersection(path.relative_to(ROOT).parts):
            continue
        if path in EXCLUDED_FILES:
            continue
        files.append(path)
    return files


def test_fetch_page_relocated():
    assert (ROOT / "skills" / "geo" / "scripts" / "fetch_page.py").is_file()


def test_root_scripts_dir_removed():
    assert not (ROOT / "scripts").exists()


def test_webapp_relocated():
    assert (ROOT / "skills" / "geo" / "scripts" / "webapp" / "app.py").is_file()


def test_no_hardcoded_python3_scripts_invocations():
    stale = [str(p.relative_to(ROOT)) for p in source_files() if "python3 scripts/" in p.read_text(encoding="utf-8", errors="replace")]
    assert stale == []
