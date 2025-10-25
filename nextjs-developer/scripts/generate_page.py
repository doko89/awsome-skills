#!/usr/bin/env python3
"""
Generate Next.js pages with App Router.
"""

import argparse
import sys
from pathlib import Path


def create_basic_page(project_path: Path, page_name: str, route: str):
    """Create a basic Next.js page."""
    page_content = f"""export default function {page_name}Page() {{
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-4xl font-bold mb-6">{page_name}</h1>
      <p className="text-muted-foreground">
        This is the {page_name.lower()} page.
      </p>
    </div>
  )
}}
"""
    
    page_dir = project_path / "src" / "app" / route
    page_dir.mkdir(parents=True, exist_ok=True)
    
    page_file = page_dir / "page.tsx"
    page_file.write_text(page_content)
    print(f"✓ Created {page_file.relative_to(project_path)}")


def create_data_page(project_path: Path, page_name: str, route: str):
    """Create a page with data fetching."""
    page_content = f"""import {{ Suspense }} from "react"

interface Item {{
  id: number
  title: string
  description: string
}}

async function getData(): Promise<Item[]> {{
  // Replace with your API endpoint
  const res = await fetch("https://api.example.com/items", {{
    cache: "no-store", // or 'force-cache' for static
  }})
  
  if (!res.ok) {{
    throw new Error("Failed to fetch data")
  }}
  
  return res.json()
}}

function LoadingSkeleton() {{
  return (
    <div className="space-y-4">
      {{[...Array(3)].map((_, i) => (
        <div key={{i}} className="h-20 bg-muted animate-pulse rounded-lg" />
      ))}}
    </div>
  )
}}

async function {page_name}Content() {{
  const items = await getData()
  
  return (
    <div className="space-y-4">
      {{items.map((item) => (
        <div key={{item.id}} className="p-4 border rounded-lg">
          <h3 className="font-semibold">{{item.title}}</h3>
          <p className="text-sm text-muted-foreground">{{item.description}}</p>
        </div>
      ))}}
    </div>
  )
}}

export default function {page_name}Page() {{
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-4xl font-bold mb-6">{page_name}</h1>
      <Suspense fallback={{<LoadingSkeleton />}}>
        <{page_name}Content />
      </Suspense>
    </div>
  )
}}
"""
    
    page_dir = project_path / "src" / "app" / route
    page_dir.mkdir(parents=True, exist_ok=True)
    
    page_file = page_dir / "page.tsx"
    page_file.write_text(page_content)
    print(f"✓ Created {page_file.relative_to(project_path)}")


def create_form_page(project_path: Path, page_name: str, route: str):
    """Create a page with form."""
    page_content = f""""use client"

import {{ useState }} from "react"
import {{ Button }} from "@/components/ui/button"
import {{ Input }} from "@/components/ui/input"
import {{ Label }} from "@/components/ui/label"
import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from "@/components/ui/card"

export default function {page_name}Page() {{
  const [isLoading, setIsLoading] = useState(false)

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {{
    event.preventDefault()
    setIsLoading(true)

    const formData = new FormData(event.currentTarget)
    const data = Object.fromEntries(formData)

    try {{
      const response = await fetch("/api/{route}", {{
        method: "POST",
        headers: {{
          "Content-Type": "application/json",
        }},
        body: JSON.stringify(data),
      }})

      if (!response.ok) {{
        throw new Error("Failed to submit form")
      }}

      const result = await response.json()
      console.log("Success:", result)
      
      // Reset form or redirect
      event.currentTarget.reset()
    }} catch (error) {{
      console.error("Error:", error)
    }} finally {{
      setIsLoading(false)
    }}
  }}

  return (
    <div className="container mx-auto py-10">
      <Card className="max-w-md mx-auto">
        <CardHeader>
          <CardTitle>{page_name}</CardTitle>
          <CardDescription>Fill out the form below</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={{onSubmit}} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                name="name"
                placeholder="Enter your name"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="Enter your email"
                required
              />
            </div>
            
            <Button type="submit" className="w-full" disabled={{isLoading}}>
              {{isLoading ? "Submitting..." : "Submit"}}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}}
"""
    
    page_dir = project_path / "src" / "app" / route
    page_dir.mkdir(parents=True, exist_ok=True)
    
    page_file = page_dir / "page.tsx"
    page_file.write_text(page_content)
    print(f"✓ Created {page_file.relative_to(project_path)}")


def create_protected_page(project_path: Path, page_name: str, route: str):
    """Create a protected page with authentication."""
    page_content = f"""import {{ auth }} from "@/lib/auth"
import {{ redirect }} from "next/navigation"

export default async function {page_name}Page() {{
  const session = await auth()
  
  if (!session) {{
    redirect("/auth/signin")
  }}

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-4xl font-bold mb-6">{page_name}</h1>
      <p className="text-muted-foreground mb-4">
        Welcome, {{session.user?.name || session.user?.email}}!
      </p>
      <div className="p-4 border rounded-lg">
        <h2 className="font-semibold mb-2">User Information</h2>
        <pre className="text-sm">{{JSON.stringify(session.user, null, 2)}}</pre>
      </div>
    </div>
  )
}}
"""
    
    page_dir = project_path / "src" / "app" / route
    page_dir.mkdir(parents=True, exist_ok=True)
    
    page_file = page_dir / "page.tsx"
    page_file.write_text(page_content)
    print(f"✓ Created {page_file.relative_to(project_path)}")


def create_api_route(project_path: Path, route: str):
    """Create an API route."""
    api_content = """import { NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    // Your GET logic here
    const data = { message: "Success" }
    
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Your POST logic here
    console.log("Received:", body)
    
    return NextResponse.json({ success: true, data: body })
  } catch (error) {
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    )
  }
}
"""
    
    api_dir = project_path / "src" / "app" / "api" / route
    api_dir.mkdir(parents=True, exist_ok=True)
    
    api_file = api_dir / "route.ts"
    api_file.write_text(api_content)
    print(f"✓ Created {api_file.relative_to(project_path)}")


def main():
    parser = argparse.ArgumentParser(description="Generate Next.js pages")
    parser.add_argument("page_name", help="Name of the page (e.g., Dashboard, Profile)")
    parser.add_argument("--route", help="Route path (e.g., dashboard, profile/settings)")
    parser.add_argument("--type", choices=["basic", "data", "form", "protected", "api"],
                       default="basic", help="Type of page to generate")
    parser.add_argument("--project-path", default=".", help="Path to project root")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)
    
    if not (project_path / "package.json").exists():
        print(f"✗ Error: Not a valid Node.js project (package.json not found)")
        sys.exit(1)
    
    # Use page_name as route if not specified
    route = args.route or args.page_name.lower().replace(" ", "-")
    
    print(f"\n📄 Generating {args.type} page: {args.page_name}\n")
    
    if args.type == "basic":
        create_basic_page(project_path, args.page_name, route)
    elif args.type == "data":
        create_data_page(project_path, args.page_name, route)
    elif args.type == "form":
        create_form_page(project_path, args.page_name, route)
    elif args.type == "protected":
        create_protected_page(project_path, args.page_name, route)
    elif args.type == "api":
        create_api_route(project_path, route)
    
    print(f"\n✅ Page generated successfully!\n")
    print(f"Route: /{route}")
    
    if args.type == "form":
        print("\nNote: Make sure to install required components:")
        print("  npx shadcn@latest add button input label card")
    elif args.type == "protected":
        print("\nNote: Make sure NextAuth is configured:")
        print("  python ../scripts/add_auth.py --provider local")


if __name__ == "__main__":
    main()

