// Popup JavaScript
// Runs in the extension popup context

document.addEventListener('DOMContentLoaded', async () => {
  console.log('Popup loaded')

  // Get DOM elements
  const enabledCheckbox = document.getElementById('enabledCheckbox')
  const actionButton = document.getElementById('actionButton')
  const currentUrlDiv = document.getElementById('currentUrl')
  const statusDiv = document.getElementById('status')

  // Load current settings
  const { settings } = await chrome.storage.local.get('settings')
  if (settings) {
    enabledCheckbox.checked = settings.enabled !== false
  }

  // Get current tab info
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
  if (tab) {
    currentUrlDiv.textContent = tab.url
  }

  // Handle checkbox changes
  enabledCheckbox.addEventListener('change', async e => {
    const enabled = e.target.checked

    // Save to storage
    await chrome.storage.local.set({
      settings: { ...settings, enabled },
    })

    showStatus('Settings saved!', 'success')

    // Notify content script if needed
    if (tab) {
      chrome.tabs
        .sendMessage(tab.id, {
          action: 'settingsChanged',
          enabled: enabled,
        })
        .catch(() => {
          // Content script might not be loaded yet
        })
    }
  })

  // Handle action button click
  actionButton.addEventListener('click', async () => {
    try {
      // Send message to background script
      const response = await chrome.runtime.sendMessage({
        action: 'performAction',
        tabId: tab.id,
      })

      if (response?.success) {
        showStatus('Action completed successfully!', 'success')
      } else {
        showStatus(
          'Action failed: ' + (response?.error || 'Unknown error'),
          'error'
        )
      }
    } catch (error) {
      console.error('Error:', error)
      showStatus('Error: ' + error.message, 'error')
    }
  })

  // Utility: Show status message
  function showStatus(message, type = 'success') {
    statusDiv.textContent = message
    statusDiv.className = `status ${type}`
    statusDiv.style.display = 'block'

    // Hide after 3 seconds
    setTimeout(() => {
      statusDiv.style.display = 'none'
    }, 3000)
  }

  // Listen for storage changes
  chrome.storage.onChanged.addListener((changes, areaName) => {
    if (areaName === 'local' && changes.settings) {
      console.log('Settings changed:', changes.settings.newValue)
      enabledCheckbox.checked = changes.settings.newValue.enabled !== false
    }
  })
})
