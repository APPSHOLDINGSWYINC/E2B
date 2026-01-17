import * as path from 'path'

/**
 * Validates and normalizes a path to prevent path traversal attacks.
 * Ensures that the resolved path is within the base directory.
 * 
 * @param {string} basePath - The base directory path that should contain the resolved path
 * @param {string} userPath - The user-provided path (can be relative or absolute)
 * @returns {string} The normalized absolute path
 * @throws {Error} if path traversal is detected or path is outside the base directory
 */
export function validateAndNormalizePath(basePath, userPath) {
  // Resolve both paths to absolute paths
  const resolvedBase = path.resolve(basePath)
  const resolvedPath = path.resolve(basePath, userPath)
  
  // Check if the resolved path is within the base directory
  // We need to check both cases: exact match or child path
  if (resolvedPath !== resolvedBase && !resolvedPath.startsWith(resolvedBase + path.sep)) {
    throw new Error(`Path traversal detected: ${userPath} is outside the allowed directory`)
  }
  
  return resolvedPath
}
