# Domain-Driven Design (DDD) Architecture

## Overview

Domain-Driven Design is a software development approach that focuses on modeling software to match a domain according to input from domain experts. This reference guide explains how DDD is implemented in our Gin projects.

## Architecture Layers

### 1. Domain Layer (`internal/domain/`)

The **Domain Layer** is the heart of the application. It contains:

#### Entities (`internal/domain/entity/`)
- Pure business objects with identity
- No dependencies on external frameworks
- Contains business rules and validation
- Represents core business concepts

**Example:**
```go
type User struct {
    ID        uint      `json:"id" gorm:"primaryKey"`
    Name      string    `json:"name" gorm:"type:varchar(255)"`
    Email     string    `json:"email" gorm:"type:varchar(255);unique"`
    CreatedAt time.Time `json:"created_at" gorm:"autoCreateTime"`
    UpdatedAt time.Time `json:"updated_at" gorm:"autoUpdateTime"`
}

func (u *User) TableName() string {
    return "users"
}
```

#### Repository Interfaces (`internal/domain/repository/`)
- Define contracts for data access
- No implementation details
- Depend on domain entities only

**Example:**
```go
type UserRepository interface {
    Create(u *entity.User) error
    FindByID(id uint) (*entity.User, error)
    FindAll(limit, offset int) ([]*entity.User, error)
    Update(u *entity.User) error
    Delete(id uint) error
}
```

**Key Principles:**
- No external dependencies (database, HTTP, etc.)
- Pure Go code
- Business logic lives here
- Defines interfaces, not implementations

---

### 2. Use Case Layer (`internal/usecase/`)

The **Use Case Layer** (Application Layer) orchestrates the flow of data and business logic.

**Responsibilities:**
- Implement business workflows
- Coordinate between repositories
- Handle transactions
- Enforce business rules
- Transform data between layers

**Example:**
```go
type UserUseCase interface {
    Create(u *entity.User) error
    GetByID(id uint) (*entity.User, error)
    GetAll(limit, offset int) ([]*entity.User, int64, error)
    Update(id uint, u *entity.User) error
    Delete(id uint) error
}

type userUseCase struct {
    repo repository.UserRepository
}

func (uc *userUseCase) Create(u *entity.User) error {
    // Business logic: validate email format
    if !isValidEmail(u.Email) {
        return errors.New("invalid email format")
    }
    
    // Business logic: check if email already exists
    existing, _ := uc.repo.FindByEmail(u.Email)
    if existing != nil {
        return errors.New("email already exists")
    }
    
    return uc.repo.Create(u)
}
```

**Key Principles:**
- Depends on domain interfaces, not implementations
- Contains business logic
- No HTTP or database concerns
- Testable without external dependencies

---

### 3. Handler Layer (`internal/handler/`)

The **Handler Layer** (Interface/Presentation Layer) handles HTTP requests and responses.

**Responsibilities:**
- Parse HTTP requests
- Validate input
- Call use cases
- Format responses
- Handle HTTP status codes

**Example:**
```go
type UserHandler struct {
    useCase usecase.UserUseCase
}

func (h *UserHandler) Create(c *gin.Context) {
    var req entity.User
    if err := c.ShouldBindJSON(&req); err != nil {
        response.Error(c, http.StatusBadRequest, "Invalid request", err)
        return
    }
    
    if err := h.useCase.Create(&req); err != nil {
        response.Error(c, http.StatusInternalServerError, "Failed to create user", err)
        return
    }
    
    response.Success(c, http.StatusCreated, "User created", req)
}
```

**Key Principles:**
- Thin layer (no business logic)
- HTTP concerns only
- Delegates to use cases
- Returns appropriate status codes

---

### 4. Infrastructure Layer (`internal/infrastructure/`)

The **Infrastructure Layer** provides implementations for interfaces defined in the domain layer.

#### Repository Implementations (`internal/infrastructure/repository/`)
- Implement repository interfaces
- Handle database operations
- Use GORM or other ORMs

**Example:**
```go
type userRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) repository.UserRepository {
    return &userRepository{db: db}
}

func (r *userRepository) Create(u *entity.User) error {
    return r.db.Create(u).Error
}

func (r *userRepository) FindByID(id uint) (*entity.User, error) {
    var user entity.User
    if err := r.db.First(&user, id).Error; err != nil {
        return nil, err
    }
    return &user, nil
}
```

#### Database (`internal/infrastructure/database/`)
- Database connection setup
- Connection pooling
- Migration management

#### Configuration (`internal/infrastructure/config/`)
- Load environment variables
- Configuration management
- Feature flags

**Key Principles:**
- Implements domain interfaces
- Contains technical details
- Can be swapped without affecting domain

---

## Dependency Flow

```
Handler → Use Case → Repository Interface
                            ↑
                            |
                    Repository Implementation
```

**Dependency Rule:**
- Outer layers depend on inner layers
- Inner layers never depend on outer layers
- Domain layer has no dependencies
- Infrastructure implements domain interfaces

---

## Package Structure

```
project/
├── cmd/
│   └── api/
│       └── main.go              # Entry point, wiring
├── internal/
│   ├── domain/                  # Core business logic
│   │   ├── entity/             # Business entities
│   │   └── repository/         # Repository interfaces
│   ├── usecase/                # Application logic
│   ├── handler/                # HTTP handlers
│   └── infrastructure/         # Technical implementations
│       ├── repository/         # Repository implementations
│       ├── database/           # Database setup
│       └── config/             # Configuration
└── pkg/                        # Shared utilities
    ├── middleware/             # HTTP middleware
    ├── response/               # Response helpers
    └── validator/              # Validation utilities
```

---

## Best Practices

### 1. Keep Domain Pure
```go
// ✅ Good: Pure domain entity
type Product struct {
    ID    uint
    Name  string
    Price float64
}

func (p *Product) CalculateDiscount(percentage float64) float64 {
    return p.Price * (1 - percentage/100)
}

// ❌ Bad: Domain entity with infrastructure concerns
type Product struct {
    ID    uint
    Name  string
    Price float64
    db    *gorm.DB  // Don't do this!
}
```

### 2. Use Interfaces for Flexibility
```go
// ✅ Good: Define interface in domain
type UserRepository interface {
    Create(u *User) error
    FindByID(id uint) (*User, error)
}

// Implement in infrastructure
type postgresUserRepository struct {
    db *gorm.DB
}

// Easy to swap implementations
type mongoUserRepository struct {
    client *mongo.Client
}
```

### 3. Keep Handlers Thin
```go
// ✅ Good: Thin handler
func (h *UserHandler) Create(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        response.Error(c, 400, "Invalid input", err)
        return
    }
    
    user := req.ToEntity()
    if err := h.useCase.Create(user); err != nil {
        response.Error(c, 500, "Failed to create", err)
        return
    }
    
    response.Success(c, 201, "Created", user)
}

// ❌ Bad: Business logic in handler
func (h *UserHandler) Create(c *gin.Context) {
    var req CreateUserRequest
    c.ShouldBindJSON(&req)
    
    // Don't put business logic here!
    if !isValidEmail(req.Email) {
        // ...
    }
    if emailExists(req.Email) {
        // ...
    }
    
    // Direct database access - bad!
    h.db.Create(&user)
}
```

### 4. Use DTOs for API Contracts
```go
// Request DTO
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}

func (r *CreateUserRequest) ToEntity() *entity.User {
    return &entity.User{
        Name:  r.Name,
        Email: r.Email,
    }
}

// Response DTO
type UserResponse struct {
    ID    uint   `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

func NewUserResponse(u *entity.User) *UserResponse {
    return &UserResponse{
        ID:    u.ID,
        Name:  u.Name,
        Email: u.Email,
    }
}
```

### 5. Handle Errors Properly
```go
// Use case layer
func (uc *userUseCase) Create(u *entity.User) error {
    if err := uc.validateUser(u); err != nil {
        return fmt.Errorf("validation failed: %w", err)
    }
    
    if err := uc.repo.Create(u); err != nil {
        return fmt.Errorf("failed to create user: %w", err)
    }
    
    return nil
}

// Handler layer
func (h *UserHandler) Create(c *gin.Context) {
    // ... parse request ...
    
    if err := h.useCase.Create(&user); err != nil {
        if errors.Is(err, ErrValidation) {
            response.Error(c, 400, "Validation error", err)
            return
        }
        response.Error(c, 500, "Internal error", err)
        return
    }
    
    response.Success(c, 201, "Created", user)
}
```

---

## Testing Strategy

### Unit Tests
- Test domain entities in isolation
- Test use cases with mock repositories
- Test handlers with mock use cases

### Integration Tests
- Test repository implementations with test database
- Test full request flow

### Example: Testing Use Case
```go
func TestUserUseCase_Create(t *testing.T) {
    // Mock repository
    mockRepo := &MockUserRepository{}
    useCase := NewUserUseCase(mockRepo)
    
    user := &entity.User{
        Name:  "John Doe",
        Email: "john@example.com",
    }
    
    mockRepo.On("Create", user).Return(nil)
    
    err := useCase.Create(user)
    assert.NoError(t, err)
    mockRepo.AssertExpectations(t)
}
```

---

## Common Patterns

### 1. Repository Pattern
Abstracts data access logic

### 2. Dependency Injection
Pass dependencies through constructors

### 3. Interface Segregation
Small, focused interfaces

### 4. Single Responsibility
Each layer has one reason to change

---

## References

- [Domain-Driven Design by Eric Evans](https://www.domainlanguage.com/ddd/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)

