---
description: Display tool usage statistics for the current session or all time
argument-hint: "[--all]"
---

# Tool Statistics Command

Display statistics about tool usage tracked by claude-tool-tracker.

## Usage

- `/tool-stats` - Show current session statistics
- `/tool-stats --all` - Show all-time statistics

## What to do

When the user runs this command:

1. Run the stats display script:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/stats.py
   ```

2. If `--all` argument is provided, show all-time statistics instead of session-only.

3. Present the statistics in a clear, visual format showing:
   - Category breakdown (Native, MCP, Agent, Skill, Command)
   - Top 5 most used tools
   - Total tool call count

## Example Output

```
==================================================
  SESSION STATISTICS
==================================================

  Native Tools       31 ████████████████ (75.6%)
  MCP Servers         8 █████ (19.5%)
  Agents              2 █ (4.9%)
  Skills              0  (0.0%)
  Commands            0  (0.0%)

  Total: 41 tool calls

  Top 5 Tools:
    1. Read                      (15)
    2. Edit                      (8)
    3. Bash                      (5)
    4. context7:get-library-docs (4)
    5. Grep                      (3)
==================================================
```
