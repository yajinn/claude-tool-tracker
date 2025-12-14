#!/usr/bin/env python3
"""
Statistics manager for claude-tool-tracker plugin.
Handles tracking and persisting tool usage statistics.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Import config to get stats location
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_stats_location

STATS_DIR_NAME = "claude-tool-tracker"
STATS_FILENAME = "stats.json"


def get_stats_path() -> Path:
    """Get path to stats file based on configuration."""
    location = get_stats_location()

    if location == "local":
        base_path = Path.cwd() / ".claude" / STATS_DIR_NAME
    else:  # global
        base_path = Path.home() / ".claude" / STATS_DIR_NAME

    return base_path / STATS_FILENAME


def get_current_session_id() -> str:
    """Get or create current session ID based on date."""
    return datetime.now().strftime("%Y-%m-%d")


def load_stats() -> Dict[str, Any]:
    """Load statistics from file."""
    stats_path = get_stats_path()

    if not stats_path.exists():
        return {
            "sessions": {},
            "totals": {
                "tools": {},
                "categories": {
                    "native": 0,
                    "mcp": 0,
                    "agent": 0,
                    "skill": 0,
                    "command": 0
                }
            }
        }

    try:
        with open(stats_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "sessions": {},
            "totals": {
                "tools": {},
                "categories": {
                    "native": 0,
                    "mcp": 0,
                    "agent": 0,
                    "skill": 0,
                    "command": 0
                }
            }
        }


def save_stats(stats: Dict[str, Any]) -> bool:
    """Save statistics to file."""
    stats_path = get_stats_path()

    # Ensure directory exists
    stats_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        return True
    except IOError:
        return False


def categorize_tool(tool_name: str) -> str:
    """Determine the category of a tool.

    Supports both old format (mcp__server__tool) and new format (mcp:server:tool).
    """
    # New detailed format: category:subcategory:detail
    if tool_name.startswith("mcp:") or tool_name.startswith("mcp__"):
        return "mcp"
    elif tool_name.startswith("agent:") or tool_name == "Task":
        return "agent"
    elif tool_name.startswith("skill:") or tool_name == "Skill":
        return "skill"
    elif tool_name.startswith("cmd:") or tool_name == "SlashCommand":
        return "command"
    elif tool_name.startswith("native:"):
        return "native"
    else:
        return "native"


def parse_detailed_tool_name(tool_name: str) -> tuple:
    """Parse detailed tool name into (category, subcategory, detail).

    Examples:
        mcp:context7:get-library-docs -> (mcp, context7, get-library-docs)
        agent:code-reviewer -> (agent, code-reviewer, None)
        native:Read -> (native, Read, None)
    """
    parts = tool_name.split(":", 2)
    category = parts[0] if parts else "native"
    subcategory = parts[1] if len(parts) > 1 else tool_name
    detail = parts[2] if len(parts) > 2 else None
    return (category, subcategory, detail)


def record_tool_usage(tool_name: str) -> None:
    """Record a tool usage in statistics."""
    stats = load_stats()
    session_id = get_current_session_id()
    category = categorize_tool(tool_name)

    # Initialize session if needed
    if session_id not in stats["sessions"]:
        stats["sessions"][session_id] = {
            "start": datetime.now().isoformat(),
            "end": None,
            "tools": {},
            "categories": {
                "native": 0,
                "mcp": 0,
                "agent": 0,
                "skill": 0,
                "command": 0
            }
        }

    session = stats["sessions"][session_id]

    # Update session stats
    session["tools"][tool_name] = session["tools"].get(tool_name, 0) + 1
    session["categories"][category] = session["categories"].get(category, 0) + 1
    session["end"] = datetime.now().isoformat()

    # Update totals
    stats["totals"]["tools"][tool_name] = stats["totals"]["tools"].get(tool_name, 0) + 1
    stats["totals"]["categories"][category] = stats["totals"]["categories"].get(category, 0) + 1

    save_stats(stats)


def get_session_stats(session_id: Optional[str] = None) -> Dict[str, Any]:
    """Get statistics for a specific session or current session."""
    stats = load_stats()

    if session_id is None:
        session_id = get_current_session_id()

    return stats["sessions"].get(session_id, {
        "tools": {},
        "categories": {"native": 0, "mcp": 0, "agent": 0, "skill": 0, "command": 0}
    })


def get_total_stats() -> Dict[str, Any]:
    """Get total statistics across all sessions."""
    stats = load_stats()
    return stats["totals"]


def get_top_tools(n: int = 5, session_only: bool = True) -> list:
    """Get top N most used tools."""
    if session_only:
        data = get_session_stats()
        tools = data.get("tools", {})
    else:
        data = get_total_stats()
        tools = data.get("tools", {})

    sorted_tools = sorted(tools.items(), key=lambda x: x[1], reverse=True)
    return sorted_tools[:n]


def get_subcategory_breakdown(tools: dict) -> dict:
    """Group tools by category and subcategory.

    Returns:
        {
            "mcp": {"context7": 5, "playwright": 3},
            "agent": {"code-reviewer": 2, "Explore": 1},
            "native": {"Read": 10, "Write": 5}
        }
    """
    breakdown = {
        "native": {},
        "mcp": {},
        "agent": {},
        "skill": {},
        "command": {}
    }

    for tool_name, count in tools.items():
        category, subcategory, detail = parse_detailed_tool_name(tool_name)

        # Handle old format tools
        if tool_name.startswith("mcp__"):
            parts = tool_name.split("__")
            category = "mcp"
            subcategory = parts[1] if len(parts) > 1 else "unknown"
        elif not ":" in tool_name:
            # Old native tool format
            category = categorize_tool(tool_name)
            subcategory = tool_name

        if category in breakdown:
            breakdown[category][subcategory] = breakdown[category].get(subcategory, 0) + count

    return breakdown


def format_stats_output(session_only: bool = True) -> str:
    """Format statistics for display with subcategory breakdown."""
    if session_only:
        stats = get_session_stats()
        title = "SESSION STATISTICS"
    else:
        stats = get_total_stats()
        title = "ALL-TIME STATISTICS"

    categories = stats.get("categories", {})
    tools = stats.get("tools", {})
    total = sum(categories.values())

    if total == 0:
        return f"No tool usage recorded yet for {'this session' if session_only else 'all time'}."

    # Get subcategory breakdown
    breakdown = get_subcategory_breakdown(tools)

    # Build output
    lines = []
    lines.append(f"\033[1m\033[36m{'=' * 50}\033[0m")
    lines.append(f"\033[1m\033[36m  {title}\033[0m")
    lines.append(f"\033[1m\033[36m{'=' * 50}\033[0m")
    lines.append("")

    # Category config
    category_config = {
        "native": ("Native Tools", "\033[34m", "TOOL"),      # Blue
        "mcp": ("MCP Servers", "\033[36m", "MCP"),           # Cyan
        "agent": ("Agents", "\033[35m", "AGENT"),            # Magenta
        "skill": ("Skills", "\033[33m", "SKILL"),            # Yellow
        "command": ("Commands", "\033[32m", "CMD")           # Green
    }

    max_count = max(categories.values()) if categories.values() else 1
    bar_width = 15

    for cat, (label, color, prefix) in category_config.items():
        count = categories.get(cat, 0)
        if count == 0:
            continue

        bar_len = int((count / max_count) * bar_width) if max_count > 0 else 0
        bar = '\u2588' * bar_len
        percentage = (count / total * 100) if total > 0 else 0
        lines.append(f"  {color}{label:15}\033[0m {count:4} {color}{bar}\033[0m ({percentage:.1f}%)")

        # Show subcategory breakdown
        subcats = breakdown.get(cat, {})
        if subcats:
            # Sort by count descending
            sorted_subcats = sorted(subcats.items(), key=lambda x: x[1], reverse=True)
            for subcat, subcount in sorted_subcats[:5]:  # Top 5 per category
                lines.append(f"    \033[2m└─ {subcat[:20]:20} ({subcount})\033[0m")

        lines.append("")

    lines.append(f"\033[1m  Total: {total} tool calls\033[0m")
    lines.append(f"\033[1m\033[36m{'=' * 50}\033[0m")

    return '\n'.join(lines)


def clear_session_stats(session_id: Optional[str] = None) -> bool:
    """Clear statistics for a specific session."""
    stats = load_stats()

    if session_id is None:
        session_id = get_current_session_id()

    if session_id in stats["sessions"]:
        del stats["sessions"][session_id]
        return save_stats(stats)

    return False


if __name__ == "__main__":
    # Test stats
    print(format_stats_output(session_only=True))
