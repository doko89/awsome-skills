# React Developer Skill

A comprehensive skill for building modern React applications with Vite, TypeScript, Tailwind CSS, and shadcn/ui.

## Features

- ⚡️ **Vite** - Lightning fast build tool
- ⚛️ **React 19** - Latest React version
- 🎨 **Tailwind CSS** - Utility-first CSS framework
- 🧩 **shadcn/ui** - Beautiful, accessible UI components
- 📝 **TypeScript** - Type safety and better DX
- 🔄 **React Router** - Client-side routing
- 🔍 **TanStack Query** - Powerful data fetching
- 🐻 **Zustand** - Simple state management
- 📡 **Axios** - HTTP client

## Quick Start

### 1. Initialize a New Project

```bash
python scripts/init_project.py my-app
cd my-app
npm run dev
```

### 2. Add shadcn/ui Components

```bash
# Add essential components
python scripts/add_component.py --essential

# Add specific components
python scripts/add_component.py button card dialog

# Add form components
python scripts/add_component.py --preset forms
```

### 3. Generate Pages

```bash
# Basic page
python scripts/generate_page.py about

# Page with data fetching
python scripts/generate_page.py users --type=data

# Page with form
python scripts/generate_page.py contact --type=form
```

### 4. Generate Components

```bash
# Basic component
python scripts/generate_component.py UserCard

# Form component
python scripts/generate_component.py LoginForm --type=form

# List component
python scripts/generate_component.py UserList --type=list
```

### 5. Generate Custom Hooks

```bash
# Data fetching hook
python scripts/generate_hook.py useFetchUsers --type=fetch

# LocalStorage hook
python scripts/generate_hook.py useLocalStorage --type=local-storage

# Toggle hook
python scripts/generate_hook.py useToggle --type=toggle
```

## Scripts

### init_project.py

Initialize a new React project with all dependencies.

```bash
python scripts/init_project.py <project-name> [options]
```

**Options:**
- `--no-typescript` - Use JavaScript instead of TypeScript
- `--skip-shadcn` - Skip shadcn/ui installation
- `--skip-packages` - Skip additional packages

**Example:**
```bash
python scripts/init_project.py my-app
```

### add_component.py

Add shadcn/ui components to your project.

```bash
python scripts/add_component.py [components...] [options]
```

**Options:**
- `--list` - List all available components
- `--preset <name>` - Add preset group
- `--registry <url>` - Add from custom registry
- `--essential` - Add essential components

**Preset Groups:**
- `forms` - Form-related components
- `data` - Data display components
- `overlay` - Modal and overlay components
- `navigation` - Navigation components
- `feedback` - Feedback components
- `layout` - Layout components
- `essential` - Essential components

**Examples:**
```bash
python scripts/add_component.py button card
python scripts/add_component.py --preset forms
python scripts/add_component.py --essential
python scripts/add_component.py --registry https://www.shadcn.io/registry/ai.json
```

### generate_page.py

Generate a new page component.

```bash
python scripts/generate_page.py <name> [options]
```

**Options:**
- `--type <type>` - Page type: basic, data, form
- `--with-layout` - Include card layout

**Examples:**
```bash
python scripts/generate_page.py about
python scripts/generate_page.py users --type=data
python scripts/generate_page.py contact --type=form
```

### generate_component.py

Generate a new React component.

```bash
python scripts/generate_component.py <name> [options]
```

**Options:**
- `--type <type>` - Component type: basic, children, state, form, card, list
- `--dir <directory>` - Directory relative to src/

**Examples:**
```bash
python scripts/generate_component.py UserCard
python scripts/generate_component.py LoginForm --type=form
python scripts/generate_component.py Header --dir=components/layout
```

### generate_hook.py

Generate a custom React hook.

```bash
python scripts/generate_hook.py <name> [options]
```

**Options:**
- `--type <type>` - Hook type: basic, fetch, local-storage, debounce, media-query, toggle

**Examples:**
```bash
python scripts/generate_hook.py useFetchData --type=fetch
python scripts/generate_hook.py useLocalStorage --type=local-storage
python scripts/generate_hook.py useDebounce --type=debounce
```

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

## Tech Stack

- **React 19.2.0** - UI library
- **Vite 7.1.12** - Build tool
- **TypeScript 5.9.3** - Type safety
- **Tailwind CSS 4.1.16** - Styling
- **shadcn/ui** - UI components
- **React Router 7.9.4** - Routing
- **TanStack Query 5.90.5** - Data fetching
- **Zustand 5.0.8** - State management
- **Axios 1.12.2** - HTTP client

## Best Practices

1. **Use TypeScript** - Type safety prevents bugs
2. **Component Composition** - Build complex UIs from simple components
3. **Custom Hooks** - Extract reusable logic
4. **shadcn/ui** - Use for consistent, accessible UI
5. **TanStack Query** - Manage server state
6. **Zustand** - Manage client state
7. **Code Splitting** - Use React.lazy() for better performance
8. **Error Boundaries** - Handle errors gracefully

## Examples

### Complete Application

```bash
# Initialize project
python scripts/init_project.py blog-app
cd blog-app

# Add components
python scripts/add_component.py --essential

# Generate pages
python scripts/generate_page.py home
python scripts/generate_page.py posts --type=data
python scripts/generate_page.py create-post --type=form

# Generate components
python scripts/generate_component.py PostCard --type=card
python scripts/generate_component.py PostList --type=list

# Generate hooks
python scripts/generate_hook.py useFetchPosts --type=fetch

# Run development server
npm run dev
```

## Customization

### Tailwind Configuration

Edit `tailwind.config.js`:

```js
export default {
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#8b5cf6',
      },
    },
  },
}
```

### shadcn/ui Theme

Edit `components.json`:

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

Run manual initialization:

```bash
npx shadcn@latest init
```

### Path Aliases Not Working

Check `tsconfig.json` and `vite.config.ts` for correct path aliases.

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
- [Zustand Documentation](https://zustand-demo.pmnd.rs/)

## License

MIT License - see LICENSE file for details

