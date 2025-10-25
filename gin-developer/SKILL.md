---
name: gin-developer
description: A comprehensive skill for developing Go web applications using Gin framework with Domain-Driven Design (DDD) architecture. Includes project initialization and component generation scripts.
license: MIT
metadata:
  version: "1.0.0"
  author: "Augment Skills"
  go_version: "1.21+"
  gin_version: "v1.11.0"
---

# Gin Developer Skill

This skill provides tools and guidance for building Go web applications using the Gin framework with Domain-Driven Design (DDD) architecture.

## Overview

The Gin Developer skill helps you:
- Initialize new Gin projects with proper DDD structure
- Generate domain components (entities, repositories, use cases, handlers)
- Follow Go and DDD best practices
- Maintain clean architecture principles
- Implement proper dependency injection

## Architecture

This skill follows a 4-layer DDD architecture:

```
project/
├── cmd/
│   └── api/
│       └── main.go              # Application entry point
├── internal/
│   ├── domain/                  # Domain layer (entities, interfaces)
│   │   ├── entity/
│   │   └── repository/
│   ├── usecase/                 # Application layer (business logic)
│   ├── handler/                 # Interface layer (HTTP handlers)
│   └── infrastructure/          # Infrastructure layer (implementations)
│       ├── repository/
│       ├── database/
│       └── config/
├── pkg/                         # Shared packages
│   ├── middleware/
│   ├── response/
│   └── validator/
├── scripts/                     # Generation scripts
├── go.mod
└── go.sum
```

## Scripts

### 1. Initialize Project

Initialize a new Gin project with DDD structure:

```bash
python scripts/init_project.py <project-name> [--module-path <module-path>]
```

**Example:**
```bash
python scripts/init_project.py my-api
```

This creates:
- Complete directory structure
- go.mod with latest Gin version
- Main application file with basic setup
- Configuration management
- Database connection setup
- Middleware (CORS, Logger, Recovery)
- Response helpers
- Example health check endpoint

### 2. Generate Domain Components

Generate a complete domain with all layers:

```bash
python scripts/generate_domain.py <domain-name> [--fields <field1:type1,field2:type2>] [--project-path <path>]
```

**Example:**
```bash
python scripts/generate_domain.py user --fields "name:string,email:string,age:int,active:bool"
```

This generates:
- **Entity**: Domain model with validation tags
- **Repository Interface**: Domain layer contract
- **Repository Implementation**: Infrastructure layer with GORM
- **Use Case**: Business logic layer
- **Handler**: HTTP handler with Gin
- **Routes**: Route registration

**Field Types Supported:**
- `string` - String type
- `int`, `int64` - Integer types
- `float64` - Float type
- `bool` - Boolean type
- `time` - time.Time type
- `uuid` - UUID type

### 3. Add Authentication

Add JWT authentication with user management (local, Google OAuth, or both):

```bash
python scripts/add_auth.py [--project-path <path>] [--provider <local|google|both>]
```

**Providers:**
- `local` - Email/password authentication only
- `google` - Google OAuth only
- `both` - Both local and Google OAuth (default)

**What it creates:**
- User entity with password hashing (bcrypt) and avatar support
- Auth DTOs (RegisterRequest, LoginRequest, GoogleAuthRequest, LoginResponse)
- Auth repository (Create, FindByEmail, FindByProviderID, Update, UpdateAvatar)
- Auth service (Register, Login, GoogleAuth, UploadAvatar)
- Auth handler (Register, Login, GoogleAuth, GetProfile, UploadAvatar)
- JWT utility package (GenerateToken, ValidateToken)
- Auth middleware (AuthMiddleware, RoleMiddleware)
- Environment configuration for JWT and Google OAuth
- Uploads directory for avatars

**Examples:**
```bash
# Both local and Google OAuth
python scripts/add_auth.py --provider=both

# Local only
python scripts/add_auth.py --provider=local

# Google OAuth only
python scripts/add_auth.py --provider=google
```

**After running:**
1. Install dependencies:
   - `go get github.com/golang-jwt/jwt/v5`
   - `go get golang.org/x/crypto/bcrypt` (for local auth)
   - `go get google.golang.org/api/oauth2/v2` (for Google OAuth)
2. Update `.env` with `JWT_SECRET` (generate with: `openssl rand -base64 32`)
3. For Google OAuth, add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to `.env`
4. Add auth routes in `main.go`
5. Serve static files: `r.Static("/uploads", "./uploads")`
6. Run migrations to create users table

---

### 4. Add Infrastructure Components

Add infrastructure components like storage, cache, queue, email:

```bash
python scripts/add_infrastructure.py --type=<type> --provider=<provider>
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

---

### 5. Add Middleware

Add middleware components to your project:

```bash
python scripts/add_middleware.py --type=<type> [--project-path=<path>]
```

**Available Middlewares:**
- `cors` - CORS configuration middleware
- `ratelimit` - Rate limiting with multiple strategies (IP, user, global)
- `logging` - Request/response logging
- `recovery` - Panic recovery with error reporting
- `timeout` - Request timeout management
- `compression` - Gzip compression
- `security` - Security headers (HSTS, CSP, X-Frame-Options, etc.)
- `requestid` - Request ID tracing
- `metrics` - Prometheus metrics collection
- `validation` - Request validation middleware

**Examples:**
```bash
python scripts/add_middleware.py --type=cors
python scripts/add_middleware.py --type=ratelimit
python scripts/add_middleware.py --type=security
```

---

### 6. Generate API Documentation

Generate Swagger/OpenAPI documentation structure:

```bash
python scripts/generate_docs.py [--project-path=<path>]
```

This creates:
- Swagger annotations template
- Response models for API responses
- Handler examples with annotations
- Setup instructions for Swagger UI

After generation, add annotations to your handlers and run:
```bash
swag init -g cmd/api/main.go
```

## Usage Guidelines

### When to Use This Skill

Use this skill when:
- Starting a new Go web API project
- Building RESTful services with Gin
- Implementing clean architecture / DDD
- Need to generate CRUD operations quickly
- Want consistent project structure

### Best Practices

1. **Domain Layer**
   - Keep entities pure (no external dependencies)
   - Define repository interfaces in domain layer
   - Use value objects for complex types

2. **Use Case Layer**
   - Implement business logic here
   - Depend on repository interfaces, not implementations
   - Handle transactions at this layer

3. **Handler Layer**
   - Keep handlers thin (validation + delegation)
   - Use DTOs for request/response
   - Handle HTTP concerns only

4. **Infrastructure Layer**
   - Implement repository interfaces
   - Handle database connections
   - Manage external service integrations

### Code Generation Workflow

1. **Initialize Project**
   ```bash
   python scripts/init_project.py my-api
   cd my-api
   ```

2. **Generate First Domain**
   ```bash
   python scripts/generate_domain.py user --fields "name:string,email:string"
   ```

3. **Review Generated Code**
   - Check entity validation tags
   - Customize business logic in use case
   - Add custom queries to repository

4. **Run Application**
   ```bash
   go mod tidy
   go run cmd/api/main.go
   ```

5. **Test Endpoints**
   ```bash
   # Health check
   curl http://localhost:8080/health
   
   # Create user
   curl -X POST http://localhost:8080/api/v1/users \
     -H "Content-Type: application/json" \
     -d '{"name":"John","email":"john@example.com"}'
   ```

## Environment Variables

Generated projects support these environment variables:

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
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Dependencies

Generated projects include:

- **gin-gonic/gin** (v1.11.0) - Web framework
- **gorm.io/gorm** - ORM
- **gorm.io/driver/postgres** - PostgreSQL driver
- **github.com/joho/godotenv** - Environment variables
- **github.com/google/uuid** - UUID generation
- **github.com/go-playground/validator/v10** - Validation

## Examples

### Generate User Domain

```bash
python scripts/generate_domain.py user --fields "name:string,email:string,password:string,role:string,active:bool"
```

### Generate Product Domain

```bash
python scripts/generate_domain.py product --fields "name:string,description:string,price:float64,stock:int,category:string"
```

### Generate Order Domain

```bash
python scripts/generate_domain.py order --fields "user_id:uuid,total:float64,status:string,created_at:time"
```

## Customization

After generation, you can customize:

1. **Add Custom Methods** to entities
2. **Extend Repository** with custom queries
3. **Add Business Logic** to use cases
4. **Implement Middleware** for authentication
5. **Add Validation Rules** to handlers

## Troubleshooting

### Import Errors
```bash
go mod tidy
```

### Database Connection Issues
- Check environment variables
- Ensure PostgreSQL is running
- Verify connection string

### Port Already in Use
```bash
# Change PORT in .env or
PORT=8081 go run cmd/api/main.go
```

## References

See `references/` directory for:
- DDD architecture patterns
- Gin framework best practices
- GORM usage examples
- Testing strategies

