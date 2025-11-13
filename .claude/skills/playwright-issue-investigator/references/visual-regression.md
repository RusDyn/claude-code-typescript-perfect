# Visual Regression Testing

## Basic Setup

```typescript
test("visual test", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveScreenshot("homepage.png");
});
```

First run creates baseline, subsequent runs compare.

## Configuration

```typescript
// playwright.config.ts
expect: {
  toHaveScreenshot: {
    maxDiffPixels: 100,
    threshold: 0.2,
  },
}
```

## Update Baselines

```bash
# Update all baselines
npx playwright test --update-snapshots

# Update specific test
npx playwright test homepage.spec.ts --update-snapshots
```

## Element Screenshots

```typescript
// Compare specific element
await expect(page.locator(".header")).toHaveScreenshot("header.png");
```

## Ignore Dynamic Content

```typescript
await expect(page).toHaveScreenshot("page.png", {
  mask: [page.locator(".timestamp")],
});
```

Use for catching unintended visual changes.
