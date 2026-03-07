---
phase: 02-atlas-tools
plan: 01
subsystem: api
tags: [mcp, graphql, atlas, project-tools, fastmcp]

requires:
  - phase: 01-foundation
    provides: MCP server with FastMCP, AtlasGraphQLClient, load_config
provides:
  - get_project MCP tool for single project queries
  - get_projects MCP tool for batch project queries
  - archive_project MCP tool for archiving/unarchiving projects
  - GraphQL queries module (src/atlas/queries.py)
affects: [02-atlas-tools, 03-polish]

tech-stack:
  added: []
  patterns: [impl-function-pattern, response-flattening, separated-queries-module]

key-files:
  created:
    - src/atlas/queries.py
    - tests/test_project_tools.py
  modified:
    - src/atlas/server.py

key-decisions:
  - "Used thin _impl functions that accept client for testability instead of testing MCP tools directly"
  - "GraphQL queries isolated in separate queries.py module as module-level constants"
  - "Response flattening extracts nested GraphQL structure into readable flat JSON"

patterns-established:
  - "Impl pattern: _foo_impl(client, ...) for testable logic, MCP tool wraps with config+client"
  - "Query module: GraphQL strings as module-level constants in queries.py"
  - "Format pattern: _format_project() flattens contributors edges to list of names"

requirements-completed: [PROJ-01, PROJ-02, PROJ-03]

duration: 4min
completed: 2026-03-07
---

# Phase 2 Plan 1: Project Tools Summary

**MCP tools for querying single/batch Atlas projects and archiving/unarchiving with GraphQL queries in separate module**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-07T09:17:35Z
- **Completed:** 2026-03-07T09:21:10Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Three new MCP tools: get_project, get_projects, archive_project
- GraphQL queries and mutations isolated in src/atlas/queries.py
- Response flattening converts nested GraphQL structure to readable JSON with flat contributor lists
- 7 new tests covering all project tool behaviors

## Task Commits

Each task was committed atomically:

1. **Task 1: GraphQL queries and get_project/get_projects tools** - `d5b1040` (test RED), `685dab2` (feat GREEN)
2. **Task 2: Archive/unarchive project tool** - `9aca42a` (test RED), `ca68a89` (feat GREEN)

_Note: TDD tasks have multiple commits (test then feat)_

## Files Created/Modified
- `src/atlas/queries.py` - GraphQL query strings (GET_PROJECT_QUERY, GET_PROJECTS_QUERY, EDIT_PROJECT_MUTATION)
- `src/atlas/server.py` - Three new MCP tools with _impl functions and _format_project helper
- `tests/test_project_tools.py` - 7 tests for project query and mutation tools

## Decisions Made
- Used _impl functions accepting a pre-constructed client for direct testability without mocking config
- Isolated GraphQL query strings as module-level constants in queries.py for reuse and readability
- Flattened nested GraphQL response (contributors.edges[].node.name) to simple list of names

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Pre-existing test file `tests/test_update_tools.py` and external modifications to `queries.py` and `server.py` from an external process (future plan code). These were left in place as they don't affect current plan functionality. Logged to deferred items.

## Next Phase Readiness
- Project tools complete, ready for additional tool plans in phase 02
- Established patterns (_impl functions, queries module) for all future tools

---
*Phase: 02-atlas-tools*
*Completed: 2026-03-07*

## Self-Check: PASSED

All 3 source files verified present. All 4 task commits verified in git history.
