#!/usr/bin/env python3
"""
PR Formatter

Generates well-formatted pull request descriptions that properly
link to issues and provide complete context.
"""

import sys
import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class PRDescription:
    """Pull request description"""
    title: str
    body: str
    closes_issue: int
    type: str  # 'fix', 'feat', 'refactor', 'docs', 'test', 'chore'

class PRFormatter:
    """Format pull request descriptions"""
    
    @staticmethod
    def create_pr_description(
        issue_analysis: Dict[str, Any],
        implementation_plan: Dict[str, Any],
        changes_summary: str = ""
    ) -> PRDescription:
        """
        Create a comprehensive PR description.
        
        Args:
            issue_analysis: Output from analyze_issue.py
            implementation_plan: Output from implementation_planner.py
            changes_summary: Brief summary of what was changed
        """
        issue_type = issue_analysis.get('type', 'bug')
        issue_number = issue_analysis.get('issue_number', 0)
        title = PRFormatter._generate_title(issue_analysis)
        
        body = PRFormatter._generate_body(
            issue_analysis,
            implementation_plan,
            changes_summary
        )
        
        # Determine PR type for conventional commits
        pr_type = PRFormatter._determine_pr_type(issue_type)
        
        return PRDescription(
            title=title,
            body=body,
            closes_issue=issue_number,
            type=pr_type
        )
    
    @staticmethod
    def _generate_title(analysis: Dict[str, Any]) -> str:
        """Generate PR title following conventional commits"""
        issue_type = analysis.get('type', 'bug')
        issue_number = analysis.get('issue_number', 0)
        title = analysis.get('title', 'Update')
        
        # Map issue type to conventional commit type
        type_map = {
            'bug': 'fix',
            'feature': 'feat',
            'enhancement': 'refactor'
        }
        
        commit_type = type_map.get(issue_type, 'fix')
        
        # Extract component from labels if present
        labels = analysis.get('labels', [])
        component = None
        for label in labels:
            if label.startswith('component-'):
                component = label.replace('component-', '')
                break
        
        # Format: type(component): description (#issue)
        if component:
            return f"{commit_type}({component}): {title} (#{issue_number})"
        else:
            return f"{commit_type}: {title} (#{issue_number})"
    
    @staticmethod
    def _determine_pr_type(issue_type: str) -> str:
        """Determine PR type"""
        type_map = {
            'bug': 'fix',
            'feature': 'feat',
            'enhancement': 'refactor'
        }
        return type_map.get(issue_type, 'fix')
    
    @staticmethod
    def _generate_body(
        analysis: Dict[str, Any],
        plan: Dict[str, Any],
        changes: str
    ) -> str:
        """Generate PR body"""
        issue_number = analysis.get('issue_number', 0)
        issue_type = analysis.get('type', 'bug')
        
        body = f"## Description\n\n"
        body += f"Closes #{issue_number}\n\n"
        
        # Add type-specific content
        if issue_type == 'bug':
            body += PRFormatter._bug_fix_section(analysis, changes)
        elif issue_type == 'feature':
            body += PRFormatter._feature_section(analysis, changes)
        else:
            body += PRFormatter._enhancement_section(analysis, changes)
        
        # Add changes summary
        if changes:
            body += f"## Changes Made\n\n{changes}\n\n"
        
        # Add implementation details from plan
        body += PRFormatter._implementation_section(plan)
        
        # Add testing section
        body += PRFormatter._testing_section(analysis, plan)
        
        # Add checklist
        body += PRFormatter._checklist_section(issue_type)
        
        return body
    
    @staticmethod
    def _bug_fix_section(analysis: Dict[str, Any], changes: str) -> str:
        """Generate bug fix specific section"""
        section = "### Bug Fix\n\n"
        
        # Problem
        section += "**Problem:**\n"
        if analysis.get('actual_behavior'):
            section += f"{analysis['actual_behavior']}\n\n"
        else:
            section += f"{analysis.get('description', 'Bug described in issue')}\n\n"
        
        # Solution
        section += "**Solution:**\n"
        if analysis.get('proposed_solution'):
            section += f"{analysis['proposed_solution']}\n\n"
        elif changes:
            section += f"{changes}\n\n"
        else:
            section += "[Describe the fix here]\n\n"
        
        # Root cause if available
        if analysis.get('technical_details'):
            section += "**Root Cause:**\n"
            for detail in analysis['technical_details']:
                section += f"- {detail}\n"
            section += "\n"
        
        return section
    
    @staticmethod
    def _feature_section(analysis: Dict[str, Any], changes: str) -> str:
        """Generate feature specific section"""
        section = "### New Feature\n\n"
        
        # What was added
        section += "**What:**\n"
        section += f"{analysis.get('description', 'Feature described in issue')}\n\n"
        
        # Why (user stories)
        user_stories = analysis.get('user_stories', [])
        if user_stories:
            section += "**Why:**\n"
            for story in user_stories:
                section += f"- {story}\n"
            section += "\n"
        
        # How (implementation)
        if changes:
            section += "**How:**\n"
            section += f"{changes}\n\n"
        
        return section
    
    @staticmethod
    def _enhancement_section(analysis: Dict[str, Any], changes: str) -> str:
        """Generate enhancement specific section"""
        section = "### Enhancement\n\n"
        
        # Before
        if analysis.get('actual_behavior'):
            section += "**Before:**\n"
            section += f"{analysis['actual_behavior']}\n\n"
        
        # After
        if analysis.get('expected_behavior'):
            section += "**After:**\n"
            section += f"{analysis['expected_behavior']}\n\n"
        
        # Benefits
        if changes:
            section += "**Benefits:**\n"
            section += f"{changes}\n\n"
        
        return section
    
    @staticmethod
    def _implementation_section(plan: Dict[str, Any]) -> str:
        """Generate implementation details section"""
        section = "## Implementation Details\n\n"
        
        steps = plan.get('steps', [])
        if not steps:
            section += "[Implementation steps]\n\n"
            return section
        
        # List key steps
        for step in steps:
            if step.get('files_to_modify'):
                section += f"- **{step['title']}:** "
                section += f"{step.get('description', '')}\n"
        
        section += "\n"
        
        # Files modified
        all_files = set()
        for step in steps:
            for file in step.get('files_to_modify', []):
                if not file.startswith('['):  # Skip placeholder files
                    all_files.add(file)
        
        if all_files:
            section += "**Files Modified:**\n"
            for file in sorted(all_files):
                section += f"- `{file}`\n"
            section += "\n"
        
        return section
    
    @staticmethod
    def _testing_section(analysis: Dict[str, Any], plan: Dict[str, Any]) -> str:
        """Generate testing section"""
        section = "## Testing\n\n"
        
        # Testing strategy
        strategy = plan.get('testing_strategy', '')
        if strategy:
            section += f"{strategy}\n\n"
        
        # Test coverage
        section += "**Tests Added/Modified:**\n"
        section += "- [ ] Unit tests\n"
        section += "- [ ] Integration tests\n"
        
        # Type-specific tests
        issue_type = analysis.get('type', 'bug')
        if issue_type == 'bug':
            section += "- [ ] Regression test for bug\n"
        elif issue_type == 'feature':
            section += "- [ ] Feature acceptance tests\n"
        
        section += "\n"
        
        # Verification
        section += "**Verified:**\n"
        
        criteria = analysis.get('acceptance_criteria', [])
        if criteria:
            for criterion in criteria:
                section += f"- [ ] {criterion}\n"
        else:
            section += "- [ ] All acceptance criteria met\n"
            section += "- [ ] No regression in existing functionality\n"
        
        section += "\n"
        
        return section
    
    @staticmethod
    def _checklist_section(issue_type: str) -> str:
        """Generate PR checklist"""
        section = "## Checklist\n\n"
        
        # Common items
        section += "- [ ] Code follows project style guidelines\n"
        section += "- [ ] Self-review completed\n"
        section += "- [ ] Comments added for complex logic\n"
        section += "- [ ] Tests added/updated\n"
        section += "- [ ] All tests passing\n"
        section += "- [ ] No new warnings\n"
        
        # Type-specific items
        if issue_type == 'feature':
            section += "- [ ] Documentation updated\n"
            section += "- [ ] API changes documented\n"
        elif issue_type == 'bug':
            section += "- [ ] Bug fix verified\n"
            section += "- [ ] Regression test added\n"
        
        section += "- [ ] Changelog updated (if applicable)\n"
        
        return section
    
    @staticmethod
    def format_pr(pr: PRDescription) -> str:
        """Format PR for display"""
        output = f"# Pull Request\n\n"
        output += f"**Title:** {pr.title}\n\n"
        output += f"**Type:** {pr.type}\n\n"
        output += f"**Closes:** #{pr.closes_issue}\n\n"
        output += "---\n\n"
        output += pr.body
        return output

def main():
    if len(sys.argv) < 3:
        print("Usage: python pr_formatter.py '<issue_analysis>' '<implementation_plan>' [changes]")
        print("\nExpects JSON from analyze_issue.py and implementation_planner.py")
        sys.exit(1)
    
    issue_analysis = json.loads(sys.argv[1])
    implementation_plan = json.loads(sys.argv[2])
    changes_summary = sys.argv[3] if len(sys.argv) > 3 else ""
    
    pr = PRFormatter.create_pr_description(
        issue_analysis,
        implementation_plan,
        changes_summary
    )
    
    print(json.dumps(asdict(pr), indent=2))
    print("\n\n" + "="*80 + "\n")
    print(PRFormatter.format_pr(pr))

if __name__ == '__main__':
    main()
