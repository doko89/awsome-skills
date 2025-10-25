# Advanced Monorepo Setup

## Multi-Service Architecture

### Generate Multiple Backend Services

```bash
# API Gateway
python scripts/generate_package.py api-gateway --type backend

# User Service
python scripts/generate_package.py user-service --type backend

# Product Service
python scripts/generate_package.py product-service --type backend

# Auth Service
python scripts/generate_package.py auth-service --type backend
```

### Service Communication

`packages/api-gateway/src/index.ts`:

```typescript
import { Hono } from 'hono'
import { cors } from 'hono/cors'

const app = new Hono()

app.use('*', cors())

// Forward requests to services
app.route('/users', userServiceRouter)
app.route('/products', productServiceRouter)
app.route('/auth', authServiceRouter)

// Health check
app.get('/health', (c) => {
  return c.json({ status: 'ok', service: 'api-gateway' })
})

export default {
  port: 3000,
  fetch: app.fetch,
}
```

## Multiple Frontend Applications

### Generate Multiple Frontend Apps

```bash
# Main Dashboard
python scripts/generate_package.py dashboard --type frontend

# Admin Panel
python scripts/generate_package.py admin-panel --type frontend

# Mobile Web
python scripts/generate_package.py mobile-app --type frontend
```

### Shared UI Library

```bash
# Create UI library
python scripts/generate_package.py ui-library --type library
```

`packages/ui-library/src/index.ts`:

```typescript
export { Button } from './components/Button'
export { Card } from './components/Card'
export { Input } from './components/Input'
export { Dialog } from './components/Dialog'

export type { ButtonProps } from './components/Button'
export type { CardProps } from './components/Card'
```

### Using Shared UI Library

`packages/dashboard/src/App.tsx`:

```typescript
import { Button, Card, Input } from '@monorepo/ui-library'

export function App() {
  return (
    <Card>
      <Input placeholder='Search...' />
      <Button>Search</Button>
    </Card>
  )
}
```

## Database Integration

### Drizzle ORM Setup

`packages/backend/src/db/schema.ts`:

```typescript
import { pgTable, serial, text, timestamp, integer } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
})

export const products = pgTable('products', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  price: integer('price').notNull(),
  stock: integer('stock').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
})
```

### Database Queries

`packages/backend/src/services/userService.ts`:

```typescript
import { db } from '../db'
import { users } from '../db/schema'
import { eq } from 'drizzle-orm'

export async function getUsers() {
  return await db.select().from(users)
}

export async function getUserById(id: number) {
  return await db.select().from(users).where(eq(users.id, id))
}

export async function createUser(name: string, email: string) {
  return await db.insert(users).values({ name, email }).returning()
}
```

### API Routes with Database

`packages/backend/src/routes/users.ts`:

```typescript
import { Hono } from 'hono'
import { getUsers, getUserById, createUser } from '../services/userService'

const router = new Hono()

router.get('/', async (c) => {
  const users = await getUsers()
  return c.json(users)
})

router.get('/:id', async (c) => {
  const id = parseInt(c.req.param('id'))
  const user = await getUserById(id)
  return c.json(user[0])
})

router.post('/', async (c) => {
  const { name, email } = await c.req.json()
  const user = await createUser(name, email)
  return c.json(user[0], 201)
})

export default router
```

## Authentication

### JWT Authentication

`packages/auth-service/src/auth.ts`:

```typescript
import { sign, verify } from 'hono/jwt'

const SECRET = process.env.JWT_SECRET || 'your-secret-key'

export async function generateToken(userId: number) {
  return await sign({ userId, exp: Math.floor(Date.now() / 1000) + 60 * 60 }, SECRET)
}

export async function verifyToken(token: string) {
  try {
    return await verify(token, SECRET)
  } catch (error) {
    return null
  }
}
```

### Protected Routes

`packages/backend/src/middleware/auth.ts`:

```typescript
import { verifyToken } from '@monorepo/auth-service'

export async function authMiddleware(c, next) {
  const token = c.req.header('Authorization')?.replace('Bearer ', '')
  
  if (!token) {
    return c.json({ error: 'Unauthorized' }, 401)
  }
  
  const payload = await verifyToken(token)
  if (!payload) {
    return c.json({ error: 'Invalid token' }, 401)
  }
  
  c.set('userId', payload.userId)
  await next()
}
```

## API Client Library

### Create API Client Package

```bash
python scripts/generate_package.py api-client --type library
```

`packages/api-client/src/index.ts`:

```typescript
import axios from 'axios'
import type { User, Product, ApiResponse } from '@monorepo/shared'

const client = axios.create({
  baseURL: process.env.VITE_API_URL || 'http://localhost:3000'
})

export const api = {
  users: {
    getAll: () => client.get<ApiResponse<User[]>>('/api/users'),
    getById: (id: number) => client.get<ApiResponse<User>>(`/api/users/${id}`),
    create: (data: Omit<User, 'id'>) => client.post<ApiResponse<User>>('/api/users', data),
    update: (id: number, data: Partial<User>) => client.put<ApiResponse<User>>(`/api/users/${id}`, data),
    delete: (id: number) => client.delete(`/api/users/${id}`),
  },
  products: {
    getAll: () => client.get<ApiResponse<Product[]>>('/api/products'),
    getById: (id: number) => client.get<ApiResponse<Product>>(`/api/products/${id}`),
    create: (data: Omit<Product, 'id'>) => client.post<ApiResponse<Product>>('/api/products', data),
  }
}
```

### Using API Client in Frontend

`packages/dashboard/src/hooks/useUsers.ts`:

```typescript
import { useQuery } from '@tanstack/react-query'
import { api } from '@monorepo/api-client'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await api.users.getAll()
      return data.data || []
    }
  })
}
```

## Testing Strategy

### Unit Tests

`packages/backend/src/services/__tests__/userService.test.ts`:

```typescript
import { describe, it, expect } from 'bun:test'
import { getUsers, createUser } from '../userService'

describe('User Service', () => {
  it('should get all users', async () => {
    const users = await getUsers()
    expect(Array.isArray(users)).toBe(true)
  })

  it('should create a user', async () => {
    const user = await createUser('John', 'john@example.com')
    expect(user.name).toBe('John')
    expect(user.email).toBe('john@example.com')
  })
})
```

### Integration Tests

`packages/backend/src/__tests__/api.test.ts`:

```typescript
import { describe, it, expect } from 'bun:test'
import app from '../index'

describe('API', () => {
  it('should return users', async () => {
    const response = await app.request('/api/users')
    expect(response.status).toBe(200)
    const data = await response.json()
    expect(Array.isArray(data)).toBe(true)
  })
})
```

## CI/CD Pipeline

### GitHub Actions Workflow

`.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun test
      - run: bun run lint
      - run: bun run build
```

## Monitoring and Logging

### Structured Logging

`packages/backend/src/middleware/logging.ts`:

```typescript
export function loggingMiddleware(c, next) {
  const start = Date.now()
  
  return next().then(() => {
    const duration = Date.now() - start
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      method: c.req.method,
      path: c.req.path,
      status: c.res.status,
      duration: `${duration}ms`
    }))
  })
}
```

## Performance Monitoring

### Request Metrics

```typescript
const metrics = {
  requests: 0,
  errors: 0,
  avgResponseTime: 0
}

app.use('*', async (c, next) => {
  const start = Date.now()
  await next()
  const duration = Date.now() - start
  
  metrics.requests++
  if (c.res.status >= 400) metrics.errors++
  metrics.avgResponseTime = (metrics.avgResponseTime + duration) / 2
})

app.get('/metrics', (c) => {
  return c.json(metrics)
})
```

## Deployment

### Docker Compose

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: packages/backend/Dockerfile
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/myapp
    depends_on:
      - db

  frontend:
    build:
      context: .
      dockerfile: packages/frontend/Dockerfile
    ports:
      - "5173:5173"

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Kubernetes Deployment

`k8s/backend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: myapp/backend:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

