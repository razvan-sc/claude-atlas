"""MCP server for Atlassian Atlas integration."""

import json

from mcp.server.fastmcp import FastMCP

from atlas.config import load_config
from atlas.graphql_client import AtlasGraphQLClient

mcp = FastMCP("atlas")


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


def main() -> None:
    """Run the Atlas MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
