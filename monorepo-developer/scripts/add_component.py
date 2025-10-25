#!/usr/bin/env python3
"""
Add shadcn/ui components to a frontend package.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(command: str, cwd: Path = None, shell: bool = True):
    """Run a shell command."""
    print(f"Running: {command}")
    result = subprocess.run(
        command,
        shell=shell,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    if result.stdout:
        print(result.stdout)
    
    return True


def list_components():
    """List available shadcn/ui components."""
    components = {
        "forms": ["button", "input", "label", "select", "checkbox", "radio-group", "switch", "textarea", "form"],
        "data": ["table", "card", "badge", "avatar", "skeleton", "pagination"],
        "overlay": ["dialog", "alert-dialog", "sheet", "popover", "tooltip", "hover-card"],
        "navigation": ["tabs", "accordion", "dropdown-menu", "menubar", "navigation-menu", "command"],
        "feedback": ["alert", "toast", "sonner", "progress"],
        "layout": ["separator", "scroll-area", "resizable", "aspect-ratio"],
        "essential": ["button", "card", "input", "label", "dialog", "alert", "toast"]
    }
    
    print("\n📦 Available shadcn/ui Components:\n")
    
    for category, items in components.items():
        print(f"  {category.upper()}")
        for item in items:
            print(f"    - {item}")
        print()
    
    return components


def add_components(package_path: Path, components: list):
    """Add shadcn/ui components to a package."""
    print(f"\n✨ Adding components to {package_path.name}...\n")
    
    for component in components:
        print(f"Adding {component}...")
        command = f"npx shadcn@latest add {component} -y"
        
        if not run_command(command, cwd=package_path):
            print(f"⚠ Failed to add {component}, continuing...")
            continue
        
        print(f"✓ Added {component}\n")
    
    return True


def add_preset(package_path: Path, preset: str):
    """Add a preset group of components."""
    presets = {
        "forms": ["button", "input", "label", "select", "checkbox", "radio-group", "switch", "textarea", "form"],
        "data": ["table", "card", "badge", "avatar", "skeleton", "pagination"],
        "overlay": ["dialog", "alert-dialog", "sheet", "popover", "tooltip", "hover-card"],
        "navigation": ["tabs", "accordion", "dropdown-menu", "menubar", "navigation-menu", "command"],
        "feedback": ["alert", "toast", "sonner", "progress"],
        "layout": ["separator", "scroll-area", "resizable", "aspect-ratio"],
        "essential": ["button", "card", "input", "label", "dialog", "alert", "toast"]
    }
    
    if preset not in presets:
        print(f"✗ Unknown preset: {preset}")
        print(f"Available presets: {', '.join(presets.keys())}")
        return False
    
    components = presets[preset]
    print(f"\n📦 Adding {preset} preset ({len(components)} components)...\n")
    
    return add_components(package_path, components)


def find_frontend_package(project_path: Path, package_name: str = None):
    """Find a frontend package in the monorepo."""
    packages_dir = project_path / "packages"
    
    if not packages_dir.exists():
        print("✗ Not a valid monorepo project (packages directory not found)")
        return None
    
    if package_name:
        package_path = packages_dir / package_name
        if package_path.exists() and (package_path / "components.json").exists():
            return package_path
        else:
            print(f"✗ Frontend package '{package_name}' not found or not configured")
            return None
    
    # Find first frontend package with components.json
    for package_dir in packages_dir.iterdir():
        if package_dir.is_dir() and (package_dir / "components.json").exists():
            return package_dir
    
    print("✗ No frontend package found in monorepo")
    return None


def main():
    parser = argparse.ArgumentParser(description="Add shadcn/ui components to a frontend package")
    parser.add_argument("components", nargs="*", help="Components to add")
    parser.add_argument("--package", help="Target package name")
    parser.add_argument("--project-path", default=".", help="Path to the monorepo project")
    parser.add_argument("--preset", help="Add a preset group of components")
    parser.add_argument("--list", action="store_true", help="List available components")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    
    # List components
    if args.list:
        list_components()
        return
    
    # Find package
    package_path = find_frontend_package(project_path, args.package)
    if not package_path:
        sys.exit(1)
    
    print(f"\n📦 Target package: {package_path.name}\n")
    
    # Add preset
    if args.preset:
        if not add_preset(package_path, args.preset):
            sys.exit(1)
    
    # Add individual components
    if args.components:
        if not add_components(package_path, args.components):
            sys.exit(1)
    
    if not args.preset and not args.components:
        print("✗ Please specify components to add or use --preset")
        print("\nUsage:")
        print("  python scripts/add_component.py button card dialog")
        print("  python scripts/add_component.py --preset forms")
        print("  python scripts/add_component.py --list")
        sys.exit(1)
    
    print(f"\n✅ Components added successfully!\n")


if __name__ == "__main__":
    main()

