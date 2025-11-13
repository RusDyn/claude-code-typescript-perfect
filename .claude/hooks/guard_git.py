#!/usr/bin/env python3
import sys, json, re

payload = json.load(sys.stdin)
tool = payload.get("tool_name", "")
cmd = (payload.get("tool_input") or {}).get("command", "").strip()

if tool.lower() == "bash" and re.search(r"^git\s+commit\b.*\b--no-verify\b", cmd):
    sys.stderr.write("❌ git commit --no-verify is blocked. Remove flag and fix hooks.\n")
    sys.exit(2)

sys.exit(0)
