# Claude Atlas

## What This Is

A Claude Code integration for Atlassian Atlas Projects, providing an MCP server (6 tools) and 3 slash command skills. Users manage Atlas projects, read and write status updates, and filter projects — all from within Claude Code conversations.

## Core Value

Users can interact with their Atlas Projects directly from Claude Code without switching to the Atlassian UI — reading updates, posting status, and managing projects through natural language.

## Requirements

### Validated

- ✓ MCP server exposing Atlas Projects GraphQL API as tools — v1.0
- ✓ Slash command skills for common Atlas workflows — v1.0
- ✓ List and filter projects (by status, name, etc.) — v1.0
- ✓ Read project details and status updates (risks, highlights) — v1.0
- ✓ Write/post project status updates with summary, status, highlights — v1.0
- ✓ Edit existing projects (archive/unarchive) — v1.0
- ✓ Config file authentication (~/.atlas/config.json with email + API token) — v1.0
- ✓ Single Atlassian instance configuration — v1.0

### Active

- [ ] Create new projects with name and target date
- [ ] Search/list all projects without knowing IDs
- [ ] First-run setup flow for credentials
- [ ] Edit existing status updates

### Out of Scope

- Multiple Atlassian instance support — single instance sufficient
- OAuth authentication — API token approach is simpler and sufficient
- Atlas Goals API integration — focus on Projects API only
- Real-time notifications/webhooks — polling/on-demand only
- Web UI — CLI-only integration

## Context

- Shipped v1.0 with 541 LOC Python, 592 LOC tests, 156 LOC skills
- Tech stack: Python MCP server (FastMCP + httpx), Claude Code skill files
- 6 MCP tools registered, 3 slash commands, 27 unit tests
- Known tech debt: skill error messages reference wrong env var names

## Constraints

- **API**: Must use Atlas Projects GraphQL API (no REST alternative)
- **Auth**: Basic Auth with API tokens (Atlassian's supported method)
- **Platform**: Python MCP server + Claude Code skill files
- **Privacy**: Credentials stored locally in ~/.atlas/config.json, never committed

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| MCP server + slash commands | MCP gives tool access in any conversation; skills give optimized workflows | ✓ Good |
| Python for MCP server | User preference, good mcp SDK support | ✓ Good |
| Config file for auth | Persist credentials between sessions, don't leak into env | ✓ Good |
| Single instance | Simpler config, user only needs one org | ✓ Good |
| GraphQL over REST | Only API available for Atlas Projects | ✓ Good |
| httpx MockTransport for testing | Isolates GraphQL client tests without mocking internals | ✓ Good |
| Tools return error strings not exceptions | MCP tools catch all exceptions and return readable error messages | ✓ Good |

---
*Last updated: 2026-03-07 after v1.0 milestone*
