# Claude Tool Tracker

Visual tool usage logging with **real-time display** and detailed statistics for Claude Code.

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### Real-Time Display

See every tool call **as it happens** in the Claude console:

```
📊 MCP context7 → get-library-docs
📊 AGENT code-reviewer
📊 TOOL Read
📊 SKILL mem-search
```

### Visual Logging

Tool calls are categorized and color-coded:

- **MCP Servers** (Cyan) - External integrations like context7, playwright
- **Agents** (Magenta) - Task/subagent calls like code-reviewer, Explore
- **Skills** (Yellow) - Skill invocations
- **Commands** (Green) - Slash commands
- **Native Tools** (Blue) - Read, Write, Edit, Bash, Grep, etc.

### Statistics with Subcategory Breakdown

Track your tool usage patterns with detailed breakdowns:

```
==================================================
  SESSION STATISTICS
==================================================

  Native Tools      45 ███████████████ (75.0%)
    └─ Read                  (20)
    └─ Edit                  (12)
    └─ Bash                  (8)
    └─ Grep                  (5)

  MCP Servers       12 █████ (20.0%)
    └─ context7              (8)
    └─ playwright            (4)

  Agents             3 █ (5.0%)
    └─ code-reviewer         (2)
    └─ Explore               (1)

  Total: 60 tool calls
==================================================
```

### Theme Support

Choose your preferred visual style:

| Theme | Description |
|-------|-------------|
| **Colorful** | Full colored boxes with borders (default) |
| **Minimal** | Clean single-line format |
| **Emoji** | Emoji prefixes for quick scanning |

## Installation

### Quick Install

```bash
# Step 1: Add the marketplace source
claude plugins add-source yajinn-plugins https://raw.githubusercontent.com/yajinn/claude-tool-tracker/main/.claude-plugin/marketplace.json

# Step 2: Install the plugin
claude plugins add yajinn-plugins/claude-tool-tracker

# Step 3: Restart Claude Code
```

### Verify Installation

After restarting, use any tool and you'll see:
```
📊 TOOL Read
```

Check statistics with:
```bash
/tool-stats
```

### Local Development

```bash
git clone https://github.com/yajinn/claude-tool-tracker.git
cd claude-tool-tracker
claude plugins add ./
```

### Uninstall

```bash
claude plugins remove yajinn-plugins/claude-tool-tracker
claude plugins remove-source yajinn-plugins
```

## Usage

### Commands

| Command | Description |
|---------|-------------|
| `/tool-stats` | Show current session statistics with subcategory breakdown |
| `/tool-stats --all` | Show all-time statistics |
| `/tool-theme <theme>` | Change visual theme (colorful, minimal, emoji) |
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
MCP context7 → get-library-docs
AGENT code-reviewer
TOOL Read
```

#### Emoji

```
🌐 context7 → get-library-docs
🤖 code-reviewer
🔧 Read
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

## What's New in v1.1.0

- **Real-time console display** - See tool usage as it happens
- **Subcategory breakdown** - Detailed stats showing which MCP servers, agents, and tools are used
- **Improved minimal theme** - Cleaner, more readable format
- **Better installation** - Simplified installation process

## Requirements

- Python 3.7+
- Claude Code CLI

## License

MIT

## Author

Yasin Coskun ([@yajinn](https://github.com/yajinn))

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
