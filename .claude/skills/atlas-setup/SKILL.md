---
name: atlas-setup
description: Set up the atlas plugin for a new user - check uv, create ~/.atlas/config.json with their own Atlassian API token, and verify the atlas MCP server connects. Use when someone says "set up atlas", "atlas isn't working", or an atlas tool fails with a config or connection error.
allowed-tools: Bash, Read, mcp__atlas__list_projects
---

# Atlas Setup

Get the `atlas` MCP server working for the current user. Credentials are personal: never reuse anyone else's token, and never print the token back in chat.

## Step 1: Check uv

Run `uv --version`. If it is missing, tell the user to install it:

- macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- macOS (Homebrew): `brew install uv`
- Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

Then ask them to restart Claude Code so the MCP server can start.

## Step 2: Check the config file

Read `~/.atlas/config.json`.

- If it exists and has non-empty `email`, `api_token` and `subdomain`, go to Step 4.
- Otherwise continue to Step 3.

## Step 3: Create the config file

1. Ask the user for:
   - **email**: their Atlassian account email
   - **subdomain**: the `yoursite` part of `yoursite.atlassian.net` (for SafetyCulture this is usually `safetyculture`; confirm with the user)
2. Tell the user to create an API token at https://id.atlassian.com/manage-profile/security/api-tokens and write the file themselves, so the token never passes through chat:

   ```bash
   mkdir -p ~/.atlas && chmod 700 ~/.atlas
   cat > ~/.atlas/config.json << 'JSON'
   {
     "email": "<their email>",
     "api_token": "PASTE_TOKEN_HERE",
     "subdomain": "<their subdomain>"
   }
   JSON
   chmod 600 ~/.atlas/config.json
   ```

   Fill in email and subdomain for them; leave the token placeholder for them to replace.
3. Wait for them to confirm, then re-read the file and check the three fields are non-empty and the token is no longer `PASTE_TOKEN_HERE`. Do not echo the token.

## Step 4: Verify

Call `mcp__atlas__list_projects` with `limit: 1`.

- Success: say setup is done and list the available skills: `/atlas:projects`, `/atlas:create`, `/atlas:status`, `/atlas:update`, `/atlas:my-updates`, `/atlas:tag`.
- Tool not available: the plugin or MCP server isn't loaded. Ask them to run `/plugin install atlas@safetyculture-atlas` (after `/plugin marketplace add razvan-sc/claude-atlas`) and restart Claude Code.
- 401/403 error: the email or token is wrong, or the token expired. Have them create a new token and update the file.
- Other errors: show the error and check that `subdomain` matches their site URL.
