#!/usr/bin/env python3
"""
Validate the monorepo-developer skill structure.
"""

import sys
from pathlib import Path


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists."""
    if path.exists():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - NOT FOUND")
        return False


def check_directory_exists(path: Path, description: str) -> bool:
    """Check if a directory exists."""
    if path.is_dir():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - NOT FOUND")
        return False


def validate_skill_md(skill_path: Path) -> bool:
    """Validate SKILL.md file."""
    print("\n📋 Validating SKILL.md...\n")
    
    skill_md = skill_path / "SKILL.md"
    
    if not check_file_exists(skill_md, "SKILL.md"):
        return False
    
    content = skill_md.read_text()
    checks = []
    
    # Check for YAML frontmatter
    if content.startswith("---"):
        print("✓ YAML frontmatter found")
        checks.append(True)
        
        # Check for required fields
        required_fields = ["name:", "description:", "version:", "license:"]
        for field in required_fields:
            if field in content:
                print(f"✓ '{field}' field found")
                checks.append(True)
            else:
                print(f"✗ '{field}' field missing")
                checks.append(False)
    else:
        print("✗ YAML frontmatter missing")
        checks.append(False)
    
    # Check for main sections
    sections = [
        "# Monorepo Developer Skill",
        "## Overview",
        "## Tech Stack",
        "## Project Structure",
        "## Scripts",
        "## Usage Guidelines",
    ]
    
    for section in sections:
        if section in content:
            print(f"✓ Section '{section}' found")
            checks.append(True)
        else:
            print(f"✗ Section '{section}' missing")
            checks.append(False)
    
    return all(checks)


def validate_scripts(skill_path: Path) -> bool:
    """Validate scripts directory."""
    print("\n🔧 Validating scripts...\n")
    
    scripts_dir = skill_path / "scripts"
    
    if not check_directory_exists(scripts_dir, "scripts/ directory"):
        return False
    
    required_scripts = [
        ("init_project.py", "Project initialization script"),
        ("generate_package.py", "Package generation script"),
        ("add_component.py", "Component addition script"),
        ("validate_skill.py", "Skill validation script"),
    ]
    
    checks = []
    for script_name, description in required_scripts:
        script_path = scripts_dir / script_name
        if check_file_exists(script_path, f"{description} ({script_name})"):
            checks.append(True)
        else:
            checks.append(False)
    
    return all(checks)


def validate_documentation(skill_path: Path) -> bool:
    """Validate documentation files."""
    print("\n📚 Validating documentation...\n")
    
    checks = []
    
    # Check README.md
    readme_path = skill_path / "README.md"
    if check_file_exists(readme_path, "README.md"):
        checks.append(True)
    else:
        checks.append(False)
    
    # Check LICENSE
    license_path = skill_path / "LICENSE"
    if check_file_exists(license_path, "LICENSE"):
        checks.append(True)
    else:
        checks.append(False)
    
    return all(checks)


def validate_references(skill_path: Path) -> bool:
    """Validate references directory."""
    print("\n📖 Validating references...\n")
    
    references_dir = skill_path / "references"
    
    if references_dir.exists():
        print(f"✓ references/ directory exists")
        
        # Check for reference files
        ref_files = list(references_dir.glob("*.md"))
        if ref_files:
            print(f"✓ Found {len(ref_files)} reference file(s)")
            for ref_file in ref_files:
                print(f"  - {ref_file.name}")
            return True
        else:
            print("⚠ No reference files found (optional)")
            return True
    else:
        print("⚠ references/ directory not found (optional)")
        return True


def validate_examples(skill_path: Path) -> bool:
    """Validate examples directory."""
    print("\n💡 Validating examples...\n")
    
    examples_dir = skill_path / "examples"
    
    if examples_dir.exists():
        print(f"✓ examples/ directory exists")
        
        # Check for example files
        example_files = list(examples_dir.glob("*.md"))
        if example_files:
            print(f"✓ Found {len(example_files)} example file(s)")
            for example_file in example_files:
                print(f"  - {example_file.name}")
            return True
        else:
            print("⚠ No example files found (optional)")
            return True
    else:
        print("⚠ examples/ directory not found (optional)")
        return True


def print_summary(results: dict) -> bool:
    """Print validation summary."""
    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50 + "\n")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if failed == 0:
        print("\n✅ All validation checks passed!")
        return True
    else:
        print(f"\n❌ {failed} validation check(s) failed")
        return False


def main():
    # Get skill path
    skill_path = Path(__file__).parent.parent
    
    print(f"\n🔍 Validating monorepo-developer skill at {skill_path}\n")
    
    results = {
        "SKILL.md": validate_skill_md(skill_path),
        "Scripts": validate_scripts(skill_path),
        "Documentation": validate_documentation(skill_path),
        "References": validate_references(skill_path),
        "Examples": validate_examples(skill_path),
    }
    
    success = print_summary(results)
    
    if success:
        print("\nNext steps:")
        print("  1. Test init_project.py by creating a sample monorepo")
        print("  2. Test generate_package.py by generating a package")
        print("  3. Test add_component.py by adding components")
        print("\nExample:")
        print("  python ~/.claude/skills/monorepo-developer/scripts/init_project.py test-monorepo")
        print("  cd test-monorepo")
        print("  python ~/.claude/skills/monorepo-developer/scripts/generate_package.py api --type backend")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

