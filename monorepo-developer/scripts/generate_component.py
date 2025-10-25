#!/usr/bin/env python3
"""
Generate a new React component in a monorepo frontend package.
"""

import argparse
import sys
from pathlib import Path


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase."""
    return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())


def to_kebab_case(name: str) -> str:
    """Convert string to kebab-case."""
    return name.replace('_', '-').lower()


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
    
    return f"""import {{ ReactNode }} from 'react'
import {{ cn }} from '@/lib/utils'

interface {pascal_name}Props {{
  children: ReactNode
  className?: string
}}

export function {pascal_name}({{ children, className }}: {pascal_name}Props) {{
  return (
    <div className={{cn(className)}}>
      {{children}}
    </div>
  )
}}
"""


def generate_component_with_state(name: str) -> str:
    """Generate component with state."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useState }} from 'react'
import {{ Button }} from '@/components/ui/button'

interface {pascal_name}Props {{
  initialValue?: number
}}

export function {pascal_name}({{ initialValue = 0 }}: {pascal_name}Props) {{
  const [count, setCount] = useState(initialValue)

  return (
    <div className='space-y-4'>
      <h2 className='text-2xl font-bold'>{pascal_name}</h2>
      <p className='text-lg'>Count: {{count}}</p>
      <div className='space-x-2'>
        <Button onClick={{() => setCount(count + 1)}}>
          Increment
        </Button>
        <Button variant='outline' onClick={{() => setCount(count - 1)}}>
          Decrement
        </Button>
      </div>
    </div>
  )
}}
"""


def generate_form_component(name: str) -> str:
    """Generate form component."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useState }} from 'react'
import {{ Button }} from '@/components/ui/button'
import {{ Input }} from '@/components/ui/input'
import {{ Label }} from '@/components/ui/label'

interface {pascal_name}Props {{
  onSubmit: (data: FormData) => void | Promise<void>
}}

interface FormData {{
  name: string
  email: string
}}

export function {pascal_name}({{ onSubmit }}: {pascal_name}Props) {{
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState<FormData>({{
    name: '',
    email: '',
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
    <form onSubmit={{handleSubmit}} className='space-y-4'>
      <div className='space-y-2'>
        <Label htmlFor='name'>Name</Label>
        <Input
          id='name'
          name='name'
          value={{formData.name}}
          onChange={{handleChange}}
          required
        />
      </div>

      <div className='space-y-2'>
        <Label htmlFor='email'>Email</Label>
        <Input
          id='email'
          name='email'
          type='email'
          value={{formData.email}}
          onChange={{handleChange}}
          required
        />
      </div>

      <Button type='submit' disabled={{isLoading}}>
        {{isLoading ? 'Submitting...' : 'Submit'}}
      </Button>
    </form>
  )
}}
"""


def generate_card_component(name: str) -> str:
    """Generate card component."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from '@/components/ui/card'

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

export function {pascal_name}({{ items, renderItem, emptyMessage = 'No items found' }}: {pascal_name}Props) {{
  if (items.length === 0) {{
    return (
      <div className='text-center py-8 text-muted-foreground'>
        {{emptyMessage}}
      </div>
    )
  }}

  return (
    <div className='space-y-4'>
      {{items.map(item => (
        <div key={{item.id}}>
          {{renderItem(item)}}
        </div>
      ))}}
    </div>
  )
}}
"""


def generate_modal_component(name: str) -> str:
    """Generate modal component."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle }} from '@/components/ui/dialog'
import {{ Button }} from '@/components/ui/button'

interface {pascal_name}Props {{
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description?: string
  children?: React.ReactNode
  onConfirm?: () => void
}}

export function {pascal_name}({{
  open,
  onOpenChange,
  title,
  description,
  children,
  onConfirm
}}: {pascal_name}Props) {{
  return (
    <Dialog open={{open}} onOpenChange={{onOpenChange}}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{{title}}</DialogTitle>
          {{description && <DialogDescription>{{description}}</DialogDescription>}}
        </DialogHeader>
        <div className='py-4'>
          {{children}}
        </div>
        <div className='flex justify-end gap-2'>
          <Button variant='outline' onClick={{() => onOpenChange(false)}}>
            Cancel
          </Button>
          {{onConfirm && (
            <Button onClick={{onConfirm}}>
              Confirm
            </Button>
          )}}
        </div>
      </DialogContent>
    </Dialog>
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
    print(f"\n🚀 Generating {name} component ({component_type})\n")
    
    # Generate component content based on type
    generators = {
        "basic": generate_basic_component,
        "children": generate_component_with_children,
        "state": generate_component_with_state,
        "form": generate_form_component,
        "card": generate_card_component,
        "list": generate_list_component,
        "modal": generate_modal_component,
    }
    
    if component_type not in generators:
        print(f"✗ Unknown component type: {component_type}")
        print(f"Available types: {', '.join(generators.keys())}")
        return False
    
    generator = generators[component_type]
    content = generator(name)
    
    # Determine component path
    pascal_name = to_pascal_case(name)
    
    if directory == "ui":
        component_path = project_path / "src" / "components" / "ui" / f"{pascal_name}.tsx"
    else:
        component_path = project_path / "src" / "components" / directory / f"{pascal_name}.tsx"
    
    # Create directory if it doesn't exist
    component_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write component file
    component_path.write_text(content)
    print(f"✓ Created {component_path.relative_to(project_path)}")
    
    # Create index.ts if it doesn't exist
    index_path = component_path.parent / "index.ts"
    if not index_path.exists():
        index_path.write_text(f"export {{ {pascal_name} }} from './{pascal_name}'\n")
        print(f"✓ Created {index_path.relative_to(project_path)}")
    else:
        # Append to existing index.ts
        with open(index_path, 'a') as f:
            f.write(f"export {{ {pascal_name} }} from './{pascal_name}'\n")
        print(f"✓ Updated {index_path.relative_to(project_path)}")
    
    return True


def find_frontend_package(project_path: Path, package_name: str = None):
    """Find a frontend package in the monorepo."""
    packages_dir = project_path / "packages"
    
    if not packages_dir.exists():
        print("✗ Not a valid monorepo project (packages directory not found)")
        return None
    
    if package_name:
        package_path = packages_dir / package_name
        if package_path.exists() and (package_path / "src" / "components").exists():
            return package_path
        else:
            print(f"✗ Frontend package '{package_name}' not found or not configured")
            return None
    
    # Find first frontend package with components directory
    for package_dir in packages_dir.iterdir():
        if package_dir.is_dir() and (package_dir / "src" / "components").exists():
            return package_dir
    
    print("✗ No frontend package found in monorepo")
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate a new React component")
    parser.add_argument("name", help="Component name (e.g., UserCard, user-card)")
    parser.add_argument("--type", choices=["basic", "children", "state", "form", "card", "list", "modal"],
                        default="basic", help="Component type")
    parser.add_argument("--directory", default="components", help="Component directory (relative to src/components)")
    parser.add_argument("--package", help="Target package name")
    parser.add_argument("--project-path", default=".", help="Path to the monorepo project")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    
    # Find package
    package_path = find_frontend_package(project_path, args.package)
    if not package_path:
        sys.exit(1)
    
    print(f"\n📦 Target package: {package_path.name}\n")
    
    # Create component
    if not create_component(package_path, args.name, args.type, args.directory):
        sys.exit(1)
    
    print(f"\n✅ Component '{args.name}' generated successfully!\n")
    print("Usage:")
    print(f"  import {{ {to_pascal_case(args.name)} }} from '@/components/{args.directory}'")


if __name__ == "__main__":
    main()

