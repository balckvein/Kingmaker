
from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from ..core.error_handler import ErrorHandler

class BaseMenu(ABC):
    def __init__(self, game_instance):
        self.game = game_instance
        self.error_handler = ErrorHandler()
    
    @abstractmethod
    def display(self) -> str:
        """Display menu options"""
        pass
    
    @abstractmethod
    def handle_input(self, user_input: str) -> Tuple[str, Optional[str]]:
        """Handle user input and return (next_menu, error_message)"""
        pass
    
    def validate_input(self, user_input: str, valid_options: List[str]) -> bool:
        """Validate user input"""
        return user_input in valid_options
