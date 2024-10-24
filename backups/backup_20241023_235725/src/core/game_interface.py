# game_interface.py
from typing import Dict, Optional
import random
import json
import os
from card_game import Equipment, Village
from progression_system import EnhancedCard, CharacterClass, ProgressionSystem
from src.systems.combat.raid_systems import RaidTier
from menu_system import MenuSystem
from equipment_systems import EquipmentGenerator



class GameInterface:
    def __init__(self):
        self.village = Village()
        self.current_day = 1
        self.progression = ProgressionSystem()
        self.equipment_generator = EquipmentGenerator()
        self.menu = MenuSystem(self)

    def start_game(self):
        """Initialize and start the game"""
        print("Welcome to the Village Management Game!")
        print("\nInitializing village...")
        self._initialize_village()
        self.menu.run()

    def _initialize_village(self):
        """Initialize the village with starting resources and warriors"""
        self.village.resources = {
            "wood": 10,
            "stone": 5,
            "iron_ore": 3,
            "stick": 5,
            "plank": 0,
            "flint": 2,
            "brick": 0,
            "magic_dust": 0
        }
        self.village.buildings = []
        self.village.inventory = []
        
        # Create initial warriors
        for _ in range(3):
            warrior = self._create_starter_warrior()
            self.village.population.append(warrior)

    def display_status(self) -> str:
        """Display current game status"""
        status = f"\n=== Day {self.current_day} ===\n"
        status += f"Population: {len(self.village.population)} warriors\n"
        status += "\nResources:\n"
        for resource, amount in self.village.resources.items():
            status += f"{resource.replace('_', ' ').title()}: {amount}\n"
        return status
        

    def _create_starter_warrior(self) -> EnhancedCard:
        """Create a starter warrior with basic equipment"""
        char_class = random.choice([
            CharacterClass.WARRIOR,
            CharacterClass.RANGER,
            CharacterClass.MAGE
        ])
        
        base_stats = CharacterClass.get_base_stats(char_class)
        warrior = EnhancedCard(len(self.village.population) + 1, char_class, base_stats)
        
        # Give basic equipment
        starter_weapon = self.equipment_generator.generate_weapon(1, force_rarity="Common")
        starter_armor = self.equipment_generator.generate_armor(1, force_rarity="Common")
        
        warrior.equip_item(starter_weapon)
        warrior.equip_item(starter_armor)
        
        return warrior

    def save_game(self):
        """Save game state to file"""
        game_state = {
            "current_day": self.current_day,
            "village": {
                "resources": self.village.resources,
                "raid_cooldown": getattr(self.village, 'raid_cooldown', 0)
            },
            "warriors": [
                {
                    "id": w.id,
                    "class": w.char_class,
                    "level": w.level,
                    "exp": w.exp,
                    "stats": w.stats,
                    "equipment": {
                        "weapon": w.equipment["weapon"].__dict__ if w.equipment["weapon"] else None,
                        "armor": w.equipment["armor"].__dict__ if w.equipment["armor"] else None
                    }
                }
                for w in self.village.population
            ],
            "inventory": [item.__dict__ for item in getattr(self.village, 'inventory', [])]
        }
        
        with open("game_save.json", "w") as f:
            json.dump(game_state, f, indent=2)
            
        return True

    def load_game(self):
        """Load game state from file"""
        if not os.path.exists("game_save.json"):
            return False
            
        with open("game_save.json", "r") as f:
            game_state = json.load(f)
            
        self.current_day = game_state.get("current_day", 1)
        
        # Restore village state
        self.village.resources = game_state["village"]["resources"]
        self.village.raid_cooldown = game_state["village"]["raid_cooldown"]
        
        # Restore warriors
        self.village.population = []
        for w_data in game_state["warriors"]:
            warrior = EnhancedCard(w_data["id"], w_data["class"], w_data["stats"])
            warrior.level = w_data["level"]
            warrior.exp = w_data["exp"]
            
            # Restore equipment
            if w_data["equipment"]["weapon"]:
                warrior.equipment["weapon"] = Equipment(**w_data["equipment"]["weapon"])
            if w_data["equipment"]["armor"]:
                warrior.equipment["armor"] = Equipment(**w_data["equipment"]["armor"])
                
            self.village.population.append(warrior)
            
        # Restore inventory
        self.village.inventory = [Equipment(**item) for item in game_state["inventory"]]
        
        return True

    def end_day(self):
        """Handle end of day events"""
        self.current_day += 1
        
        # Gather resources
        gather_results = {
            "wood": random.randint(3, 6),
            "stone": random.randint(2, 4),
            "iron_ore": random.randint(1, 2),
            "stick": random.randint(2, 4)
        }
        
        # Apply building bonuses
        for building in getattr(self.village, 'buildings', []):
            if hasattr(building, 'resource_bonus'):
                for resource, bonus in building.resource_bonus.items():
                    if resource in gather_results:
                        gather_results[resource] = int(gather_results[resource] * (1 + bonus))
        
        # Update resources
        for resource, amount in gather_results.items():
            self.village.resources[resource] += amount
        
        # Reset warrior status
        for warrior in self.village.population:
            if warrior.status == "tired":
                warrior.status = "ready"
                
        return gather_results
    
def main():
    game = GameInterface()
    game.start_game()

if __name__ == "__main__":
    main()