import unittest
from unittest.mock import patch
from Utility.utility import Utility
import art

class TestUtility(unittest.TestCase):
    
    # Test for valid ASCII art display
    @patch('art.text2art')  # Mocking the `text2art` function
    def test_display_ascii_art_welcome(self, mock_text2art):
        Utility.display_ascii_art("WELCOME TO SNAKES AND LADDERS")
        mock_text2art.assert_called_once_with("SNAKES AND LADDERS")
    
    @patch('art.text2art')  # Mocking the `text2art` function
    def test_display_ascii_art_congratulations(self, mock_text2art):
        Utility.display_ascii_art("CONGRATULATIONS")
        mock_text2art.assert_called_once_with("CONGRATULATIONS")
    

if __name__ == '__main__':
    unittest.main()

