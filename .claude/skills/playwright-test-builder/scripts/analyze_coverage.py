#!/usr/bin/env python3
"""
Test Coverage Analyzer

Analyzes existing tests and suggests areas needing coverage.
"""

import sys
import json
import os
import re
from pathlib import Path
from collections import defaultdict

def analyze_test_files(test_dir):
    """Analyze existing test files"""
    
    test_files = []
    test_patterns = defaultdict(int)
    covered_flows = set()
    
    for root, dirs, files in os.walk(test_dir):
        # Skip node_modules and other excluded dirs
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'dist', 'build']]
        
        for file in files:
            if file.endswith(('.spec.ts', '.spec.js', '.test.ts', '.test.js')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, test_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Count test cases
                        test_count = len(re.findall(r"test\(|test\.skip\(|test\.only\(", content))
                        
                        # Find describe blocks
                        describes = re.findall(r"describe\(['\"]([^'\"]+)['\"]", content))
                        
                        # Find test names
                        test_names = re.findall(r"test\(['\"]([^'\"]+)['\"]", content))
                        
                        # Identify patterns
                        if 'beforeEach' in content:
                            test_patterns['uses_beforeEach'] += 1
                        if 'afterEach' in content:
                            test_patterns['uses_afterEach'] += 1
                        if 'page.goto' in content:
                            test_patterns['navigates_pages'] += 1
                        if 'expect' in content:
                            test_patterns['has_assertions'] += 1
                        if '@playwright/test' in content:
                            test_patterns['uses_playwright'] += 1
                        
                        # Track covered flows
                        for name in test_names:
                            flow_type = classify_test_flow(name)
                            if flow_type:
                                covered_flows.add(flow_type)
                        
                        test_files.append({
                            'path': rel_path,
                            'test_count': test_count,
                            'describes': describes,
                            'test_names': test_names[:5]  # First 5 for preview
                        })
                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}", file=sys.stderr)
    
    return {
        'test_files': test_files,
        'total_tests': sum(f['test_count'] for f in test_files),
        'patterns': dict(test_patterns),
        'covered_flows': list(covered_flows)
    }

def classify_test_flow(test_name):
    """Classify test into flow categories"""
    test_lower = test_name.lower()
    
    if any(word in test_lower for word in ['login', 'sign in', 'auth']):
        return 'authentication'
    elif any(word in test_lower for word in ['register', 'signup', 'sign up']):
        return 'registration'
    elif any(word in test_lower for word in ['checkout', 'purchase', 'buy', 'cart']):
        return 'checkout'
    elif any(word in test_lower for word in ['search', 'filter', 'find']):
        return 'search'
    elif any(word in test_lower for word in ['create', 'add', 'new']):
        return 'creation'
    elif any(word in test_lower for word in ['edit', 'update', 'modify']):
        return 'editing'
    elif any(word in test_lower for word in ['delete', 'remove']):
        return 'deletion'
    elif any(word in test_lower for word in ['profile', 'account', 'settings']):
        return 'profile_management'
    elif any(word in test_lower for word in ['upload', 'download', 'file']):
        return 'file_operations'
    elif any(word in test_lower for word in ['error', 'validation', 'invalid']):
        return 'error_handling'
    
    return None

def suggest_missing_coverage(analysis, app_type='general'):
    """Suggest missing test coverage"""
    
    covered = set(analysis['covered_flows'])
    
    # Define comprehensive test flows by app type
    recommended_flows = {
        'general': {
            'authentication', 'registration', 'profile_management',
            'error_handling', 'navigation', 'responsive_design'
        },
        'ecommerce': {
            'authentication', 'registration', 'search', 'filtering',
            'product_details', 'checkout', 'cart_operations',
            'payment', 'order_history', 'profile_management'
        },
        'saas': {
            'authentication', 'registration', 'onboarding',
            'dashboard', 'creation', 'editing', 'deletion',
            'collaboration', 'settings', 'billing'
        },
        'social': {
            'authentication', 'registration', 'profile_management',
            'posting', 'commenting', 'liking', 'sharing',
            'notifications', 'messaging', 'feed'
        }
    }
    
    recommended = recommended_flows.get(app_type, recommended_flows['general'])
    missing = recommended - covered
    
    suggestions = {
        'missing_flows': list(missing),
        'coverage_percentage': (len(covered) / len(recommended) * 100) if recommended else 0,
        'recommendations': []
    }
    
    # Generate specific recommendations
    flow_templates = {
        'authentication': {
            'tests': [
                'should login with valid credentials',
                'should show error for invalid credentials',
                'should logout successfully',
                'should handle password reset flow',
                'should maintain session across page refreshes'
            ],
            'priority': 'critical'
        },
        'registration': {
            'tests': [
                'should register new user with valid data',
                'should validate email format',
                'should enforce password requirements',
                'should prevent duplicate email registration',
                'should send welcome email'
            ],
            'priority': 'critical'
        },
        'checkout': {
            'tests': [
                'should complete checkout with valid payment',
                'should calculate total correctly with discounts',
                'should handle out of stock items',
                'should validate shipping address',
                'should show order confirmation'
            ],
            'priority': 'high'
        },
        'error_handling': {
            'tests': [
                'should handle network failures gracefully',
                'should show validation errors',
                'should handle 404 pages',
                'should handle server errors',
                'should timeout appropriately'
            ],
            'priority': 'high'
        },
        'responsive_design': {
            'tests': [
                'should render correctly on mobile',
                'should render correctly on tablet',
                'should handle orientation changes',
                'should have accessible navigation on mobile'
            ],
            'priority': 'medium'
        }
    }
    
    for flow in missing:
        if flow in flow_templates:
            template = flow_templates[flow]
            suggestions['recommendations'].append({
                'flow': flow,
                'priority': template['priority'],
                'suggested_tests': template['tests']
            })
    
    # Check for edge case coverage
    edge_case_suggestions = []
    
    if analysis['total_tests'] > 0:
        if analysis['total_tests'] < 20:
            edge_case_suggestions.append('Add more edge case tests for existing features')
        
        patterns = analysis['patterns']
        if patterns.get('has_assertions', 0) < patterns.get('uses_playwright', 0):
            edge_case_suggestions.append('Some tests may be missing assertions')
    
    suggestions['edge_case_recommendations'] = edge_case_suggestions
    
    return suggestions

def analyze_page_coverage(test_dir, pages_dir=None):
    """Analyze which pages have test coverage"""
    
    if not pages_dir or not os.path.exists(pages_dir):
        return {'error': 'Pages directory not found'}
    
    # Find all page objects
    page_objects = []
    for root, dirs, files in os.walk(pages_dir):
        for file in files:
            if file.endswith(('.ts', '.js')) and not file.endswith('.test.ts'):
                page_objects.append(os.path.splitext(file)[0])
    
    # Check which pages are tested
    tested_pages = set()
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.endswith(('.spec.ts', '.spec.js')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for page in page_objects:
                            if page in content:
                                tested_pages.add(page)
                except:
                    pass
    
    untested_pages = set(page_objects) - tested_pages
    
    return {
        'total_pages': len(page_objects),
        'tested_pages': list(tested_pages),
        'untested_pages': list(untested_pages),
        'coverage_percentage': (len(tested_pages) / len(page_objects) * 100) if page_objects else 0
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_coverage.py <test_directory> [app_type] [pages_directory]", file=sys.stderr)
        print("\nApp types: general, ecommerce, saas, social", file=sys.stderr)
        sys.exit(1)
    
    test_dir = sys.argv[1]
    app_type = sys.argv[2] if len(sys.argv) > 2 else 'general'
    pages_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not os.path.exists(test_dir):
        print(json.dumps({'error': f'Test directory not found: {test_dir}'}))
        sys.exit(1)
    
    # Analyze tests
    analysis = analyze_test_files(test_dir)
    
    # Suggest missing coverage
    suggestions = suggest_missing_coverage(analysis, app_type)
    
    # Analyze page coverage if pages directory provided
    page_coverage = None
    if pages_dir:
        page_coverage = analyze_page_coverage(test_dir, pages_dir)
    
    result = {
        'analysis': analysis,
        'suggestions': suggestions,
        'page_coverage': page_coverage
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
