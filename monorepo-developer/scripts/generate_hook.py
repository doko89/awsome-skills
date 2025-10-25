#!/usr/bin/env python3
"""
Generate a new React custom hook in a monorepo frontend package.
"""

import argparse
import sys
from pathlib import Path


def to_camel_case(name: str) -> str:
    """Convert string to camelCase."""
    parts = name.replace('-', ' ').replace('_', ' ').split()
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase."""
    return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())


def generate_basic_hook(name: str) -> str:
    """Generate basic hook."""
    camel_name = to_camel_case(name)
    
    return f"""import {{ useState }} from 'react'

export function {camel_name}() {{
  const [state, setState] = useState(null)

  return {{
    state,
    setState,
  }}
}}
"""


def generate_fetch_hook(name: str) -> str:
    """Generate fetch hook."""
    camel_name = to_camel_case(name)
    
    return f"""import {{ useState, useEffect }} from 'react'

interface FetchState<T> {{
  data: T | null
  loading: boolean
  error: Error | null
}}

export function {camel_name}<T>(url: string) {{
  const [state, setState] = useState<FetchState<T>>({{'
    data: null,
    loading: true,
    error: null,
  }})

  useEffect(() => {{
    let isMounted = true

    const fetchData = async () => {{
      try {{
        const response = await fetch(url)
        if (!response.ok) throw new Error('Failed to fetch')
        const data = await response.json()
        
        if (isMounted) {{
          setState({{ data, loading: false, error: null }})
        }}
      }} catch (error) {{
        if (isMounted) {{
          setState({{ data: null, loading: false, error: error as Error }})
        }}
      }}
    }}

    fetchData()

    return () => {{
      isMounted = false
    }}
  }}, [url])

  return state
}}
"""


def generate_local_storage_hook(name: str) -> str:
    """Generate localStorage hook."""
    camel_name = to_camel_case(name)
    
    return f"""import {{ useState, useEffect }} from 'react'

export function {camel_name}<T>(key: string, initialValue: T) {{
  const [storedValue, setStoredValue] = useState<T>(() => {{
    try {{
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    }} catch (error) {{
      console.error(error)
      return initialValue
    }}
  }})

  const setValue = (value: T | ((val: T) => T)) => {{
    try {{
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    }} catch (error) {{
      console.error(error)
    }}
  }}

  return [storedValue, setValue] as const
}}
"""


def generate_debounce_hook(name: str) -> str:
    """Generate debounce hook."""
    camel_name = to_camel_case(name)
    
    return f"""import {{ useState, useEffect }} from 'react'

export function {camel_name}<T>(value: T, delay: number): T {{
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {{
    const handler = setTimeout(() => {{
      setDebouncedValue(value)
    }}, delay)

    return () => clearTimeout(handler)
  }}, [value, delay])

  return debouncedValue
}}
"""


def generate_throttle_hook(name: str) -> str:
    """Generate throttle hook."""
    camel_name = to_camel_case(name)
    
    return f"""import {{ useRef, useCallback }} from 'react'

export function {camel_name}<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): T {{
  const lastRun = useRef(Date.now())

  return useCallback((...args: any[]) => {{
    const now = Date.now()
    if (now - lastRun.current >= delay) {{
      callback(...args)
      lastRun.current = now
    }}
  }}, [callback, delay]) as T
}}
"""


def generate_toggle_hook(name: str) -> str:
    """Generate toggle hook."""
    camel_name = to_camel_case(name)
    
    return f"""import {{ useState, useCallback }} from 'react'

export function {camel_name}(initialValue: boolean = false) {{
  const [value, setValue] = useState(initialValue)

  const toggle = useCallback(() => {{
    setValue(prev => !prev)
  }}, [])

  const setTrue = useCallback(() => {{
    setValue(true)
  }}, [])

  const setFalse = useCallback(() => {{
    setValue(false)
  }}, [])

  return {{
    value,
    toggle,
    setTrue,
    setFalse,
    setValue,
  }}
}}
"""


def generate_previous_hook(name: str) -> str:
    """Generate usePrevious hook."""
    camel_name = to_camel_case(name)
    
    return f"""import {{ useEffect, useRef }} from 'react'

export function {camel_name}<T>(value: T): T | undefined {{
  const ref = useRef<T>()

  useEffect(() => {{
    ref.current = value
  }}, [value])

  return ref.current
}}
"""


def generate_async_hook(name: str) -> str:
    """Generate async hook."""
    camel_name = to_camel_case(name)
    
    return f"""import {{ useState, useCallback }} from 'react'

interface AsyncState<T> {{
  status: 'idle' | 'pending' | 'success' | 'error'
  data: T | null
  error: Error | null
}}

export function {camel_name}<T>(
  asyncFunction: () => Promise<T>,
  immediate: boolean = true
) {{
  const [state, setState] = useState<AsyncState<T>>({{'
    status: 'idle',
    data: null,
    error: null,
  }})

  const execute = useCallback(async () => {{
    setState({{ status: 'pending', data: null, error: null }})
    try {{
      const response = await asyncFunction()
      setState({{ status: 'success', data: response, error: null }})
      return response
    }} catch (error) {{
      setState({{ status: 'error', data: null, error: error as Error }})
      throw error
    }}
  }}, [asyncFunction])

  return {{
    ...state,
    execute,
  }}
}}
"""


def create_hook(project_path: Path, name: str, hook_type: str = "basic"):
    """Create a new hook."""
    print(f"\n🎣 Generating {name} hook ({hook_type})\n")
    
    # Generate hook content based on type
    generators = {
        "basic": generate_basic_hook,
        "fetch": generate_fetch_hook,
        "local-storage": generate_local_storage_hook,
        "debounce": generate_debounce_hook,
        "throttle": generate_throttle_hook,
        "toggle": generate_toggle_hook,
        "previous": generate_previous_hook,
        "async": generate_async_hook,
    }
    
    if hook_type not in generators:
        print(f"✗ Unknown hook type: {hook_type}")
        print(f"Available types: {', '.join(generators.keys())}")
        return False
    
    generator = generators[hook_type]
    content = generator(name)
    
    # Determine hook path
    camel_name = to_camel_case(name)
    hook_path = project_path / "src" / "hooks" / f"{camel_name}.ts"
    
    # Create directory if it doesn't exist
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write hook file
    hook_path.write_text(content)
    print(f"✓ Created {hook_path.relative_to(project_path)}")
    
    # Create index.ts if it doesn't exist
    index_path = hook_path.parent / "index.ts"
    if not index_path.exists():
        index_path.write_text(f"export {{ {camel_name} }} from './{camel_name}'\n")
        print(f"✓ Created {index_path.relative_to(project_path)}")
    else:
        # Append to existing index.ts
        with open(index_path, 'a') as f:
            f.write(f"export {{ {camel_name} }} from './{camel_name}'\n")
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
    parser = argparse.ArgumentParser(description="Generate a new React custom hook")
    parser.add_argument("name", help="Hook name (e.g., useCounter, use-counter)")
    parser.add_argument("--type", choices=["basic", "fetch", "local-storage", "debounce", "throttle", "toggle", "previous", "async"],
                        default="basic", help="Hook type")
    parser.add_argument("--package", help="Target package name")
    parser.add_argument("--project-path", default=".", help="Path to the monorepo project")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    
    # Find package
    package_path = find_frontend_package(project_path, args.package)
    if not package_path:
        sys.exit(1)
    
    print(f"\n📦 Target package: {package_path.name}\n")
    
    # Create hook
    if not create_hook(package_path, args.name, args.type):
        sys.exit(1)
    
    camel_name = to_camel_case(args.name)
    print(f"\n✅ Hook '{camel_name}' generated successfully!\n")
    print("Usage:")
    print(f"  import {{ {camel_name} }} from '@/hooks'")


if __name__ == "__main__":
    main()

