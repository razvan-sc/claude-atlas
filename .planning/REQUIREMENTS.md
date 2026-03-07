# Requirements: Claude Atlas

**Defined:** 2026-03-07
**Core Value:** Users can interact with their Atlas Projects directly from Claude Code without switching to the Atlassian UI

## v1 Requirements

### Infrastructure

- [x] **INFRA-01**: Config file at ~/.atlas/config.json stores email, API token, and subdomain
- [x] **INFRA-02**: Python MCP server with GraphQL client using Basic Auth against `https://{subdomain}.atlassian.net/gateway/api/graphql`
- [x] **INFRA-03**: MCP server registers all Atlas tools for Claude Code discovery

### Projects

- [ ] **PROJ-01**: User can query a single project by ID (name, description, contributors, due date)
- [ ] **PROJ-02**: User can query multiple projects by IDs in a single request
- [ ] **PROJ-03**: User can archive/unarchive a project

### Updates

- [ ] **UPDT-01**: User can read status updates for a project (summary, status, target date)
- [ ] **UPDT-02**: User can read unresolved risks for a project
- [ ] **UPDT-03**: User can read highlights/learnings for a project
- [ ] **UPDT-04**: User can post a new status update with summary, status, and highlights

### Skills

- [ ] **SKIL-01**: `/atlas:projects` skill lists and filters user's projects
- [ ] **SKIL-02**: `/atlas:status` skill shows latest status for a given project
- [ ] **SKIL-03**: `/atlas:update` skill posts a status update interactively

## v2 Requirements

### Projects

- **PROJ-04**: User can create a new project with name and target date
- **PROJ-05**: User can search/list all projects without knowing IDs

### Infrastructure

- **INFRA-04**: First-run interactive setup flow when config is missing
- **INFRA-05**: Multiple Atlassian instance support

### Updates

- **UPDT-05**: User can edit an existing status update

## Out of Scope

| Feature | Reason |
|---------|--------|
| Atlas Goals API | Focus on Projects API only for v1 |
| OAuth authentication | API token approach simpler and sufficient |
| Real-time notifications/webhooks | Polling/on-demand only |
| Web UI | CLI-only integration |
| Mobile support | Claude Code is desktop CLI |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| INFRA-01 | Phase 1 | Complete |
| INFRA-02 | Phase 1 | Complete |
| INFRA-03 | Phase 1 | Complete |
| PROJ-01 | Phase 2 | Pending |
| PROJ-02 | Phase 2 | Pending |
| PROJ-03 | Phase 2 | Pending |
| UPDT-01 | Phase 2 | Pending |
| UPDT-02 | Phase 2 | Pending |
| UPDT-03 | Phase 2 | Pending |
| UPDT-04 | Phase 2 | Pending |
| SKIL-01 | Phase 3 | Pending |
| SKIL-02 | Phase 3 | Pending |
| SKIL-03 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0

---
*Requirements defined: 2026-03-07*
*Last updated: 2026-03-07 after roadmap creation*
