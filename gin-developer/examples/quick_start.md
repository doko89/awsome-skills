# Quick Start Guide

Get started with gin-developer in 5 minutes!

## Prerequisites

- Go 1.21 or higher
- Python 3.7 or higher
- PostgreSQL (optional, for database features)

## Step 1: Create Your First Project (1 minute)

```bash
# Navigate to your workspace
cd ~/projects

# Initialize a new project
python /path/to/gin-developer/scripts/init_project.py my-first-api

# Navigate to project
cd my-first-api
```

## Step 2: Configure Environment (30 seconds)

```bash
# Copy environment template
cp .env.example .env

# Edit if needed (optional for quick start)
# The defaults work for local PostgreSQL
```

## Step 3: Generate a Domain (30 seconds)

```bash
# Generate a User domain with fields
python ../gin-developer/scripts/generate_domain.py user --fields "name:string,email:string,age:int"
```

## Step 4: Wire Up the Domain (1 minute)

Edit `cmd/api/main.go` and add these lines:

```go
// After the imports, add:
import (
    "github.com/myuser/my-first-api/internal/domain/entity"
    "github.com/myuser/my-first-api/internal/handler"
    "github.com/myuser/my-first-api/internal/infrastructure/repository"
    "github.com/myuser/my-first-api/internal/usecase"
)

// In the main function, after database initialization, add:
db.AutoMigrate(&entity.User{})

// In the v1 routes section, add:
userRepo := repository.NewUserRepository(db)
userUseCase := usecase.NewUserUseCase(userRepo)
userHandler := handler.NewUserHandler(userUseCase)
userHandler.RegisterRoutes(v1)
```

## Step 5: Install Dependencies (1 minute)

```bash
go mod tidy
```

## Step 6: Run Your API (30 seconds)

```bash
go run cmd/api/main.go
```

You should see:
```
Server starting on port 8080
```

## Step 7: Test Your API (1 minute)

Open a new terminal and try these commands:

### Health Check
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

### Create a User
```bash
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com","age":25}'
```

Expected response:
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

### Get All Users
```bash
curl http://localhost:8080/api/v1/users
```

### Get User by ID
```bash
curl http://localhost:8080/api/v1/users/1
```

### Update User
```bash
curl -X PUT http://localhost:8080/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Updated","email":"alice@example.com","age":26}'
```

### Delete User
```bash
curl -X DELETE http://localhost:8080/api/v1/users/1
```

## 🎉 Congratulations!

You've just created a fully functional REST API with:
- ✅ Clean DDD architecture
- ✅ Database integration
- ✅ CRUD operations
- ✅ Input validation
- ✅ Error handling
- ✅ Consistent responses

## Next Steps

### Add More Domains

```bash
# Product domain
python ../gin-developer/scripts/generate_domain.py product --fields "name:string,price:float64,stock:int"

# Order domain
python ../gin-developer/scripts/generate_domain.py order --fields "user_id:uuid,total:float64,status:string"
```

### Customize Your API

1. **Add custom business logic** in use cases
2. **Add custom queries** in repositories
3. **Add authentication** middleware
4. **Add validation rules** in handlers
5. **Add relationships** between entities

### Learn More

Check out these resources:
- `references/ddd_architecture.md` - Learn about DDD patterns
- `references/gin_best_practices.md` - Gin framework tips
- `references/gorm_examples.md` - Database operations
- `examples/complete_example.md` - Full blog API example

## Troubleshooting

### "go.mod not found"
Make sure you're in the project directory:
```bash
cd my-first-api
```

### "database connection failed"
Check your PostgreSQL is running:
```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql

# Or use Docker
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres
```

### "port already in use"
Change the port in `.env`:
```env
PORT=8081
```

### Import errors after generation
Run:
```bash
go mod tidy
```

## Tips

1. **Use meaningful domain names** - `user`, `product`, `order` instead of `thing1`, `thing2`
2. **Start simple** - Add fields as you need them
3. **Test as you go** - Use curl or Postman to test each endpoint
4. **Read the generated code** - Understand what's created
5. **Customize gradually** - Start with generated code, then customize

## Common Patterns

### Pagination
```bash
curl "http://localhost:8080/api/v1/users?limit=10&offset=0"
```

### Filtering (after customization)
```bash
curl "http://localhost:8080/api/v1/users?active=true"
```

### Sorting (after customization)
```bash
curl "http://localhost:8080/api/v1/users?sort=name&order=asc"
```

## Development Workflow

1. **Generate domain** with basic fields
2. **Run and test** basic CRUD
3. **Add custom methods** to repository
4. **Implement business logic** in use case
5. **Add custom endpoints** in handler
6. **Test thoroughly**
7. **Repeat** for next domain

Happy coding! 🚀

