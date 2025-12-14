---
description: View or modify claude-tool-tracker configuration
argument-hint: "[show|set <key> <value>]"
---

# Tool Config Command

View or modify claude-tool-tracker plugin configuration.

## Usage

- `/tool-config` or `/tool-config show` - Display current configuration
- `/tool-config set theme <colorful|minimal|emoji>` - Set display theme
- `/tool-config set stats_location <global|local>` - Set stats storage location

## Configuration Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `theme` | colorful, minimal, emoji | colorful | Visual display theme |
| `stats_location` | global, local | global | Where to store statistics |
| `show_stats_on_exit` | true, false | false | Show stats when session ends |

### Stats Location

- **global**: Stats stored in `~/.claude/claude-tool-tracker/stats.json` (shared across all projects)
- **local**: Stats stored in `.claude/claude-tool-tracker/stats.json` (project-specific)

## What to do

When the user runs this command:

### Show Configuration
```bash
python3 -c "
import sys
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
from config import load_config
import json
config = load_config()
print(json.dumps(config, indent=2))
"
```

### Set Configuration
```bash
python3 -c "
import sys
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
from config import load_config, save_config
config = load_config()
config['KEY'] = VALUE
save_config(config)
print('Configuration updated!')
"
```

Present the current configuration in a readable format and confirm any changes.
