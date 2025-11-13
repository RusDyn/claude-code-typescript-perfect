# Content Script Patterns

Common patterns for injecting functionality into web pages.

## Pattern 1: Safe Element Selection with Retries

Handle dynamic content that loads after page load:

```javascript
function waitForElement(selector, timeout = 10000) {
  return new Promise((resolve, reject) => {
    // Check if element exists immediately
    const element = document.querySelector(selector);
    if (element) {
      resolve(element);
      return;
    }

    // Set up observer for dynamic content
    const observer = new MutationObserver((mutations) => {
      const element = document.querySelector(selector);
      if (element) {
        observer.disconnect();
        resolve(element);
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });

    // Timeout fallback
    setTimeout(() => {
      observer.disconnect();
      reject(new Error(`Element ${selector} not found within ${timeout}ms`));
    }, timeout);
  });
}

// Usage
waitForElement(".buy-button")
  .then((button) => {
    // Inject your functionality
    injectScoreButton(button);
  })
  .catch((err) => console.error(err));
```

## Pattern 2: Robust Selector Fallback Chain

Try multiple selectors with fallback:

```javascript
function findElementWithFallback(selectors) {
  for (const selector of selectors) {
    const element = document.querySelector(selector);
    if (element) {
      console.log(`Found element with: ${selector}`);
      return element;
    }
  }
  console.warn("Element not found with any selector");
  return null;
}

// Usage with priority-ordered selectors
const button = findElementWithFallback([
  '[data-action="buy"]', // Most stable
  "#buy-button-123", // Specific ID
  "button.primary-action", // Class-based
  'button[type="submit"]', // Generic fallback
]);
```

## Pattern 3: SPA Detection and Handling

Detect Single Page Apps and reinject on route changes:

```javascript
// Detect SPA frameworks
function detectSPA() {
  const indicators = {
    react: window.React || document.querySelector("[data-reactroot]"),
    vue: window.Vue || document.querySelector("[data-v-]"),
    angular: window.angular || document.querySelector("[ng-app]"),
    nextjs: window.next || document.querySelector("#__next"),
  };

  for (const [framework, detected] of Object.entries(indicators)) {
    if (detected) {
      console.log(`Detected ${framework} SPA`);
      return framework;
    }
  }
  return null;
}

// Handle SPA navigation
let lastUrl = location.href;
const observer = new MutationObserver(() => {
  if (location.href !== lastUrl) {
    lastUrl = location.href;
    console.log("Route changed:", lastUrl);

    // Reinject functionality after navigation
    setTimeout(() => {
      injectFeatures();
    }, 100); // Small delay for DOM to settle
  }
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});

// Also listen to history API
const originalPushState = history.pushState;
const originalReplaceState = history.replaceState;

history.pushState = function (...args) {
  originalPushState.apply(this, args);
  window.dispatchEvent(new Event("pushstate"));
  injectFeatures();
};

history.replaceState = function (...args) {
  originalReplaceState.apply(this, args);
  window.dispatchEvent(new Event("replacestate"));
  injectFeatures();
};

window.addEventListener("popstate", () => {
  injectFeatures();
});
```

## Pattern 4: Injecting UI Elements

Add custom buttons and UI elements safely:

```javascript
function injectButton(targetElement, position = "after") {
  // Create button
  const button = document.createElement("button");
  button.textContent = "My Feature";
  button.className = "my-extension-button";
  button.style.cssText = `
    padding: 8px 16px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-left: 8px;
  `;

  // Add click handler
  button.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    handleButtonClick();
  });

  // Insert relative to target
  if (position === "after") {
    targetElement.insertAdjacentElement("afterend", button);
  } else if (position === "before") {
    targetElement.insertAdjacentElement("beforebegin", button);
  } else if (position === "inside") {
    targetElement.appendChild(button);
  }

  return button;
}

// Usage
waitForElement(".product-actions").then((actionsBar) => {
  injectButton(actionsBar, "inside");
});
```

## Pattern 5: Overlay/Modal Injection

Create overlays that don't conflict with page styles:

```javascript
function createOverlay() {
  // Use shadow DOM to isolate styles
  const container = document.createElement("div");
  container.id = "my-extension-overlay";
  document.body.appendChild(container);

  const shadow = container.attachShadow({ mode: "open" });

  // Inject styles into shadow DOM
  const style = document.createElement("style");
  style.textContent = `
    .overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.7);
      z-index: 999999;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .modal {
      background: white;
      padding: 24px;
      border-radius: 8px;
      max-width: 500px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .close-btn {
      float: right;
      cursor: pointer;
      font-size: 24px;
      line-height: 1;
    }
  `;

  shadow.appendChild(style);

  // Create modal content
  const overlay = document.createElement("div");
  overlay.className = "overlay";
  overlay.innerHTML = `
    <div class="modal">
      <span class="close-btn">&times;</span>
      <h2>My Extension</h2>
      <div class="content">
        <!-- Your content here -->
      </div>
    </div>
  `;

  shadow.appendChild(overlay);

  // Close handler
  shadow.querySelector(".close-btn").addEventListener("click", () => {
    container.remove();
  });

  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
      container.remove();
    }
  });

  return { container, shadow };
}
```

## Pattern 6: Data Extraction

Extract structured data from pages:

```javascript
function extractProductData() {
  const data = {};

  // Try multiple selector strategies
  data.title = (
    document.querySelector("[data-product-title]")?.textContent ||
    document.querySelector("h1.product-title")?.textContent ||
    document.querySelector("#product-name")?.textContent ||
    "Unknown"
  ).trim();

  data.price = (
    document.querySelector("[data-price]")?.textContent ||
    document.querySelector(".price-current")?.textContent ||
    document.querySelector(".product-price")?.textContent ||
    "N/A"
  ).trim();

  data.rating = parseFloat(
    document.querySelector("[data-rating]")?.getAttribute("data-rating") ||
      document.querySelector(".star-rating")?.textContent ||
      "0",
  );

  data.images = Array.from(document.querySelectorAll(".product-image img")).map(
    (img) => img.src,
  );

  data.url = window.location.href;
  data.timestamp = new Date().toISOString();

  return data;
}

// Send to background script
chrome.runtime.sendMessage({
  action: "productDataExtracted",
  data: extractProductData(),
});
```

## Pattern 7: API Interception (Page Context)

Intercept fetch/XHR from page's context:

```javascript
// This must run in page context, not content script
const interceptScript = `
  (function() {
    const originalFetch = window.fetch;
    
    window.fetch = function(...args) {
      const [url, options] = args;
      
      console.log('Intercepted fetch:', url);
      
      // Modify request if needed
      if (url.includes('/api/')) {
        const newOptions = {
          ...options,
          headers: {
            ...options?.headers,
            'X-Custom-Header': 'MyValue'
          }
        };
        args[1] = newOptions;
      }
      
      // Call original and intercept response
      return originalFetch(...args).then(response => {
        // Clone response to read it
        const clonedResponse = response.clone();
        
        clonedResponse.json().then(data => {
          console.log('Response data:', data);
          // Send to content script
          window.postMessage({
            type: 'API_RESPONSE',
            url: url,
            data: data
          }, '*');
        });
        
        return response;
      });
    };
    
    // XHR interception
    const originalOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url, ...rest) {
      this._url = url;
      return originalOpen.call(this, method, url, ...rest);
    };
    
    const originalSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function(...args) {
      this.addEventListener('load', function() {
        console.log('XHR completed:', this._url, this.responseText);
      });
      return originalSend.apply(this, args);
    };
  })();
`;

// Inject into page
const script = document.createElement("script");
script.textContent = interceptScript;
(document.head || document.documentElement).appendChild(script);
script.remove();

// Listen for messages from page
window.addEventListener("message", (event) => {
  if (event.data.type === "API_RESPONSE") {
    // Handle intercepted API response
    console.log("Received API data:", event.data);

    // Send to background script if needed
    chrome.runtime.sendMessage({
      action: "apiIntercepted",
      data: event.data,
    });
  }
});
```

## Pattern 8: Persistent State Across Reloads

Handle state when content script reloads:

```javascript
// Check if already initialized
if (window.myExtensionInitialized) {
  console.log("Extension already initialized, skipping...");
} else {
  window.myExtensionInitialized = true;

  // Initialize extension
  initializeExtension();
}

// Store state in chrome.storage
async function saveState(state) {
  await chrome.storage.local.set({ pageState: state });
}

async function loadState() {
  const { pageState } = await chrome.storage.local.get("pageState");
  return pageState || {};
}

// Restore state on reload
loadState().then((state) => {
  if (state.lastAction) {
    console.log("Resuming from:", state.lastAction);
  }
});
```

## Pattern 9: Error Handling and Logging

Robust error handling for production:

```javascript
function safeInject(fn, context = "unknown") {
  try {
    fn();
  } catch (error) {
    console.error(`[Extension] Error in ${context}:`, error);

    // Report to background script
    chrome.runtime.sendMessage({
      action: "logError",
      error: {
        message: error.message,
        stack: error.stack,
        context: context,
        url: window.location.href,
      },
    });
  }
}

// Usage
safeInject(() => {
  injectButton(document.querySelector(".actions"));
}, "button-injection");
```

## Pattern 10: Performance Optimization

Debounce and throttle expensive operations:

```javascript
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

function throttle(func, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Usage for scroll events
const handleScroll = throttle(() => {
  // Check if new elements appeared
  checkForNewElements();
}, 200);

window.addEventListener("scroll", handleScroll);

// Usage for input events
const handleInput = debounce((value) => {
  // Search or validate
  performSearch(value);
}, 300);

document.querySelector("input").addEventListener("input", (e) => {
  handleInput(e.target.value);
});
```

## Complete Example: Marketplace Score Injector

```javascript
// content.js for Amazon/marketplace score injection
(async function () {
  "use strict";

  // Configuration
  const SELECTORS = {
    buyButton: [
      "#buy-now-button",
      '[data-action="buy-now"]',
      'button[name="submit.buy-now"]',
      ".buy-button",
    ],
    productId: ["[data-asin]", "[data-product-id]"],
  };

  // Find buy button with fallback
  const buyButton = await waitForElement(SELECTORS.buyButton[0]).catch(() =>
    findElementWithFallback(SELECTORS.buyButton),
  );

  if (!buyButton) {
    console.log("Buy button not found");
    return;
  }

  // Extract product ID
  const productIdElement = findElementWithFallback(SELECTORS.productId);
  const productId =
    productIdElement?.dataset.asin ||
    productIdElement?.dataset.productId ||
    extractProductIdFromUrl();

  // Fetch score from background
  chrome.runtime.sendMessage(
    {
      action: "getProductScore",
      productId: productId,
      url: window.location.href,
    },
    (response) => {
      if (response?.score) {
        injectScoreButton(buyButton, response.score);
      }
    },
  );

  function injectScoreButton(targetButton, score) {
    const scoreButton = document.createElement("button");
    scoreButton.className = "score-indicator";
    scoreButton.textContent = `Score: ${score}/100`;
    scoreButton.style.cssText = `
      padding: 10px 20px;
      background: ${score >= 70 ? "#4CAF50" : score >= 40 ? "#FF9800" : "#F44336"};
      color: white;
      border: none;
      border-radius: 4px;
      margin-left: 12px;
      cursor: pointer;
      font-weight: bold;
    `;

    scoreButton.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      showScoreDetails(score);
    });

    targetButton.insertAdjacentElement("afterend", scoreButton);
  }

  function extractProductIdFromUrl() {
    const match = window.location.pathname.match(/\/dp\/([A-Z0-9]{10})/);
    return match ? match[1] : null;
  }

  function showScoreDetails(score) {
    // Show modal with detailed scoring
    createOverlay();
  }
})();
```

This pattern library covers the most common scenarios for Chrome extension content scripts.
