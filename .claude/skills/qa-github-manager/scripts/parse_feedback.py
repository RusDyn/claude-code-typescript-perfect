#!/usr/bin/env python3
"""
Client Feedback Parser

Parses client feedback from various formats (text, email, structured data)
and extracts actionable items, issues, and feature requests.
"""

import sys
import json
import re
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class FeedbackItem:
    """Represents a single feedback item"""
    raw_text: str
    item_type: str  # 'bug', 'feature', 'enhancement', 'question', 'concern'
    severity: str  # 'critical', 'high', 'medium', 'low'
    component: str = 'general'
    title: str = ''
    description: str = ''
    steps_to_reproduce: List[str] = None
    expected_behavior: str = ''
    actual_behavior: str = ''
    
    def __post_init__(self):
        if self.steps_to_reproduce is None:
            self.steps_to_reproduce = []

class FeedbackParser:
    """Parse and structure client feedback"""
    
    # Keywords for classification
    BUG_KEYWORDS = ['bug', 'error', 'broken', 'issue', 'problem', 'crash', 'fail', 
                    'not work', 'doesn\'t work', 'incorrect', 'wrong']
    FEATURE_KEYWORDS = ['feature', 'add', 'new', 'want', 'need', 'request', 'could',
                       'should', 'would like', 'wish', 'enhancement']
    CRITICAL_KEYWORDS = ['critical', 'urgent', 'blocker', 'production', 'down',
                        'cannot', 'can\'t', 'blocking', 'stopped']
    HIGH_KEYWORDS = ['important', 'asap', 'priority', 'serious', 'major']
    
    @staticmethod
    def parse_text(text: str) -> List[FeedbackItem]:
        """Parse unstructured text feedback"""
        items = []
        
        # Split by common separators
        sections = FeedbackParser._split_feedback(text)
        
        for section in sections:
            if not section.strip():
                continue
                
            item = FeedbackParser._analyze_section(section)
            if item:
                items.append(item)
        
        return items
    
    @staticmethod
    def _split_feedback(text: str) -> List[str]:
        """Split feedback into individual items"""
        # Split by numbered lists, bullet points, or double newlines
        patterns = [
            r'\n\d+[\.\)]\s+',  # Numbered: 1. 2. or 1) 2)
            r'\n[-*•]\s+',       # Bullets: - * •
            r'\n\n+',            # Double newlines
        ]
        
        sections = [text]
        for pattern in patterns:
            new_sections = []
            for section in sections:
                new_sections.extend(re.split(pattern, section))
            sections = new_sections
        
        return [s.strip() for s in sections if s.strip()]
    
    @staticmethod
    def _analyze_section(text: str) -> FeedbackItem:
        """Analyze a section of feedback and create a FeedbackItem"""
        text_lower = text.lower()
        
        # Determine type
        is_bug = any(keyword in text_lower for keyword in FeedbackParser.BUG_KEYWORDS)
        is_feature = any(keyword in text_lower for keyword in FeedbackParser.FEATURE_KEYWORDS)
        
        if is_bug and is_feature:
            # Could be both - prioritize based on context
            item_type = 'bug' if any(w in text_lower for w in ['error', 'broken', 'crash']) else 'feature'
        elif is_bug:
            item_type = 'bug'
        elif is_feature:
            item_type = 'feature'
        else:
            item_type = 'enhancement'
        
        # Determine severity
        if any(keyword in text_lower for keyword in FeedbackParser.CRITICAL_KEYWORDS):
            severity = 'critical'
        elif any(keyword in text_lower for keyword in FeedbackParser.HIGH_KEYWORDS):
            severity = 'high'
        elif item_type == 'bug':
            severity = 'medium'
        else:
            severity = 'low'
        
        # Extract title (first sentence or line)
        lines = text.split('\n')
        title = lines[0].strip()
        if len(title) > 100:
            title = title[:97] + '...'
        
        # Extract steps to reproduce (for bugs)
        steps = []
        if item_type == 'bug':
            steps = FeedbackParser._extract_steps(text)
        
        # Extract expected/actual behavior
        expected = FeedbackParser._extract_expected(text)
        actual = FeedbackParser._extract_actual(text)
        
        return FeedbackItem(
            raw_text=text,
            item_type=item_type,
            severity=severity,
            title=title,
            description=text,
            steps_to_reproduce=steps,
            expected_behavior=expected,
            actual_behavior=actual
        )
    
    @staticmethod
    def _extract_steps(text: str) -> List[str]:
        """Extract steps to reproduce from text"""
        steps = []
        
        # Look for numbered or bulleted lists
        lines = text.split('\n')
        in_steps = False
        
        for line in lines:
            line = line.strip()
            
            # Check if this looks like a step
            if re.match(r'^\d+[\.\)]\s+', line) or re.match(r'^[-*•]\s+', line):
                # Remove the number/bullet
                step = re.sub(r'^\d+[\.\)]\s+|^[-*•]\s+', '', line)
                steps.append(step)
                in_steps = True
            elif in_steps and line and not re.match(r'^[A-Z]', line):
                # Continuation of previous step
                if steps:
                    steps[-1] += ' ' + line
            elif in_steps and not line:
                break
        
        return steps
    
    @staticmethod
    def _extract_expected(text: str) -> str:
        """Extract expected behavior"""
        patterns = [
            r'expected:?\s*(.+?)(?:\n|$)',
            r'should\s+(.+?)(?:\n|$)',
            r'supposed to\s+(.+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ''
    
    @staticmethod
    def _extract_actual(text: str) -> str:
        """Extract actual behavior"""
        patterns = [
            r'actual:?\s*(.+?)(?:\n|$)',
            r'but\s+(.+?)(?:\n|$)',
            r'instead\s+(.+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ''
    
    @staticmethod
    def parse_json(data: Dict[str, Any]) -> List[FeedbackItem]:
        """Parse structured JSON feedback"""
        items = []
        
        if 'items' in data:
            # Array of feedback items
            for item_data in data['items']:
                item = FeedbackParser._parse_json_item(item_data)
                if item:
                    items.append(item)
        else:
            # Single item
            item = FeedbackParser._parse_json_item(data)
            if item:
                items.append(item)
        
        return items
    
    @staticmethod
    def _parse_json_item(data: Dict[str, Any]) -> FeedbackItem:
        """Parse a single JSON feedback item"""
        return FeedbackItem(
            raw_text=data.get('raw_text', json.dumps(data)),
            item_type=data.get('type', 'bug'),
            severity=data.get('severity', 'medium'),
            component=data.get('component', 'general'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            steps_to_reproduce=data.get('steps', []),
            expected_behavior=data.get('expected', ''),
            actual_behavior=data.get('actual', '')
        )

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_feedback.py '<feedback_text>'")
        print("   or: python parse_feedback.py --json '<json_data>'")
        print("\nExample:")
        print("  python parse_feedback.py 'Login button is broken. When I click it nothing happens.'")
        sys.exit(1)
    
    if sys.argv[1] == '--json':
        # Parse JSON input
        data = json.loads(sys.argv[2])
        items = FeedbackParser.parse_json(data)
    else:
        # Parse text input
        text = sys.argv[1]
        items = FeedbackParser.parse_text(text)
    
    # Output as JSON
    result = {
        'total_items': len(items),
        'items': [asdict(item) for item in items],
        'summary': {
            'bugs': sum(1 for i in items if i.item_type == 'bug'),
            'features': sum(1 for i in items if i.item_type == 'feature'),
            'critical': sum(1 for i in items if i.severity == 'critical'),
            'high': sum(1 for i in items if i.severity == 'high'),
        }
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
