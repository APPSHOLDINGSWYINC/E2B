// Environment variable validation for production deployments
// This helps catch missing environment variables early

export function validateEnv() {
  const requiredVars = ['E2B_API_KEY', 'NEXT_PUBLIC_API_URL']
  const missingVars = requiredVars.filter((varName) => !process.env[varName])

  if (missingVars.length > 0) {
    console.error('❌ Missing required environment variables:', missingVars)
    // Don't throw in production to avoid breaking the build
    // Just log the warning
    if (process.env.NODE_ENV !== 'production') {
      console.warn('⚠️  Application may not work correctly without these variables')
    }
  } else {
    console.log('✅ Environment variables validated')
  }
}

// Optional: Call this in the app initialization
if (typeof window === 'undefined') {
  // Only validate on server side
  validateEnv()
}
