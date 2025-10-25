#!/usr/bin/env python3
"""
Generate a custom React hook.
"""

import argparse
import sys
from pathlib import Path


def to_camel_case(name: str) -> str:
    """Convert string to camelCase."""
    words = name.replace('-', ' ').replace('_', ' ').split()
    if not words:
        return name
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


def ensure_use_prefix(name: str) -> str:
    """Ensure hook name starts with 'use'."""
    camel_name = to_camel_case(name)
    if not camel_name.startswith('use'):
        return 'use' + camel_name[0].upper() + camel_name[1:]
    return camel_name


def generate_basic_hook(name: str) -> str:
    """Generate basic custom hook."""
    hook_name = ensure_use_prefix(name)
    
    return f"""import {{ useState, useEffect }} from "react"

export function {hook_name}() {{
  const [value, setValue] = useState<string>("")

  useEffect(() => {{
    // Add your effect logic here
  }}, [])

  return {{ value, setValue }}
}}
"""


def generate_fetch_hook(name: str) -> str:
    """Generate data fetching hook."""
    hook_name = ensure_use_prefix(name)
    
    return f"""import {{ useState, useEffect }} from "react"

interface {hook_name[0].upper() + hook_name[1:]}Options {{
  url: string
  enabled?: boolean
}}

interface {hook_name[0].upper() + hook_name[1:]}Result<T> {{
  data: T | null
  isLoading: boolean
  error: Error | null
  refetch: () => void
}}

export function {hook_name}<T = any>({{
  url,
  enabled = true
}}: {hook_name[0].upper() + hook_name[1:]}Options): {hook_name[0].upper() + hook_name[1:]}Result<T> {{
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const fetchData = async () => {{
    if (!enabled) return

    setIsLoading(true)
    setError(null)

    try {{
      const response = await fetch(url)
      if (!response.ok) {{
        throw new Error(`HTTP error! status: ${{response.status}}`)
      }}
      const result = await response.json()
      setData(result)
    }} catch (err) {{
      setError(err instanceof Error ? err : new Error('An error occurred'))
    }} finally {{
      setIsLoading(false)
    }}
  }}

  useEffect(() => {{
    fetchData()
  }}, [url, enabled])

  return {{ data, isLoading, error, refetch: fetchData }}
}}
"""


def generate_local_storage_hook(name: str) -> str:
    """Generate localStorage hook."""
    hook_name = ensure_use_prefix(name)
    
    return f"""import {{ useState, useEffect }} from "react"

export function {hook_name}<T>(key: string, initialValue: T) {{
  // Get from local storage then parse stored json or return initialValue
  const readValue = (): T => {{
    if (typeof window === 'undefined') {{
      return initialValue
    }}

    try {{
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    }} catch (error) {{
      console.warn(`Error reading localStorage key "${{key}}":`, error)
      return initialValue
    }}
  }}

  const [storedValue, setStoredValue] = useState<T>(readValue)

  // Return a wrapped version of useState's setter function that persists the new value to localStorage
  const setValue = (value: T | ((val: T) => T)) => {{
    try {{
      // Allow value to be a function so we have same API as useState
      const valueToStore = value instanceof Function ? value(storedValue) : value
      
      // Save state
      setStoredValue(valueToStore)
      
      // Save to local storage
      if (typeof window !== 'undefined') {{
        window.localStorage.setItem(key, JSON.stringify(valueToStore))
      }}
    }} catch (error) {{
      console.warn(`Error setting localStorage key "${{key}}":`, error)
    }}
  }}

  useEffect(() => {{
    setStoredValue(readValue())
  }}, [])

  return [storedValue, setValue] as const
}}
"""


def generate_debounce_hook(name: str) -> str:
    """Generate debounce hook."""
    hook_name = ensure_use_prefix(name)
    
    return f"""import {{ useState, useEffect }} from "react"

export function {hook_name}<T>(value: T, delay: number = 500): T {{
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {{
    const handler = setTimeout(() => {{
      setDebouncedValue(value)
    }}, delay)

    return () => {{
      clearTimeout(handler)
    }}
  }}, [value, delay])

  return debouncedValue
}}
"""


def generate_media_query_hook(name: str) -> str:
    """Generate media query hook."""
    hook_name = ensure_use_prefix(name)
    
    return f"""import {{ useState, useEffect }} from "react"

export function {hook_name}(query: string): boolean {{
  const [matches, setMatches] = useState(false)

  useEffect(() => {{
    const media = window.matchMedia(query)
    
    if (media.matches !== matches) {{
      setMatches(media.matches)
    }}

    const listener = () => setMatches(media.matches)
    
    // Use addEventListener instead of addListener for modern browsers
    if (media.addEventListener) {{
      media.addEventListener('change', listener)
      return () => media.removeEventListener('change', listener)
    }} else {{
      // Fallback for older browsers
      media.addListener(listener)
      return () => media.removeListener(listener)
    }}
  }}, [matches, query])

  return matches
}}

// Convenience hooks for common breakpoints
export function useIsMobile() {{
  return {hook_name}('(max-width: 768px)')
}}

export function useIsTablet() {{
  return {hook_name}('(min-width: 769px) and (max-width: 1024px)')
}}

export function useIsDesktop() {{
  return {hook_name}('(min-width: 1025px)')
}}
"""


def generate_toggle_hook(name: str) -> str:
    """Generate toggle hook."""
    hook_name = ensure_use_prefix(name)
    
    return f"""import {{ useState, useCallback }} from "react"

export function {hook_name}(initialValue: boolean = false) {{
  const [value, setValue] = useState(initialValue)

  const toggle = useCallback(() => {{
    setValue(v => !v)
  }}, [])

  const setTrue = useCallback(() => {{
    setValue(true)
  }}, [])

  const setFalse = useCallback(() => {{
    setValue(false)
  }}, [])

  return {{ value, toggle, setTrue, setFalse, setValue }}
}}
"""


def create_hook(project_path: Path, name: str, hook_type: str = "basic"):
    """Create a new custom hook."""
    print(f"\n🚀 Generating {name} hook\n")
    
    # Generate hook content based on type
    generators = {
        "basic": generate_basic_hook,
        "fetch": generate_fetch_hook,
        "local-storage": generate_local_storage_hook,
        "debounce": generate_debounce_hook,
        "media-query": generate_media_query_hook,
        "toggle": generate_toggle_hook,
    }
    
    generator = generators.get(hook_type, generate_basic_hook)
    content = generator(name)
    
    # Create hook file
    hooks_dir = project_path / "src" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    
    hook_name = ensure_use_prefix(name)
    hook_file = hooks_dir / f"{hook_name}.ts"
    
    if hook_file.exists():
        print(f"⚠ Warning: {hook_file} already exists")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled")
            return False
    
    hook_file.write_text(content)
    print(f"✓ Created {hook_file.relative_to(project_path)}")
    
    # Create index file for easier imports
    index_file = hooks_dir / "index.ts"
    export_line = f"export * from './{hook_name}'\n"
    
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
    print(f"  import {{ {hook_name} }} from '@/hooks'")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate a custom React hook")
    parser.add_argument("name", help="Name of the hook (e.g., 'fetch-data', 'local-storage')")
    parser.add_argument("--project-path", default=".", help="Path to project root")
    parser.add_argument("--type", choices=["basic", "fetch", "local-storage", "debounce", "media-query", "toggle"],
                       default="basic", help="Type of hook to generate")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)
    
    if not (project_path / "package.json").exists():
        print(f"✗ Error: Not a valid Node.js project (package.json not found)")
        sys.exit(1)
    
    if create_hook(project_path, args.name, args.type):
        print("\n✅ Hook generated successfully!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

