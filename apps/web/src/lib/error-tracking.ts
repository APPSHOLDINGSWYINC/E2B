// Error tracking utility for monitoring production errors
// Can be integrated with services like Sentry, LogRocket, etc.

export function initErrorTracking() {
  if (typeof window !== 'undefined') {
    window.addEventListener('error', (event) => {
      console.error('Global error:', event.error)
      // Send to error tracking service (Sentry, LogRocket, etc.)
      logError(event.error, { type: 'global' })
    })

    window.addEventListener('unhandledrejection', (event) => {
      console.error('Unhandled promise rejection:', event.reason)
      logError(
        event.reason instanceof Error ? event.reason : new Error(String(event.reason)),
        { type: 'unhandledRejection' }
      )
    })
  }
}

export function logError(error: Error, context?: Record<string, any>) {
  console.error('Error:', error.message, context)

  // In production, send to error tracking service
  if (process.env.NODE_ENV === 'production') {
    // TODO: Integrate with Sentry or similar service
    // Sentry.captureException(error, { extra: context })
  }
}
