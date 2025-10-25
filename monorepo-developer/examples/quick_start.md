# Quick Start Guide

## 1. Create a New Monorepo

```bash
python scripts/init_project.py my-app
cd my-app
```

This creates:
- ✅ Bun workspace configuration
- ✅ Backend package with Hono
- ✅ Frontend package with React + shadcn/ui
- ✅ Shared package for types and utilities
- ✅ All dependencies installed

## 2. Start Development

```bash
bun run dev
```

Open your browser:
- Frontend: http://localhost:5173
- Backend: http://localhost:3000

## 3. Explore the Structure

```
my-app/
├── packages/
│   ├── backend/          # Hono API server
│   │   └── src/
│   │       ├── routes/   # API routes
│   │       └── index.ts  # Main server file
│   ├── frontend/         # React app
│   │   └── src/
│   │       ├── components/
│   │       ├── pages/
│   │       └── App.tsx
│   └── shared/           # Shared types
│       └── src/
│           ├── types/
│           └── utils/
├── bun.lockb             # Bun lock file
└── package.json          # Root config
```

## 4. Add Backend Routes

Edit `packages/backend/src/index.ts`:

```typescript
import { Hono } from 'hono'
import { cors } from 'hono/cors'

const app = new Hono()

// Enable CORS
app.use('*', cors())

// Health check
app.get('/health', (c) => {
  return c.json({ status: 'ok' })
})

// API routes
app.get('/api/users', (c) => {
  return c.json([
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' }
  ])
})

app.post('/api/users', async (c) => {
  const body = await c.req.json()
  return c.json({ created: true, user: body })
})

export default {
  port: 3000,
  fetch: app.fetch,
}
```

## 5. Add Frontend Components

Add shadcn/ui components:

```bash
cd packages/frontend
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
```

Or use the script:

```bash
python scripts/add_component.py --preset forms
```

## 6. Create a React Component

Create `packages/frontend/src/components/UserList.tsx`:

```typescript
import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

type User = {
  id: number
  name: string
}

export function UserList() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://localhost:3000/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data)
        setLoading(false)
      })
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <Card>
      <CardHeader>
        <CardTitle>Users</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {users.map(user => (
            <li key={user.id} className="flex justify-between items-center">
              <span>{user.name}</span>
              <Button size="sm">Edit</Button>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}
```

## 7. Use Component in App

Edit `packages/frontend/src/App.tsx`:

```typescript
import { UserList } from '@/components/UserList'

function App() {
  return (
    <div className='min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-8'>
      <div className='max-w-4xl mx-auto'>
        <h1 className='text-4xl font-bold text-white mb-8'>My App</h1>
        <UserList />
      </div>
    </div>
  )
}

export default App
```

## 8. Generate New Packages

### Backend Service

```bash
python scripts/generate_package.py auth-service --type backend
cd packages/auth-service
bun run dev
```

### Frontend App

```bash
python scripts/generate_package.py admin-panel --type frontend
cd packages/admin-panel
bun run dev
```

### Shared Library

```bash
python scripts/generate_package.py common --type library
```

## 9. Build for Production

```bash
# Build all packages
bun run build

# Build specific package
cd packages/backend
bun run build

cd packages/frontend
bun run build
```

## 10. Deploy

### Backend (Hono)

```bash
# Build
bun build packages/backend/src/index.ts --outdir dist

# Run
bun dist/index.js
```

### Frontend (React)

```bash
# Build
cd packages/frontend
bun run build

# Serve dist/ folder with any static server
```

## Common Commands

```bash
# Install dependencies
bun install

# Add package to specific workspace
cd packages/backend
bun add hono

# Run development
bun run dev

# Build all
bun run build

# Start production
bun run start

# Run tests
bun test

# Format code
bun run format

# Lint code
bun run lint
```

## Tips & Tricks

### 1. Use TypeScript Strict Mode

Enable in `tsconfig.json`:
```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

### 2. Share Types Between Packages

In `packages/shared/src/types/index.ts`:
```typescript
export type User = {
  id: number
  name: string
  email: string
}
```

Import in other packages:
```typescript
import type { User } from '@monorepo/shared'
```

### 3. Use Environment Variables

Create `.env` file:
```
VITE_API_URL=http://localhost:3000
```

Access in frontend:
```typescript
const apiUrl = import.meta.env.VITE_API_URL
```

### 4. Add Middleware to Hono

```typescript
import { logger } from 'hono/logger'
import { cors } from 'hono/cors'

app.use('*', logger())
app.use('*', cors())
```

### 5. Use React Query for Data Fetching

```typescript
import { useQuery } from '@tanstack/react-query'

function Users() {
  const { data, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json())
  })

  if (isLoading) return <div>Loading...</div>
  return <div>{JSON.stringify(data)}</div>
}
```

## Troubleshooting

### Port Already in Use

```bash
# Find process on port 3000
lsof -i :3000

# Kill process
kill -9 <PID>
```

### Dependencies Not Installing

```bash
# Clear cache
bun install --force

# Reinstall
rm -rf node_modules bun.lockb
bun install
```

### TypeScript Errors

```bash
# Check TypeScript
bun run tsc --noEmit

# Fix issues
bun run tsc --noEmit --pretty
```

## Next Steps

1. ✅ Create monorepo
2. ✅ Add backend routes
3. ✅ Create frontend components
4. ✅ Connect frontend to backend
5. 📝 Add database (Drizzle ORM)
6. 📝 Add authentication
7. 📝 Deploy to production

Happy coding! 🚀

