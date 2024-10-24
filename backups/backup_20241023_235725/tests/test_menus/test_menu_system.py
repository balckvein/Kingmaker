
import unittest
from unittest.mock import Mock
from src.menus.menu_system import MenuSystem
from src.menus.base_menu import BaseMenu

class TestMenuSystem(unittest.TestCase):
    def setUp(self):
        self.game_mock = Mock()
        self.menu_system = MenuSystem(self.game_mock)
        
        # Create mock menu
        self.mock_menu = Mock(spec=BaseMenu)
        self.menu_system.register_menu("test_menu", self.mock_menu)
    
    def test_navigation(self):
        """Test menu navigation"""
        # Test successful navigation
        self.assertTrue(self.menu_system.navigate("test_menu"))
        self.assertEqual(self.menu_system.current_menu, "test_menu")
        self.assertEqual(len(self.menu_system.history), 1)
        
        # Test navigation to non-existent menu
        self.assertFalse(self.menu_system.navigate("non_existent"))
    
    def test_back_navigation(self):
        """Test back navigation"""
        self.menu_system.navigate("test_menu")
        previous_menu = self.menu_system.back()
        self.assertEqual(previous_menu, "main")
        self.assertEqual(len(self.menu_system.history), 0)

if __name__ == '__main__':
    unittest.main()
