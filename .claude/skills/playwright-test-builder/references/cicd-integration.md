# CI/CD Integration Guide

## GitHub Actions

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npx playwright test

      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Docker Setup

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-jammy

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

CMD ["npx", "playwright", "test"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  tests:
    build: .
    environment:
      - BASE_URL=http://app:3000
    volumes:
      - ./tests:/app/tests
      - ./playwright-report:/app/playwright-report
```

## Run Commands

```bash
# Run all tests
npx playwright test

# Run specific test
npx playwright test tests/login.spec.ts

# Run in headed mode
npx playwright test --headed

# Run with specific browser
npx playwright test --project=chromium

# Run in parallel
npx playwright test --workers=4

# Debug
npx playwright test --debug

# Generate report
npx playwright show-report
```
