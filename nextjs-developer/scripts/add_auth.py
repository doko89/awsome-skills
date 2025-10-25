#!/usr/bin/env python3
"""
Add NextAuth.js authentication to your Next.js project.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(command: str, cwd: Path = None, shell: bool = True) -> bool:
    """Run a shell command."""
    print(f"Running: {command}")
    result = subprocess.run(
        command,
        shell=shell,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    if result.stdout:
        print(result.stdout)
    
    return True


def install_dependencies(project_path: Path, provider: str):
    """Install NextAuth and dependencies."""
    print("\n📦 Installing NextAuth.js dependencies...\n")

    packages = ["next-auth@beta"]

    if provider in ["local", "both"]:
        packages.extend([
            "drizzle-orm",
            "drizzle-kit",
            "@auth/drizzle-adapter",
            "postgres",
            "bcryptjs",
            "@types/bcryptjs"
        ])

    if not run_command(f"npm install {' '.join(packages)}", cwd=project_path):
        return False

    return True


def init_drizzle(project_path: Path):
    """Initialize Drizzle."""
    print("\n🗄️ Initializing Drizzle...\n")

    # Create drizzle directory
    drizzle_dir = project_path / "src" / "db"
    drizzle_dir.mkdir(parents=True, exist_ok=True)

    return True


def create_drizzle_schema(project_path: Path):
    """Create Drizzle schema with User and Account models."""
    schema = """import { pgTable, text, timestamp, integer, primaryKey } from "drizzle-orm/pg-core"
import { createId } from "@paralleldrive/cuid2"

export const users = pgTable("user", {
  id: text("id")
    .primaryKey()
    .$defaultFn(() => createId()),
  name: text("name"),
  email: text("email").notNull().unique(),
  emailVerified: timestamp("emailVerified", { mode: "date" }),
  image: text("image"),
  avatarUrl: text("avatarUrl"),
  password: text("password"),
  createdAt: timestamp("createdAt", { mode: "date" }).defaultNow().notNull(),
  updatedAt: timestamp("updatedAt", { mode: "date" }).defaultNow().notNull(),
})

export const accounts = pgTable(
  "account",
  {
    userId: text("userId")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    type: text("type").notNull(),
    provider: text("provider").notNull(),
    providerAccountId: text("providerAccountId").notNull(),
    refresh_token: text("refresh_token"),
    access_token: text("access_token"),
    expires_at: integer("expires_at"),
    token_type: text("token_type"),
    scope: text("scope"),
    id_token: text("id_token"),
    session_state: text("session_state"),
    createdAt: timestamp("createdAt", { mode: "date" }).defaultNow().notNull(),
    updatedAt: timestamp("updatedAt", { mode: "date" }).defaultNow().notNull(),
  },
  (account) => ({
    compoundKey: primaryKey({
      columns: [account.provider, account.providerAccountId],
    }),
  })
)

export const sessions = pgTable("session", {
  sessionToken: text("sessionToken").primaryKey(),
  userId: text("userId")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  expires: timestamp("expires", { mode: "date" }).notNull(),
  createdAt: timestamp("createdAt", { mode: "date" }).defaultNow().notNull(),
  updatedAt: timestamp("updatedAt", { mode: "date" }).defaultNow().notNull(),
})

export const verificationTokens = pgTable(
  "verificationToken",
  {
    identifier: text("identifier").notNull(),
    token: text("token").notNull(),
    expires: timestamp("expires", { mode: "date" }).notNull(),
  },
  (vt) => ({
    compoundKey: primaryKey({ columns: [vt.identifier, vt.token] }),
  })
)
"""

    schema_file = project_path / "src" / "db" / "schema.ts"
    schema_file.write_text(schema)
    print("✓ Created src/db/schema.ts")

    # Create db client
    db_client = """import { drizzle } from "drizzle-orm/postgres-js"
import postgres from "postgres"
import * as schema from "./schema"

const connectionString = process.env.DATABASE_URL!

const client = postgres(connectionString)
export const db = drizzle(client, { schema })
"""

    db_file = project_path / "src" / "db" / "index.ts"
    db_file.write_text(db_client)
    print("✓ Created src/db/index.ts")

    # Create drizzle config
    drizzle_config = """import { defineConfig } from "drizzle-kit"

export default defineConfig({
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
})
"""

    config_file = project_path / "drizzle.config.ts"
    config_file.write_text(drizzle_config)
    print("✓ Created drizzle.config.ts")

    # Install cuid2 for ID generation
    run_command("npm install @paralleldrive/cuid2", cwd=project_path)

    return True


def create_auth_config(project_path: Path, provider: str):
    """Create NextAuth configuration."""
    
    if provider == "local":
        config = get_local_auth_config()
    elif provider == "google":
        config = get_google_auth_config()
    else:  # both
        config = get_both_auth_config()
    
    # Create auth.ts
    auth_file = project_path / "src" / "lib" / "auth.ts"
    auth_file.parent.mkdir(parents=True, exist_ok=True)
    auth_file.write_text(config)
    print("✓ Created src/lib/auth.ts")
    
    return True


def get_local_auth_config() -> str:
    """Get local authentication config."""
    return """import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import { DrizzleAdapter } from "@auth/drizzle-adapter"
import { db } from "@/db"
import { users } from "@/db/schema"
import { eq } from "drizzle-orm"
import bcrypt from "bcryptjs"

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: DrizzleAdapter(db),
  session: {
    strategy: "jwt",
  },
  pages: {
    signIn: "/auth/signin",
  },
  providers: [
    Credentials({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          throw new Error("Invalid credentials")
        }

        const user = await db.query.users.findFirst({
          where: eq(users.email, credentials.email as string),
        })

        if (!user || !user.password) {
          throw new Error("Invalid credentials")
        }

        const isPasswordValid = await bcrypt.compare(
          credentials.password as string,
          user.password
        )

        if (!isPasswordValid) {
          throw new Error("Invalid credentials")
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
          image: user.avatarUrl || user.image,
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
      }
      return session
    },
  },
})
"""


def get_google_auth_config() -> str:
    """Get Google OAuth config."""
    return """import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import { DrizzleAdapter } from "@auth/drizzle-adapter"
import { db } from "@/db"

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: DrizzleAdapter(db),
  session: {
    strategy: "jwt",
  },
  pages: {
    signIn: "/auth/signin",
  },
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (user) {
        token.id = user.id
      }
      // Save Google avatar on first sign in
      if (account?.provider === "google" && profile?.picture) {
        await db.update(users)
          .set({ avatarUrl: profile.picture })
          .where(eq(users.id, user.id))
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
      }
      return session
    },
  },
})
"""


def get_both_auth_config() -> str:
    """Get both local and Google OAuth config."""
    return """import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import Google from "next-auth/providers/google"
import { DrizzleAdapter } from "@auth/drizzle-adapter"
import { db } from "@/db"
import { users } from "@/db/schema"
import { eq } from "drizzle-orm"
import bcrypt from "bcryptjs"

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: DrizzleAdapter(db),
  session: {
    strategy: "jwt",
  },
  pages: {
    signIn: "/auth/signin",
  },
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    Credentials({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          throw new Error("Invalid credentials")
        }

        const user = await db.query.users.findFirst({
          where: eq(users.email, credentials.email as string),
        })

        if (!user || !user.password) {
          throw new Error("Invalid credentials")
        }

        const isPasswordValid = await bcrypt.compare(
          credentials.password as string,
          user.password
        )

        if (!isPasswordValid) {
          throw new Error("Invalid credentials")
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
          image: user.avatarUrl || user.image,
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (user) {
        token.id = user.id
      }
      // Save Google avatar on first sign in
      if (account?.provider === "google" && profile?.picture) {
        await db.update(users)
          .set({ avatarUrl: profile.picture })
          .where(eq(users.id, user.id))
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
      }
      return session
    },
  },
})
"""


def create_api_route(project_path: Path):
    """Create NextAuth API route."""
    route_content = """import { handlers } from "@/lib/auth"

export const { GET, POST } = handlers
"""

    route_dir = project_path / "src" / "app" / "api" / "auth" / "[...nextauth]"
    route_dir.mkdir(parents=True, exist_ok=True)

    route_file = route_dir / "route.ts"
    route_file.write_text(route_content)
    print("✓ Created src/app/api/auth/[...nextauth]/route.ts")

    # Create avatar upload API route
    avatar_route = """import { auth } from "@/lib/auth"
import { db } from "@/db"
import { users } from "@/db/schema"
import { eq } from "drizzle-orm"
import { NextRequest, NextResponse } from "next/server"
import { writeFile } from "fs/promises"
import { join } from "path"

export async function POST(req: NextRequest) {
  try {
    const session = await auth()

    if (!session?.user?.id) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      )
    }

    const formData = await req.formData()
    const file = formData.get("avatar") as File

    if (!file) {
      return NextResponse.json(
        { error: "No file uploaded" },
        { status: 400 }
      )
    }

    // Validate file type
    const validTypes = ["image/jpeg", "image/jpg", "image/png", "image/gif"]
    if (!validTypes.includes(file.type)) {
      return NextResponse.json(
        { error: "Invalid file type. Only jpg, jpeg, png, gif are allowed" },
        { status: 400 }
      )
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      return NextResponse.json(
        { error: "File too large. Maximum size is 5MB" },
        { status: 400 }
      )
    }

    // Generate unique filename
    const bytes = await file.arrayBuffer()
    const buffer = Buffer.from(bytes)

    const ext = file.name.split(".").pop()
    const filename = `${session.user.id}_${Date.now()}.${ext}`
    const uploadDir = join(process.cwd(), "public", "uploads", "avatars")
    const filepath = join(uploadDir, filename)

    // Ensure upload directory exists
    const fs = require("fs")
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true })
    }

    // Save file
    await writeFile(filepath, buffer)

    // Update user avatar URL
    const avatarUrl = `/uploads/avatars/${filename}`
    await db.update(users)
      .set({ avatarUrl })
      .where(eq(users.id, session.user.id))

    return NextResponse.json({
      success: true,
      avatarUrl,
    })
  } catch (error) {
    console.error("Avatar upload error:", error)
    return NextResponse.json(
      { error: "Failed to upload avatar" },
      { status: 500 }
    )
  }
}
"""

    avatar_dir = project_path / "src" / "app" / "api" / "avatar"
    avatar_dir.mkdir(parents=True, exist_ok=True)

    avatar_file = avatar_dir / "route.ts"
    avatar_file.write_text(avatar_route)
    print("✓ Created src/app/api/avatar/route.ts")

    return True


def create_middleware(project_path: Path):
    """Create middleware for protected routes."""
    middleware = """import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isAuthPage = req.nextUrl.pathname.startsWith("/auth")
  const isProtectedPage = req.nextUrl.pathname.startsWith("/dashboard")

  if (isProtectedPage && !isLoggedIn) {
    return NextResponse.redirect(new URL("/auth/signin", req.url))
  }

  if (isAuthPage && isLoggedIn) {
    return NextResponse.redirect(new URL("/dashboard", req.url))
  }

  return NextResponse.next()
})

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
"""
    
    middleware_file = project_path / "src" / "middleware.ts"
    middleware_file.write_text(middleware)
    print("✓ Created src/middleware.ts")
    
    return True


def create_signin_page(project_path: Path, provider: str):
    """Create sign-in page."""
    if provider == "local":
        page = get_local_signin_page()
    elif provider == "google":
        page = get_google_signin_page()
    else:
        page = get_both_signin_page()
    
    page_dir = project_path / "src" / "app" / "auth" / "signin"
    page_dir.mkdir(parents=True, exist_ok=True)
    
    page_file = page_dir / "page.tsx"
    page_file.write_text(page)
    print("✓ Created src/app/auth/signin/page.tsx")
    
    return True


def get_local_signin_page() -> str:
    """Get local sign-in page."""
    return """import { SignInForm } from "@/components/auth/signin-form"

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 px-4">
        <div className="text-center">
          <h2 className="text-3xl font-bold">Sign in to your account</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            Enter your credentials to continue
          </p>
        </div>
        <SignInForm />
      </div>
    </div>
  )
}
"""


def get_google_signin_page() -> str:
    """Get Google sign-in page."""
    return """import { GoogleSignInButton } from "@/components/auth/google-signin-button"

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 px-4">
        <div className="text-center">
          <h2 className="text-3xl font-bold">Sign in to your account</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            Sign in with your Google account
          </p>
        </div>
        <GoogleSignInButton />
      </div>
    </div>
  )
}
"""


def get_both_signin_page() -> str:
    """Get both sign-in page."""
    return """import { SignInForm } from "@/components/auth/signin-form"
import { GoogleSignInButton } from "@/components/auth/google-signin-button"
import { Separator } from "@/components/ui/separator"

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 px-4">
        <div className="text-center">
          <h2 className="text-3xl font-bold">Sign in to your account</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            Choose your preferred sign-in method
          </p>
        </div>
        
        <GoogleSignInButton />
        
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <Separator />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-background px-2 text-muted-foreground">
              Or continue with
            </span>
          </div>
        </div>
        
        <SignInForm />
      </div>
    </div>
  )
}
"""


def main():
    parser = argparse.ArgumentParser(description="Add NextAuth.js authentication")
    parser.add_argument("--provider", choices=["local", "google", "both"], required=True,
                       help="Authentication provider")
    parser.add_argument("--project-path", default=".", help="Path to project root")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)
    
    if not (project_path / "package.json").exists():
        print(f"✗ Error: Not a valid Node.js project (package.json not found)")
        sys.exit(1)
    
    print(f"\n🔐 Adding NextAuth.js with {args.provider} authentication\n")
    
    # Install dependencies
    if not install_dependencies(project_path, args.provider):
        print("✗ Failed to install dependencies")
        sys.exit(1)
    
    # Initialize Drizzle if using local or both
    if args.provider in ["local", "both"]:
        if not init_drizzle(project_path):
            print("✗ Failed to initialize Drizzle")
            sys.exit(1)

        if not create_drizzle_schema(project_path):
            print("✗ Failed to create Drizzle schema")
            sys.exit(1)
    
    # Create auth config
    if not create_auth_config(project_path, args.provider):
        print("✗ Failed to create auth config")
        sys.exit(1)
    
    # Create API route
    if not create_api_route(project_path):
        print("✗ Failed to create API route")
        sys.exit(1)
    
    # Create middleware
    if not create_middleware(project_path):
        print("✗ Failed to create middleware")
        sys.exit(1)
    
    # Create sign-in page
    if not create_signin_page(project_path, args.provider):
        print("✗ Failed to create sign-in page")
        sys.exit(1)

    # Create uploads directory
    uploads_dir = project_path / "public" / "uploads" / "avatars"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    print("✓ Created public/uploads/avatars directory")

    print("\n✅ NextAuth.js added successfully!\n")
    print("Next steps:")

    if args.provider in ["local", "both"]:
        print("  1. Update DATABASE_URL in .env.local")
        print("  2. Run: npx drizzle-kit generate")
        print("  3. Run: npx drizzle-kit migrate")

    if args.provider in ["google", "both"]:
        print("  4. Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env.local")

    print("  5. Generate NEXTAUTH_SECRET: openssl rand -base64 32")
    print("  6. Add auth components:")
    print("     python ~/.claude/skills/nextjs-developer/scripts/generate_auth_components.py")
    print("  7. Avatar upload endpoint available at: /api/avatar")


if __name__ == "__main__":
    main()

