---
name: chrome-extension-builder
description: Build Chrome extensions (Manifest V3) for content injection, DOM manipulation, and network interception. Use when (1) Creating new Chrome extensions, (2) Adding features to existing extensions, (3) Analyzing web pages for extension opportunities, (4) Generating extension code (content scripts, background workers, manifests), (5) Handling SPAs and shadow DOM. DO NOT use for general web scraping or automation - use playwright-automation instead. Focus: Chrome extension development, Manifest V3, content scripts, and DOM manipulation.
---

# Chrome Extension Builder

Comprehensive toolkit for analyzing web pages and building robust Chrome extensions (Manifest V3) that inject functionality, extract data, and modify page behavior.

## When to Use This Skill

Use chrome-extension-builder when you need to:

- **Create new Chrome extensions** with Manifest V3
- **Build content scripts** to inject functionality into web pages
- **Generate extension manifests** with proper permissions and configuration
- **Analyze HTML structure** to understand DOM manipulation opportunities
- **Handle SPAs and shadow DOM** in extension context
- **Create background service workers** for Chrome extensions
- **Implement network interception** in extensions

## When NOT to Use This Skill

**DO NOT use chrome-extension-builder for:**

- **General web scraping** → Use `playwright-automation` skill instead
- **E2E testing of web applications** → Use `playwright-test-builder` or `playwright-automation`
- **Server-side automation** → Use appropriate backend tools
- **Browser automation without extensions** → Use `playwright-automation` instead
- **Mobile app extensions** → This is Chrome desktop extension specific

**Clear distinction:**

- `chrome-extension-builder` = Building Chrome browser extensions (persistent, installed)
- `playwright-automation` = Ad-hoc web automation and scraping (temporary, script-based)

## Quick Start

### 1. Analyze HTML Structure

Use the HTML analyzer to understand page structure and get selector recommendations:

```bash
# Analyze from file
python scripts/analyze_html.py page.html

# Or from stdin
curl https://example.com | python scripts/analyze_html.py -
```

Output includes page type detection (e-commerce, social media, SPA), element counts, data attributes, selector recommendations, and SPA handling advice.

### 2. Generate Robust Selectors

For specific elements, generate multiple selector strategies with fallbacks:

```bash
python scripts/selector_finder.py '{
  "tag": "button",
  "attrs": {"id": "buy-button", "class": "btn primary", "data-action": "purchase"},
  "text": "Buy Now"
}'
```

Returns prioritized selectors (CSS and XPath) with stability ratings and fallback code.

### 3. Generate Manifest V3

Create properly configured manifest based on requirements:

```bash
python scripts/generate_manifest.py '{
  "name": "My Extension",
  "features": ["content_script", "storage", "network_interception"],
  "target_urls": ["https://example.com/*"]
}'
```

## Core Concepts

### Selector Strategy

Always use fallback selectors in priority order:

1. **Data attributes** (`[data-product-id]`) - Most stable
2. **Semantic IDs** (`#submit-button`) - Stable if not generated
3. **ARIA/Role** (`[role="button"]`) - Accessibility-based
4. **Name attributes** (`[name="email"]`) - Stable for forms
5. **Stable classes** (`.primary-action`) - Avoid generated classes
6. **Element + attribute** (`button[type="submit"]`) - Generic fallback

Example fallback implementation:

```javascript
function findElementWithFallback(selectors) {
  for (const selector of selectors) {
    const element = document.querySelector(selector)
    if (element) return element
  }
  return null
}

const button = findElementWithFallback([
  '[data-action="buy"]', // Best
  '#buy-button',
  'button.primary-action',
  'button[type="submit"]', // Fallback
])
```

### Handling Dynamic Content

For SPAs and dynamic pages:

```javascript
async function waitForElement(selector, timeout = 10000) {
  const element = document.querySelector(selector)
  if (element) return element

  return new Promise((resolve, reject) => {
    const observer = new MutationObserver(() => {
      const element = document.querySelector(selector)
      if (element) {
        observer.disconnect()
        resolve(element)
      }
    })

    observer.observe(document.body, { childList: true, subtree: true })

    setTimeout(() => {
      observer.disconnect()
      reject(new Error('Element not found'))
    }, timeout)
  })
}
```

### SPA Navigation Detection

Detect route changes in Single Page Applications:

```javascript
let lastUrl = location.href
const observer = new MutationObserver(() => {
  if (location.href !== lastUrl) {
    lastUrl = location.href
    injectFeatures() // Reinject on navigation
  }
})

observer.observe(document.body, { childList: true, subtree: true })

// Also intercept history API
const originalPushState = history.pushState
history.pushState = function (...args) {
  originalPushState.apply(this, args)
  injectFeatures()
}
```

## Reference Documentation

- **references/manifest-v3-guide.md** - Complete Manifest V3 reference, permissions, API usage, migration from V2
- **references/content-script-patterns.md** - Common injection patterns, UI creation, data extraction, complete examples
- **references/spa-handling.md** - React/Vue/Angular detection and handling, framework-specific patterns

## Template Assets

- **assets/templates/manifest.json** - Base Manifest V3 configuration
- **assets/templates/background.js** - Service worker with message passing, storage, API calls
- **assets/templates/content.js** - Content script with SPA support and injection patterns
- **assets/templates/popup.html** - Extension popup UI
- **assets/templates/popup.js** - Popup logic and settings management

## Example Extensions

- **assets/examples/openai-extender/** - Enhance OpenAI pages with custom features
- **assets/examples/marketplace-score/** - Inject trust scores into e-commerce buy buttons

## Common Workflows

### Workflow 1: Inject Button Into Page

1. Analyze page to identify target element
2. Generate robust selectors with fallbacks
3. Use content script template
4. Wait for element: `await waitForElement(selector)`
5. Check if already injected
6. Create and inject button with event handlers

### Workflow 2: Extract Data From Page

1. Identify data location using HTML analyzer
2. Generate selectors for each data point
3. Use fallback chains for reliability
4. Extract and structure data
5. Send to background script via `chrome.runtime.sendMessage()`
6. Background script stores or sends to API

### Workflow 3: Intercept Network Requests

**Option A: DeclarativeNetRequest (for simple cases)**

- Add `declarativeNetRequest` permission
- Create rules.json with request patterns
- Define actions (block, modify, redirect)

**Option B: Fetch/XHR interception (for complex cases)**

- Inject script into page context
- Override `window.fetch` or `XMLHttpRequest.prototype`
- Intercept requests/responses
- Communicate via `window.postMessage()`

### Workflow 4: Monitor Page Changes

1. Set up MutationObserver on target container
2. Debounce callback to avoid excessive triggers
3. Check for specific changes (new elements, attributes)
4. React by reinjecting or updating features

## Best Practices

**Performance:** Debounce operations, use `requestIdleCallback`, batch DOM operations, disconnect observers

**Reliability:** Use selector fallback chains, handle missing elements gracefully, test on SPAs, add error logging

**UX:** Use shadow DOM to avoid style conflicts, make injections visually distinct, add loading states, respect user preferences

**Security:** Sanitize input, don't trust page data, use CSP-compliant code, validate messages

## Debugging

**View Logs:**

- Content script: Regular DevTools on page
- Background: "Inspect views: service worker" on chrome://extensions
- Popup: Right-click popup → "Inspect"

**Test Selectors:**

```javascript
document.querySelector('[data-action="buy"]')
$$('[class*="button"]') // All matches
$x('//button[text()="Buy"]') // XPath
```

## Troubleshooting

**Element not found:** Check page load, verify selector in DevTools, increase timeout, check SPA navigation

**Injection disappears:** SPA clearing DOM - add navigation detection, re-inject on route changes

**Content script not loading:** Check manifest matches/host_permissions, verify run_at timing, check CSP

**CORS errors:** Move API calls to background script (bypasses CORS)

## Advanced Topics

**Shadow DOM Isolation:**

```javascript
const container = document.createElement('div')
document.body.appendChild(container)
const shadow = container.attachShadow({ mode: 'open' })
shadow.innerHTML = `<style>/* Isolated */</style><div>Content</div>`
```

**Persistent State:**

```javascript
await chrome.storage.local.set({ myState: data })
const { myState } = await chrome.storage.local.get('myState')
chrome.storage.onChanged.addListener(changes => {
  if (changes.myState) updateUI(changes.myState.newValue)
})
```

**Dynamic Injection:**

```javascript
chrome.scripting.executeScript({
  target: { tabId: tabId },
  func: () => {
    document.body.style.background = 'red'
  },
})
```

## Testing Strategy

1. Test on multiple target sites
2. Test SPAs (React/Vue/Angular)
3. Test dynamic content (infinite scroll, lazy loading)
4. Test navigation (back/forward, route changes)
5. Test edge cases (slow connections, missing elements)
6. Start with one site, perfect it, then expand

Start with minimal permissions and add as needed.
