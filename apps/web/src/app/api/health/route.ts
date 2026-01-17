import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'E2B Web Application',
    version: '1.0.0',
  })
}

export const runtime = 'nodejs'
