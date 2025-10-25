#!/usr/bin/env python3
"""
Validate the gin-developer skill structure and scripts.

Usage:
    python validate_skill.py
"""

import os
import sys
from pathlib import Path


def check_file_exists(file_path: Path, description: str) -> bool:
    """Check if a file exists."""
    if file_path.exists():
        print(f"✓ {description}: {file_path}")
        return True
    else:
        print(f"✗ {description}: {file_path} (NOT FOUND)")
        return False


def check_directory_exists(dir_path: Path, description: str) -> bool:
    """Check if a directory exists."""
    if dir_path.exists() and dir_path.is_dir():
        print(f"✓ {description}: {dir_path}")
        return True
    else:
        print(f"✗ {description}: {dir_path} (NOT FOUND)")
        return False


def validate_skill_structure():
    """Validate the skill directory structure."""
    print("\n=== Validating Skill Structure ===\n")
    
    skill_path = Path(__file__).parent.parent
    checks = []
    
    # Check required files
    print("Required Files:")
    checks.append(check_file_exists(skill_path / "SKILL.md", "SKILL.md"))
    checks.append(check_file_exists(skill_path / "README.md", "README.md"))
    
    # Check scripts
    print("\nScripts:")
    checks.append(check_file_exists(skill_path / "scripts/init_project.py", "init_project.py"))
    checks.append(check_file_exists(skill_path / "scripts/generate_domain.py", "generate_domain.py"))
    checks.append(check_file_exists(skill_path / "scripts/add_auth.py", "add_auth.py"))
    checks.append(check_file_exists(skill_path / "scripts/add_infrastructure.py", "add_infrastructure.py"))
    checks.append(check_file_exists(skill_path / "scripts/add_middleware.py", "add_middleware.py"))
    checks.append(check_file_exists(skill_path / "scripts/generate_docs.py", "generate_docs.py"))
    checks.append(check_file_exists(skill_path / "scripts/helpers.py", "helpers.py"))
    
    # Check references
    print("\nReferences:")
    checks.append(check_file_exists(skill_path / "references/ddd_architecture.md", "DDD Architecture"))
    checks.append(check_file_exists(skill_path / "references/gin_best_practices.md", "Gin Best Practices"))
    checks.append(check_file_exists(skill_path / "references/gorm_examples.md", "GORM Examples"))
    
    # Check examples
    print("\nExamples:")
    checks.append(check_file_exists(skill_path / "examples/complete_example.md", "Complete Example"))
    checks.append(check_file_exists(skill_path / "examples/quick_start.md", "Quick Start"))
    
    # Check directories
    print("\nDirectories:")
    checks.append(check_directory_exists(skill_path / "scripts", "Scripts directory"))
    checks.append(check_directory_exists(skill_path / "references", "References directory"))
    checks.append(check_directory_exists(skill_path / "examples", "Examples directory"))
    
    return all(checks)


def validate_skill_md():
    """Validate SKILL.md format."""
    print("\n=== Validating SKILL.md ===\n")
    
    skill_path = Path(__file__).parent.parent
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        print("✗ SKILL.md not found")
        return False
    
    content = skill_md.read_text()
    checks = []
    
    # Check for YAML frontmatter
    if content.startswith("---"):
        print("✓ YAML frontmatter found")
        checks.append(True)
        
        # Check for required fields
        if "name:" in content:
            print("✓ 'name' field found")
            checks.append(True)
        else:
            print("✗ 'name' field missing")
            checks.append(False)
        
        if "description:" in content:
            print("✓ 'description' field found")
            checks.append(True)
        else:
            print("✗ 'description' field missing")
            checks.append(False)
    else:
        print("✗ YAML frontmatter missing")
        checks.append(False)
    
    # Check for main sections
    sections = [
        "# Gin Developer Skill",
        "## Overview",
        "## Architecture",
        "## Scripts",
        "## Usage Guidelines",
    ]
    
    for section in sections:
        if section in content:
            print(f"✓ Section found: {section}")
            checks.append(True)
        else:
            print(f"✗ Section missing: {section}")
            checks.append(False)
    
    return all(checks)


def validate_scripts():
    """Validate Python scripts."""
    print("\n=== Validating Scripts ===\n")
    
    skill_path = Path(__file__).parent.parent
    checks = []
    
    scripts = [
        "scripts/init_project.py",
        "scripts/generate_domain.py",
        "scripts/add_auth.py",
        "scripts/add_infrastructure.py",
        "scripts/add_middleware.py",
        "scripts/generate_docs.py",
        "scripts/helpers.py",
    ]
    
    for script in scripts:
        script_path = skill_path / script
        if script_path.exists():
            # Check if file is executable
            if os.access(script_path, os.X_OK):
                print(f"✓ {script} is executable")
                checks.append(True)
            else:
                print(f"⚠ {script} is not executable (run: chmod +x {script})")
                checks.append(True)  # Not critical
            
            # Check for shebang
            with open(script_path, 'r') as f:
                first_line = f.readline()
                if first_line.startswith("#!/usr/bin/env python"):
                    print(f"✓ {script} has correct shebang")
                    checks.append(True)
                else:
                    print(f"✗ {script} missing shebang")
                    checks.append(False)
        else:
            print(f"✗ {script} not found")
            checks.append(False)
    
    return all(checks)


def validate_documentation():
    """Validate documentation completeness."""
    print("\n=== Validating Documentation ===\n")
    
    skill_path = Path(__file__).parent.parent
    checks = []
    
    # Check README.md
    readme = skill_path / "README.md"
    if readme.exists():
        content = readme.read_text()
        
        required_sections = [
            "# Gin Developer Skill",
            "## Overview",
            "## Quick Start",
            "## Project Structure",
            "## Scripts",
            "## Architecture",
        ]
        
        for section in required_sections:
            if section in content:
                print(f"✓ README section: {section}")
                checks.append(True)
            else:
                print(f"✗ README missing section: {section}")
                checks.append(False)
    else:
        print("✗ README.md not found")
        checks.append(False)
    
    return all(checks)


def print_summary(results: dict):
    """Print validation summary."""
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check}")
    
    print("\n" + "-" * 50)
    print(f"Total: {passed}/{total} checks passed")
    print("-" * 50)
    
    if passed == total:
        print("\n🎉 All validations passed! Skill is ready to use.")
        return True
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed. Please fix the issues above.")
        return False


def main():
    """Main validation function."""
    print("=" * 50)
    print("GIN DEVELOPER SKILL VALIDATOR")
    print("=" * 50)
    
    results = {
        "Skill Structure": validate_skill_structure(),
        "SKILL.md Format": validate_skill_md(),
        "Scripts": validate_scripts(),
        "Documentation": validate_documentation(),
    }
    
    success = print_summary(results)
    
    if success:
        print("\nNext steps:")
        print("  1. Test init_project.py by creating a sample project")
        print("  2. Test generate_domain.py by generating a domain")
        print("  3. Run the generated project to ensure it works")
        print("\nExample:")
        print("  python scripts/init_project.py test-api --module-path github.com/test/test-api")
        print("  cd test-api")
        print("  python ../scripts/generate_domain.py user --fields 'name:string,email:string'")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

