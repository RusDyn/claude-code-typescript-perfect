---
name: supabase-manager
description: Comprehensive Supabase CLI management for database, storage, auth, edge functions, and RLS. Use when working with Supabase projects to (1) Create and manage database migrations, (2) Design and implement RLS policies, (3) Generate edge functions, (4) Configure authentication, (5) Manage storage, (6) Set up realtime subscriptions. Includes migration generators, RLS pattern library, edge function templates, and complete CLI reference.
---

# Supabase Manager

Comprehensive toolkit for managing Supabase projects via CLI, covering database, auth, storage, edge functions, RLS, and all features.

## Related Skills

**Use with:** `playwright-test-builder` - For E2E testing of Supabase-backed applications. Use supabase-manager to set up test database fixtures and RLS policies, then playwright-test-builder to test the full application flow.

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

## Core Workflows

### Workflow 1: Database Schema Changes

1. Create migration: `supabase migration new add_users_table`
2. Write SQL in `supabase/migrations/TIMESTAMP_add_users_table.sql`
3. Apply locally: `supabase db reset`
4. Test thoroughly
5. Push to remote: `supabase db push`

### Workflow 2: Add RLS Policies

1. Generate policy: `python scripts/generate_rls_policy.py '{"pattern": "user_own_data", "table_name": "posts"}'`
2. Add to migration or execute directly
3. Test with different user contexts
4. Apply to production

### Workflow 3: Create Edge Function

1. Generate function: `python scripts/generate_edge_function.py '{"template": "with_supabase", "function_name": "my-function"}'`
2. Customize logic
3. Test locally: `supabase functions serve my-function`
4. Deploy: `supabase functions deploy my-function`

### Workflow 4: Storage Setup

1. Create bucket via SQL or Studio
2. Set up RLS policies for storage.objects
3. Configure CORS if needed
4. Test upload/download operations

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

### Edge Function Generator

Generate edge function templates:

```bash
# Basic function
python scripts/generate_edge_function.py '{
  "template": "basic",
  "function_name": "hello-world"
}'

# With Supabase client
python scripts/generate_edge_function.py '{
  "template": "with_supabase",
  "function_name": "get-user-data"
}'

# Webhook handler
python scripts/generate_edge_function.py '{
  "template": "webhook",
  "function_name": "process-webhook"
}'
```

**Available templates:**

- `basic` - Simple HTTP function
- `with_supabase` - Supabase client with auth
- `webhook` - Webhook handler with signature verification
- `scheduled` - Cron/scheduled task handler
- `stripe_webhook` - Stripe webhook integration
- `file_upload` - File upload handler with validation

## Reference Documentation

### CLI Commands Reference

**references/cli-commands.md** - Complete Supabase CLI reference:

- Installation and setup
- Project management (start, stop, status)
- Database operations (migrations, reset, push, pull, diff)
- Auth configuration
- Storage management
- Edge functions (deploy, serve, secrets)
- Realtime setup
- Testing and debugging
- CI/CD integration

### Database & Migrations

**references/database-migrations.md** - Database best practices:

- Schema design principles (standard fields, RLS, triggers, indexes)
- Migration patterns (tables, enums, functions, triggers)
- Advanced patterns (hierarchical data, versioning, full-text search)
- Performance optimization (partitioning, materialized views)
- Common patterns summary

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

### Edge Function with Auth

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      {
        global: {
          headers: { Authorization: req.headers.get("Authorization")! },
        },
      },
    );

    const {
      data: { user },
    } = await supabaseClient.auth.getUser();

    if (!user) {
      return new Response("Unauthorized", {
        status: 401,
        headers: corsHeaders,
      });
    }

    // Your logic here
    const { data, error } = await supabaseClient.from("your_table").select("*");

    if (error) throw error;

    return new Response(JSON.stringify({ data }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
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
5. **Force RLS** - Use `FORCE ROW LEVEL SECURITY`

### Edge Functions

1. **Use CORS headers** - For web requests
2. **Verify authentication** - Check user from JWT
3. **Handle errors** - Try-catch with proper status codes
4. **Use secrets** - Never hardcode API keys
5. **Test locally first** - Use `supabase functions serve`

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

### Edge Function Errors

```bash
# Check function logs
supabase functions serve my-function --debug

# View deployed function logs (in dashboard)
# Or use CLI (if available in your version)
```

## Configuration

### config.toml Template

See `assets/templates/config.toml` for complete configuration options including:

- API settings (port, schemas, max rows)
- Database configuration
- Auth providers (GitHub, Google, etc.)
- Storage limits
- Email settings
- Edge function configuration

## Advanced Features

### Database Branching

```bash
# Create branch (Pro feature)
supabase branches create feature-branch

# Link to branch
supabase link --branch feature-branch

# Delete branch
supabase branches delete feature-branch
```

### Realtime

```sql
-- Enable realtime for table
ALTER PUBLICATION supabase_realtime ADD TABLE public.messages;

-- Disable realtime
ALTER PUBLICATION supabase_realtime DROP TABLE public.messages;
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

This skill provides everything needed to manage Supabase projects effectively from CLI to production.
