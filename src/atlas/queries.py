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
    tags {
      edges {
        node {
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
    tags {
      edges {
        node {
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
        tags {
          name
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

CREATE_PROJECT_MUTATION = """
mutation projects_create($input: TownsquareProjectsCreateInput!) {
  projects_create(input: $input) {
    success
    errors {
      message
    }
    project {
      id
      key
      name
    }
  }
}
"""

SET_PROJECT_DESCRIPTION_MUTATION = """
mutation projects_edit($input: TownsquareProjectsEditInput) {
  projects_edit(input: $input) {
    success
    errors {
      message
    }
    project {
      id
      key
    }
  }
}
"""

ADD_GOAL_LINK_MUTATION = """
mutation projects_addGoalLink($input: TownsquareProjectsAddGoalLink!) {
  projects_addGoalLink(input: $input) {
    success
    errors {
      message
    }
    goal {
      id
      key
    }
  }
}
"""

ADD_TAGS_BY_NAME_MUTATION = """
mutation home_addTagsByName($input: TownsquareAddTagsByNameInput!) {
  home_addTagsByName(input: $input) {
    success
    errors {
      message
    }
  }
}
"""

ADD_JIRA_WORK_ITEM_LINK_MUTATION = """
mutation projects_addJiraWorkItemLink($input: TownsquareProjectsAddJiraWorkItemLinkInput!) {
  projects_addJiraWorkItemLink(input: $input) {
    success
    errors {
      message
    }
  }
}
"""

RESOLVE_GOAL_BY_KEY_QUERY = """
query goals_byKey($containerId: ID!, $goalKey: String!) {
  goals_byKey(containerId: $containerId, goalKey: $goalKey) {
    id
    key
    name
  }
}
"""

RESOLVE_JIRA_ISSUE_QUERY = """
query jiraIssueByKey($cloudId: ID!, $key: String!) {
  jira {
    issueByKey(cloudId: $cloudId, key: $key) {
      id
      key
      summary
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
