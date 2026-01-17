import { NextResponse } from 'next/server'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

export async function GET() {
  try {
    // Perform health checks
    const health = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      environment: process.env.NODE_ENV,
      vercel: process.env.VERCEL === '1',
      checks: {
        env: checkEnvironmentVariables(),
        runtime: 'ok',
      },
    }

    return NextResponse.json(health, { status: 200 })
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    )
  }
}

function checkEnvironmentVariables(): string {
  const required = ['E2B_API_KEY']
  const missing = required.filter((v) => !process.env[v])
  return missing.length === 0 ? 'ok' : `missing: ${missing.join(', ')}`
}
