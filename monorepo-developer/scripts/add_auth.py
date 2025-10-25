#!/usr/bin/env python3
"""
Add authentication to backend packages.
Supports: local, google, both
"""

import argparse
import sys
from pathlib import Path


def generate_local_auth() -> str:
    """Generate local authentication middleware."""
    return """import { Context, Next } from 'hono'
import { sign, verify } from 'hono/jwt'

export interface AuthPayload {
  id: string
  email: string
  name: string
  avatar_url?: string
}

export interface User extends AuthPayload {
  created_at: Date
  updated_at: Date
}

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'

export async function generateToken(payload: AuthPayload): Promise<string> {
  return sign(payload, JWT_SECRET)
}

export async function verifyToken(token: string): Promise<AuthPayload | null> {
  try {
    const payload = await verify(token, JWT_SECRET)
    return payload as AuthPayload
  } catch (error) {
    return null
  }
}

export async function authMiddleware(c: Context, next: Next) {
  const authHeader = c.req.header('Authorization')
  
  if (!authHeader) {
    return c.json({ error: 'Missing authorization header' }, 401)
  }

  const token = authHeader.replace('Bearer ', '')
  const payload = await verifyToken(token)

  if (!payload) {
    return c.json({ error: 'Invalid token' }, 401)
  }

  c.set('user', payload)
  await next()
}

export function getUser(c: Context): AuthPayload {
  return c.get('user')
}
"""


def generate_google_auth() -> str:
    """Generate Google OAuth authentication."""
    return """import { Context, Next } from 'hono'
import { sign, verify } from 'hono/jwt'

export interface GoogleAuthPayload {
  id: string
  email: string
  name: string
  picture: string
  avatar_url?: string
}

export interface User extends GoogleAuthPayload {
  created_at: Date
  updated_at: Date
}

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID || ''
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET || ''

export async function generateToken(payload: GoogleAuthPayload): Promise<string> {
  return sign(payload, JWT_SECRET)
}

export async function verifyToken(token: string): Promise<GoogleAuthPayload | null> {
  try {
    const payload = await verify(token, JWT_SECRET)
    return payload as GoogleAuthPayload
  } catch (error) {
    return null
  }
}

export async function verifyGoogleToken(token: string): Promise<GoogleAuthPayload | null> {
  try {
    const response = await fetch('https://www.googleapis.com/oauth2/v3/tokeninfo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `id_token=\${token}`
    })

    if (!response.ok) return null

    const data = await response.json()
    
    return {
      id: data.sub,
      email: data.email,
      name: data.name,
      picture: data.picture,
      avatar_url: data.picture
    }
  } catch (error) {
    return null
  }
}

export async function authMiddleware(c: Context, next: Next) {
  const authHeader = c.req.header('Authorization')
  
  if (!authHeader) {
    return c.json({ error: 'Missing authorization header' }, 401)
  }

  const token = authHeader.replace('Bearer ', '')
  const payload = await verifyToken(token)

  if (!payload) {
    return c.json({ error: 'Invalid token' }, 401)
  }

  c.set('user', payload)
  await next()
}

export function getUser(c: Context): GoogleAuthPayload {
  return c.get('user')
}
"""


def generate_combined_auth() -> str:
    """Generate combined local and Google authentication."""
    return """import { Context, Next } from 'hono'
import { sign, verify } from 'hono/jwt'

export interface AuthPayload {
  id: string
  email: string
  name: string
  avatar_url?: string
  provider: 'local' | 'google'
}

export interface User extends AuthPayload {
  created_at: Date
  updated_at: Date
}

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID || ''

export async function generateToken(payload: AuthPayload): Promise<string> {
  return sign(payload, JWT_SECRET)
}

export async function verifyToken(token: string): Promise<AuthPayload | null> {
  try {
    const payload = await verify(token, JWT_SECRET)
    return payload as AuthPayload
  } catch (error) {
    return null
  }
}

export async function verifyGoogleToken(token: string): Promise<AuthPayload | null> {
  try {
    const response = await fetch('https://www.googleapis.com/oauth2/v3/tokeninfo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `id_token=\${token}`
    })

    if (!response.ok) return null

    const data = await response.json()
    
    return {
      id: data.sub,
      email: data.email,
      name: data.name,
      avatar_url: data.picture,
      provider: 'google'
    }
  } catch (error) {
    return null
  }
}

export async function authMiddleware(c: Context, next: Next) {
  const authHeader = c.req.header('Authorization')
  
  if (!authHeader) {
    return c.json({ error: 'Missing authorization header' }, 401)
  }

  const token = authHeader.replace('Bearer ', '')
  const payload = await verifyToken(token)

  if (!payload) {
    return c.json({ error: 'Invalid token' }, 401)
  }

  c.set('user', payload)
  await next()
}

export function getUser(c: Context): AuthPayload {
  return c.get('user')
}

export async function loginLocal(email: string, password: string): Promise<AuthPayload | null> {
  // Implement local login logic
  // Hash password and verify against database
  return null
}

export async function loginGoogle(googleToken: string): Promise<AuthPayload | null> {
  return verifyGoogleToken(googleToken)
}

export async function registerLocal(
  email: string,
  password: string,
  name: string
): Promise<AuthPayload | null> {
  // Implement local registration logic
  // Hash password and save to database
  return null
}
"""


def generate_auth_routes(auth_type: str) -> str:
    """Generate authentication routes."""
    return f"""import {{ Hono }} from 'hono'
import {{
  generateToken,
  verifyGoogleToken,
  authMiddleware,
  getUser,
  loginLocal,
  loginGoogle,
  registerLocal
}} from '../middleware/auth'

const router = new Hono()

// Health check
router.get('/health', (c) => {{
  return c.json({{ status: 'ok' }})
}})

// Get current user
router.get('/me', authMiddleware, (c) => {{
  const user = getUser(c)
  return c.json(user)
}})

{f'''
// Local authentication
router.post('/register', async (c) => {{
  const {{ email, password, name }} = await c.req.json()
  
  if (!email || !password || !name) {{
    return c.json({{ error: 'Missing required fields' }}, 400)
  }}

  const user = await registerLocal(email, password, name)
  if (!user) {{
    return c.json({{ error: 'Registration failed' }}, 400)
  }}

  const token = await generateToken(user)
  return c.json({{ user, token }}, 201)
}})

router.post('/login', async (c) => {{
  const {{ email, password }} = await c.req.json()
  
  if (!email || !password) {{
    return c.json({{ error: 'Missing email or password' }}, 400)
  }}

  const user = await loginLocal(email, password)
  if (!user) {{
    return c.json({{ error: 'Invalid credentials' }}, 401)
  }}

  const token = await generateToken(user)
  return c.json({{ user, token }})
}})
''' if auth_type in ['local', 'both'] else ''}

{f'''
// Google authentication
router.post('/google', async (c) => {{
  const {{ token }} = await c.req.json()
  
  if (!token) {{
    return c.json({{ error: 'Missing token' }}, 400)
  }}

  const user = await loginGoogle(token)
  if (!user) {{
    return c.json({{ error: 'Invalid Google token' }}, 401)
  }}

  const jwtToken = await generateToken(user)
  return c.json({{ user, token: jwtToken }})
}})
''' if auth_type in ['google', 'both'] else ''}

// Logout
router.post('/logout', authMiddleware, (c) => {{
  // Implement logout logic (e.g., blacklist token)
  return c.json({{ message: 'Logged out successfully' }})
}})

export default router
"""


def create_auth(project_path: Path, auth_type: str = "local"):
    """Create authentication files."""
    print(f"\n🔐 Adding {auth_type} authentication\n")
    
    if auth_type not in ["local", "google", "both"]:
        print(f"✗ Unknown auth type: {auth_type}")
        print("Available types: local, google, both")
        return False
    
    # Create auth middleware
    auth_dir = project_path / "src" / "middleware"
    auth_dir.mkdir(parents=True, exist_ok=True)
    
    auth_file = auth_dir / "auth.ts"
    
    if auth_type == "local":
        content = generate_local_auth()
    elif auth_type == "google":
        content = generate_google_auth()
    else:  # both
        content = generate_combined_auth()
    
    auth_file.write_text(content)
    print(f"✓ Created {auth_file.relative_to(project_path)}")
    
    # Create auth routes
    routes_dir = project_path / "src" / "routes"
    routes_dir.mkdir(parents=True, exist_ok=True)
    
    routes_file = routes_dir / "auth.ts"
    routes_content = generate_auth_routes(auth_type)
    routes_file.write_text(routes_content)
    print(f"✓ Created {routes_file.relative_to(project_path)}")
    
    # Create .env.example
    env_file = project_path.parent.parent / ".env.example"
    env_content = generate_env_example(auth_type)
    
    if env_file.exists():
        with open(env_file, 'a') as f:
            f.write(f"\n# Authentication ({auth_type})\n")
            f.write(env_content)
        print(f"✓ Updated {env_file.relative_to(project_path.parent.parent)}")
    else:
        env_file.write_text(f"# Authentication ({auth_type})\n{env_content}")
        print(f"✓ Created {env_file.relative_to(project_path.parent.parent)}")
    
    return True


def generate_env_example(auth_type: str) -> str:
    """Generate environment variables example."""
    env = "JWT_SECRET=your-secret-key\n"
    
    if auth_type in ["google", "both"]:
        env += "GOOGLE_CLIENT_ID=your-google-client-id\n"
        env += "GOOGLE_CLIENT_SECRET=your-google-client-secret\n"
    
    return env


def find_backend_package(project_path: Path, package_name: str = None):
    """Find a backend package in the monorepo."""
    packages_dir = project_path / "packages"
    
    if not packages_dir.exists():
        print("✗ Not a valid monorepo project (packages directory not found)")
        return None
    
    if package_name:
        package_path = packages_dir / package_name
        if package_path.exists() and (package_path / "src").exists():
            return package_path
        else:
            print(f"✗ Backend package '{package_name}' not found or not configured")
            return None
    
    # Find first backend package with src directory
    for package_dir in packages_dir.iterdir():
        if package_dir.is_dir() and (package_dir / "src").exists():
            return package_dir
    
    print("✗ No backend package found in monorepo")
    return None


def main():
    parser = argparse.ArgumentParser(description="Add authentication to backend")
    parser.add_argument("--type", choices=["local", "google", "both"],
                        default="local", help="Authentication type")
    parser.add_argument("--package", help="Target package name")
    parser.add_argument("--project-path", default=".", help="Path to the monorepo project")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    
    # Find package
    package_path = find_backend_package(project_path, args.package)
    if not package_path:
        sys.exit(1)
    
    print(f"\n📦 Target package: {package_path.name}\n")
    
    # Create authentication
    if not create_auth(package_path, args.type):
        sys.exit(1)
    
    print(f"\n✅ Authentication ({args.type}) added successfully!\n")
    print("Next steps:")
    print("  1. Update .env with your credentials")
    print("  2. Import auth routes in your main app")
    print("  3. Use authMiddleware to protect routes")


if __name__ == "__main__":
    main()

