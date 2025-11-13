/**
 * Playwright Test Helper Functions
 *
 * Reusable utilities for E2E tests with better error handling and reliability.
 * Import these in your test files for consistent, maintainable test code.
 */

import { Page, expect } from '@playwright/test'

/**
 * Safe click with automatic waiting and retry logic
 */
export async function safeClick(
  page: Page,
  selector: string,
  options: { timeout?: number; retries?: number; force?: boolean } = {}
): Promise<void> {
  const { timeout = 10000, retries = 3, force = false } = options

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      await page.waitForSelector(selector, {
        state: 'visible',
        timeout: timeout / retries,
      })

      await page.click(selector, { force, timeout: timeout / retries })
      return
    } catch (error) {
      if (attempt === retries) {
        throw new Error(
          `Failed to click "${selector}" after ${retries} attempts: ${error}`
        )
      }
      console.log(`Click attempt ${attempt} failed, retrying...`)
      await page.waitForTimeout(500)
    }
  }
}

/**
 * Safe type with automatic clear and better error handling
 */
export async function safeType(
  page: Page,
  selector: string,
  text: string,
  options: { timeout?: number; delay?: number; clear?: boolean } = {}
): Promise<void> {
  const { timeout = 10000, delay = 50, clear = true } = options

  await page.waitForSelector(selector, { state: 'visible', timeout })

  if (clear) {
    await page.fill(selector, '')
  }

  await page.type(selector, text, { delay })
}

/**
 * Fill form with multiple fields
 */
export async function fillForm(
  page: Page,
  formData: Record<string, string>,
  options: { submitButton?: string; waitForNavigation?: boolean } = {}
): Promise<void> {
  const { submitButton, waitForNavigation = true } = options

  for (const [field, value] of Object.entries(formData)) {
    const selector = `input[name="${field}"], textarea[name="${field}"], select[name="${field}"]`
    await safeType(page, selector, value)
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
 * Wait for element to be visible
 */
export async function waitForVisible(
  page: Page,
  selector: string,
  timeout = 10000
): Promise<void> {
  await page.waitForSelector(selector, { state: 'visible', timeout })
}

/**
 * Wait for element to be hidden
 */
export async function waitForHidden(
  page: Page,
  selector: string,
  timeout = 10000
): Promise<void> {
  await page.waitForSelector(selector, { state: 'hidden', timeout })
}

/**
 * Check if element exists
 */
export async function elementExists(
  page: Page,
  selector: string,
  timeout = 1000
): Promise<boolean> {
  try {
    await page.waitForSelector(selector, { timeout })
    return true
  } catch {
    return false
  }
}

/**
 * Get text content safely
 */
export async function getText(
  page: Page,
  selector: string,
  options: { timeout?: number } = {}
): Promise<string> {
  const { timeout = 5000 } = options
  await page.waitForSelector(selector, { state: 'visible', timeout })
  const text = await page.textContent(selector)
  return text?.trim() || ''
}

/**
 * Wait for text to appear
 */
export async function waitForText(
  page: Page,
  text: string,
  timeout = 10000
): Promise<void> {
  await page.waitForSelector(`text=${text}`, { timeout })
}

/**
 * Scroll to element
 */
export async function scrollToElement(
  page: Page,
  selector: string,
  options: {
    behavior?: 'auto' | 'smooth'
    block?: 'start' | 'center' | 'end'
  } = {}
): Promise<void> {
  const { behavior = 'smooth', block = 'center' } = options

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
}

/**
 * Wait for network to be idle
 */
export async function waitForNetworkIdle(
  page: Page,
  timeout = 2000
): Promise<boolean> {
  try {
    await page.waitForLoadState('networkidle', { timeout })
    return true
  } catch {
    console.warn('Network idle timeout reached, continuing...')
    return false
  }
}

/**
 * Handle cookie consent banners
 */
export async function handleCookieBanner(
  page: Page,
  timeout = 3000
): Promise<boolean> {
  const commonSelectors = [
    'button:has-text("Accept")',
    'button:has-text("Accept all")',
    'button:has-text("I agree")',
    'button:has-text("OK")',
    '[data-testid*="cookie-accept"]',
    '[id*="cookie-accept"]',
  ]

  for (const selector of commonSelectors) {
    try {
      const button = await page.$(selector)
      if (button) {
        await button.click({ timeout })
        return true
      }
    } catch {
      // Continue to next selector
    }
  }

  return false
}

/**
 * Capture console logs during test
 */
export function captureConsoleLogs(
  page: Page,
  filter?: 'log' | 'error' | 'warn' | 'info'
): string[] {
  const logs: string[] = []

  page.on('console', msg => {
    if (!filter || msg.type() === filter) {
      logs.push(`[${msg.type()}] ${msg.text()}`)
    }
  })

  return logs
}

/**
 * Monitor network requests
 */
export function monitorNetwork(
  page: Page,
  urlFilter?: string
): Array<{ url: string; method: string; status?: number }> {
  const requests: Array<{ url: string; method: string; status?: number }> = []

  page.on('request', request => {
    if (!urlFilter || request.url().includes(urlFilter)) {
      requests.push({
        url: request.url(),
        method: request.method(),
      })
    }
  })

  page.on('response', response => {
    const req = requests.find(r => r.url === response.url())
    if (req) {
      req.status = response.status()
    }
  })

  return requests
}

/**
 * Extract table data
 */
export async function extractTableData(
  page: Page,
  tableSelector: string
): Promise<Record<string, string>[]> {
  return await page.evaluate(selector => {
    const table = document.querySelector(selector)
    if (!table) return []

    const headers = Array.from(table.querySelectorAll('thead th')).map(
      th => th.textContent?.trim() || ''
    )

    const rows = Array.from(table.querySelectorAll('tbody tr'))

    return rows.map(tr => {
      const cells = Array.from(tr.querySelectorAll('td')).map(
        td => td.textContent?.trim() || ''
      )

      return headers.reduce(
        (obj, header, index) => {
          obj[header] = cells[index] || ''
          return obj
        },
        {} as Record<string, string>
      )
    })
  }, tableSelector)
}

/**
 * Login helper for authenticated tests
 */
export async function login(
  page: Page,
  credentials: { email: string; password: string },
  options: { loginUrl?: string; dashboardUrl?: string } = {}
): Promise<void> {
  const { loginUrl = '/login', dashboardUrl = '/dashboard' } = options

  await page.goto(loginUrl)
  await safeType(page, 'input[name="email"]', credentials.email)
  await safeType(page, 'input[name="password"]', credentials.password)
  await safeClick(page, 'button[type="submit"]')
  await page.waitForURL(`**${dashboardUrl}`, { timeout: 10000 })
}

/**
 * Assertion helpers
 */
export async function expectVisible(
  page: Page,
  selector: string,
  timeout = 5000
): Promise<void> {
  await expect(page.locator(selector)).toBeVisible({ timeout })
}

export async function expectHidden(
  page: Page,
  selector: string,
  timeout = 5000
): Promise<void> {
  await expect(page.locator(selector)).toBeHidden({ timeout })
}

export async function expectText(
  page: Page,
  selector: string,
  text: string | RegExp,
  timeout = 5000
): Promise<void> {
  await expect(page.locator(selector)).toHaveText(text, { timeout })
}

export async function expectUrl(
  page: Page,
  url: string | RegExp,
  timeout = 5000
): Promise<void> {
  await expect(page).toHaveURL(url, { timeout })
}
