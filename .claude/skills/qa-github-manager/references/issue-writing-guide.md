# GitHub Issue Writing Guide

Best practices for writing clear, actionable, and well-structured GitHub issues.

## Core Principles

1. **One Issue, One Problem** - Each issue should address a single, atomic problem
2. **Actionable** - Clear what needs to be done to resolve the issue
3. **Reproducible** - For bugs, anyone should be able to reproduce the problem
4. **Searchable** - Use clear titles with relevant keywords
5. **Complete** - Include all necessary context without requiring external knowledge

## Issue Title Best Practices

### Good Titles

✅ `Login button does not respond on mobile Safari`  
✅ `Add dark mode toggle to user settings`  
✅ `API returns 500 error when uploading files >10MB`  
✅ `Improve page load time for product listings`

### Bad Titles

❌ `It's broken` - Too vague  
❌ `Problem with the system` - No specificity  
❌ `Can we add feature X, Y, and Z?` - Multiple issues  
❌ `The button` - Incomplete

### Title Formula

**For Bugs:** `[Component] [Specific problem] [Context/condition]`  
Example: "Login button does not respond on mobile Safari"

**For Features:** `[Action verb] [What] [Where/Context]`  
Example: "Add export to CSV button in reports page"

**For Enhancements:** `Improve [What] [How/Why]`  
Example: "Improve search performance for large datasets"

## Issue Body Structure

### Bug Report Template

```markdown
## Description

Clear, concise description of the bug.

## Steps to Reproduce

1. Go to [page/URL]
2. Click on [element]
3. Enter [specific data]
4. Observe [result]

## Expected Behavior

What should happen when the steps are followed.

## Actual Behavior

What actually happens. Be specific.

## Environment

- OS: [e.g., Windows 11, macOS 14]
- Browser: [e.g., Chrome 120, Safari 17]
- Version: [app version if applicable]
- Additional context: [screen size, network conditions, etc.]

## Screenshots/Videos

[If applicable, attach visual evidence]

## Additional Context

Any other relevant information, related issues, or attempted solutions.

## Severity

- [ ] Critical - System is unusable/down
- [ ] High - Major functionality broken
- [x] Medium - Feature not working as expected
- [ ] Low - Minor issue or edge case
```

### Feature Request Template

```markdown
## Feature Description

Clear description of the feature being requested.

## Problem Statement

What problem does this feature solve? Why is it needed?

## Proposed Solution

How should this feature work? Be as specific as possible.

### User Stories

- As a [user type], I want to [action] so that [benefit]
- As a [user type], I want to [action] so that [benefit]

## Alternatives Considered

What other approaches were considered and why were they not chosen?

## Acceptance Criteria

- [ ] Criterion 1: Specific, measurable outcome
- [ ] Criterion 2: Specific, measurable outcome
- [ ] Criterion 3: Specific, measurable outcome

## Mockups/Examples

[Attach any visual mockups, wireframes, or examples from other systems]

## Additional Context

- Related issues: #123, #456
- Impact: How many users will benefit?
- Priority: Why should this be done now?
```

### Enhancement Template

```markdown
## Current Behavior

Description of how the system currently works.

## Proposed Enhancement

What should be improved and how?

## Benefits

- Benefit 1: Specific improvement
- Benefit 2: Specific improvement
- Benefit 3: Specific improvement

## Implementation Considerations

- Technical complexity
- Breaking changes
- Migration requirements

## Success Metrics

How will we measure the improvement?

- Metric 1: [e.g., page load time reduced by 50%]
- Metric 2: [e.g., user satisfaction increased]
```

## Labels - Best Practices

### Type Labels (Choose One)

- `bug` - Something isn't working
- `feature` - New feature request
- `enhancement` - Improvement to existing feature
- `documentation` - Documentation updates
- `question` - Question or clarification needed

### Priority Labels (Choose One)

- `priority-critical` - System down, data loss, security issue
- `priority-high` - Major functionality broken, affecting many users
- `priority-medium` - Standard priority, normal feature work
- `priority-low` - Nice to have, minor improvements

### Status Labels

- `needs-triage` - Needs initial review and prioritization
- `needs-info` - Waiting for more information
- `in-progress` - Actively being worked on
- `blocked` - Blocked by external dependency
- `wont-fix` - Valid issue but won't be addressed

### Component Labels

- `component-frontend` - UI/client-side code
- `component-backend` - Server-side/API code
- `component-database` - Database schema or queries
- `component-auth` - Authentication/authorization
- `component-[name]` - Specific module or feature area

### Effort Labels

- `effort-small` - < 4 hours
- `effort-medium` - 1-3 days
- `effort-large` - > 3 days

## Writing Clear Descriptions

### Use Active Voice

✅ "The system returns an error when..."  
❌ "An error is returned by the system when..."

### Be Specific

✅ "Search returns 0 results for product names with special characters"  
❌ "Search doesn't work properly"

### Include Context

✅ "On the checkout page, the 'Apply Coupon' button is disabled even when a valid coupon code is entered in the input field"  
❌ "Button doesn't work"

### Avoid Assumptions

✅ "The login form requires an email address in the format 'user@example.com'. Currently it accepts 'user@example' which causes errors"  
❌ "Email validation is wrong"

## Steps to Reproduce - Best Practices

### Good Steps

```markdown
1. Navigate to https://example.com/login
2. Enter email: "test@example.com"
3. Enter password: "password123"
4. Click the "Login" button
5. Observe that the page shows "Invalid credentials" even with correct credentials
```

### What to Include

- **Exact URLs or navigation paths**
- **Specific data values** (sanitize sensitive info)
- **Precise actions** ("click", "type", "select")
- **Expected vs actual** at each critical step
- **Prerequisites** if any (logged in, specific data exists)

### What to Avoid

❌ "Just try to log in"  
❌ "Do the normal thing"  
❌ "You know what I mean"  
❌ Vague descriptions

## Common Mistakes to Avoid

### 1. Multiple Issues in One

**Bad:**

```
Title: Fix login and add password reset and improve UI

The login doesn't work on mobile and we need password reset
and the UI looks bad...
```

**Good:** Create 3 separate issues:

1. "Login button not responding on mobile Safari"
2. "Add password reset functionality to login page"
3. "Improve visual design of login page"

### 2. Missing Reproduction Steps

**Bad:**

```
The app crashes sometimes when I'm using it.
```

**Good:**

```
## Steps to Reproduce
1. Open app
2. Navigate to Settings > Profile
3. Tap "Edit Profile" button
4. Scroll down quickly while image is loading
5. App crashes with error: [paste error]
```

### 3. Unclear Expected Behavior

**Bad:**

```
The button should work better.
```

**Good:**

```
Expected: Clicking "Save" should save the form data and show
a success message, then redirect to the dashboard.

Actual: Clicking "Save" does nothing. No error message,
no redirect, no visual feedback.
```

### 4. Lack of Environment Details

**Bad:**

```
It doesn't work on my computer.
```

**Good:**

```
Environment:
- OS: Windows 11 Pro (Build 22621)
- Browser: Chrome 120.0.6099.130
- Screen resolution: 1920x1080
- App version: 2.4.1
- Reproducible on both Wi-Fi and ethernet
```

## Issue Lifecycle

### 1. Creation

- Write clear title and description
- Add appropriate labels
- Set priority if known
- Link related issues

### 2. Triage

- Verify reproducibility
- Assign priority
- Assign to milestone/sprint
- Assign to team member if known
- Add more labels if needed

### 3. In Progress

- Update labels to `in-progress`
- Link to pull request
- Update if requirements change

### 4. Review

- Verify fix/implementation
- Test acceptance criteria
- Update documentation if needed

### 5. Closure

- Add closing comment explaining resolution
- Link to pull request/commit
- Add `fixed` or `wont-fix` labels as appropriate

### 6. Reopening (if needed)

- Add comment explaining why reopening
- Include new information or reproduction steps
- Update labels appropriately

## Handling Client Feedback

### Transform Vague Feedback into Clear Issues

**Client Says:**

```
"The app is slow and things don't work right."
```

**Your Issues:**

**Issue 1:**

```
Title: Reduce dashboard load time
Description: Dashboard takes 8-12 seconds to load. Should load in <2 seconds.
Steps: [specific timing measurements]
```

**Issue 2:**

```
Title: Fix search returning no results for partial terms
Description: Search only works with exact matches...
Steps: [specific search examples]
```

### Ask Clarifying Questions

When feedback is unclear:

- What specific page/feature?
- What were you trying to do?
- What did you expect to happen?
- What actually happened?
- Can you reproduce it consistently?
- Any error messages?
- What device/browser?

## Cross-Referencing

### Link Related Issues

```markdown
Related to #123
Blocks #456
Blocked by #789
Duplicate of #101
Supersedes #202
```

### Reference in Comments

```markdown
This is similar to the issue reported in #123, but affects
a different component. The root cause might be shared.
```

## Writing for Developers

### Include Technical Context

```markdown
## Technical Details

- Occurs in `UserController.login()` method
- Stack trace: [paste trace]
- Happens only when Redis cache is empty
- Database query times out after 30s
- Affects PostgreSQL 14+ only
```

### Suggest Implementation Approach (Optional)

```markdown
## Possible Solutions

1. Add caching layer to reduce DB queries
2. Optimize SQL query using indexes
3. Implement pagination to limit result set

Recommend option 1 as it provides the best performance improvement
with minimal code changes.
```

## Examples of Well-Written Issues

### Example Bug Report

```markdown
Title: File upload fails with 413 error for files >10MB

## Description

When attempting to upload files larger than 10MB through the
document management interface, the upload fails with a 413
"Payload Too Large" error.

## Steps to Reproduce

1. Log in as any user
2. Navigate to Documents > Upload
3. Click "Choose File"
4. Select a file larger than 10MB (tested with 15MB PDF)
5. Click "Upload"
6. Observe error: "413 Payload Too Large"

## Expected Behavior

Files up to 50MB should upload successfully according to the
user documentation (page 12).

## Actual Behavior

Upload fails immediately with 413 error. No progress indicator
shown. No helpful error message to user.

## Environment

- Browser: Chrome 120.0.6099.130 on Windows 11
- Server: Production (api.example.com)
- File tested: test-document.pdf (15.2 MB)

## Additional Context

- Files under 10MB upload successfully
- Issue started after the December 15th deployment
- Server logs show: "client intended to send too large body"
- nginx config may need max_body_size adjustment

## Impact

- 40+ support tickets in the last week
- Users unable to upload important documents
- Workaround: Use FTP (but users don't have access)

## Severity

High - Major functionality broken for most users
```

### Example Feature Request

````markdown
Title: Add bulk user import from CSV

## Problem Statement

Currently, administrators must add users one at a time through
the UI. For organizations with 100+ users, this is time-consuming
and error-prone.

## Proposed Solution

Add a "Bulk Import" feature that allows admins to upload a CSV
file containing user information and create multiple user accounts
at once.

### User Story

As an administrator, I want to import multiple users from a CSV
file so that I can onboard an entire organization quickly without
manual data entry.

## Acceptance Criteria

- [ ] Admin can upload CSV file with columns: email, first_name, last_name, role
- [ ] System validates CSV format before processing
- [ ] System shows preview of users to be created
- [ ] System reports any validation errors (duplicate emails, invalid formats)
- [ ] System creates valid users and sends welcome emails
- [ ] System provides summary report of successful/failed imports
- [ ] System logs all import activities for audit

## CSV Format Example

```csv
email,first_name,last_name,role
john@example.com,John,Doe,user
jane@example.com,Jane,Smith,admin
```
````

## Alternative Considered

Manual user creation - rejected due to time requirement

## Impact

- Reduces user setup time from 3 hours to 5 minutes for 100 users
- Reduces data entry errors
- Improves onboarding experience
- 15+ customers have requested this feature

## Priority

High - Multiple customers blocked on onboarding

```

These examples demonstrate the level of detail and clarity that makes issues actionable and easy to work with.
```
