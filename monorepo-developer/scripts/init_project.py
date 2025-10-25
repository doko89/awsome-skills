#!/usr/bin/env python3
"""
Initialize a new monorepo project with Bun, Hono backend, and React frontend.
"""

import argparse
import subprocess
import sys
import json
from pathlib import Path


def run_command(command: str, cwd: Path = None, shell: bool = True):
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


def create_project_structure(project_path: Path):
    """Create monorepo directory structure."""
    print(f"\n📁 Creating project structure...\n")
    
    directories = [
        "packages/backend/src/routes",
        "packages/backend/src/middleware",
        "packages/backend/src/services",
        "packages/backend/src/db",
        "packages/frontend/src/components/ui",
        "packages/frontend/src/components/layout",
        "packages/frontend/src/pages",
        "packages/frontend/src/hooks",
        "packages/frontend/src/lib",
        "packages/frontend/src/services",
        "packages/frontend/src/store",
        "packages/frontend/src/types",
        "packages/frontend/src/utils",
        "packages/shared/src/types",
        "packages/shared/src/utils",
    ]
    
    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")
    
    return True


def create_root_package_json(project_path: Path):
    """Create root package.json."""
    package_json = {
        "name": project_path.name,
        "version": "1.0.0",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "bun run --cwd packages/backend dev & bun run --cwd packages/frontend dev",
            "build": "bun run --cwd packages/backend build && bun run --cwd packages/frontend build",
            "start": "bun run --cwd packages/backend start",
            "install": "bun install"
        },
        "workspaces": [
            "packages/*"
        ]
    }
    
    (project_path / "package.json").write_text(json.dumps(package_json, indent=2))
    print("✓ Created root package.json")
    return True


def create_backend_package(project_path: Path):
    """Create backend package with Hono."""
    print("\n🔧 Creating backend package...\n")
    
    backend_path = project_path / "packages" / "backend"
    
    # Create package.json
    package_json = {
        "name": "@monorepo/backend",
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
    
    (backend_path / "package.json").write_text(json.dumps(package_json, indent=2))
    print("✓ Created backend package.json")
    
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
    
    (backend_path / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    print("✓ Created backend tsconfig.json")
    
    # Create main index.ts
    index_ts = """import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => {
  return c.json({ message: 'Hello from Hono!' })
})

app.get('/api/health', (c) => {
  return c.json({ status: 'ok' })
})

export default {
  port: 3000,
  fetch: app.fetch,
}
"""
    
    (backend_path / "src" / "index.ts").write_text(index_ts)
    print("✓ Created backend src/index.ts")
    
    return True


def create_frontend_package(project_path: Path):
    """Create frontend package with React and shadcn/ui."""
    print("\n⚛️  Creating frontend package...\n")
    
    frontend_path = project_path / "packages" / "frontend"
    
    # Create package.json
    package_json = {
        "name": "@monorepo/frontend",
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
    
    (frontend_path / "package.json").write_text(json.dumps(package_json, indent=2))
    print("✓ Created frontend package.json")
    
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
    
    (frontend_path / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    print("✓ Created frontend tsconfig.json")
    
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
    
    (frontend_path / "vite.config.ts").write_text(vite_config)
    print("✓ Created frontend vite.config.ts")
    
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
    
    (frontend_path / "tailwind.config.js").write_text(tailwind_config)
    print("✓ Created frontend tailwind.config.js")
    
    # Create postcss.config.js
    postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
    
    (frontend_path / "postcss.config.js").write_text(postcss_config)
    print("✓ Created frontend postcss.config.js")
    
    # Create components.json for shadcn/ui
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
    
    (frontend_path / "components.json").write_text(json.dumps(components_json, indent=2))
    print("✓ Created frontend components.json")
    
    # Create index.css
    index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
    
    (frontend_path / "src" / "index.css").write_text(index_css)
    print("✓ Created frontend src/index.css")
    
    # Create lib/utils.ts
    lib_path = frontend_path / "src" / "lib"
    lib_path.mkdir(exist_ok=True)
    
    utils_ts = """import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"""
    
    (lib_path / "utils.ts").write_text(utils_ts)
    print("✓ Created frontend src/lib/utils.ts")
    
    # Create App.tsx
    app_tsx = """import { Button } from '@/components/ui/button'

function App() {
  return (
    <div className='min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center'>
      <div className='text-center'>
        <h1 className='text-4xl font-bold text-white mb-4'>Welcome to Monorepo</h1>
        <p className='text-slate-300 mb-8'>Built with Bun, Hono, React, and shadcn/ui</p>
        <Button size='lg'>Get Started</Button>
      </div>
    </div>
  )
}

export default App
"""
    
    (frontend_path / "src" / "App.tsx").write_text(app_tsx)
    print("✓ Created frontend src/App.tsx")
    
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
    
    (frontend_path / "src" / "main.tsx").write_text(main_tsx)
    print("✓ Created frontend src/main.tsx")
    
    # Create index.html
    index_html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Monorepo App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
    
    (frontend_path / "index.html").write_text(index_html)
    print("✓ Created frontend index.html")
    
    return True


def create_shared_package(project_path: Path):
    """Create shared package."""
    print("\n📦 Creating shared package...\n")
    
    shared_path = project_path / "packages" / "shared"
    
    # Create package.json
    package_json = {
        "name": "@monorepo/shared",
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
    
    (shared_path / "package.json").write_text(json.dumps(package_json, indent=2))
    print("✓ Created shared package.json")
    
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
    
    (shared_path / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    print("✓ Created shared tsconfig.json")
    
    # Create index.ts
    index_ts = """// Shared types and utilities
export const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:3000'
"""
    
    (shared_path / "src" / "index.ts").write_text(index_ts)
    print("✓ Created shared src/index.ts")
    
    return True


def create_bunfig(project_path: Path):
    """Create bunfig.toml."""
    bunfig = """# Bun configuration

[install]
# Use exact versions
exact = true

[build]
# Output directory
outdir = "dist"

[test]
# Test configuration
root = "."
"""
    
    (project_path / "bunfig.toml").write_text(bunfig)
    print("✓ Created bunfig.toml")
    return True


def create_gitignore(project_path: Path):
    """Create .gitignore."""
    gitignore = """# Dependencies
node_modules/
bun.lockb

# Build
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""
    
    (project_path / ".gitignore").write_text(gitignore)
    print("✓ Created .gitignore")
    return True


def create_readme(project_path: Path, project_name: str):
    """Create README.md."""
    readme = f"""# {project_name}

A modern monorepo application built with Bun, Hono, React, and shadcn/ui.

## Features

- 🚀 **Bun** - Fast JavaScript runtime and package manager
- 🔧 **Hono** - Lightweight web framework for backend
- ⚛️ **React 19** - Latest React version
- 🎨 **Tailwind CSS** - Utility-first CSS framework
- 🧩 **shadcn/ui** - Beautiful UI components
- 📝 **TypeScript** - Type safety across the stack
- 📦 **Monorepo** - Organized package structure

## Project Structure

```
{project_name}/
├── packages/
│   ├── backend/     # Hono backend service
│   ├── frontend/    # React frontend application
│   └── shared/      # Shared types and utilities
├── bunfig.toml      # Bun configuration
└── package.json     # Root package configuration
```

## Getting Started

### Prerequisites

- [Bun](https://bun.sh) installed

### Installation

```bash
cd {project_name}
bun install
```

### Development

Start both backend and frontend:

```bash
bun run dev
```

- Backend: http://localhost:3000
- Frontend: http://localhost:5173

### Build

```bash
bun run build
```

### Production

```bash
bun run start
```

## Packages

### Backend (`packages/backend`)

Hono-based REST API server.

```bash
cd packages/backend
bun run dev
```

### Frontend (`packages/frontend`)

React application with shadcn/ui components.

```bash
cd packages/frontend
bun run dev
```

### Shared (`packages/shared`)

Shared types and utilities used across packages.

## Adding Components

Add shadcn/ui components to frontend:

```bash
cd packages/frontend
npx shadcn@latest add button
npx shadcn@latest add card
```

## Learn More

- [Bun Documentation](https://bun.sh/docs)
- [Hono Documentation](https://hono.dev)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [shadcn/ui](https://ui.shadcn.com)

## License

MIT
"""
    
    (project_path / "README.md").write_text(readme)
    print("✓ Created README.md")
    return True


def main():
    parser = argparse.ArgumentParser(description="Initialize a new monorepo project")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--skip-git", action="store_true", help="Skip git initialization")
    parser.add_argument("--skip-install", action="store_true", help="Skip dependency installation")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_name)
    
    if project_path.exists():
        print(f"✗ Directory '{args.project_name}' already exists")
        sys.exit(1)
    
    project_path.mkdir(parents=True)
    
    print(f"\n🚀 Creating monorepo: {args.project_name}\n")
    
    # Create structure
    if not create_project_structure(project_path):
        print("✗ Failed to create project structure")
        sys.exit(1)
    
    # Create root files
    if not create_root_package_json(project_path):
        print("✗ Failed to create root package.json")
        sys.exit(1)
    
    # Create packages
    if not create_backend_package(project_path):
        print("✗ Failed to create backend package")
        sys.exit(1)
    
    if not create_frontend_package(project_path):
        print("✗ Failed to create frontend package")
        sys.exit(1)
    
    if not create_shared_package(project_path):
        print("✗ Failed to create shared package")
        sys.exit(1)
    
    # Create config files
    if not create_bunfig(project_path):
        print("✗ Failed to create bunfig.toml")
        sys.exit(1)
    
    if not create_gitignore(project_path):
        print("✗ Failed to create .gitignore")
        sys.exit(1)
    
    if not create_readme(project_path, args.project_name):
        print("✗ Failed to create README.md")
        sys.exit(1)
    
    # Initialize git
    if not args.skip_git:
        print("\n📚 Initializing git repository...\n")
        if not run_command("git init", cwd=project_path):
            print("⚠ Failed to initialize git")
    
    # Install dependencies
    if not args.skip_install:
        print("\n📦 Installing dependencies...\n")
        if not run_command("bun install", cwd=project_path):
            print("⚠ Failed to install dependencies")
    
    print(f"\n✅ Monorepo '{args.project_name}' initialized successfully!\n")
    print("Next steps:")
    print(f"  1. cd {args.project_name}")
    print("  2. bun run dev")
    print("\nTo add shadcn/ui components:")
    print("  cd packages/frontend")
    print("  npx shadcn@latest add button")


if __name__ == "__main__":
    main()

