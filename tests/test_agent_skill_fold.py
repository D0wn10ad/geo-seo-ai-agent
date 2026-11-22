"""TDD seam for folding the 5 parallel audit agents into SKILL.md-bearing skills.

`baseline_*` tests pin the pre-fold observable contract and stay green after the
fold. `newflow_*` tests are the failing-first assertions for this change.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import agent_skill_preservation as preservation  # noqa: E402

EXPECTED_STEPS: dict[str, int] = {
    "geo-ai-visibility": 7,
    "geo-content": 10,
    "geo-platform-analysis": 7,
    "geo-schema": 8,
    "geo-technical": 11,
}
EXPECTED_H1: dict[str, str] = {
    "geo-ai-visibility": "# GEO AI Visibility Agent",
    "geo-content": "# GEO Content Quality Agent",
    "geo-platform-analysis": "# GEO Platform Analysis Agent",
    "geo-schema": "# GEO Schema & Structured Data Agent",
    "geo-technical": "# GEO Technical SEO Agent",
}
NO_COUNTERPART: frozenset[str] = frozenset(
    {"geo-ai-visibility", "geo-platform-analysis"}
)
HELPER: Path = REPO_ROOT / "tests" / "agent_skill_preservation.py"


def _legacy_fixture(tmp_path: Path) -> tuple[dict[str, tuple[str, str]], Path]:
    """Reproduce the pre-fold naive 1:1 shape: 3 marker-less targets, 2 absent."""
    legacy = tmp_path / "legacy"
    mapping: dict[str, tuple[str, str]] = {}
    for name in preservation.AGENTS:
        target = legacy / "skills" / name / "SKILL.md"
        if name not in NO_COUNTERPART:
            target.parent.mkdir(parents=True)
            target.write_text(
                f"---\nname: {name}\n---\n\n# Legacy {name}\n\n"
                "## Purpose\n\nMethodology rubric only; no agent execution contract.\n",
                encoding="utf-8",
            )
        mapping[name] = (
            str(REPO_ROOT / "agents" / f"{name}.md"),
            str(target),
        )
    return mapping, legacy


def test_newflow_legacy_agent_files_absent() -> None:
    for name in preservation.AGENTS:
        source = REPO_ROOT / "agents" / f"{name}.md"
        assert not source.exists(), f"legacy agent file still present: {source}"
    assert not (REPO_ROOT / "agents").exists(), "legacy agents/ directory still present"


def test_newflow_canonical_skill_markers_present() -> None:
    for name in preservation.AGENTS:
        target = REPO_ROOT / "skills" / name / "SKILL.md"
        assert target.is_file(), f"missing canonical skill: {target}"
        markers = preservation.extract_markers(target.read_text(encoding="utf-8"))
        assert EXPECTED_H1[name] in markers, f"{name} missing agent H1 {EXPECTED_H1[name]}"
        agent_start = markers.index(EXPECTED_H1[name])
        agent_markers = markers[agent_start:]
        for fixed in preservation.FIXED_MARKERS:
            assert fixed in agent_markers, f"{name} missing {fixed}"
        steps = [m for m in agent_markers if m.startswith("### Step")]
        assert len(steps) == EXPECTED_STEPS[name]
        assert steps[0].startswith("### Step 1:")
        assert steps[-1].startswith(f"### Step {EXPECTED_STEPS[name]}:")
        assert len(agent_markers) == 4 + EXPECTED_STEPS[name]


def test_newflow_five_target_skill_dirs_exist() -> None:
    for name in preservation.AGENTS:
        target = REPO_ROOT / "skills" / name / "SKILL.md"
        assert target.is_file(), f"missing npx-discoverable skill: {target}"
        assert target.parent.name == name
        assert target.name == "SKILL.md"


def test_newflow_all_unique_markers_preserved() -> None:
    rows = preservation.check_mapping(preservation.canonical_mapping(), REPO_ROOT)
    for row in rows:
        assert row["ok"], f"{row['agent']} lost sections: {row['missing']}"
        assert row["missing"] == []
        assert row["total"] >= 4 + EXPECTED_STEPS[row["agent"]]


def test_newflow_no_counterpart_agents_now_discoverable() -> None:
    assert NO_COUNTERPART == {"geo-ai-visibility", "geo-platform-analysis"}
    for name in sorted(NO_COUNTERPART):
        target = REPO_ROOT / "skills" / name / "SKILL.md"
        body = target.read_text(encoding="utf-8")
        assert "## Execution Steps" in body
        assert "## Region Awareness" in body
        assert "## Output Format" in body


def test_newflow_phase2_dispatch_uses_skills_in_parallel() -> None:
    orchestrator = (REPO_ROOT / "skills" / "geo" / "SKILL.md").read_text(encoding="utf-8")
    start = orchestrator.index("**Phase 2:")
    end = orchestrator.index("**Phase 3:")
    phase2 = orchestrator[start:end]
    assert "agents/geo-" not in phase2
    assert "parallel" in phase2.lower()
    assert "task/subagent" in phase2.lower()
    for name in preservation.AGENTS:
        assert f"skills/{name}/SKILL.md" in phase2

    subagent_start = orchestrator.index("## Subagents (")
    subagent_block = orchestrator[subagent_start:].split("\n---\n", 1)[0]
    assert "agents/geo-" not in subagent_block
    assert "parallel" in subagent_block.lower()


def _run_helper(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HELPER), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _write_tsv(path: Path, mapping: dict[str, tuple[str, str]]) -> None:
    path.write_text(
        "".join(f"{name}\t{source}\t{target}\n" for name, (source, target) in mapping.items()),
        encoding="utf-8",
    )


def test_newflow_preservation_cli_exit_codes(tmp_path: Path) -> None:
    good = _run_helper()
    assert good.returncode == 0, good.stdout + good.stderr
    assert "OVERALL: PASS" in good.stdout
    assert good.stdout.count("| PASS |") == 5

    mapping, _ = _legacy_fixture(tmp_path)
    naive_tsv = tmp_path / "naive-map.tsv"
    _write_tsv(naive_tsv, mapping)
    bad = _run_helper("--map", str(naive_tsv))
    assert bad.returncode == 1
    assert "OVERALL: FAIL" in bad.stdout
    assert bad.stdout.count("| FAIL |") == 5

    malformed = tmp_path / "malformed-map.tsv"
    malformed.write_text("geo-content\tonly-two-fields\n", encoding="utf-8")
    broken = _run_helper("--map", str(malformed))
    assert broken.returncode == 1
    assert "malformed mapping row" in broken.stderr
