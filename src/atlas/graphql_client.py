"""GraphQL client for the Atlassian Atlas API."""

from __future__ import annotations

from typing import Any

import httpx

from atlas.config import AtlasConfig


class AtlasGraphQLClient:
    """Async GraphQL client with Basic Auth for the Atlas API."""

    def __init__(self, config: AtlasConfig, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._config = config
        self._client = httpx.AsyncClient(
            headers={
                "Authorization": config.auth_header,
                "Content-Type": "application/json",
            },
            transport=transport,
        )

    async def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a GraphQL query against the Atlas API.

        Args:
            query: The GraphQL query string.
            variables: Optional variables for the query.

        Returns:
            The parsed JSON response dictionary.

        Raises:
            httpx.HTTPStatusError: If the HTTP response is not 2xx.
            RuntimeError: If the GraphQL response contains errors.
        """
        response = await self._client.post(
            self._config.base_url,
            json={"query": query, "variables": variables or {}},
        )
        response.raise_for_status()

        result = response.json()
        if "errors" in result:
            messages = "; ".join(e["message"] for e in result["errors"])
            raise RuntimeError(f"GraphQL errors: {messages}")

        return result

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> AtlasGraphQLClient:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()
