# Marketplace Score Injector Example

Injects product quality/trust scores into marketplace buy buttons (Amazon, eBay, etc.).

## Features

- Fetches product score from API
- Injects score button next to buy button
- Color-coded scoring (green/yellow/red)
- Detailed score breakdown on click
- Works across multiple marketplaces

## Marketplace-Specific Selectors

### Amazon

```javascript
const AMAZON_SELECTORS = {
  buyButton: [
    '#buy-now-button',
    '[data-action="buy-now"]',
    'input[name="submit.buy-now"]',
    '.a-button-primary #add-to-cart-button',
  ],
  productId: ['[data-asin]', 'input[name="ASIN"]'],
  price: [
    '.a-price .a-offscreen',
    '#priceblock_ourprice',
    '#priceblock_dealprice',
  ],
}
```

### eBay

```javascript
const EBAY_SELECTORS = {
  buyButton: [
    '#binBtn_btn',
    '[data-test-id="buy-it-now-button"]',
    '.ux-call-to-action__cell button',
  ],
  productId: ['[data-item-id]', 'input[name="item"]'],
  price: ['.x-price-primary', '[itemprop="price"]'],
}
```

## Score Display

```javascript
function injectScoreButton(buyButton, score, details) {
  const button = document.createElement('button')
  button.textContent = `Trust Score: ${score}/100`
  button.className = 'marketplace-score-btn'

  // Color coding
  const color = score >= 70 ? '#4CAF50' : score >= 40 ? '#FF9800' : '#F44336'

  button.style.cssText = `
    padding: 10px 20px;
    background: ${color};
    color: white;
    border: none;
    border-radius: 4px;
    margin-left: 12px;
    cursor: pointer;
    font-weight: bold;
  `

  button.addEventListener('click', e => {
    e.preventDefault()
    e.stopPropagation()
    showScoreDetails(details)
  })

  buyButton.insertAdjacentElement('afterend', button)
}
```

## API Integration

```javascript
// Get score from background script (bypasses CORS)
chrome.runtime.sendMessage(
  {
    action: 'getProductScore',
    productId: extractedId,
    marketplace: 'amazon',
    url: window.location.href,
  },
  response => {
    if (response?.score) {
      injectScoreButton(buyButton, response.score, response.details)
    }
  }
)
```

## Files

- `manifest.json` - Supports multiple marketplace domains
- `content.js` - Universal marketplace handler
- `background.js` - API calls and score caching
- `marketplaces.js` - Marketplace-specific selectors
