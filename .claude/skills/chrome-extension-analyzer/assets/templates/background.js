// Background Service Worker (Manifest V3)
// Handles background tasks, message passing, and storage

// Installation handler
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Extension installed');
    
    // Initialize default settings
    chrome.storage.local.set({
      settings: {
        enabled: true,
        // Add your default settings
      }
    });
  } else if (details.reason === 'update') {
    console.log('Extension updated to version:', chrome.runtime.getManifest().version);
  }
});

// Message handler from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Received message:', message, 'from:', sender.tab?.id);
  
  // Handle different message types
  switch (message.action) {
    case 'getData':
      handleGetData(message, sendResponse);
      return true; // Keep channel open for async response
      
    case 'saveData':
      handleSaveData(message, sendResponse);
      return true;
      
    case 'fetchAPI':
      handleAPIFetch(message, sendResponse);
      return true;
      
    default:
      console.warn('Unknown message action:', message.action);
      sendResponse({ error: 'Unknown action' });
  }
});

// Example: Fetch data from API (bypasses CORS)
async function handleAPIFetch(message, sendResponse) {
  try {
    const response = await fetch(message.url, {
      method: message.method || 'GET',
      headers: message.headers || {},
      body: message.body ? JSON.stringify(message.body) : undefined
    });
    
    const data = await response.json();
    sendResponse({ success: true, data });
  } catch (error) {
    console.error('API fetch error:', error);
    sendResponse({ success: false, error: error.message });
  }
}

// Example: Get data from storage
async function handleGetData(message, sendResponse) {
  try {
    const result = await chrome.storage.local.get(message.key);
    sendResponse({ success: true, data: result[message.key] });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

// Example: Save data to storage
async function handleSaveData(message, sendResponse) {
  try {
    await chrome.storage.local.set({ [message.key]: message.value });
    sendResponse({ success: true });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

// Tab update listener (detect page loads)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    console.log('Page loaded:', tab.url);
    
    // You can inject scripts or send messages to content script here
    // chrome.tabs.sendMessage(tabId, { action: 'pageLoaded' });
  }
});

// Storage change listener
chrome.storage.onChanged.addListener((changes, areaName) => {
  console.log('Storage changed in', areaName);
  
  for (let [key, { oldValue, newValue }] of Object.entries(changes)) {
    console.log(`${key}: ${oldValue} -> ${newValue}`);
  }
});

// Context menu (right-click menu)
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'myExtensionAction',
    title: 'My Extension Action',
    contexts: ['selection', 'page']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'myExtensionAction') {
    console.log('Context menu clicked:', info.selectionText);
    
    // Send message to content script
    chrome.tabs.sendMessage(tab.id, {
      action: 'contextMenuClick',
      text: info.selectionText
    });
  }
});

// Alarm for periodic tasks
chrome.alarms.create('periodicTask', {
  periodInMinutes: 60
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'periodicTask') {
    console.log('Running periodic task');
    // Your periodic task here
  }
});

console.log('Background service worker loaded');
