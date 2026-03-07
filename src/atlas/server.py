"""MCP server for Atlassian Atlas integration."""

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from atlas.config import load_config
from atlas.graphql_client import AtlasGraphQLClient
from atlas.queries import (
    EDIT_PROJECT_MUTATION,
    GET_PROJECT_QUERY,
    GET_PROJECT_UPDATES_QUERY,
    GET_PROJECTS_QUERY,
)

mcp = FastMCP("atlas")


def _format_project(raw: dict[str, Any]) -> dict[str, Any]:
    """Flatten a raw GraphQL project response into a readable dict."""
    contributors = [
        edge["node"]["name"]
        for edge in raw.get("contributors", {}).get("edges", [])
    ]
    return {
        "key": raw.get("key"),
        "name": raw.get("name"),
        "description": raw.get("description"),
        "state": raw.get("state", {}).get("value") if raw.get("state") else None,
        "targetDate": raw.get("targetDate"),
        "contributors": contributors,
    }


async def _get_project_impl(client: AtlasGraphQLClient, project_id: str) -> str:
    """Fetch a single project by ID and return formatted JSON."""
    try:
        result = await client.execute(GET_PROJECT_QUERY, {"id": project_id})
        raw = result["data"]["project"]["projects_byId"]
        return json.dumps(_format_project(raw), indent=2)
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


async def _get_projects_impl(client: AtlasGraphQLClient, project_ids: list[str]) -> str:
    """Fetch multiple projects by IDs and return formatted JSON array."""
    try:
        result = await client.execute(GET_PROJECTS_QUERY, {"ids": project_ids})
        raw_list = result["data"]["project"]["projects_byIds"]
        return json.dumps([_format_project(p) for p in raw_list], indent=2)
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


async def _archive_project_impl(
    client: AtlasGraphQLClient, project_id: str, *, archive: bool = True
) -> str:
    """Archive or unarchive a project and return confirmation."""
    try:
        result = await client.execute(
            EDIT_PROJECT_MUTATION,
            {"projectId": project_id, "input": {"archived": archive}},
        )
        raw = result["data"]["project"]["projects_edit"]
        action = "Archived" if archive else "Unarchived"
        return json.dumps(
            {
                "action": action,
                "key": raw.get("key"),
                "name": raw.get("name"),
                "state": raw.get("state", {}).get("value") if raw.get("state") else None,
            },
            indent=2,
        )
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


@mcp.tool()
async def atlas_graphql_query(query: str, variables: str = "{}") -> str:
    """Execute a raw GraphQL query against the Atlassian Atlas API.

    Args:
        query: The GraphQL query string to execute
        variables: JSON string of variables for the query (default: "{}")

    Returns:
        The JSON response from the Atlas API
    """
    try:
        config = load_config()
        parsed_variables = json.loads(variables)
        async with AtlasGraphQLClient(config) as client:
            result = await client.execute(query, parsed_variables)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


@mcp.tool()
async def get_project(project_id: str) -> str:
    """Get details of a single Atlas project by ID.

    Returns project name, description, state, target date, and contributors.

    Args:
        project_id: The Atlas project ID

    Returns:
        JSON string with project details
    """
    config = load_config()
    async with AtlasGraphQLClient(config) as client:
        return await _get_project_impl(client, project_id)


@mcp.tool()
async def get_projects(project_ids: list[str]) -> str:
    """Get details of multiple Atlas projects by their IDs.

    Returns an array of project details including name, description, state,
    target date, and contributors for each project.

    Args:
        project_ids: List of Atlas project IDs

    Returns:
        JSON string with array of project details
    """
    config = load_config()
    async with AtlasGraphQLClient(config) as client:
        return await _get_projects_impl(client, project_ids)


@mcp.tool()
async def archive_project(project_id: str, archive: bool = True) -> str:
    """Archive or unarchive an Atlas project. Set archive=False to unarchive.

    Args:
        project_id: The Atlas project ID
        archive: True to archive, False to unarchive (default: True)

    Returns:
        JSON string with confirmation of the action
    """
    config = load_config()
    async with AtlasGraphQLClient(config) as client:
        return await _archive_project_impl(client, project_id, archive=archive)


async def _get_project_updates_impl(client: AtlasGraphQLClient, project_id: str) -> str:
    """Fetch status updates, risks, and highlights for a project."""
    try:
        result = await client.execute(
            GET_PROJECT_UPDATES_QUERY, {"projectId": project_id}
        )
        raw = result["data"]["project"]["projects_byId"]

        updates = [
            {
                "summary": edge["node"]["summary"],
                "status": edge["node"]["status"]["value"]
                if edge["node"].get("status")
                else None,
                "targetDate": edge["node"].get("targetDate"),
                "createdAt": edge["node"].get("createdAt"),
            }
            for edge in raw.get("updates", {}).get("edges", [])
        ]

        risks = [
            {"summary": edge["node"]["summary"]}
            for edge in raw.get("risks", {}).get("edges", [])
            if not edge["node"].get("resolved", False)
        ]

        highlights = [
            {"summary": edge["node"]["summary"]}
            for edge in raw.get("highlights", {}).get("edges", [])
        ]

        return json.dumps(
            {
                "projectId": project_id,
                "updates": updates,
                "risks": risks,
                "highlights": highlights,
            },
            indent=2,
        )
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


@mcp.tool()
async def get_project_updates(project_id: str) -> str:
    """Get status updates, risks, and highlights for an Atlas project.

    Returns the latest status updates with summary, status, target date,
    unresolved risks, and highlights/learnings.

    Args:
        project_id: The Atlas project ID

    Returns:
        JSON string with updates, risks, and highlights
    """
    config = load_config()
    async with AtlasGraphQLClient(config) as client:
        return await _get_project_updates_impl(client, project_id)


# Expose impl for testing
get_project_updates._impl = _get_project_updates_impl


def main() -> None:
    """Run the Atlas MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
