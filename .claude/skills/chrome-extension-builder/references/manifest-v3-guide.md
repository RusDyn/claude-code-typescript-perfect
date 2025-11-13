# Manifest V3 Reference Guide

Complete reference for Chrome Extension Manifest V3 with best practices and common patterns.

## Core Manifest Fields

### Required Fields

```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0"
}
```

### Recommended Fields

```json
{
  "description": "Clear description of what the extension does",
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

## Permissions

### Common Permissions

- **`storage`** - Chrome storage API (local, sync, session)
- **`tabs`** - Access tab information and manage tabs
- **`cookies`** - Read/write cookies
- **`alarms`** - Schedule code to run periodically
- **`notifications`** - Show desktop notifications
- **`scripting`** - Dynamic script injection (V3)
- **`declarativeNetRequest`** - Block/modify network requests

### Host Permissions

Required for content scripts and API access to specific domains:

```json
"host_permissions": [
  "https://*.example.com/*",
  "https://api.service.com/*"
]
```

Use `"<all_urls>"` only if absolutely necessary (requires additional justification in Chrome Web Store).

## Background Service Workers (V3)

### Basic Structure

```json
"background": {
  "service_worker": "background.js"
}
```

### Key Differences from V2

1. **No persistent background page** - Service workers terminate when idle
2. **No DOM access** - Use offscreen documents if needed
3. **No XMLHttpRequest** - Use `fetch()` instead
4. **Event-driven** - Must register all listeners synchronously at startup

### Best Practices

```javascript
// background.js

// ✅ Register listeners at top level (synchronous)
chrome.runtime.onInstalled.addListener(details => {
  if (details.reason === 'install') {
    // First install
    setupExtension()
  }
})

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete') {
    // Page finished loading
    handlePageLoad(tab)
  }
})

// ❌ Don't register listeners asynchronously
async function badInit() {
  await someAsyncWork()
  chrome.runtime.onMessage.addListener(() => {}) // Won't work!
}

// ✅ Store state in chrome.storage, not variables
chrome.storage.session.set({ lastAction: 'clicked' })

// ❌ Service worker variables are lost when it terminates
let counter = 0 // Will reset!
```

## Content Scripts

### Declaration in Manifest

```json
"content_scripts": [
  {
    "matches": ["https://*.example.com/*"],
    "js": ["content.js"],
    "css": ["styles.css"],
    "run_at": "document_idle",
    "all_frames": false
  }
]
```

### Run Timing

- **`document_start`** - Before any DOM construction (use for early interception)
- **`document_end`** - After DOM construction, before images/subframes load
- **`document_idle`** - After page load (default, safest choice)

### Execution Contexts

Content scripts run in an **isolated world**:

- ✅ Access to DOM
- ✅ Access to Chrome APIs (limited subset)
- ❌ No access to page's JavaScript variables
- ❌ No access to page's `window` object

To interact with page JavaScript:

```javascript
// Inject script into page context
const script = document.createElement('script')
script.textContent = `
  // This runs in the page's context
  window.myPageFunction();
`
;(document.head || document.documentElement).appendChild(script)
script.remove()
```

### Dynamic Injection (V3)

```javascript
// From service worker or popup
chrome.scripting.executeScript({
  target: { tabId: tabId },
  files: ['content.js'],
})

// Or inline code
chrome.scripting.executeScript({
  target: { tabId: tabId },
  func: () => {
    document.body.style.backgroundColor = 'red'
  },
})
```

## Message Passing

### One-Time Messages

```javascript
// Send from content script
chrome.runtime.sendMessage({ action: 'getData', id: 123 }, response => {
  console.log(response)
})

// Receive in background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'getData') {
    fetchData(message.id).then(data => {
      sendResponse({ data })
    })
    return true // Keep channel open for async response
  }
})
```

### Long-Lived Connections

```javascript
// Content script
const port = chrome.runtime.connect({ name: 'data-stream' })
port.postMessage({ type: 'start' })
port.onMessage.addListener(msg => {
  console.log('Received:', msg)
})

// Background
chrome.runtime.onConnect.addListener(port => {
  if (port.name === 'data-stream') {
    port.onMessage.addListener(msg => {
      if (msg.type === 'start') {
        // Send periodic updates
        setInterval(() => {
          port.postMessage({ data: 'update' })
        }, 1000)
      }
    })
  }
})
```

## Network Request Interception

### DeclarativeNetRequest (V3)

Replace webRequest (V2) with declarativeNetRequest:

```json
"permissions": ["declarativeNetRequest"],
"declarative_net_request": {
  "rule_resources": [{
    "id": "ruleset_1",
    "enabled": true,
    "path": "rules.json"
  }]
},
"host_permissions": ["<all_urls>"]
```

### rules.json Example

```json
[
  {
    "id": 1,
    "priority": 1,
    "action": {
      "type": "block"
    },
    "condition": {
      "urlFilter": "||ads.example.com^",
      "resourceTypes": ["script", "image"]
    }
  },
  {
    "id": 2,
    "priority": 1,
    "action": {
      "type": "modifyHeaders",
      "requestHeaders": [
        {
          "header": "User-Agent",
          "operation": "set",
          "value": "CustomAgent/1.0"
        }
      ]
    },
    "condition": {
      "urlFilter": "||api.example.com/*",
      "resourceTypes": ["xmlhttprequest"]
    }
  },
  {
    "id": 3,
    "priority": 1,
    "action": {
      "type": "redirect",
      "redirect": {
        "url": "https://example.com/replaced.js"
      }
    },
    "condition": {
      "urlFilter": "||cdn.example.com/old.js",
      "resourceTypes": ["script"]
    }
  }
]
```

### Dynamic Rules

```javascript
// Add rules programmatically
chrome.declarativeNetRequest.updateDynamicRules({
  addRules: [
    {
      id: 1000,
      priority: 1,
      action: { type: 'block' },
      condition: {
        urlFilter: '||evil.com/*',
        resourceTypes: ['script'],
      },
    },
  ],
  removeRuleIds: [999],
})
```

## Storage

### Types

```javascript
// Local storage (10MB limit)
chrome.storage.local.set({ key: 'value' })
chrome.storage.local.get(['key'], result => {
  console.log(result.key)
})

// Sync storage (100KB, syncs across devices)
chrome.storage.sync.set({ settings: { theme: 'dark' } })

// Session storage (V3, lost when browser restarts)
chrome.storage.session.set({ tempData: 'value' })
```

### Best Practices

```javascript
// Use structured data
const settings = {
  theme: 'dark',
  notifications: true,
  apiKey: 'encrypted_key',
}
chrome.storage.local.set({ settings })

// Listen for changes
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (changes.settings) {
    console.log('Settings changed:', changes.settings.newValue)
  }
})

// Error handling
chrome.storage.local.set({ data }, () => {
  if (chrome.runtime.lastError) {
    console.error('Storage error:', chrome.runtime.lastError)
  }
})
```

## Common Pitfalls

### 1. Service Worker Lifecycle

❌ **Wrong:**

```javascript
let cache = null
chrome.runtime.onMessage.addListener(() => {
  if (!cache) {
    cache = loadData() // Lost when service worker restarts!
  }
})
```

✅ **Correct:**

```javascript
chrome.runtime.onMessage.addListener(async () => {
  const { cache } = await chrome.storage.session.get('cache')
  const data = cache || (await loadData())
  await chrome.storage.session.set({ cache: data })
})
```

### 2. CORS in Content Scripts

Content scripts inherit page's CORS policy. Use background script for API calls:

```javascript
// content.js
chrome.runtime.sendMessage({ action: 'fetchAPI', url })

// background.js
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'fetchAPI') {
    fetch(msg.url)
      .then(r => r.json())
      .then(sendResponse)
    return true
  }
})
```

### 3. CSP Violations

Inline scripts are blocked. Use event listeners:

❌ **Wrong:**

```html
<button onclick="doSomething()">Click</button>
```

✅ **Correct:**

```javascript
document.querySelector('button').addEventListener('click', doSomething)
```

## Migration from V2 to V3

| V2                               | V3                                            |
| -------------------------------- | --------------------------------------------- |
| `background.page`                | `background.service_worker`                   |
| `background.persistent: false`   | Service workers are non-persistent by default |
| `browser_action` / `page_action` | `action`                                      |
| `webRequest`                     | `declarativeNetRequest`                       |
| `chrome.tabs.executeScript`      | `chrome.scripting.executeScript`              |

## Testing & Debugging

### Load Unpacked Extension

1. Navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select extension directory

### Debugging

- **Service worker**: Click "Inspect views: service worker" on extensions page
- **Content scripts**: Use regular DevTools on the target page
- **Popup**: Right-click popup → "Inspect"

### Console Logs

```javascript
// Will appear in appropriate context
console.log('From content script') // Page DevTools
console.log('From background') // Service worker DevTools
console.log('From popup') // Popup DevTools
```
