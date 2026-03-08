import { cookies } from 'next/headers'

const AUTH_COOKIE = 'tracker_auth'

export function createToken(): string {
  const secret = process.env.AUTH_SECRET || 'default-secret'
  // Simple token: timestamp + secret hash
  const payload = `${Date.now()}-${secret}`
  return Buffer.from(payload).toString('base64')
}

export function verifyToken(token: string): boolean {
  try {
    const decoded = Buffer.from(token, 'base64').toString()
    const secret = process.env.AUTH_SECRET || 'default-secret'
    return decoded.includes(secret)
  } catch {
    return false
  }
}

export async function isAuthenticated(): Promise<boolean> {
  const cookieStore = await cookies()
  const token = cookieStore.get(AUTH_COOKIE)?.value
  if (!token) return false
  return verifyToken(token)
}
