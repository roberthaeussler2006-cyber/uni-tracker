import { NextResponse } from 'next/server'
import { createToken } from '@/lib/auth'

export async function POST(request: Request) {
  const { pin } = await request.json()
  const correctPin = process.env.DASHBOARD_PIN

  if (!correctPin) {
    return NextResponse.json({ error: 'Server misconfigured' }, { status: 500 })
  }

  if (pin !== correctPin) {
    return NextResponse.json({ error: 'Invalid PIN' }, { status: 401 })
  }

  const token = createToken()
  const response = NextResponse.json({ success: true })
  response.cookies.set('tracker_auth', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60 * 24 * 30, // 30 days
  })

  return response
}
