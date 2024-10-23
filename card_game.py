import random
import menu

class Character:
    def __init__(self, card_type, health, strength, defense, intelligence, special_ability):
        self.card_type = card_type
        self.health = health
        self.strength = strength
        self.defense = defense
        self.intelligence = intelligence
        self.special_ability = special_ability

class Resource:
    def __init__(self, name, amount, type=None):
        if not isinstance(type, dict):
            self.type = type
            self.name = name
            self.amount = amount
        else:
            for key, value in type.items():
                setattr(self, key, value)

class Building:
    def __init__(self, card_type, cost=None, upgrade_cost=None, upgrade_benefit=None, special_ability=""):
        if not isinstance(cost, dict):
            self.cost = {"Wood": 2, "Stone": 1}
            self.upgrade_cost = None
            self.upgrade_benefit = None
            self.special_ability = special_ability
        else:
            self.cost = cost
            self.upgrade_cost = upgrade_cost
            self.upgrade_benefit = upgrade_benefit
            self.special_ability = special_ability

class Game:
    def __init__(self):
        self.player_army = []
        self.resources = {}
        self.buildings = {
            "House": {"card_type": "House", "cost": {"Wood": 2, "Stone": 1}, "benefit": "Allows recruiting 1 villager"},
            "Lumber Hut": {"card_type": "Lumber Hut", "cost": {"Wood": 5, "Flint": 2}, "benefit": "Increases wood gathering", "upgrade_cost": {"Flint": 3}},
            "Quarry": {"card_type": "Quarry", "cost": {"Stone": 6, "Flint": 3}, "benefit": "Increases stone gathering"},
            "Smithy": {"card_type": "Smithy", "cost": {"Stone": 6, "Iron": 2}, "benefit": "Allows crafting tools and weapons"}
        }
        self.available_characters = {
            "Villager": {"cost": {"Food": 5}, "stats": {"Health": 8, "STR": 2, "DEF": 2, "INT": 1}, "ability": "Base character"},
            "Hero": {"cost": {"Food": 10, "Iron": 5}, "stats": {"Health": 12, "STR": 4, "DEF": 3, "INT": 2}, "ability": "Leadership Bonus"}
        }

    def add_character(self, character):
        self.player_army.append(character)

    def add_resource(self, resource_type, amount):
        if resource_type in self.resources:
            self.resources[resource_type] += amount
        else:
            self.resources[resource_type] = amount

    def build(self, building_type):
        if building_type["card_type"] in self.buildings:
            cost = self.buildings[building_type["card_type"]]["cost"]
            for resource, amount in cost.items():
                self.resources[resource] -= amount
            if "upgrade_cost" in self.buildings[building_type["card_type"]]:
                upgrade_cost = self.buildings[building_type["card_type"]]["upgrade_cost"]
                for resource, amount in upgrade_cost.items():
                    self.resources[resource] -= amount
            else:
                print("No upgrade cost")
            self.add_building(Building(building_type["card_type"], str(cost), self.buildings[building_type["card_type"]]["benefit"], 
                                        upgrade_cost=self.buildings[building_type["card_type"]]["upgrade_cost"] if "upgrade_cost" in self.buildings[building_type["card_type"]] else None,
                                        upgrade_benefit=self.buildings[building_type["card_type"]]["benefit"] if "upgrade_cost" in self.buildings[building_type["card_type"]] else ""))
            print(f"Built a {building_type['card_type']}")
        else:
            print("Invalid building type")

    def recruit_character(self, character_type):
        if character_type in self.available_characters:
            cost = self.available_characters[character_type]["cost"]
            for resource, amount in cost.items():
                self.resources[resource] -= amount
            stats = self.available_characters[character_type]["stats"]
            ability = self.available_characters[character_type]["ability"]
            self.add_character(Character(character_type, stats["Health"], stats["STR"], stats["DEF"], stats["INT"], ability))
            print(f"Recruited a {character_type}")
        else:
            print("Invalid character type")

    def gather_resources(self):
        resources = ["Wood", "Stone", "Iron Ore", "Food"]
        gathered = random.choice(resources)
        amount = random.randint(1, 3)
        self.add_resource(gathered, amount)
        print(f"Gathered {amount} {gathered}")

    def play_turn(self):
        menu.display_game_state(self)
        menu.display_menu(self)
        
        choice = menu.get_player_choice(self)
        
        if choice == 1:
            self.gather_resources()
        elif 2 <= choice <= len(self.buildings) + len(self.available_characters) + 1:
            building_type = list(self.buildings.values())[choice - 2]
            self.build(building_type)
        elif (len(self.buildings) + len(self.available_characters) + 1) % 2 == 0:
            character_type = list(self.available_characters.keys())[choice - len(self.buildings) - 2]
            self.recruit_character(character_type)
        elif choice == len(self.buildings) + len(self.available_characters) + 2:
            self.turn += 1
        else:
            print("Invalid choice. Try again.")

    def get_turn(self):
        return self.turn

def display_game_state(game):
    print(f"\n--- Turn {game.get_turn()} ---")

def main():
    game = Game()
    
    while True:
        if len(game.player_army) < 1:
            continue
        else:
            game.add_character(Character("Villager", 8, 2, 2, 1, "Base character"))
        
        game.play_turn()
        if game.turn > 10:  
            break

    print("\nGame Over!")
    menu.display_game_state(game)

if __name__ == "__main__":
    main()