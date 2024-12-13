import unittest
from Board.board import Board
from SnakesAndLadders.snakesandladders import SnakeAndLadder
from Player.player import Player
from Utility.utility import Utility
from Game.game import Game

class TestUtility(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called once before any tests in this class are executed."""
        print("\nSetting up the test class for Utility tests...")

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in this class have been executed."""
        print("\nTearing down the test class for Utility tests...")

    def setUp(self):
        """Called before every individual test."""
        print("\nSetting up for a test in the Utility test class...")

    def tearDown(self):
        """Called after each individual test."""
        print("\nTearing down after a test in the Utility test class...")

    def test_roll_dice(self):
        """Test the dice roll function."""
        rolls = [Utility.roll_dice() for _ in range(100)]  # Roll dice multiple times
        
        # Check that all rolls are within the expected range
        for roll in rolls:
            self.assertIn(roll, range(1, 7), f"Dice roll {roll} is out of range, should be between 1 and 6.")
        
        # Check minimum and maximum values were rolled
        self.assertIn(1, rolls, "Dice roll did not produce the minimum value of 1.")
        self.assertIn(6, rolls, "Dice roll did not produce the maximum value of 6.")
        
        # Check the number of rolls
        self.assertEqual(len(rolls), 100, "Dice rolls should generate 100 results.")
        self.assertTrue(all(isinstance(roll, int) for roll in rolls), "All dice rolls should be integers.")

    def test_display_ascii_art_welcome(self):
        """Test the ASCII art display for the welcome message."""
        try:
            Utility.display_ascii_art("WELCOME TO SNAKES AND LADDERS")
        except Exception as e:
            self.fail(f"display_ascii_art() raised an exception with valid input: {e}")
        
        # Check if the function is callable and does not return a value
        result = Utility.display_ascii_art("WELCOME TO SNAKES AND LADDERS")
        self.assertIsNone(result, "display_ascii_art should not return any value.")
        self.assertTrue(callable(Utility.display_ascii_art), "display_ascii_art should be callable.")

    def test_display_ascii_art_default(self):
        """Test the ASCII art display for the default message."""
        try:
            Utility.display_ascii_art()
        except Exception as e:
            self.fail(f"display_ascii_art() raised an exception with no input: {e}")
        
        # Check if the function handles default cases without errors
        result = Utility.display_ascii_art()
        self.assertIsNone(result, "display_ascii_art should not return any value.")
        self.assertTrue(callable(Utility.display_ascii_art), "display_ascii_art should be callable.")

    def test_display_ascii_art_unrecognized(self):
        """Test the ASCII art display for unrecognized input."""
        try:
            Utility.display_ascii_art("RANDOM TEXT")
        except Exception as e:
            self.fail(f"display_ascii_art() raised an exception with unrecognized input: {e}")
        
        # Check that it handles unrecognized input gracefully
        result = Utility.display_ascii_art("RANDOM TEXT")
        self.assertIsNone(result, "display_ascii_art should not return any value.")
        self.assertTrue(callable(Utility.display_ascii_art), "display_ascii_art should be callable.")

