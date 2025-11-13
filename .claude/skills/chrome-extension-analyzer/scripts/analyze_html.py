#!/usr/bin/env python3
"""
HTML Analyzer for Chrome Extension Development

Analyzes HTML structure to identify key elements and generate robust selectors.
Handles dynamic content, SPAs, shadow DOM, and suggests best practices.
"""

import sys
import json
from html.parser import HTMLParser
from collections import defaultdict, Counter

class HTMLAnalyzer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []
        self.current_path = []
        self.id_count = Counter()
        self.class_count = Counter()
        self.data_attrs = set()
        self.interactive_elements = []
        self.forms = []
        self.links = []
        self.buttons = []
        self.inputs = []
        self.depth = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.depth += 1
        
        # Track element with context
        element_info = {
            'tag': tag,
            'attrs': attrs_dict,
            'depth': self.depth,
            'path': '/'.join(self.current_path + [tag])
        }
        self.elements.append(element_info)
        self.current_path.append(tag)
        
        # Track IDs and classes
        if 'id' in attrs_dict:
            self.id_count[attrs_dict['id']] += 1
        if 'class' in attrs_dict:
            classes = attrs_dict['class'].split()
            for cls in classes:
                self.class_count[cls] += 1
        
        # Track data attributes
        for attr_name in attrs_dict.keys():
            if attr_name.startswith('data-'):
                self.data_attrs.add(attr_name)
        
        # Track interactive elements
        if tag in ['button', 'a', 'input', 'select', 'textarea']:
            self.interactive_elements.append(element_info)
            
        if tag == 'button':
            self.buttons.append(element_info)
        elif tag == 'a':
            self.links.append(element_info)
        elif tag == 'input':
            self.inputs.append(element_info)
        elif tag == 'form':
            self.forms.append(element_info)
    
    def handle_endtag(self, tag):
        if self.current_path and self.current_path[-1] == tag:
            self.current_path.pop()
        self.depth -= 1

def analyze_page_type(analyzer):
    """Detect the type of page based on structure"""
    page_types = []
    
    # E-commerce indicators
    if any('cart' in str(e).lower() or 'checkout' in str(e).lower() 
           for e in analyzer.elements):
        page_types.append('e-commerce')
    
    # Social media indicators
    if any('post' in str(e).lower() or 'feed' in str(e).lower() 
           or 'timeline' in str(e).lower() for e in analyzer.elements):
        page_types.append('social-media')
    
    # Chat/messaging indicators
    if any('message' in str(e).lower() or 'chat' in str(e).lower() 
           for e in analyzer.elements):
        page_types.append('chat/messaging')
    
    # Form-heavy
    if len(analyzer.forms) > 2:
        page_types.append('form-based')
    
    # SPA indicators (lots of divs, minimal semantic HTML)
    div_count = sum(1 for e in analyzer.elements if e['tag'] == 'div')
    if div_count > 50 and len(analyzer.elements) > 100:
        page_types.append('SPA (likely React/Vue/Angular)')
    
    return page_types if page_types else ['general']

def suggest_selectors(element_info, analyzer):
    """Generate robust selector suggestions for an element"""
    selectors = []
    attrs = element_info['attrs']
    tag = element_info['tag']
    
    # ID selector (most specific, but can be dynamic)
    if 'id' in attrs:
        elem_id = attrs['id']
        is_unique = analyzer.id_count[elem_id] == 1
        is_dynamic = any(char.isdigit() for char in elem_id[-8:])
        
        selectors.append({
            'selector': f"#{elem_id}",
            'type': 'id',
            'robustness': 'high' if (is_unique and not is_dynamic) else 'medium',
            'note': 'Unique ID' if is_unique else 'Non-unique ID (avoid)',
            'warning': 'May be dynamically generated' if is_dynamic else None
        })
    
    # Data attribute selectors (usually most stable)
    for attr_name, attr_value in attrs.items():
        if attr_name.startswith('data-') and attr_value:
            selectors.append({
                'selector': f"[{attr_name}='{attr_value}']",
                'type': 'data-attribute',
                'robustness': 'high',
                'note': 'Data attributes are usually stable'
            })
    
    # Class selectors
    if 'class' in attrs:
        classes = attrs['class'].split()
        stable_classes = [c for c in classes if not any(
            substring in c.lower() for substring in ['random', 'hash', 'css-']
        )]
        
        for cls in stable_classes[:3]:  # Limit to top 3 classes
            frequency = analyzer.class_count[cls]
            selectors.append({
                'selector': f".{cls}",
                'type': 'class',
                'robustness': 'medium' if frequency < 10 else 'low',
                'note': f'Used {frequency} times on page'
            })
    
    # Attribute selectors for specific element types
    if tag == 'input' and 'type' in attrs:
        selectors.append({
            'selector': f"input[type='{attrs['type']}']",
            'type': 'attribute',
            'robustness': 'medium',
            'note': 'Input type selector'
        })
    
    if 'name' in attrs:
        selectors.append({
            'selector': f"[name='{attrs['name']}']",
            'type': 'attribute',
            'robustness': 'high',
            'note': 'Name attribute is usually stable'
        })
    
    # Role-based selectors (accessibility)
    if 'role' in attrs:
        selectors.append({
            'selector': f"[role='{attrs['role']}']",
            'type': 'role',
            'robustness': 'high',
            'note': 'ARIA role selector (accessibility)'
        })
    
    return selectors

def generate_report(html_content):
    """Generate comprehensive analysis report"""
    analyzer = HTMLAnalyzer()
    analyzer.feed(html_content)
    
    page_types = analyze_page_type(analyzer)
    
    report = {
        'summary': {
            'total_elements': len(analyzer.elements),
            'unique_ids': len([id for id, count in analyzer.id_count.items() if count == 1]),
            'total_classes': len(analyzer.class_count),
            'data_attributes': list(analyzer.data_attrs),
            'page_types': page_types,
            'interactive_elements': len(analyzer.interactive_elements)
        },
        'key_elements': {
            'buttons': len(analyzer.buttons),
            'links': len(analyzer.links),
            'inputs': len(analyzer.inputs),
            'forms': len(analyzer.forms)
        },
        'recommendations': []
    }
    
    # Generate recommendations
    if 'SPA' in str(page_types):
        report['recommendations'].append({
            'type': 'SPA_DETECTED',
            'message': 'Page appears to be a Single Page Application. Use MutationObserver to detect dynamic content changes.',
            'code_snippet': '''
// Watch for dynamic content
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.addedNodes.length) {
            // New content added, reinject your functionality
            injectFeatures();
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
'''
        })
    
    if analyzer.data_attrs:
        report['recommendations'].append({
            'type': 'DATA_ATTRIBUTES',
            'message': f'Found {len(analyzer.data_attrs)} data attributes. These are usually stable selectors.',
            'attributes': list(analyzer.data_attrs)[:10]
        })
    
    # Analyze interactive elements for selector suggestions
    sample_buttons = analyzer.buttons[:5]
    if sample_buttons:
        report['button_selectors'] = []
        for btn in sample_buttons:
            selectors = suggest_selectors(btn, analyzer)
            report['button_selectors'].append({
                'element': btn,
                'suggested_selectors': selectors
            })
    
    return report

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_html.py <html_file>")
        print("   or: python analyze_html.py - (read from stdin)")
        sys.exit(1)
    
    if sys.argv[1] == '-':
        html_content = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            html_content = f.read()
    
    report = generate_report(html_content)
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
