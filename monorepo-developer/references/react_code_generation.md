# React Code Generation Guide

This guide covers the code generation scripts for React components, hooks, and pages in the monorepo.

## Overview

The monorepo-developer skill provides three powerful code generation scripts:

1. **generate_component.py** - Generate React components
2. **generate_hook.py** - Generate custom React hooks
3. **generate_page.py** - Generate React pages

These scripts help you quickly scaffold common patterns and maintain consistency across your frontend packages.

## Generate Components

### Basic Usage

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py <component-name> [--type <type>] [--directory <dir>] [--package <name>]
```

### Component Types

#### 1. Basic Component

Simple component with props interface:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py Button --type basic
```

Generated structure:
```typescript
interface ButtonProps {
  // Add your props here
}

export function Button({ }: ButtonProps) {
  return (
    <div>
      <h2>Button</h2>
    </div>
  )
}
```

#### 2. Component with Children

Component that accepts children:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py Card --type children
```

Use for layout components, wrappers, and containers.

#### 3. Component with State

Component with useState hook:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py Counter --type state
```

Includes increment/decrement buttons and state management.

#### 4. Form Component

Form with validation and submission:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py LoginForm --type form
```

Includes:
- Form state management
- Input handling
- Loading state
- shadcn/ui integration

#### 5. Card Component

Card component using shadcn/ui:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserCard --type card
```

Includes:
- Card header with title
- Optional description
- Content area

#### 6. List Component

List component with rendering:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserList --type list
```

Includes:
- Item rendering
- Empty state
- Key management

#### 7. Modal Component

Modal/Dialog component:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py ConfirmDialog --type modal
```

Includes:
- Dialog state management
- Confirm/Cancel buttons
- shadcn/ui Dialog integration

### Advanced Options

#### Custom Directory

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserCard --type card --directory features/users
```

Creates: `src/components/features/users/UserCard.tsx`

#### Target Specific Package

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py Dashboard --type basic --package admin-panel
```

#### Auto-generated Index

The script automatically creates/updates `index.ts`:

```typescript
export { UserCard } from './UserCard'
```

## Generate Custom Hooks

### Basic Usage

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py <hook-name> [--type <type>] [--package <name>]
```

### Hook Types

#### 1. Basic Hook

Simple hook template:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useCounter --type basic
```

#### 2. Fetch Hook

Data fetching with loading and error states:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useUserData --type fetch
```

Returns:
```typescript
{
  data: T | null
  loading: boolean
  error: Error | null
}
```

#### 3. localStorage Hook

Persist state to localStorage:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useLocalStorage --type local-storage
```

Usage:
```typescript
const [value, setValue] = useLocalStorage('key', initialValue)
```

#### 4. Debounce Hook

Debounce values:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useDebounce --type debounce
```

Usage:
```typescript
const debouncedValue = useDebounce(value, 500)
```

#### 5. Throttle Hook

Throttle function calls:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useThrottle --type throttle
```

#### 6. Toggle Hook

Toggle boolean state:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useModal --type toggle
```

Returns:
```typescript
{
  value: boolean
  toggle: () => void
  setTrue: () => void
  setFalse: () => void
  setValue: (value: boolean) => void
}
```

#### 7. Previous Hook

Get previous value:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py usePrevious --type previous
```

#### 8. Async Hook

Handle async operations:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useFetchUser --type async
```

Returns:
```typescript
{
  status: 'idle' | 'pending' | 'success' | 'error'
  data: T | null
  error: Error | null
  execute: () => Promise<T>
}
```

## Generate Pages

### Basic Usage

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py <page-name> [--type <type>] [--package <name>]
```

### Page Types

#### 1. Basic Page

Simple page template:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py About --type basic
```

#### 2. List Page

Page with list, search, and filtering:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py Users --type list
```

Includes:
- Search input
- Item list
- Empty state
- Add button

#### 3. Detail Page

Page for viewing item details:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py UserDetail --type detail
```

Includes:
- Back button
- Details section
- Actions sidebar
- Edit/Delete buttons

#### 4. Form Page

Page with form submission:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py CreateUser --type form
```

Includes:
- Form fields
- Submit button
- Loading state
- Cancel button

#### 5. Dashboard Page

Dashboard with stats cards:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py Dashboard --type dashboard
```

Includes:
- Stats cards
- Recent activity section
- Quick stats section
- Responsive grid

## Best Practices

### Naming Conventions

- **Components**: PascalCase (e.g., `UserCard`, `LoginForm`)
- **Hooks**: camelCase with `use` prefix (e.g., `useUserData`, `useLocalStorage`)
- **Pages**: PascalCase (e.g., `Dashboard`, `UserList`)

### Organization

```
src/
├── components/
│   ├── ui/              # shadcn/ui components
│   ├── features/        # Feature-specific components
│   │   ├── users/
│   │   ├── products/
│   │   └── orders/
│   └── common/          # Shared components
├── hooks/               # Custom hooks
├── pages/               # Page components
└── lib/                 # Utilities
```

### Component Structure

```typescript
// 1. Imports
import { useState } from 'react'
import { Button } from '@/components/ui/button'

// 2. Types
interface MyComponentProps {
  title: string
  onSubmit?: () => void
}

// 3. Component
export function MyComponent({ title, onSubmit }: MyComponentProps) {
  const [state, setState] = useState(false)

  return (
    <div>
      <h1>{title}</h1>
    </div>
  )
}

// 4. Export
export default MyComponent
```

### Hook Patterns

```typescript
// Custom hook pattern
export function useMyHook(initialValue: string) {
  const [value, setValue] = useState(initialValue)

  const reset = () => setValue(initialValue)

  return { value, setValue, reset }
}

// Usage
const { value, setValue, reset } = useMyHook('default')
```

## Workflow Example

### Create a User Management Feature

```bash
# 1. Generate pages
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py UserList --type list
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py UserDetail --type detail
python ~/.claude/skills/monorepo-developer/scripts/generate_page.py CreateUser --type form

# 2. Generate components
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserCard --type card
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py UserForm --type form

# 3. Generate hooks
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useUsers --type fetch
python ~/.claude/skills/monorepo-developer/scripts/generate_hook.py useUserForm --type basic

# 4. Add shadcn/ui components
python ~/.claude/skills/monorepo-developer/scripts/add_component.py button input label dialog
```

## Tips & Tricks

### Reusing Generated Code

Generated code is a starting point. Customize it for your needs:

```typescript
// Generated code
interface UserCardProps {
  title: string
  description?: string
  children?: React.ReactNode
}

// Customize for your use case
interface UserCardProps {
  user: User
  onEdit?: (user: User) => void
  onDelete?: (userId: string) => void
}
```

### Combining Hooks and Components

```typescript
// Use generated hook in generated component
import { useUsers } from '@/hooks'
import { UserList } from '@/components'

export function UsersPage() {
  const { data: users, loading, error } = useUsers()

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <UserList items={users} />
}
```

### Type Safety

All generated code includes TypeScript interfaces:

```typescript
// Always define props interface
interface ComponentProps {
  required: string
  optional?: number
}

// Use in component
export function Component({ required, optional }: ComponentProps) {
  // ...
}
```

## Troubleshooting

### Script Not Found

Ensure you're in the monorepo root directory:

```bash
cd my-monorepo
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py MyComponent --type basic
```

### Package Not Found

Specify the package explicitly:

```bash
python ~/.claude/skills/monorepo-developer/scripts/generate_component.py MyComponent --package frontend
```

### Import Errors

Check that the generated file is in the correct location and index.ts is updated:

```bash
# Verify structure
ls -la src/components/
cat src/components/index.ts
```

## See Also

- [React + shadcn Best Practices](./react_shadcn_best_practices.md)
- [Monorepo Best Practices](./monorepo_best_practices.md)
- [Bun + Hono Setup](./bun_hono_setup.md)

