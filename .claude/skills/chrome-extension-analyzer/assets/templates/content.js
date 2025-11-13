// Content Script - Runs in the context of web pages
// Has access to the DOM but isolated from page JavaScript

(function() {
  'use strict';
  
  // Prevent multiple initializations
  if (window.__MY_EXTENSION_LOADED__) {
    console.log('[Extension] Already loaded, skipping initialization');
    return;
  }
  window.__MY_EXTENSION_LOADED__ = true;
  
  console.log('[Extension] Initializing...');
  
  // Configuration
  const CONFIG = {
    selectors: {
      // Add your selectors here
      targetElement: '.target-class',
      button: '#button-id'
    },
    debug: true
  };
  
  // Utility: Wait for element with timeout
  function waitForElement(selector, timeout = 10000) {
    return new Promise((resolve, reject) => {
      const element = document.querySelector(selector);
      if (element) {
        resolve(element);
        return;
      }
      
      const observer = new MutationObserver(() => {
        const element = document.querySelector(selector);
        if (element) {
          observer.disconnect();
          resolve(element);
        }
      });
      
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
      
      setTimeout(() => {
        observer.disconnect();
        reject(new Error(`Element ${selector} not found within ${timeout}ms`));
      }, timeout);
    });
  }
  
  // Utility: Find element with fallback selectors
  function findElementWithFallback(selectors) {
    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) {
        if (CONFIG.debug) console.log('[Extension] Found element with:', selector);
        return element;
      }
    }
    return null;
  }
  
  // SPA Handler
  class SPAHandler {
    constructor(onNavigate) {
      this.lastUrl = location.href;
      this.onNavigate = onNavigate;
      this.init();
    }
    
    init() {
      // Intercept history API
      const originalPushState = history.pushState;
      const originalReplaceState = history.replaceState;
      
      history.pushState = (...args) => {
        originalPushState.apply(history, args);
        this.checkNavigation();
      };
      
      history.replaceState = (...args) => {
        originalReplaceState.apply(history, args);
        this.checkNavigation();
      };
      
      // Listen to popstate
      window.addEventListener('popstate', () => this.checkNavigation());
      
      // Observe DOM changes
      const observer = new MutationObserver(
        this.debounce(() => this.checkNavigation(), 100)
      );
      
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
    }
    
    checkNavigation() {
      if (location.href !== this.lastUrl) {
        this.lastUrl = location.href;
        setTimeout(() => this.onNavigate(location.href), 50);
      }
    }
    
    debounce(func, wait) {
      let timeout;
      return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
      };
    }
  }
  
  // Initialize SPA handler
  const spaHandler = new SPAHandler((url) => {
    if (CONFIG.debug) console.log('[Extension] Navigation detected:', url);
    setTimeout(() => injectFeatures(), 200);
  });
  
  // Main injection function
  async function injectFeatures() {
    try {
      if (CONFIG.debug) console.log('[Extension] Injecting features...');
      
      // Wait for target element
      const targetElement = await waitForElement(CONFIG.selectors.targetElement, 5000);
      
      if (!targetElement) {
        console.warn('[Extension] Target element not found');
        return;
      }
      
      // Check if already injected
      if (targetElement.querySelector('.my-extension-injected')) {
        if (CONFIG.debug) console.log('[Extension] Already injected, skipping');
        return;
      }
      
      // Inject your features here
      injectButton(targetElement);
      
      if (CONFIG.debug) console.log('[Extension] Features injected successfully');
    } catch (error) {
      console.error('[Extension] Injection failed:', error);
    }
  }
  
  // Example: Inject a button
  function injectButton(targetElement) {
    const button = document.createElement('button');
    button.className = 'my-extension-injected';
    button.textContent = 'Extension Button';
    button.style.cssText = `
      padding: 10px 20px;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 4px;
      margin: 10px;
      cursor: pointer;
      font-weight: bold;
    `;
    
    button.addEventListener('click', handleButtonClick);
    targetElement.appendChild(button);
  }
  
  // Button click handler
  function handleButtonClick(e) {
    e.preventDefault();
    e.stopPropagation();
    
    if (CONFIG.debug) console.log('[Extension] Button clicked');
    
    // Send message to background script
    chrome.runtime.sendMessage({
      action: 'buttonClicked',
      url: window.location.href
    }, (response) => {
      if (response?.success) {
        console.log('[Extension] Background responded:', response);
      }
    });
  }
  
  // Listen for messages from background script
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (CONFIG.debug) console.log('[Extension] Received message:', message);
    
    switch (message.action) {
      case 'pageLoaded':
        injectFeatures();
        sendResponse({ success: true });
        break;
        
      case 'getData':
        // Handle data request
        sendResponse({ success: true, data: extractPageData() });
        break;
        
      default:
        sendResponse({ success: false, error: 'Unknown action' });
    }
  });
  
  // Example: Extract data from page
  function extractPageData() {
    return {
      url: window.location.href,
      title: document.title,
      // Add more data extraction as needed
    };
  }
  
  // Initial injection
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectFeatures);
  } else {
    injectFeatures();
  }
  
  console.log('[Extension] Content script loaded');
})();
