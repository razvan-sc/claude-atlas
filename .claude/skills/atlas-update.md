---
name: Atlas Update
description: Compose and post a status update to an Atlas project
trigger: /atlas:update
---

# Atlas Status Update

Guide the user through composing and posting a status update to an Atlas project. This is an interactive workflow -- gather input step by step, confirm before posting.

## Workflow

### Step 1: Get the project ID

Check if a project ID was provided as an argument. If not, ask: "Which project would you like to update? Please provide the project ID."

### Step 2: Show current status for context

Call the `get_project_updates` MCP tool with the project ID. If updates exist, show the most recent one briefly:

> **Current status:** [status emoji] [status value] -- "[summary]" (posted [createdAt])

If no previous updates exist, note: "This will be the first status update for this project."

### Step 3: Gather update details

Ask the user for each field one at a time:

1. **Summary** (required): "What's the status update? Describe what's happening with the project."
2. **Status** (required, with default): "What's the project status? Options: ON_TRACK, AT_RISK, OFF_TRACK, DONE (default: ON_TRACK)"
3. **Highlights** (optional): "Any wins or accomplishments to highlight? You can list multiple, or skip this."

### Step 4: Preview and confirm

Show a preview of the update before posting:

> ### Preview
>
> **Project:** [project ID]
> **Summary:** [summary text]
> **Status:** [emoji] [status value]
> **Highlights:** [list of highlights, or "None"]
>
> Post this update? (yes/no)

### Step 5: Post or abort

**If the user confirms:**

Call the `create_project_update` MCP tool with:
- `project_id`: the project ID
- `summary`: the user's summary text
- `status`: the chosen status (e.g., "ON_TRACK")
- `highlights`: JSON string array of highlight summaries (e.g., `'["Shipped feature X", "Completed migration"]'`), or `"[]"` if no highlights

On success, show: "Status update posted successfully at [createdAt timestamp]."

**If the user declines:**

Respond: "Update cancelled. No changes were made."

### Error Handling

If any MCP tool call fails, display the error message clearly and suggest:
- Verify the project ID is correct
- Check that the Atlas MCP server is configured in `.mcp.json`
- Ensure `ATLAS_API_TOKEN` and `ATLAS_ORG_ID` environment variables are set
