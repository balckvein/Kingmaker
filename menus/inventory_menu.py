# menus/inventory_menu.py
from .base_menu import BaseMenu
from typing import Dict

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