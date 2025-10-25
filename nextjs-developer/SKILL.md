---
name: nextjs-developer
description: Next.js development skill with TypeScript, Tailwind CSS, shadcn/ui, and NextAuth.js authentication
version: 1.0.0
author: AI Assistant
tags:
  - nextjs
  - react
  - typescript
  - tailwindcss
  - shadcn
  - nextauth
  - drizzle
  - web-development
license: MIT
---

# Next.js Developer Skill

A comprehensive skill for developing modern web applications using Next.js 16 with App Router, TypeScript, Tailwind CSS, shadcn/ui components, and NextAuth.js authentication with Drizzle ORM.

## Overview

This skill provides automated tools for:
- **Project Initialization** - Create Next.js projects with best practices
- **Component Management** - Add shadcn/ui components easily
- **Page Generation** - Generate pages with different patterns
- **Authentication** - Add NextAuth.js with local/Google/both providers
- **Component Generation** - Create reusable React components
- **Hook Generation** - Generate custom React hooks
- **API Routes** - Create API endpoints

## Tech Stack

### Core Framework
- **Next.js 16.0.0** - React framework with App Router
- **React 19.2.0** - Latest React with Server Components
- **TypeScript 5.9.3** - Type safety

### Styling
- **Tailwind CSS 4.1.16** - Utility-first CSS framework
- **shadcn/ui** - Beautiful, accessible UI components (449+ components)
- **next-themes 0.4.4** - Dark mode support

### Authentication
- **NextAuth.js (beta)** - Authentication for Next.js
- **Drizzle ORM** - TypeScript ORM for database
- **@auth/drizzle-adapter** - Drizzle adapter for NextAuth
- **bcryptjs** - Password hashing

### Data Fetching & State
- **TanStack Query 5.90.5** - Data fetching and caching
- **Axios 1.12.2** - HTTP client
- **Zustand 5.0.8** - State management

## Project Structure

```
my-nextjs-app/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Global styles
│   │   ├── api/                # API routes
│   │   │   └── auth/           # NextAuth routes
│   │   └── auth/               # Auth pages
│   │       └── signin/         # Sign-in page
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   └── layout/             # Layout components
│   ├── db/                     # Database (Drizzle)
│   │   ├── schema.ts           # Database schema
│   │   └── index.ts            # Database client
│   ├── lib/
│   │   ├── utils.ts            # Utility functions
│   │   └── auth.ts             # NextAuth config
│   ├── hooks/                  # Custom hooks
│   ├── services/               # API services
│   ├── store/                  # State management
│   ├── types/                  # TypeScript types
│   ├── utils/                  # Helper functions
│   └── middleware.ts           # Next.js middleware
├── drizzle/                    # Drizzle migrations
├── components.json             # shadcn/ui config
├── drizzle.config.ts           # Drizzle config
├── tailwind.config.ts          # Tailwind config
├── tsconfig.json               # TypeScript config
├── next.config.js              # Next.js config
├── .env.local                  # Environment variables
└── package.json                # Dependencies
```

## Scripts

### 1. Project Initialization (`init_project.py`)

Initialize a new Next.js project with all dependencies configured.

**Usage:**
```bash
python scripts/init_project.py <project-name> [options]
```

**Options:**
- `--no-typescript` - Use JavaScript instead of TypeScript
- `--pages-router` - Use Pages Router instead of App Router
- `--skip-shadcn` - Skip shadcn/ui installation
- `--skip-packages` - Skip additional packages

**Example:**
```bash
# Create new project with all features
python scripts/init_project.py my-app

# Create with Pages Router
python scripts/init_project.py my-app --pages-router

# Create without TypeScript
python scripts/init_project.py my-app --no-typescript
```

**What it does:**
- Creates Next.js project with `create-next-app`
- Installs and configures Tailwind CSS
- Sets up shadcn/ui with components.json
- Installs TanStack Query, Zustand, Axios
- Creates project structure
- Generates .env.local and README.md

---

### 2. Add Authentication (`add_auth.py`)

Add NextAuth.js authentication with Drizzle ORM.

**Usage:**
```bash
python scripts/add_auth.py --provider <local|google|both> [options]
```

**Options:**
- `--provider` - Authentication provider (required)
  - `local` - Email/password authentication
  - `google` - Google OAuth
  - `both` - Both local and Google
- `--project-path` - Path to project root (default: current directory)

**Examples:**
```bash
# Add local authentication
cd my-app
python ../scripts/add_auth.py --provider local

# Add Google OAuth
python ../scripts/add_auth.py --provider google

# Add both local and Google
python ../scripts/add_auth.py --provider both
```

**What it does:**
- Installs NextAuth.js and Drizzle ORM
- Creates database schema (User with avatarUrl, Account, Session, VerificationToken)
- Generates auth configuration in `src/lib/auth.ts`
- Creates API route `/api/auth/[...nextauth]`
- Creates avatar upload API route `/api/avatar`
- Generates middleware for protected routes
- Creates sign-in page
- Configures Drizzle adapter
- Creates uploads directory for avatars
- Saves Google avatar on first sign-in

**After running:**
1. Update `DATABASE_URL` in `.env.local`
2. Run `npx drizzle-kit generate` to generate migrations
3. Run `npx drizzle-kit migrate` to apply migrations
4. For Google OAuth: Add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
5. Generate `NEXTAUTH_SECRET`: `openssl rand -base64 32`
6. Avatar upload endpoint available at `/api/avatar` (POST multipart/form-data)

---

### 3. Add Components (`add_component.py`)

Add shadcn/ui components to your project.

**Usage:**
```bash
python scripts/add_component.py [component-name] [options]
```

**Options:**
- `--list` - List all available components
- `--preset <name>` - Add preset group of components
- `--batch <comp1,comp2,...>` - Add multiple components
- `--registry <url>` - Add from custom registry
- `--project-path` - Path to project root

**Examples:**
```bash
# Add single component
python scripts/add_component.py button

# Add multiple components
python scripts/add_component.py --batch button,card,dialog

# Add preset group
python scripts/add_component.py --preset forms

# Add from custom registry
python scripts/add_component.py --registry https://www.shadcn.io/registry/ai.json

# List all components
python scripts/add_component.py --list
```

**Available Presets:**
- `forms` - button, input, label, textarea, select, checkbox, radio-group, switch, form
- `data` - table, card, badge, avatar, separator, pagination
- `overlay` - dialog, sheet, popover, tooltip, alert-dialog, hover-card
- `navigation` - tabs, accordion, dropdown-menu, menubar, navigation-menu, command
- `feedback` - toast, alert, progress, skeleton, sonner
- `layout` - scroll-area, separator, card
- `essential` - button, card, input, label, dialog, toast

---

### 4. Generate Pages (`generate_page.py`)

Generate Next.js pages with different patterns.

**Usage:**
```bash
python scripts/generate_page.py <page-name> [options]
```

**Options:**
- `--route` - Route path (default: lowercase page-name)
- `--type` - Page type (default: basic)
  - `basic` - Simple page
  - `data` - Page with data fetching (Server Component)
  - `form` - Page with form (Client Component)
  - `protected` - Protected page with auth
  - `api` - API route
- `--project-path` - Path to project root

**Examples:**
```bash
# Generate basic page
python scripts/generate_page.py Dashboard --route dashboard

# Generate page with data fetching
python scripts/generate_page.py Products --type data --route products

# Generate form page
python scripts/generate_page.py Contact --type form --route contact

# Generate protected page
python scripts/generate_page.py Profile --type protected --route profile

# Generate API route
python scripts/generate_page.py users --type api --route users
```

**Page Types:**
- **basic** - Simple page with heading and content
- **data** - Server Component with async data fetching and Suspense
- **form** - Client Component with form handling and validation
- **protected** - Server Component with authentication check
- **api** - API route with GET and POST handlers

---

### 5. Generate Components (`generate_component.py`)

Generate reusable React components.

**Usage:**
```bash
python scripts/generate_component.py <component-name> [options]
```

**Options:**
- `--type` - Component type (default: basic)
  - `basic` - Simple component
  - `children` - Component with children
  - `state` - Component with state
  - `form` - Form component
  - `card` - Card component
  - `list` - List component
- `--client` - Generate as Client Component
- `--project-path` - Path to project root

**Examples:**
```bash
# Generate basic component
python scripts/generate_component.py Header

# Generate component with state (Client Component)
python scripts/generate_component.py Counter --type state

# Generate form component
python scripts/generate_component.py LoginForm --type form

# Generate card component
python scripts/generate_component.py ProductCard --type card
```

---

### 6. Generate Hooks (`generate_hook.py`)

Generate custom React hooks.

**Usage:**
```bash
python scripts/generate_hook.py <hook-name> [options]
```

**Options:**
- `--type` - Hook type (default: basic)
  - `basic` - Simple hook
  - `fetch` - Data fetching hook
  - `local-storage` - LocalStorage hook
  - `debounce` - Debounce hook
  - `media-query` - Media query hook
  - `toggle` - Toggle hook
- `--project-path` - Path to project root

**Examples:**
```bash
# Generate basic hook
python scripts/generate_hook.py useCounter

# Generate fetch hook
python scripts/generate_hook.py useUsers --type fetch

# Generate localStorage hook
python scripts/generate_hook.py useTheme --type local-storage

# Generate debounce hook
python scripts/generate_hook.py useDebounce --type debounce
```

---

### 7. Validate Skill (`validate_skill.py`)

Validate the skill structure and files.

**Usage:**
```bash
python scripts/validate_skill.py
```

## Usage Guidelines

### 1. Starting a New Project

```bash
# Initialize project
python scripts/init_project.py my-app

# Navigate to project
cd my-app

# Add authentication
python ../scripts/add_auth.py --provider both

# Add UI components
python ../scripts/add_component.py --preset essential

# Generate pages
python ../scripts/generate_page.py Dashboard --type protected --route dashboard

# Start development server
npm run dev
```

### 2. Authentication Flow

**Local Authentication:**
1. Add auth: `python ../scripts/add_auth.py --provider local`
2. Setup database and run migrations
3. Create sign-up page or use API to create users
4. Users can sign in at `/auth/signin`

**Google OAuth:**
1. Create Google OAuth credentials
2. Add auth: `python ../scripts/add_auth.py --provider google`
3. Add credentials to `.env.local`
4. Users can sign in with Google at `/auth/signin`

### 3. Protected Routes

Use middleware to protect routes:
```typescript
// src/middleware.ts automatically protects /dashboard routes
// Customize in the middleware file
```

Or check auth in Server Components:
```typescript
import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"

export default async function ProtectedPage() {
  const session = await auth()
  if (!session) redirect("/auth/signin")
  // ... rest of component
}
```

### 4. Database Operations

```typescript
import { db } from "@/db"
import { users } from "@/db/schema"
import { eq } from "drizzle-orm"

// Query users
const allUsers = await db.query.users.findMany()

// Find user by email
const user = await db.query.users.findFirst({
  where: eq(users.email, "user@example.com")
})

// Insert user
await db.insert(users).values({
  email: "new@example.com",
  name: "New User"
})
```

## Dependencies

All dependencies are automatically installed with the latest stable versions:

- next@^16.0.0
- react@^19.2.0
- typescript@^5.9.3
- tailwindcss@^4.1.16
- next-auth@beta
- drizzle-orm@latest
- @auth/drizzle-adapter@latest
- @tanstack/react-query@^5.90.5
- zustand@^5.0.8
- axios@^1.12.2

## Customization

### Tailwind Configuration

Customize colors, fonts, and more in `tailwind.config.ts`:
```typescript
export default {
  theme: {
    extend: {
      colors: {
        // Add custom colors
      }
    }
  }
}
```

### shadcn/ui Configuration

Modify `components.json` to change:
- Style (new-york, default)
- Base color
- CSS variables
- Component aliases

### Authentication

Customize auth in `src/lib/auth.ts`:
- Add more providers
- Modify callbacks
- Change session strategy
- Add custom pages

## Troubleshooting

### Issue: shadcn init fails
**Solution:** Run manual setup or check Node.js version (requires 18+)

### Issue: Database connection error
**Solution:** Verify `DATABASE_URL` in `.env.local` and ensure database is running

### Issue: NextAuth session not working
**Solution:** 
- Check `NEXTAUTH_SECRET` is set
- Verify `NEXTAUTH_URL` matches your domain
- Clear cookies and try again

### Issue: TypeScript errors after adding components
**Solution:** Restart TypeScript server or run `npm run build`

## Examples

See `examples/` directory for:
- Quick start guide
- Authentication examples
- Full application examples

## License

MIT License - See LICENSE file for details

