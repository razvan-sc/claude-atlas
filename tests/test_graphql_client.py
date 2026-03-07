"""Tests for atlas.graphql_client module."""

import json

import httpx
import pytest

from atlas.config import AtlasConfig
from atlas.graphql_client import AtlasGraphQLClient


@pytest.fixture
def config():
    return AtlasConfig(email="user@example.com", api_token="tok123", subdomain="mysite")


class TestAtlasGraphQLClient:
    """Tests for the AtlasGraphQLClient class."""

    @pytest.mark.asyncio
    async def test_successful_query_returns_parsed_json(self, config):
        response_data = {"data": {"project": {"name": "Test"}}}

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response_data)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await client.execute("{ project { name } }")
        assert result == response_data

    @pytest.mark.asyncio
    async def test_auth_header_is_set(self, config):
        captured_headers = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            captured_headers.update(dict(request.headers))
            return httpx.Response(200, json={"data": {}})

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            await client.execute("{ test }")
        assert captured_headers["authorization"] == config.auth_header

    @pytest.mark.asyncio
    async def test_http_error_raises(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, text="Unauthorized")

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            with pytest.raises(httpx.HTTPStatusError):
                await client.execute("{ test }")

    @pytest.mark.asyncio
    async def test_graphql_errors_raise_runtime_error(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={
                "errors": [{"message": "Field not found"}],
            })

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            with pytest.raises(RuntimeError, match="Field not found"):
                await client.execute("{ badField }")

    @pytest.mark.asyncio
    async def test_sends_query_and_variables(self, config):
        captured_body = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            captured_body.update(json.loads(request.content))
            return httpx.Response(200, json={"data": {}})

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            await client.execute("query($id: ID!) { node(id: $id) { id } }", {"id": "123"})
        assert captured_body["query"] == "query($id: ID!) { node(id: $id) { id } }"
        assert captured_body["variables"] == {"id": "123"}
