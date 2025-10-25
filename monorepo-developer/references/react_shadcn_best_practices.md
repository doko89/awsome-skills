# React + shadcn/ui Best Practices

## Component Organization

### Directory Structure

```
src/
├── components/
│   ├── ui/              # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── layout/          # Layout components
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   ├── features/        # Feature components
│   │   ├── UserList.tsx
│   │   ├── ProductCard.tsx
│   │   └── ...
│   └── common/          # Reusable components
│       ├── Loading.tsx
│       ├── Error.tsx
│       └── ...
├── pages/               # Page components
├── hooks/               # Custom hooks
├── lib/                 # Utilities
├── services/            # API services
├── store/               # State management
├── types/               # TypeScript types
└── utils/               # Helper functions
```

## Component Patterns

### Functional Component with TypeScript

```typescript
import { FC, ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface CardProps {
  title: string
  description?: string
  children: ReactNode
  className?: string
}

export const Card: FC<CardProps> = ({
  title,
  description,
  children,
  className
}) => {
  return (
    <div className={cn('rounded-lg border bg-white p-6', className)}>
      <h2 className='text-lg font-semibold'>{title}</h2>
      {description && <p className='text-sm text-gray-600'>{description}</p>}
      {children}
    </div>
  )
}
```

### Using shadcn/ui Components

```typescript
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'

export function UserForm() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Create User</CardTitle>
      </CardHeader>
      <CardContent className='space-y-4'>
        <Input placeholder='Name' />
        <Input placeholder='Email' type='email' />
        <Button>Create</Button>
      </CardContent>
    </Card>
  )
}
```

## State Management with Zustand

### Store Definition

```typescript
import { create } from 'zustand'

interface User {
  id: number
  name: string
  email: string
}

interface UserStore {
  users: User[]
  addUser: (user: User) => void
  removeUser: (id: number) => void
  updateUser: (id: number, user: Partial<User>) => void
}

export const useUserStore = create<UserStore>((set) => ({
  users: [],
  addUser: (user) => set((state) => ({
    users: [...state.users, user]
  })),
  removeUser: (id) => set((state) => ({
    users: state.users.filter(u => u.id !== id)
  })),
  updateUser: (id, updates) => set((state) => ({
    users: state.users.map(u => u.id === id ? { ...u, ...updates } : u)
  }))
}))
```

### Using Store in Component

```typescript
import { useUserStore } from '@/store/userStore'

export function UserList() {
  const { users, removeUser } = useUserStore()

  return (
    <div className='space-y-2'>
      {users.map(user => (
        <div key={user.id} className='flex justify-between items-center'>
          <span>{user.name}</span>
          <Button
            variant='destructive'
            size='sm'
            onClick={() => removeUser(user.id)}
          >
            Delete
          </Button>
        </div>
      ))}
    </div>
  )
}
```

## Data Fetching with React Query

### Query Hook

```typescript
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

interface User {
  id: number
  name: string
  email: string
}

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await axios.get('/api/users')
      return data as User[]
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}
```

### Using Query Hook

```typescript
import { useUsers } from '@/hooks/useUsers'

export function UserList() {
  const { data: users, isLoading, error } = useUsers()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div className='space-y-2'>
      {users?.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  )
}
```

## Custom Hooks

### useLocalStorage Hook

```typescript
import { useState, useEffect } from 'react'

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(error)
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue] as const
}
```

### useDebounce Hook

```typescript
import { useState, useEffect } from 'react'

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}
```

## Styling with Tailwind CSS

### Using cn() Utility

```typescript
import { cn } from '@/lib/utils'

interface ButtonProps {
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function Button({ variant = 'primary', size = 'md', className }: ButtonProps) {
  return (
    <button
      className={cn(
        'font-semibold rounded-lg transition-colors',
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
          'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary',
          'px-2 py-1 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        className
      )}
    >
      Click me
    </button>
  )
}
```

## Form Handling

### React Hook Form Integration

```typescript
import { useForm } from 'react-hook-form'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface FormData {
  name: string
  email: string
}

export function UserForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>()

  const onSubmit = (data: FormData) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className='space-y-4'>
      <div>
        <Input
          placeholder='Name'
          {...register('name', { required: 'Name is required' })}
        />
        {errors.name && <span className='text-red-500'>{errors.name.message}</span>}
      </div>
      <div>
        <Input
          placeholder='Email'
          type='email'
          {...register('email', { required: 'Email is required' })}
        />
        {errors.email && <span className='text-red-500'>{errors.email.message}</span>}
      </div>
      <Button type='submit'>Submit</Button>
    </form>
  )
}
```

## Performance Optimization

### Memoization

```typescript
import { memo, useMemo, useCallback } from 'react'

interface UserItemProps {
  user: User
  onDelete: (id: number) => void
}

export const UserItem = memo(({ user, onDelete }: UserItemProps) => {
  return (
    <div className='flex justify-between items-center'>
      <span>{user.name}</span>
      <Button onClick={() => onDelete(user.id)}>Delete</Button>
    </div>
  )
})

export function UserList() {
  const users = useUsers()
  
  const handleDelete = useCallback((id: number) => {
    // Delete logic
  }, [])

  const memoizedUsers = useMemo(() => users, [users])

  return (
    <div>
      {memoizedUsers?.map(user => (
        <UserItem key={user.id} user={user} onDelete={handleDelete} />
      ))}
    </div>
  )
}
```

## Error Handling

### Error Boundary

```typescript
import { ReactNode } from 'react'

interface ErrorBoundaryProps {
  children: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className='p-4 bg-red-100 border border-red-400 rounded'>
          <h2 className='font-bold'>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
        </div>
      )
    }

    return this.props.children
  }
}
```

## Testing

### Component Testing

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { UserForm } from '@/components/UserForm'

describe('UserForm', () => {
  it('submits form data', async () => {
    const user = userEvent.setup()
    render(<UserForm />)

    await user.type(screen.getByPlaceholderText('Name'), 'John')
    await user.type(screen.getByPlaceholderText('Email'), 'john@example.com')
    await user.click(screen.getByText('Submit'))

    // Assert
  })
})
```

