## Implementation Workflow

Complete workflow for taking a GitHub issue from analysis to pull request.

## Overview

```
GitHub Issue
     ↓
[1. Analyze Issue]
     ↓
[2. Plan Implementation]
     ↓
[3. Set Up Environment]
     ↓
[4. Implement Solution]
     ↓
[5. Test Thoroughly]
     ↓
[6. Create Pull Request]
     ↓
[7. Code Review & Iterate]
```

## Step 1: Analyze the Issue

### Read Thoroughly

**What to look for:**

- Issue type (bug/feature/enhancement)
- Reproduction steps (for bugs)
- Acceptance criteria
- Technical details
- Related issues
- Labels and priority

**Use analyzer:**

```bash
python scripts/analyze_issue.py '<issue_json>'
```

**Extract:**

- ✅ Clear problem statement
- ✅ Expected vs actual behavior
- ✅ Environment details
- ✅ Files mentioned
- ✅ Proposed solutions
- ✅ Dependencies

### Ask Clarifying Questions

**If unclear, ask:**

- What's the expected behavior?
- In what environment does this occur?
- Can you provide more details on [X]?
- Is this related to issue #[Y]?
- What's the priority/deadline?

**Add comments to issue:**

```markdown
## Clarification Questions

Before starting implementation, I need clarity on:

1. [Question 1]
2. [Question 2]

This will help ensure the fix addresses the root cause.
```

### Document Understanding

**Create analysis document:**

```markdown
# Issue #123 Analysis

## Problem

[Clear problem statement]

## Root Cause

[What's causing the issue]

## Proposed Solution

[How to fix it]

## Affected Components

- Component A
- Component B

## Dependencies

- Depends on #456
- Blocks #789
```

## Step 2: Plan Implementation

### Break Down into Steps

**Use planner:**

```bash
python scripts/implementation_planner.py '<analysis_json>'
```

**Create detailed plan:**

1. Step-by-step approach
2. Files to modify
3. Dependencies between steps
4. Testing strategy
5. Time estimate

### Consider Architecture

**Ask yourself:**

- Does this require refactoring?
- Will this affect other components?
- Are there performance implications?
- Does this change any APIs?
- Will this need migration?

### Identify Risks

**Common risks:**

- Breaking changes
- Performance regression
- Security implications
- Data migration needed
- Third-party dependencies

## Step 3: Set Up Environment

### Branch Strategy

**Create feature branch:**

```bash
git checkout -b fix/issue-123-login-button
# or
git checkout -b feat/issue-123-export-csv
```

**Branch naming:**

- `fix/issue-N-short-description` for bugs
- `feat/issue-N-short-description` for features
- `refactor/issue-N-short-description` for enhancements

### Reproduce the Issue (for bugs)

**Follow reproduction steps exactly:**

1. Set up test environment
2. Follow steps from issue
3. Confirm bug exists
4. Document any differences

**If can't reproduce:**

- Check environment differences
- Ask for more details
- Try different scenarios
- Document attempts

### Set Up Tests

**Create failing test first (TDD):**

```python
def test_issue_123_login_button_works():
    """Test for issue #123: Login button not responding"""
    # Setup
    page = setup_login_page()

    # Action
    page.click_login_button()

    # Assert
    assert page.is_logged_in()  # Currently fails
```

## Step 4: Implement Solution

### Start with Smallest Change

**Principle:** Make the smallest change that fixes the issue.

**Good approach:**

```python
# Minimal fix
def login(credentials):
    if not credentials:
        raise ValueError("Credentials required")  # Add validation
    return authenticate(credentials)
```

**Avoid:**

```python
# Over-engineering
def login(credentials, options=None, retry_count=3, timeout=30, ...):
    # Too many changes at once
```

### Follow the Plan

**Work through steps sequentially:**

```
✅ Step 1: Reproduce bug
✅ Step 2: Identify root cause
⏳ Step 3: Write failing test
⬜ Step 4: Implement fix
⬜ Step 5: Verify fix
⬜ Step 6: Test regression
```

**Track progress:**

- Update issue with progress
- Commit after each step
- Note any deviations from plan

### Write Clean Code

**Best practices:**

- Follow project style guide
- Add comments for complex logic
- Use meaningful variable names
- Keep functions small and focused
- Don't repeat yourself (DRY)

### Commit Frequently

**Good commit messages:**

```bash
git commit -m "Add failing test for issue #123"
git commit -m "Identify root cause in auth.js"
git commit -m "Fix login button event handler"
git commit -m "Verify fix resolves issue #123"
```

**Conventional commits:**

```bash
git commit -m "fix: resolve login button not responding (#123)"
git commit -m "test: add regression test for issue #123"
git commit -m "docs: update login documentation"
```

## Step 5: Test Thoroughly

### Run Tests Locally

**Test levels:**

```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# Full suite
npm run test:all
```

### Verify Acceptance Criteria

**Check each criterion:**

- [ ] Criterion 1: Login button responds to clicks
- [ ] Criterion 2: User is redirected after login
- [ ] Criterion 3: Error messages display correctly

### Test Edge Cases

**Consider:**

- Null/undefined inputs
- Empty strings
- Very large inputs
- Concurrent operations
- Network failures
- Slow connections

### Manual Testing

**For bugs:**

1. Follow original reproduction steps
2. Verify bug is fixed
3. Test on same environment
4. Test on different environments

**For features:**

1. Test happy path
2. Test error scenarios
3. Test edge cases
4. Verify UI/UX
5. Test accessibility

### Performance Testing

**If relevant:**

```javascript
console.time('operation')
performOperation()
console.timeEnd('operation')
```

**Check for:**

- Memory leaks
- Slow queries
- Blocking operations
- Large payload sizes

### Check for Regression

**Run full test suite:**

```bash
npm test
```

**Manual checks:**

- Related features still work
- No new errors in console
- No broken UI elements
- No performance degradation

## Step 6: Create Pull Request

### Format PR Description

**Use formatter:**

```bash
python scripts/pr_formatter.py '<analysis>' '<plan>' 'Summary of changes'
```

### Write Comprehensive Description

**Template:**

```markdown
## Description

Closes #123

Brief summary of what was changed and why.

## Changes Made

- Change 1: Description
- Change 2: Description

## Testing

- [x] Unit tests added
- [x] Integration tests pass
- [x] Manual testing completed

## Screenshots

[If UI changes]

## Checklist

- [x] Code follows style guide
- [x] Tests added/updated
- [x] Documentation updated
```

### Link to Issue

**Always include:**

```markdown
Closes #123
```

**Or:**

```markdown
Fixes #123
Resolves #123
```

### Add Context

**Help reviewers by including:**

- Why this approach was chosen
- Alternative approaches considered
- Any tradeoffs made
- Areas that need special attention

### Request Specific Feedback

```markdown
## Questions for Reviewers

1. Is the error handling sufficient?
2. Should we add more logging?
3. Any concerns about performance?
```

## Step 7: Code Review & Iterate

### Respond to Feedback

**Good responses:**

```markdown
> Should we add validation here?

Good catch! Added validation in commit abc123.
```

**If disagree:**

```markdown
> This seems overly complex

I understand the concern. The complexity is needed because [reason].
However, I've added comments to explain the logic. Open to alternative approaches.
```

### Make Requested Changes

**Commit changes:**

```bash
git commit -m "Address review feedback: add validation"
git push
```

**Update PR:**

```markdown
## Updates

- Added validation per @reviewer's suggestion
- Simplified logic in AuthService
- Added more test cases
```

### Re-test After Changes

**Always verify:**

- Tests still pass
- No new issues introduced
- Feedback addressed completely

### Squash if Needed

**Before merge (if required):**

```bash
git rebase -i main
# Squash commits
# Force push
git push --force-with-lease
```

## Best Practices

### Do

✅ Read issue completely before starting  
✅ Ask clarifying questions  
✅ Create detailed implementation plan  
✅ Write tests first (TDD)  
✅ Commit frequently with good messages  
✅ Test thoroughly  
✅ Write comprehensive PR description  
✅ Respond professionally to feedback

### Don't

❌ Start coding without understanding issue  
❌ Skip writing tests  
❌ Make unrelated changes  
❌ Ignore edge cases  
❌ Forget to update documentation  
❌ Create huge PRs  
❌ Take feedback personally  
❌ Merge without approval

## Time Management

### Estimate Realistically

**Consider:**

- Understanding issue: 10-20%
- Planning: 10-15%
- Implementation: 40-50%
- Testing: 20-30%
- PR & review: 10-15%

**Example: 1-day bug fix**

- Analyze: 1 hour
- Plan: 1 hour
- Implement: 3 hours
- Test: 2 hours
- PR: 1 hour

### Track Time

**Document:**

- Time spent understanding issue
- Blockers encountered
- Actual vs estimated time

**Learn from:**

- What took longer than expected?
- What was easier than expected?
- How to improve estimates?

## Common Pitfalls

### Pitfall 1: Not Understanding Issue

**Problem:** Start coding before fully understanding  
**Solution:** Spend time analyzing, ask questions

### Pitfall 2: Scope Creep

**Problem:** Fix other issues while working  
**Solution:** Stay focused, create separate issues

### Pitfall 3: Insufficient Testing

**Problem:** Only test happy path  
**Solution:** Test edge cases, errors, regression

### Pitfall 4: Poor Communication

**Problem:** Silent for days, then huge PR  
**Solution:** Update issue, commit frequently, communicate blockers

### Pitfall 5: Ignoring Feedback

**Problem:** Defensive about code review  
**Solution:** View feedback as learning, collaborate

## Checklist

Use this for every issue:

**Before Starting:**

- [ ] Issue fully understood
- [ ] Clarifying questions asked and answered
- [ ] Implementation plan created
- [ ] Branch created
- [ ] Can reproduce bug (if applicable)

**During Implementation:**

- [ ] Following the plan
- [ ] Writing clean, maintainable code
- [ ] Committing frequently
- [ ] Adding tests as you go
- [ ] Updating documentation

**Before Creating PR:**

- [ ] All tests passing
- [ ] Acceptance criteria met
- [ ] Edge cases handled
- [ ] No regression
- [ ] Code self-reviewed
- [ ] Documentation updated

**After PR Created:**

- [ ] Comprehensive description
- [ ] Linked to issue
- [ ] Requested reviewers
- [ ] Responded to feedback
- [ ] Made requested changes
- [ ] Tests still passing

**After Merge:**

- [ ] Issue closed automatically
- [ ] Verified in staging/production
- [ ] Celebrated success! 🎉

This workflow ensures high-quality implementations from issue to merged PR.
