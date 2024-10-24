# card_game.py
import random
from typing import List, Dict
from combat import CombatSystem
from raid_systems import EnhancedCard, EnhancedCombatSystem, Equipment, display_raid_menu

class GameLogger:
    @staticmethod
    def combat_log(message: str):
        print(f"\n[COMBAT] {message}")
    
    @staticmethod
    def raid_log(message: str):
        print(f"\n[RAID] {message}")
    
    @staticmethod
    def resource_log(message: str):
        print(f"\n[RESOURCE] {message}")
    
    @staticmethod
    def status_log(message: str):
        print(f"\n[STATUS] {message}")
        
class Equipment:
    def __init__(self, name: str, equip_type: str, tier: int, rarity: str, stats: Dict):
        self.name = name
        self.type = equip_type
        self.tier = tier
        self.rarity = rarity
        self.durability = 100
        self.max_durability = 100
        self.stats = stats
        
    def repair(self, amount: int):
        self.durability = min(self.max_durability, self.durability + amount)
        
    def __str__(self):
        stats_str = ", ".join([f"{k}: {v}" for k, v in self.stats.items()])
        return f"{self.name} ({self.rarity} Tier {self.tier}) | {stats_str} | Durability: {self.durability}%"
        
class BaseCard:
    def __init__(self, card_id: int, card_type: str, stats: Dict):
        self.id = card_id
        self.type = card_type
        self.stats = stats
        self.victories = 0
        self.raids_survived = 0
        self.status = "ready"  # ready, tired, injured

    def __str__(self):
        return (f"Card #{self.id} ({self.type}) | "
                f"STR: {self.stats['strength']}, "
                f"HP: {self.stats['health']}, "
                f"DEF: {self.stats['defense']} | "
                f"Status: {self.status}")

class Card:
    def __init__(self, card_id: int, card_type: str, stats: Dict):
        self.id = card_id
        self.type = card_type
        self.stats = stats
        self.victories = 0
        self.raids_survived = 0
        self.status = "ready"  # ready, tired, injured

    def __str__(self):
        return (f"Card #{self.id} ({self.type}) | STR: {self.stats['strength']}, "
                f"HP: {self.stats['health']}, DEF: {self.stats['defense']} | "
                f"Status: {self.status}")

class Village:
    def __init__(self):
        self.population = []  # List of cards
        self.resources = {
            "food": 10,
            "wood": 5,
            "stone": 3,
            "flint": 1,
            "coins": 100
        }
        self.buildings = []
        self.raid_cooldown = 0
        self.inventory = []  # For storing unequipped items

    def add_resources(self, resources: Dict[str, int]):
        for resource, amount in resources.items():
            self.resources[resource] = self.resources.get(resource, 0) + amount
            
    def remove_resources(self, resources: Dict[str, int]) -> bool:
        # Check if we have enough resources
        for resource, amount in resources.items():
            if self.resources.get(resource, 0) < amount:
                return False
        
        # Remove resources
        for resource, amount in resources.items():
            self.resources[resource] -= amount
        return True

class CardGame:
    def __init__(self):
        self.village = Village()
        self.combat_system = CombatSystem()
        self.day = 1
        self.card_counter = 0
        self.logger = GameLogger()
        
    def display_status(self) -> str:
        """Display current game status"""
        status = [
            "\n=== GAME STATUS ===",
            f"Day: {self.day}",
            f"Raid Cooldown: {self.village.raid_cooldown}",
            "\n=== RESOURCES ===",
            f"Food: {self.village.resources['food']}",
            f"Wood: {self.village.resources['wood']}",
            f"Stone: {self.village.resources['stone']}",
            f"Flint: {self.village.resources['flint']}",
            "\n=== POPULATION ==="
        ]
        
        for card in self.village.population:
            status.append(
                f"#{card.id} {card.type}: "
                f"STR:{card.stats['strength']}, "
                f"HP:{card.stats['health']}, "
                f"DEF:{card.stats['defense']} | "
                f"Status: {card.status} | "
                f"Victories: {card.victories} | "
                f"Raids: {card.raids_survived}"
            )
        
        if self.village.buildings:
            status.append("\n=== BUILDINGS ===")
            for building in self.village.buildings:
                status.append(str(building))
                
        return "\n".join(status)

    def create_card(self, card_type: str) -> Card:
        """Create a new card with specified type"""
        stats = {
            "warrior": {
                "strength": random.randint(3, 6),
                "health": random.randint(10, 15),
                "defense": 2,
                "gathering": 1
            },
            "elite": {
                "strength": random.randint(6, 9),
                "health": random.randint(15, 20),
                "defense": 3,
                "gathering": 2
            },
            "champion": {
                "strength": random.randint(9, 12),
                "health": random.randint(20, 25),
                "defense": 4,
                "gathering": 3
            }
        }
        
        self.card_counter += 1
        card = Card(self.card_counter, card_type, stats.get(card_type, stats["warrior"]))
        self.logger.status_log(f"Created new {card_type}: {card}")
        return card

    def conduct_raid(self, raiding_party: List[Card]) -> Dict:
        """Conduct a raid with selected cards"""
        self.logger.raid_log("Preparing for raid...")
        self.logger.raid_log(f"Raiding party: {[str(card) for card in raiding_party]}")
        
        if self.village.raid_cooldown > 0:
            self.logger.raid_log(f"Raid on cooldown for {self.village.raid_cooldown} more days")
            return {"success": False, "message": f"Raid on cooldown for {self.village.raid_cooldown} more days"}
            
        if not raiding_party:
            self.logger.raid_log("No raiders selected")
            return {"success": False, "message": "No raiders selected"}
        
        # Check if all raiders are ready
        if not all(card.status == "ready" for card in raiding_party):
            self.logger.raid_log("Not all raiders are ready")
            return {"success": False, "message": "Not all raiders are ready"}
        
        # Calculate defender strength based on day number
        defender_strength = 15 + (self.day * 2)
        self.logger.raid_log(f"Defender strength: {defender_strength}")
        
        # Conduct raid
        success, captives, resources = self.combat_system.conduct_raid(raiding_party, defender_strength)
        
        # Update raider status
        for raider in raiding_party:
            raider.status = "tired"
            if success:
                raider.raids_survived += 1
                self.logger.status_log(f"Raider {raider.id} survived another raid (Total: {raider.raids_survived})")
        
        # Apply raid results
        if success:
            self.logger.raid_log("Raid successful!")
            # Add resources
            for resource, amount in resources.items():
                self.village.resources[resource] = self.village.resources.get(resource, 0) + amount
                self.logger.resource_log(f"Gained {amount} {resource}")
            
            # Create captive cards
            new_captives = []
            for _ in range(captives):
                captive = self.create_card("warrior")
                new_captives.append(captive)
                self.village.population.append(captive)  # Add captives to village population
                self.logger.status_log(f"Captured new warrior: {captive}")
            
            self.village.raid_cooldown = 3
            self.logger.raid_log(f"Raid cooldown set to {self.village.raid_cooldown} days")
            
            return {
                "success": True,
                "message": "Raid successful!",
                "resources_gained": resources,
                "captives": len(new_captives),
                "raiders_status": [(r.id, r.status) for r in raiding_party]
            }
        
        self.logger.raid_log("Raid failed!")
        return {
            "success": False,
            "message": "Raid failed!",
            "raiders_status": [(r.id, r.status) for r in raiding_party]
        }

    def arena_combat(self, fighters: List[Card]) -> Dict:
        """Conduct arena combat between selected fighters"""
        self.logger.combat_log("Beginning arena combat...")
        self.logger.combat_log(f"Fighters: {[str(card) for card in fighters]}")
        
        if len(fighters) < 2:
            self.logger.combat_log("Need at least 2 fighters")
            return {"success": False, "message": "Need at least 2 fighters"}
        
        # Check if all fighters are ready
        if not all(card.status == "ready" for card in fighters):
            self.logger.combat_log("Not all fighters are ready")
            return {"success": False, "message": "Not all fighters are ready"}
        
        winner = self.combat_system.arena_combat(fighters)
        
        if winner:
            winner.victories += 1
            self.logger.combat_log(f"Winner: {winner}")
            self.logger.combat_log(f"Fighter {winner.id} now has {winner.victories} victories")
            
            # Update status of all fighters
            for fighter in fighters:
                if fighter != winner:
                    fighter.status = "injured"
                    self.logger.status_log(f"Fighter {fighter.id} is now injured")
                else:
                    fighter.status = "tired"
                    self.logger.status_log(f"Winner {fighter.id} is now tired")
            
            return {
                "success": True,
                "message": f"Fighter {winner.id} wins!",
                "winner_stats": winner.stats,
                "fighters_status": [(f.id, f.status) for f in fighters]
            }
        
        self.logger.combat_log("No winner determined")
        return {"success": False, "message": "No winner determined"}

    def end_day(self) -> Dict:
        """End the current day and update game state"""
        self.logger.status_log(f"=== Ending Day {self.day} ===")
        
        # Update raid cooldown
        if self.village.raid_cooldown > 0:
            self.village.raid_cooldown -= 1
            self.logger.status_log(f"Raid cooldown reduced to {self.village.raid_cooldown}")
        
        # Refresh card statuses
        for card in self.village.population:
            old_status = card.status
            if card.status == "tired":
                card.status = "ready"
            elif card.status == "injured":
                card.status = "tired"
            if old_status != card.status:
                self.logger.status_log(f"Card {card.id} status changed: {old_status} -> {card.status}")
        
        # Consume food
        total_food_cost = sum(1 for card in self.village.population)
        self.logger.resource_log(f"Food needed: {total_food_cost}")
        if self.village.resources["food"] >= total_food_cost:
            self.village.resources["food"] -= total_food_cost
            self.logger.resource_log(f"Consumed {total_food_cost} food. Remaining: {self.village.resources['food']}")
        else:
            self.logger.resource_log("Not enough food!")
            return {"success": False, "message": "Not enough food!"}
        
        self.day += 1
        
        # Check for special event (every 30 days)
        special_event = (self.day % 30 == 0)
        if special_event:
            self.logger.status_log("=== SPECIAL EVENT DAY ===")
        
        return {
            "success": True,
            "message": f"Day {self.day} begins",
            "food_remaining": self.village.resources["food"],
            "special_event": special_event
        }

def test_game():
    game = CardGame()
    game.combat_system = EnhancedCombatSystem()
    
    # Add initial population
    game.logger.status_log("=== Initializing Game ===")
    for _ in range(3):
        card = game.create_card("warrior")
        game.village.population.append(card)
    
    # Display initial status
    print(game.display_status())
    
    # Conduct a raid
    game.logger.status_log("=== Testing Raid ===")
    raiders = game.village.population[:2]  # Select first two warriors
    raid_result = game.conduct_raid(raiders)
    print("\nRaid Result:", raid_result)
    
    # Test arena combat
    game.logger.status_log("=== Testing Arena Combat ===")
    fighters = game.village.population[1:]  # Select last two warriors
    combat_result = game.arena_combat(fighters)
    print("\nCombat Result:", combat_result)
    
    # End the day
    end_day_result = game.end_day()
    print("\nEnd Day Result:", end_day_result)
    
    # Display updated status
    print(game.display_status())

if __name__ == "__main__":
    test_game()