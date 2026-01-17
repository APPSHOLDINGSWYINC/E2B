import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname

  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-middleware-pathname', path)

  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  })

  // Cache static assets
  if (
    request.nextUrl.pathname.startsWith('/_next/static/') ||
    request.nextUrl.pathname.startsWith('/images/')
  ) {
    response.headers.set('Cache-Control', 'public, max-age=31536000, immutable')
  }

  // Cache API responses for 1 minute (only for GET requests)
  if (request.nextUrl.pathname.startsWith('/api/') && request.method === 'GET') {
    response.headers.set(
      'Cache-Control',
      'public, s-maxage=60, stale-while-revalidate=30'
    )
  }

  return response
}

export const config = {
  matcher: ['/docs/:path*', '/_next/static/:path*', '/images/:path*', '/api/:path*'],
}
