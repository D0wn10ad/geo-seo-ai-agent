# Platform Tool Map

Abstract tool names used in instruction text → platform-specific tool names.

| Abstract name | Claude Code | OpenCode |
|---|---|---|
| `` `fetch_url` `` | `WebFetch` | `webfetch` |
| `` `run_command` `` | `Bash` | `bash` |
| `` `read_file` `` | `Read` | `read` |
| `` `write_file` `` | `Write` | `write` |
| `` `edit_file` `` | `Edit` | `edit` |
| `` `search_files` `` | `Glob` | `glob` |
| `` `search_content` `` | `Grep` | `grep` |

The AI resolves abstract names to the correct tool name based on platform detection.
