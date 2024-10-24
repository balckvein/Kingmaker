from abc import ABC, abstractmethod
from typing import Dict, Optional
import os


class BaseMenu(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def display(self) -> str:
        """Display the menu options"""
        pass

    @abstractmethod
    def handle_input(self, choice: int) -> Dict:
        """Handle menu input"""
        pass

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_input(self, prompt: str = "Enter your choice: ") -> str:
        """Get user input with proper error handling"""
        return input(prompt).strip()
