import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('tracker_auth')?.value

  // Allow login page and auth API
  if (
    request.nextUrl.pathname.startsWith('/login') ||
    request.nextUrl.pathname.startsWith('/api/auth')
  ) {
    // If already authenticated, redirect away from login
    if (request.nextUrl.pathname === '/login' && token && isValidToken(token)) {
      return NextResponse.redirect(new URL('/', request.url))
    }
    return NextResponse.next()
  }

  // Check auth for all other routes
  if (!token || !isValidToken(token)) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

function isValidToken(token: string): boolean {
  try {
    const decoded = Buffer.from(token, 'base64').toString()
    const secret = process.env.AUTH_SECRET || 'default-secret'
    return decoded.includes(secret)
  } catch {
    return false
  }
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
