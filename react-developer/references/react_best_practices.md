# React Best Practices

## Component Design

### 1. Keep Components Small and Focused

```tsx
// ❌ Bad: Component does too much
function UserDashboard() {
  // Fetching, state management, rendering all in one
}

// ✅ Good: Split into smaller components
function UserDashboard() {
  return (
    <>
      <UserProfile />
      <UserStats />
      <UserActivity />
    </>
  )
}
```

### 2. Use Composition Over Inheritance

```tsx
// ✅ Good: Composition
function Card({ children, title }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  )
}

function UserCard({ user }) {
  return (
    <Card title={user.name}>
      <p>{user.email}</p>
    </Card>
  )
}
```

### 3. Extract Reusable Logic into Custom Hooks

```tsx
// ✅ Good: Custom hook
function useFetchUser(userId) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false))
  }, [userId])

  return { user, loading }
}

function UserProfile({ userId }) {
  const { user, loading } = useFetchUser(userId)
  // ...
}
```

## State Management

### 1. Use Local State When Possible

```tsx
// ✅ Good: Local state for UI-only state
function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### 2. Lift State Up When Needed

```tsx
// ✅ Good: Shared state lifted to parent
function Parent() {
  const [value, setValue] = useState('')
  return (
    <>
      <Input value={value} onChange={setValue} />
      <Display value={value} />
    </>
  )
}
```

### 3. Use Context for Global State

```tsx
// ✅ Good: Context for theme, auth, etc.
const ThemeContext = createContext()

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}
```

## Performance

### 1. Use React.memo for Expensive Components

```tsx
// ✅ Good: Memoize expensive component
const ExpensiveComponent = React.memo(function ExpensiveComponent({ data }) {
  // Expensive rendering logic
  return <div>{/* ... */}</div>
})
```

### 2. Use useMemo for Expensive Calculations

```tsx
// ✅ Good: Memoize expensive calculation
function Component({ items }) {
  const sortedItems = useMemo(
    () => items.sort((a, b) => a.value - b.value),
    [items]
  )
  return <List items={sortedItems} />
}
```

### 3. Use useCallback for Event Handlers

```tsx
// ✅ Good: Memoize callback
function Parent() {
  const handleClick = useCallback(() => {
    console.log('clicked')
  }, [])
  
  return <Child onClick={handleClick} />
}
```

## TypeScript

### 1. Define Prop Types

```tsx
// ✅ Good: Explicit prop types
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}

function Button({ label, onClick, variant = 'primary', disabled }: ButtonProps) {
  return <button onClick={onClick} disabled={disabled}>{label}</button>
}
```

### 2. Use Type Inference

```tsx
// ✅ Good: Let TypeScript infer types
const [count, setCount] = useState(0) // TypeScript infers number
const [user, setUser] = useState<User | null>(null) // Explicit when needed
```

## Error Handling

### 1. Use Error Boundaries

```tsx
// ✅ Good: Error boundary
class ErrorBoundary extends React.Component {
  state = { hasError: false }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>
    }
    return this.props.children
  }
}
```

### 2. Handle Async Errors

```tsx
// ✅ Good: Handle async errors
function Component() {
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchData()
      .catch(err => setError(err.message))
  }, [])

  if (error) return <div>Error: {error}</div>
  // ...
}
```

## Code Organization

### 1. File Structure

```
src/
├── components/
│   ├── ui/           # Reusable UI components
│   └── features/     # Feature-specific components
├── hooks/            # Custom hooks
├── lib/              # Utilities
├── pages/            # Page components
├── services/         # API services
└── types/            # TypeScript types
```

### 2. Naming Conventions

- Components: PascalCase (`UserCard.tsx`)
- Hooks: camelCase with 'use' prefix (`useFetchData.ts`)
- Utilities: camelCase (`formatDate.ts`)
- Constants: UPPER_SNAKE_CASE (`API_URL`)

## Testing

### 1. Test User Behavior

```tsx
// ✅ Good: Test what users see and do
test('shows error message when login fails', async () => {
  render(<LoginForm />)
  
  fireEvent.change(screen.getByLabelText('Email'), {
    target: { value: 'invalid@email.com' }
  })
  fireEvent.click(screen.getByText('Login'))
  
  expect(await screen.findByText('Invalid credentials')).toBeInTheDocument()
})
```

## Accessibility

### 1. Use Semantic HTML

```tsx
// ✅ Good: Semantic HTML
function Navigation() {
  return (
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  )
}
```

### 2. Add ARIA Labels

```tsx
// ✅ Good: ARIA labels
<button aria-label="Close dialog" onClick={onClose}>
  <X />
</button>
```

## Code Style

### 1. Use Destructuring

```tsx
// ✅ Good: Destructuring
function UserCard({ user: { name, email, avatar } }) {
  return (
    <div>
      <img src={avatar} alt={name} />
      <h2>{name}</h2>
      <p>{email}</p>
    </div>
  )
}
```

### 2. Use Optional Chaining

```tsx
// ✅ Good: Optional chaining
const userName = user?.profile?.name ?? 'Guest'
```

### 3. Use Template Literals

```tsx
// ✅ Good: Template literals
const className = `button ${variant} ${disabled ? 'disabled' : ''}`
```

