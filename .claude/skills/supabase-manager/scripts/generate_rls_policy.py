#!/usr/bin/env python3
"""
Supabase RLS Policy Generator

Generates Row Level Security policies for common patterns.
"""

import sys
import json

RLS_PATTERNS = {
    'user_own_data': {
        'description': 'Users can only access their own data',
        'policies': [
            {
                'name': 'Users can view own {resource}',
                'operation': 'SELECT',
                'using': 'auth.uid() = user_id'
            },
            {
                'name': 'Users can insert own {resource}',
                'operation': 'INSERT',
                'with_check': 'auth.uid() = user_id'
            },
            {
                'name': 'Users can update own {resource}',
                'operation': 'UPDATE',
                'using': 'auth.uid() = user_id',
                'with_check': 'auth.uid() = user_id'
            },
            {
                'name': 'Users can delete own {resource}',
                'operation': 'DELETE',
                'using': 'auth.uid() = user_id'
            }
        ]
    },
    
    'public_read_own_write': {
        'description': 'Public can read, users can manage own data',
        'policies': [
            {
                'name': 'Anyone can view {resource}',
                'operation': 'SELECT',
                'role': 'anon',
                'using': 'true'
            },
            {
                'name': 'Users can insert own {resource}',
                'operation': 'INSERT',
                'role': 'authenticated',
                'with_check': 'auth.uid() = user_id'
            },
            {
                'name': 'Users can update own {resource}',
                'operation': 'UPDATE',
                'role': 'authenticated',
                'using': 'auth.uid() = user_id'
            },
            {
                'name': 'Users can delete own {resource}',
                'operation': 'DELETE',
                'role': 'authenticated',
                'using': 'auth.uid() = user_id'
            }
        ]
    },
    
    'org_based': {
        'description': 'Organization-based access control',
        'policies': [
            {
                'name': 'Users can view own org {resource}',
                'operation': 'SELECT',
                'using': '''EXISTS (
        SELECT 1 FROM public.org_members
        WHERE org_members.org_id = {table}.org_id
        AND org_members.user_id = auth.uid()
    )'''
            },
            {
                'name': 'Users can insert into own org {resource}',
                'operation': 'INSERT',
                'with_check': '''EXISTS (
        SELECT 1 FROM public.org_members
        WHERE org_members.org_id = {table}.org_id
        AND org_members.user_id = auth.uid()
    )'''
            },
            {
                'name': 'Org admins can update {resource}',
                'operation': 'UPDATE',
                'using': '''EXISTS (
        SELECT 1 FROM public.org_members
        WHERE org_members.org_id = {table}.org_id
        AND org_members.user_id = auth.uid()
        AND org_members.role = 'admin'
    )'''
            },
            {
                'name': 'Org admins can delete {resource}',
                'operation': 'DELETE',
                'using': '''EXISTS (
        SELECT 1 FROM public.org_members
        WHERE org_members.org_id = {table}.org_id
        AND org_members.user_id = auth.uid()
        AND org_members.role = 'admin'
    )'''
            }
        ]
    },
    
    'role_based': {
        'description': 'Role-based access control',
        'policies': [
            {
                'name': 'Users can view {resource}',
                'operation': 'SELECT',
                'using': "auth.jwt()->>'role' IN ('user', 'admin')"
            },
            {
                'name': 'Users can insert {resource}',
                'operation': 'INSERT',
                'with_check': "auth.jwt()->>'role' IN ('user', 'admin')"
            },
            {
                'name': 'Admins can update {resource}',
                'operation': 'UPDATE',
                'using': "auth.jwt()->>'role' = 'admin'"
            },
            {
                'name': 'Admins can delete {resource}',
                'operation': 'DELETE',
                'using': "auth.jwt()->>'role' = 'admin'"
            }
        ]
    },
    
    'time_based': {
        'description': 'Time-based access (e.g., published content)',
        'policies': [
            {
                'name': 'Anyone can view published {resource}',
                'operation': 'SELECT',
                'role': 'anon',
                'using': "published_at <= now() AND (unpublished_at IS NULL OR unpublished_at > now())"
            },
            {
                'name': 'Authors can view own {resource}',
                'operation': 'SELECT',
                'role': 'authenticated',
                'using': 'auth.uid() = author_id'
            },
            {
                'name': 'Authors can manage own {resource}',
                'operation': 'ALL',
                'role': 'authenticated',
                'using': 'auth.uid() = author_id'
            }
        ]
    },
    
    'hierarchical': {
        'description': 'Hierarchical permissions (e.g., teams > projects > tasks)',
        'policies': [
            {
                'name': 'Team members can view {resource}',
                'operation': 'SELECT',
                'using': '''EXISTS (
        SELECT 1 FROM public.projects p
        INNER JOIN public.team_members tm ON tm.team_id = p.team_id
        WHERE p.id = {table}.project_id
        AND tm.user_id = auth.uid()
    )'''
            },
            {
                'name': 'Project members can manage {resource}',
                'operation': 'ALL',
                'using': '''EXISTS (
        SELECT 1 FROM public.project_members pm
        WHERE pm.project_id = {table}.project_id
        AND pm.user_id = auth.uid()
    )'''
            }
        ]
    }
}

def generate_policy_sql(table_name, policy, resource_name=None):
    """Generate SQL for a single RLS policy"""
    
    resource = resource_name or table_name
    role = policy.get('role', 'authenticated')
    policy_type = policy.get('policy_type', 'PERMISSIVE')
    
    name = policy['name'].format(resource=resource)
    operation = policy['operation']
    
    sql = f"CREATE POLICY \"{name}\" ON public.{table_name}\n"
    sql += f"    AS {policy_type}\n"
    sql += f"    FOR {operation}\n"
    sql += f"    TO {role}\n"
    
    if 'using' in policy:
        using_clause = policy['using'].replace('{table}', table_name)
        sql += f"    USING ({using_clause})"
    
    if 'with_check' in policy:
        with_check_clause = policy['with_check'].replace('{table}', table_name)
        sql += f"\n    WITH CHECK ({with_check_clause})"
    
    sql += ";\n"
    
    return sql

def generate_pattern(pattern_name, table_name, resource_name=None):
    """Generate all policies for a pattern"""
    
    if pattern_name not in RLS_PATTERNS:
        return f"-- Unknown pattern: {pattern_name}\n-- Available: {', '.join(RLS_PATTERNS.keys())}"
    
    pattern = RLS_PATTERNS[pattern_name]
    resource = resource_name or table_name
    
    sql = f"-- {pattern['description']}\n"
    sql += f"-- Pattern: {pattern_name}\n"
    sql += f"-- Table: {table_name}\n\n"
    
    # Enable RLS
    sql += f"ALTER TABLE public.{table_name} ENABLE ROW LEVEL SECURITY;\n\n"
    
    # Generate all policies
    for policy in pattern['policies']:
        sql += generate_policy_sql(table_name, policy, resource)
        sql += "\n"
    
    return sql

def list_patterns():
    """List all available patterns"""
    result = {}
    for name, pattern in RLS_PATTERNS.items():
        result[name] = {
            'description': pattern['description'],
            'policies_count': len(pattern['policies'])
        }
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_rls_policy.py '<config_json>'")
        print("\nExamples:")
        print("\n1. Generate pattern:")
        print(json.dumps({
            'pattern': 'user_own_data',
            'table_name': 'posts',
            'resource_name': 'posts'
        }, indent=2))
        print("\n2. List patterns:")
        print(json.dumps({'action': 'list'}, indent=2))
        print("\n3. Custom policy:")
        print(json.dumps({
            'table_name': 'posts',
            'policy_name': 'Custom policy',
            'operation': 'SELECT',
            'role': 'authenticated',
            'using': 'auth.uid() = user_id'
        }, indent=2))
        sys.exit(1)
    
    config = json.loads(sys.argv[1])
    
    if config.get('action') == 'list':
        print(json.dumps(list_patterns(), indent=2))
        return
    
    if 'pattern' in config:
        # Generate from pattern
        sql = generate_pattern(
            config['pattern'],
            config['table_name'],
            config.get('resource_name')
        )
    else:
        # Generate single policy
        policy = {
            'name': config['policy_name'],
            'operation': config['operation'],
            'role': config.get('role', 'authenticated')
        }
        
        if 'using' in config:
            policy['using'] = config['using']
        if 'with_check' in config:
            policy['with_check'] = config['with_check']
        
        sql = generate_policy_sql(config['table_name'], policy)
    
    result = {
        'sql': sql,
        'table_name': config.get('table_name'),
        'pattern': config.get('pattern', 'custom')
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
