---
name: atlas-create
description: Create one or more Atlas projects, optionally linked to a goal, tagged, and linked to Jira issues
allowed-tools: mcp__atlas__create_project, mcp__atlas__list_projects, mcp__atlas__get_project
---

# Atlas Create Project

Create one or more Atlas projects. Each project takes a name and description, and can optionally be linked to a goal, given a tag, and linked to a Jira issue.

## MCP Server

Use the `atlas` MCP server. All tool calls use the `mcp__atlas__` prefix.

## The `create_project` tool

`mcp__atlas__create_project` accepts:

- `name` (required): project name
- `description` (optional): the "what" text describing the project
- `goal` (optional): a goal key (e.g. `SAFET-2881`) or a goal ARI — resolved by key automatically
- `tag` (optional): a tag name — created if it doesn't already exist
- `jira_issue_key` (optional): a Jira issue key (e.g. `FG-6269`) or a work-item ARI — resolved by key automatically

The project is created first; each optional attribute is applied as a follow-up. If an optional step fails, the project is still created and the failure is returned in a `warnings` array. Read the returned JSON and surface any warnings to the user.

## Workflow: single project

1. Gather the details. `name` is required; ask for it if not provided. `description`, `goal`, `tag`, and `jira_issue_key` are optional — only include the ones the user wants.

2. Preview before creating:

   > ### Preview
   >
   > **Name:** [name]
   > **Description:** [description or "None"]
   > **Goal:** [goal or "None"]
   > **Tag:** [tag or "None"]
   > **Jira issue:** [jira_issue_key or "None"]
   >
   > Create this project? (yes/no)

3. On confirmation, call `mcp__atlas__create_project` with the gathered arguments.

4. On success, report the new project's `key`, `name`, and any `warnings`. Include a link: `https://<subdomain>.atlassian.net/o/-/s/projects/<key>` if the subdomain is known, otherwise just the key.

## Workflow: batch from a list of Jira issues

When the user provides a list of Jira issue keys and wants an Atlas project created for and linked to each:

1. Confirm the shared conventions once, up front:
   - **Naming**: name each project after its Jira ticket (default), or use names the user supplies. When naming after the ticket, the tool resolves the issue and its summary is available — a project named after the summary reads best.
   - **Description**: same text for all, per-ticket, or blank.
   - **Goal**: one goal key to link all of them to, or none.
   - **Tag**: one tag to apply to all, or none.

2. Show the full plan as a table and confirm before creating anything:

   | Jira issue | Project name | Goal | Tag |
   |------------|--------------|------|-----|
   | FG-6269 | ... | SAFET-2881 | platform |

3. On confirmation, call `mcp__atlas__create_project` **once per ticket**, passing `jira_issue_key` for each. Do not stop on the first failure — create the rest and collect results.

4. Report a summary table of results: each ticket, the created project key (or error), and any warnings.

## Error Handling

If a `create_project` call returns a string starting with `Error:`, the project was not created (creation is the first, required step). Surface the message and suggest:
- Verify the Jira issue key / goal key is correct and visible to you
- Check that the Atlas MCP server is configured in `.mcp.json`
- Verify `~/.atlas/config.json` exists with valid credentials

If the result is JSON with a `warnings` array, the project **was** created but one or more optional attributes did not apply — report both the success and the warnings.
