#!/usr/bin/env python3
"""
Add JWT authentication to your Gin project.
Supports local (credentials), Google OAuth, or both.
"""

import argparse
import sys
from pathlib import Path


def create_auth_domain(project_path: Path, module_path: str, provider: str):
    """Create auth domain with user entity and authentication logic."""
    
    # Create user entity
    password_field = "" if provider == "google" else 'Password  string    `gorm:"" json:"-"`'

    user_entity = f"""package entity

import (
	"time"
	"golang.org/x/crypto/bcrypt"
)

type User struct {{
	ID         uint      `gorm:"primaryKey" json:"id"`
	Email      string    `gorm:"uniqueIndex;not null" json:"email"`
	{password_field}
	Name       string    `gorm:"not null" json:"name"`
	AvatarURL  string    `gorm:"" json:"avatar_url"`
	Provider   string    `gorm:"default:'local'" json:"provider"` // local, google
	ProviderID string    `gorm:"" json:"provider_id"`
	Role       string    `gorm:"default:'user'" json:"role"`
	IsActive   bool      `gorm:"default:true" json:"is_active"`
	CreatedAt  time.Time `json:"created_at"`
	UpdatedAt  time.Time `json:"updated_at"`
}}

// HashPassword hashes the user password
func (u *User) HashPassword(password string) error {{
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {{
		return err
	}}
	u.Password = string(hashedPassword)
	return nil
}}

// CheckPassword checks if the provided password is correct
func (u *User) CheckPassword(password string) bool {{
	err := bcrypt.CompareHashAndPassword([]byte(u.Password), []byte(password))
	return err == nil
}}
"""
    
    entity_dir = project_path / "internal" / "domain" / "auth" / "entity"
    entity_dir.mkdir(parents=True, exist_ok=True)
    
    entity_file = entity_dir / "user.go"
    entity_file.write_text(user_entity)
    print(f"✓ Created {entity_file.relative_to(project_path)}")
    
    # Create auth DTOs
    dto_content = """package dto

type RegisterRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required,min=8"`
	Name     string `json:"name" binding:"required"`
}

type LoginRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}

type GoogleAuthRequest struct {
	IDToken string `json:"id_token" binding:"required"`
}

type GoogleUserInfo struct {
	Sub           string `json:"sub"`
	Email         string `json:"email"`
	EmailVerified bool   `json:"email_verified"`
	Name          string `json:"name"`
	Picture       string `json:"picture"`
}

type LoginResponse struct {
	Token string       `json:"token"`
	User  UserResponse `json:"user"`
}

type UserResponse struct {
	ID        uint   `json:"id"`
	Email     string `json:"email"`
	Name      string `json:"name"`
	AvatarURL string `json:"avatar_url"`
	Provider  string `json:"provider"`
	Role      string `json:"role"`
	IsActive  bool   `json:"is_active"`
}

type UploadAvatarResponse struct {
	AvatarURL string `json:"avatar_url"`
}
"""

    dto = dto_content
    
    dto_dir = project_path / "internal" / "domain" / "auth" / "dto"
    dto_dir.mkdir(parents=True, exist_ok=True)
    
    dto_file = dto_dir / "auth_dto.go"
    dto_file.write_text(dto)
    print(f"✓ Created {dto_file.relative_to(project_path)}")
    
    # Create auth repository interface
    repository_interface = f"""package repository

import (
	"{module_path}/internal/domain/auth/entity"
)

type AuthRepository interface {{
	Create(user *entity.User) error
	FindByEmail(email string) (*entity.User, error)
	FindByProviderID(provider, providerID string) (*entity.User, error)
	FindByID(id uint) (*entity.User, error)
	Update(user *entity.User) error
	UpdateAvatar(userID uint, avatarURL string) error
	Delete(id uint) error
}}
"""
    
    repo_dir = project_path / "internal" / "domain" / "auth" / "repository"
    repo_dir.mkdir(parents=True, exist_ok=True)
    
    repo_file = repo_dir / "auth_repository.go"
    repo_file.write_text(repository_interface)
    print(f"✓ Created {repo_file.relative_to(project_path)}")
    
    # Create auth repository implementation
    repository_impl = f"""package repository

import (
	"{module_path}/internal/domain/auth/entity"
	"gorm.io/gorm"
)

type authRepository struct {{
	db *gorm.DB
}}

func NewAuthRepository(db *gorm.DB) AuthRepository {{
	return &authRepository{{db: db}}
}}

func (r *authRepository) Create(user *entity.User) error {{
	return r.db.Create(user).Error
}}

func (r *authRepository) FindByEmail(email string) (*entity.User, error) {{
	var user entity.User
	err := r.db.Where("email = ?", email).First(&user).Error
	if err != nil {{
		return nil, err
	}}
	return &user, nil
}}

func (r *authRepository) FindByProviderID(provider, providerID string) (*entity.User, error) {{
	var user entity.User
	err := r.db.Where("provider = ? AND provider_id = ?", provider, providerID).First(&user).Error
	if err != nil {{
		return nil, err
	}}
	return &user, nil
}}

func (r *authRepository) FindByID(id uint) (*entity.User, error) {{
	var user entity.User
	err := r.db.First(&user, id).Error
	if err != nil {{
		return nil, err
	}}
	return &user, nil
}}

func (r *authRepository) Update(user *entity.User) error {{
	return r.db.Save(user).Error
}}

func (r *authRepository) UpdateAvatar(userID uint, avatarURL string) error {{
	return r.db.Model(&entity.User{{}}).Where("id = ?", userID).Update("avatar_url", avatarURL).Error
}}

func (r *authRepository) Delete(id uint) error {{
	return r.db.Delete(&entity.User{{}}, id).Error
}}
"""
    
    repo_impl_file = repo_dir / "auth_repository_impl.go"
    repo_impl_file.write_text(repository_impl)
    print(f"✓ Created {repo_impl_file.relative_to(project_path)}")
    
    # Create auth service interface
    service_interface = f"""package service

import (
	"{module_path}/internal/domain/auth/dto"
)

type AuthService interface {{
	Register(req *dto.RegisterRequest) (*dto.UserResponse, error)
	Login(req *dto.LoginRequest) (*dto.LoginResponse, error)
	GoogleAuth(req *dto.GoogleAuthRequest) (*dto.LoginResponse, error)
	GetUserByID(id uint) (*dto.UserResponse, error)
	UploadAvatar(userID uint, avatarURL string) error
}}
"""
    
    service_dir = project_path / "internal" / "domain" / "auth" / "service"
    service_dir.mkdir(parents=True, exist_ok=True)
    
    service_file = service_dir / "auth_service.go"
    service_file.write_text(service_interface)
    print(f"✓ Created {service_file.relative_to(project_path)}")
    
    # Create auth service implementation
    service_impl = f"""package service

import (
	"errors"
	"{module_path}/internal/domain/auth/dto"
	"{module_path}/internal/domain/auth/entity"
	"{module_path}/internal/domain/auth/repository"
	"{module_path}/pkg/jwt"
	"gorm.io/gorm"
)

type authService struct {{
	repo repository.AuthRepository
	jwt  *jwt.JWTService
}}

func NewAuthService(repo repository.AuthRepository, jwtService *jwt.JWTService) AuthService {{
	return &authService{{
		repo: repo,
		jwt:  jwtService,
	}}
}}

func (s *authService) Register(req *dto.RegisterRequest) (*dto.UserResponse, error) {{
	// Check if user already exists
	_, err := s.repo.FindByEmail(req.Email)
	if err == nil {{
		return nil, errors.New("email already registered")
	}}
	if !errors.Is(err, gorm.ErrRecordNotFound) {{
		return nil, err
	}}

	// Create new user
	user := &entity.User{{
		Email:    req.Email,
		Name:     req.Name,
		Provider: "local",
		Role:     "user",
	}}

	if err := user.HashPassword(req.Password); err != nil {{
		return nil, err
	}}

	if err := s.repo.Create(user); err != nil {{
		return nil, err
	}}

	return &dto.UserResponse{{
		ID:        user.ID,
		Email:     user.Email,
		Name:      user.Name,
		AvatarURL: user.AvatarURL,
		Provider:  user.Provider,
		Role:      user.Role,
		IsActive:  user.IsActive,
	}}, nil
}}

func (s *authService) Login(req *dto.LoginRequest) (*dto.LoginResponse, error) {{
	// Find user by email
	user, err := s.repo.FindByEmail(req.Email)
	if err != nil {{
		if errors.Is(err, gorm.ErrRecordNotFound) {{
			return nil, errors.New("invalid email or password")
		}}
		return nil, err
	}}

	// Check if user is active
	if !user.IsActive {{
		return nil, errors.New("account is inactive")
	}}

	// Check password
	if !user.CheckPassword(req.Password) {{
		return nil, errors.New("invalid email or password")
	}}

	// Generate JWT token
	token, err := s.jwt.GenerateToken(user.ID, user.Email, user.Role)
	if err != nil {{
		return nil, err
	}}

	return &dto.LoginResponse{{
		Token: token,
		User: dto.UserResponse{{
			ID:        user.ID,
			Email:     user.Email,
			Name:      user.Name,
			AvatarURL: user.AvatarURL,
			Provider:  user.Provider,
			Role:      user.Role,
			IsActive:  user.IsActive,
		}},
	}}, nil
}}

func (s *authService) GoogleAuth(req *dto.GoogleAuthRequest) (*dto.LoginResponse, error) {{
	// Verify Google ID token and get user info
	// In production, use google.golang.org/api/oauth2/v2 to verify token
	// For now, we'll assume the token is valid and extract user info
	// You need to implement actual Google token verification

	// This is a placeholder - implement actual Google token verification
	userInfo := &dto.GoogleUserInfo{{
		Sub:           "google-user-id",
		Email:         "user@gmail.com",
		EmailVerified: true,
		Name:          "Google User",
		Picture:       "https://example.com/avatar.jpg",
	}}

	// Check if user exists by provider ID
	user, err := s.repo.FindByProviderID("google", userInfo.Sub)
	if err != nil {{
		if errors.Is(err, gorm.ErrRecordNotFound) {{
			// Create new user from Google
			user = &entity.User{{
				Email:      userInfo.Email,
				Name:       userInfo.Name,
				AvatarURL:  userInfo.Picture,
				Provider:   "google",
				ProviderID: userInfo.Sub,
				Role:       "user",
				IsActive:   true,
			}}

			if err := s.repo.Create(user); err != nil {{
				return nil, err
			}}
		}} else {{
			return nil, err
		}}
	}}

	// Check if user is active
	if !user.IsActive {{
		return nil, errors.New("account is inactive")
	}}

	// Generate JWT token
	token, err := s.jwt.GenerateToken(user.ID, user.Email, user.Role)
	if err != nil {{
		return nil, err
	}}

	return &dto.LoginResponse{{
		Token: token,
		User: dto.UserResponse{{
			ID:        user.ID,
			Email:     user.Email,
			Name:      user.Name,
			AvatarURL: user.AvatarURL,
			Provider:  user.Provider,
			Role:      user.Role,
			IsActive:  user.IsActive,
		}},
	}}, nil
}}

func (s *authService) GetUserByID(id uint) (*dto.UserResponse, error) {{
	user, err := s.repo.FindByID(id)
	if err != nil {{
		return nil, err
	}}

	return &dto.UserResponse{{
		ID:        user.ID,
		Email:     user.Email,
		Name:      user.Name,
		AvatarURL: user.AvatarURL,
		Provider:  user.Provider,
		Role:      user.Role,
		IsActive:  user.IsActive,
	}}, nil
}}

func (s *authService) UploadAvatar(userID uint, avatarURL string) error {{
	return s.repo.UpdateAvatar(userID, avatarURL)
}}
"""
    
    service_impl_file = service_dir / "auth_service_impl.go"
    service_impl_file.write_text(service_impl)
    print(f"✓ Created {service_impl_file.relative_to(project_path)}")
    
    # Create auth handler
    handler = f"""package handler

import (
	"fmt"
	"net/http"
	"path/filepath"
	"strconv"
	"time"
	"{module_path}/internal/domain/auth/dto"
	"{module_path}/internal/domain/auth/service"
	"{module_path}/pkg/response"
	"github.com/gin-gonic/gin"
)

type AuthHandler struct {{
	service service.AuthService
}}

func NewAuthHandler(service service.AuthService) *AuthHandler {{
	return &AuthHandler{{service: service}}
}}

// Register godoc
// @Summary Register a new user
// @Description Register a new user with email and password
// @Tags auth
// @Accept json
// @Produce json
// @Param request body dto.RegisterRequest true "Register request"
// @Success 201 {{object}} response.Response{{data=dto.UserResponse}}
// @Failure 400 {{object}} response.Response
// @Failure 500 {{object}} response.Response
// @Router /auth/register [post]
func (h *AuthHandler) Register(c *gin.Context) {{
	var req dto.RegisterRequest
	if err := c.ShouldBindJSON(&req); err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid request", err.Error())
		return
	}}

	user, err := h.service.Register(&req)
	if err != nil {{
		response.Error(c, http.StatusBadRequest, "Registration failed", err.Error())
		return
	}}

	response.Success(c, http.StatusCreated, "User registered successfully", user)
}}

// Login godoc
// @Summary Login user
// @Description Login with email and password
// @Tags auth
// @Accept json
// @Produce json
// @Param request body dto.LoginRequest true "Login request"
// @Success 200 {{object}} response.Response{{data=dto.LoginResponse}}
// @Failure 400 {{object}} response.Response
// @Failure 401 {{object}} response.Response
// @Router /auth/login [post]
func (h *AuthHandler) Login(c *gin.Context) {{
	var req dto.LoginRequest
	if err := c.ShouldBindJSON(&req); err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid request", err.Error())
		return
	}}

	result, err := h.service.Login(&req)
	if err != nil {{
		response.Error(c, http.StatusUnauthorized, "Login failed", err.Error())
		return
	}}

	response.Success(c, http.StatusOK, "Login successful", result)
}}

// GetProfile godoc
// @Summary Get user profile
// @Description Get current user profile
// @Tags auth
// @Accept json
// @Produce json
// @Security BearerAuth
// @Success 200 {{object}} response.Response{{data=dto.UserResponse}}
// @Failure 401 {{object}} response.Response
// @Failure 404 {{object}} response.Response
// @Router /auth/profile [get]
func (h *AuthHandler) GetProfile(c *gin.Context) {{
	userID, exists := c.Get("user_id")
	if !exists {{
		response.Error(c, http.StatusUnauthorized, "Unauthorized", "User ID not found")
		return
	}}

	user, err := h.service.GetUserByID(userID.(uint))
	if err != nil {{
		response.Error(c, http.StatusNotFound, "User not found", err.Error())
		return
	}}

	response.Success(c, http.StatusOK, "Profile retrieved successfully", user)
}}

// GoogleAuth godoc
// @Summary Google OAuth authentication
// @Description Authenticate with Google ID token
// @Tags auth
// @Accept json
// @Produce json
// @Param request body dto.GoogleAuthRequest true "Google auth request"
// @Success 200 {{object}} response.Response{{data=dto.LoginResponse}}
// @Failure 400 {{object}} response.Response
// @Failure 401 {{object}} response.Response
// @Router /auth/google [post]
func (h *AuthHandler) GoogleAuth(c *gin.Context) {{
	var req dto.GoogleAuthRequest
	if err := c.ShouldBindJSON(&req); err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid request", err.Error())
		return
	}}

	result, err := h.service.GoogleAuth(&req)
	if err != nil {{
		response.Error(c, http.StatusUnauthorized, "Google authentication failed", err.Error())
		return
	}}

	response.Success(c, http.StatusOK, "Google authentication successful", result)
}}

// UploadAvatar godoc
// @Summary Upload user avatar
// @Description Upload avatar image for current user
// @Tags auth
// @Accept multipart/form-data
// @Produce json
// @Security BearerAuth
// @Param avatar formData file true "Avatar image"
// @Success 200 {{object}} response.Response{{data=dto.UploadAvatarResponse}}
// @Failure 400 {{object}} response.Response
// @Failure 401 {{object}} response.Response
// @Failure 500 {{object}} response.Response
// @Router /auth/avatar [post]
func (h *AuthHandler) UploadAvatar(c *gin.Context) {{
	userID, exists := c.Get("user_id")
	if !exists {{
		response.Error(c, http.StatusUnauthorized, "Unauthorized", "User ID not found")
		return
	}}

	// Get file from form
	file, err := c.FormFile("avatar")
	if err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid file", err.Error())
		return
	}}

	// Validate file type
	ext := filepath.Ext(file.Filename)
	if ext != ".jpg" && ext != ".jpeg" && ext != ".png" && ext != ".gif" {{
		response.Error(c, http.StatusBadRequest, "Invalid file type", "Only jpg, jpeg, png, gif are allowed")
		return
	}}

	// Validate file size (max 5MB)
	if file.Size > 5*1024*1024 {{
		response.Error(c, http.StatusBadRequest, "File too large", "Maximum file size is 5MB")
		return
	}}

	// Generate unique filename
	filename := fmt.Sprintf("%d_%d%s", userID.(uint), time.Now().Unix(), ext)
	uploadPath := filepath.Join("uploads", "avatars", filename)

	// Save file
	if err := c.SaveUploadedFile(file, uploadPath); err != nil {{
		response.Error(c, http.StatusInternalServerError, "Failed to save file", err.Error())
		return
	}}

	// Update user avatar URL
	avatarURL := fmt.Sprintf("/uploads/avatars/%s", filename)
	if err := h.service.UploadAvatar(userID.(uint), avatarURL); err != nil {{
		response.Error(c, http.StatusInternalServerError, "Failed to update avatar", err.Error())
		return
	}}

	response.Success(c, http.StatusOK, "Avatar uploaded successfully", dto.UploadAvatarResponse{{
		AvatarURL: avatarURL,
	}})
}}
"""
    
    handler_dir = project_path / "internal" / "domain" / "auth" / "handler"
    handler_dir.mkdir(parents=True, exist_ok=True)
    
    handler_file = handler_dir / "auth_handler.go"
    handler_file.write_text(handler)
    print(f"✓ Created {handler_file.relative_to(project_path)}")


def create_jwt_package(project_path: Path, module_path: str):
    """Create JWT utility package."""
    
    jwt_service = f"""package jwt

import (
	"errors"
	"time"
	"github.com/golang-jwt/jwt/v5"
)

type JWTService struct {{
	secretKey     string
	issuer        string
	expiryMinutes int
}}

type Claims struct {{
	UserID uint   `json:"user_id"`
	Email  string `json:"email"`
	Role   string `json:"role"`
	jwt.RegisteredClaims
}}

func NewJWTService(secretKey, issuer string, expiryMinutes int) *JWTService {{
	return &JWTService{{
		secretKey:     secretKey,
		issuer:        issuer,
		expiryMinutes: expiryMinutes,
	}}
}}

func (s *JWTService) GenerateToken(userID uint, email, role string) (string, error) {{
	claims := Claims{{
		UserID: userID,
		Email:  email,
		Role:   role,
		RegisteredClaims: jwt.RegisteredClaims{{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Duration(s.expiryMinutes) * time.Minute)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Issuer:    s.issuer,
		}},
	}}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(s.secretKey))
}}

func (s *JWTService) ValidateToken(tokenString string) (*Claims, error) {{
	token, err := jwt.ParseWithClaims(tokenString, &Claims{{}}, func(token *jwt.Token) (interface{{}}, error) {{
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {{
			return nil, errors.New("invalid signing method")
		}}
		return []byte(s.secretKey), nil
	}})

	if err != nil {{
		return nil, err
	}}

	claims, ok := token.Claims.(*Claims)
	if !ok || !token.Valid {{
		return nil, errors.New("invalid token")
	}}

	return claims, nil
}}
"""
    
    jwt_dir = project_path / "pkg" / "jwt"
    jwt_dir.mkdir(parents=True, exist_ok=True)
    
    jwt_file = jwt_dir / "jwt.go"
    jwt_file.write_text(jwt_service)
    print(f"✓ Created {jwt_file.relative_to(project_path)}")


def create_auth_middleware(project_path: Path, module_path: str):
    """Create authentication middleware."""

    # Create middleware directory if it doesn't exist
    middleware_dir = project_path / "internal" / "infrastructure" / "middleware"
    middleware_dir.mkdir(parents=True, exist_ok=True)

    middleware = f"""package middleware

import (
	"net/http"
	"strings"
	"{module_path}/pkg/jwt"
	"{module_path}/pkg/response"
	"github.com/gin-gonic/gin"
)

func AuthMiddleware(jwtService *jwt.JWTService) gin.HandlerFunc {{
	return func(c *gin.Context) {{
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {{
			response.Error(c, http.StatusUnauthorized, "Unauthorized", "Authorization header is required")
			c.Abort()
			return
		}}

		// Extract token from "Bearer <token>"
		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Bearer" {{
			response.Error(c, http.StatusUnauthorized, "Unauthorized", "Invalid authorization header format")
			c.Abort()
			return
		}}

		token := parts[1]
		claims, err := jwtService.ValidateToken(token)
		if err != nil {{
			response.Error(c, http.StatusUnauthorized, "Unauthorized", err.Error())
			c.Abort()
			return
		}}

		// Set user information in context
		c.Set("user_id", claims.UserID)
		c.Set("user_email", claims.Email)
		c.Set("user_role", claims.Role)

		c.Next()
	}}
}}

func RoleMiddleware(allowedRoles ...string) gin.HandlerFunc {{
	return func(c *gin.Context) {{
		userRole, exists := c.Get("user_role")
		if !exists {{
			response.Error(c, http.StatusUnauthorized, "Unauthorized", "User role not found")
			c.Abort()
			return
		}}

		role := userRole.(string)
		allowed := false
		for _, allowedRole := range allowedRoles {{
			if role == allowedRole {{
				allowed = true
				break
			}}
		}}

		if !allowed {{
			response.Error(c, http.StatusForbidden, "Forbidden", "Insufficient permissions")
			c.Abort()
			return
		}}

		c.Next()
	}}
}}
"""
    
    middleware_file = project_path / "internal" / "infrastructure" / "middleware" / "auth.go"
    middleware_file.write_text(middleware)
    print(f"✓ Created {middleware_file.relative_to(project_path)}")


def update_env_example(project_path: Path):
    """Update .env.example with JWT configuration."""
    env_file = project_path / ".env.example"
    
    if env_file.exists():
        content = env_file.read_text()
        if "JWT_SECRET" not in content:
            content += """
# JWT Configuration
JWT_SECRET=your-secret-key-here-change-in-production
JWT_ISSUER=your-app-name
JWT_EXPIRY_MINUTES=1440
"""
            env_file.write_text(content)
            print(f"✓ Updated {env_file.relative_to(project_path)}")
    else:
        env_content = """# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=myapp
DB_SSLMODE=disable

# Server
SERVER_PORT=8080

# JWT Configuration
JWT_SECRET=your-secret-key-here-change-in-production
JWT_ISSUER=your-app-name
JWT_EXPIRY_MINUTES=1440

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
"""
        env_file.write_text(env_content)
        print(f"✓ Created {env_file.relative_to(project_path)}")


def main():
    parser = argparse.ArgumentParser(description="Add JWT authentication to Gin project")
    parser.add_argument("--project-path", default=".", help="Path to project root")
    parser.add_argument("--provider", choices=["local", "google", "both"], default="both",
                        help="Authentication provider (local, google, or both)")

    args = parser.parse_args()

    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)

    if not (project_path / "go.mod").exists():
        print(f"✗ Error: Not a valid Go project (go.mod not found)")
        sys.exit(1)

    # Read module path from go.mod
    go_mod = (project_path / "go.mod").read_text()
    module_line = [line for line in go_mod.split("\n") if line.startswith("module ")][0]
    module_path = module_line.replace("module ", "").strip()

    print(f"\n🔐 Adding JWT authentication to project")
    print(f"Provider: {args.provider}")
    print(f"Module path: {module_path}\n")

    # Create auth domain
    create_auth_domain(project_path, module_path, args.provider)

    # Create JWT package
    create_jwt_package(project_path, module_path)

    # Create auth middleware
    create_auth_middleware(project_path, module_path)

    # Update .env.example
    update_env_example(project_path)

    # Create uploads directory
    uploads_dir = project_path / "uploads" / "avatars"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created uploads/avatars directory")

    print("\n✅ JWT authentication added successfully!\n")
    print("Next steps:")
    print("  1. Install required dependencies:")
    print("     go get github.com/golang-jwt/jwt/v5")
    if args.provider in ["local", "both"]:
        print("     go get golang.org/x/crypto/bcrypt")
    if args.provider in ["google", "both"]:
        print("     go get google.golang.org/api/oauth2/v2")
    print("  2. Update .env with JWT_SECRET (generate with: openssl rand -base64 32)")
    if args.provider in ["google", "both"]:
        print("  3. Add Google OAuth credentials to .env:")
        print("     GOOGLE_CLIENT_ID=your-client-id")
        print("     GOOGLE_CLIENT_SECRET=your-client-secret")
    print("  4. Add auth routes in main.go:")
    print("     authHandler := handler.NewAuthHandler(authService)")
    print("     auth := r.Group(\"/api/auth\")")
    print("     {")
    if args.provider in ["local", "both"]:
        print("         auth.POST(\"/register\", authHandler.Register)")
        print("         auth.POST(\"/login\", authHandler.Login)")
    if args.provider in ["google", "both"]:
        print("         auth.POST(\"/google\", authHandler.GoogleAuth)")
    print("         auth.GET(\"/profile\", middleware.AuthMiddleware(jwtService), authHandler.GetProfile)")
    print("         auth.POST(\"/avatar\", middleware.AuthMiddleware(jwtService), authHandler.UploadAvatar)")
    print("     }")
    print("  5. Serve static files for avatars:")
    print("     r.Static(\"/uploads\", \"./uploads\")")
    print("  6. Run migrations to create users table")


if __name__ == "__main__":
    main()

