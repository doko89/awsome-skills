---
name: monorepo-developer
description: A comprehensive skill for building modern monorepo applications using Bun, Hono backend, React frontend with shadcn/ui, TypeScript, and Tailwind CSS. Includes project initialization, package generation, and component management scripts.
version: 1.0.0
author: Augment Skills
tags:
  - monorepo
  - bun
  - hono
  - react
  - typescript
  - tailwindcss
  - shadcn-ui
  - fullstack
  - web-development
license: MIT
metadata:
  bun_version: "1.0+"
  hono_version: "4.10.3"
  react_version: "19.2.0"
  tailwindcss_version: "4.1.16"
---

# Monorepo Developer Skill

A comprehensive skill for building modern fullstack monorepo applications using Bun, Hono backend, React frontend with shadcn/ui, TypeScript, and Tailwind CSS.

## Overview

This skill provides a complete toolkit for monorepo development, including:

- **Project Initialization** - Create new monorepo with Bun workspace, Hono backend, and React frontend
- **Package Generation** - Generate new packages (backend services, frontend apps, shared libraries)
- **shadcn/ui Integration** - Automatic setup and component management for React packages
- **Code Generation** - Generate API routes, React components, and custom hooks
- **Best Practices** - Modern fullstack patterns with TypeScript and clean architecture
- **Developer Experience** - Fast development with Bun and hot reload

## Tech Stack

- **Bun 1.0+** - Fast JavaScript runtime and package manager
- **Hono 4.10.3** - Lightweight web framework for backend
- **React 19.2.0** - Latest React version for frontend
- **TypeScript 5.9.3** - Type safety across the stack
- **Tailwind CSS 4.1.16** - Utility-first CSS framework
- **shadcn/ui** - Beautiful UI components for React
- **Vite 7.1.12** - Fast build tool for frontend
- **Drizzle ORM** - Type-safe database ORM

## Project Structure

```
my-monorepo/
├── packages/
│   ├── backend/
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   ├── middleware/
│   │   │   ├── services/
│   │   │   ├── db/
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   ├── lib/
│   │   │   └── App.tsx
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── shared/
│       ├── src/
│       │   ├── types/
│       │   └── utils/
│       └── package.json
├── bun.lockb
├── bunfig.toml
└── package.json
```

## Scripts

### 1. Initialize Project

Create a new monorepo with Bun, Hono backend, and React frontend:

```bash
python scripts/init_project.py <project-name> [options]
```

**Options:**
- `--skip-git` - Skip git initialization
- `--skip-install` - Skip dependency installation

**Example:**
```bash
python scripts/init_project.py my-monorepo
```

This creates:
- Bun workspace configuration
- Backend package with Hono
- Frontend package with React + shadcn/ui
- Shared package for types and utilities
- TypeScript configuration
- Development scripts

### 2. Generate Package

Generate a new package in the monorepo:

```bash
python scripts/generate_package.py <package-name> [--type <type>] [--project-path <path>]
```

**Package Types:**
- `backend` - Hono backend service
- `frontend` - React frontend application
- `library` - Shared library package

**Example:**
```bash
python scripts/generate_package.py api-service --type backend
python scripts/generate_package.py admin-panel --type frontend
python scripts/generate_package.py utils --type library
```

### 3. Add shadcn/ui Components

Add shadcn/ui components to frontend packages:

```bash
python scripts/add_component.py [components...] [--package <name>] [--project-path <path>]
```

**Example:**
```bash
python scripts/add_component.py button card dialog --package frontend
```

### 4. Generate React Components

Generate new React components with various templates:

```bash
python scripts/generate_component.py <component-name> [--type <type>] [--directory <dir>] [--package <name>]
```

**Component Types:**
- `basic` - Basic component with props interface
- `children` - Component with children prop
- `state` - Component with useState hook
- `form` - Form component with validation
- `card` - Card component with shadcn/ui
- `list` - List component with rendering
- `modal` - Modal/Dialog component

**Example:**
```bash
python scripts/generate_component.py UserCard --type card --package frontend
python scripts/generate_component.py LoginForm --type form --package frontend
python scripts/generate_component.py UserList --type list --directory features/users
```

### 5. Generate Custom Hooks

Generate custom React hooks:

```bash
python scripts/generate_hook.py <hook-name> [--type <type>] [--package <name>]
```

**Hook Types:**
- `basic` - Basic hook template
- `fetch` - Data fetching hook
- `local-storage` - localStorage hook
- `debounce` - Debounce hook
- `throttle` - Throttle hook
- `toggle` - Toggle boolean state
- `previous` - usePrevious hook
- `async` - Async operation hook

**Example:**
```bash
python scripts/generate_hook.py useUserData --type fetch --package frontend
python scripts/generate_hook.py useLocalStorage --type local-storage
python scripts/generate_hook.py useDebounce --type debounce
```

### 6. Generate Pages

Generate new React pages:

```bash
python scripts/generate_page.py <page-name> [--type <type>] [--package <name>]
```

**Page Types:**
- `basic` - Basic page template
- `list` - List page with search and filtering
- `detail` - Detail page with back button
- `form` - Form page with submission
- `dashboard` - Dashboard with stats cards

**Example:**
```bash
python scripts/generate_page.py Dashboard --type dashboard --package frontend
python scripts/generate_page.py UserList --type list --package frontend
python scripts/generate_page.py UserDetail --type detail --package frontend
```

### 7. Generate API Documentation

Generate API documentation for backend services:

```bash
python scripts/generate_docs.py <api-name> [--type <type>] [--package <name>]
```

**Documentation Types:**
- `markdown` - Markdown API documentation
- `openapi` - OpenAPI/Swagger specification

**Example:**
```bash
python scripts/generate_docs.py UserAPI --type markdown
python scripts/generate_docs.py ProductAPI --type openapi
```

### 8. Add Authentication

Add authentication to backend packages:

```bash
python scripts/add_auth.py [--type <type>] [--package <name>]
```

**Authentication Types:**
- `local` - Local email/password authentication
- `google` - Google OAuth authentication
- `both` - Local + Google authentication

**Features:**
- JWT token generation and verification
- Auth middleware for route protection
- User schema with `avatar_url` field
- Environment variables configuration

**Example:**
```bash
python scripts/add_auth.py --type local
python scripts/add_auth.py --type google
python scripts/add_auth.py --type both
```

### 9. Add Avatar Upload

Add avatar upload functionality:

```bash
python scripts/add_avatar.py [--type <type>] [--package <name>]
```

**Features:**
- Multipart file upload endpoint (`/avatar`)
- File validation (type, size)
- `avatar_url` field in user schema
- Google avatar URL support
- Client-side upload component
- Delete and update avatar endpoints

**Endpoints:**
- `POST /avatar` - Upload avatar
- `GET /avatar/:filename` - Get avatar
- `PUT /avatar` - Update avatar
- `DELETE /avatar` - Delete avatar

**Example:**
```bash
python scripts/add_avatar.py --type backend
python scripts/add_avatar.py --type frontend
```

### 10. Validate Skill

Validate the skill structure and files:

```bash
python scripts/validate_skill.py
```

## Usage Guidelines

### Starting a New Monorepo

```bash
# Initialize project
python scripts/init_project.py my-app

# Navigate to project
cd my-app

# Start development
bun run dev
```

### Adding New Packages

```bash
# Generate backend service
python scripts/generate_package.py auth-service --type backend

# Generate frontend app
python scripts/generate_package.py dashboard --type frontend

# Generate shared library
python scripts/generate_package.py common --type library
```

### Development Workflow

1. **Initialize monorepo** with `init_project.py`
2. **Generate packages** as needed with `generate_package.py`
3. **Add components** to frontend with `add_component.py`
4. **Run development** with `bun run dev`
5. **Build for production** with `bun run build`

## Best Practices

1. **Shared Code** - Use `packages/shared` for types and utilities
2. **Backend** - Keep Hono routes organized by domain
3. **Frontend** - Follow React component patterns with shadcn/ui
4. **TypeScript** - Enable strict mode for type safety
5. **Dependencies** - Use Bun workspace for dependency management

## Troubleshooting

### Bun not found
Install Bun: `curl -fsSL https://bun.sh/install | bash`

### Port already in use
Change port in backend configuration or kill existing process

### Module not found
Ensure all packages are properly installed: `bun install`

