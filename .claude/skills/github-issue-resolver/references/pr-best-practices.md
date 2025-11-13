# Pull Request Best Practices

Guide to creating high-quality pull requests that get merged quickly.

## The Perfect PR

A great PR has:

1. **Clear purpose** - Solves one specific issue
2. **Good description** - Explains what, why, and how
3. **Small size** - Easy to review (< 400 lines preferred)
4. **Tests included** - Proves it works
5. **Documentation updated** - Keeps docs current
6. **Clean commits** - Logical, well-described changes

## PR Title

### Format

Use conventional commits format:

```
<type>(<scope>): <subject>

Examples:
fix(auth): Handle special characters in email validation
feat(api): Add user profile endpoint
docs(readme): Update installation instructions
test(utils): Add coverage for date formatting
refactor(db): Optimize query performance
```

### Types

- `fix` - Bug fixes
- `feat` - New features
- `docs` - Documentation only
- `style` - Code style (formatting, no logic change)
- `refactor` - Code restructuring (no behavior change)
- `perf` - Performance improvements
- `test` - Adding/updating tests
- `chore` - Maintenance (dependencies, build config)
- `ci` - CI/CD changes

### Good vs Bad Titles

✅ Good:

- `fix(auth): Prevent crash on empty email input (#123)`
- `feat(api): Add pagination to user list endpoint (#456)`
- `docs: Add examples for custom configuration (#789)`

❌ Bad:

- `Fix bug`
- `Update code`
- `Changes`
- `Working version`

## PR Description

### Template

````markdown
## Description

Brief summary of what this PR does (2-3 sentences).

Fixes #123

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Changes

- Added email validation to authentication flow
- Created `isValidEmail()` utility function in `src/utils/validation.js`
- Added 5 test cases covering various email formats
- Updated API documentation with validation rules

## Testing

### Test Environment

- Node v18.16.0
- npm 9.5.1

### Tests Performed

- [x] All existing unit tests pass
- [x] All existing integration tests pass
- [x] Added new tests for email validation
- [x] Manually tested with various email formats:
  - Standard emails (user@example.com) ✓
  - Special characters (user+tag@example.com) ✓
  - International domains (user@例え.jp) ✓
  - Edge cases (empty, null, undefined) ✓

### Test Commands

```bash
npm test
npm run test:integration
```
````

## Screenshots (if applicable)

Before:
![Before](url-to-image)

After:
![After](url-to-image)

## Checklist

- [x] My code follows the style guidelines of this project
- [x] I have performed a self-review of my own code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] I have made corresponding changes to the documentation
- [x] My changes generate no new warnings
- [x] I have added tests that prove my fix is effective or that my feature works
- [x] New and existing unit tests pass locally with my changes
- [x] Any dependent changes have been merged and published

## Additional Notes

- This fix is backward compatible
- No database migrations required
- No environment variable changes needed

```

## Commit Messages

### Format

```

<type>: <subject>

<body>

<footer>
```

### Example

```
fix: Handle special characters in email validation

The previous implementation failed when email addresses contained
special characters like '+' or '='. This is now handled correctly
by using a more comprehensive regex pattern.

Also added validation for international domain names to support
non-ASCII characters in email addresses.

Fixes #123
```

### Best Practices

1. **Subject line**:
   - 50 characters or less
   - Imperative mood ("Add feature" not "Added feature")
   - No period at end
   - Capitalize first letter

2. **Body**:
   - 72 characters per line
   - Explain what and why, not how
   - Separate from subject with blank line

3. **Footer**:
   - Reference issues: `Fixes #123`, `Closes #456`, `Refs #789`
   - Breaking changes: `BREAKING CHANGE: description`

### Atomic Commits

Each commit should be:

- **Self-contained** - Works on its own
- **Focused** - One logical change
- **Buildable** - Code compiles/runs at each commit
- **Tested** - Tests pass at each commit

Good commit history:

```
feat: Add email validation function
test: Add tests for email validation
feat: Integrate email validation in auth flow
docs: Update API docs with validation rules
```

Bad commit history:

```
WIP
Fix typo
Fix tests
Actually fix tests this time
Final changes
```

## Code Review

### Responding to Feedback

✅ Do:

- Thank reviewers for their time
- Ask clarifying questions
- Explain your reasoning
- Make requested changes
- Mark resolved conversations

❌ Don't:

- Take feedback personally
- Ignore comments
- Argue unnecessarily
- Make unrelated changes

### Example Response

```markdown
> Consider using a regex constant instead of inline regex

Good point! I've extracted it to a `EMAIL_REGEX` constant at the
top of the file. This makes it more maintainable and allows reuse
in other validation functions.

Updated in commit abc123.
```

### Requesting Changes

If you disagree with feedback:

```markdown
I considered that approach, but went with this implementation because:

1. It handles edge case X that the suggested approach doesn't
2. It's more performant for large datasets
3. It's consistent with how we handle similar cases in file Y

However, I'm open to discussion if there's something I'm missing!
```

## PR Size

### Guidelines

- **Tiny (1-50 lines)**: Perfect, review immediately
- **Small (50-200 lines)**: Good, easy to review
- **Medium (200-400 lines)**: Acceptable, takes time
- **Large (400-1000 lines)**: Consider splitting
- **Huge (1000+ lines)**: Please split into multiple PRs

### When to Split

Split PRs if:

- Multiple independent changes
- Refactoring + feature addition
- Can be reviewed in stages
- Different areas of codebase

### Splitting Strategies

1. **Refactoring first**:

   ```
   PR 1: Refactor existing code
   PR 2: Add new feature (depends on PR 1)
   ```

2. **Infrastructure then feature**:

   ```
   PR 1: Add database schema
   PR 2: Add API endpoints
   PR 3: Add UI components
   ```

3. **Component by component**:
   ```
   PR 1: Add user model
   PR 2: Add auth service
   PR 3: Add API routes
   ```

## Documentation

### What to Document

- **API changes**: New endpoints, parameters, responses
- **Configuration**: New environment variables, config files
- **Breaking changes**: Migration guides
- **Usage examples**: How to use new features
- **Architecture**: Design decisions for complex features

### Where to Document

- `README.md` - Overview, quickstart
- `CHANGELOG.md` - Version history
- `docs/` - Detailed documentation
- Code comments - Complex logic
- API docs - OpenAPI/Swagger specs
- Tests - Usage examples

## Common Mistakes

### ❌ Mistake: No Issue Reference

```
feat: Add email validation

Added email validation to the auth flow.
```

✅ Fix: Link to issue

```
feat: Add email validation

Added email validation to the auth flow to prevent
authentication failures with special characters.

Fixes #123
```

### ❌ Mistake: Too Many Changes

PR with 50 files changed, adding feature + refactoring + fixing bugs.

✅ Fix: Split into focused PRs

```
PR 1: Refactor auth module
PR 2: Fix email validation bug
PR 3: Add new social login feature
```

### ❌ Mistake: No Tests

```
Files changed: src/auth.js
```

✅ Fix: Include tests

```
Files changed:
- src/auth.js
- tests/auth.test.js
```

### ❌ Mistake: Unclear Changes

```
## Changes
- Updated files
- Fixed issues
- Improved code
```

✅ Fix: Be specific

```
## Changes
- Added `isValidEmail()` function for email validation
- Updated `authenticate()` to validate email before processing
- Added 5 test cases covering edge cases
- Updated API documentation with new validation rules
```

## PR Checklist

Before submitting:

- [ ] Branch is up to date with main
- [ ] All tests pass locally
- [ ] Code follows project style guide
- [ ] No linting errors
- [ ] Self-reviewed the code
- [ ] Added/updated tests
- [ ] Updated documentation
- [ ] Added clear PR description
- [ ] Linked related issue(s)
- [ ] Commits are clean and logical
- [ ] No commented-out code
- [ ] No debug statements
- [ ] No merge conflicts

## Tips for Fast Approval

1. **Smaller is better** - Keep PRs focused and small
2. **Test thoroughly** - Include comprehensive tests
3. **Document clearly** - Explain what and why
4. **Follow conventions** - Match project style
5. **Respond quickly** - Address feedback promptly
6. **Request reviews** - Tag appropriate reviewers
7. **Check CI** - Ensure automated checks pass
8. **Be patient** - Give reviewers time
9. **Follow up** - Politely ping after reasonable time
10. **Learn continuously** - Improve with each PR

## Examples of Great PRs

### Bug Fix PR

````markdown
# fix(auth): Prevent crash on null email input

## Description

Fixes a crash that occurs when users attempt to authenticate with
a null or undefined email. The authentication handler now properly
validates input before processing.

Fixes #456

## Changes

- Added null/undefined check in `authenticate()` function
- Added early return with clear error message
- Added 3 test cases for null/undefined/empty inputs
- Updated error messages to be more descriptive

## Testing

- All 127 existing tests pass
- Added 3 new tests that previously failed, now pass
- Manually tested auth flow with various inputs

### Before

```js
function authenticate(email, password) {
  const sanitized = email.toLowerCase(); // Crashes if email is null
  // ...
}
```
````

### After

```js
function authenticate(email, password) {
  if (!email || typeof email !== "string") {
    throw new Error("Email must be a non-empty string");
  }
  const sanitized = email.toLowerCase();
  // ...
}
```

## Checklist

- [x] Tests added
- [x] All tests pass
- [x] Documentation updated
- [x] Self-reviewed

```

This PR would likely be approved quickly because it:
- Fixes a specific bug
- Includes tests
- Shows before/after code
- Has clear description
- Is small and focused
```
