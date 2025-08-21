import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import unicorn from 'eslint-plugin-unicorn';
import sonarjs from 'eslint-plugin-sonarjs';
import security from 'eslint-plugin-security';

export default [
  // Base configuration with ignores
  {
    ignores: [
      'node_modules/',
      '.next/',
      'out/',
      'dist/',
      'coverage/',
      'generated/',
      'next-env.d.ts',
      'src/components/ui/',
    ],
  },
  
  // JavaScript files configuration
  {
    files: ['**/*.{js,mjs,cjs}'],
    ...js.configs.recommended,
    plugins: {
      unicorn,
      sonarjs,
      security,
    },
    rules: {
      // Basic rules for JS files
      'unicorn/no-null': 'off',
      'unicorn/prefer-module': 'off',
      'sonarjs/no-duplicate-string': 'off',
      'security/detect-object-injection': 'warn',
    },
  },
  
  // TypeScript files configuration
  ...tseslint.config(
    {
      files: ['**/*.{ts,tsx}'],
      extends: [
        ...tseslint.configs.strict,
        ...tseslint.configs.stylistic,
      ],
      languageOptions: {
        parser: tseslint.parser,
        parserOptions: {
          project: './tsconfig.json',
          ecmaVersion: 'latest',
          sourceType: 'module',
        },
      },
      plugins: {
        '@typescript-eslint': tseslint.plugin,
        unicorn,
        sonarjs,
        security,
      },
      rules: {
        // TypeScript strict rules
        '@typescript-eslint/explicit-function-return-type': 'error',
        '@typescript-eslint/no-explicit-any': 'error',
        '@typescript-eslint/no-unsafe-assignment': 'error',
        '@typescript-eslint/no-unsafe-member-access': 'error',
        '@typescript-eslint/no-unsafe-call': 'error',
        '@typescript-eslint/no-unsafe-return': 'error',
        '@typescript-eslint/strict-boolean-expressions': 'off',
        '@typescript-eslint/no-floating-promises': 'error',
        '@typescript-eslint/no-misused-promises': 'error',
        '@typescript-eslint/await-thenable': 'error',
        '@typescript-eslint/no-unnecessary-condition': 'error',
        '@typescript-eslint/prefer-readonly': 'error',
        '@typescript-eslint/switch-exhaustiveness-check': 'error',
        '@typescript-eslint/prefer-nullish-coalescing': 'error',
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
        
        // Unicorn strict rules
        'unicorn/no-null': 'error',
        'unicorn/prefer-top-level-await': 'error',
        'unicorn/explicit-length-check': 'error',
        'unicorn/prefer-node-protocol': 'error',
        'unicorn/prefer-module': 'error',
        'unicorn/no-array-push-push': 'error',
        'unicorn/no-lonely-if': 'error',
        'unicorn/no-useless-spread': 'error',
        'unicorn/prefer-ternary': 'error',
        'unicorn/prefer-logical-operator-over-ternary': 'error',
        'unicorn/prefer-math-trunc': 'error',
        'unicorn/prefer-number-properties': 'error',
        'unicorn/prefer-string-starts-ends-with': 'error',
        'unicorn/prefer-string-slice': 'error',
        'unicorn/prefer-regexp-test': 'error',
        'unicorn/throw-new-error': 'error',
        'unicorn/no-console-spaces': 'error',
        'unicorn/escape-case': 'error',
        'unicorn/number-literal-case': 'error',
        
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
        'security/detect-object-injection': 'warn',
        'security/detect-non-literal-regexp': 'warn',
        'security/detect-possible-timing-attacks': 'warn',
        'security/detect-eval-with-expression': 'error',
        'security/detect-no-csrf-before-method-override': 'error',
        'security/detect-buffer-noassert': 'error',
        'security/detect-child-process': 'warn',
        'security/detect-disable-mustache-escape': 'error',
        'security/detect-new-buffer': 'error',
        'security/detect-unsafe-regex': 'error',
      },
    }
  ),
  
  // TypeScript config files override
  {
    files: ['*.config.ts'],
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      'unicorn/no-null': 'off',
      'unicorn/prefer-module': 'off',
      'sonarjs/no-duplicate-string': 'off',
    },
  },
  
  // Test files override
  {
    files: [
      '**/*.test.ts',
      '**/*.spec.ts',
      '**/*.test.tsx',
      '**/*.spec.tsx',
      '**/test-setup.ts',
    ],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
      '@typescript-eslint/no-unsafe-call': 'off',
      '@typescript-eslint/no-unsafe-return': 'off',
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/strict-boolean-expressions': 'off',
      '@typescript-eslint/no-floating-promises': 'off',
      '@typescript-eslint/no-misused-promises': 'off',
      '@typescript-eslint/await-thenable': 'off',
      '@typescript-eslint/no-unnecessary-condition': 'off',
      '@typescript-eslint/prefer-nullish-coalescing': 'off',
      '@typescript-eslint/no-non-null-assertion': 'off',
      '@typescript-eslint/restrict-template-expressions': 'off',
      'sonarjs/no-duplicate-string': 'off',
      'sonarjs/cognitive-complexity': ['error', 25],
      'unicorn/no-null': 'off',
      'security/detect-object-injection': 'off',
    },
  },
  
  // Type definition files override
  {
    files: ['next-env.d.ts', '*.d.ts'],
    rules: {
      'unicorn/prevent-abbreviations': 'off',
    },
  },
  
  // Specific API/lib directories with warning-level rules
  {
    files: [
      'src/app/api/**/*.ts',
      'src/contexts/**/*.tsx',
      'src/hooks/**/*.ts',
      'src/lib/**/*.ts',
    ],
    ignores: [
      '**/*.test.ts',
      '**/*.spec.ts',
      '**/*.test.tsx',
      '**/*.spec.tsx',
    ],
    rules: {
      '@typescript-eslint/explicit-function-return-type': 'warn',
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unsafe-assignment': 'warn',
      '@typescript-eslint/no-unsafe-member-access': 'warn',
      '@typescript-eslint/no-unsafe-call': 'warn',
      '@typescript-eslint/no-unsafe-return': 'warn',
      '@typescript-eslint/strict-boolean-expressions': 'warn',
      '@typescript-eslint/no-floating-promises': 'warn',
      '@typescript-eslint/await-thenable': 'warn',
      '@typescript-eslint/no-unnecessary-condition': 'warn',
      '@typescript-eslint/prefer-readonly': 'warn',
      '@typescript-eslint/prefer-nullish-coalescing': 'warn',
      'unicorn/no-null': 'warn',
      'sonarjs/no-duplicate-string': 'warn',
      'security/detect-unsafe-regex': 'warn',
    },
  },
];