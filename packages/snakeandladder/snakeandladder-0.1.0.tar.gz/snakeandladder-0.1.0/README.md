[![Build Status](https://app.travis-ci.com/mohbay95/Project_533.svg?token=yEpB9SCgzfFwNhkKRgNZ&branch=main)](https://app.travis-ci.com/mohbay95/Project_533)

# Snake and Ladder Game

## Overview
This is a Python implementation of the classic Snake and Ladder board game. Players roll dice to move along a 100-cell board while navigating through snakes (which send players back to lower positions) and ladders (which help players advance). The game is designed with modularity and inheritance, making it easy to extend and maintain.

### Features:
- Two players (extendable for more players).
- Dice rolls determine player movement.
- Randomly placed snakes and ladders affect player positions.
- Modularity supports inheritance, making it easy to extend player capabilities.
- Tracks player statistics like dice rolls and turns played.
- Interactive, console-based game play.

## Project Structure

The project is divided into the following Python modules:

### 1. **`game.py`**: The main module for game logic.
   **Functions:**
   - `play_game()`: Starts and controls the game flow. It initializes the board, handles player turns, checks for snakes and ladders, and prints the updated board after each turn. It ends the game when a player reaches position 100.

   **Classes:**
   - `Game`: The main game class. It manages the game setup, snake and ladder placement, and alternating turns between players. It also checks for winner conditions and tracks game progression.

### 2. **`player.py`**: Contains player-related logic and classes.
   **Classes:**
   - `Player`: Represents a single player. It holds the player's current position and has methods for setting and getting positions.

     **Methods:**
     - `set_position(player_index, position)`: Sets the position of the player at the given index.
     - `get_position(player_index)`: Returns the current position of the player at the given index.
     - `get_positions()`: Returns a list of all player positions.

   - `AdvancedPlayer (inherits from Player)`: Adds extra features for tracking the number of dice rolls and turns played for each player.

     **Methods:**
     - `roll_dice()`: Simulates a dice roll for the player and updates the number of rolls.
     - `get_roll_count()`: Returns the total number of rolls made by the player.
     - `get_turns_played()`: Returns the number of turns the player has taken.
     - `reset_statistics()`: Resets the statistics (roll count and turn count) for the player.

### 3. **`board.py`**: Manages the game board layout and display.
   **Functions:**
   - `print_board_with_emojis(board_size, player_positions, snakes, ladders)`: Prints a visual representation of the board with emojis for empty spaces, snakes, ladders, and player positions. This function handles formatting to display the board in a 10x10 grid.
   - `reset_board()`: Resets the board to its initial state for a new game.

### 4. **`snakeandladder.py`**: Handles the placement of snakes and ladders on the board.
   **Functions:**
   - `create_snakes()`: Generates a dictionary with snake start and end positions, randomly or according to preset rules.
   - `create_ladders()`: Generates a dictionary with ladder start and end positions, randomly or according to preset rules.

### 5. **`utility.py`**: Contains utility functions like dice rolling.
   **Functions:**
   - `roll_dice()`: Simulates a dice roll (random integer between 1 and 6).
   - `print_ascii_message(message)`: Prints the provided message in ASCII art. The message is transformed into stylized ASCII art 
      based on predefined messages. You can extend this function to add more custom messages.
  


## How to Play

1. **Start the Game**: Run the `game.py` script to start the game. The game will initialize with two players starting at position 1 on the board.
2. **Roll the Dice**: Each player takes turns rolling a dice. If a player lands on a snake, they move down the board; if they land on a ladder, they climb up the board.
3. **Win the Game**: The first player to reach position 100 wins the game. The game will automatically print the board after each roll and announce the winner.
4. **Exit the Game**: You can exit the game by pressing `q` during your turn.

