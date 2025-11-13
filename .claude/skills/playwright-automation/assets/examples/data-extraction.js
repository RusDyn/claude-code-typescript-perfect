/**
 * Example: Data Extraction from Tables
 *
 * Demonstrates extracting structured data from web pages.
 * Save to /tmp and run with: node /tmp/data-extraction.js
 */

const { chromium } = require('playwright')
const {
  extractTableData,
  waitForNetworkIdle,
} = require('../../scripts/helpers.js')
const fs = require('fs')

const TARGET_URL = 'http://localhost:3000'

;(async () => {
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
  })

  const page = await browser.newPage()

  try {
    console.log('🚀 Starting data extraction...')

    // Navigate to page with data
    await page.goto(`${TARGET_URL}/admin/users`)
    await waitForNetworkIdle(page)

    // Extract user data from table
    console.log('📊 Extracting user data...')
    const users = await extractTableData(page, 'table.user-list')

    if (users && users.length > 0) {
      console.log(`✅ Extracted ${users.length} users`)

      // Display sample
      console.log('\nSample data:')
      console.log(JSON.stringify(users.slice(0, 3), null, 2))

      // Save to file
      const outputPath = '/tmp/users-export.json'
      fs.writeFileSync(outputPath, JSON.stringify(users, null, 2))
      console.log(`\n💾 Data saved to: ${outputPath}`)

      // Generate CSV
      const csvPath = '/tmp/users-export.csv'
      const headers = Object.keys(users[0])
      const csvContent = [
        headers.join(','),
        ...users.map(row => headers.map(h => `"${row[h]}"`).join(',')),
      ].join('\n')
      fs.writeFileSync(csvPath, csvContent)
      console.log(`💾 CSV saved to: ${csvPath}`)
    } else {
      console.log('❌ No data found in table')
    }

    // Extract other structured data
    console.log('\n🔍 Extracting page statistics...')
    const stats = await page.evaluate(() => {
      return {
        totalUsers: document.querySelectorAll('table.user-list tr').length - 1,
        activeUsers: document.querySelectorAll('tr .badge-active').length,
        timestamp: new Date().toISOString(),
      }
    })

    console.log('Statistics:', stats)

    console.log('\n🎉 Data extraction completed successfully!')
  } catch (error) {
    console.error('❌ Data extraction failed:', error.message)
    throw error
  } finally {
    await browser.close()
  }
})()
