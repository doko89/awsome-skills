# Gin Developer Skill

A comprehensive skill for developing Go web applications using the Gin framework with Domain-Driven Design (DDD) architecture.

## Overview

This skill provides tools and guidance for building production-ready Go web APIs with:
- **Gin Framework** (v1.11.0) - High-performance HTTP web framework
- **Domain-Driven Design** - Clean architecture with clear separation of concerns
- **GORM** - Powerful ORM for database operations
- **Code Generation** - Automated scaffolding for rapid development

## Features

✅ **Project Initialization** - Complete project setup with best practices
✅ **Domain Generation** - Automated CRUD component generation
✅ **JWT Authentication** - User registration, login, and protected routes
✅ **DDD Architecture** - 4-layer architecture (Domain, Use Case, Handler, Infrastructure)
✅ **Database Integration** - PostgreSQL with GORM ORM
✅ **Infrastructure Components** - Storage, cache, queue, email
✅ **Middleware Support** - CORS, rate limiting, logging, security, and more
✅ **Environment Configuration** - Easy configuration management
✅ **Response Helpers** - Consistent API responses
✅ **Validation** - Built-in request validation
✅ **API Documentation** - Swagger/OpenAPI support

## Quick Start

### 1. Initialize a New Project

```bash
python scripts/init_project.py my-api
cd my-api
```

This creates a complete project structure with:
- Go modules configuration
- Main application file
- Database setup
- Middleware
- Configuration management
- Response helpers

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Generate Your First Domain

```bash
python scripts/generate_domain.py user --fields "name:string,email:string,age:int,active:bool"
```

This generates:
- Entity (domain model)
- Repository interface
- Repository implementation
- Use case (business logic)
- HTTP handler
- CRUD endpoints

### 4. Register the Domain

Edit `cmd/api/main.go` to register your domain:

```go
// Import generated packages
import (
    "github.com/myuser/my-api/internal/domain/entity"
    "github.com/myuser/my-api/internal/handler"
    "github.com/myuser/my-api/internal/infrastructure/repository"
    "github.com/myuser/my-api/internal/usecase"
)

// Add migration
db.AutoMigrate(&entity.User{})

// Register routes
userRepo := repository.NewUserRepository(db)
userUseCase := usecase.NewUserUseCase(userRepo)
userHandler := handler.NewUserHandler(userUseCase)
userHandler.RegisterRoutes(v1)
```

### 5. Run the Application

```bash
go mod tidy
go run cmd/api/main.go
```

### 6. Add Authentication (Optional)

```bash
python scripts/add_auth.py
go get github.com/golang-jwt/jwt/v5 golang.org/x/crypto/bcrypt
```

Update `.env` with JWT configuration:
```env
JWT_SECRET=your-secret-key-here
JWT_ISSUER=my-api
JWT_EXPIRY_MINUTES=1440
```

### 7. Test Your API

```bash
# Health check
curl http://localhost:8080/health

# Register user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","name":"John Doe"}'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Get profile (protected)
curl http://localhost:8080/api/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Create user
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","age":30,"active":true}'

# Get all users
curl http://localhost:8080/api/v1/users

# Get user by ID
curl http://localhost:8080/api/v1/users/1

# Update user
curl -X PUT http://localhost:8080/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated","email":"john@example.com","age":31,"active":true}'

# Delete user
curl -X DELETE http://localhost:8080/api/v1/users/1
```

## Project Structure

```
my-api/
├── cmd/
│   └── api/
│       └── main.go              # Application entry point
├── internal/
│   ├── domain/                  # Domain layer (pure business logic)
│   │   ├── entity/             # Business entities
│   │   └── repository/         # Repository interfaces
│   ├── usecase/                # Application layer (business workflows)
│   ├── handler/                # Interface layer (HTTP handlers)
│   └── infrastructure/         # Infrastructure layer (implementations)
│       ├── repository/         # Repository implementations
│       ├── database/           # Database connection
│       └── config/             # Configuration
├── pkg/                        # Shared packages
│   ├── middleware/             # HTTP middleware
│   ├── response/               # Response helpers
│   └── validator/              # Validation utilities
├── scripts/                    # Generation scripts
├── .env.example               # Environment variables template
├── .gitignore
├── go.mod
├── go.sum
└── README.md
```

## Scripts

### init_project.py

Initialize a new Gin project with DDD structure.

```bash
python scripts/init_project.py <project-name> [--module-path <module-path>]
```

**Options:**
- `project-name` - Name of the project (required)
- `--module-path` - Go module path (default: project-name)

**Example:**
```bash
python scripts/init_project.py ecommerce-api
# or with custom module path
python scripts/init_project.py ecommerce-api --module-path github.com/mycompany/ecommerce-api
```

### generate_domain.py

Generate domain components with CRUD operations.

```bash
python scripts/generate_domain.py <domain-name> [--fields <field1:type1,field2:type2>] [--project-path <path>]
```

**Options:**
- `domain-name` - Name of the domain (required)
- `--fields` - Comma-separated field definitions (optional)
- `--project-path` - Path to project root (default: current directory)

**Supported Field Types:**
- `string` - String type
- `int`, `int64` - Integer types
- `float64` - Float type
- `bool` - Boolean type
- `time` - time.Time type
- `uuid` - UUID type

**Examples:**
```bash
# User domain
python scripts/generate_domain.py user --fields "name:string,email:string,age:int,active:bool"

# Product domain
python scripts/generate_domain.py product --fields "name:string,description:string,price:float64,stock:int"

# Order domain
python scripts/generate_domain.py order --fields "user_id:uuid,total:float64,status:string,created_at:time"
```

### add_auth.py

Add JWT authentication to your project (local, Google OAuth, or both).

```bash
python scripts/add_auth.py [--project-path <path>] [--provider <local|google|both>]
```

**Providers:**
- `local` - Email/password authentication
- `google` - Google OAuth authentication
- `both` - Both local and Google OAuth (default)

**What it creates:**
- User entity with password hashing and avatar support
- Auth DTOs (Register, Login, GoogleAuth, Response)
- Auth repository and service
- Auth handler with endpoints (Register, Login, GoogleAuth, GetProfile, UploadAvatar)
- JWT utility package
- Auth middleware (JWT validation, role-based access)
- Uploads directory for avatars

**Examples:**
```bash
cd my-api
python ../scripts/add_auth.py --provider=both
python ../scripts/add_auth.py --provider=local
python ../scripts/add_auth.py --provider=google
```

---

### add_infrastructure.py

Add infrastructure components like storage, cache, queue, email.

```bash
python scripts/add_infrastructure.py --type=<type> --provider=<provider> [--project-path=<path>]
```

**Storage:**
```bash
python scripts/add_infrastructure.py --type=storage --provider=local
python scripts/add_infrastructure.py --type=storage --provider=s3
python scripts/add_infrastructure.py --type=storage --provider=gcs
```

**Cache:**
```bash
python scripts/add_infrastructure.py --type=cache --provider=redis
python scripts/add_infrastructure.py --type=cache --provider=memory
```

**Queue:**
```bash
python scripts/add_infrastructure.py --type=queue --provider=redis
python scripts/add_infrastructure.py --type=queue --provider=kafka
python scripts/add_infrastructure.py --type=queue --provider=rabbitmq
```

**Email:**
```bash
python scripts/add_infrastructure.py --type=email --provider=smtp
python scripts/add_infrastructure.py --type=email --provider=sendgrid
```

### add_middleware.py

Add middleware components to your project.

```bash
python scripts/add_middleware.py --type=<type> [--project-path=<path>]
```

**Available Middlewares:**
- `cors` - CORS configuration
- `ratelimit` - Rate limiting (IP/user/global)
- `logging` - Request/response logging
- `recovery` - Panic recovery
- `timeout` - Request timeout
- `compression` - Gzip compression
- `security` - Security headers
- `requestid` - Request ID tracing
- `metrics` - Prometheus metrics
- `validation` - Request validation

**Examples:**
```bash
python scripts/add_middleware.py --type=cors
python scripts/add_middleware.py --type=ratelimit
python scripts/add_middleware.py --type=security
```

### generate_docs.py

Generate Swagger/OpenAPI documentation structure.

```bash
python scripts/generate_docs.py [--project-path=<path>]
```

Creates documentation structure with Swagger annotations, response models, and examples.

## Architecture

This skill follows a 4-layer DDD architecture:

### 1. Domain Layer (`internal/domain/`)
- Pure business logic
- No external dependencies
- Defines entities and repository interfaces

### 2. Use Case Layer (`internal/usecase/`)
- Business workflows
- Orchestrates domain operations
- Implements business rules

### 3. Handler Layer (`internal/handler/`)
- HTTP request/response handling
- Input validation
- Delegates to use cases

### 4. Infrastructure Layer (`internal/infrastructure/`)
- Technical implementations
- Database access
- External service integrations

## Environment Variables

```env
# Server
PORT=8080
GIN_MODE=debug  # debug, release, test

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=mydb
DB_SSLMODE=disable

# CORS
CORS_ALLOWED_ORIGINS=*
```

## Dependencies

Generated projects include:

- **gin-gonic/gin** (v1.11.0) - Web framework
- **gorm.io/gorm** (v1.25.12) - ORM
- **gorm.io/driver/postgres** (v1.5.11) - PostgreSQL driver
- **github.com/joho/godotenv** (v1.5.1) - Environment variables
- **github.com/google/uuid** (v1.6.0) - UUID generation
- **github.com/go-playground/validator/v10** (v10.23.0) - Validation

## References

See the `references/` directory for detailed guides:

- **ddd_architecture.md** - Domain-Driven Design patterns and principles
- **gin_best_practices.md** - Gin framework best practices
- **gorm_examples.md** - GORM usage examples and patterns

## Examples

### Generate Multiple Domains

```bash
# User management
python scripts/generate_domain.py user --fields "name:string,email:string,password:string,role:string"

# Product catalog
python scripts/generate_domain.py product --fields "name:string,description:string,price:float64,stock:int,category:string"

# Order processing
python scripts/generate_domain.py order --fields "user_id:uuid,total:float64,status:string,payment_method:string"

# Category management
python scripts/generate_domain.py category --fields "name:string,description:string,parent_id:int"
```

### Customize Generated Code

After generation, you can:

1. **Add custom methods** to entities
2. **Extend repositories** with custom queries
3. **Implement business logic** in use cases
4. **Add middleware** for authentication/authorization
5. **Customize validation** rules

## Best Practices

1. **Keep domain layer pure** - No external dependencies
2. **Use interfaces** - Define contracts in domain layer
3. **Thin handlers** - Only HTTP concerns
4. **Business logic in use cases** - Not in handlers
5. **Test each layer** - Unit tests for use cases, integration tests for repositories

## Troubleshooting

### Import Errors
```bash
go mod tidy
```

### Database Connection Issues
- Check environment variables in `.env`
- Ensure PostgreSQL is running
- Verify connection credentials

### Port Already in Use
```bash
PORT=8081 go run cmd/api/main.go
```

## Contributing

This skill is part of the Anthropic Skills ecosystem. Contributions are welcome!

## License

MIT License

## Support

For issues and questions:
- Check the `references/` directory for detailed documentation
- Review the generated code comments
- Consult the official Gin and GORM documentation

---

**Happy Coding! 🚀**

