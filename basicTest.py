import random
from typing import Dict, List, Optional

class Card:
    def __init__(self, card_type: str, stats: Dict):
        self.card_type = card_type
        self.health = stats.get('health', 0)
        self.strength = stats.get('str', 0)
        self.defense = stats.get('def', 0)
        self.intelligence = stats.get('int', 0)
        self.special_ability = stats.get('special_ability', None)
        self.status = "ready"

class Village:
    def __init__(self):
        self.resources = {
            "iron_ore": 0,
            "iron_ingot": 0,
            "wood": 0,
            "stone": 0,
            "stick": 0,
            "plank": 0,
            "flint": 0,
            "brick": 0,
            "magic_dust": 0
        }
        self.population = []
        self.buildings = []

class GameState:
    def __init__(self):
        self.village = Village()
        self.day = 1
        
        # Initialize card templates from the provided data
        self.character_templates = {
            "villager": {"health": 8, "str": 2, "def": 2, "int": 1, "special_ability": "Base character"},
            "hero": {"health": 12, "str": 4, "def": 3, "int": 2, "special_ability": "Leadership Bonus"},
            "leader": {"health": 15, "str": 5, "def": 4, "int": 3, "special_ability": "Village-wide Bonuses"},
            "alien_scout": {"health": 6, "str": 4, "def": 2, "special_ability": "Scouting ability"},
            "alien_brute": {"health": 12, "str": 6, "def": 5, "special_ability": "High attack power"},
            "alien_boss": {"health": 20, "str": 6, "def": 5, "special_ability": "Strong Attack/Debuff"}
        }

    def create_character(self, char_type: str) -> Optional[Card]:
        if char_type in self.character_templates:
            return Card(char_type, self.character_templates[char_type])
        return None

    def gather_resources(self):
        """Basic resource gathering simulation"""
        resources_gained = {
            "wood": random.randint(1, 3),
            "stone": random.randint(1, 2),
            "iron_ore": random.randint(0, 1)
        }
        
        for resource, amount in resources_gained.items():
            self.village.resources[resource] += amount
        
        return resources_gained

def test_game():
    """Basic test function to verify game mechanics"""
    game = GameState()
    
    # Create initial population
    villager = game.create_character("villager")
    hero = game.create_character("hero")
    
    game.village.population.extend([villager, hero])
    
    # Test resource gathering
    print("Initial resources:", game.village.resources)
    gathered = game.gather_resources()
    print("Gathered resources:", gathered)
    print("Updated resources:", game.village.resources)
    
    # Test population stats
    print("\nPopulation:")
    for character in game.village.population:
        print(f"{character.card_type}: HP={character.health}, STR={character.strength}, DEF={character.defense}")

if __name__ == "__main__":
    test_game()