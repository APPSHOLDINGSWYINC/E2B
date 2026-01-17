import { describe, expect, test } from 'vitest'
import { getConfigPath } from '../../src/config/index'

describe('Path Traversal Prevention - Config', () => {
  test('getConfigPath should prevent path traversal', () => {
    const root = '/home/user/project'
    
    // Should reject path traversal attempts
    expect(() => {
      getConfigPath(root, '../../../etc/passwd')
    }).toThrow('Path traversal detected')
  })

  test('getConfigPath should allow valid relative paths', () => {
    const root = '/home/user/project'
    
    // Should allow valid paths within the directory
    const result = getConfigPath(root, 'config/e2b.toml')
    expect(result).toMatch(/project/)
    expect(result).not.toMatch(/\.\./)
  })

  test('getConfigPath should handle absolute paths', () => {
    const root = '/home/user/project'
    const absolutePath = '/some/absolute/path/config.toml'
    
    // Absolute paths should be returned as-is (per existing behavior)
    const result = getConfigPath(root, absolutePath)
    expect(result).toBe(absolutePath)
  })
})
