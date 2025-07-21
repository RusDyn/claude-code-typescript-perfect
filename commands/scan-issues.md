# Scan Codebase for Issues: $ARGUMENTS

## Scanning Process

1. **Code Quality Scan**
   Use filesystem to analyze code for:
   - TODO/FIXME/HACK comments
   - TypeScript `@ts-ignore` or `@ts-expect-error`
   - Disabled linting rules
   - Console.log statements
   - Hardcoded values that should be config
   - Missing error handling
   - Performance bottlenecks (O(n²) loops, etc.)

2. **Security Scan**
   Check for:
   - Hardcoded credentials or API keys
   - SQL injection vulnerabilities
   - Missing input validation
   - Exposed sensitive data in logs
   - Missing authentication checks

3. **Technical Debt Scan**
   Identify:
   - Deprecated API usage
   - Missing tests for critical paths
   - Overly complex functions (high cyclomatic complexity)
   - Duplicate code blocks
   - Inconsistent patterns

## GitHub Issue Check

For each found issue:
1. Use github mcp to search existing issues
2. Check if issue already reported (by title/label match)
3. If exists: add comment with additional context
4. If new: create issue with proper formatting

## Issue Format Template

Title: [Type] Brief description - File:Line
Labels: bug/tech-debt/security/performance, priority-level
Body:
- **Location**: `src/path/to/file.ts:42`
- **Type**: [Issue category]
- **Description**: [What's wrong]
- **Impact**: [Who/what is affected]
- **Suggested Fix**: [Proposed solution]
- **Code Context**:
  ```typescript
  [relevant code snippet]
  ```