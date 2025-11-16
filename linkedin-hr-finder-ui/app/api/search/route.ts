import { NextRequest, NextResponse } from 'next/server'
import type { SearchParams, SearchResponse } from '@/lib/types'

export async function POST(request: NextRequest) {
  try {
    const body: SearchParams = await request.json()

    // Validate required fields
    if (!body.company_name) {
      return NextResponse.json(
        { success: false, error: 'Company name is required' },
        { status: 400 }
      )
    }

    // Get n8n webhook URL from environment or use default
    const n8nUrl = process.env.N8N_WEBHOOK_URL || 'http://localhost:5678/webhook/linkedin-hr-finder'

    console.log('Calling n8n webhook:', n8nUrl)
    console.log('Request body:', JSON.stringify(body, null, 2))

    // Call n8n webhook
    const response = await fetch(n8nUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('n8n webhook error:', errorText)
      return NextResponse.json(
        {
          success: false,
          error: `Failed to fetch from n8n: ${response.status} ${response.statusText}`,
          details: errorText,
        },
        { status: response.status }
      )
    }

    const data: SearchResponse = await response.json()

    console.log('n8n response:', JSON.stringify(data, null, 2))

    return NextResponse.json(data)
  } catch (error: any) {
    console.error('API error:', error)
    return NextResponse.json(
      {
        success: false,
        error: 'Internal server error',
        details: error.message,
      },
      { status: 500 }
    )
  }
}
