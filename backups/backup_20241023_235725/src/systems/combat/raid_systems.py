# raid_systems.py
from typing import Dict, List, Optional
import random
import math
from combat import CombatSystem

# Base Card class definition
class Card:
    def __init__(self, card_id: int, card_type: str, stats: Dict):
        self.id = card_id
        self.type = card_type
        self.stats = stats.copy()
        self.victories = 0
        self.raids_survived = 0
        self.status = "ready"  # ready, tired, injured

    def __str__(self):
        return (f"Card #{self.id} ({self.type}) | "
                f"STR: {self.stats['strength']}, "
                f"HP: {self.stats['health']}, "
                f"DEF: {self.stats['defense']} | "
                f"Status: {self.status}")

class Equipment:
    def __init__(self, name: str, equip_type: str, tier: int, stats: Dict):
        self.name = name
        self.type = equip_type  # weapon or armor
        self.tier = tier
        self.stats = stats
        self.durability = 100
        
    def __str__(self):
        stats_str = ", ".join([f"{k}: {v}" for k, v in self.stats.items()])
        return f"{self.name} (Tier {self.tier}) | {stats_str} | Durability: {self.durability}%"

class EnhancedCard(Card):
    def __init__(self, card_id: int, card_type: str, stats: Dict):
        super().__init__(card_id, card_type, stats)
        self.level = 1
        self.exp = 0
        self.exp_needed = 100
        self.equipment = {
            "weapon": None,
            "armor": None
        }
        self.raid_cooldown = 0
        self.points = 0
        
    def add_exp(self, amount: int) -> bool:
        """Add experience and return True if leveled up"""
        self.exp += amount
        if self.exp >= self.exp_needed:
            self.level_up()
            return True
        return False
        
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_needed
        self.exp_needed = math.floor(self.exp_needed * 1.5)
        # Improve stats
        self.stats["strength"] += 1
        self.stats["health"] += 2
        self.stats["defense"] += 1
        
    def equip_item(self, item: Equipment):
        if item.type in self.equipment:
            self.equipment[item.type] = item
            # Apply equipment stats
            for stat, value in item.stats.items():
                if stat in self.stats:
                    self.stats[stat] += value
                    
    def get_recovery_time(self, health_lost: int) -> int:
        """Calculate recovery time based on health lost"""
        base_recovery = math.ceil(health_lost / 10)  # 1 day per 10 health lost
        return max(1, min(base_recovery, 7))  # Cap between 1 and 7 days
        
    def __str__(self):
        equipped_str = "\n    ".join([
            f"{slot}: {item}" if item else f"{slot}: None"
            for slot, item in self.equipment.items()
        ])
        return (f"Card #{self.id} ({self.type}) Level {self.level}\n"
                f"    STR:{self.stats['strength']}, HP:{self.stats['health']}, "
                f"DEF:{self.stats['defense']}\n"
                f"    Status: {self.status} | EXP: {self.exp}/{self.exp_needed}\n"
                f"    Victories: {self.victories} | Raids: {self.raids_survived}\n"
                f"    Equipment:\n    {equipped_str}\n"
                f"    Points: {self.points} | Raid Cooldown: {self.raid_cooldown} days")

class RaidTier:
    def __init__(self, tier_level: int, name: str, coin_cost: int, difficulty_multiplier: float):
        self.level = tier_level
        self.name = name
        self.coin_cost = coin_cost
        self.difficulty_multiplier = difficulty_multiplier
        self.boss_health = 100 * tier_level
        self.levels = self._generate_levels()
        
    def _generate_levels(self) -> List[Dict]:
        levels = []
        for i in range(1, 11):  # 10 levels per tier
            is_boss = i == 10
            level = {
                "level": i,
                "enemies": random.randint(1, 3) if not is_boss else 1,
                "difficulty": i * self.difficulty_multiplier,
                "is_boss": is_boss,
                "health_pool": self.boss_health if is_boss else 50 * i,
                "rewards": self._generate_rewards(i, is_boss)
            }
            levels.append(level)
        return levels
    
    def _generate_rewards(self, level: int, is_boss: bool) -> Dict:
        base_coins = level * 10 * self.level
        
        rewards = {
            "coins": base_coins,
            "exp": level * 5 * self.level,
            "resources": {
                "wood": random.randint(1, 3) * level,
                "stone": random.randint(1, 2) * level,
                "iron": random.randint(0, 1) * level,
                "flint": random.randint(0, 1) * level
            },
            "higher_tier_chance": 0
        }
        
        # Add tier progression chances
        if self.level == 1:
            rewards["higher_tier_chance"] = 0.25 if is_boss else 0.05
        elif self.level == 2:
            rewards["higher_tier_chance"] = 0.10 if is_boss else 0.02
        elif self.level == 3:
            rewards["higher_tier_chance"] = 0.05 if is_boss else 0.01
            
        return rewards


class EnhancedCombatSystem(CombatSystem):
    def __init__(self):
        super().__init__()
        self.raid_tiers = {
            1: RaidTier(1, "Woods", 50, 1.0),
            2: RaidTier(2, "Caves", 150, 1.5),
            3: RaidTier(3, "Fort", 300, 2.0)
        }
        
    def conduct_raid(self, raiding_party: List[EnhancedCard], tier: int, level: int) -> Dict:
        """Conduct a raid at specified tier and level"""
        if tier not in self.raid_tiers:
            return {"success": False, "message": "Invalid raid tier"}
            
        raid_tier = self.raid_tiers[tier]
        if level < 1 or level > len(raid_tier.levels):
            return {"success": False, "message": "Invalid raid level"}
            
        raid_level = raid_tier.levels[level - 1]
        
        # Calculate total raiding party strength
        party_strength = sum(
            card.stats["strength"] + 
            (card.equipment["weapon"].stats.get("strength", 0) if card.equipment["weapon"] else 0)
            for card in raiding_party
        )
        
        # Calculate success chance
        difficulty = raid_level["difficulty"]
        success_chance = min(0.9, party_strength / (difficulty * 10))
        
        # Determine raid outcome
        success = random.random() < success_chance
        
        # Calculate damage taken and update cooldowns
        for card in raiding_party:
            health_lost = random.randint(5, 20) * raid_tier.level
            if card.equipment["armor"]:
                health_lost *= (1 - card.equipment["armor"].stats.get("defense_multiplier", 0))
            card.raid_cooldown = card.get_recovery_time(health_lost)
            
            if success:
                card.add_exp(raid_level["rewards"]["exp"])
                card.points += raid_level["rewards"]["coins"] // 10
        
        if success:
            rewards = raid_level["rewards"].copy()
            if raid_level["is_boss"]:
                rewards["guaranteed_upgrade"] = True
                
            return {
                "success": True,
                "rewards": rewards,
                "party_status": [(card.id, card.raid_cooldown) for card in raiding_party]
            }
        
        return {
            "success": False,
            "message": "Raid failed",
            "party_status": [(card.id, card.raid_cooldown) for card in raiding_party]
        }

def display_raid_menu(combat_system: EnhancedCombatSystem, available_warriors: List[EnhancedCard]) -> str:
    menu = ["\n=== RAID MENU ==="]
    
    # Display available warriors
    menu.append("\nAVAILABLE WARRIORS:")
    for warrior in available_warriors:
        if warrior.raid_cooldown == 0:
            menu.append(str(warrior))
    
    # Display raid tiers
    menu.append("\nRAID TIERS:")
    for tier_num, tier in combat_system.raid_tiers.items():
        menu.append(f"\n{tier.name} (Tier {tier_num})")
        menu.append(f"Cost: {tier.coin_cost} coins")
        menu.append(f"Difficulty Multiplier: x{tier.difficulty_multiplier}")
        if tier_num < len(combat_system.raid_tiers):
            menu.append(f"Chance for Tier {tier_num + 1} loot: {tier.levels[-1]['rewards']['higher_tier_chance'] * 100}%")
    
    return "\n".join(menu)

