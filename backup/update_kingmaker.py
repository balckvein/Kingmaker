#!/usr/bin/env python3
"""
Complete Kingmaker File Reorganization Script
"""

import os
import shutil
from pathlib import Path

class CompleteReorganizer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.src_path = self.base_path / 'src'
        
    def create_directory_structure(self):
        """Create complete directory structure"""
        directories = [
            self.src_path / 'core',
            self.src_path / 'menus',
            self.src_path / 'systems' / 'combat',
            self.src_path / 'systems' / 'economy',
            self.src_path / 'systems' / 'progression',
            self.src_path / 'utils',
            self.src_path / 'tests' / 'test_menus',
            self.src_path / 'tests' / 'test_systems',
            self.src_path / 'tests' / 'test_utils'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            (directory / '__init__.py').touch()

    def move_files(self):
        """Move files to their new locations while preserving structure"""
        # Define file mappings
        file_moves = {
            # Menu files
            'menu_system.py': 'src/menus/menu_system.py',
            'base_menu.py': 'src/menus/base_menu.py',
            'menus/_init_.py': 'src/menus/__init__.py',
            'warrior_menu.py': 'src/menus/warrior_menu.py',
            
            # Core files
            'card_game.py': 'src/core/card_game.py',
            'game_interface.py': 'src/core/game_interface.py',
            'error_handler.py': 'src/core/error_handler.py',
            
            # System files
            'systems/combat/combat.py': 'src/systems/combat/combat.py',
            'systems/economy/economy_system.py': 'src/systems/economy/economy_system.py',
            'systems/progression/progression_system.py': 'src/systems/progression/progression_system.py',
            'equipment_systems.py': 'src/systems/equipment_systems.py',
            
            # Test files
            'tests/test_menus/base_test.py': 'src/tests/test_menus/base_test.py',
            'tests/test_systems/test_combat.py': 'src/tests/test_systems/test_combat.py'
        }
        
        # Move each file
        for old_path, new_path in file_moves.items():
            source = self.base_path / old_path
            destination = self.base_path / new_path
            
            # Only move if source exists
            if source.exists():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(destination))
                print(f"Moved {old_path} to {new_path}")
            else:
                print(f"Skipped {old_path} - file not found")

    def update_imports(self):
        """Update import statements in all Python files"""
        for py_file in self.src_path.rglob('*.py'):
            with open(py_file, 'r') as f:
                content = f.read()
            
            # Update import statements
            content = content.replace('from menus.', 'from src.menus.')
            content = content.replace('from systems.', 'from src.systems.')
            content = content.replace('from core.', 'from src.core.')
            
            with open(py_file, 'w') as f:
                f.write(content)
            print(f"Updated imports in {py_file}")

    def reorganize(self):
        """Run the complete reorganization process"""
        print("Starting complete file reorganization...")
        
        try:
            # Create backup
            backup_dir = self.base_path / 'backup'
            backup_dir.mkdir(exist_ok=True)
            
            # Backup existing structure
            for item in self.base_path.glob('**/*.py'):
                if 'backup' not in str(item):
                    relative_path = item.relative_to(self.base_path)
                    backup_path = backup_dir / relative_path
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(item), str(backup_path))
                    print(f"Backed up {relative_path}")
            
            # Create new structure
            self.create_directory_structure()
            
            # Move files
            self.move_files()
            
            # Update imports
            self.update_imports()
            
            print("\nFiles that should stay in their current location:")
            print("- requirements.txt (root directory)")
            print("- README.md (root directory)")
            print("- setup.py (root directory)")
            print("- game.json (root directory)")
            
            print("\nFile reorganization completed!")
            
        except Exception as e:
            print(f"Error during reorganization: {str(e)}")
            raise

def main():
    """Main function to run the reorganizer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Reorganize Kingmaker project files')
    parser.add_argument('--path', default='.', help='Base path for the Kingmaker project')
    
    args = parser.parse_args()
    
    reorganizer = CompleteReorganizer(args.path)
    reorganizer.reorganize()

if __name__ == '__main__':
    main()