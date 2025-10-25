# Gin Framework Best Practices

## Overview

This guide covers best practices for building web applications with the Gin framework in Go.

## Project Setup

### 1. Use Gin v1.11.0 or Later

```bash
go get -u github.com/gin-gonic/gin@v1.11.0
```

### 2. Set Gin Mode

```go
// In production
gin.SetMode(gin.ReleaseMode)

// In development
gin.SetMode(gin.DebugMode)

// In testing
gin.SetMode(gin.TestMode)
```

### 3. Use Environment Variables

```go
import "github.com/joho/godotenv"

func main() {
    godotenv.Load()
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
}
```

---

## Router Configuration

### 1. Use Router Groups

```go
router := gin.Default()

// API v1
v1 := router.Group("/api/v1")
{
    users := v1.Group("/users")
    {
        users.GET("", userHandler.GetAll)
        users.POST("", userHandler.Create)
        users.GET("/:id", userHandler.GetByID)
        users.PUT("/:id", userHandler.Update)
        users.DELETE("/:id", userHandler.Delete)
    }
    
    products := v1.Group("/products")
    {
        products.GET("", productHandler.GetAll)
        products.POST("", productHandler.Create)
    }
}

// API v2
v2 := router.Group("/api/v2")
{
    // New version endpoints
}
```

### 2. Apply Middleware Selectively

```go
// Global middleware
router.Use(gin.Logger())
router.Use(gin.Recovery())
router.Use(middleware.CORS())

// Group-specific middleware
authorized := router.Group("/admin")
authorized.Use(middleware.AuthRequired())
{
    authorized.GET("/dashboard", adminHandler.Dashboard)
}

// Route-specific middleware
router.GET("/special", middleware.RateLimit(), specialHandler.Handle)
```

---

## Request Handling

### 1. Use Binding and Validation

```go
type CreateUserRequest struct {
    Name     string `json:"name" binding:"required,min=3,max=50"`
    Email    string `json:"email" binding:"required,email"`
    Age      int    `json:"age" binding:"required,gte=18,lte=120"`
    Password string `json:"password" binding:"required,min=8"`
}

func (h *UserHandler) Create(c *gin.Context) {
    var req CreateUserRequest
    
    // ShouldBindJSON validates automatically
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{
            "error": err.Error(),
        })
        return
    }
    
    // Process valid request
}
```

### 2. Handle Different Content Types

```go
// JSON
func (h *Handler) HandleJSON(c *gin.Context) {
    var req Request
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
}

// Form data
func (h *Handler) HandleForm(c *gin.Context) {
    var req Request
    if err := c.ShouldBind(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
}

// Query parameters
func (h *Handler) HandleQuery(c *gin.Context) {
    page := c.DefaultQuery("page", "1")
    limit := c.DefaultQuery("limit", "10")
}

// URL parameters
func (h *Handler) HandleParam(c *gin.Context) {
    id := c.Param("id")
}

// Headers
func (h *Handler) HandleHeader(c *gin.Context) {
    token := c.GetHeader("Authorization")
}
```

### 3. Use Custom Validators

```go
import "github.com/go-playground/validator/v10"

// Custom validation function
func validateUsername(fl validator.FieldLevel) bool {
    username := fl.Field().String()
    // Only alphanumeric and underscore
    matched, _ := regexp.MatchString("^[a-zA-Z0-9_]+$", username)
    return matched
}

// Register custom validator
if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
    v.RegisterValidation("username", validateUsername)
}

// Use in struct
type User struct {
    Username string `json:"username" binding:"required,username"`
}
```

---

## Response Handling

### 1. Consistent Response Format

```go
type Response struct {
    Success bool        `json:"success"`
    Message string      `json:"message,omitempty"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
}

func Success(c *gin.Context, code int, message string, data interface{}) {
    c.JSON(code, Response{
        Success: true,
        Message: message,
        Data:    data,
    })
}

func Error(c *gin.Context, code int, message string, err error) {
    c.JSON(code, Response{
        Success: false,
        Message: message,
        Error:   err.Error(),
    })
}
```

### 2. Use Appropriate Status Codes

```go
// Success responses
c.JSON(http.StatusOK, data)           // 200 - GET, PUT, PATCH
c.JSON(http.StatusCreated, data)      // 201 - POST
c.JSON(http.StatusNoContent, nil)     // 204 - DELETE

// Client error responses
c.JSON(http.StatusBadRequest, err)         // 400 - Invalid input
c.JSON(http.StatusUnauthorized, err)       // 401 - Not authenticated
c.JSON(http.StatusForbidden, err)          // 403 - Not authorized
c.JSON(http.StatusNotFound, err)           // 404 - Resource not found
c.JSON(http.StatusConflict, err)           // 409 - Conflict (duplicate)
c.JSON(http.StatusUnprocessableEntity, err) // 422 - Validation error

// Server error responses
c.JSON(http.StatusInternalServerError, err) // 500 - Server error
c.JSON(http.StatusServiceUnavailable, err)  // 503 - Service unavailable
```

### 3. Handle Pagination

```go
type PaginatedResponse struct {
    Items  interface{} `json:"items"`
    Total  int64       `json:"total"`
    Page   int         `json:"page"`
    Limit  int         `json:"limit"`
    Pages  int         `json:"pages"`
}

func (h *Handler) GetAll(c *gin.Context) {
    page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
    limit, _ := strconv.Atoi(c.DefaultQuery("limit", "10"))
    
    items, total, err := h.useCase.GetAll(limit, (page-1)*limit)
    if err != nil {
        c.JSON(500, gin.H{"error": err.Error()})
        return
    }
    
    pages := int(math.Ceil(float64(total) / float64(limit)))
    
    c.JSON(200, PaginatedResponse{
        Items: items,
        Total: total,
        Page:  page,
        Limit: limit,
        Pages: pages,
    })
}
```

---

## Middleware

### 1. CORS Middleware

```go
func CORS() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
        c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
        c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
        c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        
        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(204)
            return
        }
        
        c.Next()
    }
}
```

### 2. Authentication Middleware

```go
func AuthRequired() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        
        if token == "" {
            c.JSON(401, gin.H{"error": "Authorization header required"})
            c.Abort()
            return
        }
        
        // Validate token
        claims, err := validateToken(token)
        if err != nil {
            c.JSON(401, gin.H{"error": "Invalid token"})
            c.Abort()
            return
        }
        
        // Set user info in context
        c.Set("user_id", claims.UserID)
        c.Next()
    }
}
```

### 3. Rate Limiting Middleware

```go
import "golang.org/x/time/rate"

func RateLimit(r rate.Limit, b int) gin.HandlerFunc {
    limiter := rate.NewLimiter(r, b)
    
    return func(c *gin.Context) {
        if !limiter.Allow() {
            c.JSON(429, gin.H{"error": "Too many requests"})
            c.Abort()
            return
        }
        c.Next()
    }
}

// Usage: 10 requests per second, burst of 20
router.Use(RateLimit(10, 20))
```

### 4. Request ID Middleware

```go
import "github.com/google/uuid"

func RequestID() gin.HandlerFunc {
    return func(c *gin.Context) {
        requestID := c.GetHeader("X-Request-ID")
        if requestID == "" {
            requestID = uuid.New().String()
        }
        
        c.Set("request_id", requestID)
        c.Writer.Header().Set("X-Request-ID", requestID)
        c.Next()
    }
}
```

### 5. Logging Middleware

```go
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path
        
        c.Next()
        
        duration := time.Since(start)
        statusCode := c.Writer.Status()
        
        log.Printf("[%s] %s %s %d %v",
            c.Request.Method,
            path,
            c.ClientIP(),
            statusCode,
            duration,
        )
    }
}
```

---

## Error Handling

### 1. Custom Error Types

```go
type AppError struct {
    Code    int
    Message string
    Err     error
}

func (e *AppError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}

var (
    ErrNotFound     = &AppError{Code: 404, Message: "Resource not found"}
    ErrUnauthorized = &AppError{Code: 401, Message: "Unauthorized"}
    ErrBadRequest   = &AppError{Code: 400, Message: "Bad request"}
)
```

### 2. Error Handler Middleware

```go
func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()
        
        if len(c.Errors) > 0 {
            err := c.Errors.Last()
            
            if appErr, ok := err.Err.(*AppError); ok {
                c.JSON(appErr.Code, gin.H{
                    "error": appErr.Message,
                })
                return
            }
            
            c.JSON(500, gin.H{
                "error": "Internal server error",
            })
        }
    }
}
```

---

## Testing

### 1. Test HTTP Handlers

```go
func TestUserHandler_Create(t *testing.T) {
    gin.SetMode(gin.TestMode)
    
    // Setup
    mockUseCase := &MockUserUseCase{}
    handler := NewUserHandler(mockUseCase)
    
    router := gin.New()
    router.POST("/users", handler.Create)
    
    // Test data
    user := &entity.User{Name: "John", Email: "john@example.com"}
    mockUseCase.On("Create", user).Return(nil)
    
    // Request
    body, _ := json.Marshal(user)
    req := httptest.NewRequest("POST", "/users", bytes.NewBuffer(body))
    req.Header.Set("Content-Type", "application/json")
    
    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)
    
    // Assert
    assert.Equal(t, 201, w.Code)
}
```

### 2. Test Middleware

```go
func TestAuthMiddleware(t *testing.T) {
    gin.SetMode(gin.TestMode)
    
    router := gin.New()
    router.Use(AuthRequired())
    router.GET("/protected", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "success"})
    })
    
    // Test without token
    req := httptest.NewRequest("GET", "/protected", nil)
    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)
    assert.Equal(t, 401, w.Code)
    
    // Test with valid token
    req = httptest.NewRequest("GET", "/protected", nil)
    req.Header.Set("Authorization", "valid-token")
    w = httptest.NewRecorder()
    router.ServeHTTP(w, req)
    assert.Equal(t, 200, w.Code)
}
```

---

## Performance Tips

### 1. Use Connection Pooling

```go
db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
sqlDB, _ := db.DB()
sqlDB.SetMaxIdleConns(10)
sqlDB.SetMaxOpenConns(100)
sqlDB.SetConnMaxLifetime(time.Hour)
```

### 2. Enable Gzip Compression

```go
import "github.com/gin-contrib/gzip"

router.Use(gzip.Gzip(gzip.DefaultCompression))
```

### 3. Use Context Timeout

```go
func (h *Handler) Handle(c *gin.Context) {
    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()
    
    result, err := h.service.DoWork(ctx)
    if err != nil {
        c.JSON(500, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(200, result)
}
```

---

## Security Best Practices

### 1. Validate All Input
### 2. Use HTTPS in Production
### 3. Implement Rate Limiting
### 4. Sanitize User Input
### 5. Use Secure Headers

```go
func SecureHeaders() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Header("X-Frame-Options", "DENY")
        c.Header("X-Content-Type-Options", "nosniff")
        c.Header("X-XSS-Protection", "1; mode=block")
        c.Header("Strict-Transport-Security", "max-age=31536000")
        c.Next()
    }
}
```

---

## References

- [Gin Documentation](https://gin-gonic.com/docs/)
- [Go Validator](https://github.com/go-playground/validator)
- [GORM Documentation](https://gorm.io/docs/)

