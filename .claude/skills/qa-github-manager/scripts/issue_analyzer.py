#!/usr/bin/env python3
"""
Issue Analyzer

Analyzes feedback items and breaks them down into atomic, well-scoped GitHub issues.
Ensures each issue is small enough to be actionable and can be completed independently.
"""

import sys
import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class GitHubIssue:
    """Represents a well-formed GitHub issue"""
    title: str
    body: str
    labels: List[str]
    assignees: List[str] = None
    milestone: str = None
    priority: str = 'medium'  # critical, high, medium, low
    estimated_effort: str = 'medium'  # small, medium, large
    
    def __post_init__(self):
        if self.assignees is None:
            self.assignees = []

class IssueAnalyzer:
    """Analyze and break down feedback into atomic issues"""
    
    @staticmethod
    def analyze_feedback_item(item: Dict[str, Any]) -> List[GitHubIssue]:
        """
        Analyze a feedback item and break it down into atomic issues.
        One feedback item may result in multiple GitHub issues.
        """
        issues = []
        
        # Check if the feedback is complex and needs to be split
        if IssueAnalyzer._is_complex(item):
            issues.extend(IssueAnalyzer._split_complex_item(item))
        else:
            issues.append(IssueAnalyzer._create_single_issue(item))
        
        return issues
    
    @staticmethod
    def _is_complex(item: Dict[str, Any]) -> bool:
        """Determine if a feedback item is complex and should be split"""
        description = item.get('description', '')
        
        # Multiple different actions mentioned
        action_words = ['add', 'remove', 'update', 'fix', 'change', 'modify', 'improve']
        action_count = sum(1 for word in action_words if word in description.lower())
        
        if action_count > 2:
            return True
        
        # Multiple components mentioned
        if 'and' in description.lower() and len(description.split('and')) > 2:
            return True
        
        # Very long description (likely multiple concerns)
        if len(description) > 500:
            return True
        
        # Multiple sections or bullet points
        if description.count('\n') > 5:
            return True
        
        return False
    
    @staticmethod
    def _split_complex_item(item: Dict[str, Any]) -> List[GitHubIssue]:
        """Split a complex feedback item into multiple atomic issues"""
        issues = []
        description = item.get('description', '')
        
        # Try to split by sentences or paragraphs
        sections = [s.strip() for s in description.split('\n') if s.strip()]
        
        if len(sections) == 1:
            # Split by sentences if it's all in one paragraph
            sentences = [s.strip() + '.' for s in description.split('.') if s.strip()]
            sections = IssueAnalyzer._group_related_sentences(sentences)
        
        base_labels = IssueAnalyzer._get_labels(item)
        
        for i, section in enumerate(sections):
            if not section:
                continue
            
            # Create a sub-issue
            issue = GitHubIssue(
                title=IssueAnalyzer._generate_title(section, item.get('title', '')),
                body=IssueAnalyzer._format_issue_body(
                    section,
                    item.get('item_type', 'enhancement'),
                    item.get('steps_to_reproduce', []),
                    item.get('expected_behavior', ''),
                    item.get('actual_behavior', '')
                ),
                labels=base_labels + [f"split-{i+1}"],
                priority=item.get('severity', 'medium'),
                estimated_effort='small'  # Split issues should be small
            )
            issues.append(issue)
        
        return issues
    
    @staticmethod
    def _group_related_sentences(sentences: List[str]) -> List[str]:
        """Group related sentences together"""
        # Simple grouping: every 2-3 sentences that seem related
        groups = []
        current_group = []
        
        for sentence in sentences:
            current_group.append(sentence)
            
            # Start new group after 2-3 sentences or when topic seems to change
            if len(current_group) >= 3 or IssueAnalyzer._is_topic_change(current_group):
                groups.append(' '.join(current_group))
                current_group = []
        
        if current_group:
            groups.append(' '.join(current_group))
        
        return groups
    
    @staticmethod
    def _is_topic_change(sentences: List[str]) -> bool:
        """Check if the last sentence indicates a topic change"""
        if len(sentences) < 2:
            return False
        
        last = sentences[-1].lower()
        
        # Topic change indicators
        indicators = ['also', 'additionally', 'furthermore', 'another', 'separately']
        return any(indicator in last for indicator in indicators)
    
    @staticmethod
    def _create_single_issue(item: Dict[str, Any]) -> GitHubIssue:
        """Create a single GitHub issue from a feedback item"""
        return GitHubIssue(
            title=IssueAnalyzer._generate_title(
                item.get('description', ''),
                item.get('title', '')
            ),
            body=IssueAnalyzer._format_issue_body(
                item.get('description', ''),
                item.get('item_type', 'bug'),
                item.get('steps_to_reproduce', []),
                item.get('expected_behavior', ''),
                item.get('actual_behavior', '')
            ),
            labels=IssueAnalyzer._get_labels(item),
            priority=item.get('severity', 'medium'),
            estimated_effort=IssueAnalyzer._estimate_effort(item)
        )
    
    @staticmethod
    def _generate_title(description: str, existing_title: str = '') -> str:
        """Generate a concise, action-oriented title"""
        if existing_title and len(existing_title) <= 100:
            return existing_title
        
        # Extract first sentence
        first_sentence = description.split('.')[0].strip()
        
        # Make it action-oriented
        if len(first_sentence) > 100:
            first_sentence = first_sentence[:97] + '...'
        
        return first_sentence
    
    @staticmethod
    def _format_issue_body(description: str, item_type: str, steps: List[str],
                          expected: str, actual: str) -> str:
        """Format issue body according to GitHub best practices"""
        
        if item_type == 'bug':
            body = f"""## Description
{description}

## Steps to Reproduce
"""
            if steps:
                for i, step in enumerate(steps, 1):
                    body += f"{i}. {step}\n"
            else:
                body += "_No steps provided_\n"
            
            body += f"""
## Expected Behavior
{expected if expected else '_Not specified_'}

## Actual Behavior
{actual if actual else '_See description_'}

## Environment
_To be filled: OS, Browser, Version, etc._
"""
        
        elif item_type == 'feature':
            body = f"""## Feature Request
{description}

## Use Case
_Why is this feature needed? What problem does it solve?_

## Proposed Solution
_How should this feature work?_

## Alternatives Considered
_What other approaches were considered?_

## Additional Context
_Any mockups, examples, or additional information_
"""
        
        else:  # enhancement
            body = f"""## Enhancement Description
{description}

## Current Behavior
{actual if actual else '_Describe current state_'}

## Proposed Behavior
{expected if expected else '_Describe desired state_'}

## Benefits
_What will this improvement enable or make easier?_
"""
        
        return body
    
    @staticmethod
    def _get_labels(item: Dict[str, Any]) -> List[str]:
        """Determine appropriate labels for the issue"""
        labels = []
        
        # Type label
        item_type = item.get('item_type', 'bug')
        labels.append(item_type)
        
        # Severity/Priority label
        severity = item.get('severity', 'medium')
        if severity in ['critical', 'high']:
            labels.append(f'priority-{severity}')
        
        # Component label if specified
        component = item.get('component', '')
        if component and component != 'general':
            labels.append(f'component-{component}')
        
        # Add "needs-triage" for initial review
        labels.append('needs-triage')
        
        return labels
    
    @staticmethod
    def _estimate_effort(item: Dict[str, Any]) -> str:
        """Estimate the effort required"""
        description = item.get('description', '')
        item_type = item.get('item_type', 'bug')
        
        # Simple heuristics
        if item_type == 'feature':
            if len(description) > 300:
                return 'large'
            elif len(description) > 100:
                return 'medium'
            else:
                return 'small'
        
        elif item_type == 'bug':
            severity = item.get('severity', 'medium')
            if severity == 'critical':
                return 'medium'  # Critical bugs need attention but often quick to fix
            else:
                return 'small'
        
        return 'small'

def main():
    if len(sys.argv) < 2:
        print("Usage: python issue_analyzer.py '<feedback_item_json>'")
        print("\nExpects JSON from parse_feedback.py")
        print("\nExample:")
        example = {
            'description': 'Login button is broken',
            'item_type': 'bug',
            'severity': 'high',
            'steps_to_reproduce': ['Go to /login', 'Click login button'],
            'expected_behavior': 'Should redirect to dashboard',
            'actual_behavior': 'Nothing happens'
        }
        print(f"  python issue_analyzer.py '{json.dumps(example)}'")
        sys.exit(1)
    
    item = json.loads(sys.argv[1])
    issues = IssueAnalyzer.analyze_feedback_item(item)
    
    result = {
        'total_issues': len(issues),
        'issues': [asdict(issue) for issue in issues]
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
