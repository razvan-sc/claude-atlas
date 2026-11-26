---
name: atlas-update
description: Compose and post a status update to an Atlas project
allowed-tools: mcp__atlas__get_project_updates, mcp__atlas__create_project_update, mcp__atlas__list_projects
---

# Atlas Status Update

Guide the user through composing and posting a status update to an Atlas project. This is an interactive workflow -- gather input step by step, confirm before posting.

## MCP Server

Use the `atlas` MCP server. All tool calls use the `mcp__atlas__` prefix.

## Workflow

### Step 1: Get the project

Check if a project key was provided as an argument (e.g., `/atlas-update SAFET-2318`). If not, ask the user which project to update.

If a project key (not ARI ID) was provided, call `mcp__atlas__list_projects` with `limit: 50` to resolve the ARI ID.

### Step 2: Show current status for context

Call `mcp__atlas__get_project_updates` with the project's ARI ID. If updates exist, show the most recent one briefly:

> **Current status:** [status value] -- "[summary extracted from ADF]" (posted [createdAt])

If no previous updates exist, note: "This will be the first status update for this project."

### Step 3: Gather update details

Ask the user for each field one at a time:

1. **Summary** (required): "What's the status update? Describe what's happening with the project."
2. **Status** (required, with default): "What's the project status? Options: on_track, at_risk, off_track, done (default: on_track)"
3. **Highlights** (optional): "Any wins or accomplishments to highlight? You can list multiple, or skip this."

### Step 4: Preview and confirm

Show a preview of the update before posting:

> ### Preview
>
> **Project:** [project key]
> **Summary:** [summary text]
> **Status:** [status value]
> **Highlights:** [list of highlights, or "None"]
>
> Post this update? (yes/no)

### Step 5: Post or abort

**If the user confirms:**

Call `mcp__atlas__create_project_update` with:
- `project_id`: the ARI ID
- `summary`: the user's summary text
- `status`: the chosen status (e.g., "on_track")
- `highlights`: JSON string array of highlight summaries (e.g., `'["Shipped feature X", "Completed migration"]'`), or `"[]"` if no highlights

On success, show: "Status update posted successfully."

**If the user declines:**

Respond: "Update cancelled. No changes were made."

### Error Handling

If any MCP tool call fails, display the error message clearly and suggest:
- Verify the project key is correct
- Check that the Atlas MCP server is configured in `.mcp.json`
- Verify `~/.atlas/config.json` exists with valid credentials

## ADF Parsing

Update summaries are in Atlassian Document Format (ADF) JSON. Extract plain text by recursively walking the JSON and collecting all `text` field values.
