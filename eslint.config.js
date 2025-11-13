import path from 'node:path'
import { fileURLToPath } from 'node:url'

import { FlatCompat } from '@eslint/eslintrc'
import js from '@eslint/js'
import typescript from '@typescript-eslint/eslint-plugin'
import typescriptParser from '@typescript-eslint/parser'
import eslintComments from 'eslint-plugin-eslint-comments'
import functional from 'eslint-plugin-functional'
import importPlugin from 'eslint-plugin-import'
import security from 'eslint-plugin-security'
import simpleImportSort from 'eslint-plugin-simple-import-sort'
import sonarjs from 'eslint-plugin-sonarjs'
import eslintPluginUnicorn from 'eslint-plugin-unicorn'
import globals from 'globals'

import localPlugin from './eslint-plugin/index.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
})

const eslintConfig = [
  // Base configuration
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parser: typescriptParser,
      parserOptions: {
        project: './tsconfig.json',
        ecmaFeatures: {
          jsx: true,
        },
      },
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2022,
        React: 'readonly',
        JSX: 'readonly',
      },
    },
  },

  // Extend base configs using compat
  ...compat.extends('prettier', 'eslint:recommended'),

  // Main rules configuration
  {
    plugins: {
      '@typescript-eslint': typescript,
      unicorn: eslintPluginUnicorn,
      sonarjs: sonarjs,
      security: security,
      functional,
      'eslint-comments': eslintComments,
      'simple-import-sort': simpleImportSort,
      import: importPlugin,
      local: localPlugin,
    },
    rules: {
      // Handle unused variables - allow underscore prefix for intentionally unused
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          caughtErrorsIgnorePattern: '^_',
        },
      ],

      // TypeScript strict rules
      '@typescript-eslint/explicit-function-return-type': 'error',
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',
      '@typescript-eslint/strict-boolean-expressions': 'off',
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/await-thenable': 'error',
      '@typescript-eslint/no-unnecessary-condition': 'error',
      '@typescript-eslint/prefer-readonly': 'error',
      '@typescript-eslint/switch-exhaustiveness-check': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/no-non-null-assertion': 'error',
      '@typescript-eslint/restrict-template-expressions': 'error',

      // Naming conventions
      '@typescript-eslint/naming-convention': [
        'error',
        {
          selector: 'interface',
          format: ['PascalCase'],
          custom: { regex: '^I[A-Z]', match: false },
        },
        {
          selector: 'typeParameter',
          format: ['PascalCase'],
        },
        {
          selector: 'enum',
          format: ['PascalCase'],
        },
      ],

      // Unicorn rules - modern best practices
      'unicorn/no-null': 'off',
      'unicorn/better-regex': 'warn',
      'unicorn/catch-error-name': 'error',
      'unicorn/consistent-function-scoping': 'error',
      'unicorn/explicit-length-check': 'error',
      'unicorn/filename-case': ['error', { case: 'kebabCase' }],
      'unicorn/new-for-builtins': 'error',
      'unicorn/no-array-for-each': 'off',
      'unicorn/no-array-push-push': 'error',
      'unicorn/no-console-spaces': 'error',
      'unicorn/no-for-loop': 'error',
      'unicorn/no-lonely-if': 'error',
      'unicorn/no-useless-spread': 'error',
      'unicorn/prefer-array-find': 'error',
      'unicorn/prefer-array-flat': 'error',
      'unicorn/prefer-array-flat-map': 'error',
      'unicorn/prefer-includes': 'error',
      'unicorn/prefer-logical-operator-over-ternary': 'error',
      'unicorn/prefer-math-trunc': 'error',
      'unicorn/prefer-module': 'off',
      'unicorn/prefer-node-protocol': 'error',
      'unicorn/prefer-number-properties': 'error',
      'unicorn/prefer-optional-catch-binding': 'error',
      'unicorn/prefer-regexp-test': 'error',
      'unicorn/prefer-set-has': 'error',
      'unicorn/prefer-string-slice': 'error',
      'unicorn/prefer-string-starts-ends-with': 'error',
      'unicorn/prefer-ternary': 'warn',
      'unicorn/prefer-top-level-await': 'warn',
      'unicorn/throw-new-error': 'error',

      // SonarJS code quality rules
      'sonarjs/cognitive-complexity': ['error', 15],
      'sonarjs/no-duplicate-string': ['error', { threshold: 6 }],
      'sonarjs/no-identical-functions': 'error',
      'sonarjs/no-collapsible-if': 'error',
      'sonarjs/no-duplicated-branches': 'error',
      'sonarjs/no-redundant-boolean': 'error',
      'sonarjs/no-redundant-jump': 'error',
      'sonarjs/no-same-line-conditional': 'error',
      'sonarjs/no-small-switch': 'error',
      'sonarjs/no-useless-catch': 'error',
      'sonarjs/prefer-immediate-return': 'error',
      'sonarjs/prefer-object-literal': 'error',
      'sonarjs/prefer-single-boolean-return': 'error',
      'sonarjs/prefer-while': 'error',

      // Security rules
      'security/detect-object-injection': 'off',
      'security/detect-non-literal-regexp': 'warn',
      'security/detect-possible-timing-attacks': 'warn',
      'security/detect-eval-with-expression': 'error',
      'security/detect-no-csrf-before-method-override': 'error',
      'security/detect-buffer-noassert': 'error',
      'security/detect-child-process': 'warn',
      'security/detect-disable-mustache-escape': 'error',
      'security/detect-new-buffer': 'error',
      'security/detect-unsafe-regex': 'error',

      // File length limit (default)
      'max-lines': ['error', 300],

      'functional/immutable-data': 'off',
      'functional/prefer-immutable-types': 'off',
      'functional/no-let': 'warn',
      'functional/no-this-expressions': 'warn',
      'functional/no-return-void': 'off',
      'functional/no-classes': 'error',

      // слишком строгие — выключаем
      'functional/no-loop-statements': 'error',
      'functional/no-conditional-statements': 'off',
      'functional/no-throw-statements': 'off',
      'functional/no-expression-statements': 'off',
      'functional/no-try-statements': 'off',

      // ESLint Comments - prevent disabling rules
      'eslint-comments/disable-enable-pair': 'error',
      'eslint-comments/no-duplicate-disable': 'error',
      'eslint-comments/no-unlimited-disable': 'error',
      'eslint-comments/no-unused-disable': 'error',
      'eslint-comments/no-unused-enable': 'error',
      'eslint-comments/no-use': 'error',
      'simple-import-sort/imports': 'warn',
      'simple-import-sort/exports': 'warn',
      '@typescript-eslint/consistent-type-imports': [
        'warn',
        { prefer: 'type-imports', fixStyle: 'inline-type-imports' },
      ],

      // Prevent re-exports
      'no-restricted-syntax': [
        'error',
        {
          selector: 'ExportAllDeclaration',
          message: 'Do not use export * from ... re-exports',
        },
        {
          selector: 'ExportNamedDeclaration[source]',
          message:
            'Do not use re-exports (export { x } from ...). Import and export explicitly.',
        },
      ],
      'local/no-transitive-reexports': 'error',
      'local/no-trivial-wrappers': 'error',

      // Prevent deep relative imports
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: [
                '../../*',
                '../../../*',
                '../../../../*',
                '../../../../../*',
              ],
              message:
                'Deep relative imports are not allowed. Use absolute imports with @ alias instead.',
            },
          ],
        },
      ],
    },
  },

  // Config files overrides
  {
    files: [
      '*.js',
      '*.config.js',
      '*.config.mjs',
      '*.config.cjs',
      'commitlint.config.js',
    ],
    languageOptions: {
      parser: undefined, // Use default parser for JS files
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        project: null, // Disable TypeScript project for JS files
      },
    },
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
      '@typescript-eslint/no-unsafe-call': 'off',
      '@typescript-eslint/no-unsafe-return': 'off',
      '@typescript-eslint/no-floating-promises': 'off',
      '@typescript-eslint/await-thenable': 'off',
      '@typescript-eslint/no-unnecessary-condition': 'off',
      '@typescript-eslint/prefer-readonly': 'off',
      '@typescript-eslint/switch-exhaustiveness-check': 'off',
      '@typescript-eslint/prefer-optional-chain': 'off',
      '@typescript-eslint/no-non-null-assertion': 'off',
      '@typescript-eslint/restrict-template-expressions': 'off',
      '@typescript-eslint/naming-convention': 'off',
      '@typescript-eslint/consistent-type-imports': 'off',
      'unicorn/prefer-module': 'off',
      'unicorn/filename-case': 'off',
      'sonarjs/no-duplicate-string': 'off',
      'max-lines': 'off',
    },
  },

  // TypeScript config files
  {
    files: ['*.config.ts', 'vitest*.config.ts'],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        project: './tsconfig.json',
      },
    },
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      'unicorn/prefer-module': 'off',
      'unicorn/filename-case': 'off',
      'sonarjs/no-duplicate-string': 'off',
      'max-lines': 'off',
    },
  },

  // Pages and React components - disable explicit return types
  {
    files: ['app/**/page.tsx', 'app/**/layout.tsx', 'components/**/*.tsx'],
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'off',
    },
  },

  // Components - 400 line limit
  {
    files: ['components/**/*.ts', 'components/**/*.tsx'],
    rules: {
      'max-lines': ['error', 400],
    },
  },

  // App route files - 250 line limit (default, but explicit for clarity)
  {
    files: ['app/**/*.ts', 'app/**/*.tsx'],
    rules: {
      'max-lines': ['error', 250],
    },
  },

  // App page and layout files - 300 line limit
  {
    files: ['app/**/page.tsx', 'app/**/layout.tsx'],
    rules: {
      'max-lines': ['error', 300],
    },
  },

  // UI Components - relaxed rules
  {
    files: ['components/ui/**/*'],
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'off',
      'sonarjs/cognitive-complexity': ['error', 25],
      'sonarjs/no-duplicate-string': ['warn', { threshold: 10 }],
    },
  },

  // API and library files - warnings instead of errors
  {
    files: ['app/api/**/*.ts', 'hooks/**/*.ts', 'lib/**/*.ts'],
    ignores: ['**/*.test.ts', '**/*.spec.ts', '**/*.test.tsx', '**/*.spec.tsx'],
    rules: {},
  },
  // Test files configuration
  {
    files: [
      'test/**/*.ts',
      'test/**/*.tsx',
      '**/*.test.ts',
      '**/*.test.tsx',
      '**/*.spec.ts',
      '**/*.spec.tsx',
      'e2e/**/*.ts',
      'test/e2e/**/*.ts',
      'playwright.config.ts',
    ],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        project: './tsconfig.json',
        ecmaFeatures: {
          jsx: false,
        },
      },
      globals: {
        ...globals.node,
        describe: 'readonly',
        it: 'readonly',
        test: 'readonly',
        expect: 'readonly',
        beforeAll: 'readonly',
        afterAll: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        vi: 'readonly',
        vitest: 'readonly',
        jest: 'readonly',
      },
    },
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
      '@typescript-eslint/no-unsafe-call': 'off',
      '@typescript-eslint/no-unsafe-return': 'off',
      '@typescript-eslint/no-floating-promises': 'off',
      '@typescript-eslint/await-thenable': 'off',
      '@typescript-eslint/no-unnecessary-condition': 'off',
      '@typescript-eslint/prefer-readonly': 'off',
      '@typescript-eslint/switch-exhaustiveness-check': 'off',
      '@typescript-eslint/prefer-optional-chain': 'off',
      '@typescript-eslint/no-non-null-assertion': 'off',
      '@typescript-eslint/restrict-template-expressions': 'off',
      '@typescript-eslint/naming-convention': 'off',
      'unicorn/prefer-module': 'off',
      'unicorn/filename-case': 'off',
      'sonarjs/no-duplicate-string': 'off',
      'sonarjs/cognitive-complexity': 'off',
      'max-lines': 'off',
      'functional/no-loop-statements': 'off',
      'functional/no-let': 'off',
    },
  },

  // Global ignores
  {
    ignores: [
      'node_modules/',
      'supabase/types.ts',
      '.next/',
      'out/',
      'dist/',
      'coverage/**/*',
      'generated/**/*',
      'next-env.d.ts',
      'components/ui/',
      'lint-staged.config.cjs',
      'next.config.ts',
      'postcss.config.cjs',
      'tailwind.config.cjs',
      'scripts/*.js',
      'public/**/*.js',
      'types/branded.ts',
      'test-results/',
      'playwright-report/',
      'integration-test-results/',
      '**/*.tsbuildinfo',
      '**/.playwright-artifacts*/**',
      'vitest.precommit.config.ts',
      'vitest.phase4.config.ts',
      'eslint-plugin/',
      'commitlint.config.js',
      '.claude/skills/',
    ],
  },
]

export default eslintConfig
