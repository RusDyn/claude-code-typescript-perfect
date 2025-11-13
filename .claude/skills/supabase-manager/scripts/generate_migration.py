#!/usr/bin/env python3
"""
Supabase Migration Generator

Generates SQL migration files with common patterns and best practices.
"""

import sys
import json
from datetime import datetime

MIGRATION_TEMPLATES = {
    'create_table': '''-- Create {table_name} table
CREATE TABLE IF NOT EXISTS public.{table_name} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable Row Level Security
ALTER TABLE public.{table_name} ENABLE ROW LEVEL SECURITY;

-- Create updated_at trigger
CREATE TRIGGER handle_{table_name}_updated_at
    BEFORE UPDATE ON public.{table_name}
    FOR EACH ROW
    EXECUTE FUNCTION moddatetime(updated_at);

-- Add indexes
CREATE INDEX IF NOT EXISTS {table_name}_created_at_idx ON public.{table_name}(created_at);

-- Grant permissions
GRANT ALL ON public.{table_name} TO authenticated;
GRANT SELECT ON public.{table_name} TO anon;
''',
    
    'add_column': '''-- Add {column_name} to {table_name}
ALTER TABLE public.{table_name}
ADD COLUMN IF NOT EXISTS {column_name} {column_type}{nullable}{default_value};

-- Add index if needed
{index_sql}

-- Add comment
COMMENT ON COLUMN public.{table_name}.{column_name} IS '{comment}';
''',
    
    'create_enum': '''-- Create {enum_name} enum type
DO $$ BEGIN
    CREATE TYPE public.{enum_name} AS ENUM ({values});
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
''',
    
    'create_function': '''-- Create {function_name} function
CREATE OR REPLACE FUNCTION public.{function_name}({parameters})
RETURNS {return_type}
LANGUAGE plpgsql
{security}
AS $$
BEGIN
    {function_body}
END;
$$;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION public.{function_name}({parameters}) TO authenticated;
''',
    
    'create_trigger': '''-- Create {trigger_name} trigger
CREATE TRIGGER {trigger_name}
    {timing} {event} ON public.{table_name}
    FOR EACH ROW
    EXECUTE FUNCTION {function_name}();
''',
    
    'create_rls_policy': '''-- Create RLS policy for {table_name}
CREATE POLICY "{policy_name}" ON public.{table_name}
    AS {policy_type}
    FOR {operation}
    TO {role}
    USING ({using_clause}){with_check};
''',
    
    'enable_realtime': '''-- Enable realtime for {table_name}
ALTER PUBLICATION supabase_realtime ADD TABLE public.{table_name};
''',
    
    'add_foreign_key': '''-- Add foreign key from {table_name}.{column_name} to {reference_table}.{reference_column}
ALTER TABLE public.{table_name}
ADD CONSTRAINT {constraint_name}
FOREIGN KEY ({column_name})
REFERENCES public.{reference_table}({reference_column})
ON DELETE {on_delete}
ON UPDATE CASCADE;

-- Add index for foreign key
CREATE INDEX IF NOT EXISTS {table_name}_{column_name}_idx ON public.{table_name}({column_name});
'''
}

def generate_migration(migration_type, config):
    """Generate migration SQL based on type and config"""
    
    if migration_type not in MIGRATION_TEMPLATES:
        return f"-- Unknown migration type: {migration_type}"
    
    template = MIGRATION_TEMPLATES[migration_type]
    
    # Handle specific migration types
    if migration_type == 'add_column':
        config['nullable'] = '' if config.get('nullable', True) else ' NOT NULL'
        config['default_value'] = f" DEFAULT {config['default']}" if config.get('default') else ''
        config['index_sql'] = ''
        if config.get('indexed'):
            config['index_sql'] = f"CREATE INDEX IF NOT EXISTS {config['table_name']}_{config['column_name']}_idx ON public.{config['table_name']}({config['column_name']});"
    
    elif migration_type == 'create_rls_policy':
        config['with_check'] = ''
        if config.get('with_check_clause'):
            config['with_check'] = f"\n    WITH CHECK ({config['with_check_clause']})"
    
    elif migration_type == 'create_function':
        config['security'] = 'SECURITY DEFINER' if config.get('security_definer') else 'SECURITY INVOKER'
    
    return template.format(**config)

def generate_timestamp():
    """Generate timestamp for migration filename"""
    return datetime.utcnow().strftime('%Y%m%d%H%M%S')

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_migration.py '<config_json>'")
        print("\nExamples:")
        print("\n1. Create table:")
        print(json.dumps({
            'type': 'create_table',
            'table_name': 'users'
        }, indent=2))
        print("\n2. Add column:")
        print(json.dumps({
            'type': 'add_column',
            'table_name': 'users',
            'column_name': 'email',
            'column_type': 'TEXT',
            'nullable': False,
            'indexed': True,
            'comment': 'User email address'
        }, indent=2))
        print("\n3. Create RLS policy:")
        print(json.dumps({
            'type': 'create_rls_policy',
            'table_name': 'users',
            'policy_name': 'Users can view own data',
            'policy_type': 'PERMISSIVE',
            'operation': 'SELECT',
            'role': 'authenticated',
            'using_clause': 'auth.uid() = user_id'
        }, indent=2))
        sys.exit(1)
    
    config = json.loads(sys.argv[1])
    migration_type = config.pop('type')
    
    # Generate migration SQL
    sql = generate_migration(migration_type, config)
    
    # Generate filename
    timestamp = generate_timestamp()
    description = config.get('description', migration_type.replace('_', ' '))
    filename = f"{timestamp}_{description.replace(' ', '_')}.sql"
    
    result = {
        'filename': filename,
        'sql': sql,
        'command': f'supabase migration new {description}'
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
