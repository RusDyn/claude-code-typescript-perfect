#!/usr/bin/env python3
"""
GitHub Issue Analyzer

Analyzes a GitHub issue to extract requirements, acceptance criteria,
technical context, and implementation hints.
"""

import sys
import json
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class IssueAnalysis:
    """Complete analysis of a GitHub issue"""
    issue_number: int
    title: str
    type: str  # 'bug', 'feature', 'enhancement'
    description: str
    
    # Bug-specific
    steps_to_reproduce: List[str]
    expected_behavior: str
    actual_behavior: str
    environment: Dict[str, str]
    
    # Feature-specific
    user_stories: List[str]
    use_cases: List[str]
    
    # Common
    acceptance_criteria: List[str]
    technical_details: List[str]
    affected_files: List[str]
    related_issues: List[int]
    labels: List[str]
    
    # Implementation hints
    proposed_solution: str
    implementation_hints: List[str]
    testing_requirements: List[str]
    
    def __post_init__(self):
        # Initialize empty lists if None
        for field in ['steps_to_reproduce', 'user_stories', 'use_cases',
                     'acceptance_criteria', 'technical_details', 'affected_files',
                     'related_issues', 'labels', 'implementation_hints',
                     'testing_requirements']:
            if getattr(self, field) is None:
                setattr(self, field, [])
        
        if self.environment is None:
            self.environment = {}

class IssueAnalyzer:
    """Analyze GitHub issues to extract actionable information"""
    
    @staticmethod
    def analyze(issue: Dict[str, Any]) -> IssueAnalysis:
        """
        Analyze a GitHub issue and extract all relevant information
        for implementation.
        """
        body = issue.get('body', '')
        title = issue.get('title', '')
        labels = [label.get('name', '') for label in issue.get('labels', [])]
        
        # Determine issue type
        issue_type = IssueAnalyzer._determine_type(labels, body, title)
        
        # Extract sections from markdown body
        sections = IssueAnalyzer._parse_markdown_sections(body)
        
        # Extract specific information based on type
        if issue_type == 'bug':
            analysis = IssueAnalyzer._analyze_bug(issue, sections)
        elif issue_type == 'feature':
            analysis = IssueAnalyzer._analyze_feature(issue, sections)
        else:
            analysis = IssueAnalyzer._analyze_enhancement(issue, sections)
        
        return analysis
    
    @staticmethod
    def _determine_type(labels: List[str], body: str, title: str) -> str:
        """Determine if issue is bug, feature, or enhancement"""
        label_str = ' '.join(labels).lower()
        text = (body + ' ' + title).lower()
        
        if 'bug' in label_str or any(word in text for word in ['error', 'crash', 'broken', 'fail']):
            return 'bug'
        elif 'feature' in label_str or any(word in text for word in ['add', 'new feature', 'implement']):
            return 'feature'
        else:
            return 'enhancement'
    
    @staticmethod
    def _parse_markdown_sections(body: str) -> Dict[str, str]:
        """Parse markdown body into sections"""
        sections = {}
        current_section = 'description'
        current_content = []
        
        lines = body.split('\n')
        for line in lines:
            # Check if this is a header (## or ###)
            if line.strip().startswith('#'):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                section_name = line.strip('#').strip().lower()
                current_section = section_name
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    @staticmethod
    def _analyze_bug(issue: Dict[str, Any], sections: Dict[str, str]) -> IssueAnalysis:
        """Analyze a bug report"""
        body = issue.get('body', '')
        
        # Extract steps to reproduce
        steps = IssueAnalyzer._extract_numbered_list(
            sections.get('steps to reproduce', '') or 
            sections.get('reproduction steps', '') or
            sections.get('how to reproduce', '')
        )
        
        # Extract expected/actual behavior
        expected = (sections.get('expected behavior', '') or 
                   sections.get('expected', ''))
        actual = (sections.get('actual behavior', '') or 
                 sections.get('actual', ''))
        
        # Extract environment
        env_text = sections.get('environment', '')
        environment = IssueAnalyzer._parse_environment(env_text)
        
        # Extract technical details
        tech_details = IssueAnalyzer._extract_technical_details(body)
        
        # Extract acceptance criteria
        criteria = IssueAnalyzer._extract_acceptance_criteria(sections)
        
        return IssueAnalysis(
            issue_number=issue.get('number', 0),
            title=issue.get('title', ''),
            type='bug',
            description=sections.get('description', body.split('\n')[0]),
            steps_to_reproduce=steps,
            expected_behavior=expected,
            actual_behavior=actual,
            environment=environment,
            user_stories=[],
            use_cases=[],
            acceptance_criteria=criteria or [
                'Bug is fixed and no longer reproducible',
                'No regression in related functionality',
                'Tests added to prevent recurrence'
            ],
            technical_details=tech_details,
            affected_files=IssueAnalyzer._extract_file_paths(body),
            related_issues=IssueAnalyzer._extract_related_issues(body),
            labels=[label.get('name', '') for label in issue.get('labels', [])],
            proposed_solution=sections.get('proposed solution', ''),
            implementation_hints=IssueAnalyzer._extract_implementation_hints(body),
            testing_requirements=[
                'Add unit test reproducing the bug',
                'Verify fix resolves the issue',
                'Test edge cases',
                'Verify no regression'
            ]
        )
    
    @staticmethod
    def _analyze_feature(issue: Dict[str, Any], sections: Dict[str, str]) -> IssueAnalysis:
        """Analyze a feature request"""
        body = issue.get('body', '')
        
        # Extract user stories
        user_stories = IssueAnalyzer._extract_user_stories(body)
        
        # Extract use cases
        use_cases = IssueAnalyzer._extract_use_cases(sections)
        
        # Extract acceptance criteria
        criteria = IssueAnalyzer._extract_acceptance_criteria(sections)
        
        return IssueAnalysis(
            issue_number=issue.get('number', 0),
            title=issue.get('title', ''),
            type='feature',
            description=sections.get('description', '') or sections.get('feature description', ''),
            steps_to_reproduce=[],
            expected_behavior='',
            actual_behavior='',
            environment={},
            user_stories=user_stories,
            use_cases=use_cases,
            acceptance_criteria=criteria,
            technical_details=IssueAnalyzer._extract_technical_details(body),
            affected_files=IssueAnalyzer._extract_file_paths(body),
            related_issues=IssueAnalyzer._extract_related_issues(body),
            labels=[label.get('name', '') for label in issue.get('labels', [])],
            proposed_solution=sections.get('proposed solution', ''),
            implementation_hints=IssueAnalyzer._extract_implementation_hints(body),
            testing_requirements=[
                'Add unit tests for new functionality',
                'Add integration tests',
                'Test happy path and edge cases',
                'Update documentation'
            ]
        )
    
    @staticmethod
    def _analyze_enhancement(issue: Dict[str, Any], sections: Dict[str, str]) -> IssueAnalysis:
        """Analyze an enhancement request"""
        body = issue.get('body', '')
        
        criteria = IssueAnalyzer._extract_acceptance_criteria(sections)
        
        return IssueAnalysis(
            issue_number=issue.get('number', 0),
            title=issue.get('title', ''),
            type='enhancement',
            description=sections.get('description', '') or sections.get('enhancement description', ''),
            steps_to_reproduce=[],
            expected_behavior=sections.get('proposed behavior', ''),
            actual_behavior=sections.get('current behavior', ''),
            environment={},
            user_stories=[],
            use_cases=[],
            acceptance_criteria=criteria,
            technical_details=IssueAnalyzer._extract_technical_details(body),
            affected_files=IssueAnalyzer._extract_file_paths(body),
            related_issues=IssueAnalyzer._extract_related_issues(body),
            labels=[label.get('name', '') for label in issue.get('labels', [])],
            proposed_solution=sections.get('proposed solution', ''),
            implementation_hints=IssueAnalyzer._extract_implementation_hints(body),
            testing_requirements=[
                'Verify improvement is measurable',
                'Test performance/UX improvement',
                'No regression in existing functionality'
            ]
        )
    
    @staticmethod
    def _extract_numbered_list(text: str) -> List[str]:
        """Extract numbered list items"""
        items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Match: 1. or 1) or - or *
            match = re.match(r'^(\d+[\.\)]|\-|\*)\s+(.+)$', line)
            if match:
                items.append(match.group(2))
        
        return items
    
    @staticmethod
    def _parse_environment(text: str) -> Dict[str, str]:
        """Parse environment information"""
        env = {}
        lines = text.split('\n')
        
        for line in lines:
            # Match: - OS: Windows or OS: Windows
            match = re.match(r'^[\-\*]?\s*([^:]+):\s*(.+)$', line.strip())
            if match:
                key = match.group(1).strip().lower()
                value = match.group(2).strip()
                env[key] = value
        
        return env
    
    @staticmethod
    def _extract_technical_details(text: str) -> List[str]:
        """Extract technical details from issue"""
        details = []
        
        # Look for code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', text)
        if code_blocks:
            details.append(f'Contains {len(code_blocks)} code block(s)')
        
        # Look for error messages
        errors = re.findall(r'error[:\s]+([^\n]+)', text, re.IGNORECASE)
        for error in errors[:3]:  # Limit to first 3
            details.append(f'Error: {error.strip()}')
        
        # Look for stack traces
        if 'stack trace' in text.lower() or 'stacktrace' in text.lower():
            details.append('Contains stack trace')
        
        # Look for technical keywords
        tech_keywords = ['api', 'database', 'query', 'performance', 'memory', 
                        'timeout', 'race condition', 'deadlock']
        found_keywords = [kw for kw in tech_keywords if kw in text.lower()]
        if found_keywords:
            details.append(f'Technical areas: {", ".join(found_keywords)}')
        
        return details
    
    @staticmethod
    def _extract_file_paths(text: str) -> List[str]:
        """Extract file paths mentioned in issue"""
        # Match common file path patterns
        patterns = [
            r'`([a-zA-Z0-9_\-/\.]+\.[a-zA-Z0-9]+)`',  # `path/to/file.ext`
            r'\bsrc/[a-zA-Z0-9_\-/\.]+',  # src/path/to/file
            r'\blib/[a-zA-Z0-9_\-/\.]+',  # lib/path/to/file
        ]
        
        files = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            files.extend(matches)
        
        return list(set(files))  # Remove duplicates
    
    @staticmethod
    def _extract_related_issues(text: str) -> List[int]:
        """Extract related issue numbers"""
        # Match #123 or GH-123 or issue 123
        patterns = [
            r'#(\d+)',
            r'GH-(\d+)',
            r'issue\s+(\d+)',
        ]
        
        issues = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            issues.extend([int(m) for m in matches])
        
        return list(set(issues))  # Remove duplicates
    
    @staticmethod
    def _extract_user_stories(text: str) -> List[str]:
        """Extract user stories (As a... I want... so that...)"""
        # Match: As a [user], I want [action] so that [benefit]
        pattern = r'[Aa]s\s+a\s+([^,]+),\s+I\s+want\s+([^,]+)(?:,?\s+so\s+that\s+(.+))?'
        matches = re.findall(pattern, text)
        
        stories = []
        for match in matches:
            user, want, benefit = match
            story = f"As a {user.strip()}, I want {want.strip()}"
            if benefit:
                story += f" so that {benefit.strip()}"
            stories.append(story)
        
        return stories
    
    @staticmethod
    def _extract_use_cases(sections: Dict[str, str]) -> List[str]:
        """Extract use cases"""
        use_case_text = sections.get('use case', '') or sections.get('use cases', '')
        if not use_case_text:
            return []
        
        return IssueAnalyzer._extract_numbered_list(use_case_text)
    
    @staticmethod
    def _extract_acceptance_criteria(sections: Dict[str, str]) -> List[str]:
        """Extract acceptance criteria"""
        criteria_text = (sections.get('acceptance criteria', '') or 
                        sections.get('definition of done', '') or
                        sections.get('success criteria', ''))
        
        if not criteria_text:
            return []
        
        # Look for checkbox items: - [ ] or - [x]
        checkbox_pattern = r'^\s*-\s*\[[ x]\]\s*(.+)$'
        criteria = []
        
        for line in criteria_text.split('\n'):
            match = re.match(checkbox_pattern, line)
            if match:
                criteria.append(match.group(1).strip())
            elif line.strip() and not line.strip().startswith('#'):
                # Also include numbered/bulleted lists
                item = IssueAnalyzer._extract_numbered_list(line)
                if item:
                    criteria.extend(item)
        
        return criteria
    
    @staticmethod
    def _extract_implementation_hints(text: str) -> List[str]:
        """Extract implementation hints from issue"""
        hints = []
        
        # Look for suggestion keywords
        hint_indicators = [
            'suggest', 'recommend', 'should use', 'could use',
            'implementation', 'approach', 'solution'
        ]
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in hint_indicators):
                clean_line = line.strip('- *#').strip()
                if len(clean_line) > 10:  # Ignore very short lines
                    hints.append(clean_line)
        
        return hints[:5]  # Limit to 5 hints

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_issue.py '<issue_json>'")
        print("\nExpects GitHub issue JSON format")
        print("\nExample:")
        example = {
            "number": 123,
            "title": "Fix login button not responding",
            "body": "## Description\nButton doesn't work...",
            "labels": [{"name": "bug"}]
        }
        print(f"  python analyze_issue.py '{json.dumps(example)}'")
        sys.exit(1)
    
    issue = json.loads(sys.argv[1])
    analysis = IssueAnalyzer.analyze(issue)
    
    print(json.dumps(asdict(analysis), indent=2))

if __name__ == '__main__':
    main()
