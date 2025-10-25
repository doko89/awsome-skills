#!/usr/bin/env python3
"""
Generate a new React page in a monorepo frontend package.
"""

import argparse
import sys
from pathlib import Path


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase."""
    return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())


def generate_basic_page(name: str) -> str:
    """Generate basic page."""
    pascal_name = to_pascal_case(name)
    
    return f"""export function {pascal_name}() {{
  return (
    <div className='min-h-screen bg-white'>
      <div className='max-w-7xl mx-auto px-4 py-8'>
        <h1 className='text-4xl font-bold mb-4'>{pascal_name}</h1>
        <p className='text-gray-600'>Welcome to {pascal_name} page</p>
      </div>
    </div>
  )
}}

export default {pascal_name}
"""


def generate_list_page(name: str) -> str:
    """Generate list page."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useState }} from 'react'
import {{ Button }} from '@/components/ui/button'
import {{ Input }} from '@/components/ui/input'

interface Item {{
  id: number
  name: string
}}

export function {pascal_name}() {{
  const [items, setItems] = useState<Item[]>([])
  const [search, setSearch] = useState('')

  const filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className='min-h-screen bg-white'>
      <div className='max-w-7xl mx-auto px-4 py-8'>
        <div className='flex justify-between items-center mb-8'>
          <h1 className='text-4xl font-bold'>{pascal_name}</h1>
          <Button>Add New</Button>
        </div>

        <div className='mb-6'>
          <Input
            placeholder='Search...'
            value={{search}}
            onChange={{(e) => setSearch(e.target.value)}}
          />
        </div>

        <div className='space-y-4'>
          {{filteredItems.length === 0 ? (
            <p className='text-gray-500'>No items found</p>
          ) : (
            filteredItems.map(item => (
              <div key={{item.id}} className='p-4 border rounded-lg'>
                {{item.name}}
              </div>
            ))
          )}}
        </div>
      </div>
    </div>
  )
}}

export default {pascal_name}
"""


def generate_detail_page(name: str) -> str:
    """Generate detail page."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useParams }} from 'react-router-dom'
import {{ Button }} from '@/components/ui/button'

export function {pascal_name}() {{
  const {{ id }} = useParams()

  return (
    <div className='min-h-screen bg-white'>
      <div className='max-w-7xl mx-auto px-4 py-8'>
        <div className='flex items-center gap-4 mb-8'>
          <Button variant='outline'>← Back</Button>
          <h1 className='text-4xl font-bold'>{pascal_name} #{{id}}</h1>
        </div>

        <div className='grid grid-cols-1 md:grid-cols-3 gap-8'>
          <div className='md:col-span-2'>
            <div className='bg-gray-50 p-6 rounded-lg'>
              <h2 className='text-2xl font-bold mb-4'>Details</h2>
              <p className='text-gray-600'>Loading details...</p>
            </div>
          </div>

          <div>
            <div className='bg-gray-50 p-6 rounded-lg'>
              <h2 className='text-2xl font-bold mb-4'>Actions</h2>
              <div className='space-y-2'>
                <Button className='w-full'>Edit</Button>
                <Button variant='destructive' className='w-full'>Delete</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}}

export default {pascal_name}
"""


def generate_form_page(name: str) -> str:
    """Generate form page."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ useState }} from 'react'
import {{ Button }} from '@/components/ui/button'
import {{ Input }} from '@/components/ui/input'
import {{ Label }} from '@/components/ui/label'
import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from '@/components/ui/card'

export function {pascal_name}() {{
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({{
    name: '',
    email: '',
  }})

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault()
    setIsLoading(true)
    
    try {{
      // Submit form
      console.log('Submitting:', formData)
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
    <div className='min-h-screen bg-white'>
      <div className='max-w-2xl mx-auto px-4 py-8'>
        <Card>
          <CardHeader>
            <CardTitle>{pascal_name}</CardTitle>
            <CardDescription>Fill in the form below</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={{handleSubmit}} className='space-y-6'>
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

              <div className='flex gap-2'>
                <Button type='submit' disabled={{isLoading}}>
                  {{isLoading ? 'Submitting...' : 'Submit'}}
                </Button>
                <Button type='button' variant='outline'>
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}}

export default {pascal_name}
"""


def generate_dashboard_page(name: str) -> str:
    """Generate dashboard page."""
    pascal_name = to_pascal_case(name)
    
    return f"""import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from '@/components/ui/card'

export function {pascal_name}() {{
  return (
    <div className='min-h-screen bg-gray-50'>
      <div className='max-w-7xl mx-auto px-4 py-8'>
        <h1 className='text-4xl font-bold mb-8'>{pascal_name}</h1>

        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8'>
          <Card>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium'>Total Users</CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-2xl font-bold'>1,234</div>
              <p className='text-xs text-gray-500'>+12% from last month</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium'>Revenue</CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-2xl font-bold'>$45,231</div>
              <p className='text-xs text-gray-500'>+8% from last month</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium'>Orders</CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-2xl font-bold'>573</div>
              <p className='text-xs text-gray-500'>+23% from last month</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium'>Conversion</CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-2xl font-bold'>3.2%</div>
              <p className='text-xs text-gray-500'>+0.5% from last month</p>
            </CardContent>
          </Card>
        </div>

        <div className='grid grid-cols-1 lg:grid-cols-2 gap-4'>
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>Your recent activities</CardDescription>
            </CardHeader>
            <CardContent>
              <p className='text-gray-500'>No recent activity</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Stats</CardTitle>
              <CardDescription>Overview of your metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <p className='text-gray-500'>Loading stats...</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}}

export default {pascal_name}
"""


def create_page(project_path: Path, name: str, page_type: str = "basic"):
    """Create a new page."""
    print(f"\n📄 Generating {name} page ({page_type})\n")
    
    # Generate page content based on type
    generators = {
        "basic": generate_basic_page,
        "list": generate_list_page,
        "detail": generate_detail_page,
        "form": generate_form_page,
        "dashboard": generate_dashboard_page,
    }
    
    if page_type not in generators:
        print(f"✗ Unknown page type: {page_type}")
        print(f"Available types: {', '.join(generators.keys())}")
        return False
    
    generator = generators[page_type]
    content = generator(name)
    
    # Determine page path
    pascal_name = to_pascal_case(name)
    page_path = project_path / "src" / "pages" / f"{pascal_name}.tsx"
    
    # Create directory if it doesn't exist
    page_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write page file
    page_path.write_text(content)
    print(f"✓ Created {page_path.relative_to(project_path)}")
    
    return True


def find_frontend_package(project_path: Path, package_name: str = None):
    """Find a frontend package in the monorepo."""
    packages_dir = project_path / "packages"
    
    if not packages_dir.exists():
        print("✗ Not a valid monorepo project (packages directory not found)")
        return None
    
    if package_name:
        package_path = packages_dir / package_name
        if package_path.exists() and (package_path / "src").exists():
            return package_path
        else:
            print(f"✗ Frontend package '{package_name}' not found or not configured")
            return None
    
    # Find first frontend package with src directory
    for package_dir in packages_dir.iterdir():
        if package_dir.is_dir() and (package_dir / "src").exists():
            return package_dir
    
    print("✗ No frontend package found in monorepo")
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate a new React page")
    parser.add_argument("name", help="Page name (e.g., Dashboard, user-list)")
    parser.add_argument("--type", choices=["basic", "list", "detail", "form", "dashboard"],
                        default="basic", help="Page type")
    parser.add_argument("--package", help="Target package name")
    parser.add_argument("--project-path", default=".", help="Path to the monorepo project")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    
    # Find package
    package_path = find_frontend_package(project_path, args.package)
    if not package_path:
        sys.exit(1)
    
    print(f"\n📦 Target package: {package_path.name}\n")
    
    # Create page
    if not create_page(package_path, args.name, args.type):
        sys.exit(1)
    
    pascal_name = to_pascal_case(args.name)
    print(f"\n✅ Page '{pascal_name}' generated successfully!\n")
    print("Usage:")
    print(f"  import {{ {pascal_name} }} from '@/pages/{pascal_name}'")


if __name__ == "__main__":
    main()

