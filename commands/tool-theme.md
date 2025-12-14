---
description: Change the visual theme for tool tracking display
argument-hint: "<colorful|minimal|emoji>"
---

# Tool Theme Command

Change the visual theme used by claude-tool-tracker for displaying tool usage.

## Usage

- `/tool-theme colorful` - Full colored boxes with borders (default)
- `/tool-theme minimal` - Single line, muted colors
- `/tool-theme emoji` - Emoji prefixes instead of boxes

## Themes Preview

### Colorful (Default)
```
┌───────────────────────────────────────────────┐
│ MCP  context7 → get-library-docs              │
└───────────────────────────────────────────────┘
```

### Minimal
```
[MCP] context7 → get-library-docs
```

### Emoji
```
🌐 context7 → get-library-docs
```

## What to do

When the user runs this command:

1. Validate the theme argument is one of: `colorful`, `minimal`, `emoji`

2. Update the configuration by running:
   ```bash
   python3 -c "
   import sys
   sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
   from config import set_theme
   result = set_theme('THEME_NAME')
   print('Theme updated successfully!' if result else 'Failed to update theme')
   "
   ```
   Replace `THEME_NAME` with the user's choice.

3. Confirm the change to the user.

If no argument provided or invalid theme, show available options.
