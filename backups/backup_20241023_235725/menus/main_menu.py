# menus/main_menu.py
from .base_menu import BaseMenu
from typing import Dict

class MainMenu(BaseMenu):
    def display(self) -> str:
        menu = [
            "=== MAIN MENU ===",
            "1. View Village Status",
            "2. Manage Warriors",
            "3. Raid Menu",
            "4. Shop",
            "5. Inventory",
            "6. End Day",
            "7. Save Game",
            "8. Exit"
        ]
        return "\n".join(menu)

    def handle_input(self, choice: str) -> Dict:
        try:
            choice = int(choice)
            if choice == 1:
                return {
                    "success": True,
                    "action": "status",
                    "message": self.game.display_status()
                }
            elif choice == 2:
                return {"success": True, "action": "navigate", "menu": "warrior"}
            elif choice == 3:
                return {"success": True, "action": "navigate", "menu": "raid"}
            elif choice == 4:
                return {"success": True, "action": "navigate", "menu": "shop"}
            elif choice == 5:
                return {"success": True, "action": "navigate", "menu": "inventory"}
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


