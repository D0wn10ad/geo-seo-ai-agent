# Frequently Asked Questions

---

## General

### What is GEO and how is it different from SEO?

SEO (Search Engine Optimization) targets ranking in traditional search engines like Google's blue-link results. GEO (Generative Engine Optimization) targets visibility inside AI-generated answers from systems like ChatGPT, Perplexity, Claude, Gemini, and Google AI Overviews. The two disciplines overlap — technical foundations and content quality matter for both — but GEO adds concerns specific to AI retrieval: citability scoring, brand mention density, llms.txt, and entity recognition across AI-cited platforms.

### Is this a paid tool or service?

The tool itself is free and MIT-licensed. It runs entirely within your own AI agent session (Claude Code or OpenCode) using your existing platform subscription. There is no separate API key, usage meter, or subscription for the skill bundle itself.

### Who is this for?

GEO agencies running client audits, in-house marketing teams monitoring AI search visibility, content creators optimizing individual pages for AI citations, and developers building or maintaining web properties who want actionable GEO and SEO feedback without a SaaS subscription.

### Does this replace my existing SEO stack?

No. It complements existing tools. The `/geo technical` command covers technical SEO foundations, but the tool does not replace crawlers like Screaming Frog, keyword research platforms, or rank trackers. Its primary value is the GEO layer — AI citability, crawler access, brand signals, and platform readiness — that most traditional SEO tools do not cover.

---

## Installation & Setup

### Why do I need Claude Code CLI or OpenCode?

The skill bundle is implemented as AI agent slash commands. All commands (`/geo audit`, `/geo quick`, etc.) are routed through the host platform's skill and agent system. The CLI is the runtime; without it, there is nothing to execute the skill files. For Claude Code: `npm install -g @anthropic-ai/claude-code`. For OpenCode: `npm install -g @opencode-ai/cli` plus the superpowers plugin.

### Can I run this on Windows without WSL?

Yes, but you must use Git Bash, not PowerShell or Command Prompt. The Windows installer is `install-win.sh` and requires Git for Windows (which bundles Git Bash). Right-click the repo folder and select "Open Git Bash here", then run `./install-win.sh`. WSL is not required.

### What does `install.sh` actually do?

It checks for Git and Python 3.8+, then delegates file copying to `scripts/update_toolkit.py` which copies files into the shared skill directory (`~/.claude/skills/geo/`), platform-specific agent directories, and OpenCode command wrappers. It then creates an isolated Python virtual environment and installs dependencies from `requirements.txt`. If you run it interactively, it also offers to install the Playwright Chromium browser for screenshot support. The installer works both from a cloned local directory and via a `curl | bash` pipe from the repository URL.

### Do I need Playwright?

Playwright is optional. The installer prompts you to install it (`python3 -m playwright install chromium`). Without it, screenshot-based features are unavailable but all other audit and analysis commands function normally. You can install it later at any time.

---

## Usage

### What is the difference between `/geo quick` and `/geo audit`?

`/geo quick` produces a 60-second inline visibility snapshot and writes no output file. It is useful for a fast read on a URL before committing to a full run. `/geo audit` is the full workflow: it fetches the site, detects the business type, launches 5 parallel subagents, aggregates scores across all categories, and writes a `GEO-AUDIT-REPORT.md` with a prioritized action plan. See [commands-reference.md](commands-reference.md) for the complete command list.

### Where does the composite GEO Score come from?

The score (0-100) is a weighted aggregate across six categories: AI Citability & Visibility (25%), Brand Authority Signals (20%), Content Quality & E-E-A-T (20%), Technical Foundations (15%), Structured Data (10%), and Platform Optimization (10%). See [scoring-methodology.md](scoring-methodology.md) for how individual signals within each category are measured.

### How do the parallel subagents work?

During a full audit, five subagents run simultaneously after the initial discovery phase: `geo-ai-visibility`, `geo-platform-analysis`, `geo-technical`, `geo-content`, and `geo-schema`. Each maps to an agent definition file (in `~/.claude/agents/` for Claude Code or `~/.config/opencode/agents/` for OpenCode) and is responsible for a distinct slice of the analysis. The host platform's agent system handles the parallel dispatch; the orchestrator then collects all five reports and synthesizes the composite score. See [architecture.md](architecture.md) for the full flow.

### Where is prospect, proposal, and report data stored?

Data from `/geo prospect`, `/geo proposal`, and `/geo compare` is written to `~/.geo-prospects/` outside the platform directories. The structure is:

```
~/.geo-prospects/
├── prospects.json
├── proposals/<domain>-proposal-<date>.md
└── reports/<domain>-monthly-<YYYY-MM>.md
```

This directory is intentionally not removed by `uninstall.sh`. Delete it manually with `rm -rf ~/.geo-prospects` if you want to discard your prospect data.

---

## Contributing

### How do I add a new sub-skill?

Create a new directory under `skills/` following the naming pattern `geo-<skill-name>/`. Add a `SKILL.md` inside it that defines the skill's name, description, and logic. If the skill should participate in the full audit, register it in the appropriate agent file under `agents/`. Follow the structure of an existing sub-skill such as `skills/geo-citability/` as a reference. See [skills-and-agents.md](skills-and-agents.md) for a map of how skills and agents relate.

### How do I test my changes before opening a PR?

Run `./install.sh` from a local clone — the script detects a local `geo/SKILL.md` and installs from the working directory rather than cloning from GitHub. Open your AI agent CLI (Claude Code or OpenCode) and exercise the affected commands against a real URL. Verify that all status checks pass before submitting your pull request, as noted in `CONTRIBUTING.md`.

### Where do I report bugs or request features?

Open an issue on GitHub. For bugs, include a clear description, the URL you were auditing if relevant, and any error output. For feature requests, explain the use case and why it matters. Search existing issues first to avoid duplicates. Both are tracked under the repository's Issues tab.

---

## Limitations

### Can this tool guarantee AI citations or rankings?

No. The tool audits signals that correlate with AI visibility and provides recommendations to improve them, but no tool can guarantee that any AI system will cite or surface a specific domain. AI retrieval is probabilistic and varies by query, platform, and model version.

### Can I use this with OpenCode?

Yes. The project provides `.opencode/agents/` (5 agent definitions in OpenCode's `permission:` frontmatter format) and `.opencode/commands/` (21 command wrappers). Install with `python3 scripts/update_toolkit.py`. The `platform/` adapter layer resolves abstract tool names (`` `fetch_url` `` → `webfetch`) at runtime.

### Does it submit anything to third-party services?

The skill uses `` `fetch_url` `` and `` `run_command` `` (via `curl`) to fetch the URLs you provide, and the brand mention scanner checks publicly accessible platforms (YouTube, Reddit, Wikipedia, LinkedIn, and others) for brand signals. No audit data is sent to any third-party analytics endpoint. Your data stays within your AI agent session and your local filesystem.
