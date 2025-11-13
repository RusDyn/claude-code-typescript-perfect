# Row Level Security (RLS) Patterns

Comprehensive guide to RLS patterns for secure data access in Supabase.

## RLS Basics

### Enable RLS

```sql
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owners (recommended)
ALTER TABLE public.posts FORCE ROW LEVEL SECURITY;
```

### Policy Structure

```sql
CREATE POLICY "policy_name" ON table_name
    AS PERMISSIVE | RESTRICTIVE
    FOR ALL | SELECT | INSERT | UPDATE | DELETE
    TO role_name
    USING (condition_for_select_update_delete)
    WITH CHECK (condition_for_insert_update);
```

## Authentication-Based Patterns

### Pattern 1: User Owns Row

**Use case:** Users can only see/modify their own data

```sql
-- Users table (profile data)
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT TO authenticated
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE TO authenticated
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- Posts table
CREATE POLICY "Users can view own posts" ON public.posts
    FOR SELECT TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own posts" ON public.posts
    FOR INSERT TO authenticated
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own posts" ON public.posts
    FOR UPDATE TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own posts" ON public.posts
    FOR DELETE TO authenticated
    USING (auth.uid() = user_id);
```

### Pattern 2: Public Read, Authenticated Write

**Use case:** Public content that authenticated users can create

```sql
-- Anyone (including anon) can read
CREATE POLICY "Anyone can view posts" ON public.posts
    FOR SELECT TO anon, authenticated
    USING (true);

-- Only authenticated users can create
CREATE POLICY "Authenticated users can create posts" ON public.posts
    FOR INSERT TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- Users can update own posts
CREATE POLICY "Users can update own posts" ON public.posts
    FOR UPDATE TO authenticated
    USING (auth.uid() = user_id);
```

### Pattern 3: Public Read Published, Own Read All

**Use case:** Published content is public, drafts are private

```sql
-- Public can see published posts
CREATE POLICY "Anyone can view published posts" ON public.posts
    FOR SELECT TO anon, authenticated
    USING (status = 'published');

-- Authors can see all their own posts
CREATE POLICY "Authors can view own posts" ON public.posts
    FOR SELECT TO authenticated
    USING (auth.uid() = user_id);

-- Note: Use SELECT OR to combine conditions
-- In practice, Supabase will return rows that match EITHER policy
```

## Organization/Team-Based Patterns

### Pattern 4: Organization Membership

**Use case:** Multi-tenant app where users belong to organizations

```sql
-- Org members table
CREATE TABLE public.org_members (
    org_id UUID REFERENCES public.organizations(id),
    user_id UUID REFERENCES auth.users(id),
    role TEXT NOT NULL, -- 'owner', 'admin', 'member'
    PRIMARY KEY (org_id, user_id)
);

-- Users can see posts in their orgs
CREATE POLICY "Org members can view org posts" ON public.posts
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.org_members
            WHERE org_members.org_id = posts.org_id
            AND org_members.user_id = auth.uid()
        )
    );

-- Members can create posts in their orgs
CREATE POLICY "Org members can create posts" ON public.posts
    FOR INSERT TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.org_members
            WHERE org_members.org_id = posts.org_id
            AND org_members.user_id = auth.uid()
        )
    );

-- Only admins/owners can delete
CREATE POLICY "Org admins can delete posts" ON public.posts
    FOR DELETE TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.org_members
            WHERE org_members.org_id = posts.org_id
            AND org_members.user_id = auth.uid()
            AND org_members.role IN ('admin', 'owner')
        )
    );
```

### Pattern 5: Hierarchical Permissions

**Use case:** Teams > Projects > Tasks hierarchy

```sql
-- Team members can see all tasks in team projects
CREATE POLICY "Team members can view tasks" ON public.tasks
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.projects p
            INNER JOIN public.team_members tm ON tm.team_id = p.team_id
            WHERE p.id = tasks.project_id
            AND tm.user_id = auth.uid()
        )
    );

-- Project members can manage tasks
CREATE POLICY "Project members can manage tasks" ON public.tasks
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.project_members pm
            WHERE pm.project_id = tasks.project_id
            AND pm.user_id = auth.uid()
        )
    );
```

## Role-Based Patterns

### Pattern 6: JWT Claims Role

**Use case:** Role stored in JWT claims

```sql
-- Function to get user role from JWT
CREATE OR REPLACE FUNCTION public.get_user_role()
RETURNS TEXT AS $$
    SELECT COALESCE(
        auth.jwt() -> 'user_metadata' ->> 'role',
        'user'
    );
$$ LANGUAGE sql STABLE;

-- Only admins can view all users
CREATE POLICY "Admins can view all users" ON public.users
    FOR SELECT TO authenticated
    USING (get_user_role() = 'admin');

-- Regular users can only view their own data
CREATE POLICY "Users can view own data" ON public.users
    FOR SELECT TO authenticated
    USING (auth.uid() = id);

-- Admins can update any user
CREATE POLICY "Admins can update users" ON public.users
    FOR UPDATE TO authenticated
    USING (get_user_role() = 'admin');
```

### Pattern 7: Database Role Table

**Use case:** Roles stored in database

```sql
-- User roles table
CREATE TABLE public.user_roles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id),
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Helper function
CREATE OR REPLACE FUNCTION public.has_role(required_role TEXT)
RETURNS BOOLEAN AS $$
    SELECT EXISTS (
        SELECT 1 FROM public.user_roles
        WHERE user_id = auth.uid()
        AND role = required_role
    );
$$ LANGUAGE sql STABLE SECURITY DEFINER;

-- Use in policies
CREATE POLICY "Admins can manage posts" ON public.posts
    FOR ALL TO authenticated
    USING (has_role('admin'));

CREATE POLICY "Moderators can update posts" ON public.posts
    FOR UPDATE TO authenticated
    USING (has_role('moderator') OR auth.uid() = user_id);
```

## Time-Based Patterns

### Pattern 8: Published/Scheduled Content

**Use case:** Content visible only when published

```sql
-- Anyone can see published content
CREATE POLICY "View published content" ON public.posts
    FOR SELECT TO anon, authenticated
    USING (
        published_at <= now()
        AND (unpublished_at IS NULL OR unpublished_at > now())
    );

-- Authors can see their own content regardless of status
CREATE POLICY "Authors see own content" ON public.posts
    FOR SELECT TO authenticated
    USING (auth.uid() = user_id);
```

### Pattern 9: Temporary Access

**Use case:** Time-limited access to resources

```sql
-- Temporary shares table
CREATE TABLE public.temp_shares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_id UUID NOT NULL,
    shared_with UUID REFERENCES auth.users(id),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Allow access if shared and not expired
CREATE POLICY "Access shared resources" ON public.documents
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.temp_shares
            WHERE temp_shares.resource_id = documents.id
            AND temp_shares.shared_with = auth.uid()
            AND temp_shares.expires_at > now()
        )
    );
```

## Advanced Patterns

### Pattern 10: Attribute-Based Access Control (ABAC)

**Use case:** Complex permission logic based on multiple attributes

```sql
-- Access rules table
CREATE TABLE public.access_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_type TEXT NOT NULL,
    user_attribute TEXT NOT NULL, -- e.g., 'department', 'level'
    user_value TEXT NOT NULL, -- e.g., 'engineering', 'senior'
    can_read BOOLEAN DEFAULT true,
    can_write BOOLEAN DEFAULT false,
    can_delete BOOLEAN DEFAULT false
);

-- User attributes table
CREATE TABLE public.user_attributes (
    user_id UUID REFERENCES auth.users(id),
    attribute_key TEXT NOT NULL,
    attribute_value TEXT NOT NULL,
    PRIMARY KEY (user_id, attribute_key)
);

-- Check access function
CREATE OR REPLACE FUNCTION public.check_access(
    p_resource_type TEXT,
    p_action TEXT -- 'read', 'write', 'delete'
)
RETURNS BOOLEAN AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.access_rules ar
        INNER JOIN public.user_attributes ua
            ON ua.attribute_key = ar.user_attribute
            AND ua.attribute_value = ar.user_value
        WHERE ar.resource_type = p_resource_type
        AND ua.user_id = auth.uid()
        AND (
            (p_action = 'read' AND ar.can_read = true) OR
            (p_action = 'write' AND ar.can_write = true) OR
            (p_action = 'delete' AND ar.can_delete = true)
        )
    );
$$ LANGUAGE sql STABLE SECURITY DEFINER;

-- Use in policy
CREATE POLICY "ABAC read policy" ON public.documents
    FOR SELECT TO authenticated
    USING (check_access('documents', 'read'));
```

### Pattern 11: Geographic/Location-Based

**Use case:** Access based on location

```sql
-- User locations table
CREATE TABLE public.user_locations (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id),
    country_code TEXT,
    region TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Region-restricted content
CREATE POLICY "Regional content access" ON public.content
    FOR SELECT TO authenticated
    USING (
        allowed_regions IS NULL OR
        EXISTS (
            SELECT 1 FROM public.user_locations
            WHERE user_locations.user_id = auth.uid()
            AND user_locations.country_code = ANY(content.allowed_regions)
        )
    );
```

### Pattern 12: Friend/Following System

**Use case:** Social network visibility

```sql
-- Followers table
CREATE TABLE public.followers (
    follower_id UUID REFERENCES auth.users(id),
    following_id UUID REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    PRIMARY KEY (follower_id, following_id)
);

-- Users can see posts from people they follow
CREATE POLICY "See followed users posts" ON public.posts
    FOR SELECT TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.followers
            WHERE followers.follower_id = auth.uid()
            AND followers.following_id = posts.user_id
        )
    );

-- Users can see their own posts
CREATE POLICY "See own posts" ON public.posts
    FOR SELECT TO authenticated
    USING (auth.uid() = user_id);

-- Users can see public posts
CREATE POLICY "See public posts" ON public.posts
    FOR SELECT TO authenticated
    USING (visibility = 'public');
```

## Performance Optimization

### Use Indexes for RLS Conditions

```sql
-- Index columns used in RLS policies
CREATE INDEX posts_user_id_idx ON public.posts(user_id);
CREATE INDEX org_members_user_id_idx ON public.org_members(user_id);
CREATE INDEX org_members_org_id_idx ON public.org_members(org_id);

-- Composite indexes for complex policies
CREATE INDEX posts_user_status_idx ON public.posts(user_id, status);
```

### Use Security Definer Functions Carefully

```sql
-- Instead of complex policy logic, use a function
CREATE OR REPLACE FUNCTION public.can_access_post(post_id UUID)
RETURNS BOOLEAN AS $$
    -- Complex logic here
    SELECT EXISTS (
        SELECT 1 FROM public.posts p
        LEFT JOIN public.org_members om ON om.org_id = p.org_id
        WHERE p.id = post_id
        AND (
            p.user_id = auth.uid() OR
            (om.user_id = auth.uid() AND om.role IN ('admin', 'owner'))
        )
    );
$$ LANGUAGE sql STABLE SECURITY DEFINER;

-- Use in policy
CREATE POLICY "Access control" ON public.posts
    FOR SELECT TO authenticated
    USING (can_access_post(id));
```

## Testing RLS Policies

### Test as Different Users

```sql
-- Set role to test as specific user
SET LOCAL role TO authenticated;
SET LOCAL request.jwt.claim.sub TO 'user-uuid-here';

-- Test query
SELECT * FROM public.posts;

-- Reset
RESET role;
```

### Create Test Users

```sql
-- Create test users in auth.users
INSERT INTO auth.users (id, email, encrypted_password, email_confirmed_at)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'test1@example.com', crypt('password', gen_salt('bf')), now()),
    ('22222222-2222-2222-2222-222222222222', 'test2@example.com', crypt('password', gen_salt('bf')), now());
```

## Common Pitfalls

1. **Forgetting to enable RLS** - Tables without RLS are fully accessible
2. **No policies = no access** - At least one policy must match for access
3. **Service role bypasses RLS** - Be careful with service_role key
4. **Complex policies are slow** - Use indexes and consider denormalization
5. **USING vs WITH CHECK** - USING for reads, WITH CHECK for writes
6. **Infinite recursion** - Avoid policies that query the same table
7. **NULL handling** - Remember NULL doesn't equal anything, including NULL

## Best Practices

1. **Always enable RLS** on tables with user data
2. **Use FORCE ROW LEVEL SECURITY** to prevent owner bypass
3. **Create separate policies** for each operation (SELECT, INSERT, UPDATE, DELETE)
4. **Index columns** used in policy conditions
5. **Test policies** with different user scenarios
6. **Document complex policies** with comments
7. **Use functions** for complex logic reuse
8. **Monitor performance** of policies
9. **Start restrictive** (deny by default) then open up as needed
10. **Version control** all RLS policies in migrations
