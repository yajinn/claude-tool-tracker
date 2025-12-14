#!/usr/bin/env python3
"""
Main hook for claude-tool-tracker plugin.
Logs tool usage with visual formatting and tracks statistics.
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path for imports
plugin_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(plugin_root / "scripts"))

from config import load_config, is_category_enabled
from stats import record_tool_usage, categorize_tool

# ANSI Color codes
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'

# Colors
CYAN = '\033[36m'
MAGENTA = '\033[35m'
YELLOW = '\033[33m'
GREEN = '\033[32m'
BLUE = '\033[34m'
WHITE = '\033[37m'
GRAY = '\033[90m'

# Background colors
BG_CYAN = '\033[46m'
BG_MAGENTA = '\033[45m'
BG_YELLOW = '\033[43m'
BG_GREEN = '\033[42m'
BG_BLUE = '\033[44m'


def render_colorful(tool_type: str, primary: str, secondary: str = "", extra: str = "") -> str:
    """Render tool usage in colorful theme (default)."""
    colors = {
        "mcp": (CYAN, BG_CYAN),
        "agent": (MAGENTA, BG_MAGENTA),
        "skill": (YELLOW, BG_YELLOW),
        "command": (GREEN, BG_GREEN),
        "native": (BLUE, BG_BLUE)
    }

    color, bg_color = colors.get(tool_type, (BLUE, BG_BLUE))
    label = tool_type.upper()

    lines = []
    lines.append(f"{BOLD}{color}\u250c{'─' * 47}\u2510{RESET}")

    if secondary:
        lines.append(f"{BOLD}{color}\u2502{RESET} {bg_color}{BOLD}{WHITE} {label} {RESET} {color}{primary}{RESET} {DIM}→{RESET} {BOLD}{secondary}{RESET}")
    else:
        lines.append(f"{BOLD}{color}\u2502{RESET} {bg_color}{BOLD}{WHITE} {label} {RESET} {color}{primary}{RESET}")

    if extra:
        lines.append(f"{BOLD}{color}\u2502{RESET} {DIM}{extra}{RESET}")

    lines.append(f"{BOLD}{color}\u2514{'─' * 47}\u2518{RESET}")

    return '\n'.join(lines)


def render_minimal(tool_type: str, primary: str, secondary: str = "", extra: str = "") -> str:
    """Render tool usage in minimal/clean theme (screenshot format)."""
    colors = {
        "mcp": CYAN,
        "agent": MAGENTA,
        "skill": YELLOW,
        "command": GREEN,
        "native": GREEN  # TOOL prefix in green
    }

    # Labels matching screenshot format
    labels = {
        "mcp": "MCP",
        "agent": "AGENT",
        "skill": "SKILL",
        "command": "CMD",
        "native": "TOOL"  # Screenshot shows "TOOL Read"
    }

    color = colors.get(tool_type, GRAY)
    label = labels.get(tool_type, tool_type.upper())

    if secondary:
        return f"{color}{label} {primary} → {secondary}{RESET}"
    else:
        return f"{color}{label} {primary}{RESET}"


def render_emoji(tool_type: str, primary: str, secondary: str = "", extra: str = "") -> str:
    """Render tool usage in emoji theme."""
    emojis = {
        "mcp": "\U0001F310",      # Globe
        "agent": "\U0001F916",    # Robot
        "skill": "\u26A1",         # Lightning
        "command": "\U0001F4DD",  # Memo
        "native": "\U0001F527"    # Wrench
    }

    emoji = emojis.get(tool_type, "\U0001F527")

    if secondary:
        return f"{emoji} {primary} → {secondary}"
    else:
        return f"{emoji} {primary}"


def parse_tool_info(tool_name: str, tool_input: dict) -> tuple:
    """Parse tool information and return (type, primary, secondary, extra, detailed_name).

    detailed_name is used for stats tracking with subcategory info.
    """

    if tool_name.startswith("mcp__"):
        # MCP Tool - Format: mcp__server__toolname
        without_prefix = tool_name[5:]  # Remove "mcp__"
        parts = without_prefix.split("__", 1)
        server = parts[0] if parts else "unknown"
        actual_tool = parts[1] if len(parts) > 1 else "unknown"
        # detailed_name: mcp:context7:get-library-docs
        detailed_name = f"mcp:{server}:{actual_tool}"
        return ("mcp", server, actual_tool, "", detailed_name)

    elif tool_name == "Task":
        # Agent/Subagent call
        subagent_type = tool_input.get("subagent_type", "general")
        description = tool_input.get("description", "")
        extra = f"Task: {description}" if description else ""
        # detailed_name: agent:code-reviewer
        detailed_name = f"agent:{subagent_type}"
        return ("agent", subagent_type, "", extra, detailed_name)

    elif tool_name == "Skill":
        # Skill/Plugin call
        skill_name = tool_input.get("skill", "unknown")
        # detailed_name: skill:mem-search
        detailed_name = f"skill:{skill_name}"
        return ("skill", skill_name, "", "", detailed_name)

    elif tool_name == "SlashCommand":
        # Slash command
        command = tool_input.get("command", "unknown")
        # detailed_name: cmd:/commit
        detailed_name = f"cmd:{command}"
        return ("command", command, "", "", detailed_name)

    else:
        # Native Claude Code tools
        # detailed_name: native:Read
        detailed_name = f"native:{tool_name}"
        return ("native", tool_name, "", "", detailed_name)


def render_output(tool_type: str, primary: str, secondary: str, extra: str, theme: str) -> str:
    """Render output based on theme."""
    if theme == "minimal":
        return render_minimal(tool_type, primary, secondary, extra)
    elif theme == "emoji":
        return render_emoji(tool_type, primary, secondary, extra)
    else:  # colorful (default)
        return render_colorful(tool_type, primary, secondary, extra)


def render_system_message(tool_type: str, primary: str, secondary: str = "") -> str:
    """Render clean message for systemMessage output (no ANSI colors)."""
    labels = {
        "mcp": "MCP",
        "agent": "AGENT",
        "skill": "SKILL",
        "command": "CMD",
        "native": "TOOL"
    }
    label = labels.get(tool_type, tool_type.upper())

    if secondary:
        return f"{label} {primary} → {secondary}"
    else:
        return f"{label} {primary}"


def main():
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "unknown")
        tool_input = input_data.get("tool_input", {})

        # Load configuration
        config = load_config()
        theme = config.get("theme", "colorful")

        # Parse tool information
        tool_type, primary, secondary, extra, detailed_name = parse_tool_info(tool_name, tool_input)

        # Check if category is enabled
        if is_category_enabled(tool_type):
            # Record statistics with detailed name for subcategory tracking
            record_tool_usage(detailed_name)

            # Generate display message for systemMessage (visible in console)
            display_msg = render_system_message(tool_type, primary, secondary)

            # Also render themed output to stderr (visible in verbose mode)
            output = render_output(tool_type, primary, secondary, extra, theme)
            print(output, file=sys.stderr)

            # Return success response with systemMessage for console visibility
            response = {
                "continue": True,
                "suppressOutput": False,
                "systemMessage": f"📊 {display_msg}"
            }
        else:
            response = {
                "continue": True,
                "suppressOutput": False
            }

        print(json.dumps(response))

    except Exception as e:
        # On error, still allow the tool to proceed
        print(json.dumps({
            "continue": True,
            "suppressOutput": False,
            "systemMessage": f"Tool tracker error: {str(e)}"
        }))


if __name__ == "__main__":
    main()
