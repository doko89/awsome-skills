#!/usr/bin/env python3
"""
Initialize a new React project with Vite, TypeScript, and shadcn/ui.
"""

import argparse
import subprocess
import sys
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


def create_react_project(project_name: str, use_typescript: bool = True):
    """Create a new React project with Vite."""
    print(f"\n🚀 Creating React project: {project_name}\n")
    
    # Create Vite project
    template = "react-ts" if use_typescript else "react"
    if not run_command(f"npm create vite@latest {project_name} -- --template {template}"):
        return False
    
    project_path = Path(project_name)
    
    print("\n📦 Installing dependencies...\n")
    if not run_command("npm install", cwd=project_path):
        return False
    
    return project_path


def install_tailwind(project_path: Path):
    """Install and configure Tailwind CSS."""
    print("\n🎨 Installing Tailwind CSS...\n")
    
    # Install Tailwind and dependencies
    if not run_command(
        "npm install -D tailwindcss@^4.1.16 postcss autoprefixer",
        cwd=project_path
    ):
        return False
    
    # Initialize Tailwind
    if not run_command("npx tailwindcss init -p", cwd=project_path):
        return False
    
    # Update tailwind.config.js
    tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
    
    config_file = project_path / "tailwind.config.js"
    config_file.write_text(tailwind_config)
    print("✓ Updated tailwind.config.js")
    
    # Update src/index.css
    index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
    
    css_file = project_path / "src" / "index.css"
    css_file.write_text(index_css)
    print("✓ Updated src/index.css")
    
    return True


def install_shadcn(project_path: Path):
    """Install and configure shadcn/ui."""
    print("\n✨ Installing shadcn/ui...\n")
    
    # Run shadcn init with default options
    command = "npx shadcn@latest init -d"
    if not run_command(command, cwd=project_path):
        print("⚠ shadcn init failed, trying manual setup...")
        return manual_shadcn_setup(project_path)
    
    return True


def manual_shadcn_setup(project_path: Path):
    """Manual shadcn/ui setup if auto-init fails."""
    # Install required dependencies
    deps = [
        "class-variance-authority",
        "clsx",
        "tailwind-merge",
        "@radix-ui/react-slot"
    ]
    
    if not run_command(f"npm install {' '.join(deps)}", cwd=project_path):
        return False
    
    # Create components.json
    components_json = """{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "zinc",
    "cssVariables": true,
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
"""
    
    (project_path / "components.json").write_text(components_json)
    print("✓ Created components.json")
    
    # Create lib/utils.ts
    lib_dir = project_path / "src" / "lib"
    lib_dir.mkdir(exist_ok=True)
    
    utils_ts = """import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"""
    
    (lib_dir / "utils.ts").write_text(utils_ts)
    print("✓ Created src/lib/utils.ts")
    
    # Update tsconfig.json for path aliases
    tsconfig_path = project_path / "tsconfig.json"
    if tsconfig_path.exists():
        import json
        with open(tsconfig_path, 'r') as f:
            tsconfig = json.load(f)
        
        if "compilerOptions" not in tsconfig:
            tsconfig["compilerOptions"] = {}
        
        tsconfig["compilerOptions"]["baseUrl"] = "."
        tsconfig["compilerOptions"]["paths"] = {
            "@/*": ["./src/*"]
        }
        
        with open(tsconfig_path, 'w') as f:
            json.dump(tsconfig, f, indent=2)
        
        print("✓ Updated tsconfig.json")
    
    # Update vite.config.ts for path aliases
    vite_config_path = project_path / "vite.config.ts"
    if vite_config_path.exists():
        vite_config = """import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
"""
        vite_config_path.write_text(vite_config)
        print("✓ Updated vite.config.ts")
    
    return True


def install_additional_packages(project_path: Path):
    """Install additional useful packages."""
    print("\n📦 Installing additional packages...\n")
    
    packages = [
        "react-router-dom@^7.9.4",
        "@tanstack/react-query@^5.90.5",
        "axios@^1.12.2",
        "zustand@^5.0.8"
    ]
    
    if not run_command(f"npm install {' '.join(packages)}", cwd=project_path):
        print("⚠ Failed to install some packages")
        return False
    
    return True


def create_project_structure(project_path: Path):
    """Create additional project structure."""
    print("\n📁 Creating project structure...\n")
    
    directories = [
        "src/components/ui",
        "src/components/layout",
        "src/pages",
        "src/hooks",
        "src/lib",
        "src/services",
        "src/store",
        "src/types",
        "src/utils",
    ]
    
    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")
    
    return True


def create_readme(project_path: Path, project_name: str):
    """Create README.md."""
    readme = f"""# {project_name}

A React application built with Vite, TypeScript, Tailwind CSS, and shadcn/ui.

## Features

- ⚡️ Vite - Fast build tool
- ⚛️ React 19 - Latest React version
- 🎨 Tailwind CSS - Utility-first CSS framework
- 🧩 shadcn/ui - Beautiful UI components
- 📝 TypeScript - Type safety
- 🔄 React Router - Client-side routing
- 🔍 TanStack Query - Data fetching and caching
- 🐻 Zustand - State management
- 📡 Axios - HTTP client

## Getting Started

### Install dependencies

```bash
npm install
```

### Run development server

```bash
npm run dev
```

### Build for production

```bash
npm run build
```

### Preview production build

```bash
npm run preview
```

## Adding shadcn/ui Components

Add components from shadcn/ui:

```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
```

## Project Structure

```
src/
├── components/
│   ├── ui/          # shadcn/ui components
│   └── layout/      # Layout components
├── pages/           # Page components
├── hooks/           # Custom hooks
├── lib/             # Utility functions
├── services/        # API services
├── store/           # State management
├── types/           # TypeScript types
└── utils/           # Helper functions
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Learn More

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [React Router](https://reactrouter.com/)
- [TanStack Query](https://tanstack.com/query/)
"""
    
    (project_path / "README.md").write_text(readme)
    print("✓ Created README.md")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Initialize a new React project")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--no-typescript", action="store_true", help="Use JavaScript instead of TypeScript")
    parser.add_argument("--skip-shadcn", action="store_true", help="Skip shadcn/ui installation")
    parser.add_argument("--skip-packages", action="store_true", help="Skip additional packages")
    
    args = parser.parse_args()
    
    use_typescript = not args.no_typescript
    
    # Create React project
    project_path = create_react_project(args.project_name, use_typescript)
    if not project_path:
        print("✗ Failed to create React project")
        sys.exit(1)
    
    # Install Tailwind CSS
    if not install_tailwind(project_path):
        print("✗ Failed to install Tailwind CSS")
        sys.exit(1)
    
    # Install shadcn/ui
    if not args.skip_shadcn:
        if not install_shadcn(project_path):
            print("✗ Failed to install shadcn/ui")
            sys.exit(1)
    
    # Install additional packages
    if not args.skip_packages:
        install_additional_packages(project_path)
    
    # Create project structure
    create_project_structure(project_path)
    
    # Create README
    create_readme(project_path, args.project_name)
    
    print(f"\n✅ Project '{args.project_name}' initialized successfully!\n")
    print("Next steps:")
    print(f"  1. cd {args.project_name}")
    print("  2. npm run dev")
    print("\nTo add shadcn/ui components:")
    print("  npx shadcn@latest add button")
    print("  npx shadcn@latest add card")
    print("  npx shadcn@latest add dialog")


if __name__ == "__main__":
    main()

