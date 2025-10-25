# Quick Start Guide

This guide will walk you through creating a complete Next.js application with authentication and UI components.

## Step 1: Initialize Project

```bash
# Create new Next.js project
python scripts/init_project.py my-blog

# Navigate to project
cd my-blog
```

This creates a Next.js project with:
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Zustand
- Axios

## Step 2: Add Authentication

```bash
# Add local + Google authentication
python ../scripts/add_auth.py --provider both
```

Update `.env.local`:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/myblog"
NEXTAUTH_SECRET="your-secret-key-here"
NEXTAUTH_URL="http://localhost:3000"
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

Generate secret:
```bash
openssl rand -base64 32
```

Run migrations:
```bash
npx drizzle-kit generate
npx drizzle-kit migrate
```

## Step 3: Add UI Components

```bash
# Add essential components
python ../scripts/add_component.py --preset essential

# Add additional components
python ../scripts/add_component.py --batch table,pagination,separator
```

## Step 4: Generate Pages

### Home Page (Already created)

Edit `src/app/page.tsx` for your home page.

### Dashboard (Protected)

```bash
python ../scripts/generate_page.py Dashboard --type protected --route dashboard
```

### Blog Posts (Data Fetching)

```bash
python ../scripts/generate_page.py Posts --type data --route posts
```

### Contact Form

```bash
python ../scripts/generate_page.py Contact --type form --route contact
```

### API Route for Posts

```bash
python ../scripts/generate_page.py posts --type api --route posts
```

## Step 5: Generate Components

### Header Component

```bash
python ../scripts/generate_component.py Header --type children
```

Edit `src/components/Header.tsx`:
```tsx
"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { useSession, signOut } from "next-auth/react"

export function Header() {
  const { data: session } = useSession()

  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-2xl font-bold">
          My Blog
        </Link>
        
        <nav className="flex items-center gap-4">
          <Link href="/posts">Posts</Link>
          <Link href="/contact">Contact</Link>
          
          {session ? (
            <>
              <Link href="/dashboard">Dashboard</Link>
              <Button onClick={() => signOut()}>Sign Out</Button>
            </>
          ) : (
            <Link href="/auth/signin">
              <Button>Sign In</Button>
            </Link>
          )}
        </nav>
      </div>
    </header>
  )
}
```

### Post Card Component

```bash
python ../scripts/generate_component.py PostCard --type card
```

Edit `src/components/PostCard.tsx`:
```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"

interface PostCardProps {
  id: number
  title: string
  excerpt: string
  author: string
  date: string
}

export function PostCard({ id, title, excerpt, author, date }: PostCardProps) {
  return (
    <Link href={`/posts/${id}`}>
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>
            By {author} • {new Date(date).toLocaleDateString()}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">{excerpt}</p>
        </CardContent>
      </Card>
    </Link>
  )
}
```

## Step 6: Generate Hooks

### Fetch Posts Hook

```bash
python ../scripts/generate_hook.py usePosts --type fetch
```

Edit `src/hooks/usePosts.ts`:
```tsx
"use client"

import { useQuery } from "@tanstack/react-query"
import axios from "axios"

interface Post {
  id: number
  title: string
  excerpt: string
  author: string
  date: string
}

export function usePosts() {
  return useQuery({
    queryKey: ["posts"],
    queryFn: async () => {
      const { data } = await axios.get<Post[]>("/api/posts")
      return data
    },
  })
}
```

## Step 7: Update Root Layout

Edit `src/app/layout.tsx`:
```tsx
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Header } from "@/components/Header"
import { Providers } from "@/components/providers"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "My Blog",
  description: "A blog built with Next.js",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <Header />
          <main>{children}</main>
        </Providers>
      </body>
    </html>
  )
}
```

Create `src/components/providers.tsx`:
```tsx
"use client"

import { SessionProvider } from "next-auth/react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { useState } from "react"

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())

  return (
    <SessionProvider>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </SessionProvider>
  )
}
```

## Step 8: Start Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Step 9: Test Features

### Test Authentication
1. Go to `/auth/signin`
2. Sign in with Google or create account
3. Access `/dashboard` (protected route)

### Test Posts
1. Go to `/posts`
2. View list of posts
3. Click on a post to view details

### Test Contact Form
1. Go to `/contact`
2. Fill out form
3. Submit

## Next Steps

### Add More Features

1. **Add Blog Post Creation**
```bash
python ../scripts/generate_page.py CreatePost --type form --route dashboard/posts/new
```

2. **Add User Profile**
```bash
python ../scripts/generate_page.py Profile --type protected --route profile
```

3. **Add Search**
```bash
python ../scripts/generate_component.py SearchBar --type state
```

### Customize Styling

Edit `tailwind.config.ts` to customize colors:
```typescript
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#0070f3",
          foreground: "#ffffff",
        },
      },
    },
  },
}
```

### Add More Components

```bash
# Add data table
python ../scripts/add_component.py data-table

# Add charts
python ../scripts/add_component.py --registry https://ui.shadcn.com/registry/charts.json

# Add AI components
python ../scripts/add_component.py --registry https://www.shadcn.io/registry/ai.json
```

### Deploy

```bash
# Build for production
npm run build

# Test production build
npm start

# Deploy to Vercel
vercel deploy
```

## Troubleshooting

### Database Connection Error
- Check `DATABASE_URL` in `.env.local`
- Ensure PostgreSQL is running
- Run migrations: `npx drizzle-kit migrate`

### Authentication Not Working
- Verify `NEXTAUTH_SECRET` is set
- Check `NEXTAUTH_URL` matches your domain
- For Google OAuth, verify credentials

### Components Not Found
- Run `npx shadcn@latest add <component>`
- Check `components.json` configuration
- Restart dev server

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
- [NextAuth.js Documentation](https://next-auth.js.org)
- [Drizzle ORM Documentation](https://orm.drizzle.team)
- [TanStack Query Documentation](https://tanstack.com/query)

