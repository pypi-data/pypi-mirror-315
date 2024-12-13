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


    def test_default_snakes_and_ladders(self):
        game = SnakeAndLadder()
        self.assertIn(16, game.get_snakes())
        self.assertIn(4, game.get_ladders())

    def test_set_valid_snakes(self):
        game = SnakeAndLadder()
        snakes = {25: 5, 45: 15}
        game.set_snakes(snakes)
        self.assertEqual(game.get_snakes(), snakes)

   
if __name__ == "__main__":
    unittest.main()
