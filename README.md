# MCP Tool Docs Server

Dockerized FastMCP server that exposes documentation about off-the-shelf tools so coding agents can check practical, production-ready options before inventing custom implementations.

## What this includes

- `base.Dockerfile`: small Debian/Python base image with `uv` and a dedicated virtualenv.
- `app.Dockerfile`: application image that installs dependencies from `pyproject.toml`.
- `docker-compose.yml`: runtime service with port `8005` and a bind mount of your local code.
- `localbuild.sh`: builds base + app images with deterministic unique names.
- `localrun.sh up|down`: starts and stops the local MCP service.
- `src/mcp_doc_server/server.py`: FastMCP server with documentation tools.
- `src/mcp_doc_server/data/tool_docs.json`: off-the-shelf tool catalog.
- `docs/mcp_strategy.md`: long-term strategy for wiring coding-agent hooks.

## Quick start

```bash
./localbuild.sh
./localrun.sh up
```

Stop it with:

```bash
./localrun.sh down
```

<<<<<<< HEAD
By default, the MCP server listens at `http://localhost:8005`, with MCP transport endpoint at `http://localhost:8005/mcp`.
=======
By default, the server listens at `http://localhost:8005` with:

- MCP transport endpoint: `http://localhost:8005/mcp/` (note trailing slash)
- Swagger UI: `http://localhost:8005/docs`
- JSON catalog API: `http://localhost:8005/api/tools`
>>>>>>> main

## Scripts

### Build

```bash
./localbuild.sh
./localbuild.sh --no-cache
```

### Run

```bash
./localrun.sh up
./localrun.sh down
```

Optional port override:

```bash
HOST_PORT=8010 ./localrun.sh up
```

## Toolset exposed by MCP

The server includes tools to:

- list documented off-the-shelf tools
- fetch full documentation for a tool
- recommend tools for a specific problem statement
- return the strategy notes for "tool-first" coding-agent behavior

This is intended as a practical foundation for future hooks in Claude Code or OpenCode so the model checks this MCP source first.
<<<<<<< HEAD
=======

## HTTP endpoints

- `GET /healthz`: liveness check
- `GET /api/tools?category=...`: list documented tools
- `GET /api/tools/{tool_name}`: fetch full entry for one tool
- `GET /api/strategy`: read the long-term MCP strategy document
- `POST /mcp/` and MCP streamable-http routes: MCP transport surface
>>>>>>> main
