"""Literal content-preservation check for the 5 audit agents -> skills fold.

Marker set (Todo 4 method): the H1 line, `## Region Awareness`,
`## Execution Steps`, `## Output Format`, and every `### Step ...` line from a
source agent must be literal-present in the target SKILL.md. A missing target,
missing source, missing marker, or malformed mapping row is a hard failure.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Mapping, Sequence, TypedDict

REPO_ROOT: Path = Path(__file__).resolve().parents[1]

AGENTS: tuple[str, ...] = (
    "geo-ai-visibility",
    "geo-content",
    "geo-platform-analysis",
    "geo-schema",
    "geo-technical",
)

FIXED_MARKERS: tuple[str, ...] = (
    "## Region Awareness",
    "## Execution Steps",
    "## Output Format",
)

CANONICAL_TARGETS: Mapping[str, str] = {
    name: f"skills/{name}/SKILL.md" for name in AGENTS
}


class CheckRow(TypedDict):
    agent: str
    source: str
    target: str
    total: int
    missing: list[str]
    absent: bool
    error: str | None
    ok: bool


def extract_markers(agent_text: str) -> list[str]:
    """Return the ordered distinct markers from an agent instruction body."""
    markers: list[str] = []
    for line in agent_text.splitlines():
        if line.startswith("# ") or line.startswith("### Step"):
            markers.append(line)
        elif line in FIXED_MARKERS:
            markers.append(line)
    return markers


def canonical_mapping() -> dict[str, tuple[str, str]]:
    return {
        name: (f"agents/{name}.md", CANONICAL_TARGETS[name]) for name in AGENTS
    }


def load_mapping(path: Path) -> dict[str, tuple[str, str]]:
    """Load a 3-column TSV: agent-name<TAB>source-agent<TAB>target-SKILL.md."""
    mapping: dict[str, tuple[str, str]] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        fields = raw.split("\t")
        if len(fields) != 3 or not all(field.strip() for field in fields):
            raise ValueError(
                f"malformed mapping row {number}: expected 3 tab-separated fields"
            )
        agent, source, target = fields
        mapping[agent.strip()] = (source.strip(), target.strip())
    if not mapping:
        raise ValueError("malformed mapping: no rows")
    return mapping


def resolve(path_text: str, root: Path) -> Path:
    candidate = Path(path_text)
    return candidate if candidate.is_absolute() else root / candidate


def check_mapping(
    mapping: Mapping[str, tuple[str, str]], root: Path = REPO_ROOT
) -> list[CheckRow]:
    """Check every mapping row; return one result dict per agent."""
    rows: list[CheckRow] = []
    for name in AGENTS:
        if name not in mapping:
            rows.append(
                {
                    "agent": name,
                    "source": "<unmapped>",
                    "target": "<unmapped>",
                    "total": 0,
                    "missing": [],
                    "absent": True,
                    "error": "agent ABSENT from mapping",
                    "ok": False,
                }
            )
            continue

        source_text, target_text = mapping[name]
        source_path = resolve(source_text, root)
        target_path = resolve(target_text, root)
        source_absent = not source_path.is_file()
        target_absent = not target_path.is_file()

        markers: list[str] = []
        if not source_absent:
            markers = extract_markers(source_path.read_text(encoding="utf-8"))
        target_body = (
            target_path.read_text(encoding="utf-8") if not target_absent else ""
        )
        missing = [marker for marker in markers if marker not in target_body]

        error: str | None = None
        if source_absent:
            error = f"source ABSENT: {source_path}"
        elif target_absent:
            error = f"target ABSENT: {target_path}"
        elif not markers:
            error = f"no markers extracted from {source_path}"

        rows.append(
            {
                "agent": name,
                "source": source_text,
                "target": target_text,
                "total": len(markers),
                "missing": missing,
                "absent": source_absent or target_absent,
                "error": error,
                "ok": error is None and not missing,
            }
        )
    return rows


def all_preserved(rows: Sequence[CheckRow]) -> bool:
    return bool(rows) and all(bool(row["ok"]) for row in rows)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", dest="map_path", help="3-column TSV mapping file")
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="base directory for relative paths (default: repo root)",
    )
    args = parser.parse_args(argv)

    try:
        mapping = (
            load_mapping(Path(args.map_path)) if args.map_path else canonical_mapping()
        )
    except (OSError, ValueError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    rows = check_mapping(mapping, args.root)
    for row in rows:
        if row["ok"]:
            print(
                f"{row['agent']} | PASS | markers {row['total']}/{row['total']} | "
                f"{row['source']} -> {row['target']}"
            )
        else:
            detail = row["error"] or (
                f"missing {len(row['missing'])} marker(s): "
                + "; ".join(str(item) for item in row["missing"])
            )
            print(f"{row['agent']} | FAIL | {detail}")

    passed = all_preserved(rows)
    print(f"OVERALL: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
