
from datetime import datetime
from typing import Dict, Any

class ErrorHandler:
    def __init__(self):
        self.error_stack = []
    
    def handle_error(self, error_type: str, message: str, context: Dict[str, Any]) -> str:
        """Handle an error and return user-friendly message"""
        error = {
            'type': error_type,
            'message': message,
            'context': context,
            'timestamp': datetime.now()
        }
        self.error_stack.append(error)
        return self.get_user_message(error_type)
    
    def get_user_message(self, error_type: str) -> str:
        """Get user-friendly error message"""
        ERROR_MESSAGES = {
            'invalid_input': 'Invalid input provided. Please try again.',
            'insufficient_resources': 'Not enough resources for this action.',
            'invalid_state': 'Cannot perform this action in the current state.',
            'system_error': 'A system error occurred. Please try again.'
        }
        return ERROR_MESSAGES.get(error_type, "An unexpected error occurred")
    
    def clear_errors(self):
        """Clear the error stack"""
        self.error_stack = []
