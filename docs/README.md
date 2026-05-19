# GEO-SEO AI Agent Skill — Documentation

`geo-seo-claude` is a multi-platform AI agent skill bundle that runs GEO (Generative Engine Optimization) and SEO audits against a website. It works with both **Claude Code** and **OpenCode** (with superpowers). It orchestrates 20 sub-skills, 5 parallel subagents, and a set of Python utilities to produce a composite GEO Score (0–100) and a prioritized action plan.

If you are new here, start with **Getting Started**. If you are contributing, skim **Architecture** and **Skills & Agents** first.

## Contents

 | Doc | What's in it |
|-----|--------------|
| [Getting Started](getting-started.md) | Prerequisites, install (Claude Code / OpenCode, macOS/Linux/Windows), first audit, troubleshooting, uninstall. |
| [Commands Reference](commands-reference.md) | Every `/geo` slash command with usage, arguments, output, and when to use it. |
| [Architecture](architecture.md) | Repo layout, audit flow, parallel subagent dispatch, data storage. |
| [Skills & Agents](skills-and-agents.md) | Reference for every sub-skill, subagent, Python script, and schema template. |
| [Scoring Methodology](scoring-methodology.md) | How the composite GEO Score is computed, per-category signals, caveats. |
| [FAQ](faq.md) | Common questions for users and contributors. |
| [Contributing](../CONTRIBUTING.md) | How to report bugs, propose features, and open PRs. |

## Quick links

- First audit: [Getting Started → Your First Audit](getting-started.md#your-first-audit)
- Full command list: [Commands Reference](commands-reference.md)
- Weight table: [Scoring Methodology](scoring-methodology.md)
- Parallel audit flow: [Architecture → Full Audit Flow](architecture.md)
