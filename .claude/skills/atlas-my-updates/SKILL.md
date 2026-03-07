---
name: atlas-my-updates
description: List status updates for all Atlas projects you own or contribute to
---

# Atlas My Updates

Show the latest status updates for all projects where the authenticated user is an owner or contributor.

## Workflow

1. Call the `list_projects` MCP tool with a limit of 50 to get all active projects.

2. Parse the returned JSON array. For each project, check:
   - The `owner` field matches the authenticated user's name
   - The `members` array contains the authenticated user's name
   - Use the user's name from the Atlas config (typically derivable from the email). The current user is **Razvan Balazs**.

3. For each matching project, call the `get_project_updates` MCP tool with the project's `id`.

4. **Format the output** grouped by project, showing the latest 3 updates per project:

   ### [Project Name] `[status]`

   **Role:** Owner | Contributor

   - **[date]** [status]: [summary text]
   - **[date]** [status]: [summary text]
   - **[date]** [status]: [summary text]

   Use these status indicators:
   - on_track = green circle
   - at_risk = yellow circle
   - off_track = red circle
   - done = checkmark
   - paused = pause icon
   - pending = white circle

   Parse update summaries from Atlassian Document Format (ADF) JSON into plain text by extracting all `text` fields from the document content tree.

5. If a project has highlights, append them:

   **Highlights:**
   - [highlight summary 1]
   - [highlight summary 2]

6. **Show a summary** at the end:
   - Total projects: N (M owned, K contributing)
   - Projects needing attention (at_risk or off_track)

7. **On error**, display the error message and suggest checking the Atlas MCP server configuration.

8. **If the MCP tools are not available**, fall back to running the query directly via Python:
   ```
   export PATH="$HOME/.local/bin:$PATH"
   uv run python -c "..." (from the claude-atlas project directory)
   ```
   Use the `atlas.config`, `atlas.graphql_client`, and `atlas.queries` modules to execute the queries programmatically.
