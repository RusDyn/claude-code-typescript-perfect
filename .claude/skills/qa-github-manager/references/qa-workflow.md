# QA Workflow for GitHub Issue Management

Complete workflow for processing client feedback and managing GitHub issues as a senior QA engineer.

## Overview

This workflow transforms raw client feedback into well-structured, actionable GitHub issues while avoiding duplicates and maintaining issue quality.

## Complete Workflow

```
Client Feedback
      ↓
[1. Receive & Parse]
      ↓
[2. Analyze & Break Down]
      ↓
[3. Search Existing Issues]
      ↓
[4. Compare & Decide]
      ↓
[5. Take Action]
   ↓           ↓          ↓
Reopen    Create New   Skip/Merge
```

## Step 1: Receive & Parse Feedback

### Input Sources

**Email:**

- Forward to parsing system
- Extract key information
- Preserve original context

**Support Tickets:**

- Extract ticket body
- Include ticket ID in issue
- Tag with `from-support`

**Direct Client Communication:**

- Document verbatim first
- Then structure and clarify
- Get permission to create public issue if needed

**User Analytics/Monitoring:**

- Error logs
- User behavior analytics
- Performance metrics

### Parsing Process

Use `parse_feedback.py` script:

```bash
python scripts/parse_feedback.py "Client feedback text here"
```

**What it does:**

- Splits multi-item feedback
- Classifies as bug/feature/enhancement
- Assigns severity
- Extracts steps to reproduce
- Identifies expected vs actual behavior

### Initial Classification

**Is it a Bug?**

- Something that worked before stopped working
- System behavior doesn't match documentation
- Error messages or crashes
- Data integrity issues

**Is it a Feature Request?**

- New capability not currently available
- "Can you add..." or "It would be great if..."
- Enhancement to workflow
- Integration request

**Is it an Enhancement?**

- Improvement to existing feature
- Performance optimization
- UX improvement
- Better error messages

**Is it a Question?**

- Unclear how to use feature
- Documentation clarification needed
- May indicate UX problem

## Step 2: Analyze & Break Down

### Complexity Check

**Simple Issue (Create as-is):**

- Single, clear problem
- Well-defined scope
- Can be completed in one PR
- One component affected

**Complex Issue (Split):**

- Multiple problems in one feedback
- Affects multiple components
- Multiple steps to completion
- Can be parallelized

### Splitting Strategy

Use `issue_analyzer.py` script:

```bash
python scripts/issue_analyzer.py '{"description": "...", "item_type": "bug"}'
```

**When to Split:**

- "And" appears multiple times
- Multiple action verbs (fix X, add Y, change Z)
- Affects 3+ components
- Would take multiple sprints
- Has independent sub-tasks

**How to Split:**

```
Original: "Fix login on mobile and add password reset and improve error messages"

Split into:
1. "Fix login button not responding on mobile Safari"
2. "Add password reset link to login page"
3. "Improve error messages on login failures"
```

**Maintain Relationships:**

- Link related issues: "Related to #123"
- Use same labels/milestone
- Reference parent issue if tracking needed

### Scope Validation

Each issue should answer:

- [ ] Can one developer complete this alone?
- [ ] Is the scope clear and bounded?
- [ ] Can it be completed in 1-5 days?
- [ ] Has clear acceptance criteria?
- [ ] Doesn't depend on multiple other issues?

## Step 3: Search Existing Issues

### Search Strategy

1. **Keyword Search**

```bash
# Use GitHub search or API
# Search: "login button mobile"
```

2. **Label-Based Search**

```bash
# Search: "label:bug label:component-auth"
```

3. **Automated Search**

```bash
python scripts/github_issues.py queries --issue '{"title": "..."}'
# Returns optimized search queries
```

### What to Look For

**Exact Duplicates:**

- Same title or very similar
- Same component
- Same symptoms

**Related Issues:**

- Same component, different symptom
- Similar root cause
- Part of same epic/feature

**Closed Issues:**

- Was this fixed before?
- Is this a regression?
- Why was it closed?

## Step 4: Compare & Decide

### Decision Tree

```
Found similar issue?
    ├─ No → [Create new issue]
    └─ Yes → Is it open?
           ├─ Yes → Is it the same issue?
           │        ├─ Yes → [Add comment to existing]
           │        └─ No → [Create new, link to similar]
           └─ No (closed) → Should reopen?
                    ├─ Yes → [Reopen with new info]
                    └─ No → [Create new, reference old]
```

### Similarity Assessment

Use `github_issues.py`:

```bash
python scripts/github_issues.py search \
  --issue '{"title": "Login fails", "body": "..."}' \
  --existing '[{existing issues JSON}]'
```

**Similarity Score:**

- 90-100%: Almost certainly duplicate
- 80-89%: Very likely duplicate, review manually
- 70-79%: Possibly related
- <70%: Different issue

### Reopen Decision Matrix

| Scenario                            | Action           | Confidence |
| ----------------------------------- | ---------------- | ---------- |
| Same bug, regression                | Reopen           | 95%        |
| Similar symptom, same component     | Reopen           | 85%        |
| Same user story, new implementation | Create new       | 80%        |
| Related but different root cause    | Create new, link | 90%        |
| Closed as won't-fix, new context    | Create new       | 100%       |

Use reopen checker:

```bash
python scripts/github_issues.py reopen-check \
  --new '{"title": "..."}' \
  --existing '{"number": 123, "state": "closed"}'
```

## Step 5: Take Action

### Action A: Create New Issue

**When:**

- No similar issue found
- Similar issue but different problem
- Closed issue was won't-fix
- Issue is complex enough to warrant separate tracking

**Process:**

1. Use appropriate template (bug/feature/enhancement)
2. Write clear, actionable title
3. Include all context
4. Add proper labels
5. Set priority
6. Link related issues
7. Assign to appropriate team/person if known
8. Add to milestone if applicable

**Quality Checklist:**

- [ ] Title is specific and searchable
- [ ] Description follows template
- [ ] Steps to reproduce included (bugs)
- [ ] Expected vs actual clearly stated
- [ ] Environment details provided
- [ ] Screenshots attached if relevant
- [ ] Proper labels applied
- [ ] Priority set based on impact
- [ ] Acceptance criteria clear

### Action B: Reopen Existing Issue

**When:**

- Confirmed regression
- Additional symptoms of same issue
- Original fix was incomplete
- Issue recurred under new conditions

**Process:**

1. Add comment explaining reopen reason
2. Include new client feedback
3. Add new reproduction steps if different
4. Update labels (remove `fixed`, add `regression`)
5. Set priority (often higher for regressions)
6. @mention original assignee
7. Link to new client report/ticket

**Reopen Comment Template:**

```markdown
## Reopening Issue

This issue is being reopened due to new client feedback indicating
the problem has recurred.

### New Report Date

[Date of feedback]

### New Context

[What's different about this occurrence]

### Client Feedback

[Paste relevant feedback]

### Additional Reproduction Steps

1. [Step 1]
2. [Step 2]

### Environment

[New environment details if different]

Original issue was closed on [date] in PR #[number].
The fix may have been incomplete or a regression was introduced.

cc @original-assignee
```

### Action C: Add to Existing Open Issue

**When:**

- Exact duplicate
- Additional context for same issue
- New reproduction steps for open issue

**Process:**

1. Add comment with new information
2. Thank client for reporting
3. Update severity if warranted
4. Add new labels if applicable
5. Upvote/react to show increased priority

**Comment Template:**

```markdown
## Additional Report

Thank you for the additional feedback. This appears to be the same
issue currently being tracked.

### New Information

[What's new from this report]

### Impact Update

This issue has now been reported by [X] clients/users.

### Additional Details

[Any new context, reproduction steps, or environment info]
```

### Action D: Skip (Mark as Duplicate)

**When:**

- Exact duplicate of open issue
- No new information
- Client issue already captured

**Process:**

1. Do NOT create new issue
2. Update internal tracker (if separate from GitHub)
3. Notify client their issue is being tracked
4. Provide link to existing issue if public

## Step 6: Follow-up & Monitoring

### After Creating/Reopening

**Immediate:**

- [ ] Notify client (if appropriate)
- [ ] Add to project board
- [ ] Tag in daily standup if high priority
- [ ] Update any dependent issues

**Within 24 Hours:**

- [ ] Verify issue was triaged
- [ ] Confirm priority assignment
- [ ] Check for any questions from dev team

**Ongoing:**

- [ ] Monitor for similar reports
- [ ] Update with new information
- [ ] Track resolution progress

### Metrics to Track

**Issue Quality:**

- Time to first response
- Number of clarification questions needed
- Issues requiring significant edits

**Process Efficiency:**

- Duplicate issues created (should be <5%)
- Issues closed as invalid (should be <10%)
- Issues requiring re-scoping (should be <15%)

**Impact:**

- Critical issues opened
- Average time to resolution
- Regression rate

## Best Practices

### Communication

**With Clients:**

- Acknowledge feedback quickly
- Set expectations on response time
- Provide updates on critical issues
- Thank them for detailed reports

**With Development Team:**

- Provide complete context
- Don't assume knowledge
- Link to relevant documentation
- Be available for questions

**With Product/Management:**

- Escalate critical issues immediately
- Provide impact analysis
- Suggest priorities based on user pain
- Report on trends

### Issue Hygiene

**Weekly:**

- Review `needs-triage` issues
- Close stale issues
- Update status on in-progress
- Check for duplicates

**Monthly:**

- Review closed issues for patterns
- Update templates based on feedback
- Analyze common rejection reasons
- Clean up old labels

### Handling Edge Cases

**Vague Feedback:**

1. Create draft/internal issue
2. Request clarification from client
3. Don't publish until clear
4. Document the clarification process

**Confidential Issues:**

1. Create private issue or use internal tracker
2. Sanitize before making public
3. Mark as `security` or `confidential`
4. Follow security disclosure process

**Disputed Issues:**

1. Document both perspectives
2. Bring in PM/tech lead
3. Create issue for investigation
4. Be objective, not defensive

**Feature vs Enhancement:**

1. When in doubt, label both
2. Let PM/PO decide during triage
3. Document the ambiguity
4. Err on side of calling it a feature

## Common Pitfalls to Avoid

❌ Creating duplicate issues without searching  
✅ Always search first, document search queries

❌ Combining multiple issues to save time  
✅ Split into atomic issues even if time-consuming

❌ Writing vague titles to match vague feedback  
✅ Clarify first, then write specific title

❌ Skipping environment details "everyone knows"  
✅ Always include complete environment

❌ Setting priority without understanding impact  
✅ Ask about impact, # of users affected

❌ Creating issues for every complaint  
✅ Verify it's actually a bug/valid request

❌ Reopening issues without new information  
✅ Only reopen with new evidence/context

## Templates for Common Scenarios

### Regression Issue

```markdown
Title: [REGRESSION] [Original issue description]

## Original Issue

Fixed in PR #[number] on [date]: [link to original issue]

## Regression Details

The issue has recurred as of [date] under the following conditions:
[describe new conditions]

## New Reproduction Steps

[List steps]

## Environment

[New environment if different]

## Root Cause Analysis Needed

This is the second occurrence - investigation needed to determine:

- Was the fix incomplete?
- New condition not covered by tests?
- Related but different bug?

## Severity

[Often elevated due to regression]
```

### Complex Feedback Breakdown

```markdown
[Create parent tracking issue]

Title: [Client Name] Feedback: [Date] - Multiple Issues

## Overview

Client provided feedback with multiple issues. This tracks the breakdown.

## Sub-Issues

- #[X] - [Issue 1 title]
- #[Y] - [Issue 2 title]
- #[Z] - [Issue 3 title]

## Original Feedback

[Paste original feedback]

## Status

- [x] All issues created and linked
- [ ] All issues triaged
- [ ] All issues assigned
```

This workflow ensures consistent, high-quality issue management that serves both the development team and clients effectively.
