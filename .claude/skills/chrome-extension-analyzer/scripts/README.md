# Chrome Extension Analyzer Scripts

## Requirements

**Python:** 3.7+ (no external dependencies required)

All scripts use only Python standard library modules:
- `html.parser` for HTML parsing
- `json` for data serialization
- `collections` for data structures
- `sys` for I/O operations

## Scripts

### analyze_html.py
Analyzes HTML structure to identify elements and suggest selectors.

**Usage:**
```bash
# From file
python analyze_html.py page.html

# From stdin
curl https://example.com | python analyze_html.py -

# From saved HTML
cat saved_page.html | python analyze_html.py -
```

**Output:** JSON with page analysis, element counts, selector recommendations, SPA detection.

### selector_finder.py
Generates robust selectors with fallback strategies.

**Usage:**
```bash
python selector_finder.py '{
  "tag": "button",
  "attrs": {"id": "submit", "class": "btn primary"},
  "text": "Submit"
}'
```

**Output:** Prioritized selector list with CSS and XPath options, stability ratings, fallback code.

### generate_manifest.py
Creates Manifest V3 configuration based on requirements.

**Usage:**
```bash
python generate_manifest.py '{
  "name": "My Extension",
  "features": ["content_script", "storage"],
  "target_urls": ["https://example.com/*"]
}'
```

**Output:** Complete manifest.json file with proper permissions and structure.

## Quick Setup

```bash
# No installation needed - uses Python standard library only
python3 --version  # Verify Python 3.7+

# Run any script
python3 analyze_html.py page.html
python3 selector_finder.py '{"tag": "button", "attrs": {...}}'
```

## Examples

```bash
# Analyze a live page
curl -s https://github.com | python3 analyze_html.py - | jq .

# Generate manifest for content injection
python3 generate_manifest.py '{
  "name": "GitHub Enhancer",
  "features": ["content_script", "storage", "tabs"],
  "target_urls": ["https://github.com/*"]
}' > manifest.json
```
