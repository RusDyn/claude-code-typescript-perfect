---
name: playwright-test-builder
description: Build comprehensive Playwright E2E test suites with best practices - create well-structured tests, implement Page Object Model, manage test data and fixtures, set up database connections, organize test coverage, and integrate with CI/CD. Use when (1) Building new test suites, (2) Expanding test coverage, (3) Writing E2E tests, (4) Setting up test infrastructure, (5) Organizing test code, (6) Creating page objects, (7) Managing test data. Focuses on test creation, organization, and coverage strategies.
---

# Playwright Test Suite Builder

Comprehensive toolkit for building maintainable E2E test suites with Playwright.

## Quick Start

### 1. Use Helper Functions in Tests

```typescript
import { test, expect } from '@playwright/test'
import {
  safeClick,
  safeType,
  fillForm,
  login,
  expectVisible,
} from './.claude/skills/playwright-test-builder/scripts/test-helpers'

test('user can submit form', async ({ page }) => {
  await page.goto('/contact')

  await fillForm(
    page,
    {
      name: 'John Doe',
      email: 'john@example.com',
      message: 'Test message',
    },
    {
      submitButton: 'button[type="submit"]',
    }
  )

  await expectVisible(page, '.success-message')
})
```

### 2. Generate Test Scaffolding

```bash
# Generate a basic test file
python scripts/generate_test_scaffold.py '{
  "type": "test",
  "test_name": "Login Flow",
  "page_object": "LoginPage"
}'

# Generate a Page Object
python scripts/generate_test_scaffold.py '{
  "type": "page",
  "page_name": "Login",
  "elements": [
    {"name": "emailInput", "selector": "input[name=email]", "type": "input"}
  ]
}'
```

### 3. Analyze Coverage

```bash
python scripts/analyze_coverage.py ./tests ecommerce ./pages
```

## Core Concepts

### Selector Priority

1. data-testid
2. ARIA roles
3. Visible text
4. CSS (last resort)

### Page Object Pattern

```typescript
export class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email)
    await this.page.fill('[name="password"]', password)
    await this.page.click('button[type="submit"]')
  }
}
```

## Reference Documentation

- **references/test-patterns.md** - Test patterns, selectors, waits, assertions
- **references/page-object-model.md** - POM implementation guide
- **references/database-fixtures.md** - Database setup and test data
- **references/cicd-integration.md** - CI/CD workflows

## Helper Functions

Located in `scripts/test-helpers.ts`, these utilities make tests more reliable:

### Interaction Helpers

- `safeClick(page, selector, options)` - Click with retry logic
- `safeType(page, selector, text, options)` - Type with auto-clear
- `fillForm(page, formData, options)` - Fill multiple fields at once
- `scrollToElement(page, selector)` - Scroll element into view

### Waiting Helpers

- `waitForVisible(page, selector)` - Wait for element visibility
- `waitForHidden(page, selector)` - Wait for element to hide
- `waitForText(page, text)` - Wait for text to appear
- `waitForNetworkIdle(page)` - Wait for network activity to settle

### Data Helpers

- `getText(page, selector)` - Get text content safely
- `elementExists(page, selector)` - Check if element exists
- `extractTableData(page, tableSelector)` - Extract table to JSON

### Debugging Helpers

- `captureConsoleLogs(page, filter)` - Capture console output
- `monitorNetwork(page, urlFilter)` - Monitor API calls

### Authentication

- `login(page, credentials, options)` - Reusable login helper

### Assertion Helpers

- `expectVisible(page, selector)` - Assert visibility
- `expectHidden(page, selector)` - Assert hidden
- `expectText(page, selector, text)` - Assert text content
- `expectUrl(page, url)` - Assert current URL

## Best Practices

1. **Test independence** - Each test should run standalone
2. **Meaningful names** - Describe what is being tested
3. **Stable selectors** - Use data-testid, ARIA roles, or semantic selectors
4. **Clean test data** - Reset database state between tests
5. **Use Page Objects** - Encapsulate page interactions
6. **Use helper functions** - Import from test-helpers.ts for reliability
7. **Handle waits properly** - Use appropriate wait strategies
8. **Capture errors** - Screenshots and logs on failure

## Integration with Other Skills

- **playwright-automation**: Use for quick ad-hoc automation before building formal tests
- **playwright-issue-investigator**: Use for debugging test failures with traces and network analysis

Start building comprehensive test coverage with confidence!
