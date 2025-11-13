# Supabase Manager Scripts

## Requirements

**Python:** 3.7+ (no external dependencies required)
**Supabase CLI:** Required for applying generated migrations

All Python scripts use only standard library modules:
- `json` for configuration
- `datetime` for timestamps
- `sys` for I/O operations

## Prerequisites

Install Supabase CLI:
```bash
npm install -g supabase
# or
brew install supabase/tap/supabase
```

## Scripts

### generate_migration.py
Generates SQL migration files with common patterns.

**Usage:**
```bash
# Create table
python generate_migration.py '{
  "type": "create_table",
  "table_name": "posts",
  "description": "Add posts table"
}'

# Add column
python generate_migration.py '{
  "type": "add_column",
  "table_name": "users",
  "column_name": "avatar_url",
  "column_type": "TEXT",
  "nullable": true
}'
```

**Available types:** `create_table`, `add_column`, `create_enum`, `create_function`, `create_trigger`, `create_rls_policy`, `enable_realtime`, `add_foreign_key`

### generate_rls_policy.py
Creates RLS policies from common patterns.

**Usage:**
```bash
# List patterns
python generate_rls_policy.py '{"action": "list"}'

# Generate from pattern
python generate_rls_policy.py '{
  "pattern": "user_own_data",
  "table_name": "posts"
}'

# Custom policy
python generate_rls_policy.py '{
  "table_name": "posts",
  "policy_name": "Users view own",
  "operation": "SELECT",
  "role": "authenticated",
  "using": "auth.uid() = user_id"
}'
```

**Available patterns:** `user_own_data`, `public_read_own_write`, `org_based`, `role_based`, `time_based`, `hierarchical`

### generate_edge_function.py
Creates edge function templates.

**Usage:**
```bash
python generate_edge_function.py '{
  "template": "with_supabase",
  "function_name": "get-user-data"
}'
```

**Available templates:** `basic`, `with_supabase`, `webhook`, `scheduled`, `stripe_webhook`, `file_upload`

## Quick Setup

```bash
# Verify Python
python3 --version  # Need 3.7+

# Initialize Supabase in project
supabase init

# Generate and apply migration
python3 generate_migration.py '{...}' > supabase/migrations/$(date +%Y%m%d%H%M%S)_my_migration.sql
supabase db reset

# Generate edge function
python3 generate_edge_function.py '{...}' > supabase/functions/my-function/index.ts
supabase functions serve my-function
```

## Workflow Example

```bash
# 1. Generate migration
python3 generate_migration.py '{
  "type": "create_table",
  "table_name": "posts"
}' > supabase/migrations/$(date +%Y%m%d%H%M%S)_create_posts.sql

# 2. Generate RLS policies
python3 generate_rls_policy.py '{
  "pattern": "user_own_data",
  "table_name": "posts"
}' >> supabase/migrations/$(date +%Y%m%d%H%M%S)_create_posts.sql

# 3. Apply locally
supabase db reset

# 4. Test and push
supabase db push
```
