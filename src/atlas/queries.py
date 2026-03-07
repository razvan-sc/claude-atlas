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
