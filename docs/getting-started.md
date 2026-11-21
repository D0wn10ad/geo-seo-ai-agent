# Getting Started

## Supported platforms

- **macOS / Linux** — use the pinned `npx skills@1.9.0` command below.
- **Windows** — use the same pinned command from **Git Bash** (bundled with Git for Windows). PowerShell and Command Prompt are not supported; WSL is not required.

## Prerequisites

| Requirement | Why it's needed |
|---|---|
| Node.js + npx | Runs the pinned `skills@1.9.0` CLI installer |
| Python 3.10+ | Runs the utility scripts (pinned `lxml` needs 3.10+) |
| Claude Code CLI and/or OpenCode | Host runtime for the installed skills and agents |
| Internet access | Audits fetch live URLs and query AI-cited platforms |

### Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### OpenCode

```bash
npm install -g @opencode-ai/cli
```

---

## Installation

### Default: pinned npx add (both agents, one command)

This fork distributes skills exclusively through the pinned `skills` CLI. Run the
command below from any directory; no repository clone is required.

```bash
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git
```

- `-a claude-code -a opencode` installs into both agents at once. Keep only the
  `-a` flag for the agent you use.
- The `1.9.0` pin is deliberate. `skills-lock.json` in the install root records
  the pinned source and version, and the lock format and CLI surface change
  between releases. Never substitute an unpinned `npx skills`.
- Nothing is generated or rewritten at install time: the committed tree is the
  source of truth, and `SKILL.md` directories are copied verbatim with their
  nested `geo/commands/`, `geo/scripts/`, and `geo/regions/` files.

### Python dependencies — one-time bootstrap

`npx` does not install Python dependencies. From a clone of this repo, run the
pinned bootstrap helper and the checksum-keyed env bootstrap:

```bash
bash geo/scripts/install_uv.sh     # installs pinned uv 0.13.9 only if absent
bash geo/scripts/bootstrap_env.sh  # venv at ${XDG_CACHE_HOME:-~/.cache}/geo-seo-ai-agent/venv
```

If you are not in the repo, pass a `requirements.txt` path as the first argument
to `bootstrap_env.sh`. The script is idempotent: it re-runs only when
`requirements.txt` changes. It requires `uv` on `PATH` (installed above), uses
`uv venv` and `uv pip install`, and leaves your system Python untouched.

### LEGACY installers (not the default)

`install.sh` and `install-win.sh` are retained only as **LEGACY** installers for
older setups; they no longer distribute or update skills. If you previously used
one, clean up with `bash uninstall.sh` (it preserves `~/.geo-prospects/`) and then
run the pinned `npx skills@1.9.0 add` command above. Do not pipe either LEGACY
installer into `bash` for a new install.

---

## Verify the Install

After installation, open your AI agent CLI (Claude Code or OpenCode) in any
project directory and run:

```
/geo quick https://example.com
```

If the skill is wired up correctly, it starts a 60-second GEO visibility snapshot.
If you see "unknown command" or nothing happens, restart your AI agent CLI — it
reads skills and agents at startup.

Confirm the pinned install from the install root:

```bash
npx skills@1.9.0 check      # exits non-zero when a skill is behind its pin
cat skills-lock.json        # records the pinned source and version
```

To confirm the observable installed surface:

```bash
ls ~/.claude/skills/geo/SKILL.md
ls ~/.claude/skills/geo/commands/geo-*.md | wc -l   # expect 21
ls ~/.claude/skills/ | grep geo
ls ~/.claude/agents/ | grep geo
# OpenCode-specific:
ls ~/.config/opencode/agents/ | grep geo
ls ~/.config/opencode/commands/ | grep geo
```

---

## Check and Update

From the install root (the directory holding `skills-lock.json` / `.agents/skills/`):

```bash
npx skills@1.9.0 check
npx skills@1.9.0 update
```

A non-zero exit from `check` is the expected signal to run `update`. After the
update, re-run `check` to confirm a clean state. If `requirements.txt` changed,
re-run `geo/scripts/bootstrap_env.sh`. Restart your AI client so new sessions see
the updated skills; runtime data under `~/.geo-prospects/` is never touched.

**Pinning policy:** always invoke the CLI as `npx skills@1.9.0`. Bump the pin only
as a deliberate repo-wide change — update `skills/geo-update/SKILL.md`, the README
Quick Start, and these docs together, then re-run the full test suite and a fresh
`npx skills@1.9.0 add` verification. See
[skills/geo-update/SKILL.md](../skills/geo-update/SKILL.md) for the complete
workflow.

---

## Your First Audit

### Quick path — 60-second snapshot

```
/geo quick https://yoursite.com
```

Returns a high-level GEO visibility score and the top issues. Good for a first
look or a fast client check.

### Full path — complete audit

```
/geo audit https://yoursite.com
```

Launches five parallel subagents covering AI visibility, platform optimization,
technical SEO, content quality, and structured data. Produces a prioritized action
plan with a composite GEO score (0–100).

The full audit takes several minutes depending on the site. See
[scoring-methodology.md](scoring-methodology.md) for how the score is calculated
and [commands-reference.md](commands-reference.md) for all available commands.
For China-market audits, append `--region cn` to a `/geo` command; the region data
ships nested under the installed skill.

---

## Troubleshooting

**`npx`/Node not found**
- Symptom: `npx: command not found`
- Fix: install Node.js (which provides `npx`), reopen your terminal, and re-run the pinned `add` command.

**Skills not showing up**
- Symptom: `/geo quick` produces "unknown command" or no response
- Cause: the agent CLI reads skills and agents at startup
- Fix: fully quit and reopen your AI agent CLI. Re-run `npx skills@1.9.0 check` to confirm the install is current.

**Python not found during bootstrap**
- Symptom: `bootstrap_env.sh` cannot locate an interpreter
- Cause: Python 3.10+ is not installed or not on `PATH`
- Fix: install Python 3.10+ from [python.org](https://www.python.org/downloads/) (on Windows check "Add Python to PATH"), reopen your terminal, then re-run the bootstrap.

**`uv` not found during bootstrap**
- Symptom: `error: uv not found on PATH; run geo/scripts/install_uv.sh first`
- Fix: run `bash geo/scripts/install_uv.sh`, which installs the pinned uv 0.13.9 only if absent, then re-run `bash geo/scripts/bootstrap_env.sh`.

**Wrong shell on Windows**
- Symptom: `npx` or script syntax errors
- Cause: running commands in PowerShell or Command Prompt
- Fix: use Git Bash only — right-click the folder, "Open Git Bash here".

**Python dependencies failed**
- Symptom: the bootstrap reports a `uv pip install` failure
- Cause: network or permission error while installing from `requirements.txt`
- Fix: re-run `bash geo/scripts/bootstrap_env.sh` after resolving the network/permission issue. The bootstrap is checksum-keyed, so delete `${XDG_CACHE_HOME:-~/.cache}/geo-seo-ai-agent/.env-bootstrap-sentinel` first if you need a forced retry with an unchanged `requirements.txt`.

---

## Uninstall

For an **npx-managed** install, remove the skills through the same pinned CLI (this
leaves the lock/manifest and cache intact):

```bash
npx skills@1.9.0 remove    # select the geo / geo-* skills
```

`bash uninstall.sh` is retained as a **LEGACY-cleanup fallback** for installs made
by the old git-clone installer. It detects the npx layout; when found it deletes
nothing and only prints the pinned command above. On a LEGACY install it removes
only the old `~/.claude/skills/geo*`, `~/.claude/agents/geo-*.md`, and the OpenCode
agents/commands under `${XDG_CONFIG_HOME:-~/.config}`, with symlink-safe handling.

### Runtime data

The directory `~/.geo-prospects/` (used by `/geo prospect`, `/geo proposal`, and
`/geo compare`) is **always preserved** by both uninstall paths. Delete it
manually only if you no longer need the data:

```bash
rm -rf ~/.geo-prospects
```

---

See also: [architecture.md](architecture.md) | [commands-reference.md](commands-reference.md) | [scoring-methodology.md](scoring-methodology.md) | [skills-and-agents.md](skills-and-agents.md)
