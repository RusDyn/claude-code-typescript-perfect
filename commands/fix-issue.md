# Fix GitHub Issue: $ARGUMENTS

## Pre-Fix Verification

1. **Fetch Issue Details**
   ```
   Use github mcp to get issue #[NUMBER]:
   - Read full description
   - Check comments for additional context
   - Note acceptance criteria
   - Review linked PRs
   ```

2. **Reproduce Issue**
   - Locate the code mentioned
   - Verify the issue still exists
   - Create failing test if applicable

## Implementation Process

1. **Create Feature Branch**
   ```bash
   git checkout -b fix/issue-[NUMBER]-brief-description
   ```

2. **Implement Fix**
   - Follow patterns in CLAUDE.md
   - Use Result<T,E> for error handling
   - Add comprehensive tests
   - Update documentation

3. **Validation**
   - Run `npm run quality`
   - Ensure all tests pass
   - Check no new issues introduced

## GitHub Integration

1. **Create Pull Request**
   Use github mcp to:
   - Create PR with title: "Fix #[NUMBER]: [Issue Title]"
   - Link to issue automatically
   - Add description with:
     - What was broken
     - How it was fixed
     - How to test
   - Request reviewers

2. **Update Issue**
   - Add comment: "PR #[PR_NUMBER] addresses this issue"
   - Add label: "in-review"
   - Link PR to issue

## Post-Merge Actions

1. **Verify Deployment**
   - Confirm fix in staging
   - Run smoke tests

2. **Close Issue**
   - Add final comment with verification
   - Close with message: "Fixed in #[PR_NUMBER]"
   - Remove "in-review" label
   - Add "resolved" label