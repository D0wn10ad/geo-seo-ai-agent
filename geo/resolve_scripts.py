"""Print the first existing GEO helper-scripts root for a SKILL.md directory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MARKER_SCRIPT: str = "fetch_page.py"

CANDIDATE_SUFFIXES: tuple[str, ...] = (
    "scripts",
    "../geo/scripts",
    "../../geo/scripts",
    "../../../.claude/skills/geo/scripts",
)


def resolve_scripts_root(skill_dir: Path, marker: str = MARKER_SCRIPT) -> Path | None:
    """Return the first candidate root containing *marker*, or None."""
    for suffix in CANDIDATE_SUFFIXES:
        candidate = (skill_dir / suffix).resolve()
        if (candidate / marker).is_file():
            return candidate
    return None


def main() -> int:
    """Resolve and print the scripts root; fail closed when no candidate exists."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path, help="directory containing the SKILL.md")
    args = parser.parse_args()

    anchor = args.skill_dir.resolve()
    root = resolve_scripts_root(anchor)
    if root is None:
        print(
            f"GEO scripts root not found below {anchor}; probed: "
            + ", ".join(CANDIDATE_SUFFIXES),
            file=sys.stderr,
        )
        return 1
    print(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
