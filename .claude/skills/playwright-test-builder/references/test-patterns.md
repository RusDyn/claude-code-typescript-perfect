# Playwright Test Patterns and Best Practices

Comprehensive guide to writing maintainable, reliable Playwright tests.

## Core Testing Principles

### 1. Arrange-Act-Assert Pattern

Structure every test clearly:

```typescript
test("should login successfully", async ({ page }) => {
  // Arrange - Setup
  const email = "test@example.com";
  const password = "SecurePass123!";
  await page.goto("/login");

  // Act - Perform action
  await page.fill('[name="email"]', email);
  await page.fill('[name="password"]', password);
  await page.click('button[type="submit"]');

  // Assert - Verify result
  await expect(page).toHaveURL("/dashboard");
  await expect(page.locator("h1")).toContainText("Welcome");
});
```

### 2. Test Independence

Each test should run independently:

```typescript
// ✅ Good - Independent test
test("should add item to cart", async ({ page }) => {
  await page.goto("/products");
  await page.click('[data-product-id="1"] button');
  await expect(page.locator(".cart-count")).toHaveText("1");
});

// ❌ Bad - Depends on previous test
test("should checkout cart", async ({ page }) => {
  // Assumes cart already has items from previous test
  await page.goto("/checkout");
});
```

### 3. Descriptive Test Names

Use clear, behavior-driven names:

```typescript
// ✅ Good
test('should show error message when email is invalid', async ({ page }) => {

// ✅ Good
test('should complete checkout with valid credit card', async ({ page }) => {

// ❌ Bad
test('test1', async ({ page }) => {

// ❌ Bad
test('works', async ({ page }) => {
```

## Selector Strategies

### Prefer Stable Selectors

Priority order:

1. `data-testid` attributes
2. ARIA roles and labels
3. User-visible text
4. CSS selectors (last resort)

```typescript
// 1. Best - data-testid
await page.click('[data-testid="submit-button"]');

// 2. Good - ARIA role
await page.click('role=button[name="Submit"]');

// 3. Good - User-visible text
await page.click("text=Submit");

// 4. Acceptable - Semantic CSS
await page.click('button[type="submit"]');

// 5. Avoid - Fragile selectors
await page.click(".btn.btn-primary.submit-btn"); // May break with styling changes
```

### Use Locators Properly

```typescript
// Chain locators for specificity
const form = page.locator('form[data-testid="login-form"]');
await form.locator('input[name="email"]').fill("test@example.com");
await form.locator('button[type="submit"]').click();

// Use getByRole for accessibility
await page.getByRole("button", { name: "Submit" }).click();
await page.getByRole("textbox", { name: "Email" }).fill("test@example.com");

// Use getByLabel for form inputs
await page.getByLabel("Email address").fill("test@example.com");
await page.getByLabel("Password").fill("password123");
```

## Wait Strategies

### Auto-Waiting

Playwright auto-waits for elements to be actionable:

```typescript
// Playwright automatically waits for:
// - Element to be visible
// - Element to be stable
// - Element to receive events
// - Element to be enabled
await page.click("button"); // Waits automatically
```

### Explicit Waits

When you need specific conditions:

```typescript
// Wait for element
await page.waitForSelector('[data-testid="results"]');

// Wait for load state
await page.waitForLoadState("networkidle");

// Wait for response
const responsePromise = page.waitForResponse(
  (resp) => resp.url().includes("/api/users") && resp.status() === 200,
);
await page.click("button");
await responsePromise;

// Wait for function
await page.waitForFunction(() => document.querySelectorAll(".item").length > 5);

// Wait for timeout (avoid - use as last resort)
await page.waitForTimeout(1000); // ❌ Avoid if possible
```

## Assertions

### Use Playwright Assertions

```typescript
// Element visibility
await expect(page.locator(".success")).toBeVisible();
await expect(page.locator(".loading")).toBeHidden();

// Text content
await expect(page.locator("h1")).toHaveText("Welcome");
await expect(page.locator(".error")).toContainText("Invalid");

// Attributes
await expect(page.locator("input")).toHaveAttribute("type", "email");
await expect(page.locator("button")).toBeDisabled();
await expect(page.locator("input")).toBeFocused();

// Count
await expect(page.locator(".item")).toHaveCount(5);

// URL
await expect(page).toHaveURL("/dashboard");
await expect(page).toHaveURL(/\/dashboard/);

// Screenshots
await expect(page).toHaveScreenshot("homepage.png");
```

### Soft Assertions

Continue test even if assertion fails:

```typescript
test("should validate multiple fields", async ({ page }) => {
  await expect.soft(page.locator(".title")).toBeVisible();
  await expect.soft(page.locator(".description")).toBeVisible();
  await expect.soft(page.locator(".price")).toBeVisible();
  // Test continues even if some assertions fail
});
```

## Test Organization

### Group Related Tests

```typescript
test.describe("Login Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
  });

  test.describe("valid credentials", () => {
    test("should login with email", async ({ page }) => {
      // ...
    });

    test("should login with username", async ({ page }) => {
      // ...
    });
  });

  test.describe("invalid credentials", () => {
    test("should show error for wrong password", async ({ page }) => {
      // ...
    });

    test("should show error for non-existent user", async ({ page }) => {
      // ...
    });
  });
});
```

### Use Hooks Effectively

```typescript
test.describe("User Management", () => {
  let userId: string;

  // Runs before all tests in this describe block
  test.beforeAll(async ({ request }) => {
    // Create test user once
    const response = await request.post("/api/users", {
      data: { email: "test@example.com" },
    });
    userId = (await response.json()).id;
  });

  // Runs before each test
  test.beforeEach(async ({ page }) => {
    await page.goto(`/users/${userId}`);
  });

  // Runs after each test
  test.afterEach(async ({ page }) => {
    // Cleanup UI state if needed
  });

  // Runs after all tests
  test.afterAll(async ({ request }) => {
    // Delete test user
    await request.delete(`/api/users/${userId}`);
  });

  test("should display user profile", async ({ page }) => {
    // Test implementation
  });
});
```

## Fixtures and Test Data

### Custom Fixtures

```typescript
// fixtures/auth.ts
import { test as base } from "@playwright/test";

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Setup: Login
    await page.goto("/login");
    await page.fill('[name="email"]', "test@example.com");
    await page.fill('[name="password"]', "password");
    await page.click('button[type="submit"]');
    await page.waitForURL("/dashboard");

    // Use the authenticated page
    await use(page);

    // Teardown: Logout
    await page.click('[data-testid="logout"]');
  },
});

// Usage
test("should access protected resource", async ({ authenticatedPage }) => {
  await authenticatedPage.goto("/admin");
  await expect(authenticatedPage.locator("h1")).toBeVisible();
});
```

### Storage State for Authentication

```typescript
// Setup authentication once
import { test as setup } from "@playwright/test";

setup("authenticate", async ({ page }) => {
  await page.goto("/login");
  await page.fill('[name="email"]', "test@example.com");
  await page.fill('[name="password"]', "password");
  await page.click('button[type="submit"]');

  // Save authentication state
  await page.context().storageState({ path: "auth.json" });
});

// Use in tests
test.use({ storageState: "auth.json" });

test("should access dashboard", async ({ page }) => {
  await page.goto("/dashboard");
  // Already authenticated!
});
```

## API Testing Patterns

### Test API Endpoints

```typescript
test("should create user via API", async ({ request }) => {
  const response = await request.post("/api/users", {
    data: {
      email: "new@example.com",
      name: "New User",
    },
  });

  expect(response.ok()).toBeTruthy();
  expect(response.status()).toBe(201);

  const user = await response.json();
  expect(user).toHaveProperty("id");
  expect(user.email).toBe("new@example.com");
});
```

### Combine UI and API Testing

```typescript
test("should reflect API changes in UI", async ({ page, request }) => {
  // Setup via API
  const response = await request.post("/api/products", {
    data: { name: "New Product", price: 29.99 },
  });
  const product = await response.json();

  // Verify in UI
  await page.goto("/products");
  await expect(page.locator(`[data-product-id="${product.id}"]`)).toBeVisible();
  await expect(
    page.locator(`[data-product-id="${product.id}"] .name`),
  ).toContainText("New Product");
});
```

## Mobile Testing

### Test Responsive Designs

```typescript
test.describe("Mobile View", () => {
  test.use({
    viewport: { width: 375, height: 667 }, // iPhone SE
  });

  test("should show mobile menu", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator(".hamburger-menu")).toBeVisible();
    await expect(page.locator(".desktop-nav")).toBeHidden();
  });
});

// Test specific devices
test.describe("iPad", () => {
  test.use({ ...devices["iPad Pro"] });

  test("should adapt layout for tablet", async ({ page }) => {
    // Test implementation
  });
});
```

### Touch Gestures

```typescript
test("should support swipe gesture", async ({ page }) => {
  await page.goto("/gallery");

  const carousel = page.locator(".carousel");
  await carousel.hover();

  // Swipe left
  await page.mouse.move(300, 300);
  await page.mouse.down();
  await page.mouse.move(100, 300);
  await page.mouse.up();

  await expect(page.locator(".carousel .active")).toHaveAttribute(
    "data-index",
    "2",
  );
});
```

## Performance Testing

### Measure Performance

```typescript
test("should load page quickly", async ({ page }) => {
  const startTime = Date.now();

  await page.goto("/");
  await page.waitForLoadState("networkidle");

  const loadTime = Date.now() - startTime;
  expect(loadTime).toBeLessThan(3000); // 3 seconds
});

// Use Performance API
test("should have good performance metrics", async ({ page }) => {
  await page.goto("/");

  const metrics = await page.evaluate(() => {
    const navigation = performance.getEntriesByType(
      "navigation",
    )[0] as PerformanceNavigationTiming;
    return {
      domContentLoaded:
        navigation.domContentLoadedEventEnd -
        navigation.domContentLoadedEventStart,
      loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
    };
  });

  expect(metrics.domContentLoaded).toBeLessThan(1000);
});
```

## Error Handling

### Test Error States

```typescript
test("should handle network failure", async ({ page, context }) => {
  // Simulate offline
  await context.setOffline(true);

  await page.goto("/products");
  await expect(page.locator(".error-message")).toBeVisible();
  await expect(page.locator(".error-message")).toContainText("Network error");
});

test("should show validation errors", async ({ page }) => {
  await page.goto("/signup");

  // Submit empty form
  await page.click('button[type="submit"]');

  await expect(page.locator('[data-error="email"]')).toBeVisible();
  await expect(page.locator('[data-error="password"]')).toBeVisible();
});
```

## Best Practices Summary

### Do's ✅

- Use data-testid for test-specific selectors
- Write independent, isolated tests
- Use Page Object Model for complex pages
- Test user flows, not implementation details
- Use auto-waiting instead of fixed timeouts
- Group related tests with describe blocks
- Use beforeEach for test setup
- Clean up test data after tests
- Test error cases and edge cases
- Use meaningful test names

### Don'ts ❌

- Don't use unstable selectors (generated classes)
- Don't share state between tests
- Don't test third-party code
- Don't use fixed timeouts (waitForTimeout)
- Don't make tests depend on execution order
- Don't test every possible combination
- Don't skip cleanup
- Don't ignore flaky tests
- Don't test implementation details
- Don't have overly complex tests

## Common Patterns

### Login Helper

```typescript
async function login(page: Page, email: string, password: string) {
  await page.goto("/login");
  await page.fill('[name="email"]', email);
  await page.fill('[name="password"]', password);
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL("/dashboard");
}
```

### Form Filling Helper

```typescript
async function fillForm(page: Page, data: Record<string, string>) {
  for (const [field, value] of Object.entries(data)) {
    await page.fill(`[name="${field}"]`, value);
  }
}
```

### Wait for API Call

```typescript
async function waitForAPICall(page: Page, endpoint: string) {
  return await page.waitForResponse(
    (response) =>
      response.url().includes(endpoint) && response.status() === 200,
  );
}
```

These patterns will help you write maintainable, reliable Playwright tests.
