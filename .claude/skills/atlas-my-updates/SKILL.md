---
name: atlas-my-updates
description: List status updates for all Atlas projects you own or contribute to
allowed-tools: mcp__atlas__list_projects, mcp__atlas__get_project_updates, mcp__atlas__atlas_graphql_query
---

# Atlas My Updates

Show the latest status updates for all projects where the authenticated user is an owner or contributor.

## MCP Server

Use the `atlas` MCP server. All tool calls use the `mcp__atlas__` prefix.

## Workflow

1. Call `mcp__atlas__list_projects` with `limit: 50` to get all active projects.

2. Work out the current user's display name: call `mcp__atlas__atlas_graphql_query` with `query { me { user { name } } }` and read `data.me.user.name`. If that fails or returns nothing, ask the user for their name as it appears in Atlas.

3. Parse the returned project JSON array. Filter for projects where:
   - The `owner` field matches the user's name
   - OR the `members` array contains the user's name

4. For each matching project, call `mcp__atlas__get_project_updates` with the project's `id` (ARI format).

5. **Format the output** grouped by project, showing the latest 3 updates per project:

   ### [Project Name] `[key]` `[status]`

   **Role:** Owner | Contributor (Owner: [name]) | **Due:** [dueDate]

   - **[date]** [status]: [summary text]
   - **[date]** [status]: [summary text]
   - **[date]** [status]: [summary text]

6. If a project has highlights, append them:

   **Highlights:**
   - [highlight summary 1]
   - [highlight summary 2]

7. **Show a summary** at the end:
   - Total projects: N (M owned, K contributing)
   - Projects needing attention (at_risk or off_track or due within 2 weeks)

8. **On error**, display the error message and suggest checking the Atlas MCP server configuration.

## ADF Parsing

Update summaries are in Atlassian Document Format (ADF) JSON. Extract plain text by recursively walking the JSON and collecting all `text` field values. Join them with spaces. Ignore media, emoji, and other non-text nodes.
