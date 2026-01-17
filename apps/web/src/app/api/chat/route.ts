import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { messages } = await request.json()

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json(
        { error: 'Invalid messages format' },
        { status: 400 }
      )
    }

    // Mock response for now - replace with actual Claude API integration when API keys are available
    const mockResponse = `Hello! I'm AgentX5 Assistant. I received your message. To enable full AI functionality, please add your ANTHROPIC_API_KEY to the environment variables.

Your message: "${messages[messages.length - 1]?.content || ''}"

I have access to 219 specialized agents for:
- Code execution and analysis
- Legal document processing
- Financial data analysis
- Multi-format data parsing
- And much more!`

    return NextResponse.json({
      message: mockResponse,
      usage: { input_tokens: 0, output_tokens: 0 },
    })
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      {
        error: 'Failed to process chat request',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    )
  }
}

export const runtime = 'nodejs'
export const maxDuration = 60
