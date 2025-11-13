---
name: github-issue-resolver
description: Complete workflow for resolving GitHub issues - fetch and analyze issues, understand codebase, implement fixes/features, write tests, and create professional pull requests. Use when working with GitHub repositories to (1) Analyze and understand issues, (2) Locate relevant code in repositories, (3) Implement bug fixes or new features, (4) Write appropriate tests, (5) Create well-documented pull requests with proper formatting and best practices. Includes scripts for GitHub API interaction and comprehensive guides for contribution workflow.
---

# GitHub Issue Resolver

Complete toolkit for resolving GitHub issues from initial analysis to pull request submission.

## Related Skills

**Use with:** `qa-github-manager` - For intake and structuring of client feedback into GitHub issues. This resolver skill handles the implementation and PR creation workflow.

## When to Use This Skill

**Use github-issue-resolver when:**
- ✅ You have an existing GitHub issue to resolve
- ✅ Fetching and analyzing issue details from GitHub API
- ✅ Analyzing repository structure to locate relevant code
- ✅ Implementing bug fixes or new features
- ✅ Writing tests for your implementation
- ✅ Creating professional pull requests

**Use qa-github-manager instead when:**
- ❌ Receiving raw, unstructured client feedback
- ❌ Need to parse and structure feedback first
- ❌ Breaking complex feedback into multiple issues
- ❌ Searching for duplicate issues
- ❌ Creating new GitHub issues from scratch

**Workflow:** qa-github-manager (intake) → GitHub Issues → github-issue-resolver (implementation)

## Quick Start

### 1. Fetch and Analyze Issue

```bash
# Fetch issue details from GitHub
python scripts/fetch_issue.py owner/repo#123

# Or with full URL
python scripts/fetch_issue.py https://github.com/owner/repo/issues/123

# With GitHub token (recommended for rate limits)
python scripts/fetch_issue.py owner/repo#123 ghp_yourtoken
```

Returns comprehensive issue analysis:

- Issue metadata (title, labels, author, dates)
- Type detection (bug, feature, docs, test)
- Complexity estimate
- Files mentioned in issue
- Related issues
- Comments from maintainers

### 2. Analyze Repository

```bash
# Clone repository
git clone https://github.com/owner/repo.git
cd repo

# Analyze structure
python scripts/analyze_repository.py .

# Search for specific patterns
python scripts/analyze_repository.py . "functionName"
```

Provides:

- Project type detection (Node.js, Python, Go, etc.)
- Framework identification (React, Django, Express, etc.)
- File organization and structure
- Test setup and locations
- Configuration files

### 3. Implement Solution

Create feature branch:

```bash
git checkout -b fix/issue-123-description
```

Make changes following project conventions, then commit:

```bash
git add .
git commit -m "fix: Brief description

Detailed explanation of what and why.

Fixes #123"
```

### 4. Test Changes

```bash
# Run existing tests
npm test  # or pytest, go test, cargo test, etc.

# Add new tests for your changes
# Run tests again to verify
```

### 5. Create Pull Request

```bash
# Push branch
git push origin fix/issue-123-description

# Create PR via script
python scripts/create_pr.py '{
  "owner": "username",
  "repo": "repository",
  "title": "fix: Brief description of fix",
  "head_branch": "fix/issue-123-description",
  "issue_number": 123,
  "summary": "Fixed the bug by...",
  "changes": ["Added validation", "Updated tests"],
  "testing": ["All tests pass", "Manually tested edge cases"]
}'
```

## Complete Workflow

### Step 1: Understand the Issue

Read the issue carefully and identify:

- **Problem**: What is broken or missing?
- **Expected behavior**: What should happen?
- **Reproduction**: How to reproduce the issue?
- **Scope**: Which files/components are affected?
- **Related issues**: Are there similar problems?

### Step 2: Analyze Codebase

Use `analyze_repository.py` to understand:

- Project structure and organization
- Programming language and framework
- Test setup and conventions
- Where related code likely exists

Search for mentioned functions, classes, or files:

```bash
python scripts/analyze_repository.py /path/to/repo "mentioned_function"
```

### Step 3: Plan Solution

Document your approach:

- Which files need changes
- What the changes will be
- How to test the changes
- Any breaking changes or considerations

For bugs: Understand root cause before fixing
For features: Design API and integration points

### Step 4: Implement Changes

**Branch naming:**

- `fix/issue-NUM-description` - Bug fixes
- `feature/issue-NUM-description` - New features
- `docs/issue-NUM-description` - Documentation
- `test/issue-NUM-description` - Test improvements

**Commit practices:**

- Small, focused commits
- Clear commit messages (see templates)
- Reference issue number
- One logical change per commit

### Step 5: Write Tests

**For bug fixes:**

- Test that reproduces the bug (should fail before fix)
- Test that validates the fix (should pass after)
- Test edge cases

**For features:**

- Test happy path
- Test error conditions
- Test edge cases
- Test integration with existing code

### Step 6: Create Pull Request

Use `create_pr.py` to generate well-formatted PR:

- Clear title following conventions
- Comprehensive description
- Links to related issues
- List of changes
- Testing information
- Screenshots if applicable

## Scripts Reference

### fetch_issue.py

Fetches issue details from GitHub API and analyzes content.

**Usage:**

```bash
python scripts/fetch_issue.py owner/repo#123 [token]
```

**Output includes:**

- Issue metadata (number, title, URL, state, labels)
- Author and timestamps
- Full issue body
- Type detection (bug/feature/docs/test)
- Complexity estimate
- Files mentioned in issue
- Related issue references
- First 10 comments

**Environment:**
Set `GITHUB_TOKEN` environment variable to avoid rate limits:

```bash
export GITHUB_TOKEN=ghp_yourtoken
```

### analyze_repository.py

Analyzes repository structure and helps locate relevant code.

**Usage:**

```bash
python scripts/analyze_repository.py /path/to/repo [search_pattern]
```

**Provides:**

- Total files and file type breakdown
- Programming languages detected
- Project type (Node.js, Python, Rust, etc.)
- Framework detection (React, Django, etc.)
- Main directories
- Test files and directories
- Configuration files
- Pattern search results (if pattern provided)

### create_pr.py

Creates pull request via GitHub API with proper formatting.

**Usage:**

```bash
python scripts/create_pr.py '<config_json>'
```

**Config format:**

```json
{
  "owner": "username",
  "repo": "repository",
  "title": "fix: Description",
  "head_branch": "fix/issue-123",
  "base_branch": "main",
  "issue_number": 123,
  "summary": "What this PR does",
  "changes": ["Change 1", "Change 2"],
  "testing": ["Test info"],
  "token": "ghp_token"
}
```

**Generates:**

- Professional PR description
- Fixes #NUM reference
- Changes checklist
- Testing information
- Standard PR checklist

## Reference Documentation

### Complete Workflow Guide

**references/github-workflow.md** - Comprehensive guide covering:

- Fetching and analyzing issues
- Cloning and analyzing repositories
- Planning solutions (bugs vs features)
- Implementation best practices
- Testing strategies
- PR creation and submission
- Common workflows and troubleshooting

### PR Best Practices

**references/pr-best-practices.md** - Guide to creating great PRs:

- PR title conventions (conventional commits)
- Description templates and examples
- Commit message guidelines
- Code review response strategies
- PR size recommendations
- Documentation requirements
- Common mistakes to avoid
- Examples of great PRs

### Testing Strategies

**references/testing-strategies.md** - Testing guide:

- Test types (unit, integration, e2e)
- Running tests in different languages
- Test-Driven Development (TDD)
- Edge cases to cover
- Writing good tests
- Manual testing approaches
- Coverage goals
- Testing checklist

## Templates

### PR Description Template

**assets/templates/pr-template.md** - Copy-paste PR template with:

- Description section
- Type of change checkboxes
- Changes list
- Testing information
- Screenshots section
- Checklist items
- Related issues/PRs

### Commit Message Template

**assets/templates/commit-message-template.txt** - Guidelines for commits:

- Conventional commit format
- Type descriptions (feat, fix, docs, etc.)
- Subject line rules
- Body formatting
- Footer conventions
- Good and bad examples

## Common Issue Types

### Bug Fixes

1. Fetch issue to understand the bug
2. Locate the buggy code
3. Write test that reproduces bug (should fail)
4. Fix the bug
5. Verify test passes
6. Add edge case tests
7. Create PR

**Example:**

```bash
python scripts/fetch_issue.py owner/repo#123
git clone https://github.com/owner/repo.git
cd repo
python scripts/analyze_repository.py . "buggy_function"
# ... make changes ...
npm test
git commit -m "fix: Handle null input in buggy_function

Fixes #123"
```

### Feature Implementation

1. Understand requirements from issue
2. Analyze how feature fits into codebase
3. Design the implementation
4. Implement in small commits
5. Add comprehensive tests
6. Update documentation
7. Create PR

**Branch naming:**

```bash
git checkout -b feature/issue-456-add-pagination
```

### Documentation Updates

1. Identify what needs documentation
2. Find existing docs structure
3. Write clear, concise documentation
4. Add code examples
5. Update table of contents if needed
6. Create PR

**Commit:**

```bash
git commit -m "docs: Add examples for authentication

Added usage examples for:
- Basic authentication
- OAuth integration
- Custom auth providers

Closes #789"
```

## Best Practices

### Before Starting

- Read issue carefully multiple times
- Check for related issues/PRs
- Understand project conventions
- Review CONTRIBUTING.md if it exists

### During Implementation

- Keep changes focused and minimal
- Follow existing code style
- Add comments for complex logic
- Commit frequently with clear messages
- Run tests often

### Before Submitting PR

- All tests pass locally
- Code follows project style
- Documentation updated
- Self-review completed
- Branch up to date with main
- No debug code or commented-out code

### After Creating PR

- Respond to CI/CD failures promptly
- Address review feedback quickly
- Be polite and professional
- Keep PR updated with main branch

## Troubleshooting

**Issue fetch fails:**

- Check GitHub token (rate limits without token)
- Verify issue exists and is public
- Check repository name spelling

**Repository analysis slow:**

- Exclude large directories (already handled)
- Limit search depth for large repos
- Use specific search patterns

**Tests failing:**

- Read error messages carefully
- Check test environment setup
- Verify dependencies installed
- Look for flaky tests

**PR creation fails:**

- Verify GitHub token permissions
- Check branch names (no typos)
- Ensure commits are pushed
- Verify base branch exists

## GitHub Token Setup

Get a personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Copy token

Set as environment variable:

```bash
export GITHUB_TOKEN=ghp_yourtoken

# Or add to ~/.bashrc or ~/.zshrc
echo 'export GITHUB_TOKEN=ghp_yourtoken' >> ~/.bashrc
```

## Integration with Git

Set up git commit template:

```bash
git config --global commit.template assets/templates/commit-message-template.txt
```

Now `git commit` will open editor with template.

## Tips for Success

1. **Start small** - Look for "good first issue" labels
2. **Communicate** - Ask questions in issue comments
3. **Follow conventions** - Match existing code style
4. **Test thoroughly** - Over-test rather than under-test
5. **Document clearly** - Help reviewers understand changes
6. **Be patient** - Reviews take time
7. **Learn from feedback** - Use reviews to improve

## Example Workflow

Complete example:

```bash
# 1. Fetch and understand issue
python scripts/fetch_issue.py facebook/react#12345 $GITHUB_TOKEN

# 2. Clone and analyze repo
git clone https://github.com/facebook/react.git
cd react
python scripts/analyze_repository.py . "useState"

# 3. Create feature branch
git checkout -b fix/issue-12345-usestate-bug

# 4. Read relevant files
cat packages/react/src/ReactHooks.js
cat packages/react-reconciler/src/ReactFiberHooks.js

# 5. Make changes
# ... edit files ...

# 6. Add tests
# ... add test files ...

# 7. Run tests
npm test

# 8. Commit changes
git add .
git commit -m "fix(hooks): Prevent crash in useState with null initial value

The useState hook crashed when provided with null as initial value
in certain edge cases. Added proper null handling.

Fixes #12345"

# 9. Push branch
git push origin fix/issue-12345-usestate-bug

# 10. Create PR
python scripts/create_pr.py '{
  "owner": "facebook",
  "repo": "react",
  "title": "fix(hooks): Prevent crash in useState with null initial value",
  "head_branch": "fix/issue-12345-usestate-bug",
  "issue_number": 12345,
  "summary": "Fixed crash when useState receives null initial value",
  "changes": [
    "Added null check in useState implementation",
    "Added tests for null initial value",
    "Updated hooks documentation"
  ],
  "testing": [
    "All 1,247 existing tests pass",
    "Added 3 new tests for null handling",
    "Manually tested with example app"
  ],
  "token": "'$GITHUB_TOKEN'"
}'
```

This workflow ensures a professional contribution from start to finish.
