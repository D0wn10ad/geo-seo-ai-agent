---
name: geo-update
description: Check and update the pinned npx skills install for this fork across Claude Code and OpenCode.
---

# GEO-SEO Update Skill

## Purpose

Check for and apply updates to the locally installed GEO-SEO skills from **this fork**,
[D0wn10ad/geo-seo-ai-agent](https://github.com/D0wn10ad/geo-seo-ai-agent), using the
pinned `skills` CLI. `npx skills add` is the only skill-distribution path; there is no
git-clone/copy updater script and no deploy-time rewriting of installed markdown.

Source of truth for what gets installed is the committed tree itself:
- `skills/geo/SKILL.md` — orchestrator and `/geo` command table.
- `skills/geo-*/SKILL.md` and vendored skills (for example `skills/uv/SKILL.md`) — npx discovers directories containing a `SKILL.md` and copies their hierarchy verbatim. npx distributes skills only; it does not install command files.
- `skills/geo/scripts/`, `skills/geo/assets/schema/` and `skills/geo/references/regions/` — nested utilities, JSON-LD templates and region profiles travel with the `geo` skill. The CN knowledge base lives in `skills/geo/references/regions/cn/`, and the 17 CN skill companions live at `skills/<geo-x>/references/cn.md`.

---

## Pinning policy

The upgrade path is `skills check` followed by `skills update`, always invoked
with the pinned prefix: `npx skills@1.9.0 check` and `npx skills@1.9.0 update`.

Always invoke the CLI as `npx skills@1.9.0`. Do **not** use an unpinned `npx skills`:
the tool's lock format and CLI surface change between releases, and an unpinned
invocation can silently rewrite the install. The pin is deliberately repeated in
this skill so the documented commands are executable as written.

- `skills-lock.json` in the install root records the pinned source and version for
  each installed skill; `skills update` honors it.
- Bump the pin only as a deliberate, repo-wide change: update this skill, the README
  quick start, and the docs together, then re-run the full suite and a fresh
  `npx skills@1.9.0 add` verification.
- Both targets are supported in one command: `-a claude-code -a opencode`.
- Python dependencies are **not** installed by npx. After an update, re-run the
  minimal env/deps bootstrap (`skills/geo/scripts/bootstrap_env.sh`, using the
  pinned `skills/geo/scripts/install_uv.sh` helper) if `requirements.txt` changed.

---

## Update Workflow

### Step 1: Check for updates

From the install root (the directory holding `skills-lock.json` / `.agents/skills/`):

```
npx skills@1.9.0 check
```

The command exits non-zero when an installed skill is behind its pinned source;
that is an expected signal to continue to Step 2, not an error to ignore.

### Step 2: Apply updates

```
npx skills@1.9.0 update
```

Use the recorded targets from `skills-lock.json`. If the install must be rebuilt
for both agents, the equivalent add form is:

```
npx skills@1.9.0 add -a claude-code -a opencode -y https://github.com/D0wn10ad/geo-seo-ai-agent.git
```

Do not pass old git-clone flags or deploy-time rewrite options; none exist in
the npx CLI and none are needed.

### Step 3: Verify

```
npx skills@1.9.0 check
```

Confirm the check is clean. Then verify the observable install surface:
- The orchestrator `geo/SKILL.md` is present in the installed `geo` skill, and
  the 21 `geo-*` worker skills are installed under the single `skills/` root.
- `skills/geo-update/SKILL.md` still documents this fork and the pin.
- Scripts, JSON-LD templates and region profiles remain nested under the
  installed `geo` skill (`scripts/`, `assets/schema/`, `references/regions/`).

### Step 4: Report results

Report to the user:
- Which agents/platforms were updated (Claude Code, OpenCode, or both).
- The pinned CLI version used (`1.9.0`) and the fork source.
- Whether env/deps bootstrap needs re-running.
- That changes take effect in new sessions; restart the AI client.
- That runtime data under `~/.geo-prospects/` is never touched by an update.
- That `--region <code>` (for example `--region cn`) still applies to `/geo` commands
  after the update, with CN knowledge from `skills/geo/references/regions/cn/` and
  the 17 companions at `skills/<geo-x>/references/cn.md`.

---

## Pre-npx installs

The old git-clone install scripts were deleted; `uninstall.sh` remains a
cleanup fallback only. npx is the only install and update path. For a pre-npx
install, clean up with `uninstall.sh` (it preserves `~/.geo-prospects/`), then
perform a fresh `npx skills@1.9.0 add` as shown above.
