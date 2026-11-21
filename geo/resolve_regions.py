"""Print the first existing geo regions root for a SKILL.md directory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MARKER_PROFILE: str = "profiles.yaml"

CANDIDATE_SUFFIXES: tuple[str, ...] = (
    "regions",
    "../geo/regions",
    "../../regions",
    "../../../.claude/skills/geo/regions",
)


def resolve_regions_root(skill_dir: Path, marker: str = MARKER_PROFILE) -> Path | None:
    """Return the first candidate root containing *marker*, or None."""
    for suffix in CANDIDATE_SUFFIXES:
        candidate = (skill_dir / suffix).resolve()
        if (candidate / marker).is_file():
            return candidate
    return None


def main() -> int:
    """Resolve and print the regions root; fail closed when no candidate exists."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path, help="directory containing the SKILL.md")
    args = parser.parse_args()

    anchor = args.skill_dir.resolve()
    root = resolve_regions_root(anchor)
    if root is None:
        print(
            f"GEO regions root not found below {anchor}; probed: "
            + ", ".join(CANDIDATE_SUFFIXES),
            file=sys.stderr,
        )
        return 1
    print(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
