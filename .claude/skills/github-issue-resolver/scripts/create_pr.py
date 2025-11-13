#!/usr/bin/env python3
"""
GitHub Pull Request Creator

Creates pull requests via GitHub API with proper formatting and linking to issues.
"""

import sys
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def create_pull_request(owner, repo, title, body, head_branch, base_branch='main', token=None):
    """
    Create a pull request via GitHub API
    
    Args:
        owner: Repository owner
        repo: Repository name
        title: PR title
        body: PR description
        head_branch: Source branch (your changes)
        base_branch: Target branch (default: main)
        token: GitHub personal access token
    """
    if not token:
        return {'error': 'GitHub token required. Provide via GITHUB_TOKEN env var or as argument'}
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    
    data = {
        'title': title,
        'body': body,
        'head': head_branch,
        'base': base_branch,
        'maintainer_can_modify': True
    }
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}',
        'User-Agent': 'GitHub-Issue-Resolver-Skill',
        'Content-Type': 'application/json'
    }
    
    try:
        request = Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urlopen(request) as response:
            pr_data = json.loads(response.read().decode())
            return {
                'success': True,
                'pr_number': pr_data['number'],
                'pr_url': pr_data['html_url'],
                'pr_api_url': pr_data['url'],
                'state': pr_data['state']
            }
    
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ''
        try:
            error_data = json.loads(error_body)
            error_message = error_data.get('message', str(e))
        except:
            error_message = str(e)
        
        return {
            'error': f'HTTP Error {e.code}: {error_message}',
            'details': error_body
        }
    
    except URLError as e:
        return {'error': f'Network error: {e.reason}'}

def generate_pr_body(issue_number, summary, changes, testing=None, notes=None):
    """
    Generate a well-formatted PR body
    
    Args:
        issue_number: Issue this PR fixes/implements
        summary: Brief summary of changes
        changes: List of changes made
        testing: How the changes were tested
        notes: Additional notes
    """
    body = f"## Description\n\n{summary}\n\n"
    
    if issue_number:
        body += f"Fixes #{issue_number}\n\n"
    
    if changes:
        body += "## Changes\n\n"
        for change in changes:
            body += f"- {change}\n"
        body += "\n"
    
    if testing:
        body += "## Testing\n\n"
        if isinstance(testing, list):
            for test in testing:
                body += f"- {test}\n"
        else:
            body += f"{testing}\n"
        body += "\n"
    
    if notes:
        body += "## Notes\n\n"
        body += f"{notes}\n\n"
    
    body += "## Checklist\n\n"
    body += "- [x] Code follows project style guidelines\n"
    body += "- [x] Self-review completed\n"
    body += "- [x] Comments added for complex logic\n"
    body += "- [x] Documentation updated if needed\n"
    body += "- [x] No new warnings generated\n"
    body += "- [x] Tests added/updated\n"
    body += "- [x] All tests passing\n"
    
    return body

def add_pr_comment(owner, repo, pr_number, comment, token):
    """Add a comment to a pull request"""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}',
        'User-Agent': 'GitHub-Issue-Resolver-Skill',
        'Content-Type': 'application/json'
    }
    
    data = {'body': comment}
    
    try:
        request = Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urlopen(request) as response:
            return {'success': True}
    
    except Exception as e:
        return {'error': str(e)}

def request_review(owner, repo, pr_number, reviewers, token):
    """Request review from specific users"""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}',
        'User-Agent': 'GitHub-Issue-Resolver-Skill',
        'Content-Type': 'application/json'
    }
    
    data = {'reviewers': reviewers}
    
    try:
        request = Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urlopen(request) as response:
            return {'success': True}
    
    except Exception as e:
        return {'error': str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_pr.py '<pr_config_json>'", file=sys.stderr)
        print("\nExample config:", file=sys.stderr)
        example = {
            'owner': 'username',
            'repo': 'repository',
            'title': 'Fix bug in authentication',
            'head_branch': 'fix/auth-bug',
            'base_branch': 'main',
            'issue_number': 123,
            'summary': 'Fixed authentication bug that caused...',
            'changes': [
                'Updated auth.js to handle edge case',
                'Added unit tests for authentication',
                'Updated documentation'
            ],
            'testing': [
                'Ran full test suite',
                'Manually tested auth flow',
                'Tested edge cases'
            ],
            'token': 'ghp_yourtoken'
        }
        print(json.dumps(example, indent=2), file=sys.stderr)
        sys.exit(1)
    
    config = json.loads(sys.argv[1])
    
    # Get token from config or environment
    token = config.get('token') or os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print(json.dumps({
            'error': 'GitHub token required',
            'hint': 'Provide token in config or set GITHUB_TOKEN environment variable'
        }, indent=2))
        sys.exit(1)
    
    # Generate PR body
    pr_body = generate_pr_body(
        issue_number=config.get('issue_number'),
        summary=config.get('summary', config.get('body', '')),
        changes=config.get('changes', []),
        testing=config.get('testing'),
        notes=config.get('notes')
    )
    
    # Create PR
    result = create_pull_request(
        owner=config['owner'],
        repo=config['repo'],
        title=config['title'],
        body=pr_body,
        head_branch=config['head_branch'],
        base_branch=config.get('base_branch', 'main'),
        token=token
    )
    
    if result.get('success'):
        # Add comment if provided
        if config.get('comment'):
            add_pr_comment(
                config['owner'],
                config['repo'],
                result['pr_number'],
                config['comment'],
                token
            )
        
        # Request reviewers if provided
        if config.get('reviewers'):
            request_review(
                config['owner'],
                config['repo'],
                result['pr_number'],
                config['reviewers'],
                token
            )
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
