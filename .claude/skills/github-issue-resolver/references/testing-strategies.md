# Testing Strategies for Issue Resolution

Guide to testing changes effectively before creating pull requests.

## Testing Philosophy

Before submitting a PR:

1. **Verify the fix** - Confirm the issue is resolved
2. **Prevent regressions** - Ensure nothing else breaks
3. **Cover edge cases** - Test boundary conditions
4. **Document behavior** - Tests serve as documentation

## Test Types

### Unit Tests

Test individual functions/methods in isolation.

**When to write:**

- New utility functions
- Complex business logic
- Data transformations
- Input validation

**Example (JavaScript/Jest):**

```javascript
// Function to test
function isValidEmail(email) {
  if (!email || typeof email !== "string") return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Unit tests
describe("isValidEmail", () => {
  it("returns true for valid emails", () => {
    expect(isValidEmail("user@example.com")).toBe(true);
  });

  it("returns false for invalid emails", () => {
    expect(isValidEmail("invalid")).toBe(false);
    expect(isValidEmail("missing@domain")).toBe(false);
  });

  it("handles edge cases", () => {
    expect(isValidEmail(null)).toBe(false);
    expect(isValidEmail(undefined)).toBe(false);
    expect(isValidEmail("")).toBe(false);
  });
});
```

### Integration Tests

Test how components work together.

**When to write:**

- API endpoints
- Database operations
- Service interactions
- Feature workflows

**Example (Python/pytest):**

```python
def test_user_registration_flow():
    # Create user
    response = client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'secure123'
    })
    assert response.status_code == 201

    # Verify user in database
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.email == 'test@example.com'

    # Verify login works
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'secure123'
    })
    assert response.status_code == 200
```

### End-to-End Tests

Test complete user workflows.

**When to write:**

- Critical user paths
- Multi-step processes
- UI interactions
- Cross-system features

## Running Tests

### JavaScript/Node.js

```bash
# Jest
npm test
npm run test:watch  # Watch mode
npm run test:coverage  # With coverage

# Specific tests
npm test -- auth.test.js
npm test -- --grep "email validation"

# Mocha
npx mocha tests/
npx mocha tests/auth.test.js
```

### Python

```bash
# pytest
pytest
pytest -v  # Verbose
pytest --cov  # Coverage
pytest tests/test_auth.py  # Specific file
pytest -k "email"  # Match test names

# unittest
python -m unittest
python -m unittest tests.test_auth
```

### Go

```bash
go test ./...  # All packages
go test -v ./...  # Verbose
go test -cover ./...  # Coverage
go test -run TestEmailValidation  # Specific test
```

### Rust

```bash
cargo test
cargo test --verbose
cargo test test_email_validation  # Specific test
cargo test -- --nocapture  # Show println!
```

## Test-Driven Development (TDD)

For bug fixes, follow TDD:

1. **Write failing test** - Reproduces the bug
2. **Implement fix** - Make the test pass
3. **Refactor** - Clean up if needed

**Example:**

```javascript
// 1. Write failing test
it("should not crash with null email", () => {
  expect(() => authenticate(null, "password")).not.toThrow();
});
// Test fails ❌

// 2. Implement fix
function authenticate(email, password) {
  if (!email) throw new Error("Email required");
  // ... rest of function
}
// Test passes ✅

// 3. Refactor if needed
```

## Edge Cases to Test

### Input Validation

- Null/undefined
- Empty strings
- Whitespace
- Very long inputs
- Special characters
- Unicode characters

### Boundary Conditions

- Zero, one, many
- First, middle, last
- Empty collections
- Single item collections
- Maximum sizes

### Error Conditions

- Network failures
- Database errors
- Permission denied
- Resource not found
- Invalid credentials

## Writing Good Tests

### Arrange, Act, Assert Pattern

```javascript
it("calculates total price correctly", () => {
  // Arrange - Setup
  const items = [
    { price: 10.0, quantity: 2 },
    { price: 5.5, quantity: 3 },
  ];

  // Act - Execute
  const total = calculateTotal(items);

  // Assert - Verify
  expect(total).toBe(36.5);
});
```

### Test Names

Good test names describe behavior:

✅ `should return 404 when user not found`
✅ `should validate email format`
✅ `should throw error on invalid input`

❌ `test1`
❌ `works`
❌ `returns value`

### One Assertion Per Test (Generally)

```javascript
// ❌ Too many assertions
it("validates user", () => {
  expect(user.email).toBe("test@example.com");
  expect(user.name).toBe("Test User");
  expect(user.age).toBe(25);
  expect(user.active).toBe(true);
});

// ✅ Split into focused tests
it("sets email correctly", () => {
  expect(user.email).toBe("test@example.com");
});

it("sets name correctly", () => {
  expect(user.name).toBe("Test User");
});
```

## Manual Testing

When automated tests aren't enough:

### UI Changes

1. Run application locally
2. Navigate to affected page
3. Test changed functionality
4. Test in different browsers
5. Test responsive design
6. Check accessibility

### API Changes

```bash
# Test with curl
curl -X POST http://localhost:3000/api/auth \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "pass123"}'

# Test with httpie
http POST localhost:3000/api/auth email=test@example.com password=pass123
```

## Coverage Goals

Aim for:

- **Critical paths**: 100% coverage
- **Business logic**: 80%+ coverage
- **Utility functions**: 90%+ coverage
- **Overall project**: 70%+ coverage

But remember: **Coverage ≠ Quality**

100% coverage with bad tests is worse than 70% coverage with good tests.

## Common Testing Patterns

### Mocking External Dependencies

```javascript
// Mock API calls
jest.mock('axios');
axios.get.mockResolvedValue({ data: { user: {...} } });

// Mock database
jest.mock('../db');
db.query.mockResolvedValue([{ id: 1, name: 'Test' }]);
```

### Testing Async Code

```javascript
// Using async/await
it("fetches user data", async () => {
  const user = await fetchUser(1);
  expect(user.id).toBe(1);
});

// Using promises
it("fetches user data", () => {
  return fetchUser(1).then((user) => {
    expect(user.id).toBe(1);
  });
});
```

### Testing Error Handling

```javascript
it("throws error on invalid input", () => {
  expect(() => validateEmail("invalid")).toThrow("Invalid email");
});

it("handles network errors", async () => {
  axios.get.mockRejectedValue(new Error("Network error"));

  await expect(fetchUser(1)).rejects.toThrow("Network error");
});
```

## Test Organization

```
tests/
├── unit/
│   ├── utils/
│   │   ├── validation.test.js
│   │   └── formatting.test.js
│   └── services/
│       └── auth.test.js
├── integration/
│   ├── api/
│   │   └── auth.test.js
│   └── database/
│       └── user.test.js
└── e2e/
    └── user-flow.test.js
```

## Before Submitting PR

Run this checklist:

```bash
# 1. Run all tests
npm test

# 2. Check coverage
npm run test:coverage

# 3. Run linter
npm run lint

# 4. Format code
npm run format

# 5. Type check (if TypeScript)
npm run type-check

# 6. Build
npm run build

# 7. Manual smoke test
npm start
# Then test in browser
```

## CI/CD Integration

Your tests should run automatically on:

- Every commit (local pre-commit hook)
- Every push (CI pipeline)
- Every PR (required checks)

Ensure all checks pass before merging.

## Testing Checklist

For each change:

- [ ] Unit tests added for new functions
- [ ] Integration tests for new features
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] All existing tests still pass
- [ ] No test warnings
- [ ] Coverage maintained or improved
- [ ] Manual testing completed (if applicable)
- [ ] Tests document the behavior clearly
- [ ] Tests run in CI/CD successfully
