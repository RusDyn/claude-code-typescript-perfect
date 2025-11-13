# GitHub Issue Resolution Workflow

Complete workflow for resolving GitHub issues from analysis to pull request.

## Overview

The complete workflow:

1. **Fetch & Analyze Issue** - Understand the problem
2. **Analyze Repository** - Understand the codebase
3. **Plan Solution** - Design the fix/feature
4. **Implement Changes** - Write the code
5. **Test Changes** - Verify the solution
6. **Create Pull Request** - Submit for review

## Step 1: Fetch & Analyze Issue

### Using the fetch_issue.py Script

```bash
# Fetch issue details
python scripts/fetch_issue.py owner/repo#123

# Or with full URL
python scripts/fetch_issue.py https://github.com/owner/repo/issues/123

# With GitHub token (for private repos or higher rate limits)
python scripts/fetch_issue.py owner/repo#123 ghp_yourtoken
```

### Analyze Issue Output

The script provides:

- **Issue details**: Title, body, author, labels
- **Type detection**: Bug, feature, documentation, test
- **Complexity estimate**: Low, medium, high
- **Context clues**:
  - Files mentioned in issue
  - Related issues
  - Code samples provided
  - Reproduction steps

### Understanding the Issue

Key questions to answer:

1. **What is broken or missing?** - Core problem
2. **What should happen instead?** - Expected behavior
3. **How to reproduce?** - Steps or conditions
4. **Which files are involved?** - Scope of changes
5. **Are there related issues?** - Additional context

## Step 2: Analyze Repository

### Clone the Repository

```bash
# Clone the repository
git clone https://github.com/owner/repo.git
cd repo

# Or if already cloned, update it
git fetch origin
git checkout main  # or master
git pull origin main
```

### Analyze Repository Structure

```bash
# Analyze repository
python scripts/analyze_repository.py /path/to/repo

# Search for specific patterns (e.g., function names mentioned in issue)
python scripts/analyze_repository.py /path/to/repo "function_name"
```

### Key Things to Identify

1. **Project type**: Node.js, Python, Rust, etc.
2. **Framework**: React, Django, Express, etc.
3. **Test setup**: Jest, pytest, Go test, etc.
4. **Code organization**: Where related code lives
5. **Contributing guidelines**: CONTRIBUTING.md requirements

### Read Key Files

Always read:

- `README.md` - Project overview
- `CONTRIBUTING.md` - Contribution guidelines
- `package.json` or equivalent - Dependencies and scripts
- Related source files identified from issue

## Step 3: Plan Solution

### For Bug Fixes

1. **Locate the bug**:
   - Search for error messages
   - Find files mentioned in issue
   - Look at stack traces if provided

2. **Understand root cause**:
   - Why does this bug happen?
   - What conditions trigger it?
   - Are there edge cases?

3. **Plan the fix**:
   - Minimal change to fix the issue
   - Won't break existing functionality
   - Handles edge cases

### For Features

1. **Understand requirements**:
   - What functionality is needed?
   - How should it integrate?
   - API design if applicable

2. **Design the solution**:
   - Which files to modify
   - New files needed
   - Changes to existing APIs

3. **Consider impact**:
   - Breaking changes?
   - Performance implications?
   - Documentation needs?

### Create Implementation Plan

Document your plan:

```
## Implementation Plan

Files to modify:
- src/auth.js - Add new validation
- src/utils.js - Helper function
- tests/auth.test.js - Add tests

Changes:
1. Add email validation in auth.js
2. Create isValidEmail() utility
3. Add 5 test cases

Edge cases to handle:
- Empty email
- Invalid format
- Special characters
```

## Step 4: Implement Changes

### Create Feature Branch

```bash
# Create and checkout new branch
git checkout -b fix/issue-123-auth-bug
# Or for features: git checkout -b feature/issue-123-add-email-validation
```

Branch naming conventions:

- `fix/issue-NUM-description` - Bug fixes
- `feature/issue-NUM-description` - New features
- `docs/issue-NUM-description` - Documentation
- `test/issue-NUM-description` - Test improvements

### Make Changes

Best practices:

1. **Small, focused commits** - One logical change per commit
2. **Good commit messages** - Describe what and why
3. **Follow project style** - Match existing code style
4. **Add comments** - Explain complex logic
5. **Update docs** - Keep documentation current

### Commit Messages

Good commit message format:

```
Fix authentication bug with special characters

- Add email validation before authentication
- Handle special characters in email addresses
- Add isValidEmail() utility function

Fixes #123
```

Structure:

- **First line**: Brief summary (50 chars or less)
- **Blank line**
- **Body**: Detailed explanation
- **Footer**: Issue references

## Step 5: Test Changes

### Run Existing Tests

```bash
# Node.js
npm test
npm run test:unit
npm run test:integration

# Python
pytest
python -m pytest tests/
pytest -v

# Go
go test ./...
go test -v ./...

# Rust
cargo test
cargo test --all

# Ruby
bundle exec rspec
rake test
```

### Add New Tests

For bugs:

- Test that reproduces the bug
- Test that validates the fix
- Test edge cases

For features:

- Test happy path
- Test error conditions
- Test edge cases
- Test integration with existing code

### Manual Testing

If applicable:

1. Run the application locally
2. Test the specific feature/fix
3. Verify no regressions
4. Test in different scenarios

### Test Checklist

- [ ] All existing tests pass
- [ ] New tests added for changes
- [ ] New tests pass
- [ ] Manual testing completed (if applicable)
- [ ] No new warnings or errors
- [ ] Code coverage maintained or improved

## Step 6: Create Pull Request

### Push Your Branch

```bash
# Push branch to your fork or origin
git push origin fix/issue-123-auth-bug

# If pushing for first time
git push -u origin fix/issue-123-auth-bug
```

### Create PR Using Script

```bash
python scripts/create_pr.py '{
  "owner": "username",
  "repo": "repository",
  "title": "Fix: Handle special characters in email validation",
  "head_branch": "fix/issue-123-auth-bug",
  "base_branch": "main",
  "issue_number": 123,
  "summary": "Fixed bug where special characters in email addresses caused authentication to fail.",
  "changes": [
    "Added email validation before authentication",
    "Created isValidEmail() utility function",
    "Added comprehensive test coverage for email validation",
    "Updated documentation with new validation rules"
  ],
  "testing": [
    "All existing tests pass",
    "Added 5 new test cases for email validation",
    "Manually tested with various email formats",
    "Verified no regressions in authentication flow"
  ]
}'
```

### PR Best Practices

1. **Link to issue**: Use "Fixes #123" or "Closes #123"
2. **Clear description**: Explain what and why
3. **List changes**: Bullet points of modifications
4. **Show testing**: How you verified it works
5. **Add screenshots**: If UI changes
6. **Request review**: Tag relevant reviewers
7. **Keep it focused**: One issue per PR

### PR Title Guidelines

Good titles:

- `Fix: Authentication fails with special characters (#123)`
- `Feature: Add email validation to auth flow (#123)`
- `Docs: Update authentication documentation (#123)`
- `Test: Add coverage for email validation (#123)`

Bad titles:

- `Fix bug`
- `Update code`
- `Changes`

### After Creating PR

1. **Watch for CI/CD**: Ensure automated tests pass
2. **Respond to feedback**: Address review comments promptly
3. **Keep updated**: Rebase if main branch changes
4. **Be patient**: Reviews take time

## Common Workflows

### Simple Bug Fix

```bash
# 1. Fetch issue
python scripts/fetch_issue.py owner/repo#123

# 2. Clone and analyze
git clone https://github.com/owner/repo.git
cd repo
python scripts/analyze_repository.py .

# 3. Create branch
git checkout -b fix/issue-123-bug-description

# 4. Make changes
# ... edit files ...
git add .
git commit -m "Fix: Bug description

Detailed explanation.

Fixes #123"

# 5. Test
npm test  # or appropriate test command

# 6. Push
git push origin fix/issue-123-bug-description

# 7. Create PR
python scripts/create_pr.py '{...config...}'
```

### Feature Implementation

```bash
# 1-2. Same as bug fix

# 3. Create feature branch
git checkout -b feature/issue-123-feature-name

# 4. Implement in small commits
git commit -m "Add basic structure"
git commit -m "Implement core functionality"
git commit -m "Add tests"
git commit -m "Update documentation"

# 5-7. Same as bug fix
```

## Troubleshooting

### Issue Not Loading

- Check GitHub token (rate limits)
- Verify issue number and repository
- Check repository visibility (public/private)

### Tests Failing

- Read test output carefully
- Run tests locally before pushing
- Check if test environment setup needed
- Look for unrelated failures (flaky tests)

### PR Creation Fails

- Verify GitHub token has correct permissions
- Check branch names (no typos)
- Ensure commits are pushed
- Verify base branch exists

### Merge Conflicts

```bash
# Update your branch with latest main
git fetch origin
git checkout main
git pull origin main
git checkout your-branch
git rebase main

# Resolve conflicts
# ... edit files ...
git add .
git rebase --continue

# Force push (rewrites history)
git push -f origin your-branch
```

## Tips for Success

1. **Start small**: Begin with good first issues
2. **Communicate**: Ask questions in issue comments
3. **Follow conventions**: Match project style and patterns
4. **Test thoroughly**: Better to over-test than under-test
5. **Document well**: Help reviewers understand changes
6. **Be responsive**: Address feedback quickly
7. **Learn from reviews**: Improve with each PR

## GitHub API Rate Limits

Without token: 60 requests/hour
With token: 5,000 requests/hour

Always use a token for development:

```bash
export GITHUB_TOKEN=ghp_yourtoken
```

Or provide in scripts:

```bash
python scripts/fetch_issue.py owner/repo#123 ghp_yourtoken
```
