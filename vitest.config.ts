import { resolve } from 'node:path'

import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./test/setup.ts'],
    include: ['**/*.{test,spec}.{js,ts,tsx}'],
    exclude: [
      'node_modules',
      'dist',
      '.next',
      'e2e',
      'test/e2e/**', // Exclude e2e tests from vitest (they use Playwright)
      'playwright-report',
      'test-results',
      'coverage',
      'supabase/migrations/**',
    ],
    // Maximize parallel execution for speed
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false,
        isolate: true, // Enable isolation for reliable tests
        useAtomics: true,
        minThreads: 1,
        maxThreads: 4, // Increase for better performance
      },
    },
    // Proper isolation for reliable DOM tests
    isolate: true, // Enable isolation for reliable tests
    sequence: {
      concurrent: false, // Run tests sequentially to prevent DOM conflicts
      shuffle: false, // Run in predictable order
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov', 'text-summary'],
      include: [
        'app/**/*.{ts,tsx}',
        'lib/**/*.{ts,tsx}',
        'components/**/*.{ts,tsx}',
      ],
      exclude: [
        'node_modules/**',
        'dist/**',
        '.next/**',
        'e2e/**',
        'test/**',
        'coverage/**',
        '**/*.d.ts',
        '**/*.config.{js,ts}',
        '**/types/**',
        'middleware.ts',
        'instrumentation*.ts',
        'sentry*.ts',
        'next-env.d.ts',
        'global.d.ts',
        'mdx-components.tsx',
        // Next.js framework files (integration tested)
        'app/**/page.tsx',
        'app/**/layout.tsx',
        'app/**/not-found.tsx',
        'app/**/error.tsx',
        'app/**/global-error.tsx',
        'app/**/loading.tsx',
        // External libraries and dependencies
        'supabase/**',
        '**/migrations/**',
        '**/docs/**',
        '**/*.stories.{js,ts,tsx}',
        '**/*.test.{js,ts,tsx}',
        '**/*.spec.{js,ts,tsx}',
        // shadcn/ui components (externally maintained)
        'components/ui/**',
        // Third-party wrapper utilities
        'lib/database/client-browser.ts', // Supabase wrapper
        'lib/database/client-factory.ts', // Supabase wrapper
        'lib/database/storage.ts', // Supabase storage wrapper
        // External service integrations
        'lib/integrations/zoho-crm.ts', // External API wrapper
        // AI service wrappers
        'lib/ai/pdf-parser-utils.ts', // External PDF library wrapper
        // Email service wrappers
        'lib/email/sendgrid.ts', // SendGrid wrapper
        // File upload service wrappers
        'lib/storage/supabase-storage.ts', // Supabase storage wrapper
        // Authentication service wrappers
        'lib/auth/client-auth-utils.ts', // Supabase auth wrapper
        'lib/auth/client-session.ts', // Supabase session wrapper
      ],
      // Strict coverage thresholds for 100% coverage goal
      thresholds: {
        global: {
          branches: 100,
          functions: 100,
          lines: 100,
          statements: 100,
        },
        // Allow lower thresholds for specific patterns
        'lib/ai/**': {
          branches: 95,
          functions: 95,
          lines: 95,
          statements: 95,
        },
        'lib/integrations/**': {
          branches: 90,
          functions: 90,
          lines: 90,
          statements: 90,
        },
      },
      reportsDirectory: './coverage',
      // Include uncovered files in coverage report
      all: true,
    },
    // Reasonable timeouts for CI
    testTimeout: 10000, // Max 10 seconds per individual test
    hookTimeout: 5000, // Max 5 seconds for setup/teardown hooks
    // Global timeout for entire test suite (60 seconds)
    globalSetup: [],
    // Fast reporter for parallel execution
    reporters: ['default'], // Simplified reporter for speed
    outputFile: {
      html: './test-results/index.html',
    },
    // Silent console logs during tests unless debugging
    silent: false,
    // Only show stderr for failed tests
    onConsoleLog(log, type) {
      // Suppress console.warn and other non-error logs for cleaner output
      return !(
        type === 'stderr' &&
        !log.includes('Error:') &&
        !log.includes('Failed')
      )
    },
    // Fail fast for CI environments
    bail: process.env['CI'] ? 1 : 0,
    // Parallel file processing
    fileParallelism: true,
    // Optimize for speed over comprehensive reporting
    passWithNoTests: true,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './'),
      '@/lib': resolve(__dirname, './lib'),
      '@/components': resolve(__dirname, './components'),
      '@/app': resolve(__dirname, './app'),
      '@/types': resolve(__dirname, './types'),
      '@/utils': resolve(__dirname, './utils'),
    },
  },
  // Optimize for faster test runs
  esbuild: {
    target: 'node18',
  },
})
