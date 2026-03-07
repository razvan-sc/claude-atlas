"""GraphQL query and mutation strings for Atlas project operations."""

GET_PROJECT_QUERY = """
query projects_byId($id: ID!) {
  project {
    projects_byId(id: $id) {
      key
      name
      description
      state {
        value
      }
      targetDate
      contributors {
        edges {
          node {
            name
            aaid
          }
        }
      }
    }
  }
}
"""

GET_PROJECTS_QUERY = """
query projects_byIds($ids: [ID!]!) {
  project {
    projects_byIds(ids: $ids) {
      key
      name
      description
      state {
        value
      }
      targetDate
      contributors {
        edges {
          node {
            name
            aaid
          }
        }
      }
    }
  }
}
"""

EDIT_PROJECT_MUTATION = """
mutation projects_edit($projectId: ID!, $input: ProjectEditInput!) {
  project {
    projects_edit(projectId: $projectId, input: $input) {
      key
      name
      state {
        value
      }
    }
  }
}
"""

CREATE_UPDATE_MUTATION = """
mutation projects_createUpdate($projectId: ID!, $input: ProjectUpdateInput!) {
  project {
    projects_createUpdate(projectId: $projectId, input: $input) {
      summary
      status {
        value
      }
      createdAt
    }
  }
}
"""

GET_PROJECT_UPDATES_QUERY = """
query GetProjectUpdates($projectId: ID!) {
  project {
    projects_byId(id: $projectId) {
      updates {
        edges {
          node {
            summary
            status {
              value
            }
            targetDate
            createdAt
          }
        }
      }
      risks {
        edges {
          node {
            summary
            resolved
          }
        }
      }
      highlights {
        edges {
          node {
            summary
          }
        }
      }
    }
  }
}
"""
