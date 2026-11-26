# claude-atlas

An MCP (Model Context Protocol) server that gives Claude Code access to [Atlassian Atlas](https://www.atlassian.com/software/atlas) -- Atlassian's project tracking and teamwork directory.

## What it does

claude-atlas exposes Atlas project data as MCP tools, allowing Claude to read and update your Atlas projects through natural conversation. It communicates with the Atlas GraphQL API using Basic Auth.

### MCP Tools

| Tool | Description |
|------|-------------|
| `list_projects` | List all non-archived projects, sorted by most recently updated |
| `create_project` | Create a project with a name, description, and optional goal link, tag, and Jira issue link |
| `get_project` | Get details of a single project by ID (name, description, state, due date, owner, members) |
| `get_projects` | Get details of multiple projects by their IDs |
| `get_project_updates` | Get status updates and highlights for a project |
| `create_project_update` | Post a new status update with summary, status, and highlights |
| `archive_project` | Archive or unarchive a project |
| `atlas_graphql_query` | Execute a raw GraphQL query against the Atlas API |

### Claude Code Skills

The server also ships with Claude Code slash command skills. They live in
`skills/` (symlinked from `.claude/skills/`), so anyone who clones this repo
gets them automatically. Each skill calls the `atlas` MCP tools, so the server must be
configured (see Setup below) for them to work.

- `/atlas-projects` -- List and browse your Atlas projects in a formatted table
- `/atlas-create` -- Create one or more projects, optionally linked to a goal, tagged, and linked to Jira issues
- `/atlas-status` -- View the latest status updates for a project
- `/atlas-update` -- Compose and post a new status update to a project
- `/atlas-my-updates` -- List status updates for projects you own or contribute to
- `/atlas-tag` -- List projects filtered by a tag
- `/atlas-setup` -- First-run setup: checks `uv`, creates `~/.atlas/config.json`, verifies the connection

## Install

Every option needs [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
on your machine, since the server runs through `uv run`. You also need your own
[Atlassian API token](https://id.atlassian.com/manage-profile/security/api-tokens).
Credentials are personal and are not bundled with the plugin.

### Claude Code (CLI, IDE, or the desktop app's Code tab)

This repo is a plugin marketplace. You get the MCP server and all the skills in
one step:

```bash
/plugin marketplace add razvan-sc/claude-atlas
/plugin install atlas@safetyculture-atlas
```

Then run `/atlas:setup`. It checks `uv`, creates `~/.atlas/config.json`, and
verifies the connection. Skills are namespaced as `/atlas:create`,
`/atlas:projects`, `/atlas:status`, and so on. To pick up new versions:

```bash
/plugin marketplace update safetyculture-atlas
```

### Claude Desktop: Cowork (plugin with skills)

1. In Claude Desktop, open **Customize → Plugins → Add marketplace** and enter
   `razvan-sc/claude-atlas`.
2. Install **atlas** from the `safetyculture-atlas` marketplace.
3. Create `~/.atlas/config.json` (see [Config file](#config-file)), or ask Claude
   to run the `atlas-setup` skill.

### Claude Desktop: Chat (one-click extension)

The chat app loads MCP servers as Desktop Extensions (`.mcpb`). The extension
asks for your email, API token, and site in a settings form. The token is
stored in the OS keychain, so no config file is needed.

1. Download `atlas.mcpb` from the
   [latest release](https://github.com/razvan-sc/claude-atlas/releases), or
   build it yourself (see [Building the Desktop extension](#building-the-desktop-extension)).
2. Double-click it, or drag it onto **Settings → Extensions** in Claude Desktop.
3. Fill in the form and enable the extension.

The extension adds only the MCP tools. The chat app does not load plugin
skills. If you want the slash-command workflows in chat too, zip a folder from
`skills/` and upload it under **Settings → Capabilities → Skills**.

## Config file

Claude Code and Cowork read `~/.atlas/config.json`:

```bash
mkdir -p ~/.atlas
cat > ~/.atlas/config.json << 'EOF'
{
  "email": "you@company.com",
  "api_token": "your-atlassian-api-token",
  "subdomain": "yoursite"
}
EOF
chmod 600 ~/.atlas/config.json
```

- `email`: your Atlassian account email
- `api_token`: an [Atlassian API token](https://id.atlassian.com/manage-profile/security/api-tokens)
- `subdomain`: your Atlassian site name (the `yoursite` part of `yoursite.atlassian.net`)
- `cloud_id` (optional): your Atlassian cloud ID. If you leave it out, it is resolved automatically.

You can also set `ATLAS_EMAIL`, `ATLAS_API_TOKEN`, `ATLAS_SUBDOMAIN`, and
optionally `ATLAS_CLOUD_ID` as environment variables. When all three required
variables are set, they take precedence over the file. The Desktop extension
uses this mechanism.

## Manual MCP setup (without the plugin)

For a local clone, point any MCP client at the launcher script. The script
finds `uv` even when a GUI app starts it with a minimal `PATH`:

```json
{
  "mcpServers": {
    "atlas": {
      "command": "/path/to/claude-atlas/bin/atlas-mcp"
    }
  }
}
```

In this repo, `.mcp.json` already does this, so opening the clone in Claude
Code picks up the server and the skills in `.claude/skills` (a symlink to
`skills/`).

## Building the Desktop extension

```bash
npm install -g @anthropic-ai/mcpb
mcpb validate manifest.json
mcpb pack . dist/atlas.mcpb
```

`.mcpbignore` keeps tests, planning docs, and plugin files out of the bundle.
Attach `dist/atlas.mcpb` to a GitHub release so others can download it.

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
