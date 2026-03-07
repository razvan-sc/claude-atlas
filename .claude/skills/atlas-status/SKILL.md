---
name: atlas-status
description: View the latest status, risks, and highlights for an Atlas project
allowed-tools: mcp__atlas__get_project_updates, mcp__atlas__list_projects
---

# Atlas Project Status

Show the latest status update, risks, and highlights for a specific Atlas project.

## MCP Server

Use the `atlas` MCP server. All tool calls use the `mcp__atlas__` prefix.

## Workflow

1. Check if a project key was provided as an argument (e.g., `/atlas-status SAFET-2318`).
   - If a project key (not ARI ID) was provided, first call `mcp__atlas__list_projects` with `limit: 50` to find the matching project's ARI ID.
   - If not provided, ask the user: "Which project would you like to check? Please provide the project key (e.g. SAFET-1234)."

2. Call `mcp__atlas__get_project_updates` with the project's ARI ID.

3. Parse the returned JSON which contains `projectId`, `updates` (array), and `highlights` (array).

4. **If no updates exist**, respond: "No status updates found for this project."

5. **If updates exist**, display the **most recent update** (first in the array) formatted as:

   ### Latest Status Update

   - **Summary:** [extract text from ADF JSON by walking all `text` nodes]
   - **Status:** [status value]
     - Use these indicators: on_track = ON_TRACK, at_risk = AT_RISK, off_track = OFF_TRACK, done = DONE
   - **Updated:** [createdAt date]

   If there are more updates beyond the first, add: "_N more status updates available._"

6. **Highlights** (if any exist):

   ### Highlights

   - [highlight summary 1]
   - [highlight summary 2]

   If no highlights, omit this section.

7. **On error**, display the error message and suggest checking the project ID and Atlas MCP configuration.

## ADF Parsing

Update summaries are in Atlassian Document Format (ADF) JSON. Extract plain text by recursively walking the JSON and collecting all `text` field values. Join them with spaces.
