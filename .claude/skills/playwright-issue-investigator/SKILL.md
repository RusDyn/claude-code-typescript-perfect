---
name: playwright-issue-investigator
description: Debug Playwright tests and investigate issues with comprehensive tooling - capture screenshots on demand or failure, record videos, generate and analyze trace files, inspect network activity, analyze console logs, perform visual regression testing, and document bugs. Use when (1) Tests fail, (2) Investigating bugs, (3) Creating documentation screenshots, (4) Debugging flaky tests, (5) Analyzing performance issues, (6) Visual regression testing, (7) Network debugging. Focuses on investigation, debugging, and issue documentation.
---

# Playwright Issue Investigator

Debug and investigate test failures with comprehensive debugging tools.

## Related Skills

**Use with:** `playwright-test-builder` - For creating new tests and expanding coverage. Use this investigator skill when those tests fail or need debugging.

## When to Use This Skill

**Use playwright-issue-investigator when:**
- ✅ Tests are failing and you need to understand why
- ✅ Debugging flaky or intermittent test failures
- ✅ Capturing screenshots for bug reports or documentation
- ✅ Recording videos of test execution
- ✅ Analyzing trace files for detailed debugging
- ✅ Inspecting network requests and responses
- ✅ Performing visual regression testing
- ✅ Investigating performance issues

**Use playwright-test-builder instead when:**
- ❌ Creating new test files and test cases
- ❌ Setting up Page Object Model
- ❌ Organizing test structure
- ❌ Setting up test fixtures and database data
- ❌ Configuring CI/CD pipelines
- ❌ Planning test coverage strategy

**Workflow:** playwright-test-builder (create) → Run Tests → playwright-issue-investigator (debug failures)

## Quick Start

### Capture Screenshots

```typescript
// On test failure (automatic)
test.use({ screenshot: "only-on-failure" });

// On demand
await page.screenshot({ path: "screenshot.png" });

// Full page
await page.screenshot({ path: "full.png", fullPage: true });

// Element screenshot
await page.locator(".element").screenshot({ path: "element.png" });
```

### Record Videos

```typescript
// playwright.config.ts
use: {
  video: 'retain-on-failure', // or 'on', 'off', 'on-first-retry'
}

// Access video after test
test.afterEach(async ({}, testInfo) => {
  if (testInfo.status === 'failed') {
    const video = testInfo.attachments.find(a => a.name === 'video');
    console.log('Video:', video?.path);
  }
});
```

### Generate Traces

```typescript
// Auto-capture on retry
use: {
  trace: 'on-first-retry', // or 'on', 'off', 'retain-on-failure'
}

// View trace
// npx playwright show-trace trace.zip
```

## Core Investigation Tools

### 1. Screenshot Strategies

**Failure Screenshots**:

```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status === "failed") {
    await page.screenshot({
      path: `screenshots/${testInfo.title}-failure.png`,
      fullPage: true,
    });
  }
});
```

**Documentation Screenshots**:

```typescript
test("capture user flow", async ({ page }) => {
  await page.goto("/");
  await page.screenshot({ path: "docs/step1-homepage.png" });

  await page.click("button");
  await page.screenshot({ path: "docs/step2-clicked.png" });
});
```

### 2. Video Recording

```typescript
// playwright.config.ts
use: {
  video: {
    mode: 'retain-on-failure',
    size: { width: 1280, height: 720 }
  }
}
```

### 3. Trace Analysis

```bash
# Generate trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

Traces include:

- Network requests
- DOM snapshots
- Console logs
- Screenshots
- Source code

### 4. Console Log Capture

```typescript
test("capture console", async ({ page }) => {
  const logs: string[] = [];

  page.on("console", (msg) => logs.push(msg.text()));

  await page.goto("/");

  console.log("Console logs:", logs);
});
```

### 5. Network Inspection

```typescript
test("monitor API calls", async ({ page }) => {
  // Listen to requests
  page.on("request", (request) => {
    console.log("Request:", request.url());
  });

  // Listen to responses
  page.on("response", (response) => {
    console.log("Response:", response.url(), response.status());
  });

  // Wait for specific API call
  const response = await page.waitForResponse((resp) =>
    resp.url().includes("/api/users"),
  );

  console.log("API Response:", await response.json());
});
```

## Debugging Techniques

### Debug Mode

```bash
# Run in debug mode
npx playwright test --debug

# Debug specific test
npx playwright test tests/login.spec.ts --debug

# Debug from specific line
# Add: await page.pause();
```

### Headed Mode

```bash
# See browser
npx playwright test --headed

# Slow down
npx playwright test --headed --slow-mo=1000
```

### Inspector

```typescript
// Pause execution
await page.pause();

// Step through
await page.screenshot(); // Take screenshot at this point
```

## Visual Regression Testing

### Setup

```typescript
test("visual regression", async ({ page }) => {
  await page.goto("/");

  // Compare against baseline
  await expect(page).toHaveScreenshot("homepage.png");
});

// First run creates baseline
// Subsequent runs compare
```

### Configuration

```typescript
// playwright.config.ts
use: {
  screenshot: 'only-on-failure',
}

expect: {
  toHaveScreenshot: {
    maxDiffPixels: 100,  // Allow small differences
  },
}
```

## Reference Documentation

- **references/debugging-guide.md** - Complete debugging techniques
- **references/trace-analysis.md** - Trace file interpretation
- **references/visual-regression.md** - Visual testing strategies
- **references/network-debugging.md** - Network inspection and mocking

## Common Investigation Patterns

### Pattern 1: Investigate Flaky Test

1. Enable trace on retry
2. Run test multiple times
3. Analyze trace for timing issues
4. Check network requests
5. Review console logs

### Pattern 2: Debug Visual Issue

1. Take screenshot at each step
2. Compare with expected
3. Check element visibility
4. Verify CSS/styling
5. Test on different viewports

### Pattern 3: Investigate Performance

1. Record video
2. Analyze trace timeline
3. Check network waterfall
4. Measure load times
5. Identify bottlenecks

## Best Practices

1. **Always capture on failure** - Screenshots and videos
2. **Use traces for complex issues** - Complete picture
3. **Monitor network** - Catch API issues
4. **Capture console logs** - JavaScript errors
5. **Visual regression** - Catch UI changes
6. **Document with screenshots** - For bug reports

This skill helps you quickly identify and resolve test failures and bugs.
