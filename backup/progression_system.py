# progression_system.py
from typing import Dict, List, Optional
import math
from card_game import BaseCard, Equipment

class ProgressionSystem:
    def __init__(self):
        self.level_multiplier = 1.5
        self.skill_costs = {
            "strength": 100,
            "health": 80,
            "defense": 90,
            "speed": 85,
            "intelligence": 95
        }
        
    def calculate_exp_needed(self, current_level: int) -> int:
        return math.floor(100 * (self.level_multiplier ** (current_level - 1)))
        
    def calculate_skill_cost(self, skill: str, current_value: int) -> int:
        base_cost = self.skill_costs.get(skill, 100)
        return math.floor(base_cost * (1.2 ** (current_value - 1)))

class CharacterClass:
    WARRIOR = "Warrior"
    RANGER = "Ranger"
    MAGE = "Mage"
    
    @staticmethod
    def get_base_stats(char_class: str) -> Dict:
        base_stats = {
            "Warrior": {
                "health": 12,
                "strength": 4,
                "defense": 3,
                "intelligence": 1,
                "speed": 2
            },
            "Ranger": {
                "health": 10,
                "strength": 3,
                "defense": 2,
                "intelligence": 2,
                "speed": 4
            },
            "Mage": {
                "health": 8,
                "strength": 2,
                "defense": 2,
                "intelligence": 5,
                "speed": 3
            }
        }
        return base_stats.get(char_class, base_stats["Warrior"])

class EnhancedCard:
    def __init__(self, card_id: int, char_class: str, base_stats: Dict):
        self.id = card_id
        self.char_class = char_class
        self.base_stats = base_stats.copy()
        self.current_stats = base_stats.copy()
        self.level = 1
        self.exp = 0
        self.exp_needed = self._calculate_exp_needed()
        self.status = "ready"
        self.equipment = {
            "weapon": None,
            "armor": None
        }
        
    def _calculate_exp_needed(self) -> int:
        """Calculate experience needed for next level"""
        return int(100 * (1.5 ** (self.level - 1)))
        
    def add_exp(self, amount: int) -> bool:
        """Add experience and handle leveling up"""
        self.exp += amount
        if self.exp >= self.exp_needed:
            self._level_up()
            return True
        return False
        
    def _level_up(self):
        """Handle level up process"""
        self.level += 1
        self.exp -= self.exp_needed
        self.exp_needed = self._calculate_exp_needed()
        
        # Increase stats based on class
        if self.char_class == CharacterClass.WARRIOR:
            self.base_stats["health"] += 3
            self.base_stats["strength"] += 2
            self.base_stats["defense"] += 2
        elif self.char_class == CharacterClass.RANGER:
            self.base_stats["health"] += 2
            self.base_stats["strength"] += 2
            self.base_stats["speed"] += 2
        elif self.char_class == CharacterClass.MAGE:
            self.base_stats["health"] += 2
            self.base_stats["intelligence"] += 3
            self.base_stats["speed"] += 1
            
        self._update_stats()
        
    def equip_item(self, item: Optional[Equipment]):
        """Equip an item and update stats"""
        if not item:
            return
            
        if item.type == "weapon":
            self.equipment["weapon"] = item
        elif item.type == "armor":
            self.equipment["armor"] = item
            
        self._update_stats()
        
    def unequip_item(self, slot: str):
        """Unequip an item and update stats"""
        if slot in self.equipment:
            item = self.equipment[slot]
            self.equipment[slot] = None
            self._update_stats()
            return item
        return None
        
    def _update_stats(self):
        """Update current stats based on base stats and equipment"""
        self.current_stats = self.base_stats.copy()
        
        # Add equipment bonuses
        for item in self.equipment.values():
            if item:
                for stat, value in item.stats.items():
                    if stat in self.current_stats:
                        self.current_stats[stat] += value
                        
    def __str__(self):
        status = f"{self.char_class} (Level {self.level})\n"
        status += f"EXP: {self.exp}/{self.exp_needed}\n"
        status += "\nStats:\n"
        for stat, value in self.current_stats.items():
            status += f"{stat.title()}: {value}"
            if stat in self.base_stats:
                bonus = value - self.base_stats[stat]
                if bonus != 0:
                    status += f" ({'+' if bonus > 0 else ''}{bonus})"
            status += "\n"
        
        status += "\nEquipment:\n"
        for slot, item in self.equipment.items():
            status += f"{slot.title()}: {item.name if item else 'None'}\n"
            
        return status