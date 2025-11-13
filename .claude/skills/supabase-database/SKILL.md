---
name: supabase-database
description: Supabase database management - migrations, schema design, RLS policies, and queries. Use when (1) Creating database migrations, (2) Designing table schemas, (3) Implementing RLS policies, (4) Managing database structure, (5) Optimizing queries and indexes, (6) Setting up storage RLS. DO NOT use for edge functions - use supabase-functions instead. Focus: PostgreSQL database, migrations, RLS, and schema management.
---

# Supabase Database Manager

Comprehensive toolkit for managing Supabase PostgreSQL databases via CLI, covering migrations, schema design, RLS policies, and query optimization.

## When to Use This Skill

Use supabase-database when you need to:

- **Create database migrations** for schema changes
- **Design table schemas** with proper types, constraints, and indexes
- **Implement RLS policies** for row-level security
- **Manage database structure** (tables, columns, foreign keys, enums)
- **Optimize queries and indexes** for performance
- **Set up storage RLS** policies for file access
- **Configure realtime** subscriptions for tables
- **Design full-text search** with tsvector

## When NOT to Use This Skill

**DO NOT use supabase-database for:**

- **Edge functions or webhooks** → Use `supabase-functions` skill instead
- **API routes or serverless logic** → Use `supabase-functions` skill instead
- **Scheduled tasks or cron jobs** → Use `supabase-functions` skill instead
- **External API integrations** → Use `supabase-functions` skill unless database-related

**Clear separation:**

- `supabase-database` = Database structure, migrations, RLS (data layer)
- `supabase-functions` = Serverless compute, webhooks, APIs (logic layer)

**Workflow:** Often use both - database for schema, functions for business logic

## Quick Start

### Project Setup

```bash
# Initialize Supabase in project
supabase init

# Start local development
supabase start

# Link to remote project
supabase link --project-ref <your-project-ref>

# Generate TypeScript types
supabase gen types typescript --local > types/supabase.ts
```

### Key Services After Start

- **PostgreSQL Database**: localhost:54322
- **API Server**: http://localhost:54321
- **Studio UI**: http://localhost:54323
- **Inbucket (Email testing)**: http://localhost:54324

## Core Workflow: Database Schema Changes

1. **Create migration**: `supabase migration new add_users_table`
2. **Write SQL** in `supabase/migrations/TIMESTAMP_add_users_table.sql`
3. **Apply locally**: `supabase db reset`
4. **Test thoroughly** - verify schema, RLS, constraints
5. **Push to remote**: `supabase db push`

## Scripts

### Migration Generator

Generate common migration patterns:

```bash
# Create table migration
python scripts/generate_migration.py '{
  "type": "create_table",
  "table_name": "posts",
  "description": "Add posts table"
}'

# Add column migration
python scripts/generate_migration.py '{
  "type": "add_column",
  "table_name": "users",
  "column_name": "avatar_url",
  "column_type": "TEXT",
  "nullable": true,
  "indexed": true,
  "comment": "User avatar URL"
}'

# Create RLS policy
python scripts/generate_migration.py '{
  "type": "create_rls_policy",
  "table_name": "posts",
  "policy_name": "Users can view own posts",
  "policy_type": "PERMISSIVE",
  "operation": "SELECT",
  "role": "authenticated",
  "using_clause": "auth.uid() = user_id"
}'
```

**Available migration types:**

- `create_table` - Standard table with RLS, triggers, indexes
- `add_column` - Add column with constraints and indexes
- `create_enum` - Create enum type
- `create_function` - PostgreSQL function
- `create_trigger` - Database trigger
- `create_rls_policy` - RLS policy
- `enable_realtime` - Enable realtime for table
- `add_foreign_key` - Foreign key constraint with indexes

### RLS Policy Generator

Generate RLS policies from patterns:

```bash
# List available patterns
python scripts/generate_rls_policy.py '{"action": "list"}'

# Generate from pattern
python scripts/generate_rls_policy.py '{
  "pattern": "user_own_data",
  "table_name": "posts",
  "resource_name": "posts"
}'

# Custom policy
python scripts/generate_rls_policy.py '{
  "table_name": "posts",
  "policy_name": "Custom policy",
  "operation": "SELECT",
  "role": "authenticated",
  "using": "auth.uid() = user_id"
}'
```

**Available patterns:**

- `user_own_data` - Users can only access their own data
- `public_read_own_write` - Public read, authenticated write
- `org_based` - Organization-based access control
- `role_based` - Role-based permissions
- `time_based` - Published/scheduled content
- `hierarchical` - Nested permissions (teams > projects > tasks)

## Reference Documentation

### Database & Migrations

**references/database-migrations.md** - Database best practices:

- Schema design principles (standard fields, RLS, triggers, indexes)
- Migration patterns (tables, enums, functions, triggers)
- Advanced patterns (hierarchical data, versioning, full-text search)
- Performance optimization (partitioning, materialized views)

### RLS Patterns

**references/rls-patterns.md** - Comprehensive RLS guide:

- Authentication-based patterns (user owns row, public read)
- Organization/team-based patterns
- Role-based access control
- Time-based access (published content, temporary shares)
- Advanced patterns (ABAC, geographic, social networks)
- Performance optimization
- Testing strategies

## Common Patterns

### Standard Table Creation

```sql
CREATE TABLE public.posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,

    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    status TEXT DEFAULT 'draft',

    CONSTRAINT title_length CHECK (char_length(title) > 0)
);

-- Enable RLS
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

-- Updated_at trigger
CREATE TRIGGER handle_posts_updated_at
    BEFORE UPDATE ON public.posts
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

-- Indexes
CREATE INDEX posts_user_id_idx ON public.posts(user_id);
CREATE INDEX posts_created_at_idx ON public.posts(created_at DESC);

-- Basic RLS policies
CREATE POLICY "Users can view own posts" ON public.posts
    FOR SELECT TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own posts" ON public.posts
    FOR INSERT TO authenticated
    WITH CHECK (auth.uid() = user_id);
```

### Storage RLS Policies

```sql
-- Enable RLS on storage
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Users can upload to their own folder
CREATE POLICY "Users can upload own files" ON storage.objects
    FOR INSERT TO authenticated
    WITH CHECK (
        bucket_id = 'avatars' AND
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Users can view their own files
CREATE POLICY "Users can view own files" ON storage.objects
    FOR SELECT TO authenticated
    USING (
        bucket_id = 'avatars' AND
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Users can delete their own files
CREATE POLICY "Users can delete own files" ON storage.objects
    FOR DELETE TO authenticated
    USING (
        bucket_id = 'avatars' AND
        auth.uid()::text = (storage.foldername(name))[1]
    );
```

### Full-Text Search

```sql
-- Add search vector column
ALTER TABLE posts ADD COLUMN search_vector tsvector;

-- Update function
CREATE OR REPLACE FUNCTION posts_search_trigger()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.content, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER posts_search_update
    BEFORE INSERT OR UPDATE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION posts_search_trigger();

-- Index
CREATE INDEX posts_search_idx ON posts USING gin(search_vector);
```

## Best Practices

### Database

1. **Always use migrations** - Never modify schema directly
2. **Enable RLS by default** - Security first approach
3. **Add standard fields** - id, created_at, updated_at on all tables
4. **Index foreign keys** - Performance for joins
5. **Use constraints** - Enforce data integrity
6. **Test locally** - `supabase db reset` frequently

### RLS

1. **Start restrictive** - Deny by default, allow explicitly
2. **Use indexes** - Index columns in RLS conditions
3. **Test as users** - Verify policies with different contexts
4. **Document complex policies** - Add SQL comments
5. **Force RLS** - Use `FORCE ROW LEVEL SECURITY` when needed

### Storage

1. **Set size limits** - Prevent abuse
2. **Validate file types** - Security check
3. **Use RLS policies** - Secure bucket access
4. **Organize with folders** - Use user_id/file structure
5. **Clean up unused files** - Implement cleanup jobs

## Troubleshooting

### Migration Issues

```bash
# Check migration status
supabase migration list

# Repair failed migration
supabase migration repair <version> --status reverted

# Reset and reapply
supabase db reset

# View diff before pushing
supabase db diff
```

### RLS Not Working

```sql
-- Check if RLS is enabled
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- List all policies
SELECT * FROM pg_policies WHERE schemaname = 'public';

-- Test as specific user
SET LOCAL role TO authenticated;
SET LOCAL request.jwt.claim.sub TO 'user-uuid';
SELECT * FROM your_table;
RESET role;
```

## TypeScript Integration

```bash
# Generate types from schema
supabase gen types typescript --local > types/supabase.ts

# Use in application
import { Database } from './types/supabase'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient<Database>(url, key)

// Now fully typed
const { data } = await supabase.from('posts').select('*')
```

## Working with Edge Functions

When your edge function needs to query the database:

1. Use `supabase-database` to design schema and RLS
2. Use `supabase-functions` to create the edge function
3. Edge function imports Supabase client to query database
4. RLS policies from database automatically apply to function queries

**Example workflow:**

```bash
# Step 1: Create schema (this skill)
supabase migration new add_posts_table

# Step 2: Create edge function (supabase-functions skill)
# Function will query the posts table created above
```

## CLI Quick Reference

```bash
# Database operations
supabase db reset              # Reset local database
supabase db push               # Push migrations to remote
supabase db pull               # Pull remote schema
supabase db diff               # View schema differences

# Migration operations
supabase migration new <name>  # Create new migration
supabase migration list        # List all migrations
supabase migration repair      # Repair failed migration

# Type generation
supabase gen types typescript --local > types/supabase.ts
```

For edge functions, webhooks, or serverless logic, use the `supabase-functions` skill.
For quick reference and skill selection, see `supabase-quickref`.

This skill provides everything needed to manage Supabase database schema, migrations, and security effectively.
