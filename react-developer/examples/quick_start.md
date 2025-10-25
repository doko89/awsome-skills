# Quick Start Guide

Get started with React Developer skill in 5 minutes!

## 1. Create a New Project

```bash
python scripts/init_project.py my-app
cd my-app
```

This creates a complete React project with:
- Vite + React + TypeScript
- Tailwind CSS
- shadcn/ui
- React Router, TanStack Query, Zustand, Axios

## 2. Start Development Server

```bash
npm run dev
```

Open http://localhost:5173 in your browser.

## 3. Add UI Components

```bash
# Add essential components
python ../scripts/add_component.py --essential

# Or add specific components
python ../scripts/add_component.py button card dialog input
```

## 4. Generate a Page

```bash
# Basic page
python ../scripts/generate_page.py home

# Page with data fetching
python ../scripts/generate_page.py users --type=data

# Page with form
python ../scripts/generate_page.py contact --type=form
```

## 5. Generate Components

```bash
# Card component
python ../scripts/generate_component.py UserCard --type=card

# Form component
python ../scripts/generate_component.py LoginForm --type=form

# List component
python ../scripts/generate_component.py UserList --type=list
```

## 6. Generate Custom Hooks

```bash
# Data fetching hook
python ../scripts/generate_hook.py useFetchUsers --type=fetch

# LocalStorage hook
python ../scripts/generate_hook.py useLocalStorage --type=local-storage
```

## 7. Set Up Routing

Edit `src/App.tsx`:

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from '@/pages/HomePage'
import UsersPage from '@/pages/UsersPage'
import ContactPage from '@/pages/ContactPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/contact" element={<ContactPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

## 8. Add TanStack Query Provider

Edit `src/main.tsx`:

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App.tsx'
import './index.css'

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
)
```

## 9. Build for Production

```bash
npm run build
npm run preview
```

## Next Steps

- Read [React Best Practices](../references/react_best_practices.md)
- Check out [Complete Example](./complete_example.md)
- Explore [shadcn/ui Documentation](https://ui.shadcn.com/)
- Learn [TanStack Query](https://tanstack.com/query/)

## Common Commands

```bash
# Development
npm run dev

# Build
npm run build

# Preview production build
npm run preview

# Lint
npm run lint

# Add shadcn/ui component
npx shadcn@latest add <component-name>

# Generate page
python ../scripts/generate_page.py <name> [--type=basic|data|form]

# Generate component
python ../scripts/generate_component.py <name> [--type=basic|children|state|form|card|list]

# Generate hook
python ../scripts/generate_hook.py <name> [--type=basic|fetch|local-storage|debounce|media-query|toggle]
```

## Tips

1. **Use TypeScript** - It catches errors early
2. **Use shadcn/ui** - Beautiful, accessible components
3. **Use TanStack Query** - For server state management
4. **Use Zustand** - For client state management
5. **Keep components small** - Easier to maintain
6. **Extract custom hooks** - Reuse logic across components
7. **Use code splitting** - Better performance

## Troubleshooting

### Port already in use

```bash
# Kill process on port 5173
npx kill-port 5173

# Or use different port
npm run dev -- --port 3000
```

### Module not found

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript errors

```bash
# Check TypeScript config
cat tsconfig.json

# Make sure path aliases are correct
```

## Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [shadcn/ui Documentation](https://ui.shadcn.com/)

