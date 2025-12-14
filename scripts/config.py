#!/usr/bin/env python3
"""
Configuration manager for claude-tool-tracker plugin.
Handles reading and writing configuration from .local.md files.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration
DEFAULT_CONFIG = {
    "theme": "colorful",  # colorful (default), minimal (clean), emoji
    "stats_location": "global",  # global, local
    "enabled_categories": ["native", "mcp", "agent", "skill", "command"],
    "show_stats_on_exit": False,
}

# Config file name
CONFIG_FILENAME = "claude-tool-tracker.local.md"


def get_global_config_path() -> Path:
    """Get path to global config file."""
    return Path.home() / ".claude" / CONFIG_FILENAME


def get_local_config_path() -> Optional[Path]:
    """Get path to local (project) config file if exists."""
    cwd = Path.cwd()
    local_path = cwd / ".claude" / CONFIG_FILENAME
    if local_path.exists():
        return local_path
    return None


def parse_yaml_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from markdown content."""
    config = {}

    # Match YAML frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return config

    yaml_content = match.group(1)

    # Simple YAML parsing for our use case
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Handle different value types
            if value.lower() == 'true':
                config[key] = True
            elif value.lower() == 'false':
                config[key] = False
            elif value.startswith('[') or value.startswith('-'):
                # Handle list (inline or multiline)
                continue  # Skip for now, handle below
            else:
                config[key] = value

    # Handle multiline lists (enabled_categories)
    lines = yaml_content.split('\n')
    current_key = None
    current_list = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- '):
            if current_key:
                current_list.append(stripped[2:].strip())
        elif ':' in stripped and not stripped.startswith('#'):
            if current_key and current_list:
                config[current_key] = current_list
            key = stripped.split(':')[0].strip()
            value = stripped.split(':', 1)[1].strip() if ':' in stripped else ''
            if not value:
                current_key = key
                current_list = []
            else:
                current_key = None
                current_list = []

    if current_key and current_list:
        config[current_key] = current_list

    return config


def load_config() -> Dict[str, Any]:
    """Load configuration, merging local over global over defaults."""
    config = DEFAULT_CONFIG.copy()

    # Load global config
    global_path = get_global_config_path()
    if global_path.exists():
        try:
            content = global_path.read_text()
            global_config = parse_yaml_frontmatter(content)
            config.update(global_config)
        except Exception:
            pass

    # Load local config (overrides global)
    local_path = get_local_config_path()
    if local_path:
        try:
            content = local_path.read_text()
            local_config = parse_yaml_frontmatter(content)
            config.update(local_config)
        except Exception:
            pass

    return config


def save_config(config: Dict[str, Any], location: str = "global") -> bool:
    """Save configuration to file."""
    if location == "global":
        config_path = get_global_config_path()
    else:
        config_path = Path.cwd() / ".claude" / CONFIG_FILENAME

    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate YAML content
    yaml_lines = ["---"]
    for key, value in config.items():
        if isinstance(value, bool):
            yaml_lines.append(f"{key}: {str(value).lower()}")
        elif isinstance(value, list):
            yaml_lines.append(f"{key}:")
            for item in value:
                yaml_lines.append(f"  - {item}")
        else:
            yaml_lines.append(f"{key}: {value}")
    yaml_lines.append("---")
    yaml_lines.append("")
    yaml_lines.append("# Claude Tool Tracker Configuration")
    yaml_lines.append("")
    yaml_lines.append("This file contains settings for the claude-tool-tracker plugin.")
    yaml_lines.append("Edit the YAML frontmatter above to customize behavior.")

    content = '\n'.join(yaml_lines)

    try:
        config_path.write_text(content)
        return True
    except Exception:
        return False


def get_theme() -> str:
    """Get current theme setting."""
    config = load_config()
    return config.get("theme", "colorful")


def set_theme(theme: str) -> bool:
    """Set theme and save to config."""
    if theme not in ["colorful", "minimal", "emoji"]:
        return False

    config = load_config()
    config["theme"] = theme
    return save_config(config)


def get_stats_location() -> str:
    """Get stats storage location setting."""
    config = load_config()
    return config.get("stats_location", "global")


def is_category_enabled(category: str) -> bool:
    """Check if a category is enabled for logging."""
    config = load_config()
    enabled = config.get("enabled_categories", DEFAULT_CONFIG["enabled_categories"])
    return category in enabled


if __name__ == "__main__":
    # Test config loading
    print("Current config:", load_config())
