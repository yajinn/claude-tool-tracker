# Claude Tool Tracker

Visual tool usage logging with statistics and theme support for Claude Code.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### Visual Logging

See every tool call categorized and color-coded:

- **MCP Servers** - Cyan boxes for external integrations
- **Agents** - Magenta boxes for Task/subagent calls
- **Skills** - Yellow boxes for skill invocations
- **Commands** - Green boxes for slash commands
- **Native Tools** - Blue boxes for Read, Write, Edit, Bash, etc.

### Statistics Tracking

Track your tool usage patterns:

- Session-based and all-time statistics
- Category breakdown with visual bars
- Top 5 most used tools
- Persistent storage (global or per-project)

### Theme Support

Choose your preferred visual style:

| Theme | Description |
|-------|-------------|
| **Colorful** | Full colored boxes with borders (default) |
| **Minimal** | Single line, muted colors |
| **Emoji** | Emoji prefixes for quick scanning |

## Installation

### From GitHub

```bash
claude plugins add yasincoskun/claude-tool-tracker
```

### Local Development

```bash
claude plugins add /path/to/claude-tool-tracker
```

## Usage

### Commands

| Command | Description |
|---------|-------------|
| `/tool-stats` | Show current session statistics |
| `/tool-stats --all` | Show all-time statistics |
| `/tool-theme <theme>` | Change visual theme |
| `/tool-config` | View/modify configuration |

### Theme Examples

#### Colorful (Default)

```
┌───────────────────────────────────────────────┐
│ MCP  context7 → get-library-docs              │
└───────────────────────────────────────────────┘

┌───────────────────────────────────────────────┐
│ AGENT  code-reviewer                          │
│ Task: Review authentication changes           │
└───────────────────────────────────────────────┘

┌───────────────────────────────────────────────┐
│ TOOL  Read                                    │
└───────────────────────────────────────────────┘
```

#### Minimal

```
[MCP] context7 → get-library-docs
[AGE] code-reviewer
[NAT] Read
```

#### Emoji

```
🌐 context7 → get-library-docs
🤖 code-reviewer
🔧 Read
```

### Statistics Output

```
==================================================
  SESSION STATISTICS
==================================================

  Native Tools       45 ████████████████████ (75.0%)
  MCP Servers        12 █████ (20.0%)
  Agents              2 █ (3.3%)
  Skills              1  (1.7%)
  Commands            0  (0.0%)

  Total: 60 tool calls

  Top 5 Tools:
    1. Read                      (28)
    2. Edit                      (12)
    3. Bash                      (8)
    4. context7:get-library-docs (6)
    5. Grep                      (5)
==================================================
```

## Configuration

Configuration is stored in `~/.claude/claude-tool-tracker.local.md` (global) or `.claude/claude-tool-tracker.local.md` (per-project).

### Options

```yaml
---
theme: colorful           # colorful, minimal, emoji
stats_location: global    # global, local
enabled_categories:       # Categories to track
  - native
  - mcp
  - agent
  - skill
  - command
show_stats_on_exit: false # Show stats when session ends
---
```

### Stats Storage

- **Global**: `~/.claude/claude-tool-tracker/stats.json`
- **Local**: `.claude/claude-tool-tracker/stats.json`

## Requirements

- Python 3.7+
- Claude Code CLI

## License

MIT

## Author

Yasin Coskun ([@yasincoskun](https://github.com/yasincoskun))

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
