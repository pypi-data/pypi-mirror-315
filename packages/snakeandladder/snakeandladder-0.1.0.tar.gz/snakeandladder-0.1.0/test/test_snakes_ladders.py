import unittest
from Board.board import Board
from SnakesAndLadders.snakesandladders import SnakeAndLadder
from Player.player import Player
from Utility.utility import Utility
from Game.game import Game

class TestSnakeAndLadder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called once before any tests in this class are executed."""
        print("\nSetting up the test class for Snake and Ladder tests...")
        cls.default_snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        cls.default_ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in this class have been executed."""
        print("\nTearing down the test class for Snake and Ladder tests...")

    def setUp(self):
        """Called before every individual test."""
        print("\nSetting up for a test in the Snake and Ladder test class...")
        self.snakes_and_ladders = SnakeAndLadder()  # Initialize a new SnakeAndLadder object before each test

    def tearDown(self):
        """Called after each individual test."""
        print("\nTearing down after a test in the Snake and Ladder test class...")
        self.snakes_and_ladders = None  # Cleanup the SnakeAndLadder object after each test

    def test_snakes_positions(self):
        """Test if the snakes are correctly placed on the board."""
        snakes = self.snakes_and_ladders.get_snakes()

        self.assertEqual(snakes, self.default_snakes, "Snakes should match the default setup.")
        self.assertIn(16, snakes, "Snake at position 16 should exist.")
        self.assertEqual(snakes[16], 6, "Snake at position 16 should lead to position 6.")
        self.assertNotIn(15, snakes, "There should not be a snake at position 15.")

    def test_ladders_positions(self):
        """Test if the ladders are correctly placed on the board."""
        ladders = self.snakes_and_ladders.get_ladders()

        self.assertEqual(ladders, self.default_ladders, "Ladders should match the default setup.")
        self.assertIn(1, ladders, "Ladder at position 1 should exist.")
        self.assertEqual(ladders[1], 38, "Ladder at position 1 should lead to position 38.")
        self.assertNotIn(2, ladders, "There should not be a ladder at position 2.")
