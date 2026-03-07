"""GraphQL query and mutation strings for Atlas project operations."""

GET_PROJECT_QUERY = """
query projects_byId($projectId: String!) {
  projects_byId(projectId: $projectId) {
    key
    name
    description {
      what
      why
    }
    state {
      value
    }
    dueDate {
      label
      confidence
    }
    owner {
      name
      accountId
    }
    members {
      edges {
        node {
          accountId
          name
        }
      }
    }
  }
}
"""

GET_PROJECTS_QUERY = """
query projects_byIds($projectIds: [String!]!) {
  projects_byIds(projectIds: $projectIds) {
    key
    name
    description {
      what
      why
    }
    state {
      value
    }
    dueDate {
      label
      confidence
    }
    owner {
      name
      accountId
    }
    members {
      edges {
        node {
          accountId
          name
        }
      }
    }
  }
}
"""

EDIT_PROJECT_MUTATION = """
mutation projects_edit($input: TownsquareProjectsEditInput) {
  projects_edit(input: $input) {
    key
    name
    state {
      value
    }
  }
}
"""

CREATE_UPDATE_MUTATION = """
mutation projects_createUpdate($input: TownsquareProjectsCreateUpdateInput) {
  projects_createUpdate(input: $input) {
    summary
    newState {
      value
    }
    creationDate
  }
}
"""

LIST_PROJECTS_QUERY = """
query ListProjects($first: Int, $containerId: String!) {
  projects_search(
    searchString: ""
    containerId: $containerId
    first: $first
    sort: [LATEST_UPDATE_DATE_DESC]
  ) {
    edges {
      node {
        id
        key
        name
        description {
          what
        }
        state {
          value
        }
        dueDate {
          label
        }
        owner {
          name
          accountId
        }
        members {
          edges {
            node {
              name
              accountId
            }
          }
        }
      }
    }
  }
}
"""

GET_PROJECT_UPDATES_QUERY = """
query GetProjectUpdates($projectId: String!) {
  projects_byId(projectId: $projectId) {
    updates @optIn(to: "Townsquare") {
      edges {
        node {
          summary
          newState {
            value
          }
          creationDate
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
"""

TENANT_CONTEXT_QUERY = """
query GetTenantContext($hostNames: [String!]!) {
  tenantContexts(hostNames: $hostNames) {
    orgId
    cloudId
  }
}
"""
