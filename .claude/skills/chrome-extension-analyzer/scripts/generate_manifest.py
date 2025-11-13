#!/usr/bin/env python3
"""
Manifest V3 Generator for Chrome Extensions

Generates proper Manifest V3 configuration based on extension requirements.
"""

import sys
import json

def generate_manifest(config):
    """Generate Manifest V3 JSON based on configuration"""
    
    name = config.get('name', 'My Chrome Extension')
    description = config.get('description', 'A Chrome extension')
    version = config.get('version', '1.0.0')
    
    # Base manifest structure
    manifest = {
        "manifest_version": 3,
        "name": name,
        "description": description,
        "version": version,
        "icons": {
            "16": "icons/icon16.png",
            "48": "icons/icon48.png",
            "128": "icons/icon128.png"
        }
    }
    
    # Add permissions based on features
    permissions = set()
    host_permissions = set()
    
    features = config.get('features', [])
    
    # Storage
    if 'storage' in features:
        permissions.add('storage')
    
    # Tabs (for URL detection, tab management)
    if 'tabs' in features or 'url_detection' in features:
        permissions.add('tabs')
    
    # Network interception
    if 'network_interception' in features or 'api_intercept' in features:
        permissions.add('declarativeNetRequest')
        permissions.add('declarativeNetRequestFeedback')
    
    # Cookies
    if 'cookies' in features:
        permissions.add('cookies')
    
    # Alarms/scheduling
    if 'alarms' in features:
        permissions.add('alarms')
    
    # Notifications
    if 'notifications' in features:
        permissions.add('notifications')
    
    # Host permissions for content scripts
    target_urls = config.get('target_urls', [])
    if target_urls:
        for url in target_urls:
            # Convert URL patterns
            if url.startswith('http'):
                host_permissions.add(url + '/*')
            else:
                host_permissions.add(url)
    else:
        # Default to all URLs if none specified
        host_permissions.add('<all_urls>')
    
    if permissions:
        manifest['permissions'] = sorted(list(permissions))
    
    if host_permissions:
        manifest['host_permissions'] = sorted(list(host_permissions))
    
    # Background service worker
    if 'background' in features or 'network_interception' in features:
        manifest['background'] = {
            "service_worker": "background.js"
        }
    
    # Content scripts
    if 'content_script' in features or config.get('inject_sites'):
        inject_sites = config.get('inject_sites', target_urls or ['<all_urls>'])
        
        content_scripts = {
            "matches": inject_sites,
            "js": ["content.js"],
            "run_at": config.get('run_at', 'document_idle')
        }
        
        # Add CSS if specified
        if config.get('inject_css'):
            content_scripts['css'] = ['styles.css']
        
        # Frame injection
        if config.get('all_frames'):
            content_scripts['all_frames'] = True
        
        manifest['content_scripts'] = [content_scripts]
    
    # Action (popup)
    if 'popup' in features:
        manifest['action'] = {
            "default_popup": "popup.html",
            "default_icon": {
                "16": "icons/icon16.png",
                "48": "icons/icon48.png",
                "128": "icons/icon128.png"
            }
        }
    
    # Options page
    if 'options' in features:
        manifest['options_page'] = 'options.html'
    
    # Web accessible resources (for injected content)
    if config.get('web_accessible_resources'):
        manifest['web_accessible_resources'] = [{
            "resources": config['web_accessible_resources'],
            "matches": sorted(list(host_permissions)) if host_permissions else ["<all_urls>"]
        }]
    
    # DeclarativeNetRequest rules (for request interception)
    if 'network_interception' in features:
        manifest['declarative_net_request'] = {
            "rule_resources": [{
                "id": "ruleset_1",
                "enabled": True,
                "path": "rules.json"
            }]
        }
    
    # Content Security Policy (if needed)
    if config.get('csp'):
        manifest['content_security_policy'] = {
            "extension_pages": config['csp']
        }
    
    return manifest

def print_feature_recommendations(config):
    """Print recommendations based on use case"""
    features = config.get('features', [])
    
    print("\n=== RECOMMENDATIONS ===\n", file=sys.stderr)
    
    if 'content_script' in features:
        print("📝 Content Script Tips:", file=sys.stderr)
        print("  - Use document_idle (default) for most cases", file=sys.stderr)
        print("  - Use document_start if you need to run before page loads", file=sys.stderr)
        print("  - Use MutationObserver for dynamic content (SPAs)", file=sys.stderr)
    
    if 'network_interception' in features:
        print("\n🌐 Network Interception Tips:", file=sys.stderr)
        print("  - declarativeNetRequest has limits (max 30k static rules)", file=sys.stderr)
        print("  - Use background.js to handle dynamic rule updates", file=sys.stderr)
        print("  - Consider using chrome.webRequest for complex cases", file=sys.stderr)
    
    if 'storage' in features:
        print("\n💾 Storage Tips:", file=sys.stderr)
        print("  - chrome.storage.local: 10MB limit (unlimited with 'unlimitedStorage')", file=sys.stderr)
        print("  - chrome.storage.sync: 100KB limit, syncs across devices", file=sys.stderr)
        print("  - Use chrome.storage.session for temporary data", file=sys.stderr)
    
    print("\n=== FILE STRUCTURE ===\n", file=sys.stderr)
    print("Recommended extension structure:", file=sys.stderr)
    print("""
  my-extension/
  ├── manifest.json
  ├── background.js       (if using background features)
  ├── content.js          (if injecting into pages)
  ├── popup.html          (if using popup)
  ├── popup.js
  ├── styles.css          (if injecting CSS)
  ├── rules.json          (if using declarativeNetRequest)
  └── icons/
      ├── icon16.png
      ├── icon48.png
      └── icon128.png
    """, file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        example_config = {
            "name": "My Extension",
            "description": "Does cool things",
            "version": "1.0.0",
            "features": [
                "content_script",
                "storage",
                "tabs",
                "popup"
            ],
            "target_urls": [
                "https://example.com/*",
                "https://another-site.com/*"
            ],
            "inject_css": True,
            "all_frames": False,
            "run_at": "document_idle"
        }
        
        print("Usage: python generate_manifest.py '<config_json>'", file=sys.stderr)
        print("\nExample config:", file=sys.stderr)
        print(json.dumps(example_config, indent=2), file=sys.stderr)
        print("\nAvailable features:", file=sys.stderr)
        print("  - content_script: Inject JS into pages", file=sys.stderr)
        print("  - background: Background service worker", file=sys.stderr)
        print("  - storage: Chrome storage API", file=sys.stderr)
        print("  - tabs: Tab management", file=sys.stderr)
        print("  - network_interception: Intercept network requests", file=sys.stderr)
        print("  - popup: Extension popup UI", file=sys.stderr)
        print("  - cookies: Cookie access", file=sys.stderr)
        print("  - notifications: Browser notifications", file=sys.stderr)
        sys.exit(1)
    
    config = json.loads(sys.argv[1])
    manifest = generate_manifest(config)
    
    print(json.dumps(manifest, indent=2))
    print_feature_recommendations(config)

if __name__ == '__main__':
    main()
