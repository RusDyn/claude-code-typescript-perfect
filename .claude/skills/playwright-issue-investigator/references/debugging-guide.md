# Debugging Guide

## Debug Mode

```bash
npx playwright test --debug
```

Opens Playwright Inspector with:

- Step through execution
- Inspect selectors
- View console logs
- Generate code

## Breakpoints

```typescript
// Pause at this point
await page.pause();

// Continue manually in inspector
```

## Headed Mode

```bash
# See browser while running
npx playwright test --headed

# Slow down actions
npx playwright test --headed --slow-mo=1000
```

## Console Logs

```typescript
page.on("console", (msg) => console.log("PAGE LOG:", msg.text()));
page.on("pageerror", (err) => console.log("PAGE ERROR:", err));
```

## Network Debugging

```typescript
// Log all requests
page.on("request", (req) => console.log(">>", req.method(), req.url()));
page.on("response", (res) => console.log("<<", res.status(), res.url()));

// Mock responses
await page.route("**/api/users", (route) => {
  route.fulfill({ body: JSON.stringify([{ id: 1, name: "Test" }]) });
});
```

## Common Issues

**Element not found**: Check selector, wait for element
**Flaky tests**: Add proper waits, check race conditions
**Timeout**: Increase timeout or fix slow operations
