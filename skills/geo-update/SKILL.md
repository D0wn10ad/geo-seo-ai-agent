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
- `geo/SKILL.md` — orchestrator and `/geo` command table.
- `geo/commands/geo-*.md` — canonical OpenCode command wrappers (committed, never generated at install time).
- `skills/geo-*/SKILL.md` and vendored skills (for example `skills/uv/SKILL.md`) — npx discovers directories containing a `SKILL.md` and copies their hierarchy verbatim.
- `geo/scripts/` and `geo/regions/` — nested files and region profiles travel with the `geo` skill; the CN knowledge base lives in `geo/regions/cn/`.

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
  minimal env/deps bootstrap (`geo/scripts/bootstrap_env.sh`, using the pinned
  `geo/scripts/install_uv.sh` helper) if `requirements.txt` changed.

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

Do not pass legacy installer flags or deploy-time rewrite options; none exist
in the npx CLI and none are needed.

### Step 3: Verify

```
npx skills@1.9.0 check
```

Confirm the check is clean. Then verify the observable install surface:
- `geo/SKILL.md` is present in the installed `geo` skill, and the 21 canonical
  `geo/commands/geo-*.md` wrappers are present.
- `skills/geo-update/SKILL.md` still documents this fork and the pin.
- Scripts and region profiles remain nested under the installed `geo` skill.

### Step 4: Report results

Report to the user:
- Which agents/platforms were updated (Claude Code, OpenCode, or both).
- The pinned CLI version used (`1.9.0`) and the fork source.
- Whether env/deps bootstrap needs re-running.
- That changes take effect in new sessions; restart the AI client.
- That runtime data under `~/.geo-prospects/` is never touched by an update.
- That `--region <code>` (for example `--region cn`) still applies to `/geo` commands
  after the update, with CN knowledge from `geo/regions/cn/`.

---

## Legacy installs

`install.sh` and `install-win.sh` are legacy installers; `uninstall.sh` remains a
legacy-cleanup fallback. They do not distribute or update skills anymore. For a
legacy install, clean up with `uninstall.sh` (it preserves `~/.geo-prospects/`),
then perform a fresh `npx skills@1.9.0 add` as shown above.
