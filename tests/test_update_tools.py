"""Tests for Atlas project update tools."""

import json

import httpx
import pytest

from atlas.config import AtlasConfig
from atlas.graphql_client import AtlasGraphQLClient
from atlas.server import get_project_updates


@pytest.fixture
def config():
    return AtlasConfig(email="user@example.com", api_token="tok123", subdomain="mysite")


def _make_client(config: AtlasConfig, handler):
    transport = httpx.MockTransport(handler)
    return AtlasGraphQLClient(config, transport=transport)


class TestGetProjectUpdates:
    """Tests for the get_project_updates tool."""

    @pytest.mark.asyncio
    async def test_returns_updates_with_risks_and_highlights(self, config):
        response_data = {
            "data": {
                "project": {
                    "projects_byId": {
                        "updates": {
                            "edges": [
                                {
                                    "node": {
                                        "summary": "Sprint 1 complete",
                                        "status": {"value": "ON_TRACK"},
                                        "targetDate": "2026-04-01",
                                        "createdAt": "2026-03-01T10:00:00Z",
                                    }
                                }
                            ]
                        },
                        "risks": {
                            "edges": [
                                {"node": {"summary": "Budget risk", "resolved": False}},
                                {"node": {"summary": "Old risk", "resolved": True}},
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
        assert parsed["updates"][0]["status"] == "ON_TRACK"
        # Only unresolved risks
        assert len(parsed["risks"]) == 1
        assert parsed["risks"][0]["summary"] == "Budget risk"
        assert len(parsed["highlights"]) == 1
        assert parsed["highlights"][0]["summary"] == "Shipped feature X"

    @pytest.mark.asyncio
    async def test_empty_updates(self, config):
        response_data = {
            "data": {
                "project": {
                    "projects_byId": {
                        "updates": {"edges": []},
                        "risks": {"edges": []},
                        "highlights": {"edges": []},
                    }
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
        assert parsed["risks"] == []
        assert parsed["highlights"] == []

    @pytest.mark.asyncio
    async def test_filters_resolved_risks(self, config):
        response_data = {
            "data": {
                "project": {
                    "projects_byId": {
                        "updates": {"edges": []},
                        "risks": {
                            "edges": [
                                {"node": {"summary": "Resolved one", "resolved": True}},
                                {"node": {"summary": "Active risk", "resolved": False}},
                                {"node": {"summary": "Another resolved", "resolved": True}},
                            ]
                        },
                        "highlights": {"edges": []},
                    }
                }
            }
        }

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response_data)

        client = _make_client(config, handler)
        async with client:
            result = await get_project_updates._impl(client, "proj-123")

        parsed = json.loads(result)
        assert len(parsed["risks"]) == 1
        assert parsed["risks"][0]["summary"] == "Active risk"

    @pytest.mark.asyncio
    async def test_error_returns_error_string(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, text="Internal Server Error")

        client = _make_client(config, handler)
        async with client:
            result = await get_project_updates._impl(client, "proj-123")

        assert result.startswith("Error:")
