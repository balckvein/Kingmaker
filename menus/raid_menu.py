from .base_menu import BaseMenu
from typing import Dict

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
