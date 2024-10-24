#!/usr/bin/env python3
"""
Kingmaker Project File Organization Script
Handles complete backup and organization of project files
"""

import os
from pathlib import Path
import shutil
from datetime import datetime
from typing import Dict, List, Set

class ProjectOrganizer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.backup_dir = self.base_path / 'backups'
        
        # Define important file patterns
        self.file_patterns = {
            'python': '*.py',
            'json': '*.json',
            'markdown': '*.md',
            'yaml': '*.yaml',
            'txt': '*.txt'
        }
        
        # Define directory structure and files
        self.project_structure = {
            'docs': [
                'GAME_STRUCTURE.md',
                'MECHANICS.md',
                'README.md',
                'kingmaker-complete-analysis.md'
            ],
            'src': {
                'core': [
                    'game_interface.py',
                    'card_game.py',
                    'constants.py',
                    'error_handler.py'
                ],
                'systems': {
                    'combat': [
                        'combat.py',
                        'raid_systems.py'
                    ],
                    'economy': [
                        'economy_system.py'
                    ],
                    'progression': [
                        'progression_system.py',
                        'equipment_system.py'
                    ]
                }
            },
            'data': [
                'game_mechanics.json',
                'game_structure.json'
            ],
            'utils': [
                'game_structure_update.py',
                'generate_mechanics.py',
                'update_kingmaker.py',
                'basicTest.py'
            ],
            'config': [
                'requirements.txt'
            ]
        }

    def find_all_project_files(self) -> Set[Path]:
        """Find all project files that should be backed up"""
        files = set()
        for pattern in self.file_patterns.values():
            files.update(self.base_path.glob(f"**/{pattern}"))
        
        # Exclude files from backup directory
        return {f for f in files if 'backups' not in str(f)}

    def create_backup(self):
        """Create backup of all project files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f'backup_{timestamp}'
        backup_path.mkdir(parents=True, exist_ok=True)

        files = self.find_all_project_files()
        
        for file in files:
            # Create relative path for backup
            rel_path = file.relative_to(self.base_path)
            backup_file = backup_path / rel_path
            
            # Create directories if needed
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file with metadata
            shutil.copy2(file, backup_file)
            
        return backup_path

    def create_directory_structure(self):
        """Create the project directory structure"""
        def create_recursive(base: Path, structure: Dict):
            if isinstance(structure, dict):
                for dir_name, contents in structure.items():
                    dir_path = base / dir_name
                    dir_path.mkdir(exist_ok=True)
                    create_recursive(dir_path, contents)
            elif isinstance(structure, list):
                base.mkdir(exist_ok=True)

        create_recursive(self.base_path, self.project_structure)

    def organize_files(self):
        """Move files to their appropriate locations"""
        def move_files_recursive(base: Path, structure: Dict):
            if isinstance(structure, dict):
                for dir_name, contents in structure.items():
                    dir_path = base / dir_name
                    move_files_recursive(dir_path, contents)
            elif isinstance(structure, list):
                for file_name in structure:
                    src_file = self.base_path / file_name
                    if src_file.exists():
                        dest_file = base / file_name
                        if src_file != dest_file and 'backups' not in str(src_file):
                            shutil.move(str(src_file), str(dest_file))

        move_files_recursive(self.base_path, self.project_structure)

    def organize(self):
        """Main organization process"""
        try:
            print("Creating backup of all project files...")
            backup_path = self.create_backup()
            print(f"Backup created at: {backup_path}")
            
            print("\nCreating directory structure...")
            self.create_directory_structure()
            
            print("Organizing files...")
            self.organize_files()
            
            # List all files in backup for verification
            print("\nBacked up files:")
            for file in sorted(backup_path.rglob('*')):
                if file.is_file():
                    print(f"- {file.relative_to(backup_path)}")
            
            print("\nProject organization completed successfully!")
            
        except Exception as e:
            print(f"Error organizing project: {str(e)}")
            raise

def main():
    """Main function to run the project organizer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Organize Kingmaker project files')
    parser.add_argument('--path', default='.', help='Base path for the project')
    
    args = parser.parse_args()
    
    organizer = ProjectOrganizer(args.path)
    organizer.organize()

if __name__ == '__main__':
    main()