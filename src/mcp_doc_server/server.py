from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

CATALOG_PATH = Path(__file__).resolve().parent / "data" / "tool_docs.json"
STRATEGY_PATH = Path(__file__).resolve().parents[2] / "docs" / "mcp_strategy.md"

mcp = FastMCP("Off-the-Shelf Tool Docs")


def _load_catalog() -> list[dict[str, Any]]:
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    tools = payload.get("tools", [])
    if not isinstance(tools, list):
        return []
    return [t for t in tools if isinstance(t, dict)]


def _normalize_tool_name(name: str) -> str:
    return name.strip().lower().replace("_", "-")


def _keyword_set(raw: str) -> set[str]:
    cleaned = "".join(ch if ch.isalnum() else " " for ch in raw.lower())
    return {token for token in cleaned.split() if len(token) > 2}


def _score_tool(problem: str, tool: dict[str, Any]) -> int:
    text_fields: list[str] = []
    text_fields.append(str(tool.get("summary", "")))
    for item in tool.get("use_cases", []):
        text_fields.append(str(item))
    haystack = _keyword_set(" ".join(text_fields))
    needles = _keyword_set(problem)
    return len(haystack.intersection(needles))


@mcp.tool()
def list_documented_tools(category: str | None = None) -> list[dict[str, str]]:
    """List known off-the-shelf tools and short summaries."""
    tools = _load_catalog()
    results: list[dict[str, str]] = []
    wanted = category.lower().strip() if category else None

    for tool in tools:
        tool_category = str(tool.get("category", "")).strip().lower()
        if wanted and tool_category != wanted:
            continue
        results.append(
            {
                "name": str(tool.get("name", "")),
                "category": str(tool.get("category", "")),
                "summary": str(tool.get("summary", "")),
            }
        )
    return results


@mcp.tool()
def get_tool_documentation(tool_name: str) -> dict[str, Any]:
    """Fetch full documentation for one tool by name."""
    wanted = _normalize_tool_name(tool_name)
    for tool in _load_catalog():
        current = _normalize_tool_name(str(tool.get("name", "")))
        if current == wanted:
            return tool
    return {
        "error": f"Tool '{tool_name}' not found.",
        "hint": "Use list_documented_tools to inspect available names.",
    }


@mcp.tool()
def recommend_tools(problem_statement: str, limit: int = 5) -> list[dict[str, str]]:
    """Recommend tools from this catalog for a specific problem statement."""
    if limit < 1:
        limit = 1
    if limit > 15:
        limit = 15

    scored: list[tuple[int, dict[str, Any]]] = []
    for tool in _load_catalog():
        score = _score_tool(problem_statement, tool)
        scored.append((score, tool))

    scored.sort(key=lambda item: item[0], reverse=True)

    recommendations: list[dict[str, str]] = []
    for score, tool in scored:
        if score <= 0:
            continue
        recommendations.append(
            {
                "name": str(tool.get("name", "")),
                "category": str(tool.get("category", "")),
                "summary": str(tool.get("summary", "")),
                "docs_url": str(tool.get("docs_url", "")),
            }
        )
        if len(recommendations) >= limit:
            break
    return recommendations


@mcp.tool()
def get_agent_strategy_notes() -> str:
    """Return the long-term MCP strategy for tool-first coding workflows."""
    if not STRATEGY_PATH.exists():
        return "Strategy document is missing."
    return STRATEGY_PATH.read_text(encoding="utf-8")


def main() -> None:
    transport = os.getenv("MCP_TRANSPORT", "streamable-http")
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8005"))
    try:
        mcp.run(transport=transport, host=host, port=port)
    except TypeError:
        mcp.run()


if __name__ == "__main__":
    main()
