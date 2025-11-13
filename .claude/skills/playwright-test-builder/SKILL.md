---
name: playwright-test-builder
description: Build comprehensive Playwright E2E test suites with best practices - create well-structured tests, implement Page Object Model, manage test data and fixtures, set up database connections, organize test coverage, and integrate with CI/CD. Use when (1) Building new test suites, (2) Expanding test coverage, (3) Writing E2E tests, (4) Setting up test infrastructure, (5) Organizing test code, (6) Creating page objects, (7) Managing test data. Focuses on test creation, organization, and coverage strategies.
---

# Playwright Test Suite Builder

Comprehensive toolkit for building maintainable E2E test suites with Playwright.

## Related Skills

**Use with:** `playwright-issue-investigator` - When tests fail or become flaky, use the investigator skill to debug with screenshots, traces, and network analysis.

## When to Use This Skill

**Use playwright-test-builder when:**
- ✅ Building new test suites from scratch
- ✅ Expanding test coverage
- ✅ Implementing Page Object Model
- ✅ Setting up test infrastructure and fixtures
- ✅ Organizing test code structure
- ✅ Creating database test data
- ✅ Setting up CI/CD integration

**Use playwright-issue-investigator instead when:**
- ❌ Tests are failing and you need to debug
- ❌ Investigating flaky tests
- ❌ Capturing screenshots or videos
- ❌ Analyzing network requests
- ❌ Performing visual regression testing
- ❌ Creating bug documentation

**Workflow:** playwright-test-builder (create) → Run Tests → playwright-issue-investigator (debug failures)

## Quick Start

### 1. Generate Test Scaffolding

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

### 2. Analyze Coverage

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
    await this.page.fill('[name="email"]', email);
    await this.page.fill('[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }
}
```

## Reference Documentation

- **references/test-patterns.md** - Test patterns, selectors, waits, assertions
- **references/page-object-model.md** - POM implementation guide
- **references/database-fixtures.md** - Database setup and test data
- **references/cicd-integration.md** - CI/CD workflows

## Best Practices

1. Test independence
2. Meaningful names
3. Stable selectors
4. Clean test data
5. Use Page Objects

Start building comprehensive test coverage with confidence!
