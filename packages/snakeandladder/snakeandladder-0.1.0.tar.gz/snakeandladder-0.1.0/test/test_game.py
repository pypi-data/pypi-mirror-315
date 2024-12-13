import unittest
from Board.board import Board
from SnakesAndLadders.snakesandladders import SnakeAndLadder
from Player.player import Player
from Utility.utility import Utility
from Game.game import Game


class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called once before any tests in this class are executed."""
        print("\nSetting up the test class for Game tests...")
        cls.snakes = {16: 6}
        cls.ladders = {4: 14}

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in this class have been executed."""
        print("\nTearing down the test class for Game tests...")

    def setUp(self):
        """Called before every individual test."""
        print("\nSetting up for a test in the Game test class...")
        self.game = Game()  # Initialize a new Game object before each test
        self.game.snake_and_ladder.snakes = self.snakes  # Set snakes for testing
        self.game.snake_and_ladder.ladders = self.ladders  # Set ladders for testing

    def tearDown(self):
        """Called after each individual test."""
        print("\nTearing down after a test in the Game test class...")
        self.game = None  # Cleanup the game object after each test

    def test_game_initialization(self):
        """Test the initial setup of the game."""
        self.assertEqual(self.game.players.get_positions(), [1, 1], "Players should start at position 1")
        self.assertEqual(self.game.board.get_size(), 100, "Board size should be 100")
        self.assertDictEqual(self.game.snake_and_ladder.snakes, self.snakes, "Snakes should match the initial setup.")
        self.assertDictEqual(self.game.snake_and_ladder.ladders, self.ladders, "Ladders should match the initial setup.")

    def test_player_turn(self):
        """Test if the player's turn plays correctly."""
        self.game.players.set_position(0, 95)  # Set Player 1 near the finish
        self.game.current_player = 0
        self.game.play_turn()  # Play one turn
        player_position = self.game.players.get_position(0)
         
        self.assertIn(self.game.players.get_position(0), range(96, 101), "Player 1 should move within valid range")
        self.assertGreaterEqual(player_position, 95, "Player 1 should not move backward.")
        self.assertLessEqual(player_position, 100, "Player 1 should not exceed the board size.")
        if player_position == 100:
            self.assertTrue(player_position == 100, "Player 1 should win if reaching 100.")


