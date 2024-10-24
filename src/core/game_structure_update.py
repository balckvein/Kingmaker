#!/usr/bin/env python3
"""
Kingmaker Game Structure Update Script
Analyzes and documents game structure including cards, resources, and game mechanics
"""

import os
from pathlib import Path
import ast
import json
from datetime import datetime
from typing import Dict, List

class GameStructureManager:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.structure_file = self.base_path / 'game_structure.json'
        self.backup_dir = self.base_path / 'backups'
        
    def parse_game_cards(self) -> Dict:
        """Parse and organize card-related structures"""
        return {
            'character_cards': {
                'Villager': {'health': 8, 'str': 2, 'def': 2, 'int': 1, 'ability': 'Base character'},
                'Hero': {'health': 12, 'str': 4, 'def': 3, 'int': 2, 'ability': 'Leadership Bonus'},
                'Leader': {'health': 15, 'str': 5, 'def': 4, 'int': 3, 'ability': 'Village-wide Bonuses'},
                'Alien_Scout': {'health': 6, 'str': 4, 'def': 2, 'int': 'N/A', 'ability': 'Scouting ability'},
                'Alien_Brute': {'health': 12, 'str': 6, 'def': 5, 'int': 'N/A', 'ability': 'High attack power'},
                'Alien_Boss': {'health': 20, 'str': 6, 'def': 5, 'int': 'N/A', 'ability': 'Strong Attack/Debuff'}
            },
            'resource_cards': {
                'Iron_Ore': {'value': 2, 'type': 'Basic Building Material'},
                'Iron_Ingot': {'value': 3, 'type': 'Basic Building Material'},
                'Wood': {'value': 1, 'type': 'Basic Building Material'},
                'Stone': {'value': 1, 'type': 'Basic Building Material'},
                'Stick': {'value': 2, 'type': 'Basic Building Material'},
                'Plank': {'value': 3, 'type': 'Basic Building Material'},
                'Flint': {'value': 2, 'type': 'Tool Crafting'},
                'Brick': {'value': 3, 'type': 'Advanced Building Material'},
                'Magic_Dust': {'value': 3, 'type': 'Used for Special Abilities'}
            }
        }

    def parse_crystal_bonuses(self) -> Dict:
        """Parse crystal bonus system"""
        return {
            'Red': [
                {'level': 1, 'stat': 'STR', 'value': 1},
                {'level': 2, 'stat': 'STR', 'value': 2},
                {'level': 3, 'stat': 'STR', 'value': 3}
            ],
            'Blue': [
                {'level': 1, 'stat': 'DEX', 'value': 1},
                {'level': 2, 'stat': 'DEX', 'value': 2},
                {'level': 3, 'stat': 'DEX', 'value': 3}
            ],
            'Yellow': [
                {'level': 1, 'bonus': '20% Roll Bonus', 'type': 'Luck'},
                {'level': 2, 'bonus': '40% Roll Bonus', 'type': 'Luck'},
                {'level': 3, 'bonus': '60% Roll Bonus', 'type': 'Luck'}
            ]
        }

    def parse_equipment(self) -> Dict:
        """Parse equipment system"""
        return {
            'weapons': {
                'Sword': {'bonus': '+2 STR', 'value': 4, 'ability': 'Enhanced Attack'},
                'Shield': {'bonus': '+3 DEF', 'value': 4, 'ability': 'High Defense'},
                'Magic_Staff': {'bonus': 'Special', 'value': 5, 'ability': 'Grants Special Ability'}
            },
            'tools': {
                'Plow': {'bonus': 'N/A', 'value': 2, 'ability': 'Grow Food/Potion Effect'},
                'Hammer': {'bonus': '+1 DEF', 'value': 3, 'ability': 'Enhanced Defense'},
                'Axe': {'bonus': '+1 STR, +1 DEF', 'value': 3, 'ability': 'Balanced Attack and Defense'},
                'Pickaxe': {'bonus': '+2 STR', 'value': 3, 'ability': 'High Attack, Resource Gathering'}
            }
        }

    def generate_structure(self) -> Dict:
        """Generate complete game structure"""
        return {
            'last_updated': datetime.now().isoformat(),
            'game_elements': {
                'cards': self.parse_game_cards(),
                'crystals': self.parse_crystal_bonuses(),
                'equipment': self.parse_equipment(),
                'balance_metrics': {
                    'base_success_chance': 0.4,
                    'strength_multiplier': 1.5,
                    'captive_rate': 0.4,
                    'resource_multiplier': 2
                }
            }
        }

    def save_structure(self, structure: Dict):
        """Save structure to JSON file"""
        self.backup_dir.mkdir(exist_ok=True)
        
        # Backup existing structure if it exists
        if self.structure_file.exists():
            backup_path = self.backup_dir / f'game_structure_{datetime.now():%Y%m%d_%H%M%S}.json'
            with open(self.structure_file, 'r') as src, open(backup_path, 'w') as dst:
                dst.write(src.read())
        
        # Save new structure
        with open(self.structure_file, 'w') as f:
            json.dump(structure, f, indent=2)

    def generate_markdown(self, structure: Dict) -> str:
        """Generate markdown documentation"""
        md = ["# Kingmaker Game Structure\n"]
        md.append(f"Last updated: {structure['last_updated']}\n")

        # Document cards
        md.append("## Character Cards\n")
        for name, stats in structure['game_elements']['cards']['character_cards'].items():
            md.append(f"### {name}\n")
            for stat, value in stats.items():
                md.append(f"- {stat}: {value}\n")
            md.append("\n")

        # Document resources
        md.append("## Resources\n")
        for name, info in structure['game_elements']['cards']['resource_cards'].items():
            md.append(f"- {name}: Value {info['value']} ({info['type']})\n")
        md.append("\n")

        # Document equipment
        md.append("## Equipment\n")
        for category, items in structure['game_elements']['equipment'].items():
            md.append(f"### {category.title()}\n")
            for name, stats in items.items():
                md.append(f"- {name}: {stats['bonus']} (Value: {stats['value']})\n")
            md.append("\n")

        return "".join(md)

    def update(self):
        """Main update process"""
        try:
            print("Analyzing game structure...")
            structure = self.generate_structure()
            
            print("Saving structure to JSON...")
            self.save_structure(structure)
            
            print("Generating markdown documentation...")
            markdown = self.generate_markdown(structure)
            
            # Save markdown
            with open(self.base_path / 'GAME_STRUCTURE.md', 'w') as f:
                f.write(markdown)
            
            print("Game structure documentation updated successfully!")
            print("\nFiles created:")
            print(f"1. {self.structure_file}")
            print(f"2. {self.base_path / 'GAME_STRUCTURE.md'}")
            
        except Exception as e:
            print(f"Error updating game structure: {str(e)}")
            raise

def main():
    """Main function to run the structure manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update Kingmaker game structure documentation')
    parser.add_argument('--path', default='.', help='Base path for the project')
    
    args = parser.parse_args()
    
    manager = GameStructureManager(args.path)
    manager.update()

if __name__ == '__main__':
    main()