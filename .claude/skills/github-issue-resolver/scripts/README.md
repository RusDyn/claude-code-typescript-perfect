# GitHub Issue Resolver Scripts

## Requirements

**Python:** 3.7+ (no external dependencies required)

All scripts use only Python standard library modules:
- `urllib` for HTTP requests
- `json` for data parsing
- `re` for pattern matching
- `sys`, `os` for system operations

## Scripts

### fetch_issue.py
Fetches issue details from GitHub API.

**Usage:**
```bash
python fetch_issue.py owner/repo#123 [GITHUB_TOKEN]
# or
python fetch_issue.py https://github.com/owner/repo/issues/123
```

### analyze_repository.py
Analyzes repository structure and locates relevant code.

**Usage:**
```bash
python analyze_repository.py /path/to/repo [search_pattern]
```

### create_pr.py
Creates pull request via GitHub API.

**Usage:**
```bash
python create_pr.py '{"owner": "...", "repo": "...", "title": "...", ...}'
```

## Environment Variables

- `GITHUB_TOKEN` - GitHub personal access token (recommended to avoid rate limits)
  - Get from: https://github.com/settings/tokens
  - Required scopes: `repo`, `workflow`

## Quick Setup

```bash
# No installation needed - uses Python standard library only
python3 --version  # Verify Python 3.7+

# Set GitHub token (optional but recommended)
export GITHUB_TOKEN=ghp_yourtoken

# Run any script
python3 fetch_issue.py owner/repo#123
```
