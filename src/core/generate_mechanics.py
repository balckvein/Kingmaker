#!/usr/bin/env python3
"""
Kingmaker Game Mechanics Documentation Generator
Creates and maintains documentation for game mechanics and systems
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class GameMechanicsManager:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.mechanics_file = self.base_path / 'game_mechanics.json'
        self.structure_file = self.base_path / 'game_structure.json'
        self.docs_dir = self.base_path / 'docs'
        
    def generate_default_mechanics(self) -> Dict:
        """Generate default game mechanics structure"""
        return {
            "combat_system": {
                "attack_calculation": {
                    "base_formula": "attacker_str + weapon_bonus + crystal_bonus",
                    "critical_chance": 0.15,
                    "critical_multiplier": 1.5,
                    "defense_reduction": "target_def * 0.5"
                },
                "raid_system": {
                    "tier_1": {
                        "required_strength": 10,
                        "reward_multiplier": 1.0,
                        "captive_chance": 0.3
                    },
                    "tier_2": {
                        "required_strength": 20,
                        "reward_multiplier": 1.5,
                        "captive_chance": 0.4
                    },
                    "tier_3": {
                        "required_strength": 30,
                        "reward_multiplier": 2.0,
                        "captive_chance": 0.5
                    }
                },
                "status_effects": {
                    "stunned": {"duration": 2, "effect": "Cannot attack"},
                    "wounded": {"duration": 3, "effect": "-25% STR"},
                    "inspired": {"duration": 2, "effect": "+25% STR"}
                }
            },
            "progression_system": {
                "experience_gain": {
                    "combat_victory": 100,
                    "raid_success": 200,
                    "resource_gathering": 50
                },
                "level_scaling": {
                    "exp_multiplier": 1.5,
                    "stat_increase": {
                        "health": 2,
                        "strength": 1,
                        "defense": 1
                    }
                },
                "skill_trees": {
                    "warrior": [
                        {"level": 1, "skill": "Power Strike", "effect": "+20% damage"},
                        {"level": 5, "skill": "Battle Cry", "effect": "Team buff"},
                        {"level": 10, "skill": "Berserker", "effect": "Double damage"}
                    ],
                    "hero": [
                        {"level": 1, "skill": "Leadership", "effect": "Team exp bonus"},
                        {"level": 5, "skill": "Rally", "effect": "Prevent retreat"},
                        {"level": 10, "skill": "Heroic Stand", "effect": "Team invulnerable"}
                    ]
                }
            },
            "resource_system": {
                "gathering_rates": {
                    "wood": {"base_rate": 10, "tool_bonus": 5},
                    "stone": {"base_rate": 8, "tool_bonus": 4},
                    "iron": {"base_rate": 5, "tool_bonus": 3}
                },
                "processing": {
                    "plank": {"input": {"wood": 2}, "output": 1},
                    "iron_ingot": {"input": {"iron_ore": 2}, "output": 1},
                    "brick": {"input": {"stone": 2}, "output": 1}
                }
            },
            "building_system": {
                "house": {
                    "cost": {"wood": 4, "stone": 2},
                    "build_time": 2,
                    "capacity": 4
                },
                "barracks": {
                    "cost": {"wood": 6, "stone": 4},
                    "build_time": 3,
                    "training_bonus": 0.2
                },
                "workshop": {
                    "cost": {"wood": 5, "stone": 3},
                    "build_time": 2,
                    "crafting_bonus": 0.25
                }
            }
        }

    def save_mechanics(self, mechanics: Dict):
        """Save mechanics to JSON file"""
        self.docs_dir.mkdir(exist_ok=True)
        with open(self.mechanics_file, 'w') as f:
            json.dump(mechanics, f, indent=2)

    def generate_mechanics_md(self, mechanics: Dict) -> str:
        """Generate markdown documentation for game mechanics"""
        md = ["# Kingmaker Game Mechanics Documentation\n\n"]
        
        # Combat System
        md.append("## Combat System\n\n")
        md.append("### Attack Calculations\n")
        combat = mechanics['combat_system']
        md.append(f"- Base Formula: `{combat['attack_calculation']['base_formula']}`\n")
        md.append(f"- Critical Chance: {combat['attack_calculation']['critical_chance']*100}%\n")
        md.append(f"- Critical Multiplier: {combat['attack_calculation']['critical_multiplier']}x\n\n")

        # Raid System
        md.append("### Raid System\n")
        md.append("| Tier | Required Strength | Reward Multiplier | Captive Chance |\n")
        md.append("|------|------------------|------------------|----------------|\n")
        for tier, info in combat['raid_system'].items():
            md.append(f"| {tier} | {info['required_strength']} | {info['reward_multiplier']}x | ")
            md.append(f"{info['captive_chance']*100}% |\n")
        md.append("\n")

        # Progression System
        md.append("## Progression System\n\n")
        progression = mechanics['progression_system']
        md.append("### Experience Gains\n")
        for activity, exp in progression['experience_gain'].items():
            md.append(f"- {activity.replace('_', ' ').title()}: {exp} EXP\n")
        md.append("\n")

        # Skill Trees
        md.append("### Skill Trees\n")
        for class_name, skills in progression['skill_trees'].items():
            md.append(f"\n#### {class_name.title()} Skills\n")
            md.append("| Level | Skill | Effect |\n")
            md.append("|-------|-------|--------|\n")
            for skill in skills:
                md.append(f"| {skill['level']} | {skill['skill']} | {skill['effect']} |\n")
        md.append("\n")

        # Resource System
        md.append("## Resource System\n\n")
        resources = mechanics['resource_system']
        
        md.append("### Gathering Rates\n")
        md.append("| Resource | Base Rate | Tool Bonus |\n")
        md.append("|----------|------------|------------|\n")
        for resource, rates in resources['gathering_rates'].items():
            md.append(f"| {resource} | {rates['base_rate']} | +{rates['tool_bonus']} |\n")
        md.append("\n")

        # Building System
        md.append("## Building System\n\n")
        md.append("| Building | Wood Cost | Stone Cost | Build Time | Special |\n")
        md.append("|----------|------------|------------|------------|---------||\n")
        for building, info in mechanics['building_system'].items():
            special = (f"Training +{info.get('training_bonus')*100}%" if 'training_bonus' in info 
                      else f"Crafting +{info.get('crafting_bonus')*100}%" if 'crafting_bonus' in info
                      else f"Capacity: {info.get('capacity')}")
            md.append(f"| {building} | {info['cost']['wood']} | {info['cost']['stone']} | ")
            md.append(f"{info['build_time']} days | {special} |\n")

        return "".join(md)

    def update(self):
        """Update game mechanics documentation"""
        try:
            print("Generating game mechanics structure...")
            mechanics = self.generate_default_mechanics()
            
            print("Saving mechanics JSON...")
            self.save_mechanics(mechanics)
            
            print("Generating mechanics documentation...")
            md_content = self.generate_mechanics_md(mechanics)
            
            # Save markdown documentation
            with open(self.docs_dir / 'MECHANICS.md', 'w') as f:
                f.write(md_content)
            
            print("Game mechanics documentation updated successfully!")
            print("\nFiles created:")
            print(f"1. {self.mechanics_file}")
            print(f"2. {self.docs_dir / 'MECHANICS.md'}")
            
        except Exception as e:
            print(f"Error updating game mechanics: {str(e)}")
            raise

def main():
    """Main function to run the mechanics documentation generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Kingmaker game mechanics documentation')
    parser.add_argument('--path', default='.', help='Base path for the project')
    
    args = parser.parse_args()
    
    manager = GameMechanicsManager(args.path)
    manager.update()

if __name__ == '__main__':
    main()