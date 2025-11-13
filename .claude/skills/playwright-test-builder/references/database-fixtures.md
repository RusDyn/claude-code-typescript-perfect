# Database Setup and Fixtures

Guide to managing test databases and fixtures in Playwright.

## Database Setup

### PostgreSQL Example

```typescript
// db/setup.ts
import { Pool } from "pg";

export class TestDatabase {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: process.env.TEST_DB_HOST || "localhost",
      database: process.env.TEST_DB_NAME || "test_db",
      user: process.env.TEST_DB_USER || "test",
      password: process.env.TEST_DB_PASSWORD || "test",
    });
  }

  async seed() {
    await this.pool.query(`
      INSERT INTO users (email, name, role)
      VALUES 
        ('test@example.com', 'Test User', 'user'),
        ('admin@example.com', 'Admin', 'admin')
    `);
  }

  async cleanup() {
    await this.pool.query("TRUNCATE users, products, orders CASCADE");
  }

  async close() {
    await this.pool.end();
  }
}
```

### Use in Tests

```typescript
import { test } from "@playwright/test";
import { TestDatabase } from "../db/setup";

let db: TestDatabase;

test.beforeAll(async () => {
  db = new TestDatabase();
  await db.seed();
});

test.afterAll(async () => {
  await db.cleanup();
  await db.close();
});
```

## Fixtures

### Test Data Fixtures

```typescript
// fixtures/users.ts
export const testUsers = {
  regular: {
    email: "user@example.com",
    password: "UserPass123!",
    name: "Regular User",
  },
  admin: {
    email: "admin@example.com",
    password: "AdminPass123!",
    name: "Admin User",
    role: "admin",
  },
};
```

### Custom Fixtures

```typescript
// fixtures/database.ts
import { test as base } from "@playwright/test";

export const test = base.extend({
  testUser: async ({}, use) => {
    // Setup: Create user
    const user = await createTestUser();

    await use(user);

    // Teardown: Delete user
    await deleteTestUser(user.id);
  },
});
```

This ensures proper test isolation and cleanup.
