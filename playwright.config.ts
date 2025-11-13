import { defineConfig, devices } from '@playwright/test'

/**
 * Playwright E2E Test Configuration
 *
 * Unified configuration for all E2E tests.
 * Uses MSW mocks for reliable, fast testing.
 * Run manually with 'npm run e2e' or in CI/CD pipeline.
 */
export default defineConfig({
  testDir: './test/e2e',

  // Global setup and teardown
  globalSetup: './test/e2e/global-setup.ts',
  globalTeardown: './test/e2e/global-teardown.ts',

  // Test execution settings
  fullyParallel: true,
  forbidOnly: !!process.env['CI'],
  retries: process.env['CI'] ? 2 : 0,
  workers: process.env['CI'] ? 1 : 2, // Limit workers to prevent dev server crashes
  timeout: 30000, // 30 second timeout for most tests

  // Reporter configuration
  reporter: process.env['CI'] ? 'github' : 'list',

  // Global test settings
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 10000,
  },

  // Browser projects
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      timeout: 45000, // Firefox can be slower
    },
  ],

  // Dev server configuration for E2E tests
  // Automatically starts dev server if not already running
  // If server is already running (manual start), reuses it (faster workflow)
  // If no server is running, starts a new one (CI and fresh local runs)
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: true, // Always try to reuse, start fresh if none exists
    timeout: 120000,
    stdout: 'ignore',
    stderr: 'pipe',
    env: {
      NODE_OPTIONS: '--max-old-space-size=2048',
    },
  },
})
