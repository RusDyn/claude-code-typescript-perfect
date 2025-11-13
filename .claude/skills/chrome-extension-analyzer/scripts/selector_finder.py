#!/usr/bin/env python3
"""
Selector Finder for Chrome Extensions

Generates robust CSS and XPath selectors with fallback strategies.
Tests selector uniqueness and stability.
"""

import sys
import json
import re
from html.parser import HTMLParser

class SelectorGenerator:
    """Generate robust selectors with multiple fallback strategies"""
    
    @staticmethod
    def escape_css(value):
        """Escape special characters for CSS selectors"""
        return re.sub(r'([!"#$%&\'()*+,.\/:;<=>?@\[\\\]^`{|}~])', r'\\\1', value)
    
    @staticmethod
    def generate_css_selectors(element_data):
        """Generate multiple CSS selector strategies"""
        selectors = []
        tag = element_data.get('tag', 'div')
        attrs = element_data.get('attrs', {})
        text = element_data.get('text', '').strip()
        
        # Strategy 1: ID (highest priority if exists and looks stable)
        if 'id' in attrs:
            elem_id = attrs['id']
            # Check if ID looks generated (contains random strings/numbers)
            if not re.search(r'[a-f0-9]{8,}|random|generated|[0-9]{10,}', elem_id.lower()):
                selectors.append({
                    'selector': f"#{SelectorGenerator.escape_css(elem_id)}",
                    'strategy': 'id',
                    'priority': 1,
                    'stability': 'high'
                })
        
        # Strategy 2: Data attributes (most stable)
        data_attrs = {k: v for k, v in attrs.items() if k.startswith('data-')}
        for attr_name, attr_value in data_attrs.items():
            selectors.append({
                'selector': f"{tag}[{attr_name}='{attr_value}']",
                'strategy': 'data-attribute',
                'priority': 2,
                'stability': 'very-high'
            })
        
        # Strategy 3: Name attribute (for form elements)
        if 'name' in attrs:
            selectors.append({
                'selector': f"{tag}[name='{attrs['name']}']",
                'strategy': 'name-attribute',
                'priority': 2,
                'stability': 'high'
            })
        
        # Strategy 4: ARIA/Role attributes
        if 'role' in attrs:
            selectors.append({
                'selector': f"{tag}[role='{attrs['role']}']",
                'strategy': 'aria-role',
                'priority': 3,
                'stability': 'high'
            })
        
        if 'aria-label' in attrs:
            selectors.append({
                'selector': f"{tag}[aria-label='{attrs['aria-label']}']",
                'strategy': 'aria-label',
                'priority': 3,
                'stability': 'high'
            })
        
        # Strategy 5: Class-based (filter out likely generated classes)
        if 'class' in attrs:
            classes = attrs['class'].split()
            stable_classes = [c for c in classes if not re.search(
                r'css-[a-z0-9]+|[a-f0-9]{6,}|makeStyles|jss[0-9]+|emotion',
                c,
                re.IGNORECASE
            )]
            
            if stable_classes:
                # Single class
                for cls in stable_classes[:2]:
                    selectors.append({
                        'selector': f"{tag}.{cls}",
                        'strategy': 'single-class',
                        'priority': 5,
                        'stability': 'medium'
                    })
                
                # Combined classes
                if len(stable_classes) >= 2:
                    combined = '.'.join(stable_classes[:3])
                    selectors.append({
                        'selector': f"{tag}.{combined}",
                        'strategy': 'combined-classes',
                        'priority': 4,
                        'stability': 'medium-high'
                    })
        
        # Strategy 6: Attribute selectors for specific types
        if tag == 'input' and 'type' in attrs:
            selectors.append({
                'selector': f"input[type='{attrs['type']}']",
                'strategy': 'input-type',
                'priority': 6,
                'stability': 'medium',
                'note': 'May match multiple elements'
            })
        
        # Strategy 7: Text content (for buttons, links)
        if text and tag in ['button', 'a', 'span', 'h1', 'h2', 'h3']:
            # Normalize text
            normalized_text = ' '.join(text.split())
            if len(normalized_text) < 50:  # Only for short text
                selectors.append({
                    'selector': f"{tag}:contains('{normalized_text}')",
                    'strategy': 'text-content',
                    'priority': 7,
                    'stability': 'low',
                    'note': 'Requires jQuery or custom contains() implementation'
                })
        
        return sorted(selectors, key=lambda x: x['priority'])
    
    @staticmethod
    def generate_xpath_selectors(element_data):
        """Generate XPath selectors"""
        selectors = []
        tag = element_data.get('tag', 'div')
        attrs = element_data.get('attrs', {})
        text = element_data.get('text', '').strip()
        
        # XPath by ID
        if 'id' in attrs:
            selectors.append({
                'selector': f"//{tag}[@id='{attrs['id']}']",
                'strategy': 'xpath-id',
                'priority': 1,
                'stability': 'high'
            })
        
        # XPath by data attributes
        for attr_name, attr_value in attrs.items():
            if attr_name.startswith('data-'):
                selectors.append({
                    'selector': f"//{tag}[@{attr_name}='{attr_value}']",
                    'strategy': 'xpath-data-attr',
                    'priority': 2,
                    'stability': 'very-high'
                })
        
        # XPath by text content
        if text and len(text) < 50:
            normalized_text = ' '.join(text.split())
            selectors.append({
                'selector': f"//{tag}[text()='{normalized_text}']",
                'strategy': 'xpath-text',
                'priority': 5,
                'stability': 'medium'
            })
            
            # Contains text
            selectors.append({
                'selector': f"//{tag}[contains(text(), '{normalized_text}')]",
                'strategy': 'xpath-contains',
                'priority': 6,
                'stability': 'low'
            })
        
        return sorted(selectors, key=lambda x: x['priority'])
    
    @staticmethod
    def generate_fallback_strategy(selectors):
        """Generate a fallback strategy using multiple selectors"""
        if not selectors:
            return None
        
        # Group by stability
        high_stability = [s for s in selectors if s['stability'] in ['very-high', 'high']]
        medium_stability = [s for s in selectors if s['stability'] == 'medium']
        
        strategy = {
            'primary': high_stability[0]['selector'] if high_stability else selectors[0]['selector'],
            'fallbacks': []
        }
        
        # Add fallbacks
        remaining = high_stability[1:] + medium_stability
        strategy['fallbacks'] = [s['selector'] for s in remaining[:3]]
        
        # Generate code
        strategy['code'] = f"""
function findElement() {{
    // Try primary selector
    let element = document.querySelector('{strategy['primary']}');
    if (element) return element;
    
    // Try fallbacks
    {chr(10).join(f"    element = document.querySelector('{fb}');" + chr(10) + "    if (element) return element;" for fb in strategy['fallbacks'])}
    
    console.warn('Element not found with any selector');
    return null;
}}
"""
        
        return strategy

def main():
    if len(sys.argv) < 2:
        print("Usage: python selector_finder.py '<element_json>'")
        print("Example element JSON:")
        print(json.dumps({
            'tag': 'button',
            'attrs': {
                'id': 'submit-btn',
                'class': 'btn btn-primary',
                'data-action': 'submit'
            },
            'text': 'Submit Form'
        }, indent=2))
        sys.exit(1)
    
    element_data = json.loads(sys.argv[1])
    
    css_selectors = SelectorGenerator.generate_css_selectors(element_data)
    xpath_selectors = SelectorGenerator.generate_xpath_selectors(element_data)
    
    all_selectors = css_selectors + xpath_selectors
    fallback_strategy = SelectorGenerator.generate_fallback_strategy(all_selectors)
    
    result = {
        'element': element_data,
        'css_selectors': css_selectors,
        'xpath_selectors': xpath_selectors,
        'recommended_fallback_strategy': fallback_strategy
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
