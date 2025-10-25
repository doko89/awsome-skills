#!/usr/bin/env python3
"""
Generate a new React component.
"""

import argparse
import sys
from pathlib import Path


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase."""
    return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())


def generate_basic_component(name: str) -> str:
    """Generate basic component."""
    pascal_name = to_pascal_case(name)
    
    return f"""interface {pascal_name}Props {{
  // Add your props here
}}

export function {pascal_name}({{  }}: {pascal_name}Props) {{
  return (
    <div>
      <h2>{pascal_name}</h2>
    </div>
  )
}}
"""


def generate_component_with_children(name: str) -> str:
    """Generate component with children prop."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ ReactNode }} from "react"

interface {pascal_name}Props {{
  children: ReactNode
  className?: string
}}

export function {pascal_name}({{ children, className }}: {pascal_name}Props) {{
  return (
    <div className={{className}}>
      {{children}}
    </div>
  )
}}
"""


def generate_component_with_state(name: str) -> str:
    """Generate component with state."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useState }} from "react"

interface {pascal_name}Props {{
  initialValue?: number
}}

export function {pascal_name}({{ initialValue = 0 }}: {pascal_name}Props) {{
  const [count, setCount] = useState(initialValue)

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">{pascal_name}</h2>
      <p>Count: {{count}}</p>
      <div className="space-x-2">
        <button
          onClick={{() => setCount(count + 1)}}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Increment
        </button>
        <button
          onClick={{() => setCount(count - 1)}}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Decrement
        </button>
      </div>
    </div>
  )
}}
"""


def generate_form_component(name: str) -> str:
    """Generate form component."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useState }} from "react"
import {{ Button }} from "@/components/ui/button"
import {{ Input }} from "@/components/ui/input"
import {{ Label }} from "@/components/ui/label"

interface {pascal_name}Props {{
  onSubmit: (data: FormData) => void | Promise<void>
}}

interface FormData {{
  // Define your form fields here
  name: string
  email: string
}}

export function {pascal_name}({{ onSubmit }}: {pascal_name}Props) {{
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState<FormData>({{
    name: "",
    email: "",
  }})

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault()
    setIsLoading(true)
    
    try {{
      await onSubmit(formData)
    }} finally {{
      setIsLoading(false)
    }}
  }}

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {{
    setFormData(prev => ({{
      ...prev,
      [e.target.name]: e.target.value
    }}))
  }}

  return (
    <form onSubmit={{handleSubmit}} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name</Label>
        <Input
          id="name"
          name="name"
          value={{formData.name}}
          onChange={{handleChange}}
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          value={{formData.email}}
          onChange={{handleChange}}
          required
        />
      </div>

      <Button type="submit" disabled={{isLoading}}>
        {{isLoading ? "Submitting..." : "Submit"}}
      </Button>
    </form>
  )
}}
"""


def generate_card_component(name: str) -> str:
    """Generate card component."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from "@/components/ui/card"

interface {pascal_name}Props {{
  title: string
  description?: string
  children?: React.ReactNode
}}

export function {pascal_name}({{ title, description, children }}: {pascal_name}Props) {{
  return (
    <Card>
      <CardHeader>
        <CardTitle>{{title}}</CardTitle>
        {{description && <CardDescription>{{description}}</CardDescription>}}
      </CardHeader>
      <CardContent>
        {{children}}
      </CardContent>
    </Card>
  )
}}
"""


def generate_list_component(name: str) -> str:
    """Generate list component."""
    pascal_name = to_pascal_case(name)
    
    return f"""interface {pascal_name}Item {{
  id: string | number
  // Add more fields as needed
}}

interface {pascal_name}Props {{
  items: {pascal_name}Item[]
  renderItem: (item: {pascal_name}Item) => React.ReactNode
  emptyMessage?: string
}}

export function {pascal_name}({{ items, renderItem, emptyMessage = "No items found" }}: {pascal_name}Props) {{
  if (items.length === 0) {{
    return (
      <div className="text-center py-8 text-muted-foreground">
        {{emptyMessage}}
      </div>
    )
  }}

  return (
    <div className="space-y-4">
      {{items.map(item => (
        <div key={{item.id}}>
          {{renderItem(item)}}
        </div>
      ))}}
    </div>
  )
}}
"""


def create_component(
    project_path: Path,
    name: str,
    component_type: str = "basic",
    directory: str = "components"
):
    """Create a new component."""
    print(f"\n🚀 Generating {name} component\n")
    
    # Generate component content based on type
    generators = {
        "basic": generate_basic_component,
        "children": generate_component_with_children,
        "state": generate_component_with_state,
        "form": generate_form_component,
        "card": generate_card_component,
        "list": generate_list_component,
    }
    
    generator = generators.get(component_type, generate_basic_component)
    content = generator(name)
    
    # Create component file
    components_dir = project_path / "src" / directory
    components_dir.mkdir(parents=True, exist_ok=True)
    
    pascal_name = to_pascal_case(name)
    component_file = components_dir / f"{pascal_name}.tsx"
    
    if component_file.exists():
        print(f"⚠ Warning: {component_file} already exists")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled")
            return False
    
    component_file.write_text(content)
    print(f"✓ Created {component_file.relative_to(project_path)}")
    
    # Create index file for easier imports
    index_file = components_dir / "index.ts"
    export_line = f"export * from './{pascal_name}'\n"
    
    if index_file.exists():
        content = index_file.read_text()
        if export_line not in content:
            index_file.write_text(content + export_line)
            print(f"✓ Updated {index_file.relative_to(project_path)}")
    else:
        index_file.write_text(export_line)
        print(f"✓ Created {index_file.relative_to(project_path)}")
    
    # Print usage instructions
    print("\n📝 Usage:")
    print(f"  import {{ {pascal_name} }} from '@/{directory}'")
    print(f"  // or")
    print(f"  import {{ {pascal_name} }} from '@/{directory}/{pascal_name}'")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate a new React component")
    parser.add_argument("name", help="Name of the component (e.g., 'UserCard', 'product-list')")
    parser.add_argument("--project-path", default=".", help="Path to project root")
    parser.add_argument("--type", choices=["basic", "children", "state", "form", "card", "list"],
                       default="basic", help="Type of component to generate")
    parser.add_argument("--dir", default="components", help="Directory to create component in (relative to src/)")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)
    
    if not (project_path / "package.json").exists():
        print(f"✗ Error: Not a valid Node.js project (package.json not found)")
        sys.exit(1)
    
    if create_component(project_path, args.name, args.type, args.dir):
        print("\n✅ Component generated successfully!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

