# Common Automation Patterns

Proven patterns for browser automation tasks using Playwright.

## Table of Contents

1. [Navigation Patterns](#navigation-patterns)
2. [Form Interaction](#form-interaction)
3. [Data Extraction](#data-extraction)
4. [Error Handling](#error-handling)
5. [Authentication](#authentication)
6. [File Operations](#file-operations)

## Navigation Patterns

### Basic Navigation

```typescript
// Simple navigation
await page.goto('http://localhost:3000')

// Wait for network idle
await page.goto('http://localhost:3000', { waitUntil: 'networkidle' })

// With timeout
await page.goto('http://localhost:3000', { timeout: 30000 })
```

### Multi-Step Navigation

```typescript
const steps = [
  { url: '/', wait: 'networkidle' },
  { selector: 'a:has-text("Products")', action: 'click' },
  { selector: 'button.add-to-cart', action: 'click' },
]

for (const step of steps) {
  if (step.url) {
    await page.goto(`http://localhost:3000${step.url}`, {
      waitUntil: step.wait || 'load',
    })
  } else if (step.selector && step.action === 'click') {
    await safeClick(page, step.selector)
  }
}
```

### URL Validation

```typescript
// Wait for specific URL
await page.waitForURL('**/dashboard')

// Check current URL
const currentUrl = page.url()
console.log('Current URL:', currentUrl)

// Navigate back and forward
await page.goBack()
await page.goForward()
```

## Form Interaction

### Simple Form Fill

```typescript
const { fillForm } = require('../scripts/helpers.js')

await fillForm(
  page,
  {
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+1234567890',
    message: 'Hello world',
  },
  {
    submitButton: 'button[type="submit"]',
    waitForNavigation: true,
  }
)
```

### Complex Form Handling

```typescript
// Radio buttons
await page.check('input[type="radio"][value="option1"]')

// Checkboxes
await page.check('input[type="checkbox"][name="agree"]')
await page.uncheck('input[type="checkbox"][name="newsletter"]')

// Select dropdowns
await page.selectOption('select[name="country"]', 'US')
await page.selectOption('select[name="city"]', { label: 'New York' })

// Multi-select
await page.selectOption('select[multiple]', ['option1', 'option2'])

// File upload
await page.setInputFiles('input[type="file"]', '/path/to/file.pdf')
```

### Form Validation

```typescript
// Check for error messages
const errorVisible = await elementExists(page, '.error-message')
if (errorVisible) {
  const errorText = await getText(page, '.error-message')
  console.log('Validation error:', errorText)
}

// Check field validity
const isValid = await page.evaluate(() => {
  const input = document.querySelector('input[name="email"]')
  return input.validity.valid
})
```

## Data Extraction

### Extract Text Content

```typescript
// Single element
const title = await page.textContent('h1')

// Multiple elements
const items = await page.$$eval('li.product', elements =>
  elements.map(el => el.textContent.trim())
)

// Structured data
const products = await page.$$eval('.product-card', cards =>
  cards.map(card => ({
    name: card.querySelector('.name')?.textContent,
    price: card.querySelector('.price')?.textContent,
    image: card.querySelector('img')?.src,
  }))
)
```

### Extract Attributes

```typescript
// Get attribute
const href = await page.getAttribute('a.download', 'href')

// Get multiple attributes
const links = await page.$$eval('a', anchors =>
  anchors.map(a => ({
    text: a.textContent,
    href: a.href,
    target: a.target,
  }))
)
```

### Extract Tables

```typescript
const { extractTableData } = require('../scripts/helpers.js')

// Simple table extraction
const data = await extractTableData(page, 'table.users')

// Manual table extraction with custom logic
const tableData = await page.evaluate(() => {
  const rows = Array.from(document.querySelectorAll('table tr'))
  return rows.map(row => {
    const cells = Array.from(row.querySelectorAll('td, th'))
    return cells.map(cell => cell.textContent.trim())
  })
})
```

### API Response Interception

```typescript
// Intercept and extract API responses
const apiData = []

page.on('response', async response => {
  if (response.url().includes('/api/users')) {
    const data = await response.json()
    apiData.push(data)
  }
})

await page.goto('http://localhost:3000/users')
await waitForNetworkIdle(page)

console.log('Collected API data:', apiData)
```

## Error Handling

### Try-Catch Pattern

```typescript
async function automateTask(page) {
  try {
    await safeClick(page, 'button.submit')
    console.log('✅ Task completed')
  } catch (error) {
    console.error('❌ Task failed:', error.message)
    await takeScreenshot(page, 'error')
    throw error
  }
}
```

### Retry Pattern

```typescript
async function retryOperation(operation, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation()
    } catch (error) {
      if (attempt === maxRetries) throw error
      console.log(`Attempt ${attempt} failed, retrying...`)
      await new Promise(resolve => setTimeout(resolve, 1000 * attempt))
    }
  }
}

// Usage
await retryOperation(async () => {
  await page.goto('http://localhost:3000')
  await page.waitForSelector('.content', { timeout: 5000 })
})
```

### Graceful Degradation

```typescript
// Try preferred method, fall back to alternative
let success = false

try {
  await safeClick(page, 'button#primary-action')
  success = true
} catch (error) {
  console.log('Primary action failed, trying alternative...')
  try {
    await page.evaluate(() => {
      document.querySelector('button#alternative-action')?.click()
    })
    success = true
  } catch (altError) {
    console.error('Both actions failed')
  }
}
```

## Authentication

### Login Pattern

```typescript
async function login(page, credentials) {
  await page.goto('http://localhost:3000/login')

  await safeType(page, 'input[name="email"]', credentials.email)
  await safeType(page, 'input[name="password"]', credentials.password)

  await safeClick(page, 'button[type="submit"]')

  // Wait for successful login
  await page.waitForURL('**/dashboard', { timeout: 10000 })

  // Verify login
  const isLoggedIn = await elementExists(page, '.user-menu')
  if (!isLoggedIn) {
    throw new Error('Login verification failed')
  }

  return true
}
```

### Token-Based Auth

```typescript
// Set auth token directly
await page.evaluate(token => {
  localStorage.setItem('authToken', token)
  // or
  document.cookie = `token=${token}; path=/`
}, 'your-auth-token')

await page.goto('http://localhost:3000/dashboard')
```

### Session Persistence

```typescript
// Save authentication state
const context = await browser.newContext()
const page = await context.newPage()

// Login once
await login(page, credentials)

// Save state
await context.storageState({ path: '/tmp/auth-state.json' })

// Reuse in new context
const newContext = await browser.newContext({
  storageState: '/tmp/auth-state.json',
})
```

## File Operations

### Download Files

```typescript
// Wait for download
const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.click('a.download-link'),
])

// Save file
const path = `/tmp/${download.suggestedFilename()}`
await download.saveAs(path)
console.log('Downloaded:', path)
```

### Upload Files

```typescript
// Single file
await page.setInputFiles('input[type="file"]', '/path/to/file.pdf')

// Multiple files
await page.setInputFiles('input[type="file"]', [
  '/path/to/file1.pdf',
  '/path/to/file2.jpg',
])

// Remove files
await page.setInputFiles('input[type="file"]', [])
```

### Working with PDFs

```typescript
// Generate PDF from page
await page.pdf({
  path: '/tmp/page.pdf',
  format: 'A4',
  printBackground: true,
})
```

## Advanced Patterns

### Parallel Operations

```typescript
// Run multiple operations concurrently
await Promise.all([
  page.goto('http://localhost:3000/page1'),
  page.goto('http://localhost:3000/page2'),
  page.goto('http://localhost:3000/page3'),
])

// With separate pages
const [page1, page2, page3] = await Promise.all([
  context.newPage(),
  context.newPage(),
  context.newPage(),
])

await Promise.all([
  page1.goto('http://localhost:3000/page1'),
  page2.goto('http://localhost:3000/page2'),
  page3.goto('http://localhost:3000/page3'),
])
```

### Conditional Actions

```typescript
// Perform action only if element exists
if (await elementExists(page, '.cookie-banner')) {
  await handleCookieBanner(page)
}

// Wait for one of multiple elements
const element = await page.waitForSelector('.success-message, .error-message', {
  timeout: 5000,
})

const className = await element.getAttribute('class')
if (className.includes('success')) {
  console.log('Operation succeeded')
} else {
  console.log('Operation failed')
}
```

### Dynamic Content Handling

```typescript
// Wait for dynamic content to load
await page.waitForFunction(
  () => document.querySelectorAll('.product-card').length > 0,
  { timeout: 10000 }
)

// Infinite scroll
async function scrollToBottom(page) {
  await page.evaluate(async () => {
    await new Promise(resolve => {
      let totalHeight = 0
      const distance = 100
      const timer = setInterval(() => {
        window.scrollBy(0, distance)
        totalHeight += distance

        if (totalHeight >= document.body.scrollHeight) {
          clearInterval(timer)
          resolve()
        }
      }, 100)
    })
  })
}
```

## Best Practices

1. **Always use try-catch** for error handling
2. **Take screenshots** on errors for debugging
3. **Wait for elements** before interacting
4. **Use helper functions** for common operations
5. **Log progress** for visibility
6. **Parameterize URLs** at script top
7. **Clean up resources** with finally blocks
8. **Test selectors** before bulk operations

These patterns provide a solid foundation for building reliable browser automation scripts.
