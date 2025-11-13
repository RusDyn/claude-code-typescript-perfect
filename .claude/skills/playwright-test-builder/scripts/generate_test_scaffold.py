#!/usr/bin/env python3
"""
Playwright Test Scaffolding Generator

Generates test files, page objects, and fixtures following best practices.
"""

import sys
import json
import os
from pathlib import Path

def generate_test_file(config):
    """Generate a Playwright test file"""
    
    test_name = config.get('test_name', 'example')
    page_object = config.get('page_object')
    use_fixtures = config.get('use_fixtures', True)
    test_type = config.get('test_type', 'e2e')  # e2e, api, component
    
    # Base imports
    imports = ["import { test, expect } from '@playwright/test';"]
    
    if page_object:
        imports.append(f"import {{ {page_object} }} from '../pages/{page_object}';")
    
    if use_fixtures:
        imports.append("import { testData } from '../fixtures/testData';")
    
    # Test describe block
    test_content = f"""{''.join(imp + '\\n' for imp in imports)}

test.describe('{test_name}', () => {{
  test.beforeEach(async ({{ page }}) => {{
    // Setup: Navigate to page or set initial state
    await page.goto('/');
  }});

  test('should pass example test', async ({{ page }}) => {{
    // Arrange
    const expectedTitle = 'My App';
    
    // Act
    const title = await page.title();
    
    // Assert
    expect(title).toBe(expectedTitle);
  }});

  test('should interact with elements', async ({{ page }}) => {{
    // Example interaction
    await page.click('button[data-testid="submit"]');
    await expect(page.locator('.success-message')).toBeVisible();
  }});

  test.describe('authenticated user', () => {{
    test.use({{ storageState: 'auth.json' }});
    
    test('should access protected resource', async ({{ page }}) => {{
      await page.goto('/dashboard');
      await expect(page.locator('h1')).toContainText('Dashboard');
    }});
  }});
}});
"""
    
    return test_content

def generate_page_object(config):
    """Generate a Page Object Model class"""
    
    page_name = config.get('page_name', 'Example')
    elements = config.get('elements', [])
    
    # Generate selectors
    selector_definitions = []
    for element in elements:
        selector_definitions.append(
            f"  readonly {element['name']} = this.page.locator('{element['selector']}');"
        )
    
    # Generate methods
    method_definitions = []
    for element in elements:
        if element.get('type') == 'button':
            method_definitions.append(f"""
  async click{element['name'].title()}() {{
    await this.{element['name']}.click();
  }}""")
        elif element.get('type') == 'input':
            method_definitions.append(f"""
  async fill{element['name'].title()}(text: string) {{
    await this.{element['name']}.fill(text);
  }}""")
    
    page_object = f"""import {{ Page, Locator }} from '@playwright/test';

export class {page_name}Page {{
  readonly page: Page;
  
  // Selectors
{chr(10).join(selector_definitions)}

  constructor(page: Page) {{
    this.page = page;
  }}

  async goto() {{
    await this.page.goto('/{page_name.lower()}');
  }}

  async waitForLoad() {{
    await this.page.waitForLoadState('networkidle');
  }}
{''.join(method_definitions)}

  async getTitle(): Promise<string> {{
    return await this.page.title();
  }}
}}
"""
    
    return page_object

def generate_fixture(config):
    """Generate test fixture/data"""
    
    fixture_name = config.get('fixture_name', 'testData')
    data_type = config.get('data_type', 'user')
    
    fixtures = {
        'user': """export const testData = {
  validUser: {
    email: 'test@example.com',
    password: 'SecurePass123!',
    name: 'Test User'
  },
  
  invalidUser: {
    email: 'invalid@example.com',
    password: 'wrong',
    name: ''
  },
  
  adminUser: {
    email: 'admin@example.com',
    password: 'AdminPass123!',
    name: 'Admin User',
    role: 'admin'
  }
};
""",
        'product': """export const testData = {
  validProduct: {
    name: 'Test Product',
    price: 29.99,
    description: 'A test product',
    category: 'Electronics',
    stock: 100
  },
  
  outOfStockProduct: {
    name: 'Out of Stock Item',
    price: 49.99,
    description: 'This item is out of stock',
    category: 'Electronics',
    stock: 0
  }
};
""",
        'api': """export const testData = {
  endpoints: {
    users: '/api/users',
    products: '/api/products',
    auth: '/api/auth/login'
  },
  
  headers: {
    json: {
      'Content-Type': 'application/json'
    },
    auth: (token: string) => ({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    })
  }
};
"""
    }
    
    return fixtures.get(data_type, fixtures['user'])

def generate_playwright_config(config):
    """Generate playwright.config.ts"""
    
    base_url = config.get('base_url', 'http://localhost:3000')
    workers = config.get('workers', 4)
    retries = config.get('retries', 2)
    timeout = config.get('timeout', 30000)
    
    playwright_config = f"""import {{ defineConfig, devices }} from '@playwright/test';

export default defineConfig({{
  testDir: './tests',
  
  // Maximum time one test can run
  timeout: {timeout},
  
  // Test execution settings
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? {retries} : 0,
  workers: process.env.CI ? 1 : {workers},
  
  // Reporter
  reporter: [
    ['html', {{ outputFolder: 'playwright-report' }}],
    ['json', {{ outputFile: 'test-results.json' }}],
    ['junit', {{ outputFile: 'junit-results.xml' }}],
    ['list']
  ],
  
  // Shared settings for all tests
  use: {{
    baseURL: '{base_url}',
    
    // Collect trace on failure
    trace: 'on-first-retry',
    
    // Screenshot on failure
    screenshot: 'only-on-failure',
    
    // Video on failure
    video: 'retain-on-failure',
    
    // Action timeout
    actionTimeout: 10000,
    
    // Navigation timeout
    navigationTimeout: 30000,
  }},

  // Configure projects for major browsers
  projects: [
    {{
      name: 'chromium',
      use: {{ ...devices['Desktop Chrome'] }},
    }},

    {{
      name: 'firefox',
      use: {{ ...devices['Desktop Firefox'] }},
    }},

    {{
      name: 'webkit',
      use: {{ ...devices['Desktop Safari'] }},
    }},

    // Mobile browsers
    {{
      name: 'Mobile Chrome',
      use: {{ ...devices['Pixel 5'] }},
    }},
    
    {{
      name: 'Mobile Safari',
      use: {{ ...devices['iPhone 12'] }},
    }},

    // Authenticated tests
    {{
      name: 'authenticated',
      use: {{
        ...devices['Desktop Chrome'],
        storageState: 'auth.json',
      }},
    }},
  ],

  // Run local dev server before tests
  webServer: {{
    command: 'npm run dev',
    url: '{base_url}',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  }},
}});
"""
    
    return playwright_config

def generate_database_setup(config):
    """Generate database setup script"""
    
    db_type = config.get('db_type', 'postgres')
    
    if db_type == 'postgres':
        return """import { Pool } from 'pg';

export class DatabaseHelper {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      database: process.env.DB_NAME || 'test_db',
      user: process.env.DB_USER || 'test_user',
      password: process.env.DB_PASSWORD || 'test_pass',
    });
  }

  async query(text: string, params?: any[]) {
    return await this.pool.query(text, params);
  }

  async seedTestData() {
    await this.query(`
      INSERT INTO users (email, name, password_hash)
      VALUES 
        ('test@example.com', 'Test User', '$2b$10$...'),
        ('admin@example.com', 'Admin User', '$2b$10$...')
      ON CONFLICT (email) DO NOTHING
    `);
  }

  async cleanupTestData() {
    await this.query('DELETE FROM users WHERE email LIKE \'test%\'');
  }

  async close() {
    await this.pool.end();
  }
}
"""
    
    elif db_type == 'mongodb':
        return """import { MongoClient, Db } from 'mongodb';

export class DatabaseHelper {
  private client: MongoClient;
  private db: Db;

  constructor() {
    const uri = process.env.MONGO_URI || 'mongodb://localhost:27017/test_db';
    this.client = new MongoClient(uri);
  }

  async connect() {
    await this.client.connect();
    this.db = this.client.db();
  }

  async seedTestData() {
    await this.db.collection('users').insertMany([
      { email: 'test@example.com', name: 'Test User' },
      { email: 'admin@example.com', name: 'Admin User', role: 'admin' }
    ]);
  }

  async cleanupTestData() {
    await this.db.collection('users').deleteMany({ 
      email: { $regex: /^test/ } 
    });
  }

  async close() {
    await this.client.close();
  }
}
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_test_scaffold.py '<config_json>'", file=sys.stderr)
        print("\nConfig options:", file=sys.stderr)
        print("  type: 'test' | 'page' | 'fixture' | 'config' | 'database'", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        
        example_test = {
            'type': 'test',
            'test_name': 'Login Flow',
            'page_object': 'LoginPage',
            'use_fixtures': True
        }
        print("\nGenerate test:", file=sys.stderr)
        print(json.dumps(example_test, indent=2), file=sys.stderr)
        
        example_page = {
            'type': 'page',
            'page_name': 'Login',
            'elements': [
                {'name': 'emailInput', 'selector': 'input[name="email"]', 'type': 'input'},
                {'name': 'passwordInput', 'selector': 'input[name="password"]', 'type': 'input'},
                {'name': 'submitButton', 'selector': 'button[type="submit"]', 'type': 'button'}
            ]
        }
        print("\nGenerate page object:", file=sys.stderr)
        print(json.dumps(example_page, indent=2), file=sys.stderr)
        
        sys.exit(1)
    
    config = json.loads(sys.argv[1])
    output_type = config.get('type')
    
    if output_type == 'test':
        output = generate_test_file(config)
    elif output_type == 'page':
        output = generate_page_object(config)
    elif output_type == 'fixture':
        output = generate_fixture(config)
    elif output_type == 'config':
        output = generate_playwright_config(config)
    elif output_type == 'database':
        output = generate_database_setup(config)
    else:
        print(json.dumps({'error': f'Unknown type: {output_type}'}))
        sys.exit(1)
    
    print(output)

if __name__ == '__main__':
    main()
