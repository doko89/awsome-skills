#!/usr/bin/env python3
"""
Generate a new page component for React project.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase."""
    return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())


def to_kebab_case(name: str) -> str:
    """Convert string to kebab-case."""
    return name.replace('_', '-').replace(' ', '-').lower()


def generate_page_component(name: str, with_layout: bool = False) -> str:
    """Generate page component code."""
    pascal_name = to_pascal_case(name)
    
    if with_layout:
        return f"""import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from "@/components/ui/card"

export default function {pascal_name}Page() {{
  return (
    <div className="container mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>{pascal_name}</CardTitle>
          <CardDescription>
            This is the {name} page
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p>Welcome to the {name} page!</p>
        </CardContent>
      </Card>
    </div>
  )
}}
"""
    else:
        return f"""export default function {pascal_name}Page() {{
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-4xl font-bold mb-4">{pascal_name}</h1>
      <p>Welcome to the {name} page!</p>
    </div>
  )
}}
"""


def generate_page_with_data_fetching(name: str) -> str:
    """Generate page with data fetching using TanStack Query."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useQuery }} from "@tanstack/react-query"
import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from "@/components/ui/card"
import {{ Skeleton }} from "@/components/ui/skeleton"

// TODO: Replace with your actual API endpoint
async function fetch{pascal_name}Data() {{
  const response = await fetch('/api/{to_kebab_case(name)}')
  if (!response.ok) {{
    throw new Error('Failed to fetch data')
  }}
  return response.json()
}}

export default function {pascal_name}Page() {{
  const {{ data, isLoading, error }} = useQuery({{
    queryKey: ['{to_kebab_case(name)}'],
    queryFn: fetch{pascal_name}Data,
  }})

  if (isLoading) {{
    return (
      <div className="container mx-auto py-8">
        <Card>
          <CardHeader>
            <Skeleton className="h-8 w-[200px]" />
            <Skeleton className="h-4 w-[300px]" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-4 w-full" />
          </CardContent>
        </Card>
      </div>
    )
  }}

  if (error) {{
    return (
      <div className="container mx-auto py-8">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
            <CardDescription>Failed to load data</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-red-500">{{error.message}}</p>
          </CardContent>
        </Card>
      </div>
    )
  }}

  return (
    <div className="container mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>{pascal_name}</CardTitle>
          <CardDescription>
            Data loaded successfully
          </CardDescription>
        </CardHeader>
        <CardContent>
          <pre className="bg-muted p-4 rounded-lg overflow-auto">
            {{JSON.stringify(data, null, 2)}}
          </pre>
        </CardContent>
      </Card>
    </div>
  )
}}
"""


def generate_page_with_form(name: str) -> str:
    """Generate page with form."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useState }} from "react"
import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from "@/components/ui/card"
import {{ Button }} from "@/components/ui/button"
import {{ Input }} from "@/components/ui/input"
import {{ Label }} from "@/components/ui/label"
import {{ useToast }} from "@/hooks/use-toast"

export default function {pascal_name}Page() {{
  const [isLoading, setIsLoading] = useState(false)
  const {{ toast }} = useToast()

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {{
    e.preventDefault()
    setIsLoading(true)

    try {{
      const formData = new FormData(e.currentTarget)
      const data = Object.fromEntries(formData)
      
      // TODO: Replace with your actual API call
      console.log('Form data:', data)
      
      toast({{
        title: "Success",
        description: "Form submitted successfully!",
      }})
    }} catch (error) {{
      toast({{
        title: "Error",
        description: "Failed to submit form",
        variant: "destructive",
      }})
    }} finally {{
      setIsLoading(false)
    }}
  }}

  return (
    <div className="container mx-auto py-8 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>{pascal_name}</CardTitle>
          <CardDescription>
            Fill out the form below
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={{handleSubmit}} className="space-y-4">
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
            
            <Button type="submit" disabled={{isLoading}}>
              {{isLoading ? "Submitting..." : "Submit"}}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}}
"""


def create_page(
    project_path: Path,
    name: str,
    page_type: str = "basic",
    with_layout: bool = False
):
    """Create a new page component."""
    print(f"\n🚀 Generating {name} page\n")
    
    # Generate page content based on type
    if page_type == "data":
        content = generate_page_with_data_fetching(name)
    elif page_type == "form":
        content = generate_page_with_form(name)
    else:
        content = generate_page_component(name, with_layout)
    
    # Create page file
    pages_dir = project_path / "src" / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    pascal_name = to_pascal_case(name)
    page_file = pages_dir / f"{pascal_name}Page.tsx"
    
    if page_file.exists():
        print(f"⚠ Warning: {page_file} already exists")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled")
            return False
    
    page_file.write_text(content)
    print(f"✓ Created {page_file.relative_to(project_path)}")
    
    # Print usage instructions
    print("\n📝 Usage:")
    print(f"  import {pascal_name}Page from '@/pages/{pascal_name}Page'")
    print("\n  // In your router:")
    print(f"  <Route path=\"/{to_kebab_case(name)}\" element={{<{pascal_name}Page />}} />")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate a new page component")
    parser.add_argument("name", help="Name of the page (e.g., 'about', 'contact', 'user-profile')")
    parser.add_argument("--project-path", default=".", help="Path to project root")
    parser.add_argument("--type", choices=["basic", "data", "form"], default="basic",
                       help="Type of page to generate")
    parser.add_argument("--with-layout", action="store_true", help="Include card layout")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)
    
    if not (project_path / "package.json").exists():
        print(f"✗ Error: Not a valid Node.js project (package.json not found)")
        sys.exit(1)
    
    if create_page(project_path, args.name, args.type, args.with_layout):
        print("\n✅ Page generated successfully!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

