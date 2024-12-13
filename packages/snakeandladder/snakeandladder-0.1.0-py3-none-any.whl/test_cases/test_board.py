from Board.board import InvalidPositionError
import unittest
from Board.board import Board
from SnakesAndLadders.snakesandladders import SnakeAndLadder
from Player.player import Player
from Utility.utility import Utility
from Game.game import Game


class TestBoard(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        """Called once before any tests in this class are executed."""
        print("\nSetting up the test class for Board tests...")

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in this class have been executed."""
        print("\nTearing down the test class for Board tests...")

    def setUp(self):
        """Called before every individual test."""
        print("\nSetting up for a test in the Board test class...")
        self.board = Board(size=100)  # Initialize a new Board object before each test
        # Initialize player positions, snakes, and ladders
        self.player_positions = [1, 1]  # Player 1 at position 1, Player 2 at position 3
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

    def tearDown(self):
        """Called after each individual test."""
        print("\nTearing down after a test in the Board test class...")
        self.board = None  # Cleanup the board after each test
        

    def test_board_initialization(self):
        """Test board initialization and default values."""
        self.assertEqual(self.board.get_size(), 100)
        self.assertEqual(len(self.board.get_display_board()), 100)
        self.assertTrue(all(tile == '⬜' for tile in self.board.get_display_board()))

    def test_invalid_board_initialization(self):
        """Test invalid board sizes."""
        with self.assertRaises(ValueError):
            Board(size=0)
        with self.assertRaises(ValueError):
            Board(size=-10)
        with self.assertRaises(ValueError):
            Board(size="large")

    def test_set_display_board_success(self):
        """Test setting a valid display board."""
        new_board = ['⬜'] * 100
        self.board.set_display_board(new_board)
        self.assertEqual(self.board.get_display_board(), new_board)

    def test_set_display_board_failure(self):
        """Test setting an invalid display board."""
        with self.assertRaises(TypeError):
            self.board.set_display_board("invalid_type")
        with self.assertRaises(ValueError):
            self.board.set_display_board(['⬜'] * 50)

    def test_print_board_valid(self):
        """Test printing the board with valid snakes, ladders, and player positions."""
        player_positions = [1, 10]
        snakes = {16: 6}
        ladders = {3: 22}
        try:
            self.board.print_board_with_emojis(player_positions, snakes, ladders)
        except Exception as e:
            self.fail(f"print_board_with_emojis raised an exception: {e}")

    def test_snakes_out_of_bounds(self):
        """Test snakes with out-of-bounds positions."""
        player_positions = [1, 10]
        snakes = {101: 99}
        with self.assertRaises(InvalidPositionError):
            self.board.print_board_with_emojis(player_positions, snakes, {})

    def test_ladders_out_of_bounds(self):
        """Test ladders with out-of-bounds positions."""
        player_positions = [1, 10]
        ladders = {0: 20}
        with self.assertRaises(InvalidPositionError):
            self.board.print_board_with_emojis(player_positions, {}, ladders)

    def test_player_position_out_of_bounds(self):
        """Test player positions that are outside the board."""
        with self.assertRaises(InvalidPositionError):
            self.board.print_board_with_emojis([0, 10], {}, {})
        with self.assertRaises(InvalidPositionError):
            self.board.print_board_with_emojis([101, 10], {}, {})

    def test_snake_and_ladder_overlap(self):
        """Test a case where a snake and ladder overlap at the same position."""
        snakes = {5: 2}
        ladders = {5: 15}
        try:
            self.board.print_board_with_emojis([1, 2], snakes, ladders)
        except Exception as e:
            self.fail(f"print_board_with_emojis raised an exception for overlapping snakes and ladders: {e}")

    def test_player_collision(self):
        """Test when both players land on the same position."""
        player_positions = [10, 10]
        snakes = {16: 6}
        ladders = {3: 22}
        try:
            self.board.print_board_with_emojis(player_positions, snakes, ladders)
        except Exception as e:
            self.fail(f"print_board_with_emojis raised an exception for player collision: {e}")

    def test_edge_positions(self):
        """Test edge cases for the first and last positions on the board."""
        player_positions = [1, 100]
        snakes = {16: 6}
        ladders = {3: 22}
        try:
            self.board.print_board_with_emojis(player_positions, snakes, ladders)
        except Exception as e:
            self.fail(f"print_board_with_emojis raised an exception for edge positions: {e}")

 

if __name__ == "__main__":
    unittest.main()




