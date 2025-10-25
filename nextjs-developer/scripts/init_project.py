#!/usr/bin/env python3
"""
Initialize a new Next.js project with TypeScript, Tailwind CSS, and shadcn/ui.
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


def create_nextjs_project(project_name: str, use_typescript: bool = True, use_app_router: bool = True):
    """Create a new Next.js project."""
    print(f"\n🚀 Creating Next.js project: {project_name}\n")
    
    # Create Next.js project with options
    flags = []
    if use_typescript:
        flags.append("--typescript")
    else:
        flags.append("--js")
    
    flags.append("--tailwind")
    flags.append("--eslint")
    
    if use_app_router:
        flags.append("--app")
    else:
        flags.append("--no-app")
    
    flags.append("--src-dir")
    flags.append("--import-alias '@/*'")
    
    command = f"npx create-next-app@latest {project_name} {' '.join(flags)} --no-git"
    
    if not run_command(command):
        return False
    
    return Path(project_name)


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
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/app/globals.css",
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
    
    return True


def install_additional_packages(project_path: Path):
    """Install additional useful packages."""
    print("\n📦 Installing additional packages...\n")
    
    packages = [
        "@tanstack/react-query@^5.90.5",
        "axios@^1.12.2",
        "zustand@^5.0.8",
        "next-themes@^0.4.4"
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
        "src/lib",
        "src/hooks",
        "src/types",
        "src/utils",
        "src/services",
        "src/store",
    ]
    
    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")
    
    return True


def create_env_file(project_path: Path):
    """Create .env.local file."""
    env_content = """# Database
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

# NextAuth.js
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-secret-key-here"

# OAuth Providers (optional)
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""

# App
NEXT_PUBLIC_APP_URL="http://localhost:3000"
"""
    
    env_file = project_path / ".env.local"
    env_file.write_text(env_content)
    print("✓ Created .env.local")
    
    return True


def create_readme(project_path: Path, project_name: str):
    """Create README.md."""
    readme = f"""# {project_name}

A Next.js application built with TypeScript, Tailwind CSS, and shadcn/ui.

## Features

- ⚡️ Next.js 16 - React framework with App Router
- ⚛️ React 19 - Latest React version
- 🎨 Tailwind CSS - Utility-first CSS framework
- 🧩 shadcn/ui - Beautiful UI components
- 📝 TypeScript - Type safety
- 🔍 TanStack Query - Data fetching and caching
- 🐻 Zustand - State management
- 📡 Axios - HTTP client
- 🌙 next-themes - Dark mode support

## Getting Started

### Install dependencies

```bash
npm install
```

### Run development server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for production

```bash
npm run build
npm start
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
├── app/                 # Next.js App Router
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page
│   └── globals.css      # Global styles
├── components/
│   ├── ui/              # shadcn/ui components
│   └── layout/          # Layout components
├── lib/                 # Utility functions
├── hooks/               # Custom hooks
├── services/            # API services
├── store/               # State management
├── types/               # TypeScript types
└── utils/               # Helper functions
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Environment Variables

Copy `.env.local` and update with your values:

```bash
cp .env.local .env.local
```

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [TanStack Query](https://tanstack.com/query/)
"""
    
    (project_path / "README.md").write_text(readme)
    print("✓ Created README.md")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Initialize a new Next.js project")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--no-typescript", action="store_true", help="Use JavaScript instead of TypeScript")
    parser.add_argument("--pages-router", action="store_true", help="Use Pages Router instead of App Router")
    parser.add_argument("--skip-shadcn", action="store_true", help="Skip shadcn/ui installation")
    parser.add_argument("--skip-packages", action="store_true", help="Skip additional packages")
    
    args = parser.parse_args()
    
    use_typescript = not args.no_typescript
    use_app_router = not args.pages_router
    
    # Create Next.js project
    project_path = create_nextjs_project(args.project_name, use_typescript, use_app_router)
    if not project_path:
        print("✗ Failed to create Next.js project")
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
    
    # Create .env.local
    create_env_file(project_path)
    
    # Create README
    create_readme(project_path, args.project_name)
    
    print(f"\n✅ Project '{args.project_name}' initialized successfully!\n")
    print("Next steps:")
    print(f"  1. cd {args.project_name}")
    print("  2. npm run dev")
    print("\nTo add shadcn/ui components:")
    print("  npx shadcn@latest add button")
    print("  npx shadcn@latest add card")
    print("\nTo add authentication:")
    print("  python ~/.claude/skills/nextjs-developer/scripts/add_auth.py --provider local")
    print("  python ~/.claude/skills/nextjs-developer/scripts/add_auth.py --provider google")


if __name__ == "__main__":
    main()

