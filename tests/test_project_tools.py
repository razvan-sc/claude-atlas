"""Tests for Atlas project MCP tools."""

import json

import httpx
import pytest

from atlas.config import AtlasConfig
from atlas.graphql_client import AtlasGraphQLClient
from atlas.server import (
    _archive_project_impl,
    _get_project_impl,
    _get_projects_impl,
    _list_projects_impl,
)


@pytest.fixture
def config():
    return AtlasConfig(email="user@example.com", api_token="tok123", subdomain="mysite")


def _make_project_response(project_data, *, single=True):
    """Build a mock GraphQL response for project queries."""
    if single:
        return {"data": {"projects_byId": project_data}}
    return {"data": {"projects_byIds": project_data}}


def _sample_project(name="My Project", key="PROJ-1", tags=None):
    return {
        "key": key,
        "name": name,
        "description": {"what": "A test project", "why": "Testing"},
        "state": {"value": "on_track"},
        "dueDate": {"label": "Jun 2026", "confidence": "MONTH"},
        "owner": {"name": "Alice", "accountId": "acc-1"},
        "members": {
            "edges": [
                {"node": {"name": "Alice", "accountId": "acc-1"}},
                {"node": {"name": "Bob", "accountId": "acc-2"}},
            ]
        },
        "tags": {"edges": [{"node": {"name": t}} for t in (tags or [])]},
    }


class TestGetProject:
    """Tests for get_project tool."""

    @pytest.mark.asyncio
    async def test_returns_formatted_project(self, config):
        project = _sample_project()
        response = _make_project_response(project)

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _get_project_impl(client, "proj-123")

        parsed = json.loads(result)
        assert parsed["name"] == "My Project"
        assert parsed["description"] == "A test project"
        assert parsed["state"] == "on_track"
        assert parsed["dueDate"] == "Jun 2026"
        assert parsed["owner"] == "Alice"
        assert parsed["members"] == ["Alice", "Bob"]
        assert parsed["tags"] == []

    @pytest.mark.asyncio
    async def test_returns_tags(self, config):
        project = _sample_project(tags=["platform", "q1"])
        response = _make_project_response(project)

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _get_project_impl(client, "proj-123")

        parsed = json.loads(result)
        assert parsed["tags"] == ["platform", "q1"]

    @pytest.mark.asyncio
    async def test_error_returns_error_string(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={
                "errors": [{"message": "Project not found"}],
            })

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _get_project_impl(client, "nonexistent")

        assert result.startswith("Error:")


class TestGetProjects:
    """Tests for get_projects tool."""

    @pytest.mark.asyncio
    async def test_returns_formatted_projects(self, config):
        projects = [_sample_project("Proj A", "P-1"), _sample_project("Proj B", "P-2")]
        response = _make_project_response(projects, single=False)

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _get_projects_impl(client, ["p-1", "p-2"])

        parsed = json.loads(result)
        assert len(parsed) == 2
        assert parsed[0]["name"] == "Proj A"
        assert parsed[1]["name"] == "Proj B"
        assert parsed[0]["members"] == ["Alice", "Bob"]

    @pytest.mark.asyncio
    async def test_error_returns_error_string(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={
                "errors": [{"message": "Bad request"}],
            })

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _get_projects_impl(client, ["bad-id"])

        assert result.startswith("Error:")


class TestListProjects:
    """Tests for list_projects tag filtering."""

    def _make_search_response(self, projects):
        return {
            "data": {
                "projects_search": {
                    "edges": [{"node": {**p, "id": f"ari:{p['key']}"}} for p in projects]
                }
            }
        }

    @pytest.mark.asyncio
    async def test_returns_all_projects_without_tag_filter(self, config):
        projects = [
            _sample_project("Proj A", "P-1", tags=["platform"]),
            _sample_project("Proj B", "P-2", tags=["mobile"]),
        ]
        response = self._make_search_response(projects)

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _list_projects_impl(client, 50, "ari:cloud:townsquare::site/abc")

        parsed = json.loads(result)
        assert len(parsed) == 2

    @pytest.mark.asyncio
    async def test_filters_projects_by_tag(self, config):
        projects = [
            _sample_project("Proj A", "P-1", tags=["platform"]),
            _sample_project("Proj B", "P-2", tags=["mobile"]),
            _sample_project("Proj C", "P-3", tags=["platform", "mobile"]),
        ]
        response = self._make_search_response(projects)

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _list_projects_impl(
                client, 50, "ari:cloud:townsquare::site/abc", tag="platform"
            )

        parsed = json.loads(result)
        assert len(parsed) == 2
        assert {p["name"] for p in parsed} == {"Proj A", "Proj C"}

    @pytest.mark.asyncio
    async def test_tag_filter_returns_empty_when_no_match(self, config):
        projects = [_sample_project("Proj A", "P-1", tags=["mobile"])]
        response = self._make_search_response(projects)

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=response)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _list_projects_impl(
                client, 50, "ari:cloud:townsquare::site/abc", tag="platform"
            )

        parsed = json.loads(result)
        assert parsed == []


class TestArchiveProject:
    """Tests for archive_project tool."""

    @pytest.mark.asyncio
    async def test_archive_sends_correct_mutation(self, config):
        captured_body = {}
        response = {
            "data": {
                "projects_edit": {
                    "key": "PROJ-1",
                    "name": "My Project",
                    "state": {"value": "archived"},
                }
            }
        }

        async def handler(request: httpx.Request) -> httpx.Response:
            captured_body.update(json.loads(request.content))
            return httpx.Response(200, json=response)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _archive_project_impl(client, "proj-123", archive=True)

        parsed = json.loads(result)
        assert parsed["name"] == "My Project"
        assert parsed["state"] == "archived"
        assert captured_body["variables"]["input"]["archived"] is True

    @pytest.mark.asyncio
    async def test_unarchive_sends_correct_mutation(self, config):
        captured_body = {}
        response = {
            "data": {
                "projects_edit": {
                    "key": "PROJ-1",
                    "name": "My Project",
                    "state": {"value": "on_track"},
                }
            }
        }

        async def handler(request: httpx.Request) -> httpx.Response:
            captured_body.update(json.loads(request.content))
            return httpx.Response(200, json=response)

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _archive_project_impl(client, "proj-123", archive=False)

        parsed = json.loads(result)
        assert parsed["state"] == "on_track"
        assert captured_body["variables"]["input"]["archived"] is False

    @pytest.mark.asyncio
    async def test_error_returns_error_string(self, config):
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={
                "errors": [{"message": "Project not found"}],
            })

        transport = httpx.MockTransport(handler)
        async with AtlasGraphQLClient(config, transport=transport) as client:
            result = await _archive_project_impl(client, "bad-id", archive=True)

        assert result.startswith("Error:")
