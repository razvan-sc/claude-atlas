---
name: atlas-projects
description: List and browse your Atlassian Atlas projects
allowed-tools: mcp__atlas__list_projects, mcp__atlas__get_projects, mcp__atlas__atlas_graphql_query
---

# Atlas Projects

List the user's Atlas projects in a formatted table.

## MCP Server

Use the `atlas` MCP server. All tool calls use the `mcp__atlas__` prefix.

## Workflow

1. Check if the user provided project IDs as arguments to the command.

2. **If no project IDs provided**, call the `mcp__atlas__list_projects` tool with `limit: 20`.

3. **If specific project IDs provided**, call the `mcp__atlas__get_projects` tool with the list of IDs.

4. Parse the returned JSON and **format the results as a table:**

   | Key | Name | Status | Target Date |
   |-----|------|--------|-------------|
   | PROJ-1 | Example Project | ON_TRACK | 2025-06-30 |

   - If status is missing, show "-"
   - If target date is missing, show "-"

5. **Show a count summary** at the end: "Showing N projects"

6. **On error**, display the error message clearly and suggest:
   - Check that the Atlas MCP server is configured in `.mcp.json`
   - Verify `~/.atlas/config.json` exists with valid credentials
