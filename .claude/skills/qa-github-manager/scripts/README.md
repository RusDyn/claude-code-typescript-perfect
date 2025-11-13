# QA GitHub Manager Scripts

## Requirements

**Python:** 3.7+ (no external dependencies required)

All scripts use only Python standard library modules:
- `json` for data parsing
- `difflib` for text comparison
- `dataclasses` for structured data
- `typing` for type hints

## Scripts

### parse_feedback.py
Parses unstructured client feedback into structured issue items.

**Usage:**
```bash
python parse_feedback.py "Client reported login broken on mobile. Also need password reset."
```

**Output:** JSON array of structured feedback items with type, severity, and extracted details.

### issue_analyzer.py
Analyzes feedback complexity and suggests atomic issue breakdown.

**Usage:**
```bash
python issue_analyzer.py '{
  "description": "Fix login and add 2FA",
  "item_type": "bug",
  "severity": "high"
}'
```

**Output:** Recommendations for splitting complex feedback into atomic issues.

### github_issues.py
Manages GitHub issue operations - search, compare, create, reopen.

**Usage:**
```bash
# Search for similar issues
python github_issues.py search --issue '{"title": "Login broken"}' --existing '[...]'

# Check if should reopen
python github_issues.py reopen-check \
  --new '{"title": "Login broken", "body": "..."}' \
  --existing '{"number": 123, "state": "closed", "closed_at": "2024-01-10"}'

# Create issue
python github_issues.py create --issue '{...}' --token $GITHUB_TOKEN
```

## Environment Variables

- `GITHUB_TOKEN` - GitHub personal access token (required for creating issues)
  - Get from: https://github.com/settings/tokens
  - Required scopes: `repo`, `workflow`

## Quick Setup

```bash
# No installation needed - uses Python standard library only
python3 --version  # Verify Python 3.7+

# Set GitHub token for issue creation
export GITHUB_TOKEN=ghp_yourtoken

# Parse feedback
python3 parse_feedback.py "Client feedback text here"

# Analyze complexity
python3 issue_analyzer.py '{"description": "...", "item_type": "bug"}'
```

## Workflow Example

```bash
# 1. Parse client feedback
FEEDBACK="Login doesn't work on mobile and we need password reset"
python3 parse_feedback.py "$FEEDBACK" > parsed.json

# 2. Analyze each item for complexity
cat parsed.json | jq -r '.[]' | while read item; do
  python3 issue_analyzer.py "$item"
done

# 3. Search for existing similar issues
python3 github_issues.py search \
  --issue '{"title": "Login broken on mobile"}' \
  --existing "$(gh issue list --json number,title,body,state)"

# 4. Create new issue if no duplicates
python3 github_issues.py create \
  --issue '{"title": "...", "body": "...", "labels": ["bug"]}' \
  --token $GITHUB_TOKEN
```
