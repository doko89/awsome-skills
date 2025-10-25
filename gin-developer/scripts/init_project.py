#!/usr/bin/env python3
"""
Initialize a new Gin project with DDD architecture.

Usage:
    python ~/.claude/skills/gin-developer/scripts/init_project.py <project-name> [--module-path <module-path>]

Example:
    python ~/.claude/skills/gin-developer/scripts/init_project.py my-api --module-path github.com/myuser/my-api
"""

import os
import sys
import argparse
from pathlib import Path


def create_directory_structure(project_path: Path):
    """Create the DDD directory structure."""
    directories = [
        "cmd/api",
        "internal/domain/entity",
        "internal/domain/repository",
        "internal/usecase",
        "internal/handler",
        "internal/infrastructure/repository",
        "internal/infrastructure/database",
        "internal/infrastructure/config",
        "pkg/middleware",
        "pkg/response",
        "pkg/validator",
        "scripts",
    ]
    
    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def create_go_mod(project_path: Path, module_path: str):
    """Create go.mod file."""
    content = f"""module {module_path}

go 1.21

require (
	github.com/gin-gonic/gin v1.11.0
	gorm.io/gorm v1.25.12
	gorm.io/driver/postgres v1.5.11
	github.com/joho/godotenv v1.5.1
	github.com/google/uuid v1.6.0
	github.com/go-playground/validator/v10 v10.23.0
)
"""
    
    file_path = project_path / "go.mod"
    file_path.write_text(content)
    print(f"✓ Created go.mod")


def create_main_file(project_path: Path, module_path: str):
    """Create main.go file."""
    content = f"""package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"{module_path}/internal/infrastructure/config"
	"{module_path}/internal/infrastructure/database"
	"{module_path}/pkg/middleware"
)

func main() {{
	// Load environment variables
	if err := godotenv.Load(); err != nil {{
		log.Println("No .env file found, using system environment variables")
	}}

	// Load configuration
	cfg := config.Load()

	// Initialize database
	db, err := database.NewPostgresDB(cfg.Database)
	if err != nil {{
		log.Fatalf("Failed to connect to database: %v", err)
	}}

	// Auto migrate all entities
	if err := database.AutoMigrateAll(db); err != nil {{
		log.Fatalf("Failed to migrate database: %v", err)
	}}

	// Set Gin mode
	gin.SetMode(cfg.Server.Mode)

	// Initialize router
	router := gin.New()

	// Apply middleware
	router.Use(gin.Logger())
	router.Use(gin.Recovery())
	router.Use(middleware.CORS(cfg.CORS))

	// Health check endpoint
	router.GET("/health", func(c *gin.Context) {{
		c.JSON(200, gin.H{{
			"status": "ok",
			"message": "Server is running",
		}})
	}})

	// API v1 routes
	v1 := router.Group("/api/v1")
	{{
		// Register your routes here
		// Example:
		// userRepo := repository.NewUserRepository(db)
		// userUseCase := usecase.NewUserUseCase(userRepo)
		// userHandler := handler.NewUserHandler(userUseCase)
		// userHandler.RegisterRoutes(v1)
	}}

	// Start server
	port := cfg.Server.Port
	if port == "" {{
		port = "8080"
	}}

	log.Printf("Server starting on port %s", port)
	if err := router.Run(":" + port); err != nil {{
		log.Fatalf("Failed to start server: %v", err)
	}}
}}
"""
    
    file_path = project_path / "cmd/api/main.go"
    file_path.write_text(content)
    print(f"✓ Created cmd/api/main.go")


def create_config_file(project_path: Path):
    """Create config.go file."""
    content = """package config

import (
	"os"
)

type Config struct {
	Server   ServerConfig
	Database DatabaseConfig
	CORS     CORSConfig
}

type ServerConfig struct {
	Port string
	Mode string
}

type DatabaseConfig struct {
	Host     string
	Port     string
	User     string
	Password string
	DBName   string
	SSLMode  string
}

type CORSConfig struct {
	AllowedOrigins []string
}

func Load() *Config {
	return &Config{
		Server: ServerConfig{
			Port: getEnv("PORT", "8080"),
			Mode: getEnv("GIN_MODE", "debug"),
		},
		Database: DatabaseConfig{
			Host:     getEnv("DB_HOST", "localhost"),
			Port:     getEnv("DB_PORT", "5432"),
			User:     getEnv("DB_USER", "postgres"),
			Password: getEnv("DB_PASSWORD", "postgres"),
			DBName:   getEnv("DB_NAME", "mydb"),
			SSLMode:  getEnv("DB_SSLMODE", "disable"),
		},
		CORS: CORSConfig{
			AllowedOrigins: []string{getEnv("CORS_ALLOWED_ORIGINS", "*")},
		},
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
"""
    
    file_path = project_path / "internal/infrastructure/config/config.go"
    file_path.write_text(content)
    print(f"✓ Created config/config.go")


def create_database_file(project_path: Path):
    """Create database.go file."""
    content = """package database

import (
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

type DatabaseConfig struct {
	Host     string
	Port     string
	User     string
	Password string
	DBName   string
	SSLMode  string
}

func NewPostgresDB(cfg DatabaseConfig) (*gorm.DB, error) {
	dsn := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		cfg.Host, cfg.Port, cfg.User, cfg.Password, cfg.DBName, cfg.SSLMode,
	)

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}

	return db, nil
}

// AutoMigrateAll migrates all registered entities
// Add your entities here when you generate new domains
func AutoMigrateAll(db *gorm.DB) error {
	// Example:
	// return db.AutoMigrate(
	//     &entity.User{},
	//     &entity.Product{},
	// )

	// No entities yet
	return nil
}
"""

    file_path = project_path / "internal/infrastructure/database/database.go"
    file_path.write_text(content)
    print(f"✓ Created database/database.go")


def create_middleware_files(project_path: Path):
    """Create middleware files."""
    cors_content = """package middleware

import (
	"github.com/gin-gonic/gin"
)

type CORSConfig struct {
	AllowedOrigins []string
}

func CORS(cfg CORSConfig) gin.HandlerFunc {
	return func(c *gin.Context) {
		origin := c.Request.Header.Get("Origin")
		
		// Check if origin is allowed
		allowed := false
		for _, allowedOrigin := range cfg.AllowedOrigins {
			if allowedOrigin == "*" || allowedOrigin == origin {
				allowed = true
				break
			}
		}

		if allowed {
			if origin != "" {
				c.Writer.Header().Set("Access-Control-Allow-Origin", origin)
			} else {
				c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
			}
			c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
			c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
			c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE, PATCH")
		}

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}
"""
    
    file_path = project_path / "pkg/middleware/cors.go"
    file_path.write_text(cors_content)
    print(f"✓ Created middleware/cors.go")


def create_response_helper(project_path: Path):
    """Create response helper."""
    content = """package response

import (
	"github.com/gin-gonic/gin"
)

type Response struct {
	Success bool        `json:"success"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

func Success(c *gin.Context, statusCode int, message string, data interface{}) {
	c.JSON(statusCode, Response{
		Success: true,
		Message: message,
		Data:    data,
	})
}

func Error(c *gin.Context, statusCode int, message string, err error) {
	errorMsg := ""
	if err != nil {
		errorMsg = err.Error()
	}
	
	c.JSON(statusCode, Response{
		Success: false,
		Message: message,
		Error:   errorMsg,
	})
}
"""
    
    file_path = project_path / "pkg/response/response.go"
    file_path.write_text(content)
    print(f"✓ Created response/response.go")


def create_env_file(project_path: Path):
    """Create .env.example file."""
    content = """# Server Configuration
PORT=8080
GIN_MODE=debug

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=mydb
DB_SSLMODE=disable

# CORS Configuration
CORS_ALLOWED_ORIGINS=*
"""
    
    file_path = project_path / ".env.example"
    file_path.write_text(content)
    print(f"✓ Created .env.example")


def create_gitignore(project_path: Path):
    """Create .gitignore file."""
    content = """# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib
bin/
dist/

# Test binary
*.test

# Output of the go coverage tool
*.out

# Dependency directories
vendor/

# Go workspace file
go.work

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""
    
    file_path = project_path / ".gitignore"
    file_path.write_text(content)
    print(f"✓ Created .gitignore")


def create_readme(project_path: Path, project_name: str, module_path: str):
    """Create README.md file."""
    content = f"""# {project_name}

A Go web application built with Gin framework and Domain-Driven Design (DDD) architecture.

## Project Structure

```
{project_name}/
├── cmd/api/              # Application entry point
├── internal/
│   ├── domain/          # Domain layer (entities, interfaces)
│   ├── usecase/         # Application layer (business logic)
│   ├── handler/         # Interface layer (HTTP handlers)
│   └── infrastructure/  # Infrastructure layer (implementations)
├── pkg/                 # Shared packages
└── scripts/             # Utility scripts
```

## Getting Started

### Prerequisites

- Go 1.21 or higher
- PostgreSQL

### Installation

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your environment variables
3. Install dependencies:

```bash
go mod download
```

### Running the Application

```bash
go run cmd/api/main.go
```

The server will start on `http://localhost:8080`

### Health Check

```bash
curl http://localhost:8080/health
```

## Development

### Generate New Domain

Use the generation script to create new domain components:

```bash
python ~/.claude/skills/gin-developer/scripts/generate_domain.py <domain-name> --fields "field1:type1,field2:type2"
```

### Running Tests

```bash
go test ./...
```

## API Documentation

API endpoints will be available at `/api/v1/*`

## License

MIT
"""
    
    file_path = project_path / "README.md"
    file_path.write_text(content)
    print(f"✓ Created README.md")


def main():
    parser = argparse.ArgumentParser(description="Initialize a new Gin project with DDD architecture")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--module-path", help="Go module path (e.g., github.com/user/project)", default="")
    
    args = parser.parse_args()
    
    project_name = args.project_name
    module_path = args.module_path if args.module_path else project_name
    
    # Create project directory
    project_path = Path(project_name)
    if project_path.exists():
        print(f"Error: Directory '{project_name}' already exists")
        sys.exit(1)
    
    project_path.mkdir()
    print(f"\n🚀 Initializing project: {project_name}")
    print(f"📦 Module path: {module_path}\n")
    
    # Create all files and directories
    create_directory_structure(project_path)
    create_go_mod(project_path, module_path)
    create_main_file(project_path, module_path)
    create_config_file(project_path)
    create_database_file(project_path)
    create_middleware_files(project_path)
    create_response_helper(project_path)
    create_env_file(project_path)
    create_gitignore(project_path)
    create_readme(project_path, project_name, module_path)
    
    print(f"\n✅ Project '{project_name}' initialized successfully!")
    print(f"\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. cp .env.example .env")
    print(f"  3. Edit .env with your configuration")
    print(f"  4. go mod tidy")
    print(f"  5. go run cmd/api/main.go")
    print(f"\nTo generate a domain:")
    print(f"  python ~/.claude/skills/gin-developer/scripts/generate_domain.py <domain-name> --fields \"field1:type1,field2:type2\"")


if __name__ == "__main__":
    main()

