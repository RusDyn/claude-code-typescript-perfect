---
name: github-issue-resolver
description: Take an opened GitHub issue, study it carefully, implement or fix the issue, and create a PR. Use when working on GitHub issues to (1) Analyze and understand issue requirements thoroughly, (2) Create detailed implementation plans with steps, (3) Implement solutions following best practices, (4) Write comprehensive tests, (5) Create well-formatted pull requests that link to issues. Handles bugs, features, and enhancements with proper testing strategies and PR descriptions.
---

# GitHub Issue Resolver

Transform GitHub issues into implemented solutions with comprehensive pull requests.

## When to Use This Skill

Use github-issue-resolver when you need to:

- **Implement solutions** for existing GitHub issues
- **Fix bugs** described in issue tickets
- **Add features** requested in issue tickets
- **Create implementation plans** from issue requirements
- **Write comprehensive tests** for issue fixes
- **Generate PR descriptions** that properly link to issues
- **Follow development workflow** from issue analysis to PR creation

## When NOT to Use This Skill

**DO NOT use github-issue-resolver for:**

- **Creating or managing issues** → Use `qa-github-manager` skill instead
- **Processing client feedback** → Use `qa-github-manager` to create issues first
- **Reviewing PRs** → Use standard code review processes
- **Deployment or DevOps** → Use appropriate deployment tools
- **Database schema design** → This skill focuses on implementation, not architecture

**Clear separation:**

- `qa-github-manager` = Feedback → Issues (creates and manages issues)
- `github-issue-resolver` = Issue → Implementation → PR (implements solutions)

## Quick Start

### 1. Analyze the Issue

Extract all requirements and context from a GitHub issue:

```bash
python scripts/analyze_issue.py '<issue_json>'
```

**Output:** Complete analysis with acceptance criteria, technical details, affected files, and testing requirements.

### 2. Create Implementation Plan

Generate step-by-step implementation plan:

```bash
python scripts/implementation_planner.py '<analysis_json>'
```

**Output:** Detailed plan with steps, dependencies, time estimates, and testing strategy.

### 3. Create PR Description

Format comprehensive pull request:

```bash
python scripts/pr_formatter.py '<analysis_json>' '<plan_json>' 'Summary of changes'
```

**Output:** Well-formatted PR description with proper linking and context.

## Complete Workflow

### Step 1: Study the Issue

**Read thoroughly:**

- Issue type (bug/feature/enhancement)
- Problem statement
- Reproduction steps (bugs)
- Acceptance criteria
- Related issues
- Labels and priority

**Use analyzer:**

- Extracts structured information
- Identifies technical details
- Finds affected files
- Lists testing requirements

**Ask questions if unclear:**

- What's the expected behavior?
- What environment does this affect?
- Are there any constraints?
- What's the priority?

### Step 2: Plan Implementation

**Create detailed plan:**

1. Break down into sequential steps
2. Identify files to modify
3. Note dependencies between steps
4. Plan testing strategy
5. Estimate effort

**Consider:**

- Architecture implications
- Performance impact
- Breaking changes
- Security considerations
- Documentation needs

### Step 3: Set Up Environment

**Create branch:**

```bash
git checkout -b fix/issue-123-login-button
# or
git checkout -b feat/issue-456-csv-export
```

**Reproduce bug (if applicable):**

- Follow reproduction steps
- Confirm issue exists
- Document findings

**Write failing test first:**

```javascript
test('issue #123: login button should respond', () => {
  // This test should fail initially
  expect(loginButton.works()).toBe(true)
})
```

### Step 4: Implement Solution

**Follow TDD approach:**

1. Write failing test
2. Write minimal code to pass
3. Refactor and improve
4. Repeat

**Best practices:**

- Keep changes focused
- Commit frequently
- Follow style guide
- Add comments for complex logic
- Handle edge cases
- Add error handling

**Good commit messages:**

```bash
git commit -m "Add failing test for issue #123"
git commit -m "Fix login button event handler"
git commit -m "Add error handling and edge cases"
```

### Step 5: Test Thoroughly

**Testing levels:**

```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# Manual testing
npm run dev
```

**Verify:**

- All tests passing
- Acceptance criteria met
- Edge cases handled
- No regression
- Performance acceptable

**Test checklist:**

- [ ] Unit tests for new code
- [ ] Integration tests for workflows
- [ ] Manual testing completed
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] No console errors
- [ ] Works on target browsers/devices

### Step 6: Create Pull Request

**Format PR description:**

- Use proper title format: `type(scope): description (#issue)`
- Link to issue: `Closes #123`
- Explain problem and solution
- List changes made
- Document testing performed
- Add screenshots if UI changes
- Include checklist

**Quality checklist:**

- [ ] Code follows style guide
- [ ] Self-review completed
- [ ] Comments added
- [ ] Tests comprehensive
- [ ] Documentation updated
- [ ] CI passing
- [ ] No merge conflicts

### Step 7: Respond to Review

**Handle feedback professionally:**

- Thank reviewers
- Address all comments
- Explain decisions clearly
- Make requested changes
- Re-test after changes
- Update PR description if needed

## Issue Types & Strategies

### Bug Fixes

**Analysis focus:**

- Reproduction steps
- Expected vs actual behavior
- Environment details
- Error messages
- Stack traces

**Implementation approach:**

1. Reproduce bug
2. Write failing test
3. Identify root cause
4. Fix minimal code
5. Verify fix
6. Check regression

**Testing strategy:**

- Test reproduces bug
- Test verifies fix
- Test edge cases
- Regression tests

### New Features

**Analysis focus:**

- User stories
- Acceptance criteria
- Use cases
- API/UI requirements

**Implementation approach:**

1. Design architecture
2. Write tests (TDD)
3. Implement core
4. Add UI/API
5. Handle edge cases
6. Add documentation

**Testing strategy:**

- Unit tests for logic
- Integration tests for flow
- E2E tests for journey
- Acceptance criteria tests

### Enhancements

**Analysis focus:**

- Current behavior
- Desired improvement
- Success metrics
- Performance targets

**Implementation approach:**

1. Baseline measurement
2. Implement improvement
3. Measure results
4. Add tests
5. Verify no regression

**Testing strategy:**

- Performance tests
- Before/after comparison
- Regression tests
- Quality verification

## Best Practices

### Code Quality

**Do:**
✅ Follow project conventions  
✅ Write clean, readable code  
✅ Add meaningful comments  
✅ Handle errors properly  
✅ Consider edge cases  
✅ Keep functions small  
✅ Use descriptive names

**Don't:**
❌ Include debug code  
❌ Leave commented code  
❌ Make unrelated changes  
❌ Skip error handling  
❌ Ignore edge cases  
❌ Write complex functions  
❌ Use vague names

### Testing

**Required:**

- Unit tests for all new code
- Integration tests for workflows
- Regression tests for bugs
- Manual testing documented

**Quality:**

- 80%+ code coverage
- All acceptance criteria verified
- Edge cases tested
- Error scenarios handled

### Pull Requests

**Title format:**

```
fix(auth): resolve login button not responding (#123)
feat(reports): add CSV export functionality (#456)
refactor(api): improve error handling (#789)
```

**Description includes:**

- Problem statement
- Solution explanation
- Changes made
- Testing performed
- Screenshots (if UI)
- Breaking changes (if any)

## Reference Documentation

**references/implementation-workflow.md** - Complete workflow from issue to PR:

- Detailed step-by-step process
- Decision points and best practices
- Common pitfalls and solutions
- Time management and estimation
- Comprehensive checklists

**references/pr-best-practices.md** - Excellent PR creation:

- PR title and description guidelines
- Optimal PR size and scope
- Code quality standards
- Responding to feedback
- Merge strategies

**references/testing-guide.md** - Comprehensive testing:

- Unit, integration, E2E testing
- Test-driven development approach
- Testing by issue type
- Testing tools and setup
- Quality metrics

## Templates

**assets/templates/pr-description.md** - Complete PR template with all sections

**assets/templates/implementation-checklist.md** - Full implementation checklist from analysis to merge

## Common Scenarios

### Scenario 1: Simple Bug Fix

**Issue:** Login button doesn't work on mobile

**Workflow:**

1. Analyze: Extract reproduction steps
2. Plan: 6 steps - reproduce, debug, test, fix, verify, regression
3. Implement: Fix z-index issue
4. Test: Add test, verify fix, check regression
5. PR: Link issue, explain problem/solution
6. Estimate: 2-4 hours

### Scenario 2: New Feature

**Issue:** Add CSV export to reports

**Workflow:**

1. Analyze: Extract user stories and acceptance criteria
2. Plan: 7 steps - design, tests, core, UI, edge cases, docs, verify
3. Implement: Build export functionality
4. Test: TDD approach with comprehensive coverage
5. PR: Full description with usage examples
6. Estimate: 1-2 days

### Scenario 3: Performance Enhancement

**Issue:** Improve dashboard load time

**Workflow:**

1. Analyze: Current vs target performance
2. Plan: Baseline, optimize, measure, test, verify
3. Implement: Add caching and lazy loading
4. Test: Performance tests, regression tests
5. PR: Include before/after metrics
6. Estimate: 4-8 hours

## Troubleshooting

**Can't reproduce bug:**

- Check environment differences
- Verify all reproduction steps
- Ask for more details
- Try different scenarios

**Unclear requirements:**

- Ask clarifying questions on issue
- Don't assume - document assumptions
- Propose solution for feedback
- Get approval before major changes

**Tests failing:**

- Read error messages carefully
- Check test environment
- Verify test data
- Debug step by step

**PR feedback overwhelming:**

- Address one comment at a time
- Ask for clarification if needed
- Don't take it personally
- Learn from feedback

## Time Estimates

**Bug fixes:**

- Simple: 1-4 hours
- Medium: 4-8 hours
- Complex: 1-3 days

**Features:**

- Small: 1-2 days
- Medium: 3-5 days
- Large: 1-2 weeks

**Enhancements:**

- Minor: 2-6 hours
- Moderate: 1-2 days
- Major: 3-5 days

**Add:**

- +20% for testing
- +15% for documentation
- +15% for review/feedback

## Key Principles

1. **Understand before coding** - Spend time analyzing issue
2. **Plan before implementing** - Create detailed plan
3. **Test as you go** - TDD approach
4. **Commit frequently** - Small, focused commits
5. **Document decisions** - Explain why, not just what
6. **Review own code** - Catch issues early
7. **Respond professionally** - Feedback is learning

Use this skill to consistently deliver high-quality implementations with well-documented pull requests that get merged quickly.
