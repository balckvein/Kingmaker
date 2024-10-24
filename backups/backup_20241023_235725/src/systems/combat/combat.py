# combat.py
import random
from typing import List, Dict, Tuple


class CombatSystem:
    def __init__(self):
        self.arena_rounds = 3
        self.victory_threshold = 0.7
        self.promotion_chance = 0.3
        self.capture_rate = 0.4
        
    def conduct_raid(self, attacking_force: List, defender_strength: int) -> Tuple[bool, int, Dict]:
        """
        Conducts a raid with the given attacking force against a defense of specified strength
        Returns: (success, captives, resources)
        """
        # Calculate total attacking strength
        total_strength = sum(self._calculate_effective_strength(warrior) for warrior in attacking_force)
        
        # Calculate success chance based on strength ratio
        success_chance = (total_strength / defender_strength) * 0.4  # Base success chance
        success_chance = min(success_chance * 1.5, 0.9)  # Cap at 90% chance
        
        if random.random() < success_chance:
            captives = self._calculate_captives(defender_strength)
            resources = self._calculate_raid_resources(defender_strength)
            
            # Update raid survival counts
            for warrior in attacking_force:
                warrior.raids_survived += 1
                
            return True, captives, resources
        return False, 0, {}

    def arena_combat(self, fighters: List) -> object:
        """
        Conducts a tournament between fighters
        Returns: winner
        """
        if len(fighters) < 2:
            return None
            
        remaining = fighters.copy()
        
        while len(remaining) > 1:
            fighter1 = random.choice(remaining)
            remaining.remove(fighter1)
            fighter2 = random.choice(remaining)
            remaining.remove(fighter2)
            
            winner = self._resolve_duel(fighter1, fighter2)
            remaining.append(winner)
            
        return remaining[0] if remaining else None

    def _resolve_duel(self, fighter1, fighter2) -> object:
        """Resolves combat between two fighters"""
        f1_health = fighter1.stats["health"]
        f2_health = fighter2.stats["health"]
        
        for round in range(self.arena_rounds):
            # Calculate base damage using the fighter's strength stat
            f1_damage = fighter1.stats["strength"] + random.randint(-1, 1)
            f2_damage = fighter2.stats["strength"] + random.randint(-1, 1)
            
            # Apply victory bonuses
            f1_damage *= (1 + fighter1.victories * 0.1)
            f2_damage *= (1 + fighter2.victories * 0.1)
            
            # Apply defense
            f1_damage = max(0, f1_damage - fighter2.stats["defense"])
            f2_damage = max(0, f2_damage - fighter1.stats["defense"])
            
            # Apply damage
            f1_health -= f2_damage
            f2_health -= f1_damage
            
            if f1_health <= 0 or f2_health <= 0:
                break
        
        # Return winner based on remaining health percentage
        f1_health_percent = f1_health / fighter1.stats["health"]
        f2_health_percent = f2_health / fighter2.stats["health"]
        
        return fighter1 if f1_health_percent > f2_health_percent else fighter2

    def _calculate_effective_strength(self, warrior) -> float:
        """Calculates effective strength including bonuses from victories and raids"""
        base_strength = warrior.stats["strength"]
        victory_bonus = warrior.victories * 0.1
        raid_bonus = warrior.raids_survived * 0.05
        
        return base_strength * (1 + victory_bonus + raid_bonus)

    def _calculate_captives(self, defender_strength: int) -> int:
        """Calculate number of captives from raid"""
        base_captives = defender_strength // 5
        return max(1, int(base_captives * self.capture_rate))
    
    def _calculate_raid_resources(self, defender_strength: int) -> Dict:
        """Calculate resources gained from raid"""
        base_resources = defender_strength * 2
        return {
            "food": random.randint(base_resources // 4, base_resources),
            "wood": random.randint(base_resources // 8, base_resources // 4),
            "stone": random.randint(base_resources // 8, base_resources // 4),
            "flint": random.randint(0, base_resources // 10)
        }