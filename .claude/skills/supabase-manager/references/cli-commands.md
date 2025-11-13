# Supabase CLI Commands Reference

Complete reference for Supabase CLI commands and workflows.

## Installation & Setup

```bash
# Install CLI
npm install -g supabase

# Or using Homebrew (macOS)
brew install supabase/tap/supabase

# Login to Supabase
supabase login

# Initialize project
supabase init

# Link to remote project
supabase link --project-ref <project-ref>
```

## Project Management

### Start/Stop Local Development

```bash
# Start all services (PostgreSQL, Studio, Edge Functions, etc.)
supabase start

# Stop all services
supabase stop

# Stop and reset database
supabase stop --no-backup

# Check service status
supabase status
```

### Project Configuration

```bash
# Generate TypeScript types from database schema
supabase gen types typescript --local > types/supabase.ts

# Generate types for linked project
supabase gen types typescript --linked > types/supabase.ts

# Update Supabase CLI
supabase update
```

## Database Management

### Migrations

```bash
# Create new migration
supabase migration new <migration_name>

# Apply migrations locally
supabase db reset

# Apply specific migration
supabase migration up

# Rollback migration
supabase migration repair <version> --status reverted

# List migrations
supabase migration list

# Squash migrations (combine multiple into one)
supabase migration squash

# Generate migration from diff
supabase db diff -f <migration_name>

# Generate migration from schema changes
supabase db diff --schema public,auth -f schema_changes
```

### Database Operations

```bash
# Reset local database (drops and recreates)
supabase db reset

# Pull remote database schema
supabase db pull

# Push local migrations to remote
supabase db push

# Dump database
supabase db dump -f dump.sql

# Restore from dump
psql -h localhost -U postgres -d postgres < dump.sql

# Run SQL file
supabase db execute -f migration.sql

# Execute SQL command
supabase db execute -c "SELECT * FROM users LIMIT 10"
```

### Database Diff

```bash
# Show differences between local and remote
supabase db diff

# Show differences for specific schemas
supabase db diff --schema public,auth

# Generate migration from differences
supabase db diff -f fix_schema --schema public

# Use specific database as source
supabase db diff --linked
```

## Authentication

### User Management

```bash
# Create user
supabase db execute -c "
  INSERT INTO auth.users (
    id, email, encrypted_password, email_confirmed_at, raw_user_meta_data
  ) VALUES (
    gen_random_uuid(),
    'user@example.com',
    crypt('password', gen_salt('bf')),
    now(),
    '{\"name\": \"User Name\"}'::jsonb
  )
"

# List users
supabase db execute -c "SELECT id, email, created_at FROM auth.users"

# Delete user
supabase db execute -c "DELETE FROM auth.users WHERE email = 'user@example.com'"
```

### Auth Configuration

Managed in `supabase/config.toml`:

```toml
[auth]
enabled = true
site_url = "http://localhost:3000"
additional_redirect_urls = ["https://example.com"]
jwt_expiry = 3600
enable_signup = true

[auth.email]
enable_signup = true
double_confirm_changes = true
enable_confirmations = false

[auth.external.github]
enabled = true
client_id = "env(GITHUB_CLIENT_ID)"
secret = "env(GITHUB_SECRET)"
```

## Storage

### Bucket Management

```bash
# Create storage bucket (via SQL)
supabase db execute -c "
  INSERT INTO storage.buckets (id, name, public)
  VALUES ('avatars', 'avatars', true)
"

# List buckets
supabase db execute -c "SELECT * FROM storage.buckets"

# Delete bucket
supabase db execute -c "DELETE FROM storage.buckets WHERE id = 'avatars'"
```

### Storage Policies

```bash
# Enable RLS on storage
supabase db execute -c "
  ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY
"

# Create storage policy (via SQL)
supabase db execute -c "
  CREATE POLICY \"Users can upload own avatars\" ON storage.objects
  FOR INSERT TO authenticated
  WITH CHECK (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  )
"
```

### File Operations (via client, not CLI directly)

Storage operations are typically done through the client SDK, but you can query via SQL:

```sql
-- List files in bucket
SELECT * FROM storage.objects WHERE bucket_id = 'avatars';

-- Delete file
DELETE FROM storage.objects WHERE bucket_id = 'avatars' AND name = 'path/to/file.jpg';
```

## Edge Functions

### Function Management

```bash
# Create new edge function
supabase functions new <function-name>

# Serve functions locally
supabase functions serve

# Serve specific function
supabase functions serve <function-name>

# Deploy function
supabase functions deploy <function-name>

# Deploy all functions
supabase functions deploy

# Delete function
supabase functions delete <function-name>

# List functions
supabase functions list
```

### Function Secrets

```bash
# Set secret for function
supabase secrets set MY_SECRET=value

# Set multiple secrets
supabase secrets set KEY1=value1 KEY2=value2

# List secrets (only shows names, not values)
supabase secrets list

# Unset secret
supabase secrets unset MY_SECRET
```

### Invoke Functions

```bash
# Invoke function locally
curl -i --location --request POST 'http://localhost:54321/functions/v1/hello-world' \
  --header 'Authorization: Bearer <anon-key>' \
  --header 'Content-Type: application/json' \
  --data '{"name":"World"}'

# Invoke deployed function
curl -i --location --request POST 'https://<project-ref>.supabase.co/functions/v1/hello-world' \
  --header 'Authorization: Bearer <anon-key>' \
  --header 'Content-Type: application/json' \
  --data '{"name":"World"}'
```

## Realtime

### Enable Realtime for Tables

```bash
# Enable realtime for table
supabase db execute -c "
  ALTER PUBLICATION supabase_realtime ADD TABLE public.messages
"

# Disable realtime for table
supabase db execute -c "
  ALTER PUBLICATION supabase_realtime DROP TABLE public.messages
"

# List tables with realtime enabled
supabase db execute -c "
  SELECT tablename FROM pg_publication_tables
  WHERE pubname = 'supabase_realtime'
"
```

## Testing & Development

### Seeding Database

```bash
# Run seed file (create in supabase/seed.sql)
supabase db reset

# The seed.sql file runs automatically on reset
```

Example `supabase/seed.sql`:

```sql
-- Seed users
INSERT INTO public.users (id, name, email) VALUES
  ('11111111-1111-1111-1111-111111111111', 'Alice', 'alice@example.com'),
  ('22222222-2222-2222-2222-222222222222', 'Bob', 'bob@example.com');

-- Seed posts
INSERT INTO public.posts (user_id, title, content) VALUES
  ('11111111-1111-1111-1111-111111111111', 'First Post', 'Hello World'),
  ('22222222-2222-2222-2222-222222222222', 'Second Post', 'Test content');
```

### Database Branching (Pro feature)

```bash
# Create branch
supabase branches create <branch-name>

# List branches
supabase branches list

# Switch branch
supabase link --branch <branch-name>

# Delete branch
supabase branches delete <branch-name>
```

## Row Level Security (RLS)

### Enable/Disable RLS

```bash
# Enable RLS for table
supabase db execute -c "ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY"

# Disable RLS (not recommended for production)
supabase db execute -c "ALTER TABLE public.posts DISABLE ROW LEVEL SECURITY"

# Force RLS for table owners (recommended)
supabase db execute -c "ALTER TABLE public.posts FORCE ROW LEVEL SECURITY"
```

### Create Policies

```bash
# Create SELECT policy
supabase db execute -c "
  CREATE POLICY \"Users can view own posts\" ON public.posts
  FOR SELECT TO authenticated
  USING (auth.uid() = user_id)
"

# Create INSERT policy
supabase db execute -c "
  CREATE POLICY \"Users can create posts\" ON public.posts
  FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id)
"

# Create UPDATE policy
supabase db execute -c "
  CREATE POLICY \"Users can update own posts\" ON public.posts
  FOR UPDATE TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id)
"

# Create DELETE policy
supabase db execute -c "
  CREATE POLICY \"Users can delete own posts\" ON public.posts
  FOR DELETE TO authenticated
  USING (auth.uid() = user_id)
"
```

### Drop Policies

```bash
# Drop specific policy
supabase db execute -c "DROP POLICY \"policy_name\" ON public.table_name"

# Drop all policies on table
supabase db execute -c "DROP POLICY IF EXISTS policy1 ON public.posts"
```

## Supabase Studio

```bash
# Access Studio UI
# After running 'supabase start', Studio is available at:
# http://localhost:54323

# Studio provides GUI for:
# - Table Editor
# - SQL Editor
# - Authentication management
# - Storage management
# - Database schema visualization
# - API documentation
```

## Project Inspection

```bash
# Inspect database schema
supabase inspect db --schema public

# List all tables
supabase db execute -c "\dt"

# Describe table structure
supabase db execute -c "\d public.users"

# List all RLS policies
supabase db execute -c "
  SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
  FROM pg_policies
  WHERE schemaname = 'public'
"

# List all functions
supabase db execute -c "\df"
```

## Environment Variables

Access via `supabase/config.toml` or environment:

```bash
# Common env vars
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=<local-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<local-service-role-key>

# Get keys from status
supabase status
```

## Useful Queries

### Performance Monitoring

```sql
-- Find slow queries
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

### Auth Queries

```sql
-- List all users with metadata
SELECT
  id,
  email,
  created_at,
  last_sign_in_at,
  raw_user_meta_data
FROM auth.users;

-- Count users by provider
SELECT
  provider,
  COUNT(*) as user_count
FROM auth.identities
GROUP BY provider;
```

## Troubleshooting

```bash
# View logs
supabase start --debug

# Check Docker containers
docker ps

# View specific service logs
docker logs supabase_db_<project>
docker logs supabase_studio_<project>

# Reset everything (nuclear option)
supabase stop --no-backup
rm -rf supabase/.temp
supabase start
```

## CI/CD Integration

```yaml
# Example GitHub Actions workflow
name: Deploy to Supabase

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Link Supabase project
        run: supabase link --project-ref ${{ secrets.SUPABASE_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Push database changes
        run: supabase db push

      - name: Deploy edge functions
        run: supabase functions deploy
```

## Best Practices

1. **Always use migrations** - Never modify schema directly in production
2. **Enable RLS on all tables** - Security by default
3. **Use service role key carefully** - Only in backend/edge functions
4. **Version control config.toml** - Track all project settings
5. **Test migrations locally first** - Use `supabase db reset` frequently
6. **Use branches for experiments** - Keep main branch stable
7. **Document custom functions** - Add comments to SQL functions
8. **Monitor query performance** - Use `pg_stat_statements`
9. **Backup regularly** - Especially before major changes
10. **Use TypeScript types** - Generate and use type definitions
