"""Tests for Atlas project update tools."""

import json

import httpx
import pytest

from atlas.config import AtlasConfig
from atlas.graphql_client import AtlasGraphQLClient
from atlas.server import create_project_update, get_project_updates


@pytest.fixture
def config():
    return AtlasConfig(email="user@example.com", api_token="tok123", subdomain="mysite")


def _make_client(config: AtlasConfig, handler):
    transport = httpx.MockTransport(handler)
    return AtlasGraphQLClient(config, transport=transport)


class TestGetProjectUpdates:
    """Tests for the get_project_updates tool."""

    @pytest.mark.asyncio
    async def test_returns_updates_with_highlights(self, config):
        response_data = {
            "data": {
                "projects_byId": {
                    "updates": {
                        "edges": [
                            {
                                "node": {
                                    "summary": "Sprint 1 complete",
                                    "newState": {"value": "on_track"},
                                    "creationDate": "2026-03-01T10:00:00Z",
                                }
                            }
                        ]
                    },
                    "highlights": {
                        "edges": [
                            {"node": {"summary": "Shipped feature X"}}
                        ]
                    },
                }
            }
        }

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response_data)

        client = _make_client(config, handler)
        async with client:
            result = await get_project_updates._impl(client, "proj-123")

        parsed = json.loads(result)
        assert parsed["projectId"] == "proj-123"
        assert len(parsed["updates"]) == 1
        assert parsed["updates"][0]["summary"] == "Sprint 1 complete"
        assert parsed["updates"][0]["status"] == "on_track"
        assert len(parsed["highlights"]) == 1
        assert parsed["highlights"][0]["summary"] == "Shipped feature X"

    @pytest.mark.asyncio
    async def test_empty_updates(self, config):
        response_data = {
            "data": {
                "projects_byId": {
                    "updates": {"edges": []},
                    "highlights": {"edges": []},
                }
            }
        }

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response_data)

        client = _make_client(config, handler)
        async with client:
            result = await get_project_updates._impl(client, "proj-123")

        parsed = json.loads(result)
        assert parsed["updates"] == []
        assert parsed["highlights"] == []

    @pytest.mark.asyncio
    async def test_error_returns_error_string(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, text="Internal Server Error")

        client = _make_client(config, handler)
        async with client:
            result = await get_project_updates._impl(client, "proj-123")

        assert result.startswith("Error:")


class TestCreateProjectUpdate:
    """Tests for the create_project_update tool."""

    @pytest.mark.asyncio
    async def test_successful_creation_returns_confirmation(self, config):
        response_data = {
            "data": {
                "projects_createUpdate": {
                    "summary": "Q1 done",
                    "newState": {"value": "on_track"},
                    "creationDate": "2026-03-07T10:00:00Z",
                }
            }
        }

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response_data)

        client = _make_client(config, handler)
        async with client:
            result = await create_project_update._impl(
                client, "proj-123", "Q1 done", "on_track", "[]"
            )

        parsed = json.loads(result)
        assert parsed["created"] is True
        assert parsed["summary"] == "Q1 done"
        assert parsed["status"] == "on_track"
        assert parsed["createdAt"] == "2026-03-07T10:00:00Z"

    @pytest.mark.asyncio
    async def test_mutation_variables_are_correct(self, config):
        captured_body = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            captured_body.update(json.loads(request.content))
            return httpx.Response(
                200,
                json={
                    "data": {
                        "projects_createUpdate": {
                            "summary": "Update",
                            "newState": {"value": "at_risk"},
                            "creationDate": "2026-03-07T10:00:00Z",
                        }
                    }
                },
            )

        client = _make_client(config, handler)
        async with client:
            await create_project_update._impl(
                client, "proj-123", "Update", "at_risk", "[]"
            )

        variables = captured_body["variables"]
        assert variables["input"]["projectId"] == "proj-123"
        assert variables["input"]["summary"] == "Update"
        assert variables["input"]["status"] == "at_risk"

    @pytest.mark.asyncio
    async def test_invalid_status_returns_error(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"data": {}})

        client = _make_client(config, handler)
        async with client:
            result = await create_project_update._impl(
                client, "proj-123", "Update", "INVALID_STATUS", "[]"
            )

        assert result.startswith("Error:")
        assert "INVALID_STATUS" in result

    @pytest.mark.asyncio
    async def test_highlights_are_formatted_in_mutation(self, config):
        captured_body = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            captured_body.update(json.loads(request.content))
            return httpx.Response(
                200,
                json={
                    "data": {
                        "projects_createUpdate": {
                            "summary": "Update",
                            "newState": {"value": "on_track"},
                            "creationDate": "2026-03-07T10:00:00Z",
                        }
                    }
                },
            )

        client = _make_client(config, handler)
        async with client:
            await create_project_update._impl(
                client,
                "proj-123",
                "Update",
                "on_track",
                '["Shipped feature X", "Completed migration"]',
            )

        variables = captured_body["variables"]
        highlights = variables["input"]["highlights"]
        assert len(highlights) == 2
        assert highlights[0]["summary"] == "Shipped feature X"
        assert highlights[1]["summary"] == "Completed migration"

    @pytest.mark.asyncio
    async def test_error_returns_error_string(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, text="Internal Server Error")

        client = _make_client(config, handler)
        async with client:
            result = await create_project_update._impl(
                client, "proj-123", "Update", "on_track", "[]"
            )

        assert result.startswith("Error:")
