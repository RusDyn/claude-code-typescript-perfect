# SPA Handling Guide

Strategies for working with Single Page Applications (React, Vue, Angular, Next.js, etc.)

## Challenge with SPAs

SPAs dynamically update the DOM without full page reloads, which means:

- Content scripts run once but page content changes
- Elements you select may disappear and reappear
- Navigation doesn't trigger new content script injection
- Standard `DOMContentLoaded` events don't fire on route changes

## Detection Strategies

### Detect Framework

```javascript
function detectFramework() {
  const frameworks = [];

  // React
  if (
    window.React ||
    window._react ||
    document.querySelector("[data-reactroot], [data-reactid]") ||
    document.querySelector("#root, #__next, #app")
  ) {
    frameworks.push("React");
  }

  // Vue
  if (
    window.Vue ||
    window.__VUE__ ||
    document.querySelector("[data-v-], [data-vue-]")
  ) {
    frameworks.push("Vue");
  }

  // Angular
  if (
    window.angular ||
    window.ng ||
    document.querySelector("[ng-app], [ng-version]")
  ) {
    frameworks.push("Angular");
  }

  // Next.js
  if (window.__NEXT_DATA__ || document.querySelector("#__next")) {
    frameworks.push("Next.js");
  }

  // Svelte
  if (document.querySelector('[class*="svelte-"]')) {
    frameworks.push("Svelte");
  }

  return frameworks;
}
```

## Universal SPA Handler

Works with any framework:

```javascript
class SPAHandler {
  constructor(options = {}) {
    this.lastUrl = location.href;
    this.observer = null;
    this.onNavigate = options.onNavigate || (() => {});
    this.debounceDelay = options.debounceDelay || 100;
    this.init();
  }

  init() {
    // Method 1: Monitor URL changes via History API
    this.interceptHistory();

    // Method 2: Observe DOM mutations
    this.observeDOM();

    // Method 3: Listen to native navigation events
    this.listenToEvents();
  }

  interceptHistory() {
    const originalPushState = history.pushState;
    const originalReplaceState = history.replaceState;

    history.pushState = (...args) => {
      originalPushState.apply(history, args);
      this.handleNavigation("pushState");
    };

    history.replaceState = (...args) => {
      originalReplaceState.apply(history, args);
      this.handleNavigation("replaceState");
    };
  }

  observeDOM() {
    // Watch for significant DOM changes
    this.observer = new MutationObserver(
      this.debounce(() => {
        if (location.href !== this.lastUrl) {
          this.handleNavigation("mutation");
        }
      }, this.debounceDelay),
    );

    this.observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  listenToEvents() {
    // Browser back/forward
    window.addEventListener("popstate", () => {
      this.handleNavigation("popstate");
    });

    // Hash changes
    window.addEventListener("hashchange", () => {
      this.handleNavigation("hashchange");
    });
  }

  handleNavigation(method) {
    const newUrl = location.href;

    if (newUrl !== this.lastUrl) {
      console.log(`Navigation detected via ${method}: ${newUrl}`);
      this.lastUrl = newUrl;

      // Small delay to let DOM settle
      setTimeout(() => {
        this.onNavigate({
          url: newUrl,
          method: method,
        });
      }, 50);
    }
  }

  debounce(func, wait) {
    let timeout;
    return function (...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  destroy() {
    if (this.observer) {
      this.observer.disconnect();
    }
  }
}

// Usage
const spaHandler = new SPAHandler({
  onNavigate: ({ url, method }) => {
    console.log("Page navigated to:", url);

    // Reinject your features
    setTimeout(() => {
      injectFeatures();
    }, 100);
  },
});
```

## React-Specific Patterns

### Waiting for React Components

```javascript
async function waitForReactComponent(selector, timeout = 10000) {
  const startTime = Date.now();

  while (Date.now() - startTime < timeout) {
    const element = document.querySelector(selector);

    if (element) {
      // Check if React has rendered
      const reactKey = Object.keys(element).find(
        (key) =>
          key.startsWith("__reactInternalInstance") ||
          key.startsWith("__reactFiber"),
      );

      if (reactKey) {
        return element;
      }
    }

    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  throw new Error(`React component ${selector} not found`);
}

// Usage
waitForReactComponent(".profile-card").then((card) => {
  injectIntoCard(card);
});
```

### React Component Detection

```javascript
function isReactComponent(element) {
  return Object.keys(element).some(
    (key) =>
      key.startsWith("__reactInternalInstance") ||
      key.startsWith("__reactFiber"),
  );
}

function getReactInstance(element) {
  const key = Object.keys(element).find(
    (key) =>
      key.startsWith("__reactInternalInstance") ||
      key.startsWith("__reactFiber"),
  );

  return element[key];
}
```

## Vue-Specific Patterns

### Wait for Vue Mount

```javascript
function waitForVueMount(selector, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const check = () => {
      const element = document.querySelector(selector);

      if (element && element.__vue__) {
        resolve(element);
      } else if (Date.now() - startTime > timeout) {
        reject(new Error("Vue component not mounted"));
      } else {
        setTimeout(check, 100);
      }
    };

    const startTime = Date.now();
    check();
  });
}
```

### Vue Router Detection

```javascript
function detectVueRouter() {
  return (
    window.$router ||
    window.__VUE_ROUTER__ ||
    document.querySelector("[data-v-router]")
  );
}

// Listen to Vue Router navigation
if (window.$router) {
  window.$router.afterEach((to, from) => {
    console.log("Vue router navigated:", to.path);
    injectFeatures();
  });
}
```

## Angular-Specific Patterns

### Wait for Angular Bootstrap

```javascript
function waitForAngularReady(timeout = 10000) {
  return new Promise((resolve, reject) => {
    if (window.getAllAngularRootElements) {
      const rootElements = window.getAllAngularRootElements();
      if (rootElements.length > 0) {
        resolve(rootElements);
        return;
      }
    }

    const observer = new MutationObserver(() => {
      if (window.getAllAngularRootElements) {
        const roots = window.getAllAngularRootElements();
        if (roots.length > 0) {
          observer.disconnect();
          resolve(roots);
        }
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });

    setTimeout(() => {
      observer.disconnect();
      reject(new Error("Angular not bootstrapped"));
    }, timeout);
  });
}
```

### Angular Router Events

```javascript
// Inject into page context to access Angular
const angularScript = `
  (function() {
    if (window.ng && window.ng.probe) {
      const appRef = window.ng.probe(document.body).injector.get(window.ng.coreTokens.ApplicationRef);
      const router = window.ng.probe(document.body).injector.get(window.ng.router.Router);
      
      router.events.subscribe(event => {
        if (event.constructor.name === 'NavigationEnd') {
          window.postMessage({
            type: 'ANGULAR_NAVIGATION',
            url: event.url
          }, '*');
        }
      });
    }
  })();
`;

const script = document.createElement("script");
script.textContent = angularScript;
document.documentElement.appendChild(script);
script.remove();

// Listen in content script
window.addEventListener("message", (event) => {
  if (event.data.type === "ANGULAR_NAVIGATION") {
    console.log("Angular navigated:", event.data.url);
    injectFeatures();
  }
});
```

## Next.js Specific

### Detect Next.js Router

```javascript
function detectNextRouter() {
  return window.next || window.__NEXT_DATA__;
}

// Listen to Next.js router
if (window.next?.router) {
  window.next.router.events.on("routeChangeComplete", (url) => {
    console.log("Next.js route changed:", url);
    injectFeatures();
  });
}
```

## Complete SPA-Ready Content Script Template

```javascript
(function () {
  "use strict";

  // Prevent multiple initializations
  if (window.__MY_EXTENSION_LOADED__) {
    console.log("Extension already loaded");
    return;
  }
  window.__MY_EXTENSION_LOADED__ = true;

  // Detect framework
  const frameworks = detectFramework();
  console.log("Detected frameworks:", frameworks);

  // Initialize SPA handler
  const spaHandler = new SPAHandler({
    onNavigate: handleNavigation,
  });

  // Initial injection
  init();

  function init() {
    console.log("Initializing extension...");
    injectFeatures();
  }

  function handleNavigation({ url, method }) {
    console.log(`Navigated to ${url} via ${method}`);

    // Wait for new content to render
    setTimeout(() => {
      injectFeatures();
    }, 200);
  }

  async function injectFeatures() {
    try {
      // Clear old injections (if needed)
      clearPreviousInjections();

      // Wait for key elements
      const targetElement = await waitForElement(".target-selector", 5000);

      if (targetElement) {
        // Inject your functionality
        injectButton(targetElement);
        console.log("Features injected successfully");
      }
    } catch (error) {
      console.error("Injection failed:", error);
    }
  }

  function clearPreviousInjections() {
    // Remove previously injected elements
    document.querySelectorAll(".my-extension-injected").forEach((el) => {
      el.remove();
    });
  }

  function injectButton(target) {
    // Check if already injected
    if (target.querySelector(".my-extension-button")) {
      return;
    }

    const button = document.createElement("button");
    button.className = "my-extension-button my-extension-injected";
    button.textContent = "Extension Feature";
    button.addEventListener("click", handleButtonClick);

    target.appendChild(button);
  }

  function handleButtonClick(e) {
    e.preventDefault();
    e.stopPropagation();

    // Your button logic
    console.log("Button clicked");
  }

  // Cleanup on extension reload
  if (window.performance && performance.navigation.type === 1) {
    console.log("Page reloaded, reinitializing...");
  }
})();
```

## Debugging SPAs

### Check for Dynamic Content Issues

```javascript
// Log all DOM mutations for debugging
const debugObserver = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.addedNodes.length) {
      console.log("Nodes added:", mutation.addedNodes);
    }
    if (mutation.removedNodes.length) {
      console.log("Nodes removed:", mutation.removedNodes);
    }
  });
});

debugObserver.observe(document.body, {
  childList: true,
  subtree: true,
  attributes: true,
});

// Stop after 10 seconds
setTimeout(() => debugObserver.disconnect(), 10000);
```

### Monitor Route Changes

```javascript
// Log all URL changes
let lastUrl = location.href;
new MutationObserver(() => {
  const currentUrl = location.href;
  if (currentUrl !== lastUrl) {
    console.log("URL changed from:", lastUrl, "to:", currentUrl);
    lastUrl = currentUrl;
  }
}).observe(document, { subtree: true, childList: true });
```

## Performance Considerations

1. **Debounce injections** - Don't inject on every mutation
2. **Use requestIdleCallback** - Inject during browser idle time
3. **Batch DOM operations** - Minimize reflows
4. **Clean up observers** - Disconnect when not needed

```javascript
function efficientInject() {
  requestIdleCallback(
    () => {
      // Batch all DOM operations
      const fragment = document.createDocumentFragment();

      // Add all elements to fragment
      fragment.appendChild(createButton1());
      fragment.appendChild(createButton2());

      // Single DOM insertion
      document.querySelector(".target").appendChild(fragment);
    },
    { timeout: 2000 },
  );
}
```

This guide provides comprehensive strategies for handling SPAs in Chrome extensions.
