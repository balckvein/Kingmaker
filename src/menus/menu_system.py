# menu_system.py (continued)
from typing import Dict, List, Optional
from src.menus.main_menu import MainMenu  # These imports are correct
from src.menus.village_menu import VillageMenu
from progression_system import EnhancedCard
from src.menus.warrior_menu import WarriorMenu
from src.menus.raid_menu import RaidMenu
from src.menus.shop_menu import ShopMenu
from src.menus.inventory_menu import InventoryMenu
import os


class MenuSystem:
    def __init__(self, game):
        self.game = game
        self.current_menu = "main"
        self.menu_history = []
        self.menus = {
            "main": MainMenu(game),
            "village": VillageMenu(game),
            "warrior": WarriorMenu(game),
            "raid": RaidMenu(game),
            "shop": ShopMenu(game),
            "inventory": InventoryMenu(game)
        }
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_and_wait(self, message: str):
        """Display a message and wait for user input"""
        self.clear_screen()
        print(message)
        input("\nPress Enter to continue...")

    def navigate_to(self, menu_name: str):
        """Navigate to a new menu"""
        if menu_name in self.menus:
            self.menu_history.append(self.current_menu)
            self.current_menu = menu_name

    def go_back(self):
        """Return to the previous menu"""
        if self.menu_history:
            self.current_menu = self.menu_history.pop()

    def display_main_menu(self) -> str:
        menu = [
            "\n=== MAIN MENU ===",
            "1. View Village Status",
            "2. Manage Warriors",
            "3. Raid Menu",
            "4. Shop",
            "5. Inventory",
            "6. End Day",
            "7. Save Game",
            "8. Exit",
            "\nEnter your choice (1-8): "
        ]
        return "\n".join(menu)
        
    def display_warrior_menu(self, warrior: 'EnhancedCard') -> str:
        menu = [
            f"\n=== WARRIOR #{warrior.id} MENU ===",
            str(warrior),
            "\n1. Equip/Unequip Items",
            "2. Spend Skill Points",
            "3. View Stats History",
            "4. Repair Equipment",
            "5. Back to Main Menu",
            "\nEnter your choice (1-5): "
        ]
        return "\n".join(menu)
        
    def display_raid_menu(self) -> str:
        menu = [
            "\n=== RAID MENU ===",
            "Available Warriors:",
        ]
        
        # Add available warriors
        for warrior in self.game.village.population:
            if warrior.raid_cooldown == 0:
                menu.append(f"  {warrior.id}: {warrior.char_class} (Level {warrior.level})")
        
        menu.extend([
            "\nRaid Tiers:",
            "1. Woods (50 coins) - Tier 1",
            "   - 25% chance for Tier 2 loot",
            "2. Caves (150 coins) - Tier 2",
            "   - 10% chance for Tier 3 loot",
            "3. Fort (300 coins) - Tier 3",
            "   - 5% chance for Tier 4 loot",
            "\nEnter raid tier (1-3) or 0 to return: "
        ])
        return "\n".join(menu)
        
    def display_shop_menu(self) -> str:
        current_prices = self.game.village.economy.get_current_prices()
        
        menu = [
            "\n=== SHOP ===",
            f"Available Coins: {self.game.village.resources['coins']}",
            "\nBUY PRICES:",
        ]
        
        for item, price in current_prices.items():
            menu.append(f"{item}: {price} coins")
            
        menu.extend([
            "\n1. Buy Resources",
            "2. Sell Resources",
            "3. Buy Equipment",
            "4. Sell Equipment",
            "5. Back to Main Menu",
            "\nEnter your choice (1-5): "
        ])
        return "\n".join(menu)
        
    def display_inventory_menu(self) -> str:
        menu = [
            "\n=== INVENTORY ===",
            "\nResources:",
        ]
        
        # Add resources
        for resource, amount in self.game.village.resources.items():
            menu.append(f"{resource}: {amount}")
            
        # Add equipment
        menu.append("\nEquipment:")
        for i, item in enumerate(self.game.village.inventory, 1):
            menu.append(f"{i}. {item}")
            
        menu.extend([
            "\n1. Use Item",
            "2. Sort Inventory",
            "3. Back to Main Menu",
            "\nEnter your choice (1-3): "
        ])
        return "\n".join(menu)

    def handle_input(self, menu_type: str, choice: str) -> Dict:
        """Handle user input for different menus"""
        if menu_type == "main":
            return self._handle_main_menu(choice)
        elif menu_type == "warrior":
            return self._handle_warrior_menu(choice)
        elif menu_type == "raid":
            return self._handle_raid_menu(choice)
        elif menu_type == "shop":
            return self._handle_shop_menu(choice)
        elif menu_type == "inventory":
            return self._handle_inventory_menu(choice)
        return {"success": False, "message": "Invalid menu type"}

    def _handle_main_menu(self, choice: str) -> Dict:
        try:
            choice = int(choice)
            if choice == 1:
                return {"success": True, "action": "status", "message": self.game.display_status()}
            elif choice == 2:
                return {"success": True, "action": "warriors"}
            elif choice == 3:
                return {"success": True, "action": "raid"}
            elif choice == 4:
                return {"success": True, "action": "shop"}
            elif choice == 5:
                return {"success": True, "action": "inventory"}
            elif choice == 6:
                return {"success": True, "action": "end_day"}
            elif choice == 7:
                return {"success": True, "action": "save"}
            elif choice == 8:
                return {"success": True, "action": "exit"}
            else:
                return {"success": False, "message": "Invalid choice"}
        except ValueError:
            return {"success": False, "message": "Please enter a number"}

    def run(self):
        """Main menu loop"""
        running = True
        while running:
            self.clear_screen()
            current_menu = self.menus[self.current_menu]
            print(current_menu.display())
            
            try:
                choice = int(input("Enter your choice: "))
                result = current_menu.handle_input(choice)
                
                if not result["success"]:
                    self.display_and_wait(result["message"])
                    continue
                    
                running = self.handle_menu_action(result)
                
            except ValueError:
                self.display_and_wait("Please enter a valid number")
            except Exception as e:
                self.display_and_wait(f"An error occurred: {str(e)}")
    
    def handle_menu_action(self, result: Dict) -> bool:
        """Handle menu actions and navigation"""
        action = result.get("action")
        
        if action == "exit":
            return False
            
        elif action == "main_menu":
            self.current_menu = "main"
            self.menu_history.clear()  # Clear history when returning to main menu
            
        elif action == "navigate":
            menu = result.get("menu")
            if menu:
                self.navigate_to(menu)
            
        elif action == "back":
            self.go_back()
            
        elif action == "status":
            self.display_and_wait(result.get("message", self.game.display_status()))
            
        # Warrior menu actions
        elif action in ["view_warriors", "train_warrior", "equip_items", "heal_warriors"]:
            if action == "view_warriors":
                message = "=== Warriors ===\n"
                for warrior in self.game.village.population:
                    message += f"{str(warrior)}\n"
            else:
                message = f"{action.replace('_', ' ').title()} not implemented yet"
            self.display_and_wait(message)
            
        # Raid menu actions
        elif action in ["view_raids", "start_raid", "raid_history"]:
            message = f"{action.replace('_', ' ').title()} not implemented yet"
            self.display_and_wait(message)
            
        return True