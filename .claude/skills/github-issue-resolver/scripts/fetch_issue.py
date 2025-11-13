#!/usr/bin/env python3
"""
GitHub Issue Fetcher

Fetches issue details from GitHub API and analyzes the context needed to resolve it.
"""

import sys
import json
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def parse_github_url(url_or_issue):
    """
    Parse GitHub issue URL or issue reference
    
    Accepts:
    - https://github.com/owner/repo/issues/123
    - owner/repo#123
    - #123 (requires repo context)
    """
    # Full URL
    url_pattern = r'github\.com/([^/]+)/([^/]+)/issues/(\d+)'
    match = re.search(url_pattern, url_or_issue)
    if match:
        return match.group(1), match.group(2), match.group(3)
    
    # Short format: owner/repo#123
    short_pattern = r'([^/]+)/([^#]+)#(\d+)'
    match = re.match(short_pattern, url_or_issue)
    if match:
        return match.group(1), match.group(2), match.group(3)
    
    # Just issue number
    issue_pattern = r'#?(\d+)'
    match = re.match(issue_pattern, url_or_issue)
    if match:
        return None, None, match.group(1)
    
    return None, None, None

def fetch_issue(owner, repo, issue_number, token=None):
    """Fetch issue from GitHub API"""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Issue-Resolver-Skill'
    }
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        if e.code == 404:
            return {'error': f'Issue not found: {owner}/{repo}#{issue_number}'}
        elif e.code == 403:
            return {'error': 'API rate limit exceeded. Provide GitHub token via GITHUB_TOKEN env var'}
        else:
            return {'error': f'HTTP Error {e.code}: {e.reason}'}
    except URLError as e:
        return {'error': f'Network error: {e.reason}'}

def fetch_issue_comments(owner, repo, issue_number, token=None):
    """Fetch comments on the issue"""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Issue-Resolver-Skill'
    }
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        request = Request(url, headers=headers)
        with urlopen(request) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return []

def analyze_issue(issue_data):
    """Analyze issue to determine type and complexity"""
    analysis = {
        'type': 'unknown',
        'labels': issue_data.get('labels', []),
        'complexity': 'medium',
        'has_reproduction': False,
        'has_code_samples': False,
        'mentions_files': [],
        'related_issues': []
    }
    
    # Determine issue type from labels
    label_names = [l['name'].lower() for l in analysis['labels']]
    
    if any('bug' in l for l in label_names):
        analysis['type'] = 'bug'
    elif any('feature' in l or 'enhancement' in l for l in label_names):
        analysis['type'] = 'feature'
    elif any('doc' in l for l in label_names):
        analysis['type'] = 'documentation'
    elif any('test' in l for l in label_names):
        analysis['type'] = 'test'
    
    # Analyze body content
    body = issue_data.get('body', '')
    
    # Check for reproduction steps
    if any(keyword in body.lower() for keyword in ['reproduce', 'steps to', 'minimal example']):
        analysis['has_reproduction'] = True
    
    # Check for code samples
    if '```' in body:
        analysis['has_code_samples'] = True
    
    # Extract mentioned files (simple heuristic)
    file_pattern = r'`([a-zA-Z0-9_\-/\.]+\.[a-zA-Z]+)`'
    analysis['mentions_files'] = list(set(re.findall(file_pattern, body)))
    
    # Find related issue references
    issue_ref_pattern = r'#(\d+)'
    analysis['related_issues'] = list(set(re.findall(issue_ref_pattern, body)))
    
    # Estimate complexity
    if len(body) < 200:
        analysis['complexity'] = 'low'
    elif len(body) > 1000 or len(analysis['related_issues']) > 2:
        analysis['complexity'] = 'high'
    
    return analysis

def format_output(issue_data, comments, analysis):
    """Format the output for Claude"""
    output = {
        'issue': {
            'number': issue_data['number'],
            'title': issue_data['title'],
            'url': issue_data['html_url'],
            'state': issue_data['state'],
            'author': issue_data['user']['login'],
            'created_at': issue_data['created_at'],
            'updated_at': issue_data['updated_at'],
            'body': issue_data['body'],
            'labels': [l['name'] for l in issue_data.get('labels', [])],
            'assignees': [a['login'] for a in issue_data.get('assignees', [])],
            'milestone': issue_data.get('milestone', {}).get('title') if issue_data.get('milestone') else None
        },
        'analysis': analysis,
        'comments': [
            {
                'author': c['user']['login'],
                'body': c['body'],
                'created_at': c['created_at']
            }
            for c in comments[:10]  # Limit to first 10 comments
        ],
        'repository': {
            'owner': issue_data['repository_url'].split('/')[-2],
            'name': issue_data['repository_url'].split('/')[-1]
        }
    }
    
    return output

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_issue.py <issue_url_or_reference> [github_token]", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  python fetch_issue.py https://github.com/owner/repo/issues/123", file=sys.stderr)
        print("  python fetch_issue.py owner/repo#123", file=sys.stderr)
        print("  python fetch_issue.py owner/repo#123 ghp_token123", file=sys.stderr)
        sys.exit(1)
    
    issue_ref = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Try to get token from environment if not provided
    if not token:
        import os
        token = os.environ.get('GITHUB_TOKEN')
    
    owner, repo, issue_number = parse_github_url(issue_ref)
    
    if not owner or not repo or not issue_number:
        print(json.dumps({
            'error': f'Invalid issue reference: {issue_ref}',
            'hint': 'Use format: owner/repo#123 or full GitHub URL'
        }, indent=2))
        sys.exit(1)
    
    # Fetch issue
    issue_data = fetch_issue(owner, repo, issue_number, token)
    
    if 'error' in issue_data:
        print(json.dumps(issue_data, indent=2))
        sys.exit(1)
    
    # Fetch comments
    comments = fetch_issue_comments(owner, repo, issue_number, token)
    
    # Analyze issue
    analysis = analyze_issue(issue_data)
    
    # Format and output
    output = format_output(issue_data, comments, analysis)
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
