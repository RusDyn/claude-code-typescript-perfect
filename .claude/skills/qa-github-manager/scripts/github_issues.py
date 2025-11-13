#!/usr/bin/env python3
"""
GitHub Issues Manager

Search existing GitHub issues, detect duplicates, and create new issues via GitHub API.
Handles reopening closed issues when appropriate.
"""

import sys
import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from difflib import SequenceMatcher

@dataclass
class ExistingIssue:
    """Represents an existing GitHub issue"""
    number: int
    title: str
    body: str
    state: str  # 'open' or 'closed'
    labels: List[str]
    created_at: str
    updated_at: str
    closed_at: Optional[str] = None
    url: str = ''

class GitHubIssuesManager:
    """Manage GitHub issues - search, compare, create, reopen"""
    
    SIMILARITY_THRESHOLD = 0.8  # 80% similarity to consider duplicate
    
    @staticmethod
    def search_similar_issues(new_issue: Dict[str, Any], 
                             existing_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Search for similar issues in the existing issues list.
        Returns list of similar issues with similarity scores.
        """
        similar = []
        new_title = new_issue.get('title', '').lower()
        new_body = new_issue.get('body', '').lower()
        
        for existing in existing_issues:
            ex_title = existing.get('title', '').lower()
            ex_body = existing.get('body', '').lower()
            
            # Calculate similarity
            title_similarity = SequenceMatcher(None, new_title, ex_title).ratio()
            body_similarity = SequenceMatcher(None, new_body, ex_body).ratio()
            
            # Weight title more heavily
            overall_similarity = (title_similarity * 0.7) + (body_similarity * 0.3)
            
            if overall_similarity >= GitHubIssuesManager.SIMILARITY_THRESHOLD:
                similar.append({
                    'issue': existing,
                    'similarity': overall_similarity,
                    'title_match': title_similarity,
                    'body_match': body_similarity
                })
        
        # Sort by similarity
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        return similar
    
    @staticmethod
    def should_reopen(new_issue: Dict[str, Any], 
                     existing_issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine if a closed issue should be reopened instead of creating new one.
        Returns decision with reasoning.
        """
        decision = {
            'should_reopen': False,
            'confidence': 0.0,
            'reasons': []
        }
        
        if existing_issue.get('state') != 'closed':
            decision['reasons'].append('Issue is still open')
            return decision
        
        # Check if it's essentially the same issue
        new_labels = set(new_issue.get('labels', []))
        ex_labels = set(existing_issue.get('labels', []))
        
        # Similar labels suggest same issue
        label_overlap = len(new_labels & ex_labels) / max(len(new_labels | ex_labels), 1)
        
        # Check if the issue is a regression
        new_text = (new_issue.get('title', '') + ' ' + new_issue.get('body', '')).lower()
        regression_keywords = ['regression', 'broke again', 'still not working', 
                              'same issue', 'still happening', 'returned']
        is_regression = any(keyword in new_text for keyword in regression_keywords)
        
        # Recent closure suggests possible regression
        closed_at = existing_issue.get('closed_at', '')
        is_recent = False  # Would need date parsing in real implementation
        
        # Decision logic
        if is_regression:
            decision['should_reopen'] = True
            decision['confidence'] = 0.9
            decision['reasons'].append('Explicit regression mentioned')
        elif label_overlap > 0.7 and is_recent:
            decision['should_reopen'] = True
            decision['confidence'] = 0.8
            decision['reasons'].append('Recently closed with similar characteristics')
        elif label_overlap > 0.5:
            decision['should_reopen'] = True
            decision['confidence'] = 0.6
            decision['reasons'].append('Similar issue type and components')
        else:
            decision['reasons'].append('Appears to be a different issue despite similarity')
        
        return decision
    
    @staticmethod
    def generate_issue_comment(new_feedback: Dict[str, Any]) -> str:
        """Generate a comment for reopening an issue with new feedback"""
        comment = "## Issue Reopened\n\n"
        comment += "This issue is being reopened based on new client feedback.\n\n"
        comment += "### New Feedback\n"
        comment += new_feedback.get('description', '')
        
        if new_feedback.get('steps_to_reproduce'):
            comment += "\n\n### Additional Steps to Reproduce\n"
            for i, step in enumerate(new_feedback['steps_to_reproduce'], 1):
                comment += f"{i}. {step}\n"
        
        return comment
    
    @staticmethod
    def format_github_api_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
        """Format issue for GitHub API POST request"""
        return {
            'title': issue['title'],
            'body': issue['body'],
            'labels': issue.get('labels', []),
            'assignees': issue.get('assignees', []),
            'milestone': issue.get('milestone')
        }
    
    @staticmethod
    def generate_search_queries(issue: Dict[str, Any]) -> List[str]:
        """
        Generate GitHub issue search queries to find related issues.
        GitHub search syntax: https://docs.github.com/en/search-github/searching-on-github
        """
        queries = []
        title = issue.get('title', '')
        labels = issue.get('labels', [])
        
        # Extract key terms from title
        key_terms = [word for word in title.split() 
                    if len(word) > 3 and word.lower() not in 
                    ['the', 'and', 'for', 'with', 'that', 'this']]
        
        # Query 1: Key terms
        if key_terms:
            queries.append(' '.join(key_terms[:3]))
        
        # Query 2: Key terms + labels
        if labels and key_terms:
            label_query = ' '.join([f'label:{label}' for label in labels[:2]])
            queries.append(f"{' '.join(key_terms[:2])} {label_query}")
        
        # Query 3: Just labels (to find related issues)
        if labels:
            queries.append(' '.join([f'label:{label}' for label in labels]))
        
        return queries
    
    @staticmethod
    def deduplicate_issues(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate issues from a list before creating them.
        Useful when multiple feedback items result in similar issues.
        """
        unique = []
        seen_titles = set()
        
        for issue in issues:
            title_lower = issue['title'].lower().strip()
            
            # Check if we've seen a very similar title
            is_duplicate = False
            for seen in seen_titles:
                similarity = SequenceMatcher(None, title_lower, seen).ratio()
                if similarity > 0.9:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(issue)
                seen_titles.add(title_lower)
        
        return unique

def generate_example_workflow():
    """Generate an example workflow for demonstration"""
    return {
        'workflow': [
            {
                'step': 1,
                'action': 'parse_feedback',
                'description': 'Parse client feedback into structured items'
            },
            {
                'step': 2,
                'action': 'analyze_issues',
                'description': 'Break down complex feedback into atomic issues'
            },
            {
                'step': 3,
                'action': 'search_github',
                'description': 'Search for similar existing issues',
                'queries': 'Generated from issue titles and labels'
            },
            {
                'step': 4,
                'action': 'check_duplicates',
                'description': 'Compare new issues with existing ones'
            },
            {
                'step': 5,
                'action': 'decide',
                'description': 'Decide whether to reopen, create new, or skip',
                'options': ['reopen_closed', 'create_new', 'skip_duplicate']
            },
            {
                'step': 6,
                'action': 'execute',
                'description': 'Create issues or reopen with comments'
            }
        ]
    }

def main():
    if len(sys.argv) < 2:
        print("GitHub Issues Manager - Usage Examples\n")
        print("1. Search for similar issues:")
        print("   python github_issues.py search --issue '<issue_json>' --existing '<existing_issues_json>'\n")
        print("2. Check if should reopen:")
        print("   python github_issues.py reopen-check --new '<new_json>' --existing '<existing_json>'\n")
        print("3. Generate search queries:")
        print("   python github_issues.py queries --issue '<issue_json>'\n")
        print("4. View workflow:")
        print("   python github_issues.py workflow\n")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'workflow':
        print(json.dumps(generate_example_workflow(), indent=2))
    
    elif command == 'search':
        # Search for similar issues
        new_issue = json.loads(sys.argv[3])
        existing_issues = json.loads(sys.argv[5])
        
        similar = GitHubIssuesManager.search_similar_issues(new_issue, existing_issues)
        print(json.dumps({'similar_issues': similar}, indent=2))
    
    elif command == 'reopen-check':
        # Check if should reopen
        new_issue = json.loads(sys.argv[3])
        existing_issue = json.loads(sys.argv[5])
        
        decision = GitHubIssuesManager.should_reopen(new_issue, existing_issue)
        print(json.dumps(decision, indent=2))
    
    elif command == 'queries':
        # Generate search queries
        issue = json.loads(sys.argv[3])
        queries = GitHubIssuesManager.generate_search_queries(issue)
        print(json.dumps({'queries': queries}, indent=2))
    
    elif command == 'dedupe':
        # Deduplicate issues
        issues = json.loads(sys.argv[3])
        unique = GitHubIssuesManager.deduplicate_issues(issues)
        print(json.dumps({'original_count': len(issues), 
                         'unique_count': len(unique),
                         'issues': unique}, indent=2))

if __name__ == '__main__':
    main()
