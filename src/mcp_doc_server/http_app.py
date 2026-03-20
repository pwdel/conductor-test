from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from mcp_doc_server.server import (
    _load_catalog,
    _normalize_tool_name,
    get_agent_strategy_notes,
    mcp,
)

app = FastAPI(
    title="MCP Tool Docs Server",
    version="0.1.0",
    description=(
        "HTTP wrapper around FastMCP tool documentation. "
        "Use `/mcp` for MCP transport and `/docs` for Swagger UI."
    ),
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/tools")
def list_tools(category: str | None = Query(default=None)) -> list[dict[str, str]]:
    tools = _load_catalog()
    wanted = category.lower().strip() if category else None
    rows: list[dict[str, str]] = []
    for tool in tools:
        tool_category = str(tool.get("category", "")).strip().lower()
        if wanted and tool_category != wanted:
            continue
        rows.append(
            {
                "name": str(tool.get("name", "")),
                "category": str(tool.get("category", "")),
                "summary": str(tool.get("summary", "")),
                "docs_url": str(tool.get("docs_url", "")),
            }
        )
    return rows


@app.get("/api/tools/{tool_name}")
def get_tool(tool_name: str) -> dict:
    wanted = _normalize_tool_name(tool_name)
    for tool in _load_catalog():
        current = _normalize_tool_name(str(tool.get("name", "")))
        if current == wanted:
            return tool
    raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")


@app.get("/api/strategy")
def strategy() -> dict[str, str]:
    return {"strategy": get_agent_strategy_notes()}


# Mount MCP transport at /mcp and keep HTTP docs at /docs.
app.mount("/mcp", mcp.http_app(path="/", transport="streamable-http"))
