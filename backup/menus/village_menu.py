from .base_menu import BaseMenu
from typing import Dict

class VillageMenu(BaseMenu):
    def display(self) -> str:
        status = "\n=== Village Status ===\n"
        status += f"Day: {self.game.current_day}\n"
        status += "\nPopulation:\n"
        status += f"Total Warriors: {len(self.game.village.population)}\n"
        
        class_counts = {}
        for warrior in self.game.village.population:
            class_counts[warrior.char_class] = class_counts.get(warrior.char_class, 0) + 1
        
        for class_name, count in class_counts.items():
            status += f"{class_name}s: {count}\n"
        
        status += "\nResources:\n"
        for resource, amount in self.game.village.resources.items():
            status += f"{resource.replace('_', ' ').title()}: {amount}\n"
        
        if self.game.village.buildings:
            status += "\nBuildings:\n"
            for building in self.game.village.buildings:
                status += f"- {building}\n"
                
        return status

    def handle_input(self, choice: int) -> Dict:
        return {"success": True, "action": "main_menu"}
