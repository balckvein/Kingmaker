# menus/shop_menu.py
from .base_menu import BaseMenu
from typing import Dict

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

