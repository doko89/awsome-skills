#!/usr/bin/env python3
"""
Generate domain components for a Gin DDD project.

Usage:
    python ~/.claude/skills/gin-developer/scripts/generate_domain.py <domain-name> [--fields <field1:type1,field2:type2>] [--project-path <path>]

Example:
    python ~/.claude/skills/gin-developer/scripts/generate_domain.py user --fields "name:string,email:string,age:int,active:bool"
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class Field:
    """Represents a field in the domain entity."""
    
    def __init__(self, name: str, field_type: str):
        self.name = name
        self.field_type = field_type
        self.go_type = self._map_type(field_type)
        self.json_tag = self._to_snake_case(name)
        self.gorm_tag = self._generate_gorm_tag()
    
    def _map_type(self, field_type: str) -> str:
        """Map field type to Go type."""
        type_mapping = {
            "string": "string",
            "int": "int",
            "int64": "int64",
            "float64": "float64",
            "bool": "bool",
            "time": "time.Time",
            "uuid": "uuid.UUID",
        }
        return type_mapping.get(field_type.lower(), "string")
    
    def _to_snake_case(self, name: str) -> str:
        """Convert camelCase to snake_case."""
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append('_')
            result.append(char.lower())
        return ''.join(result)
    
    def _generate_gorm_tag(self) -> str:
        """Generate GORM tag based on field type."""
        if self.field_type == "string":
            return "type:varchar(255)"
        elif self.field_type in ["int", "int64"]:
            return "type:bigint"
        elif self.field_type == "float64":
            return "type:decimal(10,2)"
        elif self.field_type == "bool":
            return "type:boolean;default:false"
        elif self.field_type == "time":
            return "type:timestamp"
        elif self.field_type == "uuid":
            return "type:uuid"
        return ""
    
    def to_struct_field(self) -> str:
        """Generate struct field definition."""
        return f'\t{self.name.capitalize()} {self.go_type} `json:"{self.json_tag}" gorm:"{self.gorm_tag}"`'


def parse_fields(fields_str: str) -> List[Field]:
    """Parse fields string into Field objects."""
    if not fields_str:
        return []
    
    fields = []
    for field_def in fields_str.split(','):
        field_def = field_def.strip()
        if ':' not in field_def:
            continue
        
        name, field_type = field_def.split(':', 1)
        fields.append(Field(name.strip(), field_type.strip()))
    
    return fields


def capitalize(s: str) -> str:
    """Capitalize first letter."""
    return s[0].upper() + s[1:] if s else s


def to_snake_case(s: str) -> str:
    """Convert to snake_case."""
    result = []
    for i, char in enumerate(s):
        if char.isupper() and i > 0:
            result.append('_')
        result.append(char.lower())
    return ''.join(result)


def generate_entity(domain_name: str, fields: List[Field], module_path: str) -> str:
    """Generate entity file content."""
    entity_name = capitalize(domain_name)
    
    # Check if we need time or uuid imports
    needs_time = any(f.field_type == "time" for f in fields)
    needs_uuid = any(f.field_type == "uuid" for f in fields)
    
    imports = []
    if needs_time:
        imports.append('\t"time"')
    if needs_uuid:
        imports.append('\t"github.com/google/uuid"')
    
    import_block = ""
    if imports:
        import_block = "import (\n" + "\n".join(imports) + "\n)\n\n"
    
    fields_str = "\n".join([f.to_struct_field() for f in fields])
    
    content = f"""package entity

{import_block}type {entity_name} struct {{
	ID        uint   `json:"id" gorm:"primaryKey"`
{fields_str}
	CreatedAt time.Time `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt time.Time `json:"updated_at" gorm:"autoUpdateTime"`
}}

func (e *{entity_name}) TableName() string {{
	return "{to_snake_case(domain_name)}s"
}}
"""
    return content


def generate_repository_interface(domain_name: str, module_path: str) -> str:
    """Generate repository interface file content."""
    entity_name = capitalize(domain_name)
    
    content = f"""package repository

import (
	"{module_path}/internal/domain/entity"
)

type {entity_name}Repository interface {{
	Create(e *entity.{entity_name}) error
	FindByID(id uint) (*entity.{entity_name}, error)
	FindAll(limit, offset int) ([]*entity.{entity_name}, error)
	Update(e *entity.{entity_name}) error
	Delete(id uint) error
	Count() (int64, error)
}}
"""
    return content


def generate_repository_impl(domain_name: str, module_path: str) -> str:
    """Generate repository implementation file content."""
    entity_name = capitalize(domain_name)
    repo_name = f"{entity_name}Repository"
    
    content = f"""package repository

import (
	"gorm.io/gorm"
	"{module_path}/internal/domain/entity"
	"{module_path}/internal/domain/repository"
)

type {repo_name.lower()} struct {{
	db *gorm.DB
}}

func New{repo_name}(db *gorm.DB) repository.{repo_name} {{
	return &{repo_name.lower()}{{db: db}}
}}

func (r *{repo_name.lower()}) Create(e *entity.{entity_name}) error {{
	return r.db.Create(e).Error
}}

func (r *{repo_name.lower()}) FindByID(id uint) (*entity.{entity_name}, error) {{
	var entity entity.{entity_name}
	if err := r.db.First(&entity, id).Error; err != nil {{
		return nil, err
	}}
	return &entity, nil
}}

func (r *{repo_name.lower()}) FindAll(limit, offset int) ([]*entity.{entity_name}, error) {{
	var entities []*entity.{entity_name}
	query := r.db.Model(&entity.{entity_name}{{}})
	
	if limit > 0 {{
		query = query.Limit(limit)
	}}
	if offset > 0 {{
		query = query.Offset(offset)
	}}
	
	if err := query.Find(&entities).Error; err != nil {{
		return nil, err
	}}
	return entities, nil
}}

func (r *{repo_name.lower()}) Update(e *entity.{entity_name}) error {{
	return r.db.Save(e).Error
}}

func (r *{repo_name.lower()}) Delete(id uint) error {{
	return r.db.Delete(&entity.{entity_name}{{}}, id).Error
}}

func (r *{repo_name.lower()}) Count() (int64, error) {{
	var count int64
	if err := r.db.Model(&entity.{entity_name}{{}}).Count(&count).Error; err != nil {{
		return 0, err
	}}
	return count, nil
}}
"""
    return content


def generate_usecase(domain_name: str, module_path: str) -> str:
    """Generate use case file content."""
    entity_name = capitalize(domain_name)
    usecase_name = f"{entity_name}UseCase"
    
    content = f"""package usecase

import (
	"fmt"
	
	"{module_path}/internal/domain/entity"
	"{module_path}/internal/domain/repository"
)

type {usecase_name} interface {{
	Create(e *entity.{entity_name}) error
	GetByID(id uint) (*entity.{entity_name}, error)
	GetAll(limit, offset int) ([]*entity.{entity_name}, int64, error)
	Update(id uint, e *entity.{entity_name}) error
	Delete(id uint) error
}}

type {usecase_name.lower()} struct {{
	repo repository.{entity_name}Repository
}}

func New{usecase_name}(repo repository.{entity_name}Repository) {usecase_name} {{
	return &{usecase_name.lower()}{{repo: repo}}
}}

func (u *{usecase_name.lower()}) Create(e *entity.{entity_name}) error {{
	// Add business logic here
	if err := u.repo.Create(e); err != nil {{
		return fmt.Errorf("failed to create {domain_name}: %w", err)
	}}
	return nil
}}

func (u *{usecase_name.lower()}) GetByID(id uint) (*entity.{entity_name}, error) {{
	entity, err := u.repo.FindByID(id)
	if err != nil {{
		return nil, fmt.Errorf("failed to get {domain_name}: %w", err)
	}}
	return entity, nil
}}

func (u *{usecase_name.lower()}) GetAll(limit, offset int) ([]*entity.{entity_name}, int64, error) {{
	entities, err := u.repo.FindAll(limit, offset)
	if err != nil {{
		return nil, 0, fmt.Errorf("failed to get {domain_name}s: %w", err)
	}}
	
	count, err := u.repo.Count()
	if err != nil {{
		return nil, 0, fmt.Errorf("failed to count {domain_name}s: %w", err)
	}}
	
	return entities, count, nil
}}

func (u *{usecase_name.lower()}) Update(id uint, e *entity.{entity_name}) error {{
	// Check if exists
	existing, err := u.repo.FindByID(id)
	if err != nil {{
		return fmt.Errorf("failed to find {domain_name}: %w", err)
	}}
	
	// Update fields
	e.ID = existing.ID
	e.CreatedAt = existing.CreatedAt
	
	if err := u.repo.Update(e); err != nil {{
		return fmt.Errorf("failed to update {domain_name}: %w", err)
	}}
	return nil
}}

func (u *{usecase_name.lower()}) Delete(id uint) error {{
	// Check if exists
	if _, err := u.repo.FindByID(id); err != nil {{
		return fmt.Errorf("failed to find {domain_name}: %w", err)
	}}
	
	if err := u.repo.Delete(id); err != nil {{
		return fmt.Errorf("failed to delete {domain_name}: %w", err)
	}}
	return nil
}}
"""
    return content


def generate_handler(domain_name: str, module_path: str) -> str:
    """Generate handler file content."""
    entity_name = capitalize(domain_name)
    handler_name = f"{entity_name}Handler"
    
    content = f"""package handler

import (
	"net/http"
	"strconv"
	
	"github.com/gin-gonic/gin"
	"{module_path}/internal/domain/entity"
	"{module_path}/internal/usecase"
	"{module_path}/pkg/response"
)

type {handler_name} struct {{
	useCase usecase.{entity_name}UseCase
}}

func New{handler_name}(useCase usecase.{entity_name}UseCase) *{handler_name} {{
	return &{handler_name}{{useCase: useCase}}
}}

func (h *{handler_name}) RegisterRoutes(router *gin.RouterGroup) {{
	{domain_name}s := router.Group("/{to_snake_case(domain_name)}s")
	{{
		{domain_name}s.POST("", h.Create)
		{domain_name}s.GET("", h.GetAll)
		{domain_name}s.GET("/:id", h.GetByID)
		{domain_name}s.PUT("/:id", h.Update)
		{domain_name}s.DELETE("/:id", h.Delete)
	}}
}}

func (h *{handler_name}) Create(c *gin.Context) {{
	var req entity.{entity_name}
	if err := c.ShouldBindJSON(&req); err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid request body", err)
		return
	}}
	
	if err := h.useCase.Create(&req); err != nil {{
		response.Error(c, http.StatusInternalServerError, "Failed to create {domain_name}", err)
		return
	}}
	
	response.Success(c, http.StatusCreated, "{entity_name} created successfully", req)
}}

func (h *{handler_name}) GetByID(c *gin.Context) {{
	id, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid ID", err)
		return
	}}
	
	entity, err := h.useCase.GetByID(uint(id))
	if err != nil {{
		response.Error(c, http.StatusNotFound, "{entity_name} not found", err)
		return
	}}
	
	response.Success(c, http.StatusOK, "{entity_name} retrieved successfully", entity)
}}

func (h *{handler_name}) GetAll(c *gin.Context) {{
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "10"))
	offset, _ := strconv.Atoi(c.DefaultQuery("offset", "0"))
	
	entities, total, err := h.useCase.GetAll(limit, offset)
	if err != nil {{
		response.Error(c, http.StatusInternalServerError, "Failed to get {domain_name}s", err)
		return
	}}
	
	response.Success(c, http.StatusOK, "{entity_name}s retrieved successfully", gin.H{{
		"items": entities,
		"total": total,
		"limit": limit,
		"offset": offset,
	}})
}}

func (h *{handler_name}) Update(c *gin.Context) {{
	id, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid ID", err)
		return
	}}
	
	var req entity.{entity_name}
	if err := c.ShouldBindJSON(&req); err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid request body", err)
		return
	}}
	
	if err := h.useCase.Update(uint(id), &req); err != nil {{
		response.Error(c, http.StatusInternalServerError, "Failed to update {domain_name}", err)
		return
	}}
	
	response.Success(c, http.StatusOK, "{entity_name} updated successfully", req)
}}

func (h *{handler_name}) Delete(c *gin.Context) {{
	id, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {{
		response.Error(c, http.StatusBadRequest, "Invalid ID", err)
		return
	}}
	
	if err := h.useCase.Delete(uint(id)); err != nil {{
		response.Error(c, http.StatusInternalServerError, "Failed to delete {domain_name}", err)
		return
	}}
	
	response.Success(c, http.StatusOK, "{entity_name} deleted successfully", nil)
}}
"""
    return content


def main():
    parser = argparse.ArgumentParser(description="Generate domain components for Gin DDD project")
    parser.add_argument("domain_name", help="Name of the domain (e.g., user, product)")
    parser.add_argument("--fields", help="Comma-separated fields (e.g., name:string,age:int)", default="")
    parser.add_argument("--project-path", help="Path to the project root", default=".")
    
    args = parser.parse_args()
    
    domain_name = args.domain_name.lower()
    project_path = Path(args.project_path)
    
    # Parse fields
    fields = parse_fields(args.fields)
    
    # Read go.mod to get module path
    go_mod_path = project_path / "go.mod"
    if not go_mod_path.exists():
        print("Error: go.mod not found. Make sure you're in the project root.")
        sys.exit(1)
    
    module_path = ""
    with open(go_mod_path, 'r') as f:
        for line in f:
            if line.startswith('module '):
                module_path = line.split()[1].strip()
                break
    
    if not module_path:
        print("Error: Could not determine module path from go.mod")
        sys.exit(1)
    
    print(f"\n🚀 Generating domain: {domain_name}")
    print(f"📦 Module path: {module_path}")
    print(f"📝 Fields: {len(fields)}\n")
    
    # Generate files
    entity_name = capitalize(domain_name)
    
    # Entity
    entity_path = project_path / "internal/domain/entity" / f"{domain_name}.go"
    entity_path.write_text(generate_entity(domain_name, fields, module_path))
    print(f"✓ Created entity: {entity_path}")
    
    # Repository interface
    repo_interface_path = project_path / "internal/domain/repository" / f"{domain_name}_repository.go"
    repo_interface_path.write_text(generate_repository_interface(domain_name, module_path))
    print(f"✓ Created repository interface: {repo_interface_path}")
    
    # Repository implementation
    repo_impl_path = project_path / "internal/infrastructure/repository" / f"{domain_name}_repository.go"
    repo_impl_path.write_text(generate_repository_impl(domain_name, module_path))
    print(f"✓ Created repository implementation: {repo_impl_path}")
    
    # Use case
    usecase_path = project_path / "internal/usecase" / f"{domain_name}_usecase.go"
    usecase_path.write_text(generate_usecase(domain_name, module_path))
    print(f"✓ Created use case: {usecase_path}")
    
    # Handler
    handler_path = project_path / "internal/handler" / f"{domain_name}_handler.go"
    handler_path.write_text(generate_handler(domain_name, module_path))
    print(f"✓ Created handler: {handler_path}")
    
    print(f"\n✅ Domain '{domain_name}' generated successfully!")
    print(f"\nNext steps:")
    print(f"  1. Add migration in cmd/api/main.go:")
    print(f"     db.AutoMigrate(&entity.{entity_name}{{}})")
    print(f"  2. Register routes in cmd/api/main.go:")
    print(f"     {domain_name}Repo := repository.New{entity_name}Repository(db)")
    print(f"     {domain_name}UseCase := usecase.New{entity_name}UseCase({domain_name}Repo)")
    print(f"     {domain_name}Handler := handler.New{entity_name}Handler({domain_name}UseCase)")
    print(f"     {domain_name}Handler.RegisterRoutes(v1)")
    print(f"  3. Run: go mod tidy")
    print(f"  4. Test endpoints at: http://localhost:8080/api/v1/{to_snake_case(domain_name)}s")


if __name__ == "__main__":
    main()

