import unittest
from Board.board import Board
from SnakesAndLadders.snakesandladders import SnakeAndLadder
from Player.player import Player
from Utility.utility import Utility
from Game.game import Game

class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called once before any tests in this class are executed."""
        print("\nSetting up the test class for Player tests...")

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in this class have been executed."""
        print("\nTearing down the test class for Player tests...")

    def setUp(self):
        """Called before every individual test."""
        print("\nSetting up for a test in the Player test class...")
        self.players = Player()  # Initialize a new Player object before each test

    def tearDown(self):
        """Called after each individual test."""
        print("\nTearing down after a test in the Player test class...")
        self.players = None  # Cleanup the Player object after each test

    def test_initial_positions(self):
        """Test the initial positions of the players."""
        self.assertEqual(self.players.get_positions(), [1, 1], "Both players should start at position 1")
        self.assertEqual(self.players.get_position(0), 1, "Player 1 should start at position 1.")
        self.assertEqual(self.players.get_position(1), 1, "Player 2 should start at position 1.")
        self.assertNotEqual(self.players.get_position(0), 0, "Player 1 should not start at position 0.")

    def test_update_position(self):
        """Test if the position update works correctly."""
        self.players.set_position(0, 20)
        self.assertEqual(self.players.get_position(0), 20, "Player 1 should move to position 20")
        self.assertNotEqual(self.players.get_position(0), 1, "Player 1 should no longer be at position 1.")
        self.players.set_position(1, 35)
        self.assertEqual(self.players.get_position(1), 35, "Player 2 should move to position 35")
        self.assertNotEqual(self.players.get_position(1), 1, "Player 2 should no longer be at position 1.")



class TestAdvancedPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called once before any tests in this class are executed."""
        print("\nSetting up the test class for AdvancedPlayer tests...")

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in this class are executed."""
        print("\nTearing down the test class for AdvancedPlayer tests...")

    def setUp(self):
        """Called before every individual test."""
        print("\nSetting up for a test in the AdvancedPlayer test class...")
        self.advanced_players = AdvancedPlayer()  # Initialize an AdvancedPlayer object before each test

    def tearDown(self):
        """Called after each individual test."""
        print("\nTearing down after a test in the AdvancedPlayer test class...")
        self.advanced_players = None  # Cleanup the AdvancedPlayer object after each test

    def test_initial_rolls_and_turns(self):
        """Test the initial dice rolls and turns played for advanced players."""
        self.assertEqual(self.advanced_players.get_rolls(0), 0, "Player 1 should start with 0 dice rolls.")
        self.assertEqual(self.advanced_players.get_rolls(1), 0, "Player 2 should start with 0 dice rolls.")
        self.assertEqual(self.advanced_players.get_turns(0), 0, "Player 1 should start with 0 turns played.")
        self.assertEqual(self.advanced_players.get_turns(1), 0, "Player 2 should start with 0 turns played.")

    def test_increment_rolls_and_turns(self):
        """Test incrementing dice rolls and turns played."""
        self.advanced_players.increment_rolls(0)
        self.assertEqual(self.advanced_players.get_rolls(0), 1, "Player 1 should have 1 dice roll after increment.")
        self.advanced_players.increment_rolls(1)
        self.assertEqual(self.advanced_players.get_rolls(1), 1, "Player 2 should have 1 dice roll after increment.")
        self.advanced_players.increment_turns(0)
        self.assertEqual(self.advanced_players.get_turns(0), 1, "Player 1 should have 1 turn played after increment.")
        self.advanced_players.increment_turns(1)
        self.assertEqual(self.advanced_players.get_turns(1), 1, "Player 2 should have 1 turn played after increment.")

    def test_combined_player_functionality(self):
        """Test the combined functionality of advanced player positions and stats."""
        self.advanced_players.set_position(0, 50)
        self.advanced_players.increment_rolls(0)
        self.advanced_players.increment_turns(0)

        self.assertEqual(self.advanced_players.get_position(0), 50, "Player 1 should be at position 50.")
        self.assertEqual(self.advanced_players.get_rolls(0), 1, "Player 1 should have 1 dice roll.")
        self.assertEqual(self.advanced_players.get_turns(0), 1, "Player 1 should have 1 turn played.")
        self.assertNotEqual(self.advanced_players.get_position(0), 1, "Player 1 should not be at position 1.")


