# claude-atlas

An MCP (Model Context Protocol) server that gives Claude Code access to [Atlassian Atlas](https://www.atlassian.com/software/atlas) -- Atlassian's project tracking and teamwork directory.

## What it does

claude-atlas exposes Atlas project data as MCP tools, allowing Claude Code to read and update your Atlas projects through natural conversation. It communicates with the Atlas GraphQL API using Basic Auth.

### MCP Tools

| Tool | Description |
|------|-------------|
| `list_projects` | List all non-archived projects, sorted by most recently updated |
| `get_project` | Get details of a single project by ID (name, description, state, due date, owner, members) |
| `get_projects` | Get details of multiple projects by their IDs |
| `get_project_updates` | Get status updates and highlights for a project |
| `create_project_update` | Post a new status update with summary, status, and highlights |
| `archive_project` | Archive or unarchive a project |
| `atlas_graphql_query` | Execute a raw GraphQL query against the Atlas API |

### Claude Code Skills

The server also ships with Claude Code slash command skills:

- `/atlas:projects` -- List and browse your Atlas projects in a formatted table
- `/atlas:status` -- View the latest status updates for a project
- `/atlas:update` -- Post a new status update to a project

## Setup

### 1. Create a config file

```bash
mkdir -p ~/.atlas
cat > ~/.atlas/config.json << 'EOF'
{
  "email": "you@company.com",
  "api_token": "your-atlassian-api-token",
  "subdomain": "yoursite"
}
EOF
```

- `email` -- Your Atlassian account email
- `api_token` -- An [Atlassian API token](https://id.atlassian.com/manage-profile/security/api-tokens)
- `subdomain` -- Your Atlassian site name (the `yoursite` part of `yoursite.atlassian.net`)
- `cloud_id` (optional) -- Your Atlassian cloud ID. If omitted, it will be resolved automatically.

### 2. Install

```bash
pip install -e .
```

### 3. Add to Claude Code

Add the server to your `.mcp.json`:

```json
{
  "mcpServers": {
    "atlas": {
      "command": "atlas"
    }
  }
}
```

## Development

Requires Python 3.10+.

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Project structure

```
src/atlas/
  config.py          # Config loader (~/.atlas/config.json)
  graphql_client.py  # Async GraphQL client with Basic Auth
  queries.py         # GraphQL query and mutation strings
  server.py          # MCP tool definitions and server entrypoint
```
