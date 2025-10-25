# Monorepo Best Practices

## Workspace Structure

### Root package.json

```json
{
  "name": "my-monorepo",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "dev": "bun run --cwd packages/backend dev & bun run --cwd packages/frontend dev",
    "build": "bun run --cwd packages/backend build && bun run --cwd packages/frontend build",
    "start": "bun run --cwd packages/backend start",
    "test": "bun test",
    "lint": "eslint packages/*/src",
    "format": "prettier --write packages/*/src"
  }
}
```

### Package Naming Convention

```
@monorepo/backend      # Backend service
@monorepo/frontend     # Frontend application
@monorepo/shared       # Shared types and utilities
@monorepo/api-client   # API client library
@monorepo/ui           # UI component library
```

## Dependency Management

### Shared Dependencies

Place common dependencies in root `package.json`:

```json
{
  "devDependencies": {
    "typescript": "^5.9.3",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

### Package-Specific Dependencies

Each package has its own `package.json`:

```json
{
  "name": "@monorepo/backend",
  "dependencies": {
    "hono": "^4.10.3"
  },
  "devDependencies": {
    "@types/bun": "latest"
  }
}
```

### Installing Dependencies

```bash
# Install all dependencies
bun install

# Add to specific package
cd packages/backend
bun add hono

# Add dev dependency
bun add -D @types/node

# Remove dependency
bun remove hono
```

## Code Sharing

### Shared Types

Create `packages/shared/src/types/index.ts`:

```typescript
export type User = {
  id: number
  name: string
  email: string
  createdAt: Date
}

export type Product = {
  id: number
  name: string
  price: number
  stock: number
}

export type ApiResponse<T> = {
  success: boolean
  data?: T
  error?: string
}
```

### Using Shared Types

In backend (`packages/backend/src/index.ts`):

```typescript
import type { User, ApiResponse } from '@monorepo/shared'

app.get('/api/users', (c) => {
  const users: User[] = []
  const response: ApiResponse<User[]> = {
    success: true,
    data: users
  }
  return c.json(response)
})
```

In frontend (`packages/frontend/src/services/api.ts`):

```typescript
import type { User, ApiResponse } from '@monorepo/shared'

export async function getUsers(): Promise<User[]> {
  const response = await fetch('/api/users')
  const data: ApiResponse<User[]> = await response.json()
  return data.data || []
}
```

### Shared Utilities

Create `packages/shared/src/utils/index.ts`:

```typescript
export function formatDate(date: Date): string {
  return date.toLocaleDateString('en-US')
}

export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

export function generateId(): string {
  return Math.random().toString(36).substr(2, 9)
}
```

## Development Workflow

### Running Development Servers

```bash
# Run all dev servers
bun run dev

# Run specific package
cd packages/backend
bun run dev

# Run with specific port
PORT=3001 bun run dev
```

### Building Packages

```bash
# Build all
bun run build

# Build specific package
cd packages/backend
bun run build

# Build with watch mode
bun run --watch build
```

### Testing

```bash
# Run all tests
bun test

# Run specific package tests
cd packages/backend
bun test

# Run with coverage
bun test --coverage
```

## Environment Variables

### Root .env

```
# Backend
BACKEND_PORT=3000
DATABASE_URL=postgresql://user:password@localhost/db

# Frontend
VITE_API_URL=http://localhost:3000
VITE_APP_NAME=My App
```

### Package-Specific .env

`packages/backend/.env`:
```
PORT=3000
DATABASE_URL=postgresql://user:password@localhost/db
JWT_SECRET=your-secret-key
```

`packages/frontend/.env`:
```
VITE_API_URL=http://localhost:3000
VITE_APP_NAME=My App
```

### Accessing Environment Variables

Backend (Hono):
```typescript
const port = process.env.PORT || 3000
const dbUrl = process.env.DATABASE_URL
```

Frontend (React):
```typescript
const apiUrl = import.meta.env.VITE_API_URL
const appName = import.meta.env.VITE_APP_NAME
```

## Version Management

### Versioning Strategy

Use semantic versioning for all packages:

```
MAJOR.MINOR.PATCH
1.0.0
```

### Updating Versions

```bash
# Update patch version
bun version patch

# Update minor version
bun version minor

# Update major version
bun version major
```

## Git Workflow

### .gitignore

```
# Dependencies
node_modules/
bun.lockb

# Build
dist/
build/

# IDE
.vscode/
.idea/
*.swp

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

### Commit Messages

```
feat(backend): add user authentication
fix(frontend): resolve button styling issue
docs(shared): update type definitions
refactor(backend): optimize database queries
test(frontend): add component tests
```

## Performance Optimization

### Code Splitting

Frontend (`packages/frontend/src/App.tsx`):

```typescript
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))

export function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Dashboard />
    </Suspense>
  )
}
```

### Lazy Loading Packages

```typescript
// Only load when needed
const api = await import('@monorepo/api-client')
```

## Deployment

### Build Strategy

```bash
# Build all packages
bun run build

# Build specific packages
bun run --cwd packages/backend build
bun run --cwd packages/frontend build
```

### Docker Deployment

`Dockerfile`:
```dockerfile
FROM oven/bun:latest

WORKDIR /app

# Copy workspace files
COPY package.json bun.lockb ./
COPY packages ./packages

# Install dependencies
RUN bun install --production

# Build
RUN bun run build

# Start backend
EXPOSE 3000
CMD ["bun", "packages/backend/dist/index.js"]
```

### Environment-Specific Builds

```bash
# Development
bun run build:dev

# Production
bun run build:prod

# Staging
bun run build:staging
```

## Troubleshooting

### Dependency Conflicts

```bash
# Clear cache and reinstall
rm -rf node_modules bun.lockb
bun install
```

### Module Resolution Issues

Ensure `tsconfig.json` has correct paths:

```json
{
  "compilerOptions": {
    "paths": {
      "@monorepo/*": ["../*/src"]
    }
  }
}
```

### Port Conflicts

```bash
# Find process on port
lsof -i :3000

# Kill process
kill -9 <PID>
```

## Monitoring and Logging

### Structured Logging

Backend:
```typescript
import { logger } from 'hono/logger'

app.use('*', logger())

app.get('/api/users', (c) => {
  console.log('Fetching users...')
  return c.json({ users: [] })
})
```

### Error Tracking

```typescript
app.onError((err, c) => {
  console.error('Error:', err)
  return c.json({ error: 'Internal Server Error' }, 500)
})
```

## Security Best Practices

1. **Environment Variables** - Never commit secrets
2. **CORS** - Configure properly for frontend
3. **Authentication** - Use JWT or sessions
4. **Input Validation** - Validate all inputs
5. **Rate Limiting** - Prevent abuse
6. **HTTPS** - Use in production
7. **Dependencies** - Keep updated

### CORS Configuration

```typescript
import { cors } from 'hono/cors'

app.use('*', cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true
}))
```

