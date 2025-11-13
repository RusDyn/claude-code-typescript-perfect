---
name: qa-github-manager
description: Act as a senior QA engineer managing client feedback and GitHub issues. Use when receiving client feedback, bug reports, or feature requests that need to be transformed into well-structured GitHub issues. Handles (1) Parsing and structuring unstructured client feedback, (2) Breaking down complex feedback into atomic issues, (3) Searching existing GitHub issues to avoid duplicates, (4) Deciding whether to reopen closed issues or create new ones, (5) Creating well-formatted issues with proper labels, priorities, and templates, (6) Maintaining issue quality and relationships.
---

# QA GitHub Issue Manager

Transform client feedback into well-structured, actionable GitHub issues while avoiding duplicates and maintaining high quality standards.

## When to Use This Skill

Use qa-github-manager when you need to:

- **Process client feedback** (bug reports, feature requests, complaints)
- **Transform unstructured feedback** into well-formatted GitHub issues
- **Break down complex feedback** into atomic, manageable issues
- **Search for duplicate issues** before creating new ones
- **Decide whether to reopen** closed issues or create new ones
- **Ensure issue quality** with proper labels, priorities, and templates
- **Maintain issue relationships** (linked issues, dependencies)

## When NOT to Use This Skill

**DO NOT use qa-github-manager for:**

- **Implementing solutions** → Use `github-issue-resolver` skill instead
- **Fixing bugs or adding features** → Use `github-issue-resolver` for implementation
- **Reviewing pull requests** → Use standard PR review processes
- **Writing code** → This skill is for issue management only
- **Project planning** → Use appropriate project management tools

**Clear separation:**

- `qa-github-manager` = Feedback → Issues (QA/triage role)
- `github-issue-resolver` = Issue → Implementation → PR (developer role)

## Quick Start

### 1. Parse Client Feedback

Extract structured information from raw client feedback:

```bash
python scripts/parse_feedback.py "Client reported that login button doesn't work on mobile. They click it but nothing happens. Very urgent."
```

**Output:** Structured feedback items with classification (bug/feature), severity, and extracted details.

### 2. Break Down Complex Feedback

Split complex feedback into atomic, manageable issues:

```bash
python scripts/issue_analyzer.py '{"description": "Fix login and add password reset", "item_type": "bug", "severity": "high"}'
```

**Output:** Multiple smaller issues, each with proper scope and templates.

### 3. Search for Similar Issues

Find existing issues to avoid duplicates:

```bash
python scripts/github_issues.py search --issue '{"title": "Login button broken"}' --existing '[{...existing issues...}]'
```

**Output:** Similar issues with similarity scores and recommendations.

### 4. Decide on Action

Determine whether to reopen or create new:

```bash
python scripts/github_issues.py reopen-check --new '{"title": "..."}' --existing '{"number": 123, "state": "closed"}'
```

**Output:** Decision with confidence level and reasoning.

## Complete Workflow

Follow this workflow for every client feedback:

### Step 1: Receive & Parse

**Sources:**

- Email from client
- Support ticket
- Direct communication
- Monitoring/analytics

**Action:** Use `parse_feedback.py` to structure the feedback.

**What it does:**

- Classifies as bug/feature/enhancement
- Assigns severity (critical/high/medium/low)
- Extracts steps to reproduce
- Identifies expected vs actual behavior
- Splits multi-item feedback

### Step 2: Analyze & Break Down

**Check complexity:**

- Is it a single, clear problem? → Keep as-is
- Multiple problems? → Split into atomic issues
- Affects multiple components? → Split by component
- Too large for one PR? → Break down into sub-tasks

**Action:** Use `issue_analyzer.py` to split complex items.

**Rules for atomic issues:**

- Can be completed by one developer
- Has clear scope and boundaries
- Takes 1-5 days maximum
- Doesn't depend on multiple other issues
- Has clear acceptance criteria

### Step 3: Search Existing Issues

**Search strategy:**

1. Keywords from title
2. Labels (bug, feature, component)
3. Combination of keywords + labels

**Action:** Use `github_issues.py search` or manually search GitHub.

**Look for:**

- Exact duplicates (same title/symptoms)
- Similar issues (same component, related)
- Closed issues (potential regressions)

### Step 4: Compare & Decide

**Decision tree:**

```
Found similar issue?
├─ No → Create new issue
└─ Yes → Is it open?
   ├─ Yes → Same issue?
   │  ├─ Yes → Add comment
   │  └─ No → Create new, link
   └─ No (closed) → Reopen?
      ├─ Yes → Reopen with context
      └─ No → Create new, reference
```

**Reopen criteria:**

- Same bug, confirmed regression
- Same symptoms, same component
- Recently closed (within weeks)
- New evidence suggests incomplete fix

**Action:** Use `github_issues.py reopen-check` for guidance.

### Step 5: Take Action

**Option A: Create New Issue**

1. Choose template (bug/feature/enhancement)
2. Write clear, searchable title
3. Fill in all template sections
4. Add proper labels
5. Set priority based on severity
6. Link related issues
7. Assign if known

**Option B: Reopen Existing**

1. Add reopening comment
2. Include new feedback
3. Update labels (add `regression`)
4. Increase priority if warranted
5. @mention original assignee

**Option C: Add to Existing**

1. Comment with new information
2. Update impact/severity if needed
3. Thank reporter

### Step 6: Follow-up

- Notify client (if appropriate)
- Monitor for similar reports
- Update when questions arise
- Track resolution progress

## Best Practices

### Writing Issue Titles

**Good titles:**

- "Login button does not respond on mobile Safari"
- "Add CSV export to user reports page"
- "Improve search performance for 10k+ items"

**Bad titles:**

- "It's broken" (too vague)
- "Fix login, add reset, improve UI" (multiple issues)
- "Problem" (no context)

**Formula:**

- **Bugs:** `[Component] [Specific problem] [Context]`
- **Features:** `[Action] [What] [Where]`
- **Enhancements:** `Improve [What] [How/Why]`

### Issue Quality Checklist

Before creating:

- [ ] Title is specific and searchable
- [ ] Description follows template
- [ ] Steps to reproduce (for bugs)
- [ ] Expected vs actual clearly stated
- [ ] Environment details provided
- [ ] Screenshots if relevant
- [ ] Proper labels applied
- [ ] Priority set correctly
- [ ] Related issues linked

### Classification Guide

**Bug:**

- Something stopped working
- Behavior doesn't match documentation
- Error messages or crashes
- Data integrity issues

**Feature:**

- New capability not available
- "Can you add..." requests
- Workflow enhancements
- Integration requests

**Enhancement:**

- Improvement to existing feature
- Performance optimization
- UX improvement
- Better error messages

### Priority Assignment

**Critical:**

- System down or unusable
- Data loss or corruption
- Security vulnerability
- Production blocker

**High:**

- Major functionality broken
- Affects many users
- Significant business impact
- Workaround is complex

**Medium:**

- Feature not working as expected
- Affects some users
- Workaround available
- Standard priority

**Low:**

- Minor issue or edge case
- Cosmetic issues
- Affects few users
- Nice to have

### Handling Complex Feedback

**Example input:**

```
"The app is slow and the login doesn't work and we need
password reset and the UI looks bad."
```

**Split into:**

1. "Reduce dashboard load time from 8s to <2s"
2. "Fix login button not responding on mobile Safari"
3. "Add password reset link to login page"
4. "Improve visual design of login page"

**Maintain relationships:**

- Link issues together
- Use same milestone if related
- Reference parent tracking issue if needed

## Reference Documentation

### In-Depth Guides

**references/issue-writing-guide.md** - Complete guide to writing high-quality GitHub issues:

- Title best practices with formulas
- Templates for bugs, features, enhancements
- Labels and priority guidelines
- Steps to reproduce best practices
- Common mistakes to avoid
- Examples of well-written issues

**references/qa-workflow.md** - Detailed workflow with decision trees:

- Complete step-by-step process
- Decision matrices for reopen vs create new
- Handling edge cases (vague feedback, confidential, disputed)
- Communication templates
- Metrics to track
- Common pitfalls

**references/github-api-reference.md** - GitHub API operations:

- Authentication and rate limiting
- Search syntax and examples
- Creating, updating, reopening issues
- Adding comments and labels
- Python integration code
- Error handling

## Templates

Use these templates for consistent issue formatting:

**assets/templates/bug-report.md** - Standard bug report format
**assets/templates/feature-request.md** - Feature request with user stories
**assets/templates/enhancement.md** - Enhancement with success metrics

## Common Scenarios

### Scenario 1: Vague Client Feedback

**Client says:** "The app is slow"

**Your actions:**

1. Request clarification: Which page? How slow? When does it happen?
2. Create draft issue with "[NEEDS INFO]" prefix
3. Don't publish until you have specifics
4. Once clarified, create proper issue with measurements

### Scenario 2: Regression Report

**Client says:** "Login stopped working again"

**Your actions:**

1. Search for previously closed login issues
2. Find issue #123 closed 2 weeks ago
3. Use reopen-check script to confirm
4. Reopen with new context and label as `regression`
5. Increase priority (regressions are often critical)
6. @mention original developer

### Scenario 3: Multiple Issues in One

**Client says:** "Login is broken, password reset doesn't work, and we need 2FA"

**Your actions:**

1. Parse into 3 separate items
2. Create 3 issues:
   - "Fix login button not responding"
   - "Fix password reset email not sending"
   - "Add two-factor authentication option"
3. Link them if related
4. Prioritize independently

### Scenario 4: Duplicate Detection

**New feedback:** "Submit button doesn't work on checkout"

**Your actions:**

1. Search: "checkout button"
2. Find similar open issue #456
3. Compare details - is it the same issue?
4. If yes: Add comment to #456 with new info
5. If no: Create new issue, link to #456

### Scenario 5: Should Reopen?

**Decision factors:**

- **Reopen if:** Same bug, regression, recently closed, incomplete fix
- **Create new if:** Different symptoms, new context, won't-fix was valid, long time since closure

**Use script:**

```bash
python scripts/github_issues.py reopen-check \
  --new '{"title": "Login broken", "body": "..."}' \
  --existing '{"number": 123, "state": "closed", "closed_at": "2024-01-10"}'
```

## Communication Templates

### Client Acknowledgment

```
Thank you for reporting this issue. I've created GitHub issue #123
to track this bug. Our team will investigate and provide updates
on that ticket.

Link: https://github.com/org/repo/issues/123
```

### Reopening Comment

```markdown
## Reopening Issue

This issue is being reopened based on new client feedback indicating
the problem has recurred.

### New Report

Date: 2024-01-15
Client: Acme Corp

### New Context

Issue now occurs on all mobile devices, not just Safari.

### Client Feedback

"Login button still doesn't respond on mobile. This started
happening again yesterday."

### Additional Steps

1. Tested on Chrome Mobile - same issue
2. Tested on Firefox Mobile - same issue
3. Desktop still works fine

Original fix in PR #456 may have been incomplete or a regression
was introduced in a recent deployment.

cc @original-developer
```

### Adding to Existing

```markdown
## Additional Report

Thank you for the additional feedback. This is the same issue
currently being tracked.

### Impact Update

This issue has now been reported by 3 clients (Acme Corp,
Widget Inc, and now TechStart).

### New Information

Also affects Firefox, not just Safari as originally reported.
```

## Troubleshooting

**Script doesn't parse feedback correctly:**

- Check if feedback is too vague - clarify first
- Try breaking feedback into smaller pieces manually
- Check for unusual formatting

**Too many duplicates created:**

- Improve search process
- Use similarity threshold in scripts
- Review closed issues more carefully

**Issues are too vague:**

- Use templates consistently
- Request more details before creating
- Add "needs-info" label and follow up

**Reopens when should create new:**

- Review reopen criteria
- Check how long ago issue was closed
- Verify it's actually the same issue

## Metrics to Track

**Issue Quality:**

- Time to first dev response
- Clarification questions needed per issue
- Issues marked as duplicate (target: <5%)
- Issues closed as invalid (target: <10%)

**Process Efficiency:**

- Time from feedback to issue creation
- Number of reopened issues
- Regression rate
- Average time to resolution by severity

## Key Principles

1. **Quality over speed** - Better to take time and create good issues
2. **One issue, one problem** - Always split complex feedback
3. **Search before creating** - Duplicates waste everyone's time
4. **Be objective** - Document facts, not opinions
5. **Complete context** - Include everything needed to act
6. **Maintain relationships** - Link related issues
7. **Follow up** - Issues are living documents

Use this skill to consistently transform client feedback into actionable, well-structured GitHub issues that serve both the development team and clients effectively.
