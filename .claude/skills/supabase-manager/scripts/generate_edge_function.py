#!/usr/bin/env python3
"""
Supabase Edge Function Generator

Generates Edge Function templates with common patterns.
"""

import sys
import json

EDGE_FUNCTION_TEMPLATES = {
    'basic': '''// Basic Edge Function
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  try {
    const { name } = await req.json()
    
    const data = {
      message: `Hello ${name}!`,
    }

    return new Response(
      JSON.stringify(data),
      { headers: { "Content-Type": "application/json" } },
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    )
  }
})
''',
    
    'with_supabase': '''// Edge Function with Supabase Client
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Create Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    )

    // Get user from auth header
    const { data: { user } } = await supabaseClient.auth.getUser()
    
    if (!user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    // Your logic here
    const { data, error } = await supabaseClient
      .from('your_table')
      .select('*')
      .eq('user_id', user.id)

    if (error) throw error

    return new Response(
      JSON.stringify({ data }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } },
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
''',
    
    'webhook': '''// Webhook Handler Edge Function
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    // Verify webhook signature
    const signature = req.headers.get('X-Webhook-Signature')
    const webhookSecret = Deno.env.get('WEBHOOK_SECRET')
    
    if (signature !== webhookSecret) {
      return new Response(
        JSON.stringify({ error: 'Invalid signature' }),
        { status: 401, headers: { 'Content-Type': 'application/json' } }
      )
    }

    // Parse webhook payload
    const payload = await req.json()
    
    // Create Supabase client with service role
    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Process webhook
    const { data, error } = await supabaseAdmin
      .from('webhook_logs')
      .insert({
        event_type: payload.type,
        payload: payload,
        processed_at: new Date().toISOString()
      })

    if (error) throw error

    return new Response(
      JSON.stringify({ success: true, data }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    console.error('Webhook error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    )
  }
})
''',
    
    'scheduled': '''// Scheduled Edge Function (triggered by pg_cron or external scheduler)
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    // Verify cron secret
    const authHeader = req.headers.get('Authorization')
    const cronSecret = Deno.env.get('CRON_SECRET')
    
    if (authHeader !== `Bearer ${cronSecret}`) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401, headers: { 'Content-Type': 'application/json' } }
      )
    }

    // Create admin client
    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Perform scheduled task
    // Example: Clean up old records
    const thirtyDaysAgo = new Date()
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

    const { data, error } = await supabaseAdmin
      .from('temporary_data')
      .delete()
      .lt('created_at', thirtyDaysAgo.toISOString())

    if (error) throw error

    console.log(`Cleaned up ${data?.length || 0} records`)

    return new Response(
      JSON.stringify({ 
        success: true, 
        deleted: data?.length || 0 
      }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    console.error('Scheduled task error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    )
  }
})
''',
    
    'stripe_webhook': '''// Stripe Webhook Handler
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import Stripe from 'https://esm.sh/stripe@13.0.0?target=deno'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY') || '', {
  apiVersion: '2023-10-16',
})

serve(async (req) => {
  try {
    const signature = req.headers.get('stripe-signature')
    const webhookSecret = Deno.env.get('STRIPE_WEBHOOK_SECRET')
    
    if (!signature || !webhookSecret) {
      return new Response('Missing signature', { status: 400 })
    }

    const body = await req.text()
    const event = stripe.webhooks.constructEvent(body, signature, webhookSecret)

    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Handle different event types
    switch (event.type) {
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
        const subscription = event.data.object
        await supabaseAdmin
          .from('subscriptions')
          .upsert({
            stripe_subscription_id: subscription.id,
            stripe_customer_id: subscription.customer,
            status: subscription.status,
            price_id: subscription.items.data[0].price.id,
            current_period_start: new Date(subscription.current_period_start * 1000).toISOString(),
            current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
          })
        break

      case 'customer.subscription.deleted':
        const deletedSub = event.data.object
        await supabaseAdmin
          .from('subscriptions')
          .update({ status: 'canceled' })
          .eq('stripe_subscription_id', deletedSub.id)
        break

      case 'invoice.payment_succeeded':
        const invoice = event.data.object
        // Handle successful payment
        break

      case 'invoice.payment_failed':
        const failedInvoice = event.data.object
        // Handle failed payment
        break
    }

    return new Response(JSON.stringify({ received: true }), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    console.error('Stripe webhook error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    )
  }
})
''',
    
    'file_upload': '''// File Upload Handler
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    )

    const { data: { user } } = await supabaseClient.auth.getUser()
    
    if (!user) {
      return new Response('Unauthorized', { status: 401, headers: corsHeaders })
    }

    const formData = await req.formData()
    const file = formData.get('file') as File
    
    if (!file) {
      return new Response('No file provided', { status: 400, headers: corsHeaders })
    }

    // Validate file
    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      return new Response('File too large', { status: 400, headers: corsHeaders })
    }

    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
    if (!allowedTypes.includes(file.type)) {
      return new Response('Invalid file type', { status: 400, headers: corsHeaders })
    }

    // Upload to storage
    const fileName = `${user.id}/${Date.now()}_${file.name}`
    const { data, error } = await supabaseClient.storage
      .from('uploads')
      .upload(fileName, file, {
        contentType: file.type,
        upsert: false
      })

    if (error) throw error

    // Get public URL
    const { data: { publicUrl } } = supabaseClient.storage
      .from('uploads')
      .getPublicUrl(fileName)

    // Save metadata to database
    await supabaseClient.from('files').insert({
      user_id: user.id,
      file_name: file.name,
      file_path: fileName,
      file_size: file.size,
      file_type: file.type,
      public_url: publicUrl
    })

    return new Response(
      JSON.stringify({ url: publicUrl, path: fileName }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
'''
}

def generate_edge_function(template_type, function_name, config=None):
    """Generate edge function code"""
    
    if template_type not in EDGE_FUNCTION_TEMPLATES:
        return f"// Unknown template: {template_type}\n// Available: {', '.join(EDGE_FUNCTION_TEMPLATES.keys())}"
    
    code = EDGE_FUNCTION_TEMPLATES[template_type]
    
    # Apply any customizations from config
    if config:
        for key, value in config.items():
            code = code.replace(f'{{{key}}}', str(value))
    
    return code

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_edge_function.py '<config_json>'")
        print("\nExamples:")
        print("\n1. Basic function:")
        print(json.dumps({
            'template': 'basic',
            'function_name': 'hello-world'
        }, indent=2))
        print("\n2. With Supabase client:")
        print(json.dumps({
            'template': 'with_supabase',
            'function_name': 'get-user-data'
        }, indent=2))
        print("\n3. Webhook handler:")
        print(json.dumps({
            'template': 'webhook',
            'function_name': 'process-webhook'
        }, indent=2))
        print("\nAvailable templates:")
        for template in EDGE_FUNCTION_TEMPLATES.keys():
            print(f"  - {template}")
        sys.exit(1)
    
    config = json.loads(sys.argv[1])
    template_type = config.get('template', 'basic')
    function_name = config.get('function_name', 'my-function')
    
    code = generate_edge_function(template_type, function_name, config)
    
    result = {
        'function_name': function_name,
        'code': code,
        'command': f'supabase functions new {function_name}'
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
