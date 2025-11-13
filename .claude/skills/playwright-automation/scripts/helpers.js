/**
 * Playwright Automation Helper Functions
 *
 * Reusable utilities for common browser automation tasks.
 * Adds retry logic, better error handling, and convenience methods.
 */

const fs = require('fs')
const path = require('path')

/**
 * Safe click with retry logic and better error handling
 */
async function safeClick(page, selector, options = {}) {
  const { timeout = 10000, retries = 3, force = false } = options

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      // Wait for element to be visible and enabled
      await page.waitForSelector(selector, {
        state: 'visible',
        timeout: timeout / retries,
      })

      // Click the element
      await page.click(selector, { force, timeout: timeout / retries })

      return true
    } catch (error) {
      if (attempt === retries) {
        throw new Error(
          `Failed to click "${selector}" after ${retries} attempts: ${error.message}`
        )
      }
      console.log(`Click attempt ${attempt} failed, retrying...`)
      await page.waitForTimeout(500)
    }
  }
}

/**
 * Safe type with automatic clear and error handling
 */
async function safeType(page, selector, text, options = {}) {
  const { timeout = 10000, delay = 50, clear = true } = options

  try {
    // Wait for input to be visible
    await page.waitForSelector(selector, { state: 'visible', timeout })

    // Clear existing content if requested
    if (clear) {
      await page.fill(selector, '')
    }

    // Type the text with delay between keystrokes
    await page.type(selector, text, { delay })

    return true
  } catch (error) {
    throw new Error(`Failed to type into "${selector}": ${error.message}`)
  }
}

/**
 * Take screenshot with automatic naming and error handling
 */
async function takeScreenshot(page, name, options = {}) {
  const {
    path: customPath,
    fullPage = false,
    timeout = 5000,
    quality = 90,
  } = options

  try {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const filename = customPath || `/tmp/${name}-${timestamp}.png`

    // Ensure directory exists
    const dir = path.dirname(filename)
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true })
    }

    await page.screenshot({
      path: filename,
      fullPage,
      timeout,
      ...(filename.endsWith('.jpg') && { quality }),
    })

    console.log(`📸 Screenshot saved: ${filename}`)
    return filename
  } catch (error) {
    console.error(`Failed to take screenshot "${name}":`, error.message)
    throw error
  }
}

/**
 * Handle common cookie consent banners
 */
async function handleCookieBanner(page, options = {}) {
  const { timeout = 3000 } = options

  const commonSelectors = [
    'button:has-text("Accept")',
    'button:has-text("Accept all")',
    'button:has-text("I agree")',
    'button:has-text("OK")',
    'button:has-text("Got it")',
    '[id*="cookie"] button',
    '[class*="cookie"] button',
    '[data-testid*="cookie"] button',
  ]

  for (const selector of commonSelectors) {
    try {
      const button = await page.$(selector)
      if (button) {
        await button.click({ timeout })
        console.log('🍪 Cookie banner dismissed')
        return true
      }
    } catch (error) {
      // Continue to next selector
    }
  }

  return false
}

/**
 * Extract data from HTML table
 */
async function extractTableData(page, tableSelector) {
  try {
    const data = await page.evaluate(selector => {
      const table = document.querySelector(selector)
      if (!table) return null

      const headers = Array.from(table.querySelectorAll('thead th')).map(th =>
        th.textContent.trim()
      )

      const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr =>
        Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim())
      )

      return rows.map(row =>
        headers.reduce((obj, header, index) => {
          obj[header] = row[index]
          return obj
        }, {})
      )
    }, tableSelector)

    return data
  } catch (error) {
    throw new Error(
      `Failed to extract table data from "${tableSelector}": ${error.message}`
    )
  }
}

/**
 * Wait for network to be idle
 */
async function waitForNetworkIdle(page, timeout = 2000) {
  try {
    await page.waitForLoadState('networkidle', { timeout })
    return true
  } catch (error) {
    console.warn('Network idle timeout reached, continuing...')
    return false
  }
}

/**
 * Fill form with multiple fields
 */
async function fillForm(page, formData, options = {}) {
  const { submitButton, waitForNavigation = true } = options

  for (const [field, value] of Object.entries(formData)) {
    const selector = `input[name="${field}"], textarea[name="${field}"], select[name="${field}"]`
    await safeType(page, selector, value.toString())
  }

  if (submitButton) {
    if (waitForNavigation) {
      await Promise.all([
        page.waitForNavigation(),
        safeClick(page, submitButton),
      ])
    } else {
      await safeClick(page, submitButton)
    }
  }
}

/**
 * Get text content from element
 */
async function getText(page, selector, options = {}) {
  const { timeout = 5000 } = options

  try {
    await page.waitForSelector(selector, { state: 'visible', timeout })
    return await page.textContent(selector)
  } catch (error) {
    throw new Error(`Failed to get text from "${selector}": ${error.message}`)
  }
}

/**
 * Check if element exists
 */
async function elementExists(page, selector, options = {}) {
  const { timeout = 1000 } = options

  try {
    await page.waitForSelector(selector, { timeout })
    return true
  } catch (error) {
    return false
  }
}

/**
 * Scroll to element
 */
async function scrollToElement(page, selector, options = {}) {
  const { behavior = 'smooth', block = 'center' } = options

  try {
    await page.evaluate(
      ({ selector, behavior, block }) => {
        const element = document.querySelector(selector)
        if (element) {
          element.scrollIntoView({ behavior, block })
        }
      },
      { selector, behavior, block }
    )

    await page.waitForTimeout(300)
    return true
  } catch (error) {
    throw new Error(`Failed to scroll to "${selector}": ${error.message}`)
  }
}

/**
 * Wait for text to appear on page
 */
async function waitForText(page, text, options = {}) {
  const { timeout = 10000 } = options

  try {
    await page.waitForSelector(`text=${text}`, { timeout })
    return true
  } catch (error) {
    throw new Error(`Text "${text}" did not appear within ${timeout}ms`)
  }
}

/**
 * Capture console logs
 */
function captureConsoleLogs(page, options = {}) {
  const { filter = null } = options
  const logs = []

  page.on('console', msg => {
    const log = {
      type: msg.type(),
      text: msg.text(),
      timestamp: new Date().toISOString(),
    }

    if (!filter || msg.type() === filter) {
      logs.push(log)
      console.log(`[${log.type.toUpperCase()}] ${log.text}`)
    }
  })

  return logs
}

/**
 * Monitor network requests
 */
function monitorNetwork(page, options = {}) {
  const { filter = null } = options
  const requests = []

  page.on('request', request => {
    const req = {
      url: request.url(),
      method: request.method(),
      timestamp: new Date().toISOString(),
    }

    if (!filter || request.url().includes(filter)) {
      requests.push(req)
    }
  })

  page.on('response', async response => {
    const req = requests.find(r => r.url === response.url())
    if (req) {
      req.status = response.status()
      req.statusText = response.statusText()
      console.log(`[${req.method}] ${req.url} - ${req.status}`)
    }
  })

  return requests
}

module.exports = {
  safeClick,
  safeType,
  takeScreenshot,
  handleCookieBanner,
  extractTableData,
  waitForNetworkIdle,
  fillForm,
  getText,
  elementExists,
  scrollToElement,
  waitForText,
  captureConsoleLogs,
  monitorNetwork,
}
