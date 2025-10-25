#!/usr/bin/env python3
"""
Add middleware components to Gin project.
"""

import argparse
import sys
from pathlib import Path
from typing import List

SUPPORTED_MIDDLEWARES = [
    "cors",
    "ratelimit",
    "logging",
    "recovery",
    "timeout",
    "compression",
    "security",
    "requestid",
    "metrics",
    "validation",
]


def get_cors_middleware() -> str:
    """Get CORS middleware implementation."""
    return """package middleware

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"time"
)

// CORSConfig holds CORS configuration
type CORSConfig struct {
	AllowOrigins     []string
	AllowMethods     []string
	AllowHeaders     []string
	ExposeHeaders    []string
	AllowCredentials bool
	MaxAge           time.Duration
}

// DefaultCORSConfig returns default CORS configuration
func DefaultCORSConfig() CORSConfig {
	return CORSConfig{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: false,
		MaxAge:           12 * time.Hour,
	}
}

// CORS returns a CORS middleware with custom configuration
func CORS(config CORSConfig) gin.HandlerFunc {
	return cors.New(cors.Config{
		AllowOrigins:     config.AllowOrigins,
		AllowMethods:     config.AllowMethods,
		AllowHeaders:     config.AllowHeaders,
		ExposeHeaders:    config.ExposeHeaders,
		AllowCredentials: config.AllowCredentials,
		MaxAge:           config.MaxAge,
	})
}
"""


def get_ratelimit_middleware() -> str:
    """Get rate limiting middleware implementation."""
    return """package middleware

import (
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"golang.org/x/time/rate"
)

// RateLimitConfig holds rate limiting configuration
type RateLimitConfig struct {
	RequestsPerSecond float64
	Burst             int
	Strategy          string // "ip", "user", "global"
}

type visitor struct {
	limiter  *rate.Limiter
	lastSeen time.Time
}

var (
	visitors = make(map[string]*visitor)
	mu       sync.RWMutex
)

// RateLimit returns a rate limiting middleware
func RateLimit(config RateLimitConfig) gin.HandlerFunc {
	// Cleanup old visitors periodically
	go cleanupVisitors()

	return func(c *gin.Context) {
		var key string

		switch config.Strategy {
		case "ip":
			key = c.ClientIP()
		case "user":
			// Get user ID from context (set by auth middleware)
			if userID, exists := c.Get("user_id"); exists {
				key = userID.(string)
			} else {
				key = c.ClientIP()
			}
		case "global":
			key = "global"
		default:
			key = c.ClientIP()
		}

		limiter := getVisitor(key, config)
		if !limiter.Allow() {
			c.JSON(http.StatusTooManyRequests, gin.H{
				"error": "Rate limit exceeded",
			})
			c.Abort()
			return
		}

		c.Next()
	}
}

func getVisitor(key string, config RateLimitConfig) *rate.Limiter {
	mu.Lock()
	defer mu.Unlock()

	v, exists := visitors[key]
	if !exists {
		limiter := rate.NewLimiter(rate.Limit(config.RequestsPerSecond), config.Burst)
		visitors[key] = &visitor{limiter, time.Now()}
		return limiter
	}

	v.lastSeen = time.Now()
	return v.limiter
}

func cleanupVisitors() {
	for {
		time.Sleep(time.Minute)
		mu.Lock()
		for key, v := range visitors {
			if time.Since(v.lastSeen) > 3*time.Minute {
				delete(visitors, key)
			}
		}
		mu.Unlock()
	}
}
"""


def get_logging_middleware() -> str:
    """Get logging middleware implementation."""
    return """package middleware

import (
	"log"
	"time"

	"github.com/gin-gonic/gin"
)

// LoggingConfig holds logging configuration
type LoggingConfig struct {
	SkipPaths []string
}

// Logging returns a logging middleware
func Logging(config LoggingConfig) gin.HandlerFunc {
	skipPaths := make(map[string]bool)
	for _, path := range config.SkipPaths {
		skipPaths[path] = true
	}

	return func(c *gin.Context) {
		// Skip logging for certain paths
		if skipPaths[c.Request.URL.Path] {
			c.Next()
			return
		}

		start := time.Now()
		path := c.Request.URL.Path
		query := c.Request.URL.RawQuery

		c.Next()

		end := time.Now()
		latency := end.Sub(start)

		log.Printf("[%s] %s %s | Status: %d | Latency: %v | IP: %s | Query: %s",
			c.Request.Method,
			path,
			c.Request.Proto,
			c.Writer.Status(),
			latency,
			c.ClientIP(),
			query,
		)
	}
}
"""


def get_recovery_middleware() -> str:
    """Get recovery middleware implementation."""
    return """package middleware

import (
	"fmt"
	"log"
	"net/http"
	"runtime/debug"

	"github.com/gin-gonic/gin"
)

// Recovery returns a recovery middleware with error reporting
func Recovery() gin.HandlerFunc {
	return func(c *gin.Context) {
		defer func() {
			if err := recover(); err != nil {
				// Log the error and stack trace
				log.Printf("Panic recovered: %v\\n%s", err, debug.Stack())

				// Return error response
				c.JSON(http.StatusInternalServerError, gin.H{
					"error": "Internal server error",
					"message": fmt.Sprintf("%v", err),
				})
				c.Abort()
			}
		}()
		c.Next()
	}
}
"""


def get_timeout_middleware() -> str:
    """Get timeout middleware implementation."""
    return """package middleware

import (
	"context"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// Timeout returns a timeout middleware
func Timeout(timeout time.Duration) gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(c.Request.Context(), timeout)
		defer cancel()

		c.Request = c.Request.WithContext(ctx)

		finished := make(chan struct{})
		go func() {
			c.Next()
			finished <- struct{}{}
		}()

		select {
		case <-finished:
			return
		case <-ctx.Done():
			c.JSON(http.StatusRequestTimeout, gin.H{
				"error": "Request timeout",
			})
			c.Abort()
		}
	}
}
"""


def get_compression_middleware() -> str:
    """Get compression middleware implementation."""
    return """package middleware

import (
	"github.com/gin-contrib/gzip"
	"github.com/gin-gonic/gin"
)

// Compression returns a gzip compression middleware
func Compression() gin.HandlerFunc {
	return gzip.Gzip(gzip.DefaultCompression)
}
"""


def get_security_middleware() -> str:
    """Get security headers middleware implementation."""
    return """package middleware

import (
	"github.com/gin-gonic/gin"
)

// SecurityConfig holds security headers configuration
type SecurityConfig struct {
	ContentSecurityPolicy string
	XFrameOptions         string
	XContentTypeOptions   string
	StrictTransportSecurity string
	ReferrerPolicy        string
}

// DefaultSecurityConfig returns default security configuration
func DefaultSecurityConfig() SecurityConfig {
	return SecurityConfig{
		ContentSecurityPolicy: "default-src 'self'",
		XFrameOptions:         "DENY",
		XContentTypeOptions:   "nosniff",
		StrictTransportSecurity: "max-age=31536000; includeSubDomains",
		ReferrerPolicy:        "strict-origin-when-cross-origin",
	}
}

// Security returns a security headers middleware
func Security(config SecurityConfig) gin.HandlerFunc {
	return func(c *gin.Context) {
		if config.ContentSecurityPolicy != "" {
			c.Header("Content-Security-Policy", config.ContentSecurityPolicy)
		}
		if config.XFrameOptions != "" {
			c.Header("X-Frame-Options", config.XFrameOptions)
		}
		if config.XContentTypeOptions != "" {
			c.Header("X-Content-Type-Options", config.XContentTypeOptions)
		}
		if config.StrictTransportSecurity != "" {
			c.Header("Strict-Transport-Security", config.StrictTransportSecurity)
		}
		if config.ReferrerPolicy != "" {
			c.Header("Referrer-Policy", config.ReferrerPolicy)
		}
		c.Next()
	}
}
"""


def get_requestid_middleware() -> str:
    """Get request ID middleware implementation."""
    return """package middleware

import (
	"github.com/google/uuid"
	"github.com/gin-gonic/gin"
)

const RequestIDKey = "X-Request-ID"

// RequestID returns a request ID middleware
func RequestID() gin.HandlerFunc {
	return func(c *gin.Context) {
		requestID := c.GetHeader(RequestIDKey)
		if requestID == "" {
			requestID = uuid.New().String()
		}

		c.Set("request_id", requestID)
		c.Header(RequestIDKey, requestID)
		c.Next()
	}
}
"""


def get_metrics_middleware() -> str:
    """Get Prometheus metrics middleware implementation."""
    return """package middleware

import (
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	httpRequestsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_requests_total",
			Help: "Total number of HTTP requests",
		},
		[]string{"method", "path", "status"},
	)

	httpRequestDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "http_request_duration_seconds",
			Help:    "HTTP request duration in seconds",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"method", "path"},
	)
)

// Metrics returns a Prometheus metrics middleware
func Metrics() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		path := c.FullPath()
		if path == "" {
			path = c.Request.URL.Path
		}

		c.Next()

		duration := time.Since(start).Seconds()
		status := strconv.Itoa(c.Writer.Status())

		httpRequestsTotal.WithLabelValues(c.Request.Method, path, status).Inc()
		httpRequestDuration.WithLabelValues(c.Request.Method, path).Observe(duration)
	}
}
"""


def get_validation_middleware() -> str:
    """Get request validation middleware implementation."""
    return """package middleware

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
)

var validate *validator.Validate

func init() {
	validate = validator.New()
}

// Validation returns a request validation middleware
func Validation() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Set("validator", validate)
		c.Next()
	}
}

// ValidateStruct validates a struct and returns error response if invalid
func ValidateStruct(c *gin.Context, obj interface{}) bool {
	if err := validate.Struct(obj); err != nil {
		var errors []string
		for _, err := range err.(validator.ValidationErrors) {
			errors = append(errors, err.Error())
		}
		c.JSON(http.StatusBadRequest, gin.H{
			"error":  "Validation failed",
			"details": errors,
		})
		return false
	}
	return true
}
"""



def get_middleware_content(middleware_type: str) -> str:
    """Get middleware content by type."""
    middleware_map = {
        "cors": get_cors_middleware,
        "ratelimit": get_ratelimit_middleware,
        "logging": get_logging_middleware,
        "recovery": get_recovery_middleware,
        "timeout": get_timeout_middleware,
        "compression": get_compression_middleware,
        "security": get_security_middleware,
        "requestid": get_requestid_middleware,
        "metrics": get_metrics_middleware,
        "validation": get_validation_middleware,
    }

    func = middleware_map.get(middleware_type)
    if func:
        return func()
    return None


def get_dependencies(middleware_type: str) -> List[str]:
    """Get Go dependencies for middleware type."""
    deps = {
        "cors": ["github.com/gin-contrib/cors"],
        "ratelimit": ["golang.org/x/time/rate"],
        "compression": ["github.com/gin-contrib/gzip"],
        "requestid": ["github.com/google/uuid"],
        "metrics": [
            "github.com/prometheus/client_golang/prometheus",
            "github.com/prometheus/client_golang/prometheus/promauto",
        ],
        "validation": ["github.com/go-playground/validator/v10"],
    }
    return deps.get(middleware_type, [])


def create_middleware(project_path: Path, middleware_type: str):
    """Create middleware component."""
    print(f"\n🚀 Adding {middleware_type} middleware\n")

    # Create middleware directory
    middleware_dir = project_path / "pkg" / "middleware"
    middleware_dir.mkdir(parents=True, exist_ok=True)

    # Get content
    content = get_middleware_content(middleware_type)
    if not content:
        print(f"✗ Unsupported middleware type: {middleware_type}")
        return

    # Write middleware file
    middleware_file = middleware_dir / f"{middleware_type}.go"
    middleware_file.write_text(content)
    print(f"✓ Created middleware/{middleware_type}.go")

    # Get dependencies
    deps = get_dependencies(middleware_type)
    if deps:
        print(f"\n📦 Required dependencies:")
        for dep in deps:
            print(f"   - {dep}")
        print(f"\nRun: go get {' '.join(deps)}")

    print(f"\n✅ {middleware_type.capitalize()} middleware added successfully!")
    print(f"\nUsage example:")
    print_usage_example(middleware_type)


def print_usage_example(middleware_type: str):
    """Print usage example for the middleware."""
    examples = {
        "cors": """
// In your main.go:
import "yourproject/pkg/middleware"

func main() {
    r := gin.Default()

    // Use default CORS config
    r.Use(middleware.CORS(middleware.DefaultCORSConfig()))

    // Or custom config
    r.Use(middleware.CORS(middleware.CORSConfig{
        AllowOrigins:     []string{"https://example.com"},
        AllowMethods:     []string{"GET", "POST"},
        AllowCredentials: true,
    }))
}
""",
        "ratelimit": """
// In your main.go:
import "yourproject/pkg/middleware"

func main() {
    r := gin.Default()

    // Rate limit by IP: 10 requests per second, burst of 20
    r.Use(middleware.RateLimit(middleware.RateLimitConfig{
        RequestsPerSecond: 10,
        Burst:             20,
        Strategy:          "ip",
    }))
}
""",
        "logging": """
// In your main.go:
import "yourproject/pkg/middleware"

func main() {
    r := gin.New()

    r.Use(middleware.Logging(middleware.LoggingConfig{
        SkipPaths: []string{"/health", "/metrics"},
    }))
}
""",
        "recovery": """
// In your main.go:
import "yourproject/pkg/middleware"

func main() {
    r := gin.New()
    r.Use(middleware.Recovery())
}
""",
        "timeout": """
// In your main.go:
import (
    "time"
    "yourproject/pkg/middleware"
)

func main() {
    r := gin.Default()

    // Set 30 second timeout for all requests
    r.Use(middleware.Timeout(30 * time.Second))
}
""",
        "compression": """
// In your main.go:
import "yourproject/pkg/middleware"

func main() {
    r := gin.Default()
    r.Use(middleware.Compression())
}
""",
        "security": """
// In your main.go:
import "yourproject/pkg/middleware"

func main() {
    r := gin.Default()

    // Use default security headers
    r.Use(middleware.Security(middleware.DefaultSecurityConfig()))

    // Or custom config
    r.Use(middleware.Security(middleware.SecurityConfig{
        ContentSecurityPolicy: "default-src 'self'; script-src 'self' 'unsafe-inline'",
        XFrameOptions:         "SAMEORIGIN",
    }))
}
""",
        "requestid": """
// In your main.go:
import "yourproject/pkg/middleware"

func main() {
    r := gin.Default()
    r.Use(middleware.RequestID())

    // Access request ID in handlers
    r.GET("/", func(c *gin.Context) {
        requestID := c.GetString("request_id")
        c.JSON(200, gin.H{"request_id": requestID})
    })
}
""",
        "metrics": """
// In your main.go:
import (
    "yourproject/pkg/middleware"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
    r := gin.Default()
    r.Use(middleware.Metrics())

    // Expose metrics endpoint
    r.GET("/metrics", gin.WrapH(promhttp.Handler()))
}
""",
        "validation": """
// In your main.go:
import "yourproject/pkg/middleware"

func main() {
    r := gin.Default()
    r.Use(middleware.Validation())
}

// In your handler:
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required,min=3"`
    Email string `json:"email" validate:"required,email"`
}

func CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }

    if !middleware.ValidateStruct(c, req) {
        return
    }

    // Process request...
}
""",
    }

    print(examples.get(middleware_type, "No example available"))


def main():
    parser = argparse.ArgumentParser(description="Add middleware to Gin project")
    parser.add_argument("--type", required=True, choices=SUPPORTED_MIDDLEWARES,
                        help="Middleware type")
    parser.add_argument("--project-path", default=".", help="Path to project root")

    args = parser.parse_args()

    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)

    # Check if it's a Go project
    if not (project_path / "go.mod").exists():
        print(f"✗ Error: Not a Go project (go.mod not found)")
        sys.exit(1)

    create_middleware(project_path, args.type)


if __name__ == "__main__":
    main()


