"""GEO-SEO AI Agent Toolkit — cross-platform installer/updater.

Installs or updates the geo-seo-ai-agent skill bundle for both
Claude Code and OpenCode platforms. Auto-detects which platform(s)
are present on the system and installs accordingly.

Usage:
    python3 scripts/update_toolkit.py                    # detect & install
    python3 scripts/update_toolkit.py --upstream <url>   # custom source
    python3 scripts/update_toolkit.py --target <dir>     # custom install dir
    python3 scripts/update_toolkit.py --all-platforms    # install for both
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_URL = "https://github.com/zubair-trabzada/geo-seo-claude"
SKILLS_DIR = "geo"
SCRIPTS_DIR = "scripts"
DOCS_DIR = "docs"
AGENTS_DIR = "agents"
OPENCODE_DIR = ".opencode"

HOME = Path.home()
XDG_CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
CLAUDE_SKILLS = HOME / ".claude" / "skills"
CLAUDE_AGENTS = HOME / ".claude" / "agents"
OPENCODE_AGENTS = XDG_CONFIG / "opencode" / "agents"
OPENCODE_COMMANDS = XDG_CONFIG / "opencode" / "commands"


def platform_info():
    """Return a dict describing the current platform."""
    return {
        "system": platform.system(),
        "is_claude_code": (HOME / ".claude").is_dir(),
        "is_opencode": (XDG_CONFIG / "opencode" / "opencode.json").is_file(),
        "python": sys.executable,
    }


def detect_platforms():
    """Detect which AI agent platforms are installed."""
    platforms = []
    if platform_info()["is_claude_code"]:
        platforms.append("claude-code")
    if platform_info()["is_opencode"]:
        platforms.append("opencode")
    return platforms


def clone_or_pull_repo(upstream_url, target_dir):
    """Clone or pull the upstream repository into target_dir."""
    if target_dir.exists():
        print(f"Updating existing repo at {target_dir}...")
        subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=target_dir,
            check=False,
        )
    else:
        print(f"Cloning {upstream_url} into {target_dir}...")
        subprocess.run(
            ["git", "clone", upstream_url, str(target_dir)],
            check=True,
        )
    return target_dir


def copy_tree(src, dst, desc=""):
    """Copy src directory tree to dst, creating parents if needed."""
    if not src.exists():
        print(f"  SKIP: {desc} source not found at {src}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"  OK: {desc} -> {dst}")


def copy_files(src_dir, dst_dir, pattern, desc=""):
    """Copy files matching pattern from src_dir to dst_dir."""
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    if not src_dir.exists():
        print(f"  SKIP: {desc} source not found at {src_dir}")
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in src_dir.glob(pattern):
        shutil.copy2(f, dst_dir / f.name)
        count += 1
    print(f"  OK: {desc} -> {dst_dir} ({count} files)")


def install_for_platform(repo_dir, platform_name):
    """Install skills and agents for the given platform."""
    repo = Path(repo_dir)

    if platform_name == "claude-code":
        skills_dst = CLAUDE_SKILLS
        agents_src = repo / AGENTS_DIR
        agents_dst = CLAUDE_AGENTS
    elif platform_name == "opencode":
        skills_dst = CLAUDE_SKILLS  # shared skill path
        agents_src = repo / OPENCODE_DIR / AGENTS_DIR
        agents_dst = OPENCODE_AGENTS
    else:
        print(f"  Unknown platform: {platform_name}")
        return

    skills_dst.mkdir(parents=True, exist_ok=True)

    copy_tree(repo / SKILLS_DIR, skills_dst / SKILLS_DIR, "Skill orchestrator")
    copy_tree(repo / "skills", skills_dst / "skills", "Skill sub-commands")
    copy_tree(repo / "platform", skills_dst / "platform", "Platform adapter")
    copy_tree(repo / SCRIPTS_DIR, skills_dst / SCRIPTS_DIR, "Scripts")
    copy_tree(repo / DOCS_DIR, skills_dst / DOCS_DIR, "Documentation")
    copy_files(agents_src, agents_dst, "*.md", f"Agents ({platform_name})")

    if platform_name == "opencode":
        commands_src = repo / OPENCODE_DIR / "commands"
        commands_dst = OPENCODE_COMMANDS
        copy_files(commands_src, commands_dst, "*.md", "Commands (OpenCode)")

    print(f"  Done: {platform_name}")


def install_all_platforms(repo_dir, platforms):
    """Install for all detected platforms."""
    for p in platforms:
        install_for_platform(repo_dir, p)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Install/update the GEO-SEO AI Agent toolkit"
    )
    parser.add_argument(
        "--upstream",
        default=REPO_URL,
        help="Upstream repository URL (default: %(default)s)",
    )
    parser.add_argument(
        "--target",
        default=None,
        help="Target clone directory (default: temp directory)",
    )
    parser.add_argument(
        "--all-platforms",
        action="store_true",
        help="Install for both Claude Code and OpenCode regardless of detection",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    platforms = detect_platforms()
    if args.all_platforms:
        platforms = ["claude-code", "opencode"]

    if not platforms:
        print("No supported AI agent platforms detected.")
        print("Install Claude Code or OpenCode first, then re-run this script.")
        print("Alternatively, use --all-platforms to install for both anyway.")
        sys.exit(1)

    print(f"Detected platforms: {', '.join(platforms)}")
    print(f"Upstream: {args.upstream}")

    if args.target:
        repo_dir = Path(args.target)
        clone_or_pull_repo(args.upstream, repo_dir)
    else:
        with tempfile.TemporaryDirectory(prefix="geo-seo-") as tmp:
            repo_dir = Path(tmp) / "geo-seo"
            clone_or_pull_repo(args.upstream, repo_dir)
            install_all_platforms(repo_dir, platforms)
            print("\nInstallation complete.")
            return

    install_all_platforms(repo_dir, platforms)
    print("\nInstallation complete.")


if __name__ == "__main__":
    main()
