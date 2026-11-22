"""CN region-preservation contract: current behavior + npx-installed layout."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RESOLVER_PATH = ROOT / "skills" / "geo" / "scripts" / "region_resolver.py"
MANIFEST_PATH = ROOT / "skills" / "geo" / "references" / "regions" / "cn-variants.json"
MARKER = "<!-- GEO-CN-VARIANT:v1 -->"

VARIANT_SKILLS = (
    "geo-audit",
    "geo-brand-mentions",
    "geo-citability",
    "geo-citation-pipeline",
    "geo-compare",
    "geo-competitor-citation",
    "geo-content",
    "geo-crawlers",
    "geo-distribution-plan",
    "geo-intent-matrix",
    "geo-platform-optimizer",
    "geo-proposal",
    "geo-prospect",
    "geo-report-pdf",
    "geo-report",
    "geo-schema",
    "geo-technical",
)

CN_KNOWLEDGE = (
    "README.md",
    "ai-engines.md",
    "compliance-anti-abuse.md",
    "cross-validation.md",
    "engineering-playbooks.md",
    "kpi-and-method.md",
    "platform-behavior.md",
    "platforms.md",
    "provenance.md",
    "schema.md",
    "source-tiering.md",
)


def load_resolver(path: Path = RESOLVER_PATH):
    spec = importlib.util.spec_from_file_location("cn_region_resolver_under_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_detect_cn_tld():
    assert load_resolver().detect("https://example.cn") == "cn"


def test_detect_global_tld():
    assert load_resolver().detect("https://example.com") == "global"


def test_load_cn_profile():
    profile = load_resolver().load_profile("cn")
    assert profile is not None
    assert profile["code"] == "cn"
    assert "BaiduSpider" in profile["crawlers"]


def test_all_17_cn_variants_exist_with_content():
    for skill in VARIANT_SKILLS:
        path = ROOT / "skills" / skill / "references" / "cn.md"
        assert path.is_file(), f"missing CN variant: {path}"
        assert len(path.read_text(encoding="utf-8").strip()) > 100, f"empty CN variant: {path}"


def test_cn_knowledge_single_source_under_geo_skill():
    canonical = ROOT / "skills" / "geo" / "references" / "regions"
    legacy = ROOT / "geo" / "regions"
    assert canonical.is_dir(), f"missing canonical region dir: {canonical}"
    assert not legacy.exists(), f"legacy region mirror still present: {legacy}"
    for rel in ("profiles.yaml", "README.md"):
        assert (canonical / rel).is_file(), f"missing canonical region file: {rel}"
    for name in CN_KNOWLEDGE:
        assert (canonical / "cn" / name).is_file(), f"missing canonical CN KB file: cn/{name}"


def test_manifest_enumerates_all_17_variants_and_knowledge():
    assert MANIFEST_PATH.is_file(), f"missing manifest: {MANIFEST_PATH}"
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert data["region"] == "cn"
    assert len(data["variants"]) == 17
    assert set(data["variants"]) == set(VARIANT_SKILLS)
    assert data["variant_file"] == "references/cn.md"
    knowledge = set(data["knowledge_base"])
    assert "references/regions/profiles.yaml" in knowledge
    assert "references/regions/cn/ai-engines.md" in knowledge
    assert "references/regions/cn/platforms.md" in knowledge
    assert "references/regions/cn/schema.md" in knowledge
    assert len([k for k in knowledge if k.startswith("references/regions/cn/")]) == len(CN_KNOWLEDGE)


def test_primary_skills_declare_conditional_cn_loading():
    for skill in VARIANT_SKILLS:
        text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        assert MARKER in text, f"{skill}/SKILL.md missing {MARKER}"
        assert "references/cn.md" in text, f"{skill}/SKILL.md missing variant pointer"
        assert "REGION" in text, f"{skill}/SKILL.md missing REGION gate"


def test_orchestrator_documents_cn_manifest_and_conditional_gate():
    text = (ROOT / "skills" / "geo" / "SKILL.md").read_text(encoding="utf-8")
    assert MARKER in text
    assert "cn-variants.json" in text
    assert "references/cn.md" in text
    assert "references/regions/cn/" in text


@pytest.fixture
def installed_tree(tmp_path: Path) -> Path:
    """Simulate an npx install: only SKILL.md-bearing skill trees are copied."""
    skills = tmp_path / ".agents" / "skills"
    shutil.copytree(
        ROOT / "skills" / "geo",
        skills / "geo",
        ignore=shutil.ignore_patterns("__pycache__", ".venv"),
    )
    for skill in VARIANT_SKILLS:
        destination = skills / skill
        (destination / "references").mkdir(parents=True)
        shutil.copy2(ROOT / "skills" / skill / "SKILL.md", destination / "SKILL.md")
        shutil.copy2(ROOT / "skills" / skill / "references" / "cn.md", destination / "references" / "cn.md")
    return skills


def run_installed(skills: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(skills / "geo" / "scripts" / "region_resolver.py"), *args],
        capture_output=True,
        text=True,
        cwd=skills.parent.parent,
        check=False,
    )


def test_installed_resolver_loads_cn_profile(installed_tree: Path):
    result = run_installed(installed_tree, "profile", "cn")
    assert result.returncode == 0, result.stderr
    assert "BaiduSpider" in result.stdout or "baidu_baike" in result.stdout


def test_installed_resolver_detect_is_correct(installed_tree: Path):
    assert run_installed(installed_tree, "detect", "https://example.cn").stdout.strip() == "cn"
    assert run_installed(installed_tree, "detect", "https://example.com").stdout.strip() == "global"


def test_installed_guidance_is_conditional(installed_tree: Path):
    cn = run_installed(installed_tree, "guidance", "cn")
    assert cn.returncode == 0, cn.stderr
    assert "geo-audit/references/cn.md" in cn.stdout
    assert "references/regions/cn/ai-engines.md" in cn.stdout
    assert cn.stdout.count("references/cn.md") == 17

    global_run = run_installed(installed_tree, "guidance", "global")
    assert global_run.returncode == 0, global_run.stderr
    assert "references/cn.md" not in global_run.stdout
    assert "references/regions/cn/" not in global_run.stdout


def test_installed_manifest_and_knowledge_present(installed_tree: Path):
    manifest = json.loads((installed_tree / "geo" / "references" / "regions" / "cn-variants.json").read_text(encoding="utf-8"))
    assert set(manifest["variants"]) == set(VARIANT_SKILLS)
    for rel in ("profiles.yaml", "README.md"):
        assert (installed_tree / "geo" / "references" / "regions" / rel).is_file()
    for name in CN_KNOWLEDGE:
        assert (installed_tree / "geo" / "references" / "regions" / "cn" / name).is_file()
