#!/usr/bin/env python3
"""
Repository Analyzer

Analyzes repository structure to understand codebase organization
and locate relevant files for issue resolution.
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict

def analyze_directory_structure(repo_path, max_depth=3, exclude_dirs=None):
    """Analyze directory structure of repository"""
    if exclude_dirs is None:
        exclude_dirs = {
            '.git', 'node_modules', '__pycache__', '.pytest_cache',
            'venv', 'env', '.venv', 'dist', 'build', '.tox',
            'coverage', '.coverage', '.mypy_cache', '.ruff_cache',
            'target', 'vendor', '.next', '.nuxt'
        }
    
    structure = {
        'directories': [],
        'files_by_type': defaultdict(list),
        'total_files': 0,
        'languages': set()
    }
    
    def walk_dir(path, depth=0):
        if depth > max_depth:
            return
        
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    if entry.name not in exclude_dirs and not entry.name.startswith('.'):
                        rel_path = os.path.relpath(entry.path, repo_path)
                        structure['directories'].append(rel_path)
                        walk_dir(entry.path, depth + 1)
                
                elif entry.is_file():
                    ext = os.path.splitext(entry.name)[1]
                    rel_path = os.path.relpath(entry.path, repo_path)
                    structure['files_by_type'][ext].append(rel_path)
                    structure['total_files'] += 1
                    
                    # Detect language
                    if ext in ['.py']:
                        structure['languages'].add('Python')
                    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
                        structure['languages'].add('JavaScript/TypeScript')
                    elif ext in ['.java']:
                        structure['languages'].add('Java')
                    elif ext in ['.go']:
                        structure['languages'].add('Go')
                    elif ext in ['.rs']:
                        structure['languages'].add('Rust')
                    elif ext in ['.c', '.cpp', '.h', '.hpp']:
                        structure['languages'].add('C/C++')
                    elif ext in ['.rb']:
                        structure['languages'].add('Ruby')
                    elif ext in ['.php']:
                        structure['languages'].add('PHP')
        
        except PermissionError:
            pass
    
    walk_dir(repo_path)
    structure['languages'] = list(structure['languages'])
    
    return structure

def detect_project_type(repo_path):
    """Detect project type and framework"""
    indicators = {
        'package.json': 'Node.js/JavaScript',
        'requirements.txt': 'Python',
        'setup.py': 'Python',
        'Cargo.toml': 'Rust',
        'go.mod': 'Go',
        'pom.xml': 'Java/Maven',
        'build.gradle': 'Java/Gradle',
        'Gemfile': 'Ruby',
        'composer.json': 'PHP'
    }
    
    frameworks = {
        'package.json': {
            'react': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular',
            'next': 'Next.js',
            'express': 'Express',
            'nestjs': 'NestJS'
        },
        'requirements.txt': {
            'django': 'Django',
            'flask': 'Flask',
            'fastapi': 'FastAPI'
        }
    }
    
    detected = []
    
    for file, project_type in indicators.items():
        file_path = os.path.join(repo_path, file)
        if os.path.exists(file_path):
            detected.append(project_type)
            
            # Check for frameworks
            if file in frameworks:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read().lower()
                        for keyword, framework in frameworks[file].items():
                            if keyword in content:
                                detected.append(framework)
                except:
                    pass
    
    return detected

def find_test_files(repo_path, structure):
    """Find test files and directories"""
    test_indicators = ['test', 'spec', '__tests__', 'tests']
    
    test_files = []
    test_dirs = []
    
    # Check directories
    for directory in structure['directories']:
        dir_name = os.path.basename(directory).lower()
        if any(indicator in dir_name for indicator in test_indicators):
            test_dirs.append(directory)
    
    # Check files
    for ext, files in structure['files_by_type'].items():
        for file in files:
            file_lower = file.lower()
            if any(indicator in file_lower for indicator in test_indicators):
                test_files.append(file)
    
    return {
        'test_directories': test_dirs,
        'test_files': test_files[:20]  # Limit output
    }

def find_config_files(repo_path):
    """Find important configuration files"""
    config_files = [
        'package.json', 'package-lock.json', 'yarn.lock',
        'requirements.txt', 'Pipfile', 'pyproject.toml', 'setup.py',
        'Cargo.toml', 'Cargo.lock',
        'go.mod', 'go.sum',
        'pom.xml', 'build.gradle',
        '.gitignore', '.eslintrc', '.prettierrc',
        'tsconfig.json', 'webpack.config.js',
        'Dockerfile', 'docker-compose.yml',
        'Makefile', 'README.md', 'CONTRIBUTING.md'
    ]
    
    found = []
    for config in config_files:
        if os.path.exists(os.path.join(repo_path, config)):
            found.append(config)
    
    return found

def search_for_pattern(repo_path, pattern, file_extensions=None):
    """Search for a pattern in files"""
    import re
    
    if file_extensions is None:
        file_extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs']
    
    matches = []
    pattern_re = re.compile(pattern, re.IGNORECASE)
    
    for root, dirs, files in os.walk(repo_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in {
            '.git', 'node_modules', '__pycache__', 'venv', 'dist', 'build'
        }]
        
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if pattern_re.search(content):
                            rel_path = os.path.relpath(file_path, repo_path)
                            matches.append(rel_path)
                            
                            if len(matches) >= 50:  # Limit results
                                return matches
                except:
                    pass
    
    return matches

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_repository.py <repo_path> [search_pattern]", file=sys.stderr)
        sys.exit(1)
    
    repo_path = sys.argv[1]
    
    if not os.path.exists(repo_path):
        print(json.dumps({'error': f'Repository path not found: {repo_path}'}))
        sys.exit(1)
    
    analysis = {
        'repo_path': os.path.abspath(repo_path),
        'project_types': detect_project_type(repo_path),
        'config_files': find_config_files(repo_path)
    }
    
    # Analyze structure
    structure = analyze_directory_structure(repo_path)
    analysis['structure'] = {
        'total_files': structure['total_files'],
        'languages': structure['languages'],
        'file_types': {
            ext: len(files)
            for ext, files in structure['files_by_type'].items()
        },
        'main_directories': structure['directories'][:20]  # Top 20
    }
    
    # Find tests
    analysis['testing'] = find_test_files(repo_path, structure)
    
    # Search for pattern if provided
    if len(sys.argv) > 2:
        pattern = sys.argv[2]
        matches = search_for_pattern(repo_path, pattern)
        analysis['pattern_matches'] = {
            'pattern': pattern,
            'matches': matches
        }
    
    print(json.dumps(analysis, indent=2))

if __name__ == '__main__':
    main()
