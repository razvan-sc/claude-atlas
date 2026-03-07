# Roadmap: Claude Atlas

## Overview

Deliver a Claude Code integration for Atlassian Atlas Projects in three phases: stand up the MCP server with authentication and GraphQL connectivity, implement all project and update tools, then wrap common workflows in slash command skills.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation** - MCP server with config-based auth and GraphQL client (completed 2026-03-07)
- [ ] **Phase 2: Atlas Tools** - Project queries, updates, and mutations as MCP tools
- [ ] **Phase 3: Skills** - Slash command workflows for common Atlas operations

## Phase Details

### Phase 1: Foundation
**Goal**: A running MCP server that authenticates against Atlas and is discoverable by Claude Code
**Depends on**: Nothing (first phase)
**Requirements**: INFRA-01, INFRA-02, INFRA-03
**Success Criteria** (what must be TRUE):
  1. User can create ~/.atlas/config.json with email, API token, and subdomain, and the server reads it
  2. MCP server starts and Claude Code discovers it with its registered tools
  3. Server can execute a raw GraphQL query against the Atlas API and return a result
**Plans**: 1 plan

Plans:
- [ ] 01-01-PLAN.md — Project scaffold, config loader, GraphQL client, and MCP server with tool registration

### Phase 2: Atlas Tools
**Goal**: Users can read and manage their Atlas projects and status updates through MCP tools
**Depends on**: Phase 1
**Requirements**: PROJ-01, PROJ-02, PROJ-03, UPDT-01, UPDT-02, UPDT-03, UPDT-04
**Success Criteria** (what must be TRUE):
  1. User can ask Claude about a specific project and get back its name, description, contributors, and due date
  2. User can ask Claude for the latest status update on a project including summary, status, risks, and highlights
  3. User can ask Claude to post a new status update and it appears in Atlas
  4. User can ask Claude to archive or unarchive a project and the change is reflected in Atlas
**Plans**: TBD

Plans:
- [ ] 02-01: TBD

### Phase 3: Skills
**Goal**: Users have optimized slash command workflows for their most common Atlas tasks
**Depends on**: Phase 2
**Requirements**: SKIL-01, SKIL-02, SKIL-03
**Success Criteria** (what must be TRUE):
  1. User can run /atlas:projects and see a filtered list of their projects
  2. User can run /atlas:status with a project reference and see its latest status details
  3. User can run /atlas:update and interactively compose and post a status update
**Plans**: TBD

Plans:
- [ ] 03-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 1/1 | Complete    | 2026-03-07 |
| 2. Atlas Tools | 0/? | Not started | - |
| 3. Skills | 0/? | Not started | - |
