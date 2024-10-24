from typing import Dict, List, Optional
import random

class ItemRarity:
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    
    @staticmethod
    def get_color(rarity: str) -> str:
        colors = {
            "Common": "white",
            "Uncommon": "green",
            "Rare": "blue",
            "Epic": "purple",
            "Legendary": "gold"
        }
        return colors.get(rarity, "white")
        
    @staticmethod
    def get_multiplier(rarity: str) -> float:
        multipliers = {
            "Common": 1.0,
            "Uncommon": 1.2,
            "Rare": 1.5,
            "Epic": 2.0,
            "Legendary": 3.0
        }
        return multipliers.get(rarity, 1.0)

class Equipment:
    def __init__(self, name: str, equip_type: str, tier: int, rarity: str, stats: Dict):
        self.name = name
        self.type = equip_type
        self.tier = tier
        self.rarity = rarity
        self.durability = 100
        self.max_durability = 100
        self.stats = stats
        
        # Apply rarity multiplier to stats
        multiplier = ItemRarity.get_multiplier(rarity)
        for stat in self.stats:
            if isinstance(self.stats[stat], (int, float)):
                self.stats[stat] *= multiplier
        
    def repair(self, amount: int):
        """Repair equipment by specified amount"""
        self.durability = min(self.max_durability, self.durability + amount)
        
    def __str__(self):
        stats_str = ", ".join([f"{k}: {v}" for k, v in self.stats.items()])
        return f"{self.name} ({self.rarity}) | {stats_str} | Durability: {self.durability}%"

class EquipmentGenerator:
    @staticmethod
    def generate_weapon(tier: int, force_rarity: Optional[str] = None) -> Equipment:
        weapon_type = random.choice(list(WEAPON_TEMPLATES.keys()))
        template = WEAPON_TEMPLATES[weapon_type]
        
        if force_rarity:
            rarity = force_rarity
        else:
            rarity_roll = random.random()
            if rarity_roll < 0.01:
                rarity = ItemRarity.LEGENDARY
            elif rarity_roll < 0.05:
                rarity = ItemRarity.EPIC
            elif rarity_roll < 0.15:
                rarity = ItemRarity.RARE
            elif rarity_roll < 0.35:
                rarity = ItemRarity.UNCOMMON
            else:
                rarity = ItemRarity.COMMON
        
        # Scale base stats with tier
        base_stats = {k: v * (1 + (tier - 1) * 0.5) 
                     for k, v in template["base_stats"].items()}
        
        return Equipment(
            name=f"{rarity} {weapon_type}",
            equip_type="weapon",
            tier=tier,
            rarity=rarity,
            stats=base_stats
        )
    
    @staticmethod
    def generate_armor(tier: int, force_rarity: Optional[str] = None) -> Equipment:
        armor_type = random.choice(list(ARMOR_TEMPLATES.keys()))
        template = ARMOR_TEMPLATES[armor_type]
        
        if force_rarity:
            rarity = force_rarity
        else:
            rarity_roll = random.random()
            if rarity_roll < 0.01:
                rarity = ItemRarity.LEGENDARY
            elif rarity_roll < 0.05:
                rarity = ItemRarity.EPIC
            elif rarity_roll < 0.15:
                rarity = ItemRarity.RARE
            elif rarity_roll < 0.35:
                rarity = ItemRarity.UNCOMMON
            else:
                rarity = ItemRarity.COMMON
        
        # Scale base stats with tier
        base_stats = {k: v * (1 + (tier - 1) * 0.5) 
                     for k, v in template["base_stats"].items()}
        
        return Equipment(
            name=f"{rarity} {armor_type}",
            equip_type="armor",
            tier=tier,
            rarity=rarity,
            stats=base_stats
        )

# Equipment Templates
WEAPON_TEMPLATES = {
    "Sword": {
        "type": "weapon",
        "base_stats": {
            "strength": 3,
            "critical_chance": 0.05
        }
    },
    "Axe": {
        "type": "weapon",
        "base_stats": {
            "strength": 4,
            "speed": -1
        }
    },
    "Spear": {
        "type": "weapon",
        "base_stats": {
            "strength": 2,
            "defense": 1,
            "range": 1
        }
    },
    "Bow": {
        "type": "weapon",
        "base_stats": {
            "strength": 2,
            "range": 2,
            "critical_chance": 0.1
        }
    },
    "Staff": {
        "type": "weapon",
        "base_stats": {
            "magic": 3,
            "intelligence": 2
        }
    }
}

ARMOR_TEMPLATES = {
    "Leather": {
        "type": "armor",
        "base_stats": {
            "defense": 2,
            "speed": 1
        }
    },
    "Chain": {
        "type": "armor",
        "base_stats": {
            "defense": 3,
            "speed": 0
        }
    },
    "Plate": {
        "type": "armor",
        "base_stats": {
            "defense": 5,
            "speed": -1
        }
    },
    "Robe": {
        "type": "armor",
        "base_stats": {
            "defense": 1,
            "magic": 2,
            "intelligence": 1
        }
    }
}

class EquipmentGenerator:
    @staticmethod
    def generate_weapon(tier: int, force_rarity: Optional[str] = None) -> Equipment:
        weapon_type = random.choice(list(WEAPON_TEMPLATES.keys()))
        template = WEAPON_TEMPLATES[weapon_type]
        
        if force_rarity:
            rarity = force_rarity
        else:
            rarity_roll = random.random()
            if rarity_roll < 0.01:
                rarity = ItemRarity.LEGENDARY
            elif rarity_roll < 0.05:
                rarity = ItemRarity.EPIC
            elif rarity_roll < 0.15:
                rarity = ItemRarity.RARE
            elif rarity_roll < 0.35:
                rarity = ItemRarity.UNCOMMON
            else:
                rarity = ItemRarity.COMMON
        
        # Scale base stats with tier
        base_stats = {k: v * (1 + (tier - 1) * 0.5) 
                     for k, v in template["base_stats"].items()}
        
        return Equipment(
            name=f"{rarity} {weapon_type}",
            equip_type="weapon",
            tier=tier,
            rarity=rarity,
            stats=base_stats
        )
    
    @staticmethod
    def generate_armor(tier: int, force_rarity: Optional[str] = None) -> Equipment:
        armor_type = random.choice(list(ARMOR_TEMPLATES.keys()))
        template = ARMOR_TEMPLATES[armor_type]
        
        if force_rarity:
            rarity = force_rarity
        else:
            rarity_roll = random.random()
            if rarity_roll < 0.01:
                rarity = ItemRarity.LEGENDARY
            elif rarity_roll < 0.05:
                rarity = ItemRarity.EPIC
            elif rarity_roll < 0.15:
                rarity = ItemRarity.RARE
            elif rarity_roll < 0.35:
                rarity = ItemRarity.UNCOMMON
            else:
                rarity = ItemRarity.COMMON
        
        # Scale base stats with tier
        base_stats = {k: v * (1 + (tier - 1) * 0.5) 
                     for k, v in template["base_stats"].items()}
        
        return Equipment(
            name=f"{rarity} {armor_type}",
            equip_type="armor",
            tier=tier,
            rarity=rarity,
            stats=base_stats
        )

# Test function
def test_equipment_system():
    generator = EquipmentGenerator()
    
    print("Testing weapon generation:")
    for rarity in [ItemRarity.COMMON, ItemRarity.RARE, ItemRarity.LEGENDARY]:
        weapon = generator.generate_weapon(tier=1, force_rarity=rarity)
        print(f"\nGenerated weapon: {weapon}")
        
    print("\nTesting armor generation:")
    for tier in [1, 2, 3]:
        armor = generator.generate_armor(tier=tier)
        print(f"\nGenerated tier {tier} armor: {armor}")

if __name__ == "__main__":
    test_equipment_system()




