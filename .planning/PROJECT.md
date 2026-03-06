# Claude Atlas

## What This Is

A Claude Code integration for Atlassian Atlas Projects, providing both an MCP server and slash command skills. It lets users manage Atlas projects, read and write status updates, and filter projects — all from within Claude Code conversations.

## Core Value

Users can interact with their Atlas Projects directly from Claude Code without switching to the Atlassian UI — reading updates, posting status, and managing projects through natural language.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] MCP server exposing Atlas Projects GraphQL API as tools
- [ ] Slash command skills for common Atlas workflows
- [ ] List and filter projects (by status, name, etc.)
- [ ] Read project details and status updates (risks, highlights)
- [ ] Write/post project status updates with summary, risks, highlights
- [ ] Create new projects with initial settings
- [ ] Edit existing projects (archive/unarchive, update properties)
- [ ] Config file authentication (~/.atlas/config.json with email + API token)
- [ ] Single Atlassian instance configuration
- [ ] First-run setup flow for credentials

### Out of Scope

- Multiple Atlassian instance support — single instance sufficient for v1
- OAuth authentication — API token approach is simpler and sufficient
- Atlas Goals API integration — focus on Projects API only
- Real-time notifications/webhooks — polling/on-demand only
- Web UI — CLI-only integration

## Context

- Atlassian Atlas Projects uses a GraphQL API at `https://{subdomain}.atlassian.net/gateway/api/graphql`
- Authentication is Basic Auth with email:api_token, BASE64 encoded
- API reference: https://developer.atlassian.com/platform/projects/projects-graphql-api/using-projects-graphql-api/
- Key GraphQL operations: `projects_byId`, `projects_byIds`, `projects_create`, `projects_createUpdate`, `projects_edit`
- MCP server built in Python using the `mcp` SDK
- Slash commands built as Claude Code skills (markdown workflow files)

## Constraints

- **API**: Must use Atlas Projects GraphQL API (no REST alternative)
- **Auth**: Basic Auth with API tokens (Atlassian's supported method)
- **Platform**: Python MCP server + Claude Code skill files
- **Privacy**: Credentials stored locally in ~/.atlas/config.json, never committed

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| MCP server + slash commands | MCP gives tool access in any conversation; skills give optimized workflows | — Pending |
| Python for MCP server | User preference, good mcp SDK support | — Pending |
| Config file for auth | Persist credentials between sessions, don't leak into env | — Pending |
| Single instance | Simpler config, user only needs one org | — Pending |
| GraphQL over REST | Only API available for Atlas Projects | — Pending |

---
*Last updated: 2026-03-07 after initialization*
