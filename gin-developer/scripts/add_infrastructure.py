#!/usr/bin/env python3
"""
Add infrastructure components to a Gin project.

Usage:
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=<type> --provider=<provider> [--project-path=<path>]

Examples:
    # Storage
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=storage --provider=local
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=storage --provider=s3
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=storage --provider=gcs

    # Cache
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=cache --provider=redis
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=cache --provider=memory

    # Queue
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=queue --provider=redis
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=queue --provider=kafka
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=queue --provider=rabbitmq

    # Email
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=email --provider=smtp
    python ~/.claude/skills/gin-developer/scripts/add_infrastructure.py --type=email --provider=sendgrid
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List


SUPPORTED_TYPES = {
    "storage": ["local", "s3", "gcs"],
    "cache": ["redis", "memory"],
    "queue": ["redis", "kafka", "rabbitmq"],
    "email": ["smtp", "sendgrid"],
}


def get_storage_interface() -> str:
    """Get storage interface definition."""
    return """package storage

import (
	"context"
	"io"
)

// Storage defines the interface for file storage operations
type Storage interface {
	// Upload uploads a file to storage
	Upload(ctx context.Context, key string, reader io.Reader) error

	// Download downloads a file from storage
	Download(ctx context.Context, key string) (io.ReadCloser, error)

	// Delete deletes a file from storage
	Delete(ctx context.Context, key string) error

	// Exists checks if a file exists in storage
	Exists(ctx context.Context, key string) (bool, error)

	// GetURL gets the public URL of a file
	GetURL(ctx context.Context, key string) (string, error)
}
"""


def get_storage_local() -> str:
    """Get local storage implementation."""
    return """package storage

import (
	"context"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

type LocalStorage struct {
	basePath string
	baseURL  string
}

func NewLocalStorage(basePath, baseURL string) *LocalStorage {
	return &LocalStorage{
		basePath: basePath,
		baseURL:  baseURL,
	}
}

func (s *LocalStorage) Upload(ctx context.Context, key string, reader io.Reader) error {
	filePath := filepath.Join(s.basePath, key)

	// Create directory if not exists
	dir := filepath.Dir(filePath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	// Create file
	file, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("failed to create file: %w", err)
	}
	defer file.Close()

	// Copy data
	if _, err := io.Copy(file, reader); err != nil {
		return fmt.Errorf("failed to write file: %w", err)
	}

	return nil
}

func (s *LocalStorage) Download(ctx context.Context, key string) (io.ReadCloser, error) {
	filePath := filepath.Join(s.basePath, key)
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	return file, nil
}

func (s *LocalStorage) Delete(ctx context.Context, key string) error {
	filePath := filepath.Join(s.basePath, key)
	if err := os.Remove(filePath); err != nil {
		return fmt.Errorf("failed to delete file: %w", err)
	}
	return nil
}

func (s *LocalStorage) Exists(ctx context.Context, key string) (bool, error) {
	filePath := filepath.Join(s.basePath, key)
	_, err := os.Stat(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return false, nil
		}
		return false, err
	}
	return true, nil
}

func (s *LocalStorage) GetURL(ctx context.Context, key string) (string, error) {
	return fmt.Sprintf("%s/%s", s.baseURL, key), nil
}
"""


def get_storage_s3() -> str:
    """Get S3 storage implementation."""
    return """package storage

import (
	"context"
	"fmt"
	"io"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/credentials"
	"github.com/aws/aws-sdk-go-v2/service/s3"
)

type S3Storage struct {
	client *s3.Client
	bucket string
	region string
}

type S3Config struct {
	Endpoint        string
	Region          string
	AccessKeyID     string
	SecretAccessKey string
	Bucket          string
	UsePathStyle    bool
}

func NewS3Storage(cfg S3Config) (*S3Storage, error) {
	// Load AWS config
	awsCfg, err := config.LoadDefaultConfig(context.TODO(),
		config.WithRegion(cfg.Region),
		config.WithCredentialsProvider(credentials.NewStaticCredentialsProvider(
			cfg.AccessKeyID,
			cfg.SecretAccessKey,
			"",
		)),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to load AWS config: %w", err)
	}

	// Create S3 client
	client := s3.NewFromConfig(awsCfg, func(o *s3.Options) {
		if cfg.Endpoint != "" {
			o.BaseEndpoint = aws.String(cfg.Endpoint)
		}
		o.UsePathStyle = cfg.UsePathStyle
	})

	return &S3Storage{
		client: client,
		bucket: cfg.Bucket,
		region: cfg.Region,
	}, nil
}

func (s *S3Storage) Upload(ctx context.Context, key string, reader io.Reader) error {
	_, err := s.client.PutObject(ctx, &s3.PutObjectInput{
		Bucket: aws.String(s.bucket),
		Key:    aws.String(key),
		Body:   reader,
	})
	if err != nil {
		return fmt.Errorf("failed to upload to S3: %w", err)
	}
	return nil
}

func (s *S3Storage) Download(ctx context.Context, key string) (io.ReadCloser, error) {
	result, err := s.client.GetObject(ctx, &s3.GetObjectInput{
		Bucket: aws.String(s.bucket),
		Key:    aws.String(key),
	})
	if err != nil {
		return nil, fmt.Errorf("failed to download from S3: %w", err)
	}
	return result.Body, nil
}

func (s *S3Storage) Delete(ctx context.Context, key string) error {
	_, err := s.client.DeleteObject(ctx, &s3.DeleteObjectInput{
		Bucket: aws.String(s.bucket),
		Key:    aws.String(key),
	})
	if err != nil {
		return fmt.Errorf("failed to delete from S3: %w", err)
	}
	return nil
}

func (s *S3Storage) Exists(ctx context.Context, key string) (bool, error) {
	_, err := s.client.HeadObject(ctx, &s3.HeadObjectInput{
		Bucket: aws.String(s.bucket),
		Key:    aws.String(key),
	})
	if err != nil {
		return false, nil
	}
	return true, nil
}

func (s *S3Storage) GetURL(ctx context.Context, key string) (string, error) {
	return fmt.Sprintf("https://%s.s3.%s.amazonaws.com/%s", s.bucket, s.region, key), nil
}
"""


def get_storage_gcs() -> str:
    """Get GCS storage implementation."""
    return """package storage

import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/storage"
)

type GCSStorage struct {
	client *storage.Client
	bucket string
}

func NewGCSStorage(ctx context.Context, bucketName string) (*GCSStorage, error) {
	client, err := storage.NewClient(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to create GCS client: %w", err)
	}

	return &GCSStorage{
		client: client,
		bucket: bucketName,
	}, nil
}

func (s *GCSStorage) Upload(ctx context.Context, key string, reader io.Reader) error {
	wc := s.client.Bucket(s.bucket).Object(key).NewWriter(ctx)
	if _, err := io.Copy(wc, reader); err != nil {
		return fmt.Errorf("failed to upload to GCS: %w", err)
	}
	if err := wc.Close(); err != nil {
		return fmt.Errorf("failed to close GCS writer: %w", err)
	}
	return nil
}

func (s *GCSStorage) Download(ctx context.Context, key string) (io.ReadCloser, error) {
	rc, err := s.client.Bucket(s.bucket).Object(key).NewReader(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to download from GCS: %w", err)
	}
	return rc, nil
}

func (s *GCSStorage) Delete(ctx context.Context, key string) error {
	if err := s.client.Bucket(s.bucket).Object(key).Delete(ctx); err != nil {
		return fmt.Errorf("failed to delete from GCS: %w", err)
	}
	return nil
}

func (s *GCSStorage) Exists(ctx context.Context, key string) (bool, error) {
	_, err := s.client.Bucket(s.bucket).Object(key).Attrs(ctx)
	if err != nil {
		if err == storage.ErrObjectNotExist {
			return false, nil
		}
		return false, err
	}
	return true, nil
}

func (s *GCSStorage) GetURL(ctx context.Context, key string) (string, error) {
	return fmt.Sprintf("https://storage.googleapis.com/%s/%s", s.bucket, key), nil
}
"""


def get_cache_interface() -> str:
    """Get cache interface definition."""
    return """package cache

import (
	"context"
	"time"
)

// Cache defines the interface for caching operations
type Cache interface {
	// Get retrieves a value from cache
	Get(ctx context.Context, key string) (string, error)

	// Set stores a value in cache with expiration
	Set(ctx context.Context, key string, value string, expiration time.Duration) error

	// Delete removes a value from cache
	Delete(ctx context.Context, key string) error

	// Exists checks if a key exists in cache
	Exists(ctx context.Context, key string) (bool, error)

	// Clear clears all cache entries
	Clear(ctx context.Context) error
}
"""


def get_cache_redis() -> str:
    """Get Redis cache implementation."""
    return """package cache

import (
	"context"
	"fmt"
	"time"

	"github.com/redis/go-redis/v9"
)

type RedisCache struct {
	client *redis.Client
}

type RedisConfig struct {
	Host     string
	Port     string
	Password string
	DB       int
}

func NewRedisCache(cfg RedisConfig) *RedisCache {
	client := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", cfg.Host, cfg.Port),
		Password: cfg.Password,
		DB:       cfg.DB,
	})

	return &RedisCache{
		client: client,
	}
}

func (c *RedisCache) Get(ctx context.Context, key string) (string, error) {
	val, err := c.client.Get(ctx, key).Result()
	if err == redis.Nil {
		return "", fmt.Errorf("key not found")
	}
	if err != nil {
		return "", fmt.Errorf("failed to get from cache: %w", err)
	}
	return val, nil
}

func (c *RedisCache) Set(ctx context.Context, key string, value string, expiration time.Duration) error {
	if err := c.client.Set(ctx, key, value, expiration).Err(); err != nil {
		return fmt.Errorf("failed to set cache: %w", err)
	}
	return nil
}

func (c *RedisCache) Delete(ctx context.Context, key string) error {
	if err := c.client.Del(ctx, key).Err(); err != nil {
		return fmt.Errorf("failed to delete from cache: %w", err)
	}
	return nil
}

func (c *RedisCache) Exists(ctx context.Context, key string) (bool, error) {
	val, err := c.client.Exists(ctx, key).Result()
	if err != nil {
		return false, fmt.Errorf("failed to check existence: %w", err)
	}
	return val > 0, nil
}

func (c *RedisCache) Clear(ctx context.Context) error {
	if err := c.client.FlushDB(ctx).Err(); err != nil {
		return fmt.Errorf("failed to clear cache: %w", err)
	}
	return nil
}
"""


def get_cache_memory() -> str:
    """Get in-memory cache implementation."""
    return """package cache

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type cacheItem struct {
	value      string
	expiration time.Time
}

type MemoryCache struct {
	items map[string]cacheItem
	mu    sync.RWMutex
}

func NewMemoryCache() *MemoryCache {
	cache := &MemoryCache{
		items: make(map[string]cacheItem),
	}

	// Start cleanup goroutine
	go cache.cleanup()

	return cache
}

func (c *MemoryCache) Get(ctx context.Context, key string) (string, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	item, exists := c.items[key]
	if !exists {
		return "", fmt.Errorf("key not found")
	}

	if time.Now().After(item.expiration) {
		return "", fmt.Errorf("key expired")
	}

	return item.value, nil
}

func (c *MemoryCache) Set(ctx context.Context, key string, value string, expiration time.Duration) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.items[key] = cacheItem{
		value:      value,
		expiration: time.Now().Add(expiration),
	}

	return nil
}

func (c *MemoryCache) Delete(ctx context.Context, key string) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	delete(c.items, key)
	return nil
}

func (c *MemoryCache) Exists(ctx context.Context, key string) (bool, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	item, exists := c.items[key]
	if !exists {
		return false, nil
	}

	if time.Now().After(item.expiration) {
		return false, nil
	}

	return true, nil
}

func (c *MemoryCache) Clear(ctx context.Context) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.items = make(map[string]cacheItem)
	return nil
}

func (c *MemoryCache) cleanup() {
	ticker := time.NewTicker(1 * time.Minute)
	defer ticker.Stop()

	for range ticker.C {
		c.mu.Lock()
		now := time.Now()
		for key, item := range c.items {
			if now.After(item.expiration) {
				delete(c.items, key)
			}
		}
		c.mu.Unlock()
	}
}
"""



def get_dependencies(infra_type: str, provider: str) -> List[str]:
    """Get Go dependencies for infrastructure type and provider."""
    deps = {
        ("storage", "s3"): [
            "github.com/aws/aws-sdk-go-v2/aws",
            "github.com/aws/aws-sdk-go-v2/config",
            "github.com/aws/aws-sdk-go-v2/credentials",
            "github.com/aws/aws-sdk-go-v2/service/s3",
        ],
        ("storage", "gcs"): [
            "cloud.google.com/go/storage",
        ],
        ("cache", "redis"): [
            "github.com/redis/go-redis/v9",
        ],
        ("queue", "redis"): [
            "github.com/redis/go-redis/v9",
        ],
        ("queue", "kafka"): [
            "github.com/segmentio/kafka-go",
        ],
        ("queue", "rabbitmq"): [
            "github.com/rabbitmq/amqp091-go",
        ],
        ("email", "sendgrid"): [
            "github.com/sendgrid/sendgrid-go",
        ],
    }
    return deps.get((infra_type, provider), [])


def create_infrastructure(project_path: Path, infra_type: str, provider: str):
    """Create infrastructure component."""
    print(f"\n🚀 Adding {infra_type} infrastructure with {provider} provider\n")

    # Create directory
    infra_dir = project_path / "internal" / "infrastructure" / infra_type
    infra_dir.mkdir(parents=True, exist_ok=True)

    # Get content based on type and provider
    interface_content = None
    impl_content = None

    if infra_type == "storage":
        interface_content = get_storage_interface()
        if provider == "local":
            impl_content = get_storage_local()
        elif provider == "s3":
            impl_content = get_storage_s3()
        elif provider == "gcs":
            impl_content = get_storage_gcs()

    elif infra_type == "cache":
        interface_content = get_cache_interface()
        if provider == "redis":
            impl_content = get_cache_redis()
        elif provider == "memory":
            impl_content = get_cache_memory()

    if not interface_content or not impl_content:
        print(f"✗ Unsupported combination: {infra_type}/{provider}")
        return

    # Write interface file
    interface_file = infra_dir / f"{infra_type}.go"
    interface_file.write_text(interface_content)
    print(f"✓ Created {infra_type}/{infra_type}.go (interface)")

    # Write implementation file
    impl_file = infra_dir / f"{provider}.go"
    impl_file.write_text(impl_content)
    print(f"✓ Created {infra_type}/{provider}.go (implementation)")

    # Get dependencies
    deps = get_dependencies(infra_type, provider)
    if deps:
        print(f"\n📦 Required dependencies:")
        for dep in deps:
            print(f"   - {dep}")
        print(f"\nRun: go get {' '.join(deps)}")

    print(f"\n✅ {infra_type.capitalize()} infrastructure added successfully!")
    print(f"\nUsage example:")
    print_usage_example(infra_type, provider)


def print_usage_example(infra_type: str, provider: str):
    """Print usage example for the infrastructure."""
    if infra_type == "storage":
        if provider == "local":
            print("""
// In your main.go or initialization code:
storage := storage.NewLocalStorage("./uploads", "http://localhost:8080/uploads")

// Upload file
err := storage.Upload(ctx, "files/image.jpg", fileReader)

// Download file
reader, err := storage.Download(ctx, "files/image.jpg")

// Get URL
url, err := storage.GetURL(ctx, "files/image.jpg")
""")
        elif provider == "s3":
            print("""
// In your main.go or initialization code:
storage, err := storage.NewS3Storage(storage.S3Config{
    Endpoint:        os.Getenv("S3_ENDPOINT"),
    Region:          os.Getenv("S3_REGION"),
    AccessKeyID:     os.Getenv("S3_ACCESS_KEY"),
    SecretAccessKey: os.Getenv("S3_SECRET_KEY"),
    Bucket:          os.Getenv("S3_BUCKET"),
    UsePathStyle:    true,
})

// Upload file
err = storage.Upload(ctx, "files/image.jpg", fileReader)
""")
        elif provider == "gcs":
            print("""
// In your main.go or initialization code:
storage, err := storage.NewGCSStorage(ctx, os.Getenv("GCS_BUCKET"))

// Upload file
err = storage.Upload(ctx, "files/image.jpg", fileReader)
""")

    elif infra_type == "cache":
        if provider == "redis":
            print("""
// In your main.go or initialization code:
cache := cache.NewRedisCache(cache.RedisConfig{
    Host:     os.Getenv("REDIS_HOST"),
    Port:     os.Getenv("REDIS_PORT"),
    Password: os.Getenv("REDIS_PASSWORD"),
    DB:       0,
})

// Set value
err := cache.Set(ctx, "key", "value", 5*time.Minute)

// Get value
val, err := cache.Get(ctx, "key")
""")
        elif provider == "memory":
            print("""
// In your main.go or initialization code:
cache := cache.NewMemoryCache()

// Set value
err := cache.Set(ctx, "key", "value", 5*time.Minute)

// Get value
val, err := cache.Get(ctx, "key")
""")


def main():
    parser = argparse.ArgumentParser(description="Add infrastructure components to Gin project")
    parser.add_argument("--type", required=True, choices=list(SUPPORTED_TYPES.keys()),
                        help="Infrastructure type")
    parser.add_argument("--provider", required=True, help="Provider name")
    parser.add_argument("--project-path", default=".", help="Path to project root")

    args = parser.parse_args()

    # Validate provider
    if args.provider not in SUPPORTED_TYPES[args.type]:
        print(f"✗ Error: Unsupported provider '{args.provider}' for type '{args.type}'")
        print(f"Supported providers: {', '.join(SUPPORTED_TYPES[args.type])}")
        sys.exit(1)

    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)

    # Check if it's a Go project
    if not (project_path / "go.mod").exists():
        print(f"✗ Error: Not a Go project (go.mod not found)")
        sys.exit(1)

    create_infrastructure(project_path, args.type, args.provider)


if __name__ == "__main__":
    main()


