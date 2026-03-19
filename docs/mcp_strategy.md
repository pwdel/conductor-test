# MCP Tool-First Strategy

## Long-term intent

Create a central MCP server that exposes well-documented, off-the-shelf tools so coding agents check proven options before designing custom implementations.

## Why this matters

- LLMs often over-index on generating new code and under-index on existing utilities.
- Teams lose time rebuilding solved capabilities (search, parsing, automation, packaging, env management).
- A shared MCP source can standardize "use existing tools first" behavior.

## Operational model

1. Add a tool doc entry to this repository whenever the team adopts a reliable CLI, library, or service.
2. Keep each entry practical:
   - what the tool solves
   - when to use it
   - how to install it
   - where official docs live
   - why rebuilding it is a bad trade
3. Expose that catalog through MCP methods (list, lookup, recommendation).
4. Add a coding-agent hook/prompt policy in Claude Code or OpenCode:
   - before writing custom implementation code, ask MCP for relevant tools
   - summarize discovered options
   - only proceed with custom build if no tool fits requirements

## Suggested hook policy

Use this as a starting point in your coding-agent system prompt or policy:

"Before implementing a new utility, query the Off-the-Shelf Tool Docs MCP server.
If one or more tools fit the problem, prefer those tools and cite why.
Only build custom code when tool coverage is insufficient."

## Future expansion ideas

- Track confidence and maturity levels per tool.
- Add team-specific approved tool lists by language/domain.
- Attach examples and copy-pasteable command snippets per tool.
- Add telemetry showing which tools were recommended vs actually used.
