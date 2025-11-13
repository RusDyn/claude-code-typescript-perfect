# GitHub API Reference for Issues

Quick reference for common GitHub API operations needed for issue management.

## Authentication

```bash
# Using Personal Access Token
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/issues
```

**Required Scopes for Token:**

- `repo` - Full repository access (for private repos)
- `public_repo` - Public repository access only

## Common API Endpoints

### Search Issues

```bash
GET /search/issues?q={query}
```

**Example:**

```bash
curl -H "Authorization: token YOUR_TOKEN" \
  "https://api.github.com/search/issues?q=repo:owner/repo+label:bug+state:open"
```

**Query Syntax:**

- `repo:owner/repo` - Specific repository
- `label:bug` - Has label "bug"
- `state:open` or `state:closed`
- `is:issue` or `is:pr`
- `author:username`
- `assignee:username`
- `created:>=2024-01-01`
- `updated:>=2024-01-01`

**Combining Terms:**

```
login button label:bug state:open
```

### List Issues

```bash
GET /repos/{owner}/{repo}/issues
```

**Parameters:**

- `state`: `open`, `closed`, or `all`
- `labels`: Comma-separated list
- `sort`: `created`, `updated`, `comments`
- `direction`: `asc` or `desc`
- `since`: ISO 8601 timestamp

**Example:**

```bash
curl -H "Authorization: token YOUR_TOKEN" \
  "https://api.github.com/repos/owner/repo/issues?state=all&labels=bug,critical&sort=updated"
```

### Get Single Issue

```bash
GET /repos/{owner}/{repo}/issues/{issue_number}
```

**Example:**

```bash
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/owner/repo/issues/123
```

### Create Issue

```bash
POST /repos/{owner}/{repo}/issues
```

**Body:**

```json
{
  "title": "Issue title",
  "body": "Issue description with markdown support",
  "labels": ["bug", "priority-high"],
  "assignees": ["username1", "username2"],
  "milestone": 1
}
```

**Example:**

```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Login button not responding",
    "body": "## Description\nButton does not respond...",
    "labels": ["bug", "component-auth"]
  }' \
  https://api.github.com/repos/owner/repo/issues
```

**Response:**

```json
{
  "id": 1,
  "number": 123,
  "state": "open",
  "title": "Login button not responding",
  "body": "## Description\nButton does not respond...",
  "user": {...},
  "labels": [...],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z",
  "html_url": "https://github.com/owner/repo/issues/123"
}
```

### Update Issue

```bash
PATCH /repos/{owner}/{repo}/issues/{issue_number}
```

**Body (all fields optional):**

```json
{
  "title": "New title",
  "body": "Updated description",
  "state": "open",
  "labels": ["bug"],
  "assignees": ["username"],
  "milestone": 2
}
```

**Reopen Issue:**

```bash
curl -X PATCH \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state": "open"}' \
  https://api.github.com/repos/owner/repo/issues/123
```

### Add Comment

```bash
POST /repos/{owner}/{repo}/issues/{issue_number}/comments
```

**Body:**

```json
{
  "body": "Comment text with **markdown** support"
}
```

**Example:**

```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"body": "## Reopening\nNew information..."}' \
  https://api.github.com/repos/owner/repo/issues/123/comments
```

### List Comments

```bash
GET /repos/{owner}/{repo}/issues/{issue_number}/comments
```

### Add Labels

```bash
POST /repos/{owner}/{repo}/issues/{issue_number}/labels
```

**Body:**

```json
{
  "labels": ["bug", "priority-high"]
}
```

### Remove Label

```bash
DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels/{label_name}
```

### Replace All Labels

```bash
PUT /repos/{owner}/{repo}/issues/{issue_number}/labels
```

**Body:**

```json
{
  "labels": ["bug", "in-progress"]
}
```

## Rate Limiting

**Limits:**

- Authenticated: 5,000 requests/hour
- Unauthenticated: 60 requests/hour

**Check Rate Limit:**

```bash
GET /rate_limit
```

**Response Headers:**

```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
X-RateLimit-Reset: 1234567890
```

## Pagination

Large result sets are paginated:

```bash
GET /repos/{owner}/{repo}/issues?page=2&per_page=50
```

**Parameters:**

- `page`: Page number (default: 1)
- `per_page`: Items per page (max: 100, default: 30)

**Response Headers:**

```
Link: <https://api.github.com/repos/owner/repo/issues?page=3>; rel="next",
      <https://api.github.com/repos/owner/repo/issues?page=10>; rel="last"
```

## Search Examples

### Find All Open Bugs

```
GET /search/issues?q=repo:owner/repo+label:bug+state:open
```

### Find Issues by Title Keywords

```
GET /search/issues?q=repo:owner/repo+login+button+in:title
```

### Find Recent Critical Issues

```
GET /search/issues?q=repo:owner/repo+label:priority-critical+created:>2024-01-01
```

### Find Issues Assigned to User

```
GET /search/issues?q=repo:owner/repo+assignee:username+state:open
```

### Find Issues Without Assignee

```
GET /search/issues?q=repo:owner/repo+no:assignee+state:open
```

### Find Closed Issues with Specific Label

```
GET /search/issues?q=repo:owner/repo+label:bug+state:closed
```

## Python Integration Example

```python
import requests
import json

class GitHubIssuesAPI:
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def search_issues(self, query):
        """Search issues"""
        url = f"{self.base_url}/search/issues"
        params = {"q": f"repo:{self.owner}/{self.repo} {query}"}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_issue(self, issue_number):
        """Get single issue"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_issue(self, title, body, labels=None, assignees=None):
        """Create new issue"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
        data = {
            "title": title,
            "body": body,
            "labels": labels or [],
            "assignees": assignees or []
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def reopen_issue(self, issue_number, comment=None):
        """Reopen closed issue"""
        # Update state to open
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}"
        data = {"state": "open"}
        response = requests.patch(url, headers=self.headers, json=data)

        # Add comment if provided
        if comment:
            comment_url = f"{url}/comments"
            requests.post(comment_url, headers=self.headers,
                         json={"body": comment})

        return response.json()

    def add_comment(self, issue_number, comment):
        """Add comment to issue"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}/comments"
        data = {"body": comment}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def add_labels(self, issue_number, labels):
        """Add labels to issue"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues/{issue_number}/labels"
        data = {"labels": labels}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

# Usage
api = GitHubIssuesAPI(token="YOUR_TOKEN", owner="owner", repo="repo")

# Search for bugs
results = api.search_issues("label:bug state:open")

# Create issue
new_issue = api.create_issue(
    title="Login button not responding",
    body="## Description\nButton does not respond on mobile",
    labels=["bug", "priority-high"],
    assignees=["developer1"]
)

# Reopen with comment
api.reopen_issue(
    issue_number=123,
    comment="## Reopening\nIssue has recurred..."
)
```

## Error Handling

**Common HTTP Status Codes:**

- `200 OK` - Success
- `201 Created` - Issue created successfully
- `304 Not Modified` - Cached response
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication failed
- `403 Forbidden` - Rate limit or permissions
- `404 Not Found` - Issue doesn't exist
- `422 Unprocessable Entity` - Validation failed

**Error Response:**

```json
{
  "message": "Validation Failed",
  "errors": [
    {
      "resource": "Issue",
      "field": "title",
      "code": "missing_field"
    }
  ]
}
```

## Best Practices

1. **Cache API Results** - Reduce API calls
2. **Use Conditional Requests** - Save rate limit with `If-None-Match`
3. **Handle Rate Limits** - Check `X-RateLimit-Remaining`
4. **Batch Operations** - Use GraphQL API for complex queries
5. **Use Webhooks** - For real-time updates instead of polling
6. **Paginate Results** - Don't assume all results in one page

## Useful Links

- API Documentation: https://docs.github.com/en/rest/issues
- Search Syntax: https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests
- GraphQL API: https://docs.github.com/en/graphql
- Rate Limiting: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
