# Platform Adapter

This skill provides a platform detection and tool mapping layer for geo-seo-ai-agent. It must be loaded before any geo skill or agent.

## Platform Detection

The adapter detects the platform by checking for platform-specific configuration:

- **Claude Code**: `~/.claude/` directory exists (without OpenCode config)
- **OpenCode**: `~/.config/opencode/opencode.json` exists

## Tool Mapping

Instruction text across all skills and agents uses **abstract tool names** in backticks. Resolve them to the real tool name based on the detected platform:

| Abstract | Claude Code | OpenCode |
|---|---|---|
| `` `fetch_url` `` | `WebFetch` | `webfetch` |
| `` `run_command` `` | `Bash` | `bash` |
| `` `read_file` `` | `Read` | `read` |
| `` `write_file` `` | `Write` | `write` |
| `` `edit_file` `` | `Edit` | `edit` |
| `` `search_files` `` | `Glob` | `glob` |
| `` `search_content` `` | `Grep` | `grep` |

When you encounter an abstract tool name in instruction text (e.g., `` `fetch_url` ``), substitute the platform-specific tool name before invoking.
