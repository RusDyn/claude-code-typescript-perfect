# PRODUCTION INCIDENT - IMMEDIATE ACTION REQUIRED

## Current Status
- **Severity**: P0/P1/P2
- **Started**: [TIME]
- **Impact**: [USER COUNT] users affected
- **Symptoms**: [WHAT'S BROKEN]

## Immediate Actions Needed
1. **Stop the bleeding** - Mitigate user impact
2. **Gather data** - Logs, metrics, traces
3. **Find root cause** - Recent changes, dependencies
4. **Fix or rollback** - Fastest path to recovery
5. **Verify fix** - Confirm resolution

## Available Tools
- Rollback command: `npm run deploy:rollback`
- Emergency config: `npm run emergency:config`
- Feature flags: `npm run flags:disable -- FEATURE_NAME`
- Cache clear: `npm run cache:clear`

## Do NOT
- Make large changes
- Skip testing the fix
- Forget to document actions

FOCUS: User impact first, root cause second.