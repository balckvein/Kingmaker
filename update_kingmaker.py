#!/usr/bin/env python3
"""
Script to move remaining Kingmaker files to proper locations
"""

import os
import shutil
from pathlib import Path

def fix_additional_files(base_path: str):
    """Move constants.py and raid_systems.py to proper locations"""
    base = Path(base_path)
    src = base / 'src'
    
    # File mappings for movement
    moves = {
        'constants.py': src / 'core' / 'constants.py',  # Constants go in core
        'raid_systems.py': src / 'systems' / 'combat' / 'raid_systems.py'  # Raid systems go with combat
    }
    
    print("Moving additional files to proper locations...")
    
    try:
        for source_file, dest_path in moves.items():
            source_path = base / source_file
            
            if source_path.exists():
                # Ensure destination directory exists
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move the file
                shutil.move(str(source_path), str(dest_path))
                print(f"Moved {source_file} to {dest_path.relative_to(base)}")
                
                # Update imports in the moved file
                with open(dest_path, 'r') as f:
                    content = f.read()
                
                # Update imports to reflect new structure
                content = content.replace('from constants', 'from src.core.constants')
                content = content.replace('from raid_systems', 'from src.systems.combat.raid_systems')
                
                with open(dest_path, 'w') as f:
                    f.write(content)
                print(f"Updated imports in {dest_path.name}")
            else:
                print(f"Warning: {source_file} not found")
        
        # Update any files that might import these modules
        for py_file in src.rglob('*.py'):
            if py_file.is_file():
                with open(py_file, 'r') as f:
                    content = f.read()
                
                # Update imports
                content = content.replace('from constants', 'from src.core.constants')
                content = content.replace('from raid_systems', 'from src.systems.combat.raid_systems')
                
                with open(py_file, 'w') as f:
                    f.write(content)
                
        print("\nFile structure is now:")
        print("src/")
        print("  ├── core/")
        print("  │   └── constants.py")
        print("  └── systems/")
        print("      └── combat/")
        print("          └── raid_systems.py")
        
    except Exception as e:
        print(f"Error moving files: {str(e)}")
        raise

def main():
    """Main function to run the file fix"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix additional Kingmaker files')
    parser.add_argument('--path', default='.', help='Base path for the Kingmaker project')
    
    args = parser.parse_args()
    
    fix_additional_files(args.path)

if __name__ == '__main__':
    main()