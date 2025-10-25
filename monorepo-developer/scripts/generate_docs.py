#!/usr/bin/env python3
"""
Generate API documentation for backend packages.
"""

import argparse
import sys
from pathlib import Path


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase."""
    return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())


def generate_api_docs(name: str) -> str:
    """Generate API documentation."""
    pascal_name = to_pascal_case(name)
    
    return f"""# {pascal_name} API Documentation

## Overview

API documentation for {pascal_name} service.

## Base URL

```
http://localhost:3000/api
```

## Authentication

All endpoints require authentication unless otherwise specified.

### Headers

```
Authorization: Bearer <token>
Content-Type: application/json
```

## Endpoints

### Health Check

Check if the service is running.

**Request:**
```
GET /health
```

**Response:**
```json
{{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00Z"
}}
```

### Example Endpoint

**Request:**
```
GET /items
```

**Query Parameters:**
- `page` (optional) - Page number (default: 1)
- `limit` (optional) - Items per page (default: 10)

**Response:**
```json
{{
  "data": [],
  "pagination": {{
    "page": 1,
    "limit": 10,
    "total": 0
  }}
}}
```

## Error Handling

All errors follow this format:

```json
{{
  "error": "Error message",
  "code": "ERROR_CODE",
  "status": 400
}}
```

### Common Error Codes

- `UNAUTHORIZED` - Missing or invalid authentication
- `FORBIDDEN` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `VALIDATION_ERROR` - Invalid request data
- `INTERNAL_ERROR` - Server error

## Rate Limiting

- Rate limit: 100 requests per minute
- Headers:
  - `X-RateLimit-Limit`: 100
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

## Pagination

Use `page` and `limit` query parameters:

```
GET /items?page=1&limit=10
```

Response includes pagination info:

```json
{{
  "data": [],
  "pagination": {{
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  }}
}}
```

## Filtering

Use query parameters for filtering:

```
GET /items?status=active&category=electronics
```

## Sorting

Use `sort` parameter:

```
GET /items?sort=-created_at,name
```

- Prefix with `-` for descending order
- Comma-separated for multiple fields

## Versioning

API version is specified in the URL:

```
GET /api/v1/items
```

## Webhooks

Subscribe to events:

```
POST /webhooks
Content-Type: application/json

{{
  "url": "https://example.com/webhook",
  "events": ["item.created", "item.updated"]
}}
```

## Examples

### Using cURL

```bash
# Get items
curl -H "Authorization: Bearer TOKEN" \\
  http://localhost:3000/api/items

# Create item
curl -X POST \\
  -H "Authorization: Bearer TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{{"name": "Item"}}' \\
  http://localhost:3000/api/items
```

### Using JavaScript/Fetch

```javascript
// Get items
const response = await fetch('http://localhost:3000/api/items', {{
  headers: {{
    'Authorization': `Bearer ${{token}}`,
    'Content-Type': 'application/json'
  }}
}})

const data = await response.json()
```

### Using Python/Requests

```python
import requests

headers = {{
    'Authorization': f'Bearer {{token}}',
    'Content-Type': 'application/json'
}}

response = requests.get('http://localhost:3000/api/items', headers=headers)
data = response.json()
```

## Support

For issues or questions:
- Email: support@example.com
- GitHub: https://github.com/example/repo
- Documentation: https://docs.example.com

## Changelog

### v1.0.0 (2024-01-01)
- Initial release
- Basic CRUD operations
- Authentication support
"""


def generate_openapi_docs(name: str) -> str:
    """Generate OpenAPI/Swagger documentation."""
    pascal_name = to_pascal_case(name)
    
    return f"""openapi: 3.0.0
info:
  title: {pascal_name} API
  description: API documentation for {pascal_name} service
  version: 1.0.0
  contact:
    name: Support
    email: support@example.com

servers:
  - url: http://localhost:3000/api
    description: Development server
  - url: https://api.example.com
    description: Production server

paths:
  /health:
    get:
      summary: Health check
      tags:
        - Health
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: ok
                  timestamp:
                    type: string
                    format: date-time

  /items:
    get:
      summary: List items
      tags:
        - Items
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: List of items
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Item'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '401':
          description: Unauthorized

    post:
      summary: Create item
      tags:
        - Items
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateItemRequest'
      responses:
        '201':
          description: Item created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Item'
        '400':
          description: Invalid request
        '401':
          description: Unauthorized

  /items/{{id}}:
    get:
      summary: Get item by ID
      tags:
        - Items
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Item details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Item'
        '404':
          description: Item not found

    put:
      summary: Update item
      tags:
        - Items
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateItemRequest'
      responses:
        '200':
          description: Item updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Item'
        '404':
          description: Item not found

    delete:
      summary: Delete item
      tags:
        - Items
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Item deleted
        '404':
          description: Item not found

components:
  schemas:
    Item:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    CreateItemRequest:
      type: object
      required:
        - name
      properties:
        name:
          type: string

    UpdateItemRequest:
      type: object
      properties:
        name:
          type: string

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        pages:
          type: integer

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
"""


def create_docs(project_path: Path, name: str, doc_type: str = "markdown"):
    """Create API documentation."""
    print(f"\n📖 Generating {name} documentation ({doc_type})\n")
    
    # Generate documentation content
    generators = {
        "markdown": generate_api_docs,
        "openapi": generate_openapi_docs,
    }
    
    if doc_type not in generators:
        print(f"✗ Unknown documentation type: {doc_type}")
        print(f"Available types: {', '.join(generators.keys())}")
        return False
    
    generator = generators[doc_type]
    content = generator(name)
    
    # Determine documentation path
    pascal_name = to_pascal_case(name)
    
    if doc_type == "markdown":
        doc_path = project_path / "docs" / f"{pascal_name}_API.md"
    else:
        doc_path = project_path / "docs" / f"{pascal_name}_OpenAPI.yaml"
    
    # Create directory if it doesn't exist
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write documentation file
    doc_path.write_text(content)
    print(f"✓ Created {doc_path.relative_to(project_path)}")
    
    return True


def find_backend_package(project_path: Path, package_name: str = None):
    """Find a backend package in the monorepo."""
    packages_dir = project_path / "packages"
    
    if not packages_dir.exists():
        print("✗ Not a valid monorepo project (packages directory not found)")
        return None
    
    if package_name:
        package_path = packages_dir / package_name
        if package_path.exists() and (package_path / "src").exists():
            return package_path
        else:
            print(f"✗ Backend package '{package_name}' not found or not configured")
            return None
    
    # Find first backend package with src directory
    for package_dir in packages_dir.iterdir():
        if package_dir.is_dir() and (package_dir / "src").exists():
            return package_dir
    
    print("✗ No backend package found in monorepo")
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate API documentation")
    parser.add_argument("name", help="API name (e.g., UserAPI, user-api)")
    parser.add_argument("--type", choices=["markdown", "openapi"],
                        default="markdown", help="Documentation type")
    parser.add_argument("--package", help="Target package name")
    parser.add_argument("--project-path", default=".", help="Path to the monorepo project")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    
    # Find package
    package_path = find_backend_package(project_path, args.package)
    if not package_path:
        sys.exit(1)
    
    print(f"\n📦 Target package: {package_path.name}\n")
    
    # Create documentation
    if not create_docs(package_path, args.name, args.type):
        sys.exit(1)
    
    print(f"\n✅ Documentation '{args.name}' generated successfully!\n")


if __name__ == "__main__":
    main()

