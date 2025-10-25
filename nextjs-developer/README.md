# Next.js Developer Skill

> Automated Next.js development with TypeScript, Tailwind CSS, shadcn/ui, and NextAuth.js

## Quick Start

### 1. Initialize Project

```bash
python ~/.claude/skills/nextjs-developer/scripts/init_project.py my-app
cd my-app
```

### 2. Add Authentication (Optional)

```bash
# Local authentication
python ~/.claude/skills/nextjs-developer/scripts/add_auth.py --provider local

# Google OAuth
python ~/.claude/skills/nextjs-developer/scripts/add_auth.py --provider google

# Both
python ~/.claude/skills/nextjs-developer/scripts/add_auth.py --provider both
```

### 3. Add UI Components

```bash
# Add single component
python ~/.claude/skills/nextjs-developer/scripts/add_component.py button

# Add preset group
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --preset forms

# Add multiple components
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --batch button,card,dialog,input
```

### 4. Generate Pages

```bash
# Basic page
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py Dashboard --route dashboard

# Page with data fetching
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py Products --type data

# Form page
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py Contact --type form

# Protected page (requires auth)
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py Profile --type protected
```

### 5. Start Development

```bash
npm run dev
```

## Scripts Overview

| Script | Purpose | Example |
|--------|---------|---------|
| `init_project.py` | Initialize Next.js project | `python ~/.claude/skills/nextjs-developer/scripts/init_project.py my-app` |
| `add_auth.py` | Add NextAuth.js | `python ~/.claude/skills/nextjs-developer/scripts/add_auth.py --provider local` |
| `add_component.py` | Add shadcn/ui components | `python ~/.claude/skills/nextjs-developer/scripts/add_component.py button` |
| `generate_page.py` | Generate pages | `python ~/.claude/skills/nextjs-developer/scripts/generate_page.py Dashboard` |
| `generate_component.py` | Generate components | `python ~/.claude/skills/nextjs-developer/scripts/generate_component.py Header` |
| `generate_hook.py` | Generate hooks | `python ~/.claude/skills/nextjs-developer/scripts/generate_hook.py useCounter` |
| `validate_skill.py` | Validate skill | `python ~/.claude/skills/nextjs-developer/scripts/validate_skill.py` |

## Tech Stack

- **Next.js 16** - React framework with App Router
- **React 19** - Latest React with Server Components
- **TypeScript 5.9** - Type safety
- **Tailwind CSS 4.1** - Utility-first CSS
- **shadcn/ui** - 449+ beautiful components
- **NextAuth.js** - Authentication
- **Drizzle ORM** - TypeScript ORM
- **TanStack Query** - Data fetching
- **Zustand** - State management

## Component Presets

Quick install component groups:

```bash
# Forms
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --preset forms
# Includes: button, input, label, textarea, select, checkbox, radio-group, switch, form

# Data Display
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --preset data
# Includes: table, card, badge, avatar, separator, pagination

# Overlays
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --preset overlay
# Includes: dialog, sheet, popover, tooltip, alert-dialog, hover-card

# Navigation
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --preset navigation
# Includes: tabs, accordion, dropdown-menu, menubar, navigation-menu, command

# Feedback
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --preset feedback
# Includes: toast, alert, progress, skeleton, sonner

# Essential
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --preset essential
# Includes: button, card, input, label, dialog, toast
```

## Authentication Setup

### Local Authentication

```bash
# 1. Add auth
python ~/.claude/skills/nextjs-developer/scripts/add_auth.py --provider local

# 2. Update .env.local
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
NEXTAUTH_SECRET="your-secret-here"
NEXTAUTH_URL="http://localhost:3000"

# 3. Run migrations
npx drizzle-kit generate
npx drizzle-kit migrate

# 4. Sign in at /auth/signin
```

### Google OAuth

```bash
# 1. Add auth
python ~/.claude/skills/nextjs-developer/scripts/add_auth.py --provider google

# 2. Update .env.local
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
NEXTAUTH_SECRET="your-secret-here"
NEXTAUTH_URL="http://localhost:3000"
GOOGLE_CLIENT_ID="your-client-id"
GOOGLE_CLIENT_SECRET="your-client-secret"

# 3. Run migrations
npx drizzle-kit generate
npx drizzle-kit migrate

# 4. Sign in at /auth/signin
```

## Page Types

### Basic Page
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py About --route about
```
Simple page with heading and content.

### Data Page (Server Component)
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py Products --type data
```
Server Component with async data fetching and Suspense.

### Form Page (Client Component)
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py Contact --type form
```
Client Component with form handling.

### Protected Page
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py Dashboard --type protected
```
Server Component with authentication check.

### API Route
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_page.py users --type api
```
API route with GET and POST handlers.

## Component Types

### Basic Component
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_component.py Header
```

### Component with State
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_component.py Counter --type state
```

### Form Component
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_component.py LoginForm --type form
```

### Card Component
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_component.py ProductCard --type card
```

### List Component
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_component.py UserList --type list
```

## Hook Types

### Basic Hook
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_hook.py useCounter
```

### Fetch Hook
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_hook.py useUsers --type fetch
```

### LocalStorage Hook
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_hook.py useTheme --type local-storage
```

### Debounce Hook
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_hook.py useDebounce --type debounce
```

### Media Query Hook
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_hook.py useMediaQuery --type media-query
```

### Toggle Hook
```bash
python ~/.claude/skills/nextjs-developer/scripts/generate_hook.py useToggle --type toggle
```

## Project Structure

```
my-app/
├── src/
│   ├── app/              # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── api/          # API routes
│   │   └── auth/         # Auth pages
│   ├── components/
│   │   ├── ui/           # shadcn/ui components
│   │   └── layout/       # Layout components
│   ├── db/               # Database (Drizzle)
│   │   ├── schema.ts
│   │   └── index.ts
│   ├── lib/
│   │   ├── utils.ts
│   │   └── auth.ts       # NextAuth config
│   ├── hooks/            # Custom hooks
│   ├── services/         # API services
│   ├── store/            # State management
│   └── middleware.ts     # Route protection
├── drizzle/              # Migrations
├── components.json       # shadcn/ui config
├── drizzle.config.ts     # Drizzle config
└── .env.local            # Environment variables
```

## Environment Variables

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

# NextAuth
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="generate-with-openssl-rand-base64-32"

# OAuth (optional)
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""

# App
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

## Common Commands

```bash
# Development
npm run dev

# Build
npm run build

# Start production
npm start

# Lint
npm run lint

# Add shadcn component
npx shadcn@latest add button

# Generate migration
npx drizzle-kit generate

# Run migration
npx drizzle-kit migrate

# Open Drizzle Studio
npx drizzle-kit studio
```

## Custom Registry

Add components from custom registries:

```bash
# AI components
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --registry https://www.shadcn.io/registry/ai.json

# Your custom registry
python ~/.claude/skills/nextjs-developer/scripts/add_component.py --registry https://your-domain.com/registry.json
```

## Documentation

- [SKILL.md](SKILL.md) - Complete documentation
- [examples/](examples/) - Usage examples
- [references/](references/) - Best practices

## License

MIT

