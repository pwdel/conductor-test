# Conductor Test: MCP Tool Docs Server

This repository is a test project used to validate a Conductor workflow end-to-end:

- spin up an isolated workspace
- iterate with an AI coding agent
- run and fix local infrastructure (`docker`, `compose`, startup scripts)
- expose an MCP server that can be consumed by coding assistants

## What We Built

We built a Dockerized MCP documentation server for coding agents. It exposes:

- an MCP endpoint (`/mcp/`) for tool calls
- a small HTTP API for querying tool documentation
- a strategy document describing tool-first agent behavior

Core files:

- `base.Dockerfile`: Python + `uv` base image
- `app.Dockerfile`: app image for the MCP server
- `docker-compose.yml`: local runtime configuration
- `localbuild.sh`: deterministic local image build helper
- `localrun.sh`: local up/down runner
- `src/mcp_doc_server/http_app.py`: HTTP app entrypoint
- `src/mcp_doc_server/server.py`: MCP server implementation
- `src/mcp_doc_server/data/tool_docs.json`: tool catalog data
- `docs/mcp_strategy.md`: strategy notes for coding-agent workflows

## Quick Start

```bash
./localbuild.sh
./localrun.sh up
```

Stop:

```bash
./localrun.sh down
```

Default local URLs:

- MCP endpoint: `http://localhost:8005/mcp/`
- Swagger UI: `http://localhost:8005/docs`

## Why This Repo Exists

This is explicitly a Conductor test repository. The goal is not only to build the MCP service, but also to validate how Conductor handles:

- isolated agent workspaces
- safe parallel task execution
- branch-per-task development
- merge and handoff workflow back to GitHub PRs

## How Conductor Leverages Git Worktrees

Conductor uses Git worktrees as the core mechanism for multi-agent local development:

- Isolation: each workspace/agent session gets its own Git worktree and branch in a separate local directory, without doing a full extra clone.
- Parallelism: multiple agents can work at the same time on different tasks without file-level conflicts in one working directory.
- Shared history: worktrees share one underlying `.git` repository, so commit history, refs, and remotes stay consistent.
- Streamlined workflow: agents and developers can switch contexts quickly without heavy `stash` workflows.
- Environment management: workspace-specific setup scripts can configure env vars and dependencies per worktree.

In practice, this lets you run concurrent coding sessions while keeping changes isolated and reviewable.

## Notes About Conductor

As described in the public Conductor announcement, Conductor is a Mac app for running multiple coding-agent sessions in parallel, built with Tauri (Rust backend + native renderer), and uses Git worktrees under the hood for one-click isolated workspaces.

## Open Source Reference

An open-source version of Conductor is available here:

- https://github.com/pwdel/crystal/tree/v0.3.4
