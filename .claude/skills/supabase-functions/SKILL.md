---
name: supabase-functions
description: Supabase edge functions development - Deno functions, webhooks, scheduled tasks, and API integrations. Use when (1) Creating edge functions, (2) Building webhooks, (3) Implementing scheduled tasks, (4) Integrating external APIs, (5) Building serverless API routes, (6) Processing background jobs. DO NOT use for database schema or migrations - use supabase-database instead. Focus: Deno edge functions, API routes, and serverless compute.
---

# Supabase Edge Functions

Comprehensive toolkit for building and deploying Supabase Edge Functions - serverless Deno functions for webhooks, APIs, and background processing.

## When to Use This Skill

Use supabase-functions when you need to:

- **Create edge functions** for serverless compute
- **Build webhooks** to receive external events (Stripe, GitHub, etc.)
- **Implement scheduled tasks** (cron jobs, background processing)
- **Integrate external APIs** (OpenAI, SendGrid, Stripe, etc.)
- **Build serverless API routes** for business logic
- **Process background jobs** (email sending, data processing)
- **Handle file uploads** with validation and processing
- **Implement custom authentication flows**

## When NOT to Use This Skill

**DO NOT use supabase-functions for:**

- **Database migrations or schema** → Use `supabase-database` skill instead
- **RLS policies or security rules** → Use `supabase-database` skill instead
- **Table design or indexes** → Use `supabase-database` skill instead
- **Pure database queries** → Use `supabase-database` unless part of function logic

**Clear separation:**

- `supabase-database` = Database structure, migrations, RLS (data layer)
- `supabase-functions` = Serverless compute, webhooks, APIs (logic layer)

**Workflow:** Often use both - database for schema, functions for business logic

## Quick Start

### Create Edge Function

```bash
# Generate edge function from template
python scripts/generate_edge_function.py '{
  "template": "with_supabase",
  "function_name": "my-function"
}'
```

### Local Testing

```bash
# Serve function locally
supabase functions serve my-function

# Serve with specific port
supabase functions serve my-function --env-file ./supabase/.env.local

# Test the function
curl -i --location --request POST 'http://localhost:54321/functions/v1/my-function' \
  --header 'Authorization: Bearer YOUR_ANON_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"name":"Functions"}'
```

### Deploy Function

```bash
# Deploy to production
supabase functions deploy my-function

# Deploy with secrets
supabase secrets set MY_SECRET_KEY=value
supabase functions deploy my-function
```

## Scripts

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

## Common Patterns

### Edge Function with Auth

```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers':
    'authorization, x-client-info, apikey, content-type',
}

serve(async req => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Create Supabase client with user's auth
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    )

    // Verify user authentication
    const {
      data: { user },
    } = await supabaseClient.auth.getUser()

    if (!user) {
      return new Response('Unauthorized', { status: 401, headers: corsHeaders })
    }

    // Your logic here
    const { data, error } = await supabaseClient.from('your_table').select('*')

    if (error) throw error

    return new Response(JSON.stringify({ data }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  }
})
```

### Webhook Handler with Signature Verification

```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createHmac } from 'https://deno.land/std@0.168.0/node/crypto.ts'

serve(async req => {
  try {
    const signature = req.headers.get('x-webhook-signature')
    const body = await req.text()

    // Verify webhook signature
    const secret = Deno.env.get('WEBHOOK_SECRET') ?? ''
    const hmac = createHmac('sha256', secret)
    hmac.update(body)
    const expectedSignature = hmac.digest('hex')

    if (signature !== expectedSignature) {
      return new Response('Invalid signature', { status: 401 })
    }

    // Process webhook
    const payload = JSON.parse(body)

    // Your webhook logic here
    console.log('Webhook received:', payload)

    return new Response(JSON.stringify({ received: true }), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
})
```

### Scheduled Task / Cron Job

```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async req => {
  try {
    // Verify it's a cron request (check authorization or headers)
    const authHeader = req.headers.get('Authorization')
    if (authHeader !== `Bearer ${Deno.env.get('CRON_SECRET')}`) {
      return new Response('Unauthorized', { status: 401 })
    }

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Your scheduled task logic
    // Example: Clean up old records
    const { error } = await supabase
      .from('temp_data')
      .delete()
      .lt(
        'created_at',
        new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
      )

    if (error) throw error

    return new Response(JSON.stringify({ success: true }), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
})
```

### File Upload with Validation

```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

serve(async req => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    )

    const {
      data: { user },
    } = await supabase.auth.getUser()
    if (!user) throw new Error('Unauthorized')

    // Get file from request
    const formData = await req.formData()
    const file = formData.get('file') as File

    // Validate file
    if (!file) throw new Error('No file provided')
    if (file.size > MAX_FILE_SIZE) throw new Error('File too large')
    if (!ALLOWED_TYPES.includes(file.type)) throw new Error('Invalid file type')

    // Upload to storage
    const filePath = `${user.id}/${crypto.randomUUID()}-${file.name}`
    const { data, error } = await supabase.storage
      .from('avatars')
      .upload(filePath, file)

    if (error) throw error

    return new Response(JSON.stringify({ path: data.path }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  }
})
```

### Stripe Webhook Integration

```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import Stripe from 'https://esm.sh/stripe@13.5.0'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY') ?? '', {
  apiVersion: '2023-08-16',
})

serve(async req => {
  const signature = req.headers.get('stripe-signature')
  const body = await req.text()

  try {
    // Verify Stripe signature
    const event = stripe.webhooks.constructEvent(
      body,
      signature!,
      Deno.env.get('STRIPE_WEBHOOK_SECRET') ?? ''
    )

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Handle different event types
    switch (event.type) {
      case 'checkout.session.completed':
        const session = event.data.object
        // Update user subscription in database
        await supabase
          .from('subscriptions')
          .update({ status: 'active' })
          .eq('stripe_session_id', session.id)
        break

      case 'customer.subscription.deleted':
        const subscription = event.data.object
        // Cancel subscription in database
        await supabase
          .from('subscriptions')
          .update({ status: 'canceled' })
          .eq('stripe_subscription_id', subscription.id)
        break
    }

    return new Response(JSON.stringify({ received: true }), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    })
  }
})
```

## Best Practices

### Edge Functions

1. **Use CORS headers** - For web requests, always include CORS
2. **Verify authentication** - Check user from JWT token
3. **Handle errors** - Try-catch with proper HTTP status codes
4. **Use secrets** - Never hardcode API keys, use `supabase secrets`
5. **Test locally first** - Use `supabase functions serve` before deploying

### Security

1. **Validate input** - Always validate request body and parameters
2. **Verify signatures** - For webhooks, verify signatures (Stripe, GitHub, etc.)
3. **Use service role carefully** - Only when needed, prefer user context
4. **Rate limiting** - Implement rate limiting for public endpoints
5. **HTTPS only** - Edge functions automatically use HTTPS

### Performance

1. **Keep functions small** - Single responsibility principle
2. **Minimize cold starts** - Import only what you need
3. **Use caching** - Cache external API responses when possible
4. **Async operations** - Use Promise.all for parallel operations
5. **Monitor logs** - Use Supabase dashboard to monitor function performance

## Troubleshooting

### Function Errors

```bash
# Check function logs locally
supabase functions serve my-function --debug

# View deployed function logs (in Supabase dashboard)
# Functions > my-function > Logs
```

### CORS Issues

```typescript
// Always include CORS headers
const corsHeaders = {
  'Access-Control-Allow-Origin': '*', // Or specify your domain
  'Access-Control-Allow-Headers':
    'authorization, x-client-info, apikey, content-type',
}

// Handle OPTIONS request
if (req.method === 'OPTIONS') {
  return new Response('ok', { headers: corsHeaders })
}
```

### Authentication Issues

```typescript
// Debug auth issues
const {
  data: { user },
  error,
} = await supabaseClient.auth.getUser()

if (error) {
  console.error('Auth error:', error)
  return new Response(JSON.stringify({ error: 'Auth failed' }), {
    status: 401,
    headers: corsHeaders,
  })
}

if (!user) {
  return new Response(JSON.stringify({ error: 'No user' }), {
    status: 401,
    headers: corsHeaders,
  })
}
```

## CLI Quick Reference

```bash
# Create function
supabase functions new my-function

# Serve locally
supabase functions serve my-function
supabase functions serve my-function --env-file ./supabase/.env.local

# Deploy
supabase functions deploy my-function
supabase functions deploy my-function --no-verify-jwt

# Manage secrets
supabase secrets set MY_SECRET=value
supabase secrets list
supabase secrets unset MY_SECRET

# Delete function
supabase functions delete my-function
```

## Working with Database

When your edge function needs to interact with the database:

1. Use `supabase-database` to create schema and RLS policies
2. Use `supabase-functions` (this skill) to create the edge function
3. Import Supabase client in function to query/mutate data
4. RLS policies automatically apply to function queries (unless using service role)

**Example workflow:**

```bash
# Step 1: Create schema (supabase-database skill)
# Created posts table with RLS policies

# Step 2: Create edge function (this skill)
python scripts/generate_edge_function.py '{
  "template": "with_supabase",
  "function_name": "create-post"
}'

# Function automatically respects RLS policies from database
```

## Deno Runtime

Edge Functions run on Deno, not Node.js:

```typescript
// ✅ Use Deno standard library
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

// ✅ Use ESM CDN for npm packages
import Stripe from 'https://esm.sh/stripe@13.5.0'

// ✅ Access environment variables
Deno.env.get('MY_SECRET')

// ❌ Don't use Node.js require
// const stripe = require('stripe') // This won't work
```

For database schema and migrations, use the `supabase-database` skill.
For quick reference and skill selection, see `supabase-quickref`.

This skill provides everything needed to build and deploy serverless Supabase Edge Functions effectively.
