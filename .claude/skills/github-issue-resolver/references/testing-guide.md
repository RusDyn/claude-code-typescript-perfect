# Testing Guide

Comprehensive guide to testing implementations before creating pull requests.

## Testing Pyramid

```
       /\
      /  \     E2E Tests (Few)
     /----\
    /      \   Integration Tests (Some)
   /--------\
  /          \ Unit Tests (Many)
 /____________\
```

**Ratio:** 70% Unit, 20% Integration, 10% E2E

## Unit Tests

### What to Test

**Every function should have tests for:**

- Happy path (expected inputs)
- Edge cases (boundary conditions)
- Error cases (invalid inputs)
- Return values
- Side effects

### Writing Good Unit Tests

**Structure: Arrange-Act-Assert**

```javascript
test('calculateTotal adds item prices correctly', () => {
  // Arrange
  const items = [{ price: 10 }, { price: 20 }, { price: 30 }]

  // Act
  const total = calculateTotal(items)

  // Assert
  expect(total).toBe(60)
})
```

### Test Coverage

**Aim for:**

- 80%+ code coverage
- 100% critical path coverage
- All error branches covered

**Check coverage:**

```bash
npm test -- --coverage
```

### Example: Bug Fix Tests

**For issue: "Login button doesn't work on mobile"**

```javascript
describe('LoginButton', () => {
  test('calls login handler when clicked', () => {
    const handleLogin = jest.fn()
    render(<LoginButton onLogin={handleLogin} />)

    fireEvent.click(screen.getByRole('button'))

    expect(handleLogin).toHaveBeenCalledTimes(1)
  })

  test('works with touch events on mobile', () => {
    const handleLogin = jest.fn()
    render(<LoginButton onLogin={handleLogin} />)

    fireEvent.touchStart(screen.getByRole('button'))
    fireEvent.touchEnd(screen.getByRole('button'))

    expect(handleLogin).toHaveBeenCalled()
  })

  test('shows loading state during authentication', () => {
    render(<LoginButton />)

    fireEvent.click(screen.getByRole('button'))

    expect(screen.getByRole('button')).toBeDisabled()
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })
})
```

### Example: Feature Tests

**For feature: "Add CSV export"**

```javascript
describe('CSV Export', () => {
  test('generates correct CSV from data', () => {
    const data = [
      { name: 'John', age: 30 },
      { name: 'Jane', age: 25 },
    ]

    const csv = generateCSV(data)

    expect(csv).toBe('name,age\nJohn,30\nJane,25')
  })

  test('handles empty data', () => {
    const csv = generateCSV([])

    expect(csv).toBe('')
  })

  test('escapes commas in values', () => {
    const data = [{ name: 'Doe, John', age: 30 }]

    const csv = generateCSV(data)

    expect(csv).toContain('"Doe, John"')
  })

  test('handles special characters', () => {
    const data = [{ name: "O'Brien", age: 30 }]

    const csv = generateCSV(data)

    expect(csv).toContain("O'Brien")
  })
})
```

## Integration Tests

### What to Test

**Test interactions between components:**

- API calls with real endpoints (or mocked)
- Database operations
- Multiple components working together
- Data flow through system

### Example: Integration Tests

```javascript
describe('User Authentication Flow', () => {
  test('complete login flow', async () => {
    // Arrange
    const { getByLabelText, getByRole } = render(<LoginPage />)

    // Act
    await userEvent.type(getByLabelText(/email/i), 'user@example.com')
    await userEvent.type(getByLabelText(/password/i), 'password123')
    await userEvent.click(getByRole('button', { name: /login/i }))

    // Assert
    await waitFor(() => {
      expect(window.location.pathname).toBe('/dashboard')
    })
  })

  test('shows error on invalid credentials', async () => {
    // Arrange - Mock API to return error
    server.use(
      rest.post('/api/login', (req, res, ctx) => {
        return res(ctx.status(401), ctx.json({ error: 'Invalid credentials' }))
      })
    )

    const { getByText, getByRole } = render(<LoginPage />)

    // Act
    await userEvent.click(getByRole('button', { name: /login/i }))

    // Assert
    expect(await getByText(/invalid credentials/i)).toBeInTheDocument()
  })
})
```

## End-to-End Tests

### What to Test

**Critical user journeys:**

- Complete workflows
- Multi-page flows
- Real browser environment
- Actual backend integration

### Tools

**Popular E2E frameworks:**

- Cypress
- Playwright
- Selenium
- Puppeteer

### Example: E2E Tests

```javascript
// Playwright example
test('user can complete purchase', async ({ page }) => {
  // Navigate to site
  await page.goto('https://example.com')

  // Add item to cart
  await page.click('text=Add to Cart')

  // Go to checkout
  await page.click('text=Checkout')

  // Fill payment info
  await page.fill('[name="cardNumber"]', '4242424242424242')
  await page.fill('[name="expiry"]', '12/25')
  await page.fill('[name="cvv"]', '123')

  // Complete purchase
  await page.click('text=Pay Now')

  // Verify success
  await expect(page.locator('text=Order Confirmed')).toBeVisible()
})
```

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle

```
1. Write failing test (Red)
     ↓
2. Write minimum code to pass (Green)
     ↓
3. Refactor and improve (Refactor)
     ↓
   Repeat
```

### Example: TDD Workflow

**1. Write failing test:**

```javascript
test('login button redirects to dashboard', async () => {
  render(<LoginButton />)

  await userEvent.click(screen.getByRole('button'))

  expect(window.location.pathname).toBe('/dashboard')
})

// Test fails: Function not implemented
```

**2. Write minimal implementation:**

```javascript
function LoginButton() {
  const handleClick = () => {
    window.location.href = '/dashboard'
  }

  return <button onClick={handleClick}>Login</button>
}

// Test passes!
```

**3. Refactor:**

```javascript
function LoginButton() {
  const navigate = useNavigate()

  const handleClick = async () => {
    try {
      await authenticate()
      navigate('/dashboard')
    } catch (error) {
      showError(error)
    }
  }

  return <button onClick={handleClick}>Login</button>
}

// Test still passes, but code is better
```

## Testing Strategies by Issue Type

### For Bug Fixes

**1. Write test that reproduces bug:**

```javascript
test('reproduces bug #123', () => {
  // Setup exact conditions from bug report
  const button = render(<LoginButton />)

  // Perform actions from reproduction steps
  fireEvent.click(button.getByRole('button'))

  // Expect: Should fail before fix
  expect(handleLogin).toHaveBeenCalled()
})
```

**2. Verify test fails:**

```bash
npm test
# Test should fail
```

**3. Fix the bug**

**4. Verify test passes:**

```bash
npm test
# Test should pass
```

**5. Add edge case tests:**

```javascript
test('works on mobile devices', () => {
  /* ... */
})
test('works with touch events', () => {
  /* ... */
})
test('works with keyboard navigation', () => {
  /* ... */
})
```

### For New Features

**1. Write tests for acceptance criteria:**

```javascript
describe('CSV Export Feature', () => {
  test('user can click export button', () => {
    /* ... */
  })
  test('generates CSV with correct data', () => {
    /* ... */
  })
  test('downloads file with correct name', () => {
    /* ... */
  })
  test('shows loading state during export', () => {
    /* ... */
  })
  test('handles export errors gracefully', () => {
    /* ... */
  })
})
```

**2. Implement feature to make tests pass**

**3. Add integration tests**

**4. Add E2E test for complete flow**

### For Enhancements

**1. Establish baseline:**

```javascript
test('current performance baseline', () => {
  const start = performance.now()

  processLargeDataset()

  const duration = performance.now() - start
  expect(duration).toBeLessThan(1000) // Current: ~900ms
})
```

**2. Make improvement**

**3. Verify improvement:**

```javascript
test('improved performance', () => {
  const start = performance.now()

  processLargeDataset()

  const duration = performance.now() - start
  expect(duration).toBeLessThan(500) // Target: <500ms
})
```

## Testing Checklist

### Before Creating PR

**Unit Tests:**

- [ ] All new functions have tests
- [ ] Happy path covered
- [ ] Edge cases covered
- [ ] Error cases covered
- [ ] 80%+ coverage
- [ ] All tests passing

**Integration Tests:**

- [ ] Component interactions tested
- [ ] API calls tested
- [ ] Data flow tested
- [ ] Error handling tested

**E2E Tests (if applicable):**

- [ ] Critical path tested
- [ ] Full workflow tested
- [ ] Tests pass in CI

**Manual Testing:**

- [ ] Tested locally
- [ ] Tested in dev environment
- [ ] Tested on target browsers
- [ ] Tested on target devices
- [ ] Tested edge cases

**Regression Testing:**

- [ ] Existing tests still pass
- [ ] Related features work
- [ ] No new errors in console
- [ ] Performance not degraded

## Testing Tools & Setup

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
  ],
  coverageThresholds: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
}
```

### Testing Library

```javascript
// jest.setup.js
import '@testing-library/jest-dom'
import { server } from './mocks/server'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### Mock Service Worker

```javascript
// mocks/server.js
import { setupServer } from 'msw/node'
import { rest } from 'msw'

export const server = setupServer(
  rest.post('/api/login', (req, res, ctx) => {
    return res(ctx.json({ token: 'fake-token' }))
  }),

  rest.get('/api/user', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'Test User' }))
  })
)
```

## Common Testing Pitfalls

### Pitfall 1: Testing Implementation Details

❌ **Bad:**

```javascript
test('uses useState', () => {
  const { result } = renderHook(() => useCounter())
  expect(result.current.state).toBeDefined()
})
```

✅ **Good:**

```javascript
test('counter increments when button clicked', () => {
  render(<Counter />)

  fireEvent.click(screen.getByText('Increment'))

  expect(screen.getByText('Count: 1')).toBeInTheDocument()
})
```

### Pitfall 2: Over-Mocking

❌ **Bad:**

```javascript
// Mocking everything
jest.mock('./utils')
jest.mock('./api')
jest.mock('./components')
```

✅ **Good:**

```javascript
// Only mock what's necessary
jest.mock('./api', () => ({
  fetchUser: jest.fn(),
}))
```

### Pitfall 3: Flaky Tests

❌ **Bad:**

```javascript
test('shows notification', () => {
  render(<Notification />)
  expect(screen.getByText('Success')).toBeInTheDocument()
})
// Fails randomly due to timing
```

✅ **Good:**

```javascript
test('shows notification', async () => {
  render(<Notification />)
  expect(await screen.findByText('Success')).toBeInTheDocument()
})
// Waits for element
```

### Pitfall 4: No Cleanup

❌ **Bad:**

```javascript
test('test 1', () => {
  localStorage.setItem('token', 'abc')
  // No cleanup
})

test('test 2', () => {
  // Affected by test 1's localStorage
})
```

✅ **Good:**

```javascript
afterEach(() => {
  localStorage.clear()
})

test('test 1', () => {
  localStorage.setItem('token', 'abc')
})
```

### Pitfall 5: Not Testing Edge Cases

❌ **Bad:**

```javascript
test('divides numbers', () => {
  expect(divide(10, 2)).toBe(5)
})
```

✅ **Good:**

```javascript
test('divides numbers', () => {
  expect(divide(10, 2)).toBe(5)
  expect(divide(10, 3)).toBeCloseTo(3.33, 2)
  expect(() => divide(10, 0)).toThrow('Division by zero')
  expect(divide(0, 10)).toBe(0)
  expect(divide(-10, 2)).toBe(-5)
})
```

## Test Quality Metrics

### What to Measure

**Coverage:**

- Line coverage
- Branch coverage
- Function coverage
- Statement coverage

**Quality:**

- Test execution time
- Test flakiness rate
- Test maintenance burden

**Effectiveness:**

- Bugs caught by tests
- Tests failing before bugs reach production
- Time to identify failing tests

### Good Targets

- Coverage: 80%+
- Test execution: < 10 seconds
- Flaky tests: < 1%
- All critical paths: 100% covered

Following this testing guide ensures your implementations are thoroughly verified before creating pull requests.
