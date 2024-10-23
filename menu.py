# menu.py

def display_game_state(game):
    print(f"\n--- Turn {game.turn} ---")
    print("Player Army:")
    for character in game.player_army:
        print(f"- {character.card_type}: Health {character.health}, STR {character.strength}, DEF {character.defense}, INT {character.intelligence}")
    
    print("\nResources:")
    for resource, amount in game.resources.items():
        print(f"- {resource}: {amount}")
    
    print("\nBuildings:")
    for building in game.buildings:
        print(f"- {building.card_type}")

def display_menu(game):
    print("\nAvailable Actions:")
    print("1. Gather Resources (Cost: None, Benefit: Random resource)")
    
    print("\nAvailable Buildings:")
    for i, (building, data) in enumerate(game.available_buildings.items(), start=2):
        cost_str = ", ".join(f"{resource}: {amount}" for resource, amount in data["cost"].items())
        print(f"{i}. Build {building} (Cost: {cost_str}, Benefit: {data['benefit']})")
    
    print("\nAvailable Characters:")
    for i, (character, data) in enumerate(game.available_characters.items(), start=len(game.available_buildings)+2):
        cost_str = ", ".join(f"{resource}: {amount}" for resource, amount in data["cost"].items())
        stats_str = ", ".join(f"{stat}: {value}" for stat, value in data["stats"].items())
        print(f"{i}. Recruit {character} (Cost: {cost_str}, Stats: {stats_str}, Ability: {data['ability']})")
    
    print(f"{len(game.available_buildings) + len(game.available_characters) + 2}. End Turn")

def get_player_choice(game):
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(game.available_buildings) + len(game.available_characters) + 2:
                return choice
        print("Invalid choice. Please try again.")