#!/usr/bin/env python3
"""
Generate a new package in the monorepo.
"""

import argparse
import json
import sys
from pathlib import Path


def to_pascal_case(text: str) -> str:
    """Convert snake_case to PascalCase."""
    return ''.join(word.capitalize() for word in text.split('_'))


def create_backend_package(project_path: Path, package_name: str):
    """Create a new backend package."""
    print(f"\n🔧 Creating backend package: {package_name}\n")
    
    package_path = project_path / "packages" / package_name
    
    # Create directories
    (package_path / "src" / "routes").mkdir(parents=True, exist_ok=True)
    (package_path / "src" / "middleware").mkdir(parents=True, exist_ok=True)
    (package_path / "src" / "services").mkdir(parents=True, exist_ok=True)
    
    # Create package.json
    package_json = {
        "name": f"@monorepo/{package_name}",
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "bun run --watch src/index.ts",
            "build": "bun build src/index.ts --outdir dist",
            "start": "bun dist/index.js"
        },
        "dependencies": {
            "hono": "^4.10.3"
        },
        "devDependencies": {
            "@types/bun": "latest",
            "typescript": "^5.9.3"
        }
    }
    
    (package_path / "package.json").write_text(json.dumps(package_json, indent=2))
    print("✓ Created package.json")
    
    # Create tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "ESNext",
            "lib": ["ES2020"],
            "moduleResolution": "bundler",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "resolveJsonModule": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True,
            "outDir": "./dist",
            "baseUrl": ".",
            "paths": {
                "@/*": ["./src/*"]
            }
        },
        "include": ["src"],
        "exclude": ["node_modules", "dist"]
    }
    
    (package_path / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    print("✓ Created tsconfig.json")
    
    # Create index.ts
    index_ts = f"""import {{ Hono }} from 'hono'

const app = new Hono()

// Health check endpoint
app.get('/health', (c) => {{
  return c.json({{ status: 'ok', service: '{package_name}' }})
}})

export default {{
  port: 3001,
  fetch: app.fetch,
}}
"""
    
    (package_path / "src" / "index.ts").write_text(index_ts)
    print("✓ Created src/index.ts")
    
    # Create example route
    route_ts = f"""import {{ Hono }} from 'hono'

const router = new Hono()

router.get('/', (c) => {{
  return c.json({{ message: 'Welcome to {package_name}' }})
}})

export default router
"""
    
    (package_path / "src" / "routes" / "index.ts").write_text(route_ts)
    print("✓ Created src/routes/index.ts")
    
    print(f"✅ Backend package '{package_name}' created successfully!")
    return True


def create_frontend_package(project_path: Path, package_name: str):
    """Create a new frontend package."""
    print(f"\n⚛️  Creating frontend package: {package_name}\n")
    
    package_path = project_path / "packages" / package_name
    
    # Create directories
    (package_path / "src" / "components" / "ui").mkdir(parents=True, exist_ok=True)
    (package_path / "src" / "pages").mkdir(parents=True, exist_ok=True)
    (package_path / "src" / "hooks").mkdir(parents=True, exist_ok=True)
    (package_path / "src" / "lib").mkdir(parents=True, exist_ok=True)
    
    # Create package.json
    package_json = {
        "name": f"@monorepo/{package_name}",
        "version": "1.0.0",
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "preview": "vite preview"
        },
        "dependencies": {
            "react": "^19.2.0",
            "react-dom": "^19.2.0",
            "react-router-dom": "^7.9.4",
            "@tanstack/react-query": "^5.90.5",
            "axios": "^1.12.2",
            "zustand": "^5.0.8",
            "class-variance-authority": "^0.7.0",
            "clsx": "^2.1.1",
            "tailwind-merge": "^2.6.0",
            "@radix-ui/react-slot": "^2.1.1"
        },
        "devDependencies": {
            "@types/react": "^19.0.0",
            "@types/react-dom": "^19.0.0",
            "@vitejs/plugin-react": "^4.3.4",
            "typescript": "^5.9.3",
            "vite": "^7.1.12",
            "tailwindcss": "^4.1.16",
            "postcss": "^8.4.49",
            "autoprefixer": "^10.4.20"
        }
    }
    
    (package_path / "package.json").write_text(json.dumps(package_json, indent=2))
    print("✓ Created package.json")
    
    # Create tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "useDefineForClassFields": True,
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "module": "ESNext",
            "skipLibCheck": True,
            "esModuleInterop": True,
            "allowSyntheticDefaultImports": True,
            "strict": True,
            "noUnusedLocals": True,
            "noUnusedParameters": True,
            "noFallthroughCasesInSwitch": True,
            "moduleResolution": "bundler",
            "allowImportingTsExtensions": True,
            "resolveJsonModule": True,
            "isolatedModules": True,
            "noEmit": True,
            "jsx": "react-jsx",
            "baseUrl": ".",
            "paths": {
                "@/*": ["./src/*"]
            }
        },
        "include": ["src"],
        "references": [{"path": "./tsconfig.node.json"}]
    }
    
    (package_path / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    print("✓ Created tsconfig.json")
    
    # Create vite.config.ts
    vite_config = """import path from 'path'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
"""
    
    (package_path / "vite.config.ts").write_text(vite_config)
    print("✓ Created vite.config.ts")
    
    # Create tailwind.config.js
    tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
    
    (package_path / "tailwind.config.js").write_text(tailwind_config)
    print("✓ Created tailwind.config.js")
    
    # Create postcss.config.js
    postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
    
    (package_path / "postcss.config.js").write_text(postcss_config)
    print("✓ Created postcss.config.js")
    
    # Create components.json
    components_json = {
        "$schema": "https://ui.shadcn.com/schema.json",
        "style": "new-york",
        "rsc": False,
        "tsx": True,
        "tailwind": {
            "config": "tailwind.config.js",
            "css": "src/index.css",
            "baseColor": "zinc",
            "cssVariables": True,
            "prefix": ""
        },
        "aliases": {
            "components": "@/components",
            "utils": "@/lib/utils",
            "ui": "@/components/ui",
            "lib": "@/lib",
            "hooks": "@/hooks"
        }
    }
    
    (package_path / "components.json").write_text(json.dumps(components_json, indent=2))
    print("✓ Created components.json")
    
    # Create index.css
    index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
    
    (package_path / "src" / "index.css").write_text(index_css)
    print("✓ Created src/index.css")
    
    # Create lib/utils.ts
    utils_ts = """import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"""
    
    (package_path / "src" / "lib" / "utils.ts").write_text(utils_ts)
    print("✓ Created src/lib/utils.ts")
    
    # Create App.tsx
    app_tsx = f"""function App() {{
  return (
    <div className='min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center'>
      <div className='text-center'>
        <h1 className='text-4xl font-bold text-white mb-4'>{to_pascal_case(package_name)}</h1>
        <p className='text-slate-300'>Frontend application</p>
      </div>
    </div>
  )
}}

export default App
"""
    
    (package_path / "src" / "App.tsx").write_text(app_tsx)
    print("✓ Created src/App.tsx")
    
    # Create main.tsx
    main_tsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
    
    (package_path / "src" / "main.tsx").write_text(main_tsx)
    print("✓ Created src/main.tsx")
    
    # Create index.html
    index_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{to_pascal_case(package_name)}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
    
    (package_path / "index.html").write_text(index_html)
    print("✓ Created index.html")
    
    print(f"✅ Frontend package '{package_name}' created successfully!")
    return True


def create_library_package(project_path: Path, package_name: str):
    """Create a new library package."""
    print(f"\n📦 Creating library package: {package_name}\n")
    
    package_path = project_path / "packages" / package_name
    
    # Create directories
    (package_path / "src").mkdir(parents=True, exist_ok=True)
    
    # Create package.json
    package_json = {
        "name": f"@monorepo/{package_name}",
        "version": "1.0.0",
        "type": "module",
        "main": "dist/index.js",
        "types": "dist/index.d.ts",
        "scripts": {
            "build": "tsc"
        },
        "devDependencies": {
            "typescript": "^5.9.3"
        }
    }
    
    (package_path / "package.json").write_text(json.dumps(package_json, indent=2))
    print("✓ Created package.json")
    
    # Create tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2020",
            "module": "ESNext",
            "lib": ["ES2020"],
            "moduleResolution": "bundler",
            "strict": True,
            "declaration": True,
            "declarationMap": True,
            "sourceMap": True,
            "outDir": "./dist",
            "baseUrl": ".",
            "paths": {
                "@/*": ["./src/*"]
            }
        },
        "include": ["src"],
        "exclude": ["node_modules", "dist"]
    }
    
    (package_path / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    print("✓ Created tsconfig.json")
    
    # Create index.ts
    index_ts = f"""// {to_pascal_case(package_name)} library
export const version = '1.0.0'
"""
    
    (package_path / "src" / "index.ts").write_text(index_ts)
    print("✓ Created src/index.ts")
    
    print(f"✅ Library package '{package_name}' created successfully!")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate a new package in the monorepo")
    parser.add_argument("package_name", help="Name of the package")
    parser.add_argument("--type", choices=["backend", "frontend", "library"], default="library",
                        help="Type of package to generate")
    parser.add_argument("--project-path", default=".", help="Path to the monorepo project")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    
    if not (project_path / "packages").exists():
        print("✗ Not a valid monorepo project (packages directory not found)")
        sys.exit(1)
    
    package_path = project_path / "packages" / args.package_name
    
    if package_path.exists():
        print(f"✗ Package '{args.package_name}' already exists")
        sys.exit(1)
    
    print(f"\n🚀 Generating {args.type} package: {args.package_name}\n")
    
    if args.type == "backend":
        if not create_backend_package(project_path, args.package_name):
            print("✗ Failed to create backend package")
            sys.exit(1)
    elif args.type == "frontend":
        if not create_frontend_package(project_path, args.package_name):
            print("✗ Failed to create frontend package")
            sys.exit(1)
    else:  # library
        if not create_library_package(project_path, args.package_name):
            print("✗ Failed to create library package")
            sys.exit(1)
    
    print(f"\nNext steps:")
    print(f"  1. cd packages/{args.package_name}")
    print(f"  2. bun install")
    print(f"  3. bun run dev")


if __name__ == "__main__":
    main()

