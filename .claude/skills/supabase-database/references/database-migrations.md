# Database Schema & Migrations Guide

Best practices for Supabase database management, migrations, and schema design.

## Schema Design Principles

### 1. Always Include Standard Fields

```sql
CREATE TABLE public.posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,

    -- Your custom fields
    title TEXT NOT NULL,
    content TEXT,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE
);
```

### 2. Enable RLS by Default

```sql
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
```

### 3. Add Updated_at Trigger

```sql
-- Create trigger function (once per database)
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add trigger to table
CREATE TRIGGER handle_posts_updated_at
    BEFORE UPDATE ON public.posts
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();
```

### 4. Add Useful Indexes

```sql
-- Index foreign keys
CREATE INDEX posts_user_id_idx ON public.posts(user_id);

-- Index commonly queried fields
CREATE INDEX posts_created_at_idx ON public.posts(created_at DESC);

-- Composite indexes for common queries
CREATE INDEX posts_user_created_idx ON public.posts(user_id, created_at DESC);

-- Full-text search index
CREATE INDEX posts_content_search_idx ON public.posts USING gin(to_tsvector('english', content));
```

## Migration Patterns

### Creating Tables

#### Basic Table

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,

    username TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    bio TEXT,

    CONSTRAINT username_length CHECK (char_length(username) >= 3)
);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Create updated_at trigger
CREATE TRIGGER handle_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

-- Create indexes
CREATE INDEX users_username_idx ON public.users(username);
CREATE INDEX users_created_at_idx ON public.users(created_at);

-- Add RLS policies
CREATE POLICY "Users can view all profiles" ON public.users
    FOR SELECT TO authenticated
    USING (true);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE TO authenticated
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);
```

#### Table with Enum

```sql
-- Create enum type
CREATE TYPE public.post_status AS ENUM ('draft', 'published', 'archived');

-- Create table using enum
CREATE TABLE public.posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    status post_status DEFAULT 'draft' NOT NULL,
    title TEXT NOT NULL,
    content TEXT
);
```

#### Many-to-Many Relationship

```sql
-- Posts table
CREATE TABLE public.posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL
);

-- Tags table
CREATE TABLE public.tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL
);

-- Junction table
CREATE TABLE public.post_tags (
    post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES public.tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,

    PRIMARY KEY (post_id, tag_id)
);

-- Indexes for junction table
CREATE INDEX post_tags_post_id_idx ON public.post_tags(post_id);
CREATE INDEX post_tags_tag_id_idx ON public.post_tags(tag_id);
```

### Modifying Tables

#### Adding Columns

```sql
-- Add nullable column
ALTER TABLE public.users
ADD COLUMN IF NOT EXISTS phone TEXT;

-- Add non-nullable column with default
ALTER TABLE public.users
ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT false NOT NULL;

-- Add column with constraint
ALTER TABLE public.users
ADD COLUMN IF NOT EXISTS age INTEGER
CHECK (age >= 18 AND age <= 120);
```

#### Changing Columns

```sql
-- Change column type
ALTER TABLE public.users
ALTER COLUMN age TYPE SMALLINT;

-- Add NOT NULL constraint
ALTER TABLE public.users
ALTER COLUMN email SET NOT NULL;

-- Remove NOT NULL constraint
ALTER TABLE public.users
ALTER COLUMN phone DROP NOT NULL;

-- Set default value
ALTER TABLE public.users
ALTER COLUMN status SET DEFAULT 'active';

-- Rename column
ALTER TABLE public.users
RENAME COLUMN old_name TO new_name;
```

#### Adding Constraints

```sql
-- Add unique constraint
ALTER TABLE public.users
ADD CONSTRAINT users_email_unique UNIQUE (email);

-- Add check constraint
ALTER TABLE public.posts
ADD CONSTRAINT posts_title_length CHECK (char_length(title) > 0);

-- Add foreign key
ALTER TABLE public.posts
ADD CONSTRAINT posts_user_id_fkey
FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;
```

### Functions & Triggers

#### Soft Delete Function

```sql
-- Add deleted_at column
ALTER TABLE public.posts
ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;

-- Create soft delete function
CREATE OR REPLACE FUNCTION public.soft_delete()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE public.posts
    SET deleted_at = timezone('utc'::text, now())
    WHERE id = OLD.id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER soft_delete_posts
    BEFORE DELETE ON public.posts
    FOR EACH ROW
    EXECUTE FUNCTION public.soft_delete();

-- Query only non-deleted
CREATE VIEW public.active_posts AS
SELECT * FROM public.posts WHERE deleted_at IS NULL;
```

#### Auto-increment Custom ID

```sql
-- Create sequence
CREATE SEQUENCE public.invoice_number_seq START 1000;

-- Create function
CREATE OR REPLACE FUNCTION public.set_invoice_number()
RETURNS TRIGGER AS $$
BEGIN
    NEW.invoice_number = 'INV-' || nextval('public.invoice_number_seq');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add trigger
CREATE TRIGGER set_invoice_number_trigger
    BEFORE INSERT ON public.invoices
    FOR EACH ROW
    WHEN (NEW.invoice_number IS NULL)
    EXECUTE FUNCTION public.set_invoice_number();
```

#### Audit Log Trigger

```sql
-- Create audit log table
CREATE TABLE public.audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name TEXT NOT NULL,
    record_id UUID NOT NULL,
    action TEXT NOT NULL,
    old_data JSONB,
    new_data JSONB,
    user_id UUID REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create audit function
CREATE OR REPLACE FUNCTION public.audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO public.audit_log (table_name, record_id, action, old_data, user_id)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', row_to_json(OLD), auth.uid());
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO public.audit_log (table_name, record_id, action, old_data, new_data, user_id)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', row_to_json(OLD), row_to_json(NEW), auth.uid());
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO public.audit_log (table_name, record_id, action, new_data, user_id)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', row_to_json(NEW), auth.uid());
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add audit trigger to table
CREATE TRIGGER posts_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON public.posts
    FOR EACH ROW
    EXECUTE FUNCTION public.audit_trigger();
```

### Full-Text Search

```sql
-- Add tsvector column
ALTER TABLE public.posts
ADD COLUMN search_vector tsvector;

-- Create function to update search vector
CREATE OR REPLACE FUNCTION public.posts_search_trigger()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add trigger
CREATE TRIGGER posts_search_update
    BEFORE INSERT OR UPDATE ON public.posts
    FOR EACH ROW
    EXECUTE FUNCTION public.posts_search_trigger();

-- Create GIN index
CREATE INDEX posts_search_idx ON public.posts USING gin(search_vector);

-- Search query example
-- SELECT * FROM posts WHERE search_vector @@ to_tsquery('english', 'search & terms');
```

## Advanced Patterns

### Hierarchical Data (Comments)

```sql
CREATE TABLE public.comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,

    post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES public.comments(id) ON DELETE CASCADE,

    content TEXT NOT NULL,

    -- For efficient querying
    path TEXT, -- e.g., '001.002.003' for nested comments
    depth INTEGER DEFAULT 0
);

-- Index for tree traversal
CREATE INDEX comments_path_idx ON public.comments(path);
CREATE INDEX comments_parent_id_idx ON public.comments(parent_id);
```

### Versioning/History

```sql
-- Main table
CREATE TABLE public.documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    title TEXT NOT NULL,
    current_version INTEGER DEFAULT 1
);

-- Version history table
CREATE TABLE public.document_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES public.documents(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    created_by UUID REFERENCES auth.users(id),

    title TEXT NOT NULL,
    content TEXT NOT NULL,

    UNIQUE(document_id, version)
);

-- Trigger to create version on update
CREATE OR REPLACE FUNCTION public.version_document()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert old version into history
    INSERT INTO public.document_versions (document_id, version, title, content, created_by)
    VALUES (OLD.id, OLD.current_version, OLD.title, OLD.content, auth.uid());

    -- Increment version
    NEW.current_version = OLD.current_version + 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER version_document_trigger
    BEFORE UPDATE ON public.documents
    FOR EACH ROW
    EXECUTE FUNCTION public.version_document();
```

### Counters (Denormalization)

```sql
-- Posts table with counter
ALTER TABLE public.posts
ADD COLUMN comment_count INTEGER DEFAULT 0;

-- Update counter function
CREATE OR REPLACE FUNCTION public.update_post_comment_count()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE public.posts
        SET comment_count = comment_count + 1
        WHERE id = NEW.post_id;
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE public.posts
        SET comment_count = comment_count - 1
        WHERE id = OLD.post_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Add trigger
CREATE TRIGGER update_post_comment_count_trigger
    AFTER INSERT OR DELETE ON public.comments
    FOR EACH ROW
    EXECUTE FUNCTION public.update_post_comment_count();
```

## Migration Best Practices

### 1. Make Migrations Reversible

Always include both up and down migrations:

```sql
-- Up migration (20230101000000_add_user_status.sql)
ALTER TABLE public.users ADD COLUMN status TEXT DEFAULT 'active';

-- Down migration (would be in separate file or section)
-- ALTER TABLE public.users DROP COLUMN status;
```

### 2. Use Transactions

```sql
BEGIN;

-- Your migration here
ALTER TABLE public.users ADD COLUMN email_verified BOOLEAN DEFAULT false;
UPDATE public.users SET email_verified = true WHERE email IS NOT NULL;

COMMIT;
```

### 3. Handle Existing Data

```sql
-- Add column with default
ALTER TABLE public.users ADD COLUMN role TEXT DEFAULT 'user';

-- Update existing data if needed
UPDATE public.users SET role = 'admin' WHERE email LIKE '%@company.com';

-- Then make it NOT NULL if desired
ALTER TABLE public.users ALTER COLUMN role SET NOT NULL;
```

### 4. Test Migrations Locally

```bash
# Test migration
supabase db reset

# If successful, commit
git add supabase/migrations/
git commit -m "Add user roles"

# Then push to remote
supabase db push
```

### 5. Use Migration Helpers

```sql
-- Create helper for common pattern
CREATE OR REPLACE FUNCTION public.create_standard_table(table_name TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('
        CREATE TABLE public.%I (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone(''utc''::text, now()) NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone(''utc''::text, now()) NOT NULL
        );

        ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY;

        CREATE TRIGGER handle_%I_updated_at
            BEFORE UPDATE ON public.%I
            FOR EACH ROW
            EXECUTE FUNCTION public.handle_updated_at();
    ', table_name, table_name, table_name, table_name);
END;
$$ LANGUAGE plpgsql;
```

## Performance Optimization

### Partitioning (for large tables)

```sql
-- Create partitioned table
CREATE TABLE public.events (
    id UUID DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    event_type TEXT,
    data JSONB
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE public.events_2024_01 PARTITION OF public.events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE public.events_2024_02 PARTITION OF public.events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

### Materialized Views

```sql
-- Create materialized view for expensive queries
CREATE MATERIALIZED VIEW public.user_stats AS
SELECT
    u.id,
    u.username,
    COUNT(DISTINCT p.id) as post_count,
    COUNT(DISTINCT c.id) as comment_count,
    MAX(p.created_at) as last_post_at
FROM public.users u
LEFT JOIN public.posts p ON p.user_id = u.id
LEFT JOIN public.comments c ON c.user_id = u.id
GROUP BY u.id, u.username;

-- Create index on materialized view
CREATE INDEX user_stats_post_count_idx ON public.user_stats(post_count DESC);

-- Refresh materialized view (can be scheduled)
REFRESH MATERIALIZED VIEW public.user_stats;

-- Or use CONCURRENTLY to avoid locks
REFRESH MATERIALIZED VIEW CONCURRENTLY public.user_stats;
```

## Common Patterns Summary

1. **Always enable RLS** on user-facing tables
2. **Use UUIDs** for primary keys (better for distributed systems)
3. **Add timestamps** (created_at, updated_at) to all tables
4. **Index foreign keys** for join performance
5. **Use constraints** to enforce data integrity
6. **Add helpful indexes** based on query patterns
7. **Use triggers** for automatic field updates
8. **Soft delete** when you need audit trails
9. **Version control** all schema changes through migrations
10. **Test migrations** locally before applying to production
