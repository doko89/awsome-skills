# Complete Example: Building a Blog API

This example demonstrates building a complete blog API with users, posts, and comments using the gin-developer skill.

## Step 1: Initialize Project

```bash
python ~/.claude/skills/gin-developer/scripts/init_project.py blog-api
cd blog-api
```

## Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
PORT=8080
GIN_MODE=debug

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=blog_db
DB_SSLMODE=disable

CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Step 3: Generate Domains

### Generate User Domain

```bash
python ~/.claude/skills/gin-developer/scripts/generate_domain.py user --fields "username:string,email:string,password:string,bio:string,avatar:string,active:bool"
```

### Generate Post Domain

```bash
python ~/.claude/skills/gin-developer/scripts/generate_domain.py post --fields "title:string,content:string,slug:string,published:bool,user_id:uuid,views:int"
```

### Generate Comment Domain

```bash
python ~/.claude/skills/gin-developer/scripts/generate_domain.py comment --fields "content:string,post_id:uuid,user_id:uuid,approved:bool"
```

### Generate Category Domain

```bash
python ~/.claude/skills/gin-developer/scripts/generate_domain.py category --fields "name:string,slug:string,description:string"
```

## Step 4: Update Main File

Edit `cmd/api/main.go`:

```go
package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"blog-api/internal/domain/entity"
	"blog-api/internal/handler"
	"blog-api/internal/infrastructure/config"
	"blog-api/internal/infrastructure/database"
	"blog-api/internal/infrastructure/repository"
	"blog-api/internal/usecase"
	"blog-api/pkg/middleware"
)

func main() {
	// Load environment variables
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found")
	}

	// Load configuration
	cfg := config.Load()

	// Initialize database
	db, err := database.NewPostgresDB(cfg.Database)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	// Auto migrate
	if err := db.AutoMigrate(
		&entity.User{},
		&entity.Post{},
		&entity.Comment{},
		&entity.Category{},
	); err != nil {
		log.Fatalf("Failed to migrate database: %v", err)
	}

	// Set Gin mode
	gin.SetMode(cfg.Server.Mode)

	// Initialize router
	router := gin.New()

	// Apply middleware
	router.Use(gin.Logger())
	router.Use(gin.Recovery())
	router.Use(middleware.CORS(cfg.CORS))

	// Health check
	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status": "ok",
			"message": "Blog API is running",
		})
	})

	// API v1 routes
	v1 := router.Group("/api/v1")
	{
		// User routes
		userRepo := repository.NewUserRepository(db)
		userUseCase := usecase.NewUserUseCase(userRepo)
		userHandler := handler.NewUserHandler(userUseCase)
		userHandler.RegisterRoutes(v1)

		// Post routes
		postRepo := repository.NewPostRepository(db)
		postUseCase := usecase.NewPostUseCase(postRepo)
		postHandler := handler.NewPostHandler(postUseCase)
		postHandler.RegisterRoutes(v1)

		// Comment routes
		commentRepo := repository.NewCommentRepository(db)
		commentUseCase := usecase.NewCommentUseCase(commentRepo)
		commentHandler := handler.NewCommentHandler(commentUseCase)
		commentHandler.RegisterRoutes(v1)

		// Category routes
		categoryRepo := repository.NewCategoryRepository(db)
		categoryUseCase := usecase.NewCategoryUseCase(categoryRepo)
		categoryHandler := handler.NewCategoryHandler(categoryUseCase)
		categoryHandler.RegisterRoutes(v1)
	}

	// Start server
	port := cfg.Server.Port
	if port == "" {
		port = "8080"
	}

	log.Printf("🚀 Blog API starting on port %s", port)
	if err := router.Run(":" + port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
```

## Step 5: Install Dependencies

```bash
go mod tidy
```

## Step 6: Run the Application

```bash
go run cmd/api/main.go
```

## Step 7: Test the API

### Create a User

```bash
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "secret123",
    "bio": "Software developer",
    "active": true
  }'
```

### Create a Category

```bash
curl -X POST http://localhost:8080/api/v1/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technology",
    "slug": "technology",
    "description": "Tech articles and tutorials"
  }'
```

### Create a Post

```bash
curl -X POST http://localhost:8080/api/v1/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with Go",
    "content": "Go is an amazing programming language...",
    "slug": "getting-started-with-go",
    "published": true,
    "user_id": "00000000-0000-0000-0000-000000000001",
    "views": 0
  }'
```

### Create a Comment

```bash
curl -X POST http://localhost:8080/api/v1/comments \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great article! Very helpful.",
    "post_id": "00000000-0000-0000-0000-000000000001",
    "user_id": "00000000-0000-0000-0000-000000000001",
    "approved": true
  }'
```

### Get All Posts

```bash
curl http://localhost:8080/api/v1/posts
```

### Get Post by ID

```bash
curl http://localhost:8080/api/v1/posts/1
```

### Update Post

```bash
curl -X PUT http://localhost:8080/api/v1/posts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with Go - Updated",
    "content": "Go is an amazing programming language... (updated)",
    "slug": "getting-started-with-go",
    "published": true,
    "user_id": "00000000-0000-0000-0000-000000000001",
    "views": 100
  }'
```

### Delete Post

```bash
curl -X DELETE http://localhost:8080/api/v1/posts/1
```

### Pagination

```bash
curl "http://localhost:8080/api/v1/posts?limit=10&offset=0"
```

## Step 8: Customize Business Logic

### Add Custom Method to Post Entity

Edit `internal/domain/entity/post.go`:

```go
func (p *Post) IncrementViews() {
    p.Views++
}

func (p *Post) IsPublished() bool {
    return p.Published
}

func (p *Post) GenerateSlug() {
    // Convert title to slug
    p.Slug = strings.ToLower(strings.ReplaceAll(p.Title, " ", "-"))
}
```

### Add Custom Repository Method

Edit `internal/domain/repository/post_repository.go`:

```go
type PostRepository interface {
    Create(e *entity.Post) error
    FindByID(id uint) (*entity.Post, error)
    FindAll(limit, offset int) ([]*entity.Post, error)
    Update(e *entity.Post) error
    Delete(id uint) error
    Count() (int64, error)
    
    // Custom methods
    FindBySlug(slug string) (*entity.Post, error)
    FindPublished(limit, offset int) ([]*entity.Post, error)
    FindByUserID(userID uuid.UUID, limit, offset int) ([]*entity.Post, error)
}
```

Edit `internal/infrastructure/repository/post_repository.go`:

```go
func (r *postrepository) FindBySlug(slug string) (*entity.Post, error) {
    var post entity.Post
    if err := r.db.Where("slug = ?", slug).First(&post).Error; err != nil {
        return nil, err
    }
    return &post, nil
}

func (r *postrepository) FindPublished(limit, offset int) ([]*entity.Post, error) {
    var posts []*entity.Post
    query := r.db.Model(&entity.Post{}).Where("published = ?", true)
    
    if limit > 0 {
        query = query.Limit(limit)
    }
    if offset > 0 {
        query = query.Offset(offset)
    }
    
    if err := query.Find(&posts).Error; err != nil {
        return nil, err
    }
    return posts, nil
}

func (r *postrepository) FindByUserID(userID uuid.UUID, limit, offset int) ([]*entity.Post, error) {
    var posts []*entity.Post
    query := r.db.Model(&entity.Post{}).Where("user_id = ?", userID)
    
    if limit > 0 {
        query = query.Limit(limit)
    }
    if offset > 0 {
        query = query.Offset(offset)
    }
    
    if err := query.Find(&posts).Error; err != nil {
        return nil, err
    }
    return posts, nil
}
```

### Add Custom Use Case Methods

Edit `internal/usecase/post_usecase.go`:

```go
func (u *postUseCase) GetBySlug(slug string) (*entity.Post, error) {
    post, err := u.repo.FindBySlug(slug)
    if err != nil {
        return nil, fmt.Errorf("failed to get post by slug: %w", err)
    }
    
    // Increment views
    post.IncrementViews()
    u.repo.Update(post)
    
    return post, nil
}

func (u *postUseCase) GetPublished(limit, offset int) ([]*entity.Post, error) {
    posts, err := u.repo.FindPublished(limit, offset)
    if err != nil {
        return nil, fmt.Errorf("failed to get published posts: %w", err)
    }
    return posts, nil
}
```

### Add Custom Handler Endpoints

Edit `internal/handler/post_handler.go`:

```go
func (h *PostHandler) RegisterRoutes(router *gin.RouterGroup) {
    posts := router.Group("/posts")
    {
        posts.POST("", h.Create)
        posts.GET("", h.GetAll)
        posts.GET("/published", h.GetPublished)  // New endpoint
        posts.GET("/:id", h.GetByID)
        posts.GET("/slug/:slug", h.GetBySlug)    // New endpoint
        posts.PUT("/:id", h.Update)
        posts.DELETE("/:id", h.Delete)
    }
}

func (h *PostHandler) GetBySlug(c *gin.Context) {
    slug := c.Param("slug")
    
    post, err := h.useCase.GetBySlug(slug)
    if err != nil {
        response.Error(c, http.StatusNotFound, "Post not found", err)
        return
    }
    
    response.Success(c, http.StatusOK, "Post retrieved successfully", post)
}

func (h *PostHandler) GetPublished(c *gin.Context) {
    limit, _ := strconv.Atoi(c.DefaultQuery("limit", "10"))
    offset, _ := strconv.Atoi(c.DefaultQuery("offset", "0"))
    
    posts, err := h.useCase.GetPublished(limit, offset)
    if err != nil {
        response.Error(c, http.StatusInternalServerError, "Failed to get posts", err)
        return
    }
    
    response.Success(c, http.StatusOK, "Posts retrieved successfully", gin.H{
        "items": posts,
        "limit": limit,
        "offset": offset,
    })
}
```

## API Endpoints Summary

### Users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/:id` - Get user by ID
- `PUT /api/v1/users/:id` - Update user
- `DELETE /api/v1/users/:id` - Delete user

### Posts
- `POST /api/v1/posts` - Create post
- `GET /api/v1/posts` - Get all posts
- `GET /api/v1/posts/published` - Get published posts
- `GET /api/v1/posts/:id` - Get post by ID
- `GET /api/v1/posts/slug/:slug` - Get post by slug
- `PUT /api/v1/posts/:id` - Update post
- `DELETE /api/v1/posts/:id` - Delete post

### Comments
- `POST /api/v1/comments` - Create comment
- `GET /api/v1/comments` - Get all comments
- `GET /api/v1/comments/:id` - Get comment by ID
- `PUT /api/v1/comments/:id` - Update comment
- `DELETE /api/v1/comments/:id` - Delete comment

### Categories
- `POST /api/v1/categories` - Create category
- `GET /api/v1/categories` - Get all categories
- `GET /api/v1/categories/:id` - Get category by ID
- `PUT /api/v1/categories/:id` - Update category
- `DELETE /api/v1/categories/:id` - Delete category

## Next Steps

1. **Add Authentication** - Implement JWT authentication middleware
2. **Add Authorization** - Role-based access control
3. **Add Relationships** - Preload related data (user, comments)
4. **Add Search** - Full-text search for posts
5. **Add Caching** - Redis caching for frequently accessed data
6. **Add Tests** - Unit and integration tests
7. **Add Documentation** - Swagger/OpenAPI documentation
8. **Add Logging** - Structured logging with context
9. **Add Monitoring** - Prometheus metrics
10. **Deploy** - Docker containerization and deployment

This example demonstrates the power of the gin-developer skill for rapid API development with clean architecture!

