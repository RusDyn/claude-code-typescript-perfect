# Network Debugging

## Monitor Requests

```typescript
page.on("request", (request) => {
  console.log(request.method(), request.url());
});

page.on("response", (response) => {
  console.log(response.status(), response.url());
});
```

## Wait for Specific Request

```typescript
const response = await page.waitForResponse(
  (resp) => resp.url().includes("/api/users") && resp.status() === 200,
);
const data = await response.json();
```

## Mock Responses

```typescript
// Mock API
await page.route("**/api/**", (route) => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ success: true }),
  });
});

// Block resources
await page.route("**/*.{png,jpg,jpeg}", (route) => route.abort());
```

## Modify Requests

```typescript
await page.route("**/api/users", (route) => {
  const headers = route.request().headers();
  headers["Authorization"] = "Bearer test-token";
  route.continue({ headers });
});
```

Essential for API testing and debugging.
