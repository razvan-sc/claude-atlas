---
name: Atlas Status
description: View the latest status, risks, and highlights for an Atlas project
trigger: /atlas:status
---

# Atlas Project Status

Show the latest status update, risks, and highlights for a specific Atlas project.

## Workflow

1. Check if a project ID or key was provided as an argument (e.g., the user typed `/atlas:status PROJ-123`). If not, ask the user: "Which project would you like to check? Please provide the project ID."

2. Call the `get_project_updates` MCP tool with the project ID.

3. Parse the returned JSON which contains `projectId`, `updates` (array), `risks` (array), and `highlights` (array).

4. **If no updates exist**, respond: "No status updates found for this project."

5. **If updates exist**, display the **most recent update** (first in the array) formatted as:

   ### Latest Status Update

   - **Summary:** [summary text]
   - **Status:** [emoji] [status value]
     - Use these emoji indicators: ON_TRACK = green circle, AT_RISK = yellow circle, OFF_TRACK = red circle, DONE = checkmark
   - **Target Date:** [target date or "-" if missing]
   - **Updated:** [createdAt date]

   If there are more updates beyond the first, add: "_N more status updates available._"

6. **Risks** (if any exist):

   ### Risks

   - [risk summary 1]
   - [risk summary 2]

   If no risks, omit this section.

7. **Highlights** (if any exist):

   ### Highlights

   - [highlight summary 1]
   - [highlight summary 2]

   If no highlights, omit this section.

8. **On error**, display the error message and suggest checking the project ID and Atlas configuration.
