#!/usr/bin/env python3
"""
Validate the React Developer skill structure and files.
"""

import os
import sys
from pathlib import Path


def check_file_exists(file_path: Path, name: str) -> bool:
    """Check if a file exists."""
    if file_path.exists():
        print(f"✓ {name}: {file_path}")
        return True
    else:
        print(f"✗ {name}: {file_path} (NOT FOUND)")
        return False


def check_directory_exists(dir_path: Path, name: str) -> bool:
    """Check if a directory exists."""
    if dir_path.is_dir():
        print(f"✓ {name}: {dir_path}")
        return True
    else:
        print(f"✗ {name}: {dir_path} (NOT FOUND)")
        return False


def validate_skill_structure(skill_path: Path) -> bool:
    """Validate the skill directory structure."""
    print("\n=== Validating Skill Structure ===\n")
    
    checks = []
    
    # Check required files
    print("Required Files:")
    checks.append(check_file_exists(skill_path / "SKILL.md", "SKILL.md"))
    checks.append(check_file_exists(skill_path / "README.md", "README.md"))
    
    # Check scripts
    print("\nScripts:")
    checks.append(check_file_exists(skill_path / "scripts/init_project.py", "init_project.py"))
    checks.append(check_file_exists(skill_path / "scripts/add_component.py", "add_component.py"))
    checks.append(check_file_exists(skill_path / "scripts/generate_page.py", "generate_page.py"))
    checks.append(check_file_exists(skill_path / "scripts/generate_component.py", "generate_component.py"))
    checks.append(check_file_exists(skill_path / "scripts/generate_hook.py", "generate_hook.py"))
    
    # Check directories
    print("\nDirectories:")
    checks.append(check_directory_exists(skill_path / "scripts", "Scripts directory"))
    checks.append(check_directory_exists(skill_path / "references", "References directory"))
    checks.append(check_directory_exists(skill_path / "examples", "Examples directory"))
    
    return all(checks)


def validate_skill_md(skill_path: Path) -> bool:
    """Validate SKILL.md format."""
    print("\n=== Validating SKILL.md ===\n")
    
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
    else:
        print("✗ YAML frontmatter not found")
        checks.append(False)
    
    # Check for required fields in frontmatter
    required_fields = ["name", "description"]
    for field in required_fields:
        if f"{field}:" in content[:500]:
            print(f"✓ '{field}' field found")
            checks.append(True)
        else:
            print(f"✗ '{field}' field not found")
            checks.append(False)
    
    # Check for required sections
    required_sections = [
        "# React Developer Skill",
        "## Overview",
        "## Tech Stack",
        "## Scripts",
        "## Usage Guidelines",
    ]
    
    for section in required_sections:
        if section in content:
            print(f"✓ Section found: {section}")
            checks.append(True)
        else:
            print(f"✗ Section not found: {section}")
            checks.append(False)
    
    return all(checks)


def validate_scripts(skill_path: Path) -> bool:
    """Validate that scripts are executable and have correct shebang."""
    print("\n=== Validating Scripts ===\n")
    
    scripts = [
        "scripts/init_project.py",
        "scripts/add_component.py",
        "scripts/generate_page.py",
        "scripts/generate_component.py",
        "scripts/generate_hook.py",
    ]
    
    checks = []
    
    for script in scripts:
        script_path = skill_path / script
        if not script_path.exists():
            print(f"✗ {script} not found")
            checks.append(False)
            continue
        
        # Check if executable
        if os.access(script_path, os.X_OK):
            print(f"✓ {script} is executable")
            checks.append(True)
        else:
            print(f"✗ {script} is not executable")
            checks.append(False)
        
        # Check shebang
        with open(script_path, 'r') as f:
            first_line = f.readline().strip()
            if first_line.startswith("#!") and "python" in first_line:
                print(f"✓ {script} has correct shebang")
                checks.append(True)
            else:
                print(f"✗ {script} has incorrect or missing shebang")
                checks.append(False)
    
    return all(checks)


def validate_documentation(skill_path: Path) -> bool:
    """Validate documentation files."""
    print("\n=== Validating Documentation ===\n")
    
    readme = skill_path / "README.md"
    if not readme.exists():
        print("✗ README.md not found")
        return False
    
    content = readme.read_text()
    checks = []
    
    # Check for required sections
    required_sections = [
        "# React Developer Skill",
        "## Features",
        "## Quick Start",
        "## Scripts",
        "## Project Structure",
    ]
    
    for section in required_sections:
        if section in content:
            print(f"✓ README section: {section}")
            checks.append(True)
        else:
            print(f"✗ README section not found: {section}")
            checks.append(False)
    
    return all(checks)


def main():
    # Get skill directory
    skill_path = Path(__file__).parent.parent
    
    print("=" * 50)
    print("REACT DEVELOPER SKILL VALIDATOR")
    print("=" * 50)
    
    # Run validations
    results = {
        "Skill Structure": validate_skill_structure(skill_path),
        "SKILL.md Format": validate_skill_md(skill_path),
        "Scripts": validate_scripts(skill_path),
        "Documentation": validate_documentation(skill_path),
    }
    
    # Print summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
    
    print("-" * 50)
    passed_count = sum(results.values())
    total_count = len(results)
    print(f"Total: {passed_count}/{total_count} checks passed")
    print("-" * 50)
    
    if all(results.values()):
        print("\n🎉 All validations passed! Skill is ready to use.")
        print("\nNext steps:")
        print("  1. Test init_project.py by creating a sample project")
        print("  2. Test add_component.py by adding components")
        print("  3. Test generate_page.py by generating a page")
        print("\nExample:")
        print("  python ~/.claude/skills/react-developer/scripts/init_project.py test-app")
        print("  cd test-app")
        print("  python ~/.claude/skills/react-developer/scripts/add_component.py button card")
        return 0
    else:
        print("\n❌ Some validations failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

