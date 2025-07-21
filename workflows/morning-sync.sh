#!/bin/bash
# Start fresh each day
claude --new-session

# Load project context
"Review recent commits and understand what changed:
1. Use github mcp to check recent PRs
2. Use filesystem to scan for TODOs
3. Summarize key areas needing attention"

# Plan the day
"Based on the review, create a prioritized task list
focusing on highest-impact work first"