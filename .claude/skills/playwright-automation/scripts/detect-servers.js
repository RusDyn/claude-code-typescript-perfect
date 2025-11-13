#!/usr/bin/env node

/**
 * Auto-detect running development servers
 *
 * Scans common ports for running web servers and identifies them.
 * Helps automatically find the correct URL for automation scripts.
 */

const http = require('http')
const https = require('https')

const COMMON_PORTS = [
  { port: 3000, name: 'Next.js / React Dev Server', protocol: 'http' },
  { port: 3001, name: 'Next.js (alternate)', protocol: 'http' },
  { port: 5173, name: 'Vite', protocol: 'http' },
  { port: 5174, name: 'Vite (alternate)', protocol: 'http' },
  { port: 4200, name: 'Angular', protocol: 'http' },
  { port: 8080, name: 'Generic Dev Server', protocol: 'http' },
  { port: 8000, name: 'Python / Django', protocol: 'http' },
  { port: 9000, name: 'Generic Dev Server', protocol: 'http' },
]

/**
 * Check if a server is running on a specific port
 */
async function checkPort(port, protocol = 'http') {
  return new Promise(resolve => {
    const client = protocol === 'https' ? https : http
    const url = `${protocol}://localhost:${port}`

    const req = client.get(url, { timeout: 1000 }, res => {
      resolve({
        running: true,
        port,
        protocol,
        statusCode: res.statusCode,
        url,
      })
    })

    req.on('error', () => {
      resolve({ running: false, port, protocol })
    })

    req.on('timeout', () => {
      req.destroy()
      resolve({ running: false, port, protocol })
    })
  })
}

/**
 * Detect all running servers
 */
async function detectDevServers() {
  console.log('🔍 Scanning for running development servers...\n')

  const checks = COMMON_PORTS.map(({ port, name, protocol }) =>
    checkPort(port, protocol).then(result => ({
      ...result,
      name,
    }))
  )

  const results = await Promise.all(checks)
  const running = results.filter(r => r.running)

  if (running.length === 0) {
    console.log('❌ No development servers detected')
    console.log('\nCommon server start commands:')
    console.log('  Next.js:  npm run dev')
    console.log('  Vite:     npm run dev')
    console.log('  Angular:  ng serve')
    return []
  }

  console.log(`✅ Found ${running.length} running server(s):\n`)

  running.forEach((server, index) => {
    console.log(`${index + 1}. ${server.name}`)
    console.log(`   URL: ${server.url}`)
    console.log(`   Status: ${server.statusCode || 'Running'}`)
    console.log('')
  })

  console.log('💡 Use these URLs in your automation scripts:')
  running.forEach(server => {
    console.log(`   await page.goto('${server.url}');`)
  })

  return running
}

/**
 * Get the primary development server (first running server found)
 */
async function getPrimaryServer() {
  const servers = await detectDevServers()
  return servers[0] || null
}

// Run if called directly
if (require.main === module) {
  detectDevServers()
    .then(servers => {
      process.exit(servers.length > 0 ? 0 : 1)
    })
    .catch(error => {
      console.error('Error detecting servers:', error)
      process.exit(1)
    })
}

module.exports = {
  detectDevServers,
  getPrimaryServer,
  checkPort,
}
