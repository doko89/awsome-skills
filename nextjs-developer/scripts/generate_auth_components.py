#!/usr/bin/env python3
"""
Generate authentication components for NextAuth.js.
"""

import argparse
import sys
from pathlib import Path


def create_signin_form(project_path: Path):
    """Create sign-in form component."""
    component = """"use client"

import { useState } from "react"
import { signIn } from "next-auth/react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function SignInForm() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError(null)

    const formData = new FormData(event.currentTarget)
    const email = formData.get("email") as string
    const password = formData.get("password") as string

    try {
      const result = await signIn("credentials", {
        email,
        password,
        redirect: false,
      })

      if (result?.error) {
        setError("Invalid email or password")
        return
      }

      router.push("/dashboard")
      router.refresh()
    } catch (error) {
      setError("An error occurred. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sign In</CardTitle>
        <CardDescription>Enter your credentials to continue</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-4">
          {error && (
            <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
              {error}
            </div>
          )}
          
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="you@example.com"
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              required
              disabled={isLoading}
            />
          </div>
          
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Signing in..." : "Sign In"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
"""
    
    component_dir = project_path / "src" / "components" / "auth"
    component_dir.mkdir(parents=True, exist_ok=True)
    
    component_file = component_dir / "signin-form.tsx"
    component_file.write_text(component)
    print(f"✓ Created {component_file.relative_to(project_path)}")


def create_signup_form(project_path: Path):
    """Create sign-up form component."""
    component = """"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import bcrypt from "bcryptjs"

export function SignUpForm() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsLoading(true)
    setError(null)

    const formData = new FormData(event.currentTarget)
    const name = formData.get("name") as string
    const email = formData.get("email") as string
    const password = formData.get("password") as string

    try {
      const response = await fetch("/api/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password }),
      })

      if (!response.ok) {
        const data = await response.json()
        setError(data.error || "Failed to create account")
        return
      }

      router.push("/auth/signin?registered=true")
    } catch (error) {
      setError("An error occurred. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Account</CardTitle>
        <CardDescription>Enter your information to get started</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-4">
          {error && (
            <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
              {error}
            </div>
          )}
          
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              name="name"
              type="text"
              placeholder="John Doe"
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="you@example.com"
              required
              disabled={isLoading}
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              required
              minLength={8}
              disabled={isLoading}
            />
          </div>
          
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Creating account..." : "Create Account"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
"""
    
    component_dir = project_path / "src" / "components" / "auth"
    component_dir.mkdir(parents=True, exist_ok=True)
    
    component_file = component_dir / "signup-form.tsx"
    component_file.write_text(component)
    print(f"✓ Created {component_file.relative_to(project_path)}")


def create_google_signin_button(project_path: Path):
    """Create Google sign-in button component."""
    component = """"use client"

import { signIn } from "next-auth/react"
import { Button } from "@/components/ui/button"

export function GoogleSignInButton() {
  return (
    <Button
      variant="outline"
      className="w-full"
      onClick={() => signIn("google", { callbackUrl: "/dashboard" })}
    >
      <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
        <path
          d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
          fill="#4285F4"
        />
        <path
          d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          fill="#34A853"
        />
        <path
          d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
          fill="#FBBC05"
        />
        <path
          d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
          fill="#EA4335"
        />
      </svg>
      Continue with Google
    </Button>
  )
}
"""
    
    component_dir = project_path / "src" / "components" / "auth"
    component_dir.mkdir(parents=True, exist_ok=True)
    
    component_file = component_dir / "google-signin-button.tsx"
    component_file.write_text(component)
    print(f"✓ Created {component_file.relative_to(project_path)}")


def create_user_button(project_path: Path):
    """Create user button component."""
    component = """"use client"

import { signOut, useSession } from "next-auth/react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export function UserButton() {
  const { data: session } = useSession()

  if (!session) {
    return null
  }

  const initials = session.user?.name
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase() || "U"

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-10 w-10 rounded-full">
          <Avatar>
            <AvatarImage src={session.user?.image || ""} alt={session.user?.name || ""} />
            <AvatarFallback>{initials}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium">{session.user?.name}</p>
            <p className="text-xs text-muted-foreground">{session.user?.email}</p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => signOut()}>
          Sign Out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
"""
    
    component_dir = project_path / "src" / "components" / "auth"
    component_dir.mkdir(parents=True, exist_ok=True)
    
    component_file = component_dir / "user-button.tsx"
    component_file.write_text(component)
    print(f"✓ Created {component_file.relative_to(project_path)}")


def main():
    parser = argparse.ArgumentParser(description="Generate authentication components")
    parser.add_argument("--project-path", default=".", help="Path to project root")
    parser.add_argument("--all", action="store_true", help="Generate all components")
    parser.add_argument("--signin", action="store_true", help="Generate sign-in form")
    parser.add_argument("--signup", action="store_true", help="Generate sign-up form")
    parser.add_argument("--google", action="store_true", help="Generate Google sign-in button")
    parser.add_argument("--user-button", action="store_true", help="Generate user button")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)
    
    if not (project_path / "package.json").exists():
        print(f"✗ Error: Not a valid Node.js project (package.json not found)")
        sys.exit(1)
    
    print("\n🎨 Generating authentication components\n")
    
    if args.all or args.signin:
        create_signin_form(project_path)
    
    if args.all or args.signup:
        create_signup_form(project_path)
    
    if args.all or args.google:
        create_google_signin_button(project_path)
    
    if args.all or args.user_button:
        create_user_button(project_path)
    
    if not any([args.all, args.signin, args.signup, args.google, args.user_button]):
        print("No components specified. Use --all or specify individual components.")
        print("Example: python generate_auth_components.py --all")
        sys.exit(1)
    
    print("\n✅ Authentication components generated successfully!\n")
    print("Required shadcn/ui components:")
    print("  npx shadcn@latest add button input label card dropdown-menu avatar")


if __name__ == "__main__":
    main()

