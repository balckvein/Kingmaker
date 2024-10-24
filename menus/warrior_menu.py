# menus/warrior_menu.py
from .base_menu import BaseMenu
from typing import Dict

class WarriorMenu(BaseMenu):
    def display(self) -> str:
        return """=== WARRIOR MANAGEMENT ===
1. View Warriors
2. Train Warrior
3. Equip Items
4. Heal Warriors
5. Return to Main Menu"""

    def handle_input(self, choice: int) -> Dict:
        if choice == 1:
            return {"success": True, "action": "view_warriors"}
        elif choice == 2:
            return {"success": True, "action": "train_warrior"}
        elif choice == 3:
            return {"success": True, "action": "equip_items"}
        elif choice == 4:
            return {"success": True, "action": "heal_warriors"}
        elif choice == 5:
            return {"success": True, "action": "main_menu"}
        return {"success": False, "message": "Invalid choice"}

# menus/raid_menu.py
class RaidMenu(BaseMenu):
    def display(self) -> str:
        return """=== RAID MENU ===
1. View Available Raids
2. Start Raid
3. View Raid History
4. Return to Main Menu"""

    def handle_input(self, choice: int) -> Dict:
        if choice == 1:
            return {"success": True, "action": "view_raids"}
        elif choice == 2:
            return {"success": True, "action": "start_raid"}
        elif choice == 3:
            return {"success": True, "action": "raid_history"}
        elif choice == 4:
            return {"success": True, "action": "main_menu"}
        return {"success": False, "message": "Invalid choice"}

# menus/shop_menu.py
class ShopMenu(BaseMenu):
    def display(self) -> str:
        return """=== SHOP MENU ===
1. Buy Items
2. Sell Items
3. View Prices
4. Return to Main Menu"""

    def handle_input(self, choice: int) -> Dict:
        if choice == 1:
            return {"success": True, "action": "buy_items"}
        elif choice == 2:
            return {"success": True, "action": "sell_items"}
        elif choice == 3:
            return {"success": True, "action": "view_prices"}
        elif choice == 4:
            return {"success": True, "action": "main_menu"}
        return {"success": False, "message": "Invalid choice"}

# menus/inventory_menu.py
class InventoryMenu(BaseMenu):
    def display(self) -> str:
        menu = ["=== INVENTORY ==="]
        
        # Display resources
        menu.append("\nResources:")
        for resource, amount in self.game.village.resources.items():
            menu.append(f"{resource.replace('_', ' ').title()}: {amount}")
        
        # Display equipment
        if hasattr(self.game.village, 'inventory'):
            menu.append("\nEquipment:")
            for i, item in enumerate(self.game.village.inventory, 1):
                menu.append(f"{i}. {str(item)}")
        
        menu.extend([
            "\n1. Use Item",
            "2. Sort Inventory",
            "3. Return to Main Menu"
        ])
        
        return "\n".join(menu)

    def handle_input(self, choice: int) -> Dict:
        if choice == 1:
            return {"success": True, "action": "use_item"}
        elif choice == 2:
            return {"success": True, "action": "sort_inventory"}
        elif choice == 3:
            return {"success": True, "action": "main_menu"}
        return {"success": False, "message": "Invalid choice"}