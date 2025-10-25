# Authentication and Avatar Upload Guide

This guide covers implementing authentication and avatar upload functionality in your monorepo backend.

## Overview

The monorepo-developer skill provides two powerful scripts:

1. **add_auth.py** - Add authentication (local, Google, or both)
2. **add_avatar.py** - Add avatar upload functionality

## Authentication

### Local Authentication

Local authentication uses email and password:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_auth.py --type local
```

**Features:**
- Email/password registration and login
- JWT token generation
- Password hashing (implement with bcrypt)
- Auth middleware for route protection

**Environment Variables:**
```
JWT_SECRET=your-secret-key
```

**Routes:**
```
POST /auth/register - Register new user
POST /auth/login - Login with email/password
POST /auth/logout - Logout
GET /auth/me - Get current user
```

**Example Usage:**

```bash
# Register
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
  }'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Get current user
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/auth/me
```

### Google OAuth

Google OAuth allows users to sign in with their Google account:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_auth.py --type google
```

**Features:**
- Google OAuth token verification
- Automatic user creation
- Avatar URL from Google profile
- JWT token generation

**Environment Variables:**
```
JWT_SECRET=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**Routes:**
```
POST /auth/google - Login with Google token
POST /auth/logout - Logout
GET /auth/me - Get current user
```

**Example Usage:**

```bash
# Login with Google
curl -X POST http://localhost:3000/api/auth/google \
  -H "Content-Type: application/json" \
  -d '{
    "token": "google-id-token"
  }'
```

### Combined Authentication

Use both local and Google authentication:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_auth.py --type both
```

**Features:**
- Local email/password authentication
- Google OAuth authentication
- User provider field ('local' or 'google')
- Unified JWT token system

**Environment Variables:**
```
JWT_SECRET=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**Routes:**
```
POST /auth/register - Register with email/password
POST /auth/login - Login with email/password
POST /auth/google - Login with Google
POST /auth/logout - Logout
GET /auth/me - Get current user
```

## Avatar Upload

### Backend Setup

Add avatar upload to your backend:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_avatar.py --type backend
```

**Features:**
- Multipart file upload
- File type validation (JPEG, PNG, WebP, GIF)
- File size validation (5MB default)
- Avatar URL storage in user schema
- Google avatar URL support

**User Schema:**
```typescript
interface User {
  id: string
  email: string
  name: string
  avatar_url?: string  // URL to avatar image
  provider: 'local' | 'google'
  created_at: Date
  updated_at: Date
}
```

**Routes:**
```
POST /avatar - Upload avatar
GET /avatar/:filename - Get avatar
PUT /avatar - Update avatar
DELETE /avatar - Delete avatar
```

### Upload Avatar

**Request:**
```bash
curl -X POST http://localhost:3000/api/avatar \
  -H "Authorization: Bearer TOKEN" \
  -F "avatar=@/path/to/image.jpg"
```

**Response:**
```json
{
  "message": "Avatar uploaded successfully",
  "avatar_url": "/uploads/avatars/avatar_1234567890.jpg",
  "filename": "avatar_1234567890.jpg"
}
```

### Update Avatar

**Request:**
```bash
curl -X PUT http://localhost:3000/api/avatar \
  -H "Authorization: Bearer TOKEN" \
  -F "avatar=@/path/to/new-image.jpg"
```

**Response:**
```json
{
  "message": "Avatar updated successfully",
  "avatar_url": "/uploads/avatars/avatar_1234567891.jpg",
  "filename": "avatar_1234567891.jpg"
}
```

### Delete Avatar

**Request:**
```bash
curl -X DELETE http://localhost:3000/api/avatar \
  -H "Authorization: Bearer TOKEN"
```

**Response:**
```json
{
  "message": "Avatar deleted successfully"
}
```

### Frontend Setup

Add avatar upload component to your frontend:

```bash
python ~/.claude/skills/monorepo-developer/scripts/add_avatar.py --type frontend
```

**Component Usage:**

```typescript
import { AvatarUpload } from '@/components/AvatarUpload'

export function ProfilePage() {
  return (
    <AvatarUpload
      onSuccess={(avatarUrl) => {
        console.log('Avatar uploaded:', avatarUrl)
      }}
      onError={(error) => {
        console.error('Upload failed:', error)
      }}
    />
  )
}
```

## Integration Example

### Complete User Registration Flow

```typescript
// 1. Register user
const registerResponse = await fetch('/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123',
    name: 'John Doe'
  })
})

const { token, user } = await registerResponse.json()

// 2. Store token
localStorage.setItem('token', token)

// 3. Upload avatar
const formData = new FormData()
formData.append('avatar', avatarFile)

const uploadResponse = await fetch('/api/avatar', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
})

const { avatar_url } = await uploadResponse.json()

// 4. User now has avatar_url in profile
```

### Google OAuth Flow

```typescript
// 1. Get Google token from frontend
const googleToken = await getGoogleToken()

// 2. Login with Google
const loginResponse = await fetch('/api/auth/google', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ token: googleToken })
})

const { token, user } = await loginResponse.json()

// 3. Store token
localStorage.setItem('token', token)

// 4. User already has avatar_url from Google profile
console.log(user.avatar_url) // Google profile picture URL
```

## Best Practices

### Security

1. **JWT Secret** - Use strong, random secret key
2. **HTTPS** - Always use HTTPS in production
3. **Token Expiration** - Implement token refresh mechanism
4. **Password Hashing** - Use bcrypt or similar
5. **Rate Limiting** - Limit login attempts
6. **CORS** - Configure CORS properly

### File Upload

1. **Validation** - Always validate file type and size
2. **Naming** - Use unique filenames with timestamps
3. **Storage** - Use cloud storage (S3, GCS) in production
4. **Cleanup** - Delete old avatars when updating
5. **CDN** - Serve avatars through CDN for performance

### User Experience

1. **Preview** - Show image preview before upload
2. **Progress** - Display upload progress
3. **Feedback** - Show success/error messages
4. **Defaults** - Provide default avatar if none uploaded
5. **Optimization** - Compress images before upload

## Environment Configuration

### .env Example

```bash
# Authentication
JWT_SECRET=your-super-secret-key-change-this
JWT_EXPIRATION=7d

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# File Upload
UPLOAD_DIR=./uploads/avatars
MAX_FILE_SIZE=5242880  # 5MB in bytes
ALLOWED_MIME_TYPES=image/jpeg,image/png,image/webp,image/gif

# Cloud Storage (Optional)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=your-bucket-name
```

## Troubleshooting

### Invalid Token

**Problem:** "Invalid token" error

**Solution:**
- Check JWT_SECRET matches between generation and verification
- Verify token hasn't expired
- Ensure Authorization header format is correct: `Bearer TOKEN`

### Upload Failed

**Problem:** "Avatar upload failed" error

**Solution:**
- Check file size (max 5MB)
- Verify file type is image (JPEG, PNG, WebP, GIF)
- Ensure upload directory exists and is writable
- Check disk space

### Google OAuth Error

**Problem:** "Invalid Google token" error

**Solution:**
- Verify GOOGLE_CLIENT_ID is correct
- Check token hasn't expired
- Ensure token is from correct Google project
- Verify CORS configuration

## See Also

- [Bun + Hono Setup](./bun_hono_setup.md)
- [Monorepo Best Practices](./monorepo_best_practices.md)
- [React Code Generation](./react_code_generation.md)

