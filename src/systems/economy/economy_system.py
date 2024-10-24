# economy_system.py
from typing import Dict, List
from equipment_systems import Equipment
import random

class EconomySystem:
    def __init__(self):
        self.base_prices = {
            "wood": 5,
            "stone": 8,
            "iron": 15,
            "flint": 10,
            "magic_dust": 25,
            "repair_kit": 50
        }
        self.market_fluctuation = 0.2  # Price can fluctuate ±20%
        
    def calculate_repair_cost(self, equipment: 'Equipment') -> int:
        """Calculate cost to repair equipment"""
        damage_percent = (equipment.max_durability - equipment.durability) / 100
        base_cost = self.calculate_equipment_value(equipment) * 0.1
        return round(base_cost * damage_percent)

    def get_current_prices(self) -> Dict[str, int]:
        """Get current market prices with random fluctuation"""
        return {
            item: round(price * (1 + random.uniform(-self.market_fluctuation, self.market_fluctuation)))
            for item, price in self.base_prices.items()
        }

class Village:
    def __init__(self):
        self.population = []  # List of cards
        self.resources = {
            "food": 10,
            "wood": 5,
            "stone": 3,
            "flint": 1,
            "iron": 0,
            "magic_dust": 0,
            "repair_kits": 0,
            "coins": 100
        }
        self.buildings = []
        self.raid_cooldown = 0
        self.economy = EconomySystem()
        self.inventory = []  # For storing unequipped items
        
    def add_resources(self, resources: Dict[str, int]):
        """Add resources to village inventory"""
        for resource, amount in resources.items():
            self.resources[resource] = self.resources.get(resource, 0) + amount
            
    def remove_resources(self, resources: Dict[str, int]) -> bool:
        """
        Remove resources from village inventory
        Returns False if not enough resources
        """
        # Check if we have enough resources
        for resource, amount in resources.items():
            if self.resources.get(resource, 0) < amount:
                return False
        
        # Remove resources
        for resource, amount in resources.items():
            self.resources[resource] -= amount
        return True
        
    def add_equipment_to_inventory(self, equipment: 'Equipment'):
        """Add equipment to village inventory"""
        self.inventory.append(equipment)
        
    def remove_equipment_from_inventory(self, equipment: 'Equipment'):
        """Remove equipment from village inventory"""
        if equipment in self.inventory:
            self.inventory.remove(equipment)