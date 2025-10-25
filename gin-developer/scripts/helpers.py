#!/usr/bin/env python3
"""
Helper utilities for code generation.
"""

import re
from typing import List


def to_snake_case(text: str) -> str:
    """
    Convert camelCase or PascalCase to snake_case.
    
    Examples:
        userName -> user_name
        UserName -> user_name
        HTTPServer -> http_server
    """
    # Insert underscore before uppercase letters
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    # Insert underscore before uppercase letters that follow lowercase letters
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def to_camel_case(text: str) -> str:
    """
    Convert snake_case to camelCase.
    
    Examples:
        user_name -> userName
        http_server -> httpServer
    """
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_pascal_case(text: str) -> str:
    """
    Convert snake_case to PascalCase.
    
    Examples:
        user_name -> UserName
        http_server -> HttpServer
    """
    return ''.join(x.title() for x in text.split('_'))


def pluralize(word: str) -> str:
    """
    Simple pluralization for English words.
    
    Examples:
        user -> users
        category -> categories
        person -> people (special case)
    """
    special_cases = {
        'person': 'people',
        'child': 'children',
        'man': 'men',
        'woman': 'women',
        'tooth': 'teeth',
        'foot': 'feet',
        'mouse': 'mice',
        'goose': 'geese',
    }
    
    if word.lower() in special_cases:
        return special_cases[word.lower()]
    
    if word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return word + 'es'
    else:
        return word + 's'


def validate_go_identifier(name: str) -> bool:
    """
    Validate if a string is a valid Go identifier.
    
    Rules:
    - Must start with a letter or underscore
    - Can contain letters, digits, and underscores
    - Cannot be a Go keyword
    """
    go_keywords = {
        'break', 'case', 'chan', 'const', 'continue',
        'default', 'defer', 'else', 'fallthrough', 'for',
        'func', 'go', 'goto', 'if', 'import',
        'interface', 'map', 'package', 'range', 'return',
        'select', 'struct', 'switch', 'type', 'var',
    }
    
    if not name:
        return False
    
    if name.lower() in go_keywords:
        return False
    
    if not (name[0].isalpha() or name[0] == '_'):
        return False
    
    return all(c.isalnum() or c == '_' for c in name)


def generate_import_block(imports: List[str]) -> str:
    """
    Generate a formatted import block.
    
    Args:
        imports: List of import paths
        
    Returns:
        Formatted import block string
    """
    if not imports:
        return ""
    
    if len(imports) == 1:
        return f'import "{imports[0]}"\n\n'
    
    import_lines = '\n'.join(f'\t"{imp}"' for imp in imports)
    return f"import (\n{import_lines}\n)\n\n"


def format_go_comment(text: str, indent: int = 0) -> str:
    """
    Format a comment for Go code.
    
    Args:
        text: Comment text
        indent: Number of tabs to indent
        
    Returns:
        Formatted comment string
    """
    indent_str = '\t' * indent
    lines = text.split('\n')
    return '\n'.join(f'{indent_str}// {line}' for line in lines)


def generate_struct_tag(json_name: str, gorm_tags: List[str] = None, validate_tags: List[str] = None) -> str:
    """
    Generate struct tags for Go fields.
    
    Args:
        json_name: JSON field name
        gorm_tags: List of GORM tags
        validate_tags: List of validation tags
        
    Returns:
        Formatted struct tag string
    """
    tags = [f'json:"{json_name}"']
    
    if gorm_tags:
        gorm_str = ';'.join(gorm_tags)
        tags.append(f'gorm:"{gorm_str}"')
    
    if validate_tags:
        validate_str = ','.join(validate_tags)
        tags.append(f'validate:"{validate_str}"')
    
    return '`' + ' '.join(tags) + '`'


class GoTypeMapper:
    """Map common types to Go types."""
    
    TYPE_MAP = {
        'string': 'string',
        'str': 'string',
        'text': 'string',
        
        'int': 'int',
        'integer': 'int',
        'int32': 'int32',
        'int64': 'int64',
        
        'uint': 'uint',
        'uint32': 'uint32',
        'uint64': 'uint64',
        
        'float': 'float64',
        'float32': 'float32',
        'float64': 'float64',
        'decimal': 'float64',
        'number': 'float64',
        
        'bool': 'bool',
        'boolean': 'bool',
        
        'time': 'time.Time',
        'datetime': 'time.Time',
        'timestamp': 'time.Time',
        'date': 'time.Time',
        
        'uuid': 'uuid.UUID',
        'guid': 'uuid.UUID',
        
        'bytes': '[]byte',
        'binary': '[]byte',
    }
    
    @classmethod
    def map_type(cls, type_str: str) -> tuple[str, List[str]]:
        """
        Map a type string to Go type and required imports.
        
        Returns:
            Tuple of (go_type, required_imports)
        """
        type_str = type_str.lower().strip()
        
        # Check for array types
        if type_str.startswith('[]'):
            inner_type = type_str[2:]
            go_type, imports = cls.map_type(inner_type)
            return f'[]{go_type}', imports
        
        # Check for pointer types
        if type_str.startswith('*'):
            inner_type = type_str[1:]
            go_type, imports = cls.map_type(inner_type)
            return f'*{go_type}', imports
        
        go_type = cls.TYPE_MAP.get(type_str, 'string')
        imports = []
        
        if 'time.Time' in go_type:
            imports.append('time')
        elif 'uuid.UUID' in go_type:
            imports.append('github.com/google/uuid')
        
        return go_type, imports


class GormTagGenerator:
    """Generate GORM tags for different field types."""
    
    @staticmethod
    def for_string(max_length: int = 255) -> str:
        """Generate GORM tag for string field."""
        return f"type:varchar({max_length})"
    
    @staticmethod
    def for_text() -> str:
        """Generate GORM tag for text field."""
        return "type:text"
    
    @staticmethod
    def for_int() -> str:
        """Generate GORM tag for integer field."""
        return "type:bigint"
    
    @staticmethod
    def for_float() -> str:
        """Generate GORM tag for float field."""
        return "type:decimal(10,2)"
    
    @staticmethod
    def for_bool(default: bool = False) -> str:
        """Generate GORM tag for boolean field."""
        return f"type:boolean;default:{str(default).lower()}"
    
    @staticmethod
    def for_time() -> str:
        """Generate GORM tag for time field."""
        return "type:timestamp"
    
    @staticmethod
    def for_uuid() -> str:
        """Generate GORM tag for UUID field."""
        return "type:uuid"
    
    @staticmethod
    def for_json() -> str:
        """Generate GORM tag for JSON field."""
        return "type:jsonb"
    
    @staticmethod
    def primary_key() -> str:
        """Generate GORM tag for primary key."""
        return "primaryKey"
    
    @staticmethod
    def unique() -> str:
        """Generate GORM tag for unique constraint."""
        return "unique"
    
    @staticmethod
    def not_null() -> str:
        """Generate GORM tag for not null constraint."""
        return "not null"
    
    @staticmethod
    def index(name: str = "") -> str:
        """Generate GORM tag for index."""
        if name:
            return f"index:{name}"
        return "index"


def generate_crud_methods(entity_name: str) -> dict:
    """
    Generate CRUD method signatures for an entity.
    
    Returns:
        Dictionary with method names and signatures
    """
    return {
        'create': f"Create(e *entity.{entity_name}) error",
        'find_by_id': f"FindByID(id uint) (*entity.{entity_name}, error)",
        'find_all': f"FindAll(limit, offset int) ([]*entity.{entity_name}, error)",
        'update': f"Update(e *entity.{entity_name}) error",
        'delete': f"Delete(id uint) error",
        'count': f"Count() (int64, error)",
    }


def generate_http_methods(entity_name: str, route_prefix: str) -> dict:
    """
    Generate HTTP handler method information.
    
    Returns:
        Dictionary with method info
    """
    snake_name = to_snake_case(entity_name)
    plural_name = pluralize(snake_name)
    
    return {
        'create': {
            'method': 'POST',
            'path': f'/{plural_name}',
            'handler': 'Create',
        },
        'get_all': {
            'method': 'GET',
            'path': f'/{plural_name}',
            'handler': 'GetAll',
        },
        'get_by_id': {
            'method': 'GET',
            'path': f'/{plural_name}/:id',
            'handler': 'GetByID',
        },
        'update': {
            'method': 'PUT',
            'path': f'/{plural_name}/:id',
            'handler': 'Update',
        },
        'delete': {
            'method': 'DELETE',
            'path': f'/{plural_name}/:id',
            'handler': 'Delete',
        },
    }


if __name__ == "__main__":
    # Test functions
    print("Testing helper functions:")
    print(f"to_snake_case('UserName'): {to_snake_case('UserName')}")
    print(f"to_camel_case('user_name'): {to_camel_case('user_name')}")
    print(f"to_pascal_case('user_name'): {to_pascal_case('user_name')}")
    print(f"pluralize('user'): {pluralize('user')}")
    print(f"pluralize('category'): {pluralize('category')}")
    print(f"validate_go_identifier('userName'): {validate_go_identifier('userName')}")
    print(f"validate_go_identifier('123user'): {validate_go_identifier('123user')}")
    
    go_type, imports = GoTypeMapper.map_type('time')
    print(f"GoTypeMapper.map_type('time'): {go_type}, imports: {imports}")

