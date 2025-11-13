# Page Object Model (POM) Guide

Complete guide to implementing Page Object Model pattern in Playwright tests.

## What is Page Object Model?

POM is a design pattern that:

- Encapsulates page elements and interactions
- Reduces code duplication
- Makes tests more maintainable
- Separates test logic from page structure

## Basic Page Object

```typescript
// pages/LoginPage.ts
import { Page, Locator } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[name="email"]');
    this.passwordInput = page.locator('[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('[data-testid="error"]');
  }

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }
}
```

## Usage in Tests

```typescript
import { test, expect } from "@playwright/test";
import { LoginPage } from "../pages/LoginPage";

test("should login successfully", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login("test@example.com", "password123");

  await expect(page).toHaveURL("/dashboard");
});

test("should show error for invalid credentials", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login("wrong@example.com", "wrong");

  const error = await loginPage.getErrorMessage();
  expect(error).toContain("Invalid credentials");
});
```

## Advanced Patterns

### Method Chaining

```typescript
export class ProductPage {
  // ... constructor and locators ...

  async selectSize(size: string) {
    await this.page.click(`[data-size="${size}"]`);
    return this;
  }

  async selectColor(color: string) {
    await this.page.click(`[data-color="${color}"]`);
    return this;
  }

  async addToCart() {
    await this.addToCartButton.click();
    return this;
  }
}

// Usage with chaining
await productPage.selectSize("L").selectColor("Blue").addToCart();
```

### Component Objects

```typescript
// components/Navigation.ts
export class Navigation {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goToProducts() {
    await this.page.click('[data-nav="products"]');
  }

  async goToCart() {
    await this.page.click('[data-nav="cart"]');
  }

  async search(query: string) {
    await this.page.fill('[data-testid="search"]', query);
    await this.page.press('[data-testid="search"]', "Enter");
  }
}

// Use in page objects
export class HomePage {
  readonly page: Page;
  readonly navigation: Navigation;

  constructor(page: Page) {
    this.page = page;
    this.navigation = new Navigation(page);
  }
}
```

### Base Page Class

```typescript
// pages/BasePage.ts
export class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState("networkidle");
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }

  async getTitle() {
    return await this.page.title();
  }
}

// Extend in specific pages
export class LoginPage extends BasePage {
  readonly emailInput: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.locator('[name="email"]');
  }
}
```

## Best Practices

1. **One page object per page/component**
2. **Methods return Page Objects for chaining**
3. **Keep locators as readonly properties**
4. **Include only public methods that tests need**
5. **Don't include assertions in page objects**
6. **Use descriptive method names**

## Full Example

```typescript
// pages/CheckoutPage.ts
import { Page, Locator } from "@playwright/test";

export class CheckoutPage {
  readonly page: Page;
  readonly shippingForm: {
    firstName: Locator;
    lastName: Locator;
    address: Locator;
    city: Locator;
    zipCode: Locator;
  };
  readonly paymentForm: {
    cardNumber: Locator;
    expiryDate: Locator;
    cvv: Locator;
  };
  readonly placeOrderButton: Locator;
  readonly orderConfirmation: Locator;

  constructor(page: Page) {
    this.page = page;

    this.shippingForm = {
      firstName: page.locator('[name="firstName"]'),
      lastName: page.locator('[name="lastName"]'),
      address: page.locator('[name="address"]'),
      city: page.locator('[name="city"]'),
      zipCode: page.locator('[name="zipCode"]'),
    };

    this.paymentForm = {
      cardNumber: page.locator('[name="cardNumber"]'),
      expiryDate: page.locator('[name="expiry"]'),
      cvv: page.locator('[name="cvv"]'),
    };

    this.placeOrderButton = page.locator('button[type="submit"]');
    this.orderConfirmation = page.locator('[data-testid="confirmation"]');
  }

  async goto() {
    await this.page.goto("/checkout");
  }

  async fillShippingInfo(info: ShippingInfo) {
    await this.shippingForm.firstName.fill(info.firstName);
    await this.shippingForm.lastName.fill(info.lastName);
    await this.shippingForm.address.fill(info.address);
    await this.shippingForm.city.fill(info.city);
    await this.shippingForm.zipCode.fill(info.zipCode);
  }

  async fillPaymentInfo(payment: PaymentInfo) {
    await this.paymentForm.cardNumber.fill(payment.cardNumber);
    await this.paymentForm.expiryDate.fill(payment.expiryDate);
    await this.paymentForm.cvv.fill(payment.cvv);
  }

  async placeOrder() {
    await this.placeOrderButton.click();
    await this.page.waitForLoadState("networkidle");
  }

  async getOrderNumber() {
    const text = await this.orderConfirmation.textContent();
    const match = text?.match(/Order #(\d+)/);
    return match ? match[1] : null;
  }
}

// Types
interface ShippingInfo {
  firstName: string;
  lastName: string;
  address: string;
  city: string;
  zipCode: string;
}

interface PaymentInfo {
  cardNumber: string;
  expiryDate: string;
  cvv: string;
}
```

This pattern makes tests clean, maintainable, and easy to update when UI changes.
