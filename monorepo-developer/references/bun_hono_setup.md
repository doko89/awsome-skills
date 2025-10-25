# Bun + Hono Setup Guide

## What is Bun?

Bun is a fast JavaScript runtime and package manager built with Zig. It's designed to be a drop-in replacement for Node.js with better performance.

### Key Features

- **Fast** - 3-4x faster than Node.js
- **Built-in TypeScript** - No need for ts-node
- **Package Manager** - Faster than npm/yarn
- **Bundler** - Built-in bundler for production builds
- **Test Runner** - Built-in test framework

## What is Hono?

Hono is a small, simple, and ultrafast web framework for the edge. It works on any JavaScript runtime (Node.js, Bun, Deno, Cloudflare Workers, etc.).

### Key Features

- **Lightweight** - Only 13KB gzipped
- **Fast** - Optimized for performance
- **Type-safe** - Full TypeScript support
- **Middleware** - Powerful middleware system
- **Routing** - Flexible routing with parameters

## Bun Workspace Setup

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
    "start": "bun run --cwd packages/backend start"
  }
}
```

### Installing Dependencies

```bash
# Install all dependencies in all packages
bun install

# Install in specific package
cd packages/backend
bun install

# Add dependency to specific package
bun add hono
```

## Hono Backend Setup

### Basic Hono Server

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => {
  return c.json({ message: 'Hello from Hono!' })
})

app.get('/api/users', (c) => {
  return c.json([
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' }
  ])
})

export default {
  port: 3000,
  fetch: app.fetch,
}
```

### Running with Bun

```bash
# Development with watch mode
bun run --watch src/index.ts

# Production build
bun build src/index.ts --outdir dist

# Run production build
bun dist/index.js
```

## Middleware in Hono

### CORS Middleware

```typescript
import { Hono } from 'hono'
import { cors } from 'hono/cors'

const app = new Hono()

app.use('*', cors())

app.get('/', (c) => {
  return c.json({ message: 'Hello' })
})
```

### Logger Middleware

```typescript
import { Hono } from 'hono'
import { logger } from 'hono/logger'

const app = new Hono()

app.use('*', logger())

app.get('/', (c) => {
  return c.json({ message: 'Hello' })
})
```

### Custom Middleware

```typescript
const customMiddleware = async (c, next) => {
  console.log(`${c.req.method} ${c.req.url}`)
  await next()
}

app.use('*', customMiddleware)
```

## Routing in Hono

### Basic Routes

```typescript
// GET
app.get('/users', (c) => {
  return c.json({ users: [] })
})

// POST
app.post('/users', (c) => {
  return c.json({ created: true })
})

// PUT
app.put('/users/:id', (c) => {
  const id = c.req.param('id')
  return c.json({ updated: true, id })
})

// DELETE
app.delete('/users/:id', (c) => {
  const id = c.req.param('id')
  return c.json({ deleted: true, id })
})
```

### Route Groups

```typescript
const api = new Hono()

api.get('/users', (c) => c.json({ users: [] }))
api.post('/users', (c) => c.json({ created: true }))

const app = new Hono()
app.route('/api', api)
```

## Environment Variables

### .env file

```
DATABASE_URL=postgresql://user:password@localhost/db
API_PORT=3000
NODE_ENV=development
```

### Accessing in Code

```typescript
const dbUrl = process.env.DATABASE_URL
const port = process.env.API_PORT || 3000
```

## Type Safety with TypeScript

### Request/Response Types

```typescript
type User = {
  id: number
  name: string
  email: string
}

app.get('/users/:id', (c) => {
  const id = c.req.param('id')
  const user: User = {
    id: parseInt(id),
    name: 'John',
    email: 'john@example.com'
  }
  return c.json(user)
})
```

### Request Body Validation

```typescript
app.post('/users', async (c) => {
  const body = await c.req.json()
  
  // Validate
  if (!body.name || !body.email) {
    return c.json({ error: 'Missing fields' }, 400)
  }
  
  return c.json({ created: true })
})
```

## Performance Tips

1. **Use Bun's built-in features** - Leverage Bun's speed
2. **Minimize middleware** - Only use necessary middleware
3. **Cache responses** - Use HTTP caching headers
4. **Optimize database queries** - Use indexes and connection pooling
5. **Use TypeScript** - Catch errors at compile time

## Deployment

### Build for Production

```bash
bun build src/index.ts --outdir dist
```

### Run in Production

```bash
bun dist/index.js
```

### Docker

```dockerfile
FROM oven/bun:latest

WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install --production

COPY src ./src

EXPOSE 3000

CMD ["bun", "src/index.ts"]
```

