import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { password } = await request.json();

  const adminPassword = process.env.ADMIN_PASSWORD;

  if (!adminPassword) {
    // If no password is set, deny access
    return NextResponse.json({ error: 'Not configured' }, { status: 500 });
  }

  if (password === adminPassword) {
    return NextResponse.json({ success: true });
  }

  return NextResponse.json({ error: 'Invalid password' }, { status: 401 });
}
