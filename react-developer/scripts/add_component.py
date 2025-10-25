#!/usr/bin/env python3
"""
Add shadcn/ui components to your React project.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


# Popular shadcn/ui components
POPULAR_COMPONENTS = {
    "button": "Button component for user interactions",
    "card": "Card component for content containers",
    "dialog": "Dialog/Modal component for overlays",
    "input": "Input component for forms",
    "label": "Label component for form fields",
    "select": "Select dropdown component",
    "checkbox": "Checkbox component",
    "radio-group": "Radio button group component",
    "switch": "Toggle switch component",
    "textarea": "Textarea component for multi-line input",
    "form": "Form component with validation",
    "table": "Table component for data display",
    "dropdown-menu": "Dropdown menu component",
    "toast": "Toast notification component",
    "alert": "Alert component for messages",
    "badge": "Badge component for labels",
    "avatar": "Avatar component for user images",
    "skeleton": "Skeleton loader component",
    "tabs": "Tabs component for navigation",
    "accordion": "Accordion component for collapsible content",
    "alert-dialog": "Alert dialog for confirmations",
    "popover": "Popover component for tooltips",
    "tooltip": "Tooltip component",
    "sheet": "Sheet/Drawer component",
    "calendar": "Calendar date picker",
    "command": "Command palette component",
    "context-menu": "Context menu component",
    "hover-card": "Hover card component",
    "menubar": "Menubar component",
    "navigation-menu": "Navigation menu component",
    "progress": "Progress bar component",
    "scroll-area": "Scroll area component",
    "separator": "Separator/Divider component",
    "slider": "Slider component",
    "sonner": "Sonner toast notifications",
    "pagination": "Pagination component",
}


def run_command(command: str, cwd: Path = None, shell: bool = True) -> bool:
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


def add_component(project_path: Path, component: str) -> bool:
    """Add a shadcn/ui component."""
    print(f"\n✨ Adding {component} component...\n")
    
    command = f"npx shadcn@latest add {component} -y"
    return run_command(command, cwd=project_path)


def add_components_batch(project_path: Path, components: List[str]) -> bool:
    """Add multiple shadcn/ui components."""
    print(f"\n✨ Adding {len(components)} components...\n")
    
    components_str = " ".join(components)
    command = f"npx shadcn@latest add {components_str} -y"
    return run_command(command, cwd=project_path)


def add_from_registry(project_path: Path, registry_url: str) -> bool:
    """Add component from custom registry."""
    print(f"\n✨ Adding component from registry: {registry_url}\n")
    
    command = f"npx shadcn@latest add {registry_url}"
    return run_command(command, cwd=project_path)


def list_components():
    """List available popular components."""
    print("\n📦 Popular shadcn/ui Components:\n")
    
    for component, description in POPULAR_COMPONENTS.items():
        print(f"  • {component:<20} - {description}")
    
    print("\n💡 Usage:")
    print("  python ~/.claude/skills/react-developer/scripts/add_component.py button")
    print("  python ~/.claude/skills/react-developer/scripts/add_component.py button card dialog")
    print("  python ~/.claude/skills/react-developer/scripts/add_component.py --all-forms")
    print("  python ~/.claude/skills/react-developer/scripts/add_component.py --registry https://www.shadcn.io/registry/ai.json")


def add_preset_group(project_path: Path, group: str) -> bool:
    """Add a preset group of components."""
    presets = {
        "forms": ["button", "input", "label", "select", "checkbox", "radio-group", "switch", "textarea", "form"],
        "data": ["table", "card", "badge", "avatar", "skeleton", "pagination"],
        "overlay": ["dialog", "alert-dialog", "sheet", "popover", "tooltip", "hover-card"],
        "navigation": ["tabs", "accordion", "dropdown-menu", "menubar", "navigation-menu", "command"],
        "feedback": ["alert", "toast", "sonner", "progress"],
        "layout": ["separator", "scroll-area", "resizable", "aspect-ratio"],
        "essential": ["button", "card", "input", "label", "dialog", "alert", "toast"],
    }
    
    if group not in presets:
        print(f"✗ Unknown preset group: {group}")
        print(f"Available groups: {', '.join(presets.keys())}")
        return False
    
    components = presets[group]
    print(f"\n✨ Adding {group} preset ({len(components)} components)...\n")
    
    return add_components_batch(project_path, components)


def main():
    parser = argparse.ArgumentParser(description="Add shadcn/ui components to your React project")
    parser.add_argument("components", nargs="*", help="Component names to add")
    parser.add_argument("--project-path", default=".", help="Path to project root")
    parser.add_argument("--list", action="store_true", help="List available components")
    parser.add_argument("--registry", help="Add component from custom registry URL")
    parser.add_argument("--preset", choices=["forms", "data", "overlay", "navigation", "feedback", "layout", "essential"],
                       help="Add a preset group of components")
    
    # Preset shortcuts
    parser.add_argument("--all-forms", action="store_true", help="Add all form components")
    parser.add_argument("--all-data", action="store_true", help="Add all data display components")
    parser.add_argument("--all-overlay", action="store_true", help="Add all overlay components")
    parser.add_argument("--essential", action="store_true", help="Add essential components")
    
    args = parser.parse_args()
    
    # List components
    if args.list:
        list_components()
        return
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"✗ Error: Project path '{args.project_path}' does not exist")
        sys.exit(1)
    
    # Check if it's a valid project
    if not (project_path / "package.json").exists():
        print(f"✗ Error: Not a valid Node.js project (package.json not found)")
        sys.exit(1)
    
    # Add from registry
    if args.registry:
        if add_from_registry(project_path, args.registry):
            print("\n✅ Component added successfully!")
        else:
            print("\n✗ Failed to add component from registry")
            sys.exit(1)
        return
    
    # Add preset groups
    if args.preset:
        if add_preset_group(project_path, args.preset):
            print(f"\n✅ {args.preset} preset added successfully!")
        else:
            sys.exit(1)
        return
    
    # Preset shortcuts
    if args.all_forms:
        if add_preset_group(project_path, "forms"):
            print("\n✅ All form components added successfully!")
        else:
            sys.exit(1)
        return
    
    if args.all_data:
        if add_preset_group(project_path, "data"):
            print("\n✅ All data components added successfully!")
        else:
            sys.exit(1)
        return
    
    if args.all_overlay:
        if add_preset_group(project_path, "overlay"):
            print("\n✅ All overlay components added successfully!")
        else:
            sys.exit(1)
        return
    
    if args.essential:
        if add_preset_group(project_path, "essential"):
            print("\n✅ Essential components added successfully!")
        else:
            sys.exit(1)
        return
    
    # Add individual components
    if not args.components:
        print("✗ Error: No components specified")
        print("\nUsage:")
        print("  python ~/.claude/skills/react-developer/scripts/add_component.py button")
        print("  python ~/.claude/skills/react-developer/scripts/add_component.py button card dialog")
        print("  python ~/.claude/skills/react-developer/scripts/add_component.py --list")
        print("  python ~/.claude/skills/react-developer/scripts/add_component.py --preset essential")
        sys.exit(1)
    
    # Add components
    if len(args.components) == 1:
        if add_component(project_path, args.components[0]):
            print(f"\n✅ {args.components[0]} component added successfully!")
        else:
            print(f"\n✗ Failed to add {args.components[0]} component")
            sys.exit(1)
    else:
        if add_components_batch(project_path, args.components):
            print(f"\n✅ {len(args.components)} components added successfully!")
        else:
            print("\n✗ Failed to add components")
            sys.exit(1)


if __name__ == "__main__":
    main()

