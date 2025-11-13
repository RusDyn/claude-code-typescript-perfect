#!/usr/bin/env python3
"""
Implementation Planner

Creates a detailed, step-by-step implementation plan for a GitHub issue
based on the issue analysis and codebase context.
"""

import sys
import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class ImplementationStep:
    """A single step in the implementation plan"""
    step_number: int
    title: str
    description: str
    files_to_modify: List[str]
    estimated_difficulty: str  # 'easy', 'medium', 'hard'
    dependencies: List[int]  # Step numbers this depends on
    testing_notes: str = ''

@dataclass
class ImplementationPlan:
    """Complete implementation plan"""
    issue_number: int
    issue_title: str
    issue_type: str
    total_steps: int
    estimated_time: str
    steps: List[ImplementationStep]
    testing_strategy: str
    potential_risks: List[str]
    
    def __post_init__(self):
        if self.steps is None:
            self.steps = []
        if self.potential_risks is None:
            self.potential_risks = []

class ImplementationPlanner:
    """Create implementation plans from issue analysis"""
    
    @staticmethod
    def create_plan(analysis: Dict[str, Any], codebase_context: Dict[str, Any] = None) -> ImplementationPlan:
        """
        Create a detailed implementation plan.
        
        Args:
            analysis: Issue analysis from analyze_issue.py
            codebase_context: Optional context about the codebase structure
        """
        issue_type = analysis.get('type', 'bug')
        
        if issue_type == 'bug':
            return ImplementationPlanner._plan_bug_fix(analysis, codebase_context)
        elif issue_type == 'feature':
            return ImplementationPlanner._plan_feature(analysis, codebase_context)
        else:
            return ImplementationPlanner._plan_enhancement(analysis, codebase_context)
    
    @staticmethod
    def _plan_bug_fix(analysis: Dict[str, Any], context: Dict[str, Any] = None) -> ImplementationPlan:
        """Create plan for fixing a bug"""
        steps = []
        
        # Step 1: Reproduce the bug
        steps.append(ImplementationStep(
            step_number=1,
            title="Reproduce the bug",
            description=f"Follow the reproduction steps to confirm the bug exists. {' '.join(analysis.get('steps_to_reproduce', [])[:2])}",
            files_to_modify=[],
            estimated_difficulty='easy',
            dependencies=[],
            testing_notes='Document exact conditions under which bug occurs'
        ))
        
        # Step 2: Identify root cause
        affected_files = analysis.get('affected_files', [])
        steps.append(ImplementationStep(
            step_number=2,
            title="Identify root cause",
            description="Debug and trace the issue to find the root cause. Check error messages, logs, and stack traces.",
            files_to_modify=affected_files if affected_files else ['[files to be determined during debugging]'],
            estimated_difficulty='medium',
            dependencies=[1],
            testing_notes='Add debug logging if needed'
        ))
        
        # Step 3: Write failing test
        steps.append(ImplementationStep(
            step_number=3,
            title="Write failing test",
            description="Create a test that reproduces the bug and fails before the fix.",
            files_to_modify=['tests/test_[component].py'],
            estimated_difficulty='easy',
            dependencies=[2],
            testing_notes='Test should fail consistently before fix'
        ))
        
        # Step 4: Implement fix
        steps.append(ImplementationStep(
            step_number=4,
            title="Implement fix",
            description=f"Fix the bug. {analysis.get('proposed_solution', 'Address the root cause identified in step 2.')}",
            files_to_modify=affected_files if affected_files else ['[determined in step 2]'],
            estimated_difficulty='medium',
            dependencies=[3],
            testing_notes='Fix should make the test from step 3 pass'
        ))
        
        # Step 5: Verify fix
        steps.append(ImplementationStep(
            step_number=5,
            title="Verify fix and test edge cases",
            description=f"Ensure fix resolves the issue. Expected: {analysis.get('expected_behavior', 'Bug no longer occurs')}",
            files_to_modify=[],
            estimated_difficulty='easy',
            dependencies=[4],
            testing_notes='Test all scenarios from steps to reproduce plus edge cases'
        ))
        
        # Step 6: Check for regression
        steps.append(ImplementationStep(
            step_number=6,
            title="Run full test suite",
            description="Verify no regression in existing functionality.",
            files_to_modify=[],
            estimated_difficulty='easy',
            dependencies=[5],
            testing_notes='All existing tests should still pass'
        ))
        
        # Estimate time
        estimated_time = ImplementationPlanner._estimate_time(len(steps), 'bug')
        
        return ImplementationPlan(
            issue_number=analysis.get('issue_number', 0),
            issue_title=analysis.get('title', ''),
            issue_type='bug',
            total_steps=len(steps),
            estimated_time=estimated_time,
            steps=steps,
            testing_strategy="Write test that reproduces bug, implement fix, verify test passes, run full suite",
            potential_risks=[
                "Fix may introduce regression in related functionality",
                "Root cause may be deeper than initially identified",
                "May need to update documentation if behavior changes"
            ]
        )
    
    @staticmethod
    def _plan_feature(analysis: Dict[str, Any], context: Dict[str, Any] = None) -> ImplementationPlan:
        """Create plan for implementing a feature"""
        steps = []
        
        # Step 1: Design the feature
        steps.append(ImplementationStep(
            step_number=1,
            title="Design feature architecture",
            description=f"Plan the implementation approach. {analysis.get('proposed_solution', 'Design interfaces, data structures, and integration points.')}",
            files_to_modify=[],
            estimated_difficulty='medium',
            dependencies=[],
            testing_notes='Document design decisions'
        ))
        
        # Step 2: Write tests first (TDD)
        user_stories = analysis.get('user_stories', [])
        test_description = "Write tests for the feature requirements."
        if user_stories:
            test_description += f" Cover user story: {user_stories[0][:100]}"
        
        steps.append(ImplementationStep(
            step_number=2,
            title="Write tests (TDD)",
            description=test_description,
            files_to_modify=['tests/test_[feature].py'],
            estimated_difficulty='medium',
            dependencies=[1],
            testing_notes='Tests should cover all acceptance criteria'
        ))
        
        # Step 3: Implement core functionality
        affected_files = analysis.get('affected_files', [])
        steps.append(ImplementationStep(
            step_number=3,
            title="Implement core functionality",
            description="Implement the main feature logic to make tests pass.",
            files_to_modify=affected_files if affected_files else ['[new feature files]'],
            estimated_difficulty='hard',
            dependencies=[2],
            testing_notes='Tests from step 2 should start passing'
        ))
        
        # Step 4: Add UI/API integration
        steps.append(ImplementationStep(
            step_number=4,
            title="Integrate with UI/API",
            description="Add user-facing interface or API endpoints.",
            files_to_modify=['src/routes/[feature].ts', 'src/components/[Feature].tsx'],
            estimated_difficulty='medium',
            dependencies=[3],
            testing_notes='Add integration tests for UI/API'
        ))
        
        # Step 5: Handle edge cases
        steps.append(ImplementationStep(
            step_number=5,
            title="Handle edge cases",
            description="Add validation, error handling, and edge case handling.",
            files_to_modify=['[files from step 3]'],
            estimated_difficulty='medium',
            dependencies=[4],
            testing_notes='Add tests for error scenarios and edge cases'
        ))
        
        # Step 6: Documentation
        steps.append(ImplementationStep(
            step_number=6,
            title="Update documentation",
            description="Update README, API docs, and user documentation.",
            files_to_modify=['README.md', 'docs/[feature].md'],
            estimated_difficulty='easy',
            dependencies=[5],
            testing_notes='Verify documentation is clear and accurate'
        ))
        
        # Step 7: Final testing
        steps.append(ImplementationStep(
            step_number=7,
            title="Comprehensive testing",
            description="Test all acceptance criteria and user stories.",
            files_to_modify=[],
            estimated_difficulty='medium',
            dependencies=[6],
            testing_notes='Verify all acceptance criteria are met'
        ))
        
        estimated_time = ImplementationPlanner._estimate_time(len(steps), 'feature')
        
        # Build testing strategy from acceptance criteria
        criteria = analysis.get('acceptance_criteria', [])
        testing_strategy = "Test-driven development approach:\n"
        for i, criterion in enumerate(criteria[:3], 1):
            testing_strategy += f"{i}. {criterion}\n"
        
        return ImplementationPlan(
            issue_number=analysis.get('issue_number', 0),
            issue_title=analysis.get('title', ''),
            issue_type='feature',
            total_steps=len(steps),
            estimated_time=estimated_time,
            steps=steps,
            testing_strategy=testing_strategy.strip(),
            potential_risks=[
                "Feature may have broader scope than initially estimated",
                "May need to refactor existing code for integration",
                "User experience may need iteration based on feedback",
                "May impact performance if not optimized"
            ]
        )
    
    @staticmethod
    def _plan_enhancement(analysis: Dict[str, Any], context: Dict[str, Any] = None) -> ImplementationPlan:
        """Create plan for implementing an enhancement"""
        steps = []
        
        # Step 1: Baseline measurement
        steps.append(ImplementationStep(
            step_number=1,
            title="Establish baseline metrics",
            description=f"Measure current performance/behavior. Current: {analysis.get('actual_behavior', '[to be measured]')}",
            files_to_modify=[],
            estimated_difficulty='easy',
            dependencies=[],
            testing_notes='Document current metrics for comparison'
        ))
        
        # Step 2: Implement improvement
        affected_files = analysis.get('affected_files', [])
        steps.append(ImplementationStep(
            step_number=2,
            title="Implement enhancement",
            description=f"Make the improvement. Goal: {analysis.get('expected_behavior', 'Improve current behavior')}",
            files_to_modify=affected_files if affected_files else ['[files to improve]'],
            estimated_difficulty='medium',
            dependencies=[1],
            testing_notes='Measure improvements incrementally'
        ))
        
        # Step 3: Measure improvement
        steps.append(ImplementationStep(
            step_number=3,
            title="Measure improvement",
            description="Verify enhancement achieves desired improvement.",
            files_to_modify=[],
            estimated_difficulty='easy',
            dependencies=[2],
            testing_notes='Compare against baseline from step 1'
        ))
        
        # Step 4: Add tests
        steps.append(ImplementationStep(
            step_number=4,
            title="Add tests",
            description="Add tests to prevent regression of improvement.",
            files_to_modify=['tests/test_[component].py'],
            estimated_difficulty='medium',
            dependencies=[3],
            testing_notes='Tests should verify improvement is maintained'
        ))
        
        # Step 5: Verify no regression
        steps.append(ImplementationStep(
            step_number=5,
            title="Verify no regression",
            description="Ensure existing functionality still works correctly.",
            files_to_modify=[],
            estimated_difficulty='easy',
            dependencies=[4],
            testing_notes='Run full test suite'
        ))
        
        estimated_time = ImplementationPlanner._estimate_time(len(steps), 'enhancement')
        
        return ImplementationPlan(
            issue_number=analysis.get('issue_number', 0),
            issue_title=analysis.get('title', ''),
            issue_type='enhancement',
            total_steps=len(steps),
            estimated_time=estimated_time,
            steps=steps,
            testing_strategy="Measure baseline, implement improvement, measure results, add regression tests",
            potential_risks=[
                "Improvement may not be as significant as expected",
                "May introduce performance tradeoffs",
                "May affect existing behavior in unexpected ways"
            ]
        )
    
    @staticmethod
    def _estimate_time(num_steps: int, issue_type: str) -> str:
        """Estimate time for implementation"""
        base_hours = {
            'bug': 2,
            'feature': 8,
            'enhancement': 4
        }
        
        base = base_hours.get(issue_type, 4)
        total_hours = base + (num_steps * 0.5)
        
        if total_hours < 4:
            return f"{int(total_hours)} hours"
        elif total_hours < 16:
            days = total_hours / 8
            return f"{days:.1f} days"
        else:
            days = total_hours / 8
            return f"{int(days)} days"
    
    @staticmethod
    def format_plan(plan: ImplementationPlan) -> str:
        """Format plan as readable markdown"""
        md = f"# Implementation Plan: {plan.issue_title}\n\n"
        md += f"**Issue:** #{plan.issue_number}\n"
        md += f"**Type:** {plan.issue_type}\n"
        md += f"**Estimated Time:** {plan.estimated_time}\n"
        md += f"**Total Steps:** {plan.total_steps}\n\n"
        
        md += "## Steps\n\n"
        for step in plan.steps:
            md += f"### Step {step.step_number}: {step.title}\n\n"
            md += f"**Description:** {step.description}\n\n"
            
            if step.files_to_modify:
                md += "**Files to modify:**\n"
                for file in step.files_to_modify:
                    md += f"- `{file}`\n"
                md += "\n"
            
            md += f"**Difficulty:** {step.estimated_difficulty}\n\n"
            
            if step.dependencies:
                deps = ', '.join([str(d) for d in step.dependencies])
                md += f"**Depends on:** Steps {deps}\n\n"
            
            if step.testing_notes:
                md += f"**Testing:** {step.testing_notes}\n\n"
            
            md += "---\n\n"
        
        md += "## Testing Strategy\n\n"
        md += plan.testing_strategy + "\n\n"
        
        md += "## Potential Risks\n\n"
        for risk in plan.potential_risks:
            md += f"- {risk}\n"
        
        return md

def main():
    if len(sys.argv) < 2:
        print("Usage: python implementation_planner.py '<issue_analysis_json>'")
        print("\nExpects output from analyze_issue.py")
        sys.exit(1)
    
    analysis = json.loads(sys.argv[1])
    plan = ImplementationPlanner.create_plan(analysis)
    
    # Output both JSON and markdown
    print(json.dumps(asdict(plan), indent=2))
    print("\n\n" + "="*80 + "\n")
    print(ImplementationPlanner.format_plan(plan))

if __name__ == '__main__':
    main()
