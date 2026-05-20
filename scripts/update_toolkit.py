"""GEO-SEO AI Agent Toolkit — cross-platform installer/updater.

Installs or updates the geo-seo-ai-agent skill bundle for both
Claude Code and OpenCode platforms. Auto-detects which platform(s)
are present on the system and installs accordingly.

Usage:
    python3 scripts/update_toolkit.py                          # detect & install
    python3 scripts/update_toolkit.py --upstream <url>         # custom source
    python3 scripts/update_toolkit.py --target <dir>           # custom install dir
    python3 scripts/update_toolkit.py --all-platforms          # install for both
    python3 scripts/update_toolkit.py --branch <branch>        # specific git branch
"""

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_URL = "https://github.com/D0wn10ad/geo-seo-ai-agent"
SKILLS_DIR = "geo"
SCRIPTS_DIR = "scripts"
DOCS_DIR = "docs"
AGENTS_DIR = "agents"
REGIONS_DIR = "regions"
OPENCODE_DIR = ".opencode"

HOME = Path.home()
XDG_CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
CLAUDE_SKILLS = HOME / ".claude" / "skills"
CLAUDE_AGENTS = HOME / ".claude" / "agents"
OPENCODE_AGENTS = XDG_CONFIG / "opencode" / "agents"
OPENCODE_COMMANDS = XDG_CONFIG / "opencode" / "commands"

# OpenCode frontmatter descriptions for agents generated from agents/*.md
_OC_AGENT_DESCRIPTIONS: dict[str, str] = {
    "geo-ai-visibility": "GEO geo-ai-visibility specialist. Subagent for parallel GEO audit execution.",
    "geo-content": "GEO geo-content specialist. Subagent for parallel GEO audit execution.",
    "geo-platform-analysis": "GEO geo-platform-analysis specialist. Subagent for parallel GEO audit execution.",
    "geo-schema": "GEO geo-schema specialist. Subagent for parallel GEO audit execution.",
    "geo-technical": "GEO geo-technical specialist. Subagent for parallel GEO audit execution.",
}

# ── Command definitions ──────────────────────────────────────
# {name: (description, body)}
# `name` maps to geo-{name}.md. `$1` / `$ARGUMENTS` are positional.
_GEO_COMMANDS: dict[str, tuple[str, str]] = {
    "audit": (
        "Run a full GEO+SEO audit with parallel subagents on a target URL",
        "Load the `geo` skill and execute the full GEO+SEO audit workflow on `$1`. "
        "Run all 3 phases: discovery (fetch homepage, detect business type, extract key pages), "
        "parallel analysis (delegate to all 5 subagents), and synthesis "
        "(calculate composite GEO score, generate action plan).",
    ),
    "brands": (
        "Scan brand mentions across AI-cited platforms for a target URL",
        "Load the `geo` skill and execute the brand mention scanning workflow on `$1`. "
        "Search for brand presence across Wikipedia, Reddit, YouTube, LinkedIn, "
        "and industry sources. Calculate brand authority score.",
    ),
    "citability": (
        "Score content for AI citation readiness on a target URL",
        "Load the `geo` skill and execute the citability scoring workflow on `$1`. "
        "Evaluate each content block on answer block quality, self-containment, "
        "structural readability, statistical density, and uniqueness. "
        "Produce the page citability score and identify citation-ready passages.",
    ),
    "compare": (
        "Monthly delta report showing score improvements for a domain",
        "Load the `geo` skill and execute the comparison workflow for domain `$1`. "
        "Compare current audit scores against historical baseline "
        "and show improvement over time.",
    ),
    "compete": (
        "Run cross-engine competitor citation gap analysis for a domain and competitors",
        "Load the `geo` skill and execute the competitor gap analysis workflow "
        "for domain `$1` against competitors `$2`. "
        "Compare citation patterns across 6 AI engines and identify gap opportunities.",
    ),
    "content": (
        "Content quality and E-E-A-T assessment on a target URL",
        "Load the `geo` skill and execute the content quality assessment workflow on `$1`. "
        "Evaluate Experience, Expertise, Authoritativeness, Trustworthiness signals, "
        "measure content depth and readability, detect AI content indicators.",
    ),
    "crawlers": (
        "Check AI crawler access via robots.txt analysis on a target URL",
        "Load the `geo` skill and execute the AI crawler access check workflow on `$1`. "
        "Fetch robots.txt, parse directives for GPTBot, ClaudeBot, PerplexityBot, "
        "OAI-SearchBot, and other AI crawlers. Calculate crawler access score.",
    ),
    "distribute": (
        "Generate a tiered 14-day multi-platform distribution plan for a topic",
        "Load the `geo` skill and execute the distribution planning workflow for topic `$1`. "
        "Generate a tiered distribution plan across AI-cited platforms "
        "(Wikipedia, Reddit, LinkedIn, YouTube, industry sources) "
        "organized as a 14-day schedule.",
    ),
    "llmstxt": (
        "Analyze or generate llms.txt file for a target URL",
        "Load the `geo` skill and execute the llms.txt analysis workflow on `$1`. "
        "Check for existing llms.txt, validate format, "
        "and recommend or generate an optimized llms.txt file.",
    ),
    "matrix": (
        "Build a 4-quadrant intent matrix and 12-week schedule for a core topic",
        "Load the `geo` skill and execute the intent matrix workflow for core topic `$1`. "
        "Build a search intent matrix with informational, commercial, "
        "navigational, and transactional quadrants. "
        "Generate a 12-week content production schedule.",
    ),
    "page": (
        "Deep single-page GEO analysis on a target URL",
        "Load the `geo` skill and execute the deep single-page GEO analysis workflow on `$1`. "
        "Score citability, check AI crawler access, analyze structured data, "
        "and provide page-level GEO recommendations.",
    ),
    "pipeline": (
        "Run the 5-stage AI citation pipeline on a target URL",
        "Load the `geo` skill and execute the citation pipeline workflow on `$1`. "
        "Run the 5-stage pipeline: content analysis, citation gap detection, "
        "preferred-answer verification across 6 AI engines, "
        "and optimization recommendations.",
    ),
    "platforms": (
        "Platform-specific optimization analysis for a target URL",
        "Load the `geo` skill and execute the platform optimization workflow on `$1`. "
        "Score readiness for Google AI Overviews, ChatGPT web search, "
        "Perplexity AI, Google Gemini, and Bing Copilot. "
        "Provide platform-specific recommendations.",
    ),
    "proposal": (
        "Auto-generate a client proposal from audit data for a domain",
        "Load the `geo` skill and execute the proposal generation workflow for domain `$1`. "
        "Compile existing audit data into a professional client engagement proposal "
        "with scope, timeline, and pricing.",
    ),
    "prospect": (
        "Manage prospects through the sales pipeline",
        "Load the `geo` skill and execute the prospect management workflow. "
        "Accept subcommands via `$ARGUMENTS`: `add`, `list`, `status`, or `note`. "
        "Interact with the CRM-lite system.",
    ),
    "quick": (
        "Run a 60-second GEO visibility snapshot on a target URL",
        "Load the `geo` skill and execute the quick GEO visibility snapshot workflow on `$1`. "
        "Provide a rapid assessment of citability, crawler access, "
        "llms.txt, and brand presence with minimal depth.",
    ),
    "report-pdf": (
        "Generate a professional PDF report with charts and scores for a target URL",
        "Load the `geo` skill and execute the PDF report generation workflow on `$1`. "
        "Generate a professional PDF with GEO score breakdown, radar charts, "
        "category scores, and prioritized action plan using the Python PDF generator.",
    ),
    "report": (
        "Generate a client-ready GEO deliverable for a target URL",
        "Load the `geo` skill and execute the GEO report generation workflow on `$1`. "
        "Compile all audit findings into a structured client-ready deliverable markdown report.",
    ),
    "schema": (
        "Detect, validate, and generate structured data for a target URL",
        "Load the `geo` skill and execute the schema markup workflow on `$1`. "
        "Detect existing JSON-LD, validate against Schema.org spec, "
        "check GEO-critical schemas (Organization, Person, Article, "
        "sameAs, speakable), and generate missing schema templates.",
    ),
    "technical": (
        "Run a technical SEO audit with GEO-specific checks on a target URL",
        "Load the `geo` skill and execute the technical SEO audit workflow on `$1`. "
        "Check SSR/JS dependency, crawlability, meta tags, security headers, "
        "Core Web Vitals risk, mobile optimization, and URL structure.",
    ),
    "update": (
        "Pull the latest GEO skill updates from upstream",
        "Load the `geo` skill and execute the update workflow. "
        "Clone or pull the latest version of the GEO skills "
        "from the upstream repository using the update toolkit script.",
    ),
}


# ── Helpers ───────────────────────────────────────────────────────

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


def clone_or_pull_repo(upstream_url, target_dir, branch="main"):
    """Clone or pull the upstream repository into target_dir."""
    if target_dir.exists():
        print(f"Updating existing repo at {target_dir}...")
        subprocess.run(
            ["git", "checkout", branch],
            cwd=target_dir,
            capture_output=True,
            check=False,
        )
        subprocess.run(
            ["git", "pull", "--ff-only", "origin", branch],
            cwd=target_dir,
            check=False,
        )
    else:
        print(f"Cloning {upstream_url} into {target_dir} (branch: {branch})...")
        subprocess.run(
            ["git", "clone", "--branch", branch, upstream_url, str(target_dir)],
            check=True,
        )
    return target_dir


def copy_tree(src, dst, desc=""):
    """Copy src directory tree to dst, creating parents if needed."""
    if not src.is_dir():
        print(f"  SKIP: {desc} not found or not a directory at {src}")
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


def strip_frontmatter(text):
    """Remove YAML frontmatter (--- ... ---) and return the body."""
    m = re.match(r'^---\s*\n.*?\n---\s*\n', text, re.DOTALL)
    if m:
        return text[m.end():]
    return text


def generate_opencode_agents(src_dir, dst_dir):
    """Generate OpenCode agent files from Claude Code agent sources.

    Strips the Claude Code frontmatter from each .md in src_dir,
    prepends OpenCode-specific frontmatter, writes to dst_dir.
    """
    if not src_dir.is_dir():
        print(f"  SKIP: Agent source not found at {src_dir}")
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for src in sorted(src_dir.glob("geo-*.md")):
        name = src.stem
        body = strip_frontmatter(src.read_text())

        desc = _OC_AGENT_DESCRIPTIONS.get(
            name, f"GEO {name} specialist. Subagent for parallel GEO audit execution.",
        )

        frontmatter = (
            "---\n"
            f"description: >\n"
            f"  {desc}\n"
            f"mode: subagent\n"
            f"permission:\n"
            f"  read: allow\n"
            f"  edit: deny\n"
            f"  bash: allow\n"
            f"  webfetch: allow\n"
            f"  glob: allow\n"
            f"  grep: allow\n"
            "---\n"
            "\n"
        )

        dst = dst_dir / src.name
        dst.write_text(frontmatter + body)
        count += 1
    print(f"  OK: OpenCode agents -> {dst_dir} ({count} files)")


def generate_opencode_commands(dst_dir):
    """Generate OpenCode command files from the _GEO_COMMANDS dict."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for name, (description, body) in _GEO_COMMANDS.items():
        content = (
            "---\n"
            f'description: "{description}"\n'
            "---\n"
            "\n"
            f"{body}\n"
        )
        (dst_dir / f"geo-{name}.md").write_text(content)
        count += 1
    print(f"  OK: OpenCode commands -> {dst_dir} ({count} files)")


# ── Install logic ─────────────────────────────────────────────────

def install_for_platform(repo_dir, platform_name):
    """Install skills and agents for the given platform."""
    repo = Path(repo_dir)

    if platform_name == "claude-code":
        skills_dst = CLAUDE_SKILLS
        agents_src = repo / AGENTS_DIR
        agents_dst = CLAUDE_AGENTS
    elif platform_name == "opencode":
        skills_dst = CLAUDE_SKILLS  # shared skill path
        agents_src = repo / AGENTS_DIR  # single source of truth
        agents_dst = OPENCODE_AGENTS
    else:
        print(f"  Unknown platform: {platform_name}")
        return

    skills_dst.mkdir(parents=True, exist_ok=True)

    copy_tree(repo / SKILLS_DIR, skills_dst / SKILLS_DIR, "Skill orchestrator")
    for sub in sorted((repo / "skills").iterdir()):
        if sub.is_dir():
            copy_tree(sub, skills_dst / sub.name, f"Skill: {sub.name}")
    copy_tree(repo / "platform", skills_dst / "platform", "Platform adapter")
    copy_tree(repo / SCRIPTS_DIR, skills_dst / "geo" / SCRIPTS_DIR, "Scripts")
    copy_tree(repo / DOCS_DIR, skills_dst / "geo" / DOCS_DIR, "Documentation")
    copy_tree(repo / REGIONS_DIR, skills_dst / SKILLS_DIR / REGIONS_DIR, "Region profiles")

    if platform_name == "claude-code":
        copy_files(agents_src, agents_dst, "*.md", f"Agents ({platform_name})")
    elif platform_name == "opencode":
        generate_opencode_agents(agents_src, agents_dst)
        generate_opencode_commands(OPENCODE_COMMANDS)

    print(f"  Done: {platform_name}")


def install_all_platforms(repo_dir, platforms):
    """Install for all detected platforms."""
    for p in platforms:
        install_for_platform(repo_dir, p)


# ── CLI ───────────────────────────────────────────────────────────

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
        "--branch",
        default="main",
        help="Git branch to clone (default: %(default)s)",
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
        clone_or_pull_repo(args.upstream, repo_dir, args.branch)
    else:
        with tempfile.TemporaryDirectory(prefix="geo-seo-") as tmp:
            repo_dir = Path(tmp) / "geo-seo"
            clone_or_pull_repo(args.upstream, repo_dir, args.branch)
            install_all_platforms(repo_dir, platforms)
            print("\nInstallation complete.")
            return

    install_all_platforms(repo_dir, platforms)
    print("\nInstallation complete.")


if __name__ == "__main__":
    main()
