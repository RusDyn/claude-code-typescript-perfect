# Pull Request Best Practices

Complete guide to creating excellent pull requests that get merged quickly.

## The Perfect PR

A perfect PR is:

- **Clear** - Easy to understand what and why
- **Focused** - Solves one problem
- **Tested** - Thoroughly verified
- **Documented** - Explains decisions
- **Reviewable** - Right size, well-organized

## PR Title

### Format

**Conventional Commits:**

```
type(scope): description (#issue)
```

**Types:**

- `fix:` - Bug fix
- `feat:` - New feature
- `refactor:` - Code improvement
- `docs:` - Documentation only
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks
- `style:` - Formatting, no logic change
- `perf:` - Performance improvement

### Examples

✅ **Good titles:**

```
fix(auth): resolve login button not responding (#123)
feat(export): add CSV export to reports page (#456)
refactor(api): improve error handling in user service (#789)
docs: update authentication setup guide (#234)
test: add integration tests for payment flow (#567)
```

❌ **Bad titles:**

```
Fixed stuff
Update
Issue 123
Changes
WIP
```

### Title Guidelines

**Do:**

- Use imperative mood ("add" not "added")
- Be specific and descriptive
- Include issue number
- Keep under 72 characters
- Use lowercase (except proper nouns)

**Don't:**

- Use vague terms ("fix things", "update")
- Include multiple changes
- Use past tense
- Add period at end
- Use all caps

## PR Description

### Template

```markdown
## Description

Closes #[issue-number]

[Brief summary of what was changed and why]

## Problem

[What problem does this solve?]

## Solution

[How does this fix solve the problem?]

## Changes Made

- [Change 1]: [Why]
- [Change 2]: [Why]
- [Change 3]: [Why]

## Testing

- [x] Unit tests added/updated
- [x] Integration tests pass
- [x] Manual testing completed
- [x] Edge cases covered

### Test Plan

[How to test this change]

### Screenshots/Videos

[If applicable]

## Technical Details

[Implementation notes, architectural decisions]

## Breaking Changes

[If any, describe and provide migration path]

## Checklist

- [x] Code follows style guide
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] Tests cover changes
- [x] Documentation updated
- [x] No new warnings
- [x] Passes CI/CD

## Questions for Reviewers

[Optional: specific areas you want feedback on]
```

### Description Guidelines

**Clear problem statement:**

```markdown
## Problem

Users reported that clicking the login button on mobile devices
(iOS Safari specifically) results in no action. The button appears
clickable but doesn't trigger the authentication flow.
```

**Clear solution:**

```markdown
## Solution

The issue was caused by a z-index conflict where an invisible overlay
was positioned above the button. Fixed by:

1. Adjusting z-index values
2. Adding pointer-events: none to overlay
3. Adding automated test to prevent regression
```

**Specific changes:**

```markdown
## Changes Made

- `src/components/LoginButton.tsx`: Fixed z-index from 10 to 100
- `src/components/Overlay.tsx`: Added pointer-events: none
- `tests/auth.test.ts`: Added test for button click handling
```

## PR Size

### Ideal Size

**Lines of code changed:**

- Small: < 200 lines
- Medium: 200-500 lines
- Large: 500-1000 lines
- Too large: > 1000 lines

**Time to review:**

- Should take < 30 minutes to review
- Large PRs take hours and often get delayed

### Break Up Large PRs

**Instead of one huge PR:**

```
❌ PR #1: Implement entire user management system (2000 lines)
```

**Create a series of smaller PRs:**

```
✅ PR #1: Add user model and database schema (150 lines)
✅ PR #2: Add user authentication endpoints (200 lines)
✅ PR #3: Add user management UI (250 lines)
✅ PR #4: Add user roles and permissions (180 lines)
```

**Benefits:**

- Easier to review
- Faster to merge
- Less likely to have conflicts
- Easier to revert if needed

## Code Quality

### Self-Review

**Before requesting review:**

```
✅ Read every line of the diff
✅ Remove console.logs and debugging code
✅ Check for commented-out code
✅ Verify formatting is consistent
✅ Look for typos in comments
✅ Check for hardcoded values
✅ Verify error handling
✅ Check for security issues
```

### Code Comments

**Good comments explain "why", not "what":**

✅ **Good:**

```javascript
// Use WeakMap to avoid memory leaks with DOM elements
const cache = new WeakMap()

// Retry with exponential backoff to handle rate limiting
await retryWithBackoff(() => api.call(), 3)
```

❌ **Bad:**

```javascript
// Create a new WeakMap
const cache = new WeakMap()

// Call the API
await api.call()
```

### Code Organization

**One logical change per commit:**

```bash
✅ Good:
commit: "Add user validation"
commit: "Add user tests"
commit: "Update user docs"

❌ Bad:
commit: "Add feature, fix bug, update deps, refactor"
```

## Testing

### Test Coverage

**Required tests:**

```markdown
- [x] Unit tests for new functions
- [x] Integration tests for new features
- [x] Regression tests for bug fixes
- [x] Edge case tests
- [x] Error handling tests
```

### Test Quality

**Good test:**

```javascript
test('login button redirects authenticated user to dashboard', async () => {
  // Arrange
  const user = await createTestUser()
  render(<LoginButton />)

  // Act
  await userEvent.click(screen.getByRole('button', { name: /login/i }))

  // Assert
  expect(window.location.pathname).toBe('/dashboard')
  expect(await screen.findByText(user.name)).toBeInTheDocument()
})
```

**Bad test:**

```javascript
test('test login', () => {
  // Doesn't test anything meaningful
  expect(true).toBe(true)
})
```

### Manual Testing

**Document what you tested:**

```markdown
## Manual Testing

Tested on:

- ✅ Chrome 120 (Mac)
- ✅ Safari 17 (iOS)
- ✅ Firefox 121 (Windows)

Scenarios tested:

1. ✅ Happy path: User can log in successfully
2. ✅ Error case: Invalid credentials show error
3. ✅ Edge case: Network failure shows retry button
4. ✅ Mobile: Works on small screens
```

## Screenshots & Videos

### When to Include

**Always include for:**

- UI changes
- Visual bugs
- Animation changes
- Layout changes
- New features with UI

### Good Screenshots

**Before/After:**

```markdown
## Screenshots

### Before

![Before fix](before.png)
_Login button was not visible on mobile_

### After

![After fix](after.png)
_Login button now displays correctly on all devices_
```

**Annotated:**

```markdown
![Annotated screenshot showing the fixed button](annotated.png)
_Red box shows the fixed login button that now responds to clicks_
```

### Videos

**Use for:**

- Complex interactions
- Animation changes
- Multi-step flows
- Hard-to-describe issues

## Linking Issues

### Always Link

**Use closing keywords:**

```markdown
Closes #123
Fixes #456
Resolves #789
```

**Multiple issues:**

```markdown
Closes #123, #124, #125
```

**Related (but not closing):**

```markdown
Related to #456
Addresses #789
Part of #234
```

### Reference in Commits

```bash
git commit -m "fix: resolve login bug

This commit fixes the login button not responding on mobile.

Closes #123"
```

## Requesting Review

### Choose Reviewers

**Select:**

- Code owners (automatic)
- Subject matter experts
- Team members familiar with area
- Mix of senior and junior (for learning)

**Don't:**

- Request everyone
- Request someone on vacation
- Request without context

### Provide Context

```markdown
## For Reviewers

### Context

This PR fixes a critical production bug affecting 30% of mobile users.

### What to Focus On

1. The z-index fix in LoginButton.tsx
2. Test coverage in auth.test.ts
3. Any edge cases I might have missed

### Questions

1. Should we add more logging?
2. Is the z-index value reasonable?
```

### Set Draft PR if Not Ready

```markdown
## 🚧 Draft PR - Do Not Merge

Still working on:

- [ ] Integration tests
- [ ] Documentation
- [ ] Performance optimization

Will mark ready for review once complete.
```

## Responding to Feedback

### Be Professional

**Good responses:**

```markdown
> This function is too complex

Good point! I've refactored it into smaller functions in commit abc123.
```

```markdown
> Should we add error handling here?

Absolutely. Added try-catch with proper error logging in commit def456.
```

```markdown
> Can you explain why you chose this approach?

Sure! I chose this approach because [reason]. Alternative would be [X]
but that has drawback [Y]. Open to other suggestions!
```

**Bad responses:**

```markdown
> This seems overly complex

No it's not. This is the right way.
```

```markdown
> Can you add tests?

Tests are overrated.
```

### When You Disagree

**Respectfully explain:**

```markdown
> This seems like overkill

I understand the concern. I chose this approach because:

1. [Reason 1]
2. [Reason 2]

However, I'm open to alternatives. Would [simpler approach] work?
What are your concerns with the current implementation?
```

### Track Changes

```markdown
## Review Updates

### Round 1 (2024-01-15)

- ✅ Refactored complex function per @reviewer1
- ✅ Added error handling per @reviewer2
- ✅ Improved test coverage

### Round 2 (2024-01-16)

- ✅ Simplified logic per @reviewer1
- ✅ Added documentation per @reviewer3
```

## Common PR Problems

### Problem 1: Too Many Changes

**Symptom:** PR with 2000+ line changes  
**Solution:** Split into multiple PRs  
**Prevention:** Plan smaller increments

### Problem 2: Unclear Description

**Symptom:** Description says "Fixed bug"  
**Solution:** Add context, problem, solution  
**Prevention:** Use PR template

### Problem 3: No Tests

**Symptom:** PR has code changes but no tests  
**Solution:** Add comprehensive tests  
**Prevention:** Write tests first (TDD)

### Problem 4: Ignoring CI Failures

**Symptom:** Requesting review with failing CI  
**Solution:** Fix CI before requesting review  
**Prevention:** Run tests locally first

### Problem 5: Scope Creep

**Symptom:** PR fixes bug A but also refactors B and adds feature C  
**Solution:** Create separate PRs  
**Prevention:** Stay focused on one issue

### Problem 6: Stale PR

**Symptom:** PR sits for weeks with no activity  
**Solution:** Respond to feedback promptly, rebase regularly  
**Prevention:** Keep PRs small, set aside time for reviews

## PR Checklist

Use before requesting review:

### Code Quality

- [ ] Code follows style guide
- [ ] No console.logs or debug code
- [ ] No commented-out code
- [ ] Error handling added
- [ ] Edge cases considered
- [ ] Security reviewed
- [ ] Performance acceptable

### Tests

- [ ] Unit tests added
- [ ] Integration tests added
- [ ] All tests passing locally
- [ ] Test coverage adequate
- [ ] Edge cases tested
- [ ] Manual testing completed

### Documentation

- [ ] Comments added for complex logic
- [ ] README updated if needed
- [ ] API docs updated if needed
- [ ] CHANGELOG updated

### PR Description

- [ ] Clear problem statement
- [ ] Solution explained
- [ ] Changes listed
- [ ] Testing documented
- [ ] Screenshots included (if UI)
- [ ] Breaking changes noted

### Process

- [ ] Branch up to date with main
- [ ] Linked to issue(s)
- [ ] CI passing
- [ ] No merge conflicts
- [ ] Appropriate reviewers requested
- [ ] Draft status correct

## Merging

### Before Merging

**Verify:**

- ✅ All reviews approved
- ✅ CI/CD passing
- ✅ No merge conflicts
- ✅ Up to date with base branch

### Merge Strategies

**Squash and merge** (recommended):

- Creates one clean commit
- Good for feature branches
- Keeps history clean

**Merge commit:**

- Preserves all commits
- Good for important features
- Shows full history

**Rebase and merge:**

- Linear history
- Good for small PRs
- Requires force push

### After Merging

**Follow up:**

- [ ] Verify in staging
- [ ] Monitor for errors
- [ ] Update related issues
- [ ] Thank reviewers
- [ ] Delete branch

## Examples

### Example 1: Bug Fix PR

```markdown
# fix(auth): resolve login button not responding on mobile (#123)

## Description

Closes #123

Fixed critical bug where login button on mobile Safari doesn't respond
to click events, affecting 30% of our mobile users.

## Problem

Users on iOS Safari reported that tapping the login button produces no
result. Debug investigation revealed a z-index conflict where an
invisible overlay was positioned above the button.

## Solution

1. Adjusted z-index of login button from 10 to 100
2. Added `pointer-events: none` to overlay component
3. Added automated test to prevent regression

## Changes Made

- `src/components/LoginButton.tsx`: Updated z-index
- `src/components/Overlay.tsx`: Added pointer-events style
- `tests/auth.test.tsx`: Added regression test

## Testing

- [x] Unit test added for button click handler
- [x] Manual testing on iOS Safari 17
- [x] Manual testing on Android Chrome
- [x] Verified fix on production-like environment

### Manual Test Results

✅ iOS Safari 17 - Working
✅ iOS Chrome 120 - Working
✅ Android Chrome 121 - Working
✅ Desktop Safari 17 - Working

## Screenshots

[Before/After screenshots]

## Checklist

- [x] Code follows style guide
- [x] Self-review completed
- [x] Tests added
- [x] All tests passing
- [x] No new warnings
```

### Example 2: Feature PR

```markdown
# feat(reports): add CSV export functionality (#456)

## Description

Closes #456

Implements CSV export for all report pages, allowing users to download
report data for offline analysis.

## User Story

As a business analyst, I want to export report data to CSV so that
I can analyze it in Excel and share with stakeholders.

## Implementation

- Added export button to report header
- Created CSV generation utility
- Implemented download functionality
- Added loading state and error handling

## Changes Made

- `src/components/ReportHeader.tsx`: Added export button
- `src/utils/csvExport.ts`: New CSV generation utility
- `src/api/reports.ts`: Added export endpoint
- `tests/csvExport.test.ts`: Comprehensive test coverage

## Testing

- [x] Unit tests for CSV generation
- [x] Integration tests for export flow
- [x] Manual testing with large datasets (10k+ rows)
- [x] Error handling for failed exports

### Test Scenarios

✅ Small dataset (100 rows) - <1s
✅ Medium dataset (1000 rows) - <2s
✅ Large dataset (10k rows) - <5s
✅ Network failure - Shows error message
✅ Empty dataset - Shows appropriate message

## Screenshots

[Export button, loading state, success message]

## Documentation

- Updated README with export feature
- Added JSDoc comments to utility functions

## Checklist

- [x] Code follows style guide
- [x] Tests comprehensive
- [x] Documentation updated
- [x] Performance acceptable
- [x] Accessibility reviewed
```

Following these best practices will result in PRs that are easy to review, quick to merge, and maintain high code quality.
