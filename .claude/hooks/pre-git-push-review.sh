#!/bin/bash
# Claude Code Hook: Pre-Git-Push Code Review
# This hook runs Codex CLI to perform automated code review before pushing

set -euo pipefail

# Cleanup temp files on exit
TEMP_FILES=()
cleanup() {
  for temp_file in "${TEMP_FILES[@]}"; do
    [[ -f "$temp_file" ]] && rm -f "$temp_file"
  done
}
trap cleanup EXIT INT TERM

# Read hook input from stdin
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
CWD=$(echo "$INPUT" | jq -r '.cwd')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')

# Validate CWD is absolute path and exists
if [[ ! "$CWD" =~ ^/ ]] || [[ ! -d "$CWD" ]]; then
  echo '{
    "permissionDecision": "allow",
    "systemMessage": "⚠️  Invalid working directory. Skipping code review."
  }'
  exit 0
fi

# Extract git push command details
COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty')

# Validate command is a git push command (basic sanitization)
if [[ -z "$COMMAND" ]]; then
  echo '{"permissionDecision": "allow"}'
  exit 0
fi

# Only process git push commands
if [[ ! "$COMMAND" =~ ^git\ push ]]; then
  # Not a git push, allow it to continue
  echo '{"permissionDecision": "allow"}'
  exit 0
fi

# Check if codex is available
if ! command -v codex &> /dev/null; then
  # Codex not installed, warn but allow push
  echo '{
    "permissionDecision": "allow",
    "systemMessage": "⚠️  Codex CLI not found. Install with: npm install -g @codex/cli\nSkipping code review..."
  }'
  exit 0
fi

# Get the current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

# Determine the base for diff comparison
# Strategy: Find what commits are being pushed by comparing with remote
DIFF_BASE=""

# Try to get the upstream tracking branch
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "")

if [[ -n "$UPSTREAM" ]]; then
  # Branch has upstream tracking, use it
  DIFF_BASE="@{u}"
  echo "📍 Comparing against upstream: $UPSTREAM" >&2
else
  # No upstream, try to extract remote branch from command or use current branch name
  REMOTE_BRANCH=$(echo "$COMMAND" | grep -oP '(?<=origin )[^ ]+' || echo "$CURRENT_BRANCH")

  # Check if remote branch exists
  if git rev-parse --verify "origin/$REMOTE_BRANCH" &> /dev/null; then
    DIFF_BASE="origin/$REMOTE_BRANCH"
    echo "📍 Comparing against remote branch: origin/$REMOTE_BRANCH" >&2
  else
    # Remote branch doesn't exist, this is a new branch
    # Compare against main/master to get all changes
    if git rev-parse --verify "origin/main" &> /dev/null; then
      DIFF_BASE="origin/main"
      echo "📍 New branch detected, comparing against: origin/main" >&2
    elif git rev-parse --verify "origin/master" &> /dev/null; then
      DIFF_BASE="origin/master"
      echo "📍 New branch detected, comparing against: origin/master" >&2
    else
      # Fallback: compare last commit
      DIFF_BASE="HEAD~1"
      echo "📍 No remote found, comparing against: HEAD~1" >&2
    fi
  fi
fi

# Create temporary files for review results
REVIEW_OUTPUT=$(mktemp)
TEMP_FILES+=("$REVIEW_OUTPUT")

# Validate and set schema path (prevent path traversal)
SCHEMA_PATH="$CWD/.claude/hooks/codex-output-schema.json"
if [[ ! "$SCHEMA_PATH" =~ ^"$CWD" ]]; then
  echo '{
    "permissionDecision": "allow",
    "systemMessage": "⚠️  Invalid schema path. Skipping code review."
  }'
  exit 0
fi

# Check if schema exists
if [[ ! -f "$SCHEMA_PATH" ]]; then
  echo '{
    "permissionDecision": "allow",
    "systemMessage": "⚠️  Codex schema not found at: '"$SCHEMA_PATH"'\nSkipping code review..."
  }'
  exit 0
fi

# Get commit info and changed files
COMMITS_COUNT=$(git rev-list "$DIFF_BASE"..HEAD 2>/dev/null | wc -l)
CHANGED_FILES=$(git diff --name-only "$DIFF_BASE"..HEAD 2>/dev/null)
FILES_COUNT=$(echo "$CHANGED_FILES" | wc -l)

# Check if there are any changes
if [[ -z "$CHANGED_FILES" ]]; then
  echo '{
    "permissionDecision": "allow",
    "systemMessage": "ℹ️  No files changed between '"$DIFF_BASE"' and HEAD.\nBranch is up-to-date with remote. Skipping code review."
  }' | jq -c
  exit 0
fi

echo "📊 Commits: $COMMITS_COUNT | Files changed: $FILES_COUNT" >&2
echo "📝 Changed files:" >&2
echo "$CHANGED_FILES" | sed 's/^/  - /' >&2

# Get commit messages for context
COMMIT_MESSAGES=$(git log --oneline "$DIFF_BASE"..HEAD 2>/dev/null)

# Create review prompt - Codex will access files directly from the repository
REVIEW_PROMPT="You are a code reviewer analyzing changes about to be pushed to the repository.

**REPOSITORY ACCESS**: You have read-only access to this Git repository. Review the changed files by reading them directly.

**CHANGES TO REVIEW**:
Branch: $CURRENT_BRANCH
Comparing: $DIFF_BASE..HEAD
Commits: $COMMITS_COUNT

Changed files:
$CHANGED_FILES

Recent commits:
$COMMIT_MESSAGES

**REVIEW FOCUS**:
- **Correctness**: Logic errors, bugs, edge cases
- **Security**: Vulnerabilities, data exposure, injection risks
- **Performance**: Inefficiencies, potential bottlenecks
- **Maintainability**: Code clarity, documentation, patterns
- **Best Practices**: TypeScript standards, React patterns, Next.js conventions

**IMPORTANT GUIDELINES**:
- Read the changed files from the repository to see the actual code
- Use 'git diff $DIFF_BASE..HEAD' to see what changed
- Only flag actionable issues with EXACT file paths and line numbers
- Avoid trivial style-only comments or formatting nitpicks
- Focus on issues that could cause bugs or security vulnerabilities
- Prioritize critical and high-priority issues that would break functionality

Provide your review in the structured JSON format specified by the output schema."

# Run Codex code review with repository access
echo "🔍 Running Codex code review on $FILES_COUNT files..." >&2

# Codex outputs header info, we need only the last line which is the JSON
CODEX_RAW_OUTPUT=$(mktemp)
TEMP_FILES+=("$CODEX_RAW_OUTPUT")

echo "🤖 Calling Codex CLI with repository access" >&2
echo "   Working directory: $CWD" >&2
echo "   Schema: $SCHEMA_PATH" >&2

# Run codex exec with:
# --cd: Set working directory to the repository
# --output-schema: Use structured JSON output
# Codex runs in read-only sandbox by default, which is perfect for code review
if codex exec --cd "$CWD" "$REVIEW_PROMPT" --output-schema "$SCHEMA_PATH" > "$CODEX_RAW_OUTPUT" 2>&1; then
  # Save raw output for debugging
  cp "$CODEX_RAW_OUTPUT" "$CWD/.claude/hooks/codex-raw-output.log"

  # Extract only the last line which contains the JSON output
  tail -n 1 "$CODEX_RAW_OUTPUT" > "$REVIEW_OUTPUT"

  # Verify JSON is valid
  if ! jq empty "$REVIEW_OUTPUT" 2>/dev/null; then
    echo "⚠️  Warning: Codex output is not valid JSON" >&2
    echo "Raw output:" >&2
    cat "$CODEX_RAW_OUTPUT" >&2
    # Save failed output for debugging
    cp "$CODEX_RAW_OUTPUT" "$CWD/.claude/hooks/codex-failed-output.log"
    echo '{
      "permissionDecision": "allow",
      "systemMessage": "⚠️  Codex returned invalid JSON. Raw output saved to .claude/hooks/codex-failed-output.log\nProceeding with push..."
    }'
    exit 0
  fi

  # Save parsed JSON output
  cp "$REVIEW_OUTPUT" "$CWD/.claude/hooks/last-review.json"

  # Parse review results
  FINDINGS_COUNT=$(jq -r '.findings | length' "$REVIEW_OUTPUT" 2>/dev/null || echo "0")
  OVERALL_CORRECTNESS=$(jq -r '.overall_correctness' "$REVIEW_OUTPUT" 2>/dev/null || echo "uncertain")
  CONFIDENCE=$(jq -r '.overall_confidence_score' "$REVIEW_OUTPUT" 2>/dev/null || echo "0")
  SUMMARY=$(jq -r '.summary // "No summary provided"' "$REVIEW_OUTPUT" 2>/dev/null)

  # Build review message
  REVIEW_MESSAGE="📊 Code Review Complete\n\n"
  CONFIDENCE_PCT=$(awk "BEGIN {print int($CONFIDENCE * 100)}")
  REVIEW_MESSAGE+="Status: $OVERALL_CORRECTNESS (confidence: ${CONFIDENCE_PCT}%)\n"
  REVIEW_MESSAGE+="Issues found: $FINDINGS_COUNT\n\n"

  if [[ "$SUMMARY" != "null" && "$SUMMARY" != "No summary provided" ]]; then
    REVIEW_MESSAGE+="Summary: $SUMMARY\n\n"
  fi

  # Show critical and high priority issues
  CRITICAL_ISSUES=$(jq -r '.findings[] | select(.priority == "critical" or .priority == "high") | "- [\(.priority | ascii_upcase)] \(.title)\n  File: \(.code_location.file_path):\(.code_location.line_start)-\(.code_location.line_end)\n  \(.body)\n"' "$REVIEW_OUTPUT" 2>/dev/null || echo "")

  if [[ -n "$CRITICAL_ISSUES" ]]; then
    REVIEW_MESSAGE+="🚨 High Priority Issues:\n$CRITICAL_ISSUES\n"
  fi

  # Check if push should be blocked
  BLOCK_PUSH=false
  CRITICAL_COUNT=$(jq -r '[.findings[] | select(.priority == "critical")] | length' "$REVIEW_OUTPUT" 2>/dev/null || echo "0")

  if [[ "$OVERALL_CORRECTNESS" == "incorrect" ]] || [[ "$CRITICAL_COUNT" -gt 0 ]]; then
    BLOCK_PUSH=true

    # Build detailed feedback for Claude
    FEEDBACK_MESSAGE="❌ Code Review Failed - Critical Issues Found\n\n"
    FEEDBACK_MESSAGE+="📊 Summary:\n"
    FEEDBACK_MESSAGE+="- Status: $OVERALL_CORRECTNESS\n"
    FEEDBACK_MESSAGE+="- Confidence: ${CONFIDENCE_PCT}%\n"
    FEEDBACK_MESSAGE+="- Total Issues: $FINDINGS_COUNT\n"
    FEEDBACK_MESSAGE+="- Critical Issues: $CRITICAL_COUNT\n\n"
    FEEDBACK_MESSAGE+="📋 Issues to Fix:\n\n"

    # Add all findings to feedback
    FEEDBACK_MESSAGE+="$CRITICAL_ISSUES"

    FEEDBACK_MESSAGE+="\n💡 Next Steps:\n"
    FEEDBACK_MESSAGE+="1. Review the issues above\n"
    FEEDBACK_MESSAGE+="2. Fix the code in the affected files\n"
    FEEDBACK_MESSAGE+="3. Retry the git push command\n\n"
    FEEDBACK_MESSAGE+="Full review saved to: .claude/hooks/last-review.json"

    # Use JSON with permissionDecision: deny
    # This blocks the tool call AND shows the reason to Claude (who can then fix issues)
    jq -nc \
      --arg reason "$(echo -e "$FEEDBACK_MESSAGE")" \
      --arg summary "Code review found $CRITICAL_COUNT critical issue(s)" \
      '{
        "permissionDecision": "deny",
        "permissionDecisionReason": $reason,
        "systemMessage": $summary
      }'

    exit 0  # Exit 0 with permissionDecision: deny blocks the command but allows Claude to continue
  else
    REVIEW_MESSAGE+="\n✅ Code review passed. Safe to push.\n"
    REVIEW_MESSAGE+="Review saved to: .claude/hooks/last-review.json\n"

    jq -nc \
      --arg msg "$(echo -e "$REVIEW_MESSAGE")" \
      '{
        "permissionDecision": "allow",
        "systemMessage": $msg
      }'

    exit 0
  fi
else
  # Codex execution failed
  ERROR_MSG=$(cat "$CODEX_RAW_OUTPUT" 2>/dev/null || echo "Unknown error")

  # Save failed execution output for debugging
  if [[ -f "$CODEX_RAW_OUTPUT" ]]; then
    cp "$CODEX_RAW_OUTPUT" "$CWD/.claude/hooks/codex-failed-execution.log"
  fi

  jq -nc \
    --arg err "$ERROR_MSG" \
    '{
      "permissionDecision": "allow",
      "systemMessage": ("⚠️  Codex code review failed: " + $err + "\nOutput saved to .claude/hooks/codex-failed-execution.log\nProceeding with push...")
    }'

  exit 0
fi
