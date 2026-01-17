import * as path from 'path'
import { describe, expect, test } from 'vitest'
import { validateAndNormalizePath } from '../../src/utils/filesystem'

describe('validateAndNormalizePath', () => {
  const baseDir = '/home/user/project'

  describe('Valid paths', () => {
    test('should allow path within base directory', () => {
      const result = validateAndNormalizePath(baseDir, 'src/file.ts')
      expect(result).toBe(path.join(baseDir, 'src/file.ts'))
    })

    test('should allow nested path within base directory', () => {
      const result = validateAndNormalizePath(baseDir, 'src/nested/deep/file.ts')
      expect(result).toBe(path.join(baseDir, 'src/nested/deep/file.ts'))
    })

    test('should allow current directory reference', () => {
      const result = validateAndNormalizePath(baseDir, '.')
      expect(result).toBe(baseDir)
    })

    test('should allow current directory with file', () => {
      const result = validateAndNormalizePath(baseDir, './file.ts')
      expect(result).toBe(path.join(baseDir, 'file.ts'))
    })

    test('should allow simple filename', () => {
      const result = validateAndNormalizePath(baseDir, 'file.ts')
      expect(result).toBe(path.join(baseDir, 'file.ts'))
    })

    test('should normalize path with redundant separators', () => {
      const result = validateAndNormalizePath(baseDir, 'src//file.ts')
      expect(result).toBe(path.join(baseDir, 'src/file.ts'))
    })

    test('should handle path with . segments', () => {
      const result = validateAndNormalizePath(baseDir, './src/./file.ts')
      expect(result).toBe(path.join(baseDir, 'src/file.ts'))
    })
  })

  describe('Path traversal attacks', () => {
    test('should reject path with .. going outside base directory', () => {
      expect(() => {
        validateAndNormalizePath(baseDir, '../outside.ts')
      }).toThrow('Path traversal detected')
    })

    test('should reject path with multiple .. going outside', () => {
      expect(() => {
        validateAndNormalizePath(baseDir, '../../outside.ts')
      }).toThrow('Path traversal detected')
    })

    test('should reject path with .. after valid segments', () => {
      expect(() => {
        validateAndNormalizePath(baseDir, 'src/../../outside.ts')
      }).toThrow('Path traversal detected')
    })

    test('should reject deeply nested path traversal', () => {
      expect(() => {
        validateAndNormalizePath(baseDir, 'src/nested/../../../outside.ts')
      }).toThrow('Path traversal detected')
    })

    test('should reject attempt to access /etc/passwd', () => {
      expect(() => {
        validateAndNormalizePath(baseDir, '../../../etc/passwd')
      }).toThrow('Path traversal detected')
    })

    test('should reject absolute path to different location', () => {
      expect(() => {
        validateAndNormalizePath(baseDir, '/etc/passwd')
      }).toThrow('Path traversal detected')
    })

    test('should reject absolute path to root', () => {
      expect(() => {
        validateAndNormalizePath(baseDir, '/')
      }).toThrow('Path traversal detected')
    })
  })

  describe('Edge cases', () => {
    test('should allow .. that stays within base directory', () => {
      const result = validateAndNormalizePath(baseDir, 'src/../file.ts')
      expect(result).toBe(path.join(baseDir, 'file.ts'))
    })

    test('should allow multiple .. that stay within base directory', () => {
      const result = validateAndNormalizePath(baseDir, 'src/nested/../../file.ts')
      expect(result).toBe(path.join(baseDir, 'file.ts'))
    })

    test('should handle empty path as current directory', () => {
      const result = validateAndNormalizePath(baseDir, '')
      expect(result).toBe(baseDir)
    })

    test.skipIf(process.platform !== 'win32')('should work with Windows-style paths on Windows', () => {
      const winBase = 'C:\\Users\\user\\project'
      const result = validateAndNormalizePath(winBase, 'src\\file.ts')
      expect(result).toBe(path.join(winBase, 'src\\file.ts'))
    })

    test.skipIf(process.platform !== 'win32')('should reject path traversal on Windows', () => {
      const winBase = 'C:\\Users\\user\\project'
      expect(() => {
        validateAndNormalizePath(winBase, '..\\..\\..\\Windows\\System32')
      }).toThrow('Path traversal detected')
    })
  })

  describe('Relative base paths', () => {
    test('should work with relative base path', () => {
      const relativeBase = 'project'
      const result = validateAndNormalizePath(relativeBase, 'src/file.ts')
      expect(result).toBe(path.resolve(relativeBase, 'src/file.ts'))
    })

    test('should reject traversal with relative base path', () => {
      const relativeBase = 'project'
      expect(() => {
        validateAndNormalizePath(relativeBase, '../outside.ts')
      }).toThrow('Path traversal detected')
    })
  })
})
