---
name: react-developer
description: A comprehensive skill for building modern React applications with Vite, TypeScript, Tailwind CSS, and shadcn/ui. Includes project initialization, component generation, and best practices.
version: 1.0.0
author: AI Assistant
tags:
  - react
  - typescript
  - vite
  - tailwindcss
  - shadcn-ui
  - frontend
  - web-development
license: MIT
---

# React Developer Skill

A comprehensive skill for building modern React applications with best practices, featuring Vite, TypeScript, Tailwind CSS, and shadcn/ui components.

## Overview

This skill provides a complete toolkit for React development, including:

- **Project Initialization** - Create new React projects with Vite, TypeScript, and Tailwind CSS
- **shadcn/ui Integration** - Automatic setup and component management
- **Code Generation** - Generate pages, components, and custom hooks
- **Best Practices** - Modern React patterns and TypeScript support
- **Developer Experience** - Fast development with Vite and hot reload

## Tech Stack

- **React 19.2.0** - Latest React version
- **Vite 7.1.12** - Fast build tool
- **TypeScript 5.9.3** - Type safety
- **Tailwind CSS 4.1.16** - Utility-first CSS
- **shadcn/ui** - Beautiful UI components
- **React Router 7.9.4** - Client-side routing
- **TanStack Query 5.90.5** - Data fetching and caching
- **Zustand 5.0.8** - State management
- **Axios 1.12.2** - HTTP client

## Project Structure

```
my-app/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   └── layout/          # Layout components
│   ├── pages/               # Page components
│   ├── hooks/               # Custom hooks
│   ├── lib/                 # Utility functions
│   ├── services/            # API services
│   ├── store/               # State management
│   ├── types/               # TypeScript types
│   ├── utils/               # Helper functions
│   ├── App.tsx              # Main app component
│   └── main.tsx             # Entry point
├── public/                  # Static assets
├── components.json          # shadcn/ui config
├── tailwind.config.js       # Tailwind config
├── tsconfig.json            # TypeScript config
├── vite.config.ts           # Vite config
└── package.json             # Dependencies
```

## Scripts

### 1. Initialize Project

Create a new React project with all dependencies:

```bash
python scripts/init_project.py <project-name> [options]
```

**Options:**
- `--no-typescript` - Use JavaScript instead of TypeScript
- `--skip-shadcn` - Skip shadcn/ui installation
- `--skip-packages` - Skip additional packages (router, query, etc.)

**Example:**
```bash
python scripts/init_project.py my-app
```

This creates a complete React project with:
- Vite + React + TypeScript
- Tailwind CSS configured
- shadcn/ui installed and configured
- React Router, TanStack Query, Zustand, Axios
- Project structure with organized directories

### 2. Add shadcn/ui Components

Add shadcn/ui components to your project:

```bash
python scripts/add_component.py [components...] [options]
```

**Options:**
- `--list` - List all available components
- `--preset <name>` - Add preset group (forms, data, overlay, navigation, feedback, layout, essential)
- `--registry <url>` - Add component from custom registry
- `--all-forms` - Add all form components
- `--all-data` - Add all data display components
- `--essential` - Add essential components

**Examples:**
```bash
# Add single component
python scripts/add_component.py button

# Add multiple components
python scripts/add_component.py button card dialog

# Add preset group
python scripts/add_component.py --preset forms

# Add essential components
python scripts/add_component.py --essential

# Add from custom registry
python scripts/add_component.py --registry https://www.shadcn.io/registry/ai.json

# List available components
python scripts/add_component.py --list
```

**Preset Groups:**
- `forms` - button, input, label, select, checkbox, radio-group, switch, textarea, form
- `data` - table, card, badge, avatar, skeleton, pagination
- `overlay` - dialog, alert-dialog, sheet, popover, tooltip, hover-card
- `navigation` - tabs, accordion, dropdown-menu, menubar, navigation-menu, command
- `feedback` - alert, toast, sonner, progress
- `layout` - separator, scroll-area, resizable, aspect-ratio
- `essential` - button, card, input, label, dialog, alert, toast

### 3. Generate Page

Generate a new page component:

```bash
python scripts/generate_page.py <name> [options]
```

**Options:**
- `--type <type>` - Page type: basic, data, form (default: basic)
- `--with-layout` - Include card layout

**Examples:**
```bash
# Basic page
python scripts/generate_page.py about

# Page with data fetching
python scripts/generate_page.py users --type=data

# Page with form
python scripts/generate_page.py contact --type=form

# Page with card layout
python scripts/generate_page.py dashboard --with-layout
```

### 4. Generate Component

Generate a new React component:

```bash
python scripts/generate_component.py <name> [options]
```

**Options:**
- `--type <type>` - Component type: basic, children, state, form, card, list (default: basic)
- `--dir <directory>` - Directory relative to src/ (default: components)

**Examples:**
```bash
# Basic component
python scripts/generate_component.py UserCard

# Component with children
python scripts/generate_component.py Container --type=children

# Component with state
python scripts/generate_component.py Counter --type=state

# Form component
python scripts/generate_component.py LoginForm --type=form

# Card component
python scripts/generate_component.py ProductCard --type=card

# List component
python scripts/generate_component.py UserList --type=list

# Component in custom directory
python scripts/generate_component.py Header --dir=components/layout
```

### 5. Generate Custom Hook

Generate a custom React hook:

```bash
python scripts/generate_hook.py <name> [options]
```

**Options:**
- `--type <type>` - Hook type: basic, fetch, local-storage, debounce, media-query, toggle (default: basic)

**Examples:**
```bash
# Basic hook
python scripts/generate_hook.py useCounter

# Data fetching hook
python scripts/generate_hook.py useFetchData --type=fetch

# LocalStorage hook
python scripts/generate_hook.py useLocalStorage --type=local-storage

# Debounce hook
python scripts/generate_hook.py useDebounce --type=debounce

# Media query hook
python scripts/generate_hook.py useMediaQuery --type=media-query

# Toggle hook
python scripts/generate_hook.py useToggle --type=toggle
```

## Usage Guidelines

### When to Use This Skill

- Building new React applications from scratch
- Creating modern web applications with TypeScript
- Need beautiful, accessible UI components (shadcn/ui)
- Want fast development experience (Vite)
- Building single-page applications (SPA)
- Need data fetching and state management

### Best Practices

1. **TypeScript** - Use TypeScript for type safety
2. **Component Organization** - Keep components small and focused
3. **Custom Hooks** - Extract reusable logic into custom hooks
4. **shadcn/ui** - Use shadcn/ui components for consistent UI
5. **TanStack Query** - Use for server state management
6. **Zustand** - Use for client state management
7. **Code Splitting** - Use React.lazy() for code splitting
8. **Error Boundaries** - Implement error boundaries for error handling

### Project Workflow

1. **Initialize Project**
   ```bash
   python scripts/init_project.py my-app
   cd my-app
   npm run dev
   ```

2. **Add UI Components**
   ```bash
   python scripts/add_component.py --essential
   ```

3. **Generate Pages**
   ```bash
   python scripts/generate_page.py home
   python scripts/generate_page.py users --type=data
   ```

4. **Generate Components**
   ```bash
   python scripts/generate_component.py UserCard --type=card
   python scripts/generate_component.py UserList --type=list
   ```

5. **Generate Hooks**
   ```bash
   python scripts/generate_hook.py useFetchUsers --type=fetch
   ```

## Dependencies

All dependencies are automatically installed during project initialization:

**Production:**
- react@^19.2.0
- react-dom@^19.2.0
- react-router-dom@^7.9.4
- @tanstack/react-query@^5.90.5
- axios@^1.12.2
- zustand@^5.0.8
- class-variance-authority
- clsx
- tailwind-merge

**Development:**
- vite@^7.1.12
- @vitejs/plugin-react@^5.1.0
- typescript@^5.9.3
- tailwindcss@^4.1.16
- autoprefixer
- postcss

## Examples

See the `examples/` directory for:
- Complete application examples
- Component patterns
- Hook patterns
- Best practices

## Customization

### Tailwind Configuration

Edit `tailwind.config.js` to customize your theme:

```js
export default {
  theme: {
    extend: {
      colors: {
        // Add custom colors
      },
    },
  },
}
```

### shadcn/ui Configuration

Edit `components.json` to customize shadcn/ui:

```json
{
  "style": "new-york",
  "tailwind": {
    "baseColor": "zinc"
  }
}
```

## Troubleshooting

### shadcn/ui Installation Fails

If automatic shadcn/ui installation fails, the script will attempt manual setup. You can also run:

```bash
npx shadcn@latest init
```

### Path Aliases Not Working

Make sure `tsconfig.json` and `vite.config.ts` have correct path aliases:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Component Not Found

Make sure you've added the component:

```bash
python scripts/add_component.py <component-name>
```

## Learn More

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [React Router Documentation](https://reactrouter.com/)
- [TanStack Query Documentation](https://tanstack.com/query/)

