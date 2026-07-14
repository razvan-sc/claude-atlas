"""Tests for the create_project MCP tool."""

import json

import httpx
import pytest

from atlas.config import AtlasConfig
from atlas.graphql_client import AtlasGraphQLClient
from atlas.server import _create_project_impl

CONTAINER = "ari:cloud:townsquare::site/cloud-1"
CLOUD_ID = "cloud-1"


@pytest.fixture
def config():
    return AtlasConfig(email="user@example.com", api_token="tok123", subdomain="mysite")


class _Router:
    """Routes GraphQL requests to canned responses keyed by operation name.

    Records every request body so tests can assert on the variables sent.
    """

    def __init__(self, responses: dict[str, dict]):
        self._responses = responses
        self.calls: list[dict] = []

    async def handler(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        self.calls.append(body)
        query = body["query"]
        for op, response in self._responses.items():
            if op in query:
                return httpx.Response(200, json=response)
        return httpx.Response(200, json={"errors": [{"message": f"unrouted: {query[:60]}"}]})

    def variables_for(self, op: str) -> dict:
        for call in self.calls:
            if op in call["query"]:
                return call["variables"]
        raise AssertionError(f"no call matched {op}")


def _create_ok(project_id="ari:proj/1", key="PROJ-1", name="My Project"):
    return {
        "data": {
            "projects_create": {
                "success": True,
                "errors": [],
                "project": {"id": project_id, "key": key, "name": name},
            }
        }
    }


def _edit_ok():
    return {"data": {"projects_edit": {"success": True, "errors": [], "project": {"id": "ari:proj/1", "key": "PROJ-1"}}}}


def _goal_link_ok(key="GOAL-9"):
    return {"data": {"projects_addGoalLink": {"success": True, "errors": [], "goal": {"id": "ari:goal/9", "key": key}}}}


def _goal_resolve_ok(goal_id="ari:goal/9", key="GOAL-9"):
    return {"data": {"goals_byKey": {"id": goal_id, "key": key, "name": "A goal"}}}


def _tag_ok():
    return {"data": {"home_addTagsByName": {"success": True, "errors": []}}}


def _jira_link_ok():
    return {"data": {"projects_addJiraWorkItemLink": {"success": True, "errors": []}}}


def _jira_resolve_ok(work_item_id="ari:cloud:jira:c:issue/42"):
    return {"data": {"jira": {"issueByKey": {"id": work_item_id, "key": "PROJ-123", "summary": "A ticket"}}}}


async def _run(config, router, **kwargs):
    transport = httpx.MockTransport(router.handler)
    async with AtlasGraphQLClient(config, transport=transport) as client:
        return await _create_project_impl(client, CONTAINER, CLOUD_ID, **kwargs)


class TestCreateProject:
    @pytest.mark.asyncio
    async def test_minimal_create(self, config):
        router = _Router({"projects_create": _create_ok()})
        result = await _run(config, router, name="My Project")

        parsed = json.loads(result)
        assert parsed["created"] is True
        assert parsed["key"] == "PROJ-1"
        assert parsed["id"] == "ari:proj/1"
        assert "warnings" not in parsed
        # only one call: the create itself
        assert len(router.calls) == 1
        assert router.variables_for("projects_create")["input"] == {
            "containerId": CONTAINER,
            "name": "My Project",
        }

    @pytest.mark.asyncio
    async def test_create_with_description(self, config):
        router = _Router({"projects_create": _create_ok(), "projects_edit": _edit_ok()})
        result = await _run(config, router, name="My Project", description="Build the thing")

        parsed = json.loads(result)
        assert parsed["description"] == "Build the thing"
        edit_vars = router.variables_for("projects_edit")["input"]
        assert edit_vars["id"] == "ari:proj/1"
        assert edit_vars["description"] == {"what": "Build the thing"}

    @pytest.mark.asyncio
    async def test_create_with_all_options(self, config):
        router = _Router(
            {
                "projects_create": _create_ok(),
                "projects_edit": _edit_ok(),
                "goals_byKey": _goal_resolve_ok(),
                "projects_addGoalLink": _goal_link_ok(),
                "home_addTagsByName": _tag_ok(),
                "issueByKey": _jira_resolve_ok(),
                "projects_addJiraWorkItemLink": _jira_link_ok(),
            }
        )
        result = await _run(
            config,
            router,
            name="My Project",
            description="desc",
            goal="GOAL-9",
            tag="platform",
            jira_issue_key="PROJ-123",
        )

        parsed = json.loads(result)
        assert parsed["description"] == "desc"
        assert parsed["goal"] == "GOAL-9"
        assert parsed["tag"] == "platform"
        assert parsed["jiraWorkItem"] == "PROJ-123"
        assert "warnings" not in parsed

        assert router.variables_for("projects_addGoalLink")["input"] == {
            "goalId": "ari:goal/9",
            "projectId": "ari:proj/1",
        }
        assert router.variables_for("home_addTagsByName")["input"] == {
            "nounId": "ari:proj/1",
            "tagNames": ["platform"],
        }
        assert router.variables_for("projects_addJiraWorkItemLink")["input"] == {
            "projectId": "ari:proj/1",
            "workItemId": "ari:cloud:jira:c:issue/42",
        }

    @pytest.mark.asyncio
    async def test_goal_ari_skips_resolution(self, config):
        router = _Router(
            {"projects_create": _create_ok(), "projects_addGoalLink": _goal_link_ok()}
        )
        await _run(config, router, name="P", goal="ari:goal/direct")

        # goals_byKey must not have been called
        assert all("goals_byKey" not in c["query"] for c in router.calls)
        assert router.variables_for("projects_addGoalLink")["input"]["goalId"] == "ari:goal/direct"

    @pytest.mark.asyncio
    async def test_jira_ari_skips_resolution(self, config):
        router = _Router(
            {"projects_create": _create_ok(), "projects_addJiraWorkItemLink": _jira_link_ok()}
        )
        await _run(config, router, name="P", jira_issue_key="ari:cloud:jira:c:issue/99")

        assert all("issueByKey" not in c["query"] for c in router.calls)
        assert (
            router.variables_for("projects_addJiraWorkItemLink")["input"]["workItemId"]
            == "ari:cloud:jira:c:issue/99"
        )

    @pytest.mark.asyncio
    async def test_create_failure_returns_error(self, config):
        router = _Router(
            {
                "projects_create": {
                    "data": {
                        "projects_create": {
                            "success": False,
                            "errors": [{"message": "name taken"}],
                            "project": None,
                        }
                    }
                }
            }
        )
        result = await _run(config, router, name="Dup")
        assert result.startswith("Error:")
        assert "name taken" in result

    @pytest.mark.asyncio
    async def test_optional_step_failure_becomes_warning(self, config):
        router = _Router(
            {
                "projects_create": _create_ok(),
                "home_addTagsByName": {
                    "data": {
                        "home_addTagsByName": {
                            "success": False,
                            "errors": [{"message": "tag service down"}],
                        }
                    }
                },
            }
        )
        result = await _run(config, router, name="P", tag="platform")

        parsed = json.loads(result)
        # project still created despite the tag failing
        assert parsed["created"] is True
        assert "tag" not in parsed
        assert any("tag not added" in w and "tag service down" in w for w in parsed["warnings"])

    @pytest.mark.asyncio
    async def test_goal_resolution_failure_becomes_warning(self, config):
        router = _Router(
            {
                "projects_create": _create_ok(),
                "goals_byKey": {"data": {"goals_byKey": None}},
            }
        )
        result = await _run(config, router, name="P", goal="MISSING-1")

        parsed = json.loads(result)
        assert parsed["created"] is True
        assert "goal" not in parsed
        assert any("goal not linked" in w for w in parsed["warnings"])
