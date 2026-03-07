---
name: Atlas Projects
description: List and browse your Atlassian Atlas projects
trigger: /atlas:projects
---

# Atlas Projects

List the user's Atlas projects in a formatted table.

## Workflow

1. Check if the user provided project IDs as arguments to the command.

2. **If no project IDs provided**, discover projects using `atlas_graphql_query`:
   ```
   Call the atlas_graphql_query MCP tool with:
   - query: "query { project { projects_search(first: 20, filter: { archived: false }) { edges { node { key name state { value } targetDate } } } } }"
   - variables: "{}"
   ```
   Extract projects from `data.project.projects_search.edges[].node`.

3. **If specific project IDs provided**, call the `get_projects` MCP tool with the list of IDs. Parse the returned JSON array.

4. **Format the results as a table:**

   | Key | Name | Status | Target Date |
   |-----|------|--------|-------------|
   | PROJ-1 | Example Project | ON_TRACK | 2025-06-30 |

   - If status is missing, show "-"
   - If target date is missing, show "-"

5. **Show a count summary** at the end: "Showing N projects"

6. **On error**, display the error message clearly and suggest:
   - Check that the Atlas MCP server is configured in `.mcp.json`
   - Verify the `ATLAS_API_TOKEN` and `ATLAS_ORG_ID` environment variables are set
