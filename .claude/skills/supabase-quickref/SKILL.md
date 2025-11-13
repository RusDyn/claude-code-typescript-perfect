# Supabase Skills Quick Reference

## Which Skill Should I Use?

| Scenario                                      | Use This Skill               |
| --------------------------------------------- | ---------------------------- |
| Create database migrations, tables, or schema | **supabase-database**        |
| Implement RLS policies or security rules      | **supabase-database**        |
| Design table structures or add columns        | **supabase-database**        |
| Set up storage RLS or file permissions        | **supabase-database**        |
| Optimize queries, add indexes                 | **supabase-database**        |
| Create edge functions or API routes           | **supabase-functions**       |
| Build webhooks (Stripe, GitHub, etc.)         | **supabase-functions**       |
| Implement scheduled tasks / cron jobs         | **supabase-functions**       |
| Integrate external APIs (OpenAI, SendGrid)    | **supabase-functions**       |
| Process file uploads with validation          | **supabase-functions**       |
| Need quick reference or unsure which to use   | **supabase-quickref** (this) |

## Common Workflows

### 1. Database Schema Work (Database Only)

```bash
# Scenario: Add a new table with RLS

# Use: supabase-database skill
1. Create migration: supabase migration new add_posts_table
2. Generate migration SQL with script or write manually
3. Enable RLS and add policies
4. Test locally: supabase db reset
5. Push to remote: supabase db push
```

### 2. Serverless API / Webhook (Functions Only)

```bash
# Scenario: Build a Stripe webhook handler

# Use: supabase-functions skill
1. Generate function: python scripts/generate_edge_function.py
2. Implement webhook logic with signature verification
3. Test locally: supabase functions serve webhook-handler
4. Deploy: supabase functions deploy webhook-handler
```

### 3. Full Feature (Database + Functions)

```bash
# Scenario: Add notification system

# Step 1: Database schema (supabase-database skill)
1. Create notifications table with RLS
2. Add migration for schema
3. Set up RLS policies for user access

# Step 2: Edge function (supabase-functions skill)
4. Create edge function to send notifications
5. Function queries notifications table
6. RLS policies automatically apply
```

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│           Supabase Project                   │
├─────────────────────────────────────────────┤
│                                              │
│  ┌────────────────────────────────────┐    │
│  │  DATABASE LAYER                     │    │
│  │  (supabase-database skill)          │    │
│  ├────────────────────────────────────┤    │
│  │  • Tables & Schema                  │    │
│  │  • Migrations                       │    │
│  │  • RLS Policies                     │    │
│  │  • Indexes & Performance            │    │
│  │  • Storage RLS                      │    │
│  │  • Realtime Subscriptions           │    │
│  └────────────────────────────────────┘    │
│                    ▲                         │
│                    │ (queries with RLS)      │
│                    │                         │
│  ┌────────────────────────────────────┐    │
│  │  SERVERLESS LAYER                   │    │
│  │  (supabase-functions skill)         │    │
│  ├────────────────────────────────────┤    │
│  │  • Edge Functions                   │    │
│  │  • Webhooks                         │    │
│  │  • Scheduled Tasks                  │    │
│  │  • API Integrations                 │    │
│  │  • File Processing                  │    │
│  └────────────────────────────────────┘    │
│                                              │
└─────────────────────────────────────────────┘
```

## Decision Tree

```
START: What are you trying to do?

├─ "I need to store data"
│  └─> Use supabase-database
│      └─ Create tables, migrations, RLS policies
│
├─ "I need to secure data access"
│  └─> Use supabase-database
│      └─ Implement RLS policies, row-level security
│
├─ "I need to process logic or call external APIs"
│  └─> Use supabase-functions
│      └─ Create edge functions for serverless compute
│
├─ "I need to receive webhooks from external services"
│  └─> Use supabase-functions
│      └─ Build webhook handlers with verification
│
├─ "I need both database AND functions"
│  └─> Use BOTH skills
│      ├─ supabase-database → schema, migrations, RLS
│      └─ supabase-functions → edge functions (queries database)
│
└─ "I'm not sure what I need"
   └─> You're in the right place! (supabase-quickref)
```

## Quick CLI Commands

### Database Operations (supabase-database skill)

```bash
# Project setup
supabase init
supabase start
supabase link --project-ref <ref>

# Migrations
supabase migration new <name>
supabase migration list
supabase db reset              # Apply migrations locally
supabase db push               # Push to remote
supabase db pull               # Pull remote schema
supabase db diff               # View differences

# Types
supabase gen types typescript --local > types/supabase.ts
```

### Functions Operations (supabase-functions skill)

```bash
# Create & deploy
supabase functions new <name>
supabase functions serve <name>
supabase functions deploy <name>
supabase functions delete <name>

# Secrets
supabase secrets set KEY=value
supabase secrets list
supabase secrets unset KEY
```

## Skill Composition Examples

### Example 1: User Profile System

**Requirements:** Store user profiles with avatar upload

```bash
# Step 1: Database (supabase-database)
- Create profiles table
- Add RLS policies (users can read all, update own)
- Create storage.objects RLS for avatars

# Step 2: Functions (supabase-functions)
- Create upload-avatar edge function
- Validates file type and size
- Stores in supabase storage
- Updates profile table
```

**Which skills:** Both (database for schema, functions for upload logic)

---

### Example 2: Scheduled Data Cleanup

**Requirements:** Delete old temporary records daily

```bash
# Step 1: Database (supabase-database)
- Ensure temp_data table exists with created_at timestamp
- Add index on created_at for performance

# Step 2: Functions (supabase-functions)
- Create cleanup-old-data scheduled function
- Runs daily via cron
- Deletes records older than 7 days
```

**Which skills:** Both (database for schema, functions for cron job)

---

### Example 3: Stripe Payment Integration

**Requirements:** Handle Stripe webhooks and update subscriptions

```bash
# Step 1: Database (supabase-database)
- Create subscriptions table
- Add RLS policies for user access
- Add indexes on stripe_subscription_id

# Step 2: Functions (supabase-functions)
- Create stripe-webhook edge function
- Verifies Stripe signature
- Updates subscriptions table based on events
```

**Which skills:** Both (database for subscriptions, functions for webhook)

---

### Example 4: Simple Table Addition

**Requirements:** Add a tags table for categorization

```bash
# Only Step 1: Database (supabase-database)
- Create migration for tags table
- Add RLS policies
- Add indexes
- Test and deploy

# No function needed - just database work
```

**Which skills:** Only supabase-database

---

### Example 5: Third-Party API Call

**Requirements:** Fetch data from OpenAI API on demand

```bash
# Step 1: Functions (supabase-functions)
- Create openai-completion edge function
- Calls OpenAI API with user prompt
- Returns completion result

# Optionally: Database (supabase-database)
- If you want to log/cache API responses
- Create api_logs table
```

**Which skills:** Primarily supabase-functions (add database if logging needed)

## Common Patterns

### Pattern 1: User-Owned Data

```sql
-- Database (supabase-database)
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  content TEXT
);

-- RLS Policy
CREATE POLICY "Users manage own posts"
  ON posts FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
```

```typescript
// Function (supabase-functions)
// Automatically respects RLS policy above
const { data } = await supabase.from('posts').select('*')
// User only sees their own posts due to RLS
```

---

### Pattern 2: Background Processing

```typescript
// Function (supabase-functions) - Scheduled Task
serve(async req => {
  const supabase = createClient(url, serviceRoleKey)

  // Process pending items
  const { data: pending } = await supabase
    .from('pending_tasks')
    .select('*')
    .eq('status', 'pending')
    .limit(100)

  for (const task of pending) {
    // Process task
    await processTask(task)

    // Update status
    await supabase
      .from('pending_tasks')
      .update({ status: 'completed' })
      .eq('id', task.id)
  }

  return new Response(JSON.stringify({ processed: pending.length }))
})
```

---

### Pattern 3: Webhook → Database Update

```typescript
// Function (supabase-functions) - Webhook Handler
serve(async req => {
  // Verify webhook signature
  const verified = verifySignature(req)
  if (!verified) return new Response('Unauthorized', { status: 401 })

  const event = await req.json()

  const supabase = createClient(url, serviceRoleKey)

  // Update database based on webhook event
  if (event.type === 'payment.succeeded') {
    await supabase.from('payments').insert({
      user_id: event.user_id,
      amount: event.amount,
      status: 'completed',
    })
  }

  return new Response(JSON.stringify({ received: true }))
})
```

## Best Practices

### When to Use Database vs Functions

**Use supabase-database when:**

- ✅ Defining data structure
- ✅ Setting up security (RLS)
- ✅ Optimizing query performance
- ✅ Managing schema changes

**Use supabase-functions when:**

- ✅ Processing business logic
- ✅ Calling external APIs
- ✅ Handling webhooks
- ✅ Running scheduled tasks
- ✅ Complex data transformations

**Use BOTH when:**

- ✅ Building complete features
- ✅ Functions need to query database
- ✅ Webhooks update database
- ✅ Scheduled tasks process database records

### Skill Selection Checklist

**Before starting, ask:**

1. Do I need to change database structure? → supabase-database
2. Do I need to implement security rules? → supabase-database
3. Do I need serverless compute? → supabase-functions
4. Do I need to call external APIs? → supabase-functions
5. Do I need both data and logic? → Both skills

## Troubleshooting

### "Should I use database or functions?"

**Ask yourself:**

- Is this about DATA STORAGE? → supabase-database
- Is this about DATA PROCESSING/LOGIC? → supabase-functions
- Both? → Use both skills

### "My function can't access the database"

```typescript
// Functions automatically query with user context
// RLS policies apply!

// For admin operations, use service role key
const supabase = createClient(
  Deno.env.get('SUPABASE_URL'),
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') // Bypasses RLS
)
```

### "Where do I put this code?"

| Code Type        | Location                        | Skill              |
| ---------------- | ------------------------------- | ------------------ |
| SQL migrations   | `supabase/migrations/*.sql`     | supabase-database  |
| RLS policies     | In migrations or direct SQL     | supabase-database  |
| Edge functions   | `supabase/functions/<name>/`    | supabase-functions |
| TypeScript types | `types/supabase.ts` (generated) | supabase-database  |
| Function secrets | `supabase secrets set`          | supabase-functions |

## Learning Path

### Beginner: Database First

1. Start with **supabase-database**
2. Learn migrations and RLS
3. Create simple tables
4. Then move to functions when needed

### Intermediate: Add Functions

1. Build your database schema
2. Add **supabase-functions** for APIs
3. Connect functions to database
4. RLS automatically applies

### Advanced: Full Stack

1. Design complex schemas with supabase-database
2. Build serverless APIs with supabase-functions
3. Integrate external services
4. Optimize performance with both skills

## Quick Links

- **Detailed Database Guide:** See `supabase-database/SKILL.md`
- **Detailed Functions Guide:** See `supabase-functions/SKILL.md`
- **Official Docs:** https://supabase.com/docs

---

**Remember:** Database for DATA, Functions for LOGIC. Often you need both! 🚀
