# Monorepo Developer Skill

A comprehensive skill for building modern fullstack monorepo applications using Bun, Hono backend, React frontend with shadcn/ui, TypeScript, and Tailwind CSS.

## Features

- 🚀 **Bun** - Fast JavaScript runtime and package manager
- 🔧 **Hono** - Lightweight web framework for backend
- ⚛️ **React 19** - Latest React version
- 🎨 **Tailwind CSS** - Utility-first CSS framework
- 🧩 **shadcn/ui** - Beautiful UI components
- 📝 **TypeScript** - Type safety across the stack
- 📦 **Monorepo** - Organized package structure with Bun workspaces
- ⚡️ **Vite** - Fast build tool for frontend

## Quick Start

### 1. Initialize a New Monorepo

```bash
python ~/.claude/skills/monorepo-developer/scripts/init_project.py my-monorepo
cd my-monorepo
```

This creates:
- Bun workspace configuration
- Backend package with Hono
- Frontend package with React + shadcn/ui
- Shared package for types and utilities

### 2. Start Development

```bash
bun run dev
```

- Backend: http://localhost:3000
- Frontend: http://localhost:5173

### 3. Generate New Packages

```bash
# Generate backend service
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py api-service --type backend

# Generate frontend app
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py admin-panel --type frontend

# Generate shared library
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py utils --type library
```

### 4. Add shadcn/ui Components

```bash
cd packages/frontend
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
```

Or use the script:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_component.py button card dialog --package frontend
python ~/.claude/skills/monorepo-developer/scripts/add_component.py --preset forms --package frontend
```

## Project Structure

```
my-monorepo/
├── packages/
│   ├── backend/
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   ├── middleware/
│   │   │   ├── services/
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
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

### init_project.py

Initialize a new monorepo project:

```bash
python ~/.claude/skills/monorepo-developer/scripts/init_project.py <project-name> [options]
```

**Options:**
- `--skip-git` - Skip git initialization
- `--skip-install` - Skip dependency installation

### generate_package.py

Generate a new package in the monorepo:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_package.py <package-name> --type <type> [--project-path <path>]
```

**Package Types:**
- `backend` - Hono backend service
- `frontend` - React frontend application
- `library` - Shared library package

### add_component.py

Add shadcn/ui components to frontend packages:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_component.py [components...] [--package <name>] [--project-path <path>]
```

**Examples:**
```bash
python ~/.claude/skills/monorepo-developer/scripts/add_component.py button card dialog
python ~/.claude/skills/monorepo-developer/scripts/add_component.py --preset forms
python ~/.claude/skills/monorepo-developer/scripts/add_component.py --list
```

### generate_component.py

Generate new React components with templates:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py <component-name> [--type <type>] [--directory <dir>] [--package <name>]
```

**Component Types:**
- `basic` - Basic component
- `children` - Component with children
- `state` - Component with useState
- `form` - Form component
- `card` - Card component
- `list` - List component
- `modal` - Modal component

**Examples:**
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserCard --type card
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py LoginForm --type form
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserList --type list
```

### generate_hook.py

Generate custom React hooks:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py <hook-name> [--type <type>] [--package <name>]
```

**Hook Types:**
- `basic` - Basic hook
- `fetch` - Data fetching
- `local-storage` - localStorage
- `debounce` - Debounce
- `throttle` - Throttle
- `toggle` - Toggle state
- `previous` - usePrevious
- `async` - Async operations

**Examples:**
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useUserData --type fetch
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useLocalStorage --type local-storage
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useDebounce --type debounce
```

### generate_page.py

Generate new React pages:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py <page-name> [--type <type>] [--package <name>]
```

**Page Types:**
- `basic` - Basic page
- `list` - List page
- `detail` - Detail page
- `form` - Form page
- `dashboard` - Dashboard

**Examples:**
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py Dashboard --type dashboard
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py UserList --type list
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py UserDetail --type detail
```

### generate_docs.py

Generate API documentation:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_docs.py <api-name> [--type <type>] [--package <name>]
```

**Documentation Types:**
- `markdown` - Markdown documentation
- `openapi` - OpenAPI/Swagger spec

**Examples:**
```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_docs.py UserAPI --type markdown
python ~/.claude/skills/monorepo-developer/scripts/generate_docs.py ProductAPI --type openapi
```

### add_auth.py

Add authentication to backend:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_auth.py [--type <type>] [--package <name>]
```

**Authentication Types:**
- `local` - Email/password auth
- `google` - Google OAuth
- `both` - Local + Google

**Features:**
- JWT token management
- Auth middleware
- User schema with avatar_url
- Environment configuration

**Examples:**
```bash
python ~/.claude/skills/monorepo-developer/scripts/add_auth.py --type local
python ~/.claude/skills/monorepo-developer/scripts/add_auth.py --type google
python ~/.claude/skills/monorepo-developer/scripts/add_auth.py --type both
```

### add_avatar.py

Add avatar upload functionality:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_avatar.py [--type <type>] [--package <name>]
```

**Features:**
- Multipart file upload
- File validation
- avatar_url field
- Google avatar support
- Upload component

**Endpoints:**
- `POST /avatar` - Upload
- `GET /avatar/:filename` - Get
- `PUT /avatar` - Update
- `DELETE /avatar` - Delete

**Examples:**
```bash
python ~/.claude/skills/monorepo-developer/scripts/add_avatar.py --type backend
python ~/.claude/skills/monorepo-developer/scripts/add_avatar.py --type frontend
```

### validate_skill.py

Validate the skill structure:

```bash
python ~/.claude/skills/monorepo-developer/scripts/validate_skill.py
```

## Tech Stack

- **Bun 1.0+** - Fast JavaScript runtime
- **Hono 4.10.3** - Lightweight web framework
- **React 19.2.0** - Latest React version
- **TypeScript 5.9.3** - Type safety
- **Tailwind CSS 4.1.16** - Utility-first CSS
- **shadcn/ui** - Beautiful UI components
- **Vite 7.1.12** - Fast build tool

## Development Workflow

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

Install Bun:
```bash
curl -fsSL https://bun.sh/install | bash
```

### Port already in use

Change port in backend configuration or kill existing process:
```bash
lsof -i :3000  # Find process on port 3000
kill -9 <PID>  # Kill the process
```

### Module not found

Ensure all packages are properly installed:
```bash
bun install
```

## Learn More

- [Bun Documentation](https://bun.sh/docs)
- [Hono Documentation](https://hono.dev)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [shadcn/ui](https://ui.shadcn.com)
- [TypeScript](https://www.typescriptlang.org)

## License

MIT

