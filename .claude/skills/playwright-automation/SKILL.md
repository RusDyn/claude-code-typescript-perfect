---
name: playwright-automation
description: Ad-hoc browser automation using Playwright - automate website interactions, scrape data, validate functionality, capture screenshots, and perform quick browser-based tasks without writing full test suites. Use when (1) Need quick browser automation, (2) Exploring website behavior, (3) Automating repetitive browser tasks, (4) Data extraction, (5) Testing ideas quickly, (6) Creating proof-of-concepts. Complements playwright-test-builder (structured tests) and playwright-issue-investigator (debugging).
---

# Playwright Browser Automation

Quick, flexible browser automation for ad-hoc tasks without the overhead of full test suites.

## When to Use This Skill

- **Quick automation**: Need to automate something fast without full test infrastructure
- **Exploration**: Investigating how a website works or responds
- **Data extraction**: Scraping or extracting data from web pages
- **Proof of concept**: Testing an automation idea before building formal tests
- **One-off tasks**: Automating repetitive browser tasks

For structured E2E test suites, use `playwright-test-builder`.
For debugging existing tests, use `playwright-issue-investigator`.

## Quick Start

### 1. Detect Running Servers (Recommended)

```bash
node .claude/skills/playwright-automation/scripts/detect-servers.js
```

This auto-detects:

- Next.js dev server (port 3000)
- Vite servers
- Other common dev servers

### 2. Create Automation Script

Create a script in `/tmp` for automatic cleanup:

```typescript
// /tmp/my-automation.js
const { chromium } = require('playwright')
const {
  safeClick,
  safeType,
  takeScreenshot,
} = require('.claude/skills/playwright-automation/scripts/helpers.js')

;(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 })
  const page = await browser.newPage()

  try {
    // Your automation here
    await page.goto('http://localhost:3000')
    await safeClick(page, 'button:has-text("Login")')
    await safeType(page, 'input[name="email"]', 'test@example.com')

    await takeScreenshot(page, 'login-form')

    console.log('Automation completed successfully!')
  } catch (error) {
    console.error('Automation failed:', error)
    await takeScreenshot(page, 'error')
  } finally {
    await browser.close()
  }
})()
```

### 3. Run Your Script

```bash
node /tmp/my-automation.js
```

## Helper Functions

Located in `scripts/helpers.js`:

### safeClick(page, selector, options)

Clicks with retry logic and waits for element to be ready.

```typescript
await safeClick(page, 'button.submit', { timeout: 5000 })
```

### safeType(page, selector, text, options)

Types with automatic clear and error handling.

```typescript
await safeType(page, 'input[name="email"]', 'user@example.com')
```

### takeScreenshot(page, name, options)

Captures timestamped screenshots with error handling.

```typescript
await takeScreenshot(page, 'homepage') // Saves as homepage-{timestamp}.png
await takeScreenshot(page, 'full-page', { fullPage: true })
```

### handleCookieBanner(page)

Automatically dismisses common cookie consent banners.

```typescript
await handleCookieBanner(page)
```

### extractTableData(page, tableSelector)

Extracts data from HTML tables into JSON.

```typescript
const data = await extractTableData(page, 'table.users')
console.log(JSON.stringify(data, null, 2))
```

### waitForNetworkIdle(page, timeout)

Waits for network activity to settle.

```typescript
await page.goto('http://localhost:3000')
await waitForNetworkIdle(page, 2000)
```

## Common Automation Patterns

### Pattern 1: Login Flow Testing

```typescript
const { chromium } = require('playwright')
const { safeClick, safeType } = require('./scripts/helpers.js')

;(async () => {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()

  await page.goto('http://localhost:3000/login')

  await safeType(page, 'input[name="email"]', 'admin@test.com')
  await safeType(page, 'input[name="password"]', 'password123')
  await safeClick(page, 'button[type="submit"]')

  await page.waitForURL('**/dashboard')
  console.log('Login successful!')

  await browser.close()
})()
```

### Pattern 2: Form Filling Automation

```typescript
const formData = {
  name: 'John Doe',
  email: 'john@example.com',
  phone: '+1234567890',
  message: 'Test message',
}

for (const [field, value] of Object.entries(formData)) {
  await safeType(page, `input[name="${field}"]`, value)
}

await safeClick(page, 'button[type="submit"]')
```

### Pattern 3: Screenshot Documentation

```typescript
const steps = [
  { action: () => page.goto('http://localhost:3000'), name: 'homepage' },
  {
    action: () => safeClick(page, 'nav a:has-text("Products")'),
    name: 'products',
  },
  {
    action: () => safeClick(page, 'button:has-text("Add to Cart")'),
    name: 'cart',
  },
]

for (const step of steps) {
  await step.action()
  await takeScreenshot(page, step.name)
}
```

### Pattern 4: Data Extraction

```typescript
const { extractTableData } = require('./scripts/helpers.js')

await page.goto('http://localhost:3000/users')
const users = await extractTableData(page, 'table.user-list')

// Save to file
const fs = require('fs')
fs.writeFileSync('/tmp/users.json', JSON.stringify(users, null, 2))
```

### Pattern 5: Multi-Viewport Testing

```typescript
const viewports = [
  { width: 1920, height: 1080, name: 'desktop' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 375, height: 667, name: 'mobile' },
]

for (const viewport of viewports) {
  await page.setViewportSize({ width: viewport.width, height: viewport.height })
  await page.goto('http://localhost:3000')
  await takeScreenshot(page, `${viewport.name}-homepage`)
}
```

## Configuration Defaults

### Browser Visibility

- **Default**: `headless: false` (visible browser for debugging)
- **Slow motion**: `slowMo: 100` (makes actions visible)
- **Use headless** only when explicitly needed for speed

```typescript
// Visible browser (default for development)
const browser = await chromium.launch({
  headless: false,
  slowMo: 100,
})

// Headless (for production automation)
const browser = await chromium.launch({
  headless: true,
})
```

### Timeouts

- Navigation: 30s (configurable)
- Action: 10s (configurable)
- Network idle: 2s (recommended)

## Best Practices

1. **Use /tmp for scripts** - Automatic cleanup, no codebase clutter
2. **Start with visible browser** - Debug visually before going headless
3. **Add slowMo for demos** - Makes automation easier to follow
4. **Use helper functions** - More reliable than raw Playwright
5. **Handle errors gracefully** - Always use try-catch blocks
6. **Take screenshots on error** - Essential for debugging
7. **Parameterize URLs** - Use constants at top of file
8. **Log progress** - Use console.log for visibility

## Integration with Other Skills

### Before Building Tests

Use this skill to explore and validate automation approaches before creating formal test suites with `playwright-test-builder`.

### For Debugging

When you find issues, use `playwright-issue-investigator` for comprehensive debugging with traces and network analysis.

### Workflow

1. **Explore** with playwright-automation (this skill)
2. **Build tests** with playwright-test-builder
3. **Debug issues** with playwright-issue-investigator

## Example Scripts

See `assets/examples/` for complete working examples:

- Login automation
- Form submission
- Data extraction
- Screenshot generation
- Responsive testing

## Reference Documentation

- **references/automation-patterns.md** - Common automation patterns
- **references/selector-strategies.md** - Finding elements reliably
- **references/error-handling.md** - Robust error handling

Start automating browser tasks quickly and efficiently!
