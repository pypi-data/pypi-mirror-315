import unittest
from Board.board import Board
from SnakesAndLadders.snakesandladders import SnakeAndLadder
from Player.player import Player
from Utility.utility import Utility
from Game.game import Game
import random
from unittest.mock import patch

class TestGame(unittest.TestCase):

    
    @classmethod
    def setUpClass(cls):
        """Called once before any tests in this class are executed."""
        print("\nSetting up the test class for Game tests...")

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in this class have been executed."""
        print("\nTearing down the test class for Game tests...")

    def setUp(self):
        """Called before every individual test."""
        print("\nSetting up for a test in the Game test class...")
        self.game = Game()  # Initialize a new Game object before each test

    def tearDown(self):
        """Called after each individual test."""
        print("\nTearing down after a test in the Game test class...")
        self.game = None  # Cleanup the game object after each test


    def test_initialization(self):
        # Test if the game initializes correctly
        self.assertEqual(self.game.current_player, 0)
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.snake_and_ladder)
        self.assertIsNotNone(self.game.players)

    def test_dice_roll(self):
        # Test if dice roll is valid
        roll = Utility.roll_dice()
        self.assertIn(roll, range(1, 7))



    def test_handle_snakes(self):
        """Test if a player slides down when landing on a snake."""
        self.game.snake_and_ladder.snakes = {16: 6}  # Snake from 16 to 6
        new_position = self.game.handle_snakes_and_ladders(16)
        self.assertEqual(new_position, 6)

    def test_handle_ladders(self):
        """Test if a player climbs up when landing on a ladder."""
        self.game.snake_and_ladder.ladders = {3: 22}  # Ladder from 3 to 22
        new_position = self.game.handle_snakes_and_ladders(3)
        self.assertEqual(new_position, 22)

    def test_handle_no_snakes_or_ladders(self):
        """Test if a player remains in the same position when not on a snake or ladder."""
        self.game.snake_and_ladder.snakes = {16: 6}
        self.game.snake_and_ladder.ladders = {3: 22}
        new_position = self.game.handle_snakes_and_ladders(10)
        self.assertEqual(new_position, 10)

    def test_check_winning_condition_true(self):
        """Test if the winning condition is correctly identified."""
        self.game.board.size = 100
        self.game.players.positions = [100, 50]
        self.game.current_player = 0
        result = self.game.check_winning_condition()
        self.assertTrue(result)

    def test_check_winning_condition_false(self):
        """Test if the game continues when no player has won."""
        self.game.board.size = 100
        self.game.players.positions = [99, 50]
        self.game.current_player = 0
        result = self.game.check_winning_condition()
        self.assertFalse(result)

    @patch("Utility.utility.Utility.roll_dice", return_value=4)
    @patch("builtins.input", lambda *args: None)  # Mock input to avoid manual entry
    def test_play_turn(self, mock_roll_dice):
        """Test a single turn of gameplay."""
        self.game.players.positions = [10, 20]
        self.game.current_player = 0
        result = self.game.play_turn()
        
        # Ensure the player moves correctly
        self.assertEqual(self.game.players.positions[0], 14)
        self.assertEqual(self.game.current_player, 1)
        self.assertFalse(result)  # The game should not end yet

    @patch("Utility.utility.Utility.display_ascii_art")
    def test_game_win_ascii_art(self, mock_display_ascii_art):
        """Test if the ASCII art is displayed when a player wins."""
        self.game.board.size = 100
        self.game.players.positions = [100, 50]
        self.game.current_player = 0
        result = self.game.check_winning_condition()
        
        # Verify ASCII art display
        mock_display_ascii_art.assert_called_once_with("CONGRATULATIONS")
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()



