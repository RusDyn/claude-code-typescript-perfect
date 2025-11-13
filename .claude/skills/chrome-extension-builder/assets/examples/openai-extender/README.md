# OpenAI Codex Page Extender Example

This example demonstrates how to extend OpenAI Codex pages with custom functionality.

## Features

- Adds custom toolbox to OpenAI Codex interface
- Injects helper buttons for common actions
- Stores code snippets for quick access
- Enhances code editor with additional features

## Selectors Used

```javascript
const SELECTORS = {
  // Main editor container
  editor: ['.monaco-editor', '[class*="editor"]', '#code-editor'],

  // Toolbar
  toolbar: ['[class*="toolbar"]', '.header-actions', 'header nav'],

  // Code output
  output: ['[class*="output"]', '.response-container', '#ai-response'],
}
```

## Implementation Notes

- Uses Monaco Editor API if available
- Falls back to DOM manipulation
- Handles dynamic content loading
- Persists user preferences in chrome.storage

## Files

- `manifest.json` - Extension configuration
- `content.js` - Main injection logic
- `background.js` - Background processes
- `styles.css` - Custom styling
