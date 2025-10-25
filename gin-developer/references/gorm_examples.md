# GORM Usage Examples

## Overview

GORM is a powerful ORM library for Go. This guide covers common patterns and best practices.

## Basic Setup

```go
import (
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
    "gorm.io/gorm/logger"
)

func NewDB() (*gorm.DB, error) {
    dsn := "host=localhost user=postgres password=postgres dbname=mydb port=5432 sslmode=disable"
    
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        return nil, err
    }
    
    return db, nil
}
```

## Model Definition

### Basic Model

```go
type User struct {
    ID        uint      `gorm:"primaryKey"`
    Name      string    `gorm:"type:varchar(255);not null"`
    Email     string    `gorm:"type:varchar(255);uniqueIndex;not null"`
    Age       int       `gorm:"type:int;default:0"`
    Active    bool      `gorm:"type:boolean;default:true"`
    CreatedAt time.Time `gorm:"autoCreateTime"`
    UpdatedAt time.Time `gorm:"autoUpdateTime"`
}

func (User) TableName() string {
    return "users"
}
```

### Model with Relationships

```go
// One-to-Many
type User struct {
    ID      uint
    Name    string
    Posts   []Post `gorm:"foreignKey:UserID"`
}

type Post struct {
    ID      uint
    Title   string
    UserID  uint
    User    User `gorm:"foreignKey:UserID"`
}

// Many-to-Many
type User struct {
    ID    uint
    Name  string
    Roles []Role `gorm:"many2many:user_roles;"`
}

type Role struct {
    ID    uint
    Name  string
    Users []User `gorm:"many2many:user_roles;"`
}

// Belongs To
type Profile struct {
    ID     uint
    Bio    string
    UserID uint
    User   User `gorm:"foreignKey:UserID"`
}
```

### Embedded Structs

```go
type BaseModel struct {
    ID        uint      `gorm:"primaryKey"`
    CreatedAt time.Time `gorm:"autoCreateTime"`
    UpdatedAt time.Time `gorm:"autoUpdateTime"`
    DeletedAt gorm.DeletedAt `gorm:"index"`
}

type User struct {
    BaseModel
    Name  string `gorm:"type:varchar(255)"`
    Email string `gorm:"type:varchar(255);uniqueIndex"`
}
```

## CRUD Operations

### Create

```go
// Create single record
user := User{Name: "John", Email: "john@example.com"}
result := db.Create(&user)
if result.Error != nil {
    return result.Error
}
fmt.Println("Created user ID:", user.ID)

// Create multiple records
users := []User{
    {Name: "John", Email: "john@example.com"},
    {Name: "Jane", Email: "jane@example.com"},
}
db.Create(&users)

// Create with selected fields
db.Select("Name", "Email").Create(&user)

// Create and omit fields
db.Omit("Age").Create(&user)
```

### Read

```go
// Find by primary key
var user User
db.First(&user, 1) // SELECT * FROM users WHERE id = 1

// Find first record
db.First(&user) // SELECT * FROM users ORDER BY id LIMIT 1

// Find last record
db.Last(&user) // SELECT * FROM users ORDER BY id DESC LIMIT 1

// Find all records
var users []User
db.Find(&users) // SELECT * FROM users

// Find with conditions
db.Where("name = ?", "John").First(&user)
db.Where("name = ? AND age >= ?", "John", 18).Find(&users)
db.Where("name IN ?", []string{"John", "Jane"}).Find(&users)
db.Where("name LIKE ?", "%john%").Find(&users)

// Find with struct
db.Where(&User{Name: "John", Age: 20}).First(&user)

// Find with map
db.Where(map[string]interface{}{"name": "John", "age": 20}).Find(&users)

// Not conditions
db.Not("name = ?", "John").Find(&users)
db.Not(map[string]interface{}{"name": []string{"John", "Jane"}}).Find(&users)

// Or conditions
db.Where("name = ?", "John").Or("name = ?", "Jane").Find(&users)

// Select specific fields
db.Select("name", "email").Find(&users)

// Order
db.Order("age desc, name").Find(&users)

// Limit & Offset
db.Limit(10).Offset(20).Find(&users)

// Group & Having
db.Model(&User{}).Select("name, sum(age) as total").Group("name").Having("sum(age) > ?", 100).Find(&results)
```

### Update

```go
// Update single column
db.Model(&user).Update("name", "John Doe")

// Update multiple columns with struct
db.Model(&user).Updates(User{Name: "John Doe", Age: 30})

// Update multiple columns with map
db.Model(&user).Updates(map[string]interface{}{"name": "John Doe", "age": 30})

// Update selected fields
db.Model(&user).Select("name").Updates(map[string]interface{}{"name": "John", "age": 0})

// Update with conditions
db.Model(&User{}).Where("active = ?", true).Update("name", "John")

// Update multiple records
db.Model(&User{}).Where("role = ?", "admin").Updates(User{Active: false})

// Update with SQL expression
db.Model(&user).Update("age", gorm.Expr("age + ?", 1))

// Batch updates
db.Model(&User{}).Where("id IN ?", []int{1, 2, 3}).Updates(map[string]interface{}{"active": false})
```

### Delete

```go
// Delete by primary key
db.Delete(&User{}, 1)

// Delete with conditions
db.Where("name = ?", "John").Delete(&User{})

// Delete multiple records
db.Delete(&User{}, []int{1, 2, 3})

// Soft delete (requires DeletedAt field)
db.Delete(&user) // Sets DeletedAt to current time

// Permanently delete
db.Unscoped().Delete(&user)

// Find soft deleted records
db.Unscoped().Where("name = ?", "John").Find(&users)
```

## Advanced Queries

### Joins

```go
// Inner Join
db.Joins("JOIN posts ON posts.user_id = users.id").Find(&users)

// Left Join
db.Joins("LEFT JOIN posts ON posts.user_id = users.id").Find(&users)

// Join with conditions
db.Joins("JOIN posts ON posts.user_id = users.id AND posts.published = ?", true).Find(&users)

// Preload associations
db.Preload("Posts").Find(&users)
db.Preload("Posts.Comments").Find(&users)
db.Preload("Posts", "published = ?", true).Find(&users)
```

### Subqueries

```go
// Subquery in Where
db.Where("amount > (?)", db.Table("orders").Select("AVG(amount)")).Find(&orders)

// Subquery in From
db.Table("(?) as u", db.Model(&User{}).Select("name", "age")).Find(&results)
```

### Raw SQL

```go
// Raw query
db.Raw("SELECT name, age FROM users WHERE name = ?", "John").Scan(&users)

// Exec raw SQL
db.Exec("UPDATE users SET age = ? WHERE name = ?", 30, "John")

// Named arguments
db.Raw("SELECT * FROM users WHERE name = @name AND age = @age",
    sql.Named("name", "John"),
    sql.Named("age", 30),
).Scan(&users)
```

### Transactions

```go
// Manual transaction
tx := db.Begin()

if err := tx.Create(&user).Error; err != nil {
    tx.Rollback()
    return err
}

if err := tx.Create(&profile).Error; err != nil {
    tx.Rollback()
    return err
}

tx.Commit()

// Transaction with closure
err := db.Transaction(func(tx *gorm.DB) error {
    if err := tx.Create(&user).Error; err != nil {
        return err
    }
    
    if err := tx.Create(&profile).Error; err != nil {
        return err
    }
    
    return nil
})
```

### Scopes

```go
// Define scope
func ActiveUsers(db *gorm.DB) *gorm.DB {
    return db.Where("active = ?", true)
}

func AgeGreaterThan(age int) func(db *gorm.DB) *gorm.DB {
    return func(db *gorm.DB) *gorm.DB {
        return db.Where("age > ?", age)
    }
}

// Use scopes
db.Scopes(ActiveUsers, AgeGreaterThan(18)).Find(&users)
```

## Hooks

```go
// Before Create
func (u *User) BeforeCreate(tx *gorm.DB) error {
    u.ID = uuid.New()
    return nil
}

// After Create
func (u *User) AfterCreate(tx *gorm.DB) error {
    // Send welcome email
    return nil
}

// Before Update
func (u *User) BeforeUpdate(tx *gorm.DB) error {
    if u.Email != "" {
        // Validate email
    }
    return nil
}

// After Update
func (u *User) AfterUpdate(tx *gorm.DB) error {
    // Clear cache
    return nil
}

// Before Delete
func (u *User) BeforeDelete(tx *gorm.DB) error {
    // Check if user has active orders
    return nil
}

// After Delete
func (u *User) AfterDelete(tx *gorm.DB) error {
    // Delete related records
    return nil
}
```

## Migrations

```go
// Auto migrate
db.AutoMigrate(&User{}, &Post{}, &Profile{})

// Create table
db.Migrator().CreateTable(&User{})

// Drop table
db.Migrator().DropTable(&User{})

// Check if table exists
db.Migrator().HasTable(&User{})

// Add column
db.Migrator().AddColumn(&User{}, "nickname")

// Drop column
db.Migrator().DropColumn(&User{}, "nickname")

// Rename column
db.Migrator().RenameColumn(&User{}, "name", "full_name")

// Create index
db.Migrator().CreateIndex(&User{}, "Email")

// Drop index
db.Migrator().DropIndex(&User{}, "Email")
```

## Performance Tips

### 1. Use Indexes

```go
type User struct {
    Email string `gorm:"uniqueIndex"`
    Name  string `gorm:"index"`
}
```

### 2. Select Only Needed Fields

```go
db.Select("id", "name").Find(&users)
```

### 3. Use Batch Processing

```go
// Find in batches
db.Where("active = ?", true).FindInBatches(&users, 100, func(tx *gorm.DB, batch int) error {
    for _, user := range users {
        // Process user
    }
    return nil
})
```

### 4. Use Prepared Statements

```go
stmt := db.Session(&gorm.Session{PrepareStmt: true})
for i := 0; i < 100; i++ {
    stmt.Create(&User{Name: fmt.Sprintf("user%d", i)})
}
```

### 5. Eager Loading

```go
// N+1 problem
db.Find(&users)
for _, user := range users {
    db.Model(&user).Association("Posts").Find(&user.Posts) // N queries
}

// Solution: Preload
db.Preload("Posts").Find(&users) // 2 queries
```

## Common Patterns

### Repository Pattern

```go
type UserRepository interface {
    Create(user *User) error
    FindByID(id uint) (*User, error)
    FindAll(limit, offset int) ([]*User, error)
    Update(user *User) error
    Delete(id uint) error
}

type userRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) UserRepository {
    return &userRepository{db: db}
}

func (r *userRepository) Create(user *User) error {
    return r.db.Create(user).Error
}

func (r *userRepository) FindByID(id uint) (*User, error) {
    var user User
    if err := r.db.First(&user, id).Error; err != nil {
        return nil, err
    }
    return &user, nil
}
```

### Pagination

```go
type Pagination struct {
    Limit  int
    Offset int
    Total  int64
}

func Paginate(p *Pagination) func(db *gorm.DB) *gorm.DB {
    return func(db *gorm.DB) *gorm.DB {
        return db.Offset(p.Offset).Limit(p.Limit)
    }
}

// Usage
var users []User
var total int64

db.Model(&User{}).Count(&total)
db.Scopes(Paginate(&Pagination{Limit: 10, Offset: 0})).Find(&users)
```

## Error Handling

```go
import "errors"

// Check if record not found
if errors.Is(err, gorm.ErrRecordNotFound) {
    // Handle not found
}

// Check if duplicate key
if errors.Is(err, gorm.ErrDuplicatedKey) {
    // Handle duplicate
}

// Get affected rows
result := db.Create(&user)
if result.Error != nil {
    return result.Error
}
fmt.Println("Rows affected:", result.RowsAffected)
```

## References

- [GORM Documentation](https://gorm.io/docs/)
- [GORM Gen](https://gorm.io/gen/) - Type-safe query builder
- [GORM Playground](https://gorm.io/play.html)

