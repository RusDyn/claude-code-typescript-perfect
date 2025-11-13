# Trace Analysis

## Generate Traces

```bash
# On all tests
npx playwright test --trace on

# On first retry
npx playwright test --trace on-first-retry

# In config
use: {
  trace: 'retain-on-failure',
}
```

## View Traces

```bash
npx playwright show-trace trace.zip
```

## What Traces Include

- **Timeline**: See execution flow
- **Network**: All requests/responses
- **Console**: All console logs
- **Snapshots**: DOM at each action
- **Screenshots**: Visual state
- **Source**: Test code

## Analyzing Failures

1. Open trace in viewer
2. Find failing action
3. Check network tab
4. Review console logs
5. Inspect DOM snapshot
6. Identify root cause

Traces are the most powerful debugging tool.
