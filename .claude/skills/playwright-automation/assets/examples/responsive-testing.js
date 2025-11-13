/**
 * Example: Responsive Design Testing
 *
 * Captures screenshots across multiple viewports for design validation.
 * Save to /tmp and run with: node /tmp/responsive-testing.js
 */

const { chromium } = require('playwright')
const { takeScreenshot } = require('../../scripts/helpers.js')

const TARGET_URL = 'http://localhost:3000'

const VIEWPORTS = [
  { width: 1920, height: 1080, name: 'desktop-hd', device: 'Desktop HD' },
  { width: 1366, height: 768, name: 'desktop', device: 'Desktop' },
  { width: 768, height: 1024, name: 'tablet', device: 'iPad Portrait' },
  {
    width: 1024,
    height: 768,
    name: 'tablet-landscape',
    device: 'iPad Landscape',
  },
  { width: 375, height: 812, name: 'mobile-iphone', device: 'iPhone X' },
  {
    width: 414,
    height: 896,
    name: 'mobile-large',
    device: 'iPhone 11 Pro Max',
  },
]

const PAGES_TO_TEST = [
  { path: '/', name: 'homepage' },
  { path: '/login', name: 'login' },
  { path: '/dashboard', name: 'dashboard' },
  { path: '/admin/users', name: 'admin-users' },
]

;(async () => {
  const browser = await chromium.launch({
    headless: true, // Use headless for faster screenshot generation
  })

  const context = await browser.newContext()
  const page = await context.newPage()

  try {
    console.log('🚀 Starting responsive design testing...')
    console.log(
      `📱 Testing ${VIEWPORTS.length} viewports across ${PAGES_TO_TEST.length} pages\n`
    )

    let totalScreenshots = 0

    for (const viewport of VIEWPORTS) {
      console.log(
        `\n📐 Testing ${viewport.device} (${viewport.width}x${viewport.height})`
      )

      await page.setViewportSize({
        width: viewport.width,
        height: viewport.height,
      })

      for (const pageConfig of PAGES_TO_TEST) {
        try {
          await page.goto(`${TARGET_URL}${pageConfig.path}`, {
            waitUntil: 'networkidle',
            timeout: 10000,
          })

          const filename = `/tmp/responsive-${viewport.name}-${pageConfig.name}.png`
          await takeScreenshot(
            page,
            `responsive-${viewport.name}-${pageConfig.name}`,
            {
              path: filename,
              fullPage: true,
            }
          )

          totalScreenshots++
          console.log(`  ✅ ${pageConfig.name}`)
        } catch (error) {
          console.log(`  ❌ ${pageConfig.name}: ${error.message}`)
        }
      }
    }

    console.log(`\n🎉 Responsive testing completed!`)
    console.log(`📸 Generated ${totalScreenshots} screenshots in /tmp/`)
    console.log(`\n💡 View screenshots: ls -lh /tmp/responsive-*.png`)
  } catch (error) {
    console.error('❌ Responsive testing failed:', error.message)
    throw error
  } finally {
    await browser.close()
  }
})()
