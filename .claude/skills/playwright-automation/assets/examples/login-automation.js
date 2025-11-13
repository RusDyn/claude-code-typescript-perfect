/**
 * Example: Login Flow Automation
 *
 * Demonstrates automated login testing with error handling and screenshots.
 * Save to /tmp and run with: node /tmp/login-automation.js
 */

const { chromium } = require('playwright')
const {
  safeClick,
  safeType,
  takeScreenshot,
  waitForText,
} = require('../../scripts/helpers.js')

const TARGET_URL = 'http://localhost:3000'

;(async () => {
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100, // Makes actions visible
  })

  const page = await browser.newPage()

  try {
    console.log('🚀 Starting login automation...')

    // Navigate to login page
    await page.goto(`${TARGET_URL}/login`)
    await takeScreenshot(page, 'login-page')

    // Fill login form
    console.log('📝 Filling login form...')
    await safeType(page, 'input[name="email"]', 'admin@test.com')
    await safeType(page, 'input[name="password"]', 'password123')
    await takeScreenshot(page, 'form-filled')

    // Submit form
    console.log('✅ Submitting form...')
    await safeClick(page, 'button[type="submit"]')

    // Wait for successful login (dashboard or redirect)
    await page.waitForURL('**/dashboard', { timeout: 10000 })
    await waitForText(page, 'Welcome')

    await takeScreenshot(page, 'login-success')
    console.log('✅ Login successful!')

    // Test navigation after login
    console.log('🧪 Testing authenticated navigation...')
    await safeClick(page, 'nav a:has-text("Settings")')
    await page.waitForURL('**/settings')
    await takeScreenshot(page, 'settings-page')

    console.log('🎉 Automation completed successfully!')
  } catch (error) {
    console.error('❌ Automation failed:', error.message)
    await takeScreenshot(page, 'error-state')
    throw error
  } finally {
    await browser.close()
  }
})()
