---
name: atlas-tag
description: List Atlas projects filtered by a tag
allowed-tools: mcp__atlas__list_projects
---

# Atlas Projects by Tag

List Atlas projects that have a specific tag.

## MCP Server

Use the `atlas` MCP server. All tool calls use the `mcp__atlas__` prefix.

## Workflow

1. Check if a tag was provided as an argument (e.g., `/atlas-tag platform`).
   - If not provided, ask the user: "Which tag would you like to filter by?"

2. Call `mcp__atlas__list_projects` with `limit: 50` and `tag: <tag>`.

3. Parse the returned JSON and **format the results as a table:**

   | Key | Name | Status | Target Date | Tags |
   |-----|------|--------|-------------|------|
   | PROJ-1 | Example Project | ON_TRACK | 2025-06-30 | platform |

   - If status is missing, show "-"
   - If target date is missing, show "-"
   - Tags are comma-separated

4. **Show a count summary** at the end: `Showing N projects tagged "<tag>"`

5. **If no projects found**, respond: `No projects found with tag "<tag>".`

6. **On error**, display the error message clearly and suggest:
   - Check that the Atlas MCP server is configured in `.mcp.json`
   - Verify `~/.atlas/config.json` exists with valid credentials
