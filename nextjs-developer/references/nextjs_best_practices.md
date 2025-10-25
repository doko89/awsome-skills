# Next.js Best Practices

## App Router Best Practices

### Server Components by Default

Use Server Components by default for better performance:

```tsx
// ✅ Good - Server Component (default)
export default async function Page() {
  const data = await fetchData()
  return <div>{data}</div>
}

// ❌ Avoid - Unnecessary Client Component
"use client"
export default function Page() {
  return <div>Static content</div>
}
```

### Use Client Components Only When Needed

Add `"use client"` only when you need:
- Event handlers (onClick, onChange, etc.)
- React hooks (useState, useEffect, etc.)
- Browser APIs

```tsx
// ✅ Good - Client Component for interactivity
"use client"
import { useState } from "react"

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### Data Fetching in Server Components

```tsx
// ✅ Good - Async Server Component
export default async function PostsPage() {
  const posts = await fetch('https://api.example.com/posts', {
    cache: 'no-store', // or 'force-cache' for static
  }).then(res => res.json())
  
  return <PostsList posts={posts} />
}

// ✅ Good - Parallel data fetching
export default async function Page() {
  const [posts, users] = await Promise.all([
    fetchPosts(),
    fetchUsers(),
  ])
  
  return <Dashboard posts={posts} users={users} />
}
```

### Loading States with Suspense

```tsx
import { Suspense } from "react"

export default function Page() {
  return (
    <Suspense fallback={<LoadingSkeleton />}>
      <AsyncComponent />
    </Suspense>
  )
}
```

### Error Handling

Create `error.tsx` for error boundaries:

```tsx
// app/posts/error.tsx
"use client"

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

### Loading States

Create `loading.tsx` for loading UI:

```tsx
// app/posts/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>
}
```

## Routing Best Practices

### Dynamic Routes

```tsx
// app/posts/[id]/page.tsx
export default async function PostPage({
  params,
}: {
  params: { id: string }
}) {
  const post = await fetchPost(params.id)
  return <Post data={post} />
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await fetchPosts()
  return posts.map((post) => ({
    id: post.id.toString(),
  }))
}
```

### Route Groups

Use route groups for organization without affecting URL:

```
app/
├── (marketing)/
│   ├── about/
│   └── contact/
├── (shop)/
│   ├── products/
│   └── cart/
└── layout.tsx
```

### Parallel Routes

```
app/
├── @analytics/
│   └── page.tsx
├── @team/
│   └── page.tsx
└── layout.tsx
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (
    <>
      {children}
      {analytics}
      {team}
    </>
  )
}
```

## Performance Best Practices

### Image Optimization

```tsx
import Image from "next/image"

// ✅ Good - Optimized images
export function Avatar() {
  return (
    <Image
      src="/avatar.jpg"
      alt="Avatar"
      width={100}
      height={100}
      priority // for above-the-fold images
    />
  )
}
```

### Font Optimization

```tsx
import { Inter, Roboto_Mono } from "next/font/google"

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
})

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  display: "swap",
})

export default function Layout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

### Metadata

```tsx
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "My Page",
  description: "Page description",
  openGraph: {
    title: "My Page",
    description: "Page description",
    images: ["/og-image.jpg"],
  },
}
```

### Dynamic Metadata

```tsx
export async function generateMetadata({
  params,
}: {
  params: { id: string }
}): Promise<Metadata> {
  const post = await fetchPost(params.id)
  
  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

## Authentication Best Practices

### Protect Routes with Middleware

```tsx
// middleware.ts
import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

export default auth((req) => {
  const isLoggedIn = !!req.auth
  const isAuthPage = req.nextUrl.pathname.startsWith("/auth")
  const isProtectedPage = req.nextUrl.pathname.startsWith("/dashboard")

  if (isProtectedPage && !isLoggedIn) {
    return NextResponse.redirect(new URL("/auth/signin", req.url))
  }

  if (isAuthPage && isLoggedIn) {
    return NextResponse.redirect(new URL("/dashboard", req.url))
  }

  return NextResponse.next()
})

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
```

### Check Auth in Server Components

```tsx
import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"

export default async function ProtectedPage() {
  const session = await auth()
  
  if (!session) {
    redirect("/auth/signin")
  }

  return <div>Protected content</div>
}
```

### Use Session in Client Components

```tsx
"use client"

import { useSession } from "next-auth/react"

export function UserProfile() {
  const { data: session, status } = useSession()

  if (status === "loading") {
    return <div>Loading...</div>
  }

  if (!session) {
    return <div>Not authenticated</div>
  }

  return <div>Welcome, {session.user?.name}</div>
}
```

## Database Best Practices

### Use Drizzle Query Builder

```tsx
import { db } from "@/db"
import { users, posts } from "@/db/schema"
import { eq, and, desc } from "drizzle-orm"

// ✅ Good - Type-safe queries
export async function getUserPosts(userId: string) {
  return await db.query.posts.findMany({
    where: eq(posts.userId, userId),
    orderBy: [desc(posts.createdAt)],
    with: {
      user: true,
    },
  })
}

// ✅ Good - Transactions
export async function createPostWithTags(postData, tagIds) {
  return await db.transaction(async (tx) => {
    const [post] = await tx.insert(posts).values(postData).returning()
    
    await tx.insert(postTags).values(
      tagIds.map(tagId => ({ postId: post.id, tagId }))
    )
    
    return post
  })
}
```

### Connection Pooling

```tsx
// db/index.ts
import { drizzle } from "drizzle-orm/postgres-js"
import postgres from "postgres"

const connectionString = process.env.DATABASE_URL!

// Disable prefetch for serverless
const client = postgres(connectionString, { prepare: false })
export const db = drizzle(client)
```

## API Routes Best Practices

### Error Handling

```tsx
import { NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    const data = await fetchData()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Error:", error)
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    )
  }
}
```

### Request Validation

```tsx
import { z } from "zod"

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
})

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validated = schema.parse(body)
    
    // Process validated data
    return NextResponse.json({ success: true })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: error.errors },
        { status: 400 }
      )
    }
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    )
  }
}
```

### Rate Limiting

```tsx
import { Ratelimit } from "@upstash/ratelimit"
import { Redis } from "@upstash/redis"

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10 s"),
})

export async function POST(request: NextRequest) {
  const ip = request.ip ?? "127.0.0.1"
  const { success } = await ratelimit.limit(ip)

  if (!success) {
    return NextResponse.json(
      { error: "Too many requests" },
      { status: 429 }
    )
  }

  // Process request
}
```

## TypeScript Best Practices

### Type-safe Environment Variables

```tsx
// env.ts
import { z } from "zod"

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  NEXTAUTH_URL: z.string().url(),
  GOOGLE_CLIENT_ID: z.string().optional(),
  GOOGLE_CLIENT_SECRET: z.string().optional(),
})

export const env = envSchema.parse(process.env)
```

### Extend NextAuth Types

```tsx
// types/next-auth.d.ts
import { DefaultSession } from "next-auth"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
    } & DefaultSession["user"]
  }
}
```

## Testing Best Practices

### Unit Tests

```tsx
import { render, screen } from "@testing-library/react"
import { Button } from "@/components/ui/button"

describe("Button", () => {
  it("renders correctly", () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText("Click me")).toBeInTheDocument()
  })
})
```

### Integration Tests

```tsx
import { test, expect } from "@playwright/test"

test("user can sign in", async ({ page }) => {
  await page.goto("/auth/signin")
  await page.fill('input[name="email"]', "user@example.com")
  await page.fill('input[name="password"]', "password")
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL("/dashboard")
})
```

## Deployment Best Practices

### Environment Variables

- Use `.env.local` for local development
- Set environment variables in Vercel/hosting platform
- Never commit `.env.local` to git

### Build Optimization

```json
// next.config.js
module.exports = {
  images: {
    domains: ["example.com"],
  },
  experimental: {
    optimizeCss: true,
  },
}
```

### Monitoring

- Use Vercel Analytics
- Add error tracking (Sentry)
- Monitor performance (Web Vitals)

## Security Best Practices

### Content Security Policy

```tsx
// next.config.js
const securityHeaders = [
  {
    key: "X-DNS-Prefetch-Control",
    value: "on",
  },
  {
    key: "X-Frame-Options",
    value: "SAMEORIGIN",
  },
  {
    key: "X-Content-Type-Options",
    value: "nosniff",
  },
]

module.exports = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ]
  },
}
```

### Sanitize User Input

```tsx
import DOMPurify from "isomorphic-dompurify"

export function sanitizeHtml(html: string) {
  return DOMPurify.sanitize(html)
}
```

