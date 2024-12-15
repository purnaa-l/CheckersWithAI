# Importing necessary libraries and constants
import pygame
from .constants import PINK, YELLOW, BLUE, SQUARE_SIZE, PURPLE
from checker.board import Board  # Importing the Board class to manage the game state

class Game:
    """
    The Game class controls the logic for the Checkers game.
    It handles the game's state, including piece selection, valid moves, and turn management.
    """
    def __init__(self, win):
        """
        Initializes the Game class with the game window.

        Args:
            win (pygame.Surface): The Pygame window to display the game.
        """
        self._init()  # Calls the _init method to initialize the game state
        self.win = win  # Stores the window surface to draw on

    def update(self):
        """
        Updates the game window by drawing the board and the valid moves.
        This method is called each frame to redraw the game state.

        Returns:
            None
        """
        self.board.draw(self.win)  # Draw the current state of the board
        self.draw_valid_moves(self.valid_moves)  # Highlight valid moves for the selected piece
        pygame.display.update()  # Update the display to reflect the changes

    def _init(self):
        """
        Initializes the game state including the board, turn, and selected piece.

        This method is used for resetting the game or starting a new game.

        Returns:
            None
        """
        self.selected = None  # No piece is selected initially
        self.board = Board()  # Create a new board instance
        self.turn = PURPLE  # Start the game with the PURPLE player's turn
        self.valid_moves = {}  # No valid moves initially

    def winner(self):
        """
        Returns the winner of the game if one exists.

        Returns:
            str or None: The winner color (PURPLE or YELLOW), or None if no winner yet.
        """
        return self.board.winner()  # Calls the Board class method to determine if there's a winner

    def reset(self):
        """
        Resets the game to its initial state.

        Returns:
            None
        """
        self._init()  # Re-initialize the game state using the _init method

    def select(self, row, col):
        """
        Selects a piece on the board based on user input (row, col).
        If a piece is already selected, attempts to move it to the target square.

        Args:
            row (int): The row index of the clicked square.
            col (int): The column index of the clicked square.

        Returns:
            bool: True if a valid piece was selected, False otherwise.
        """
        if self.selected:  # If a piece is already selected
            result = self._move(row, col)  # Try to move the piece
            if not result:  # If the move is invalid
                self.selected = None  # Deselect the piece
                self.select(row, col)  # Try to select a new piece
        
        piece = self.board.get_piece(row, col)  # Get the piece at the clicked position
        if piece != 0 and piece.color == self.turn:  # If the piece is not empty and belongs to the current player
            self.selected = piece  # Select the piece
            self.valid_moves = self.board.get_valid_moves(piece)  # Get valid moves for the selected piece
            return True
        
        return False  # Return False if no valid piece was selected

    def _move(self, row, col):
        """
        Attempts to move the selected piece to a new position.

        Args:
            row (int): The target row for the move.
            col (int): The target column for the move.

        Returns:
            bool: True if the move is successful, False otherwise.
        """
        piece = self.board.get_piece(row, col)  # Get the piece at the target position
        # If a piece is selected and the target square is empty and within valid moves
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)  # Move the selected piece
            skipped = self.valid_moves[(row, col)]  # Get any captured piece during the move
            if skipped:
                self.board.remove(skipped)  # Remove the captured piece
            self.change_turn()  # Switch the turn to the other player
        else:
            return False  # If the move is invalid, return False

        return True  # Return True if the move is successful

    def draw_valid_moves(self, moves):
        """
        Draws the valid moves for the selected piece as circles on the board.

        Args:
            moves (dict): A dictionary of valid moves, where keys are move positions
                          and values are the captured pieces (if any).
        """
        for move in moves:  # Loop through each valid move
            row, col = move  # Extract the row and column for the move
            # Draw a blue circle to indicate the valid move position
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                                row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        """
        Changes the current player's turn.

        Returns:
            None
        """
        self.valid_moves = {}  # Reset valid moves when changing turns
        if self.turn == PURPLE:  # If it was PURPLE's turn
            self.turn = YELLOW  # Switch to YELLOW's turn
        else:
            self.turn = PURPLE  # Switch back to PURPLE's turn

    def get_board(self):
        """
        Returns the current game board.

        Returns:
            Board: The current instance of the Board class.
        """
        return self.board  # Return the board instance

    def ai_move(self, board):
        """
        Updates the game state with the AI's move. The AI makes a move using the minimax algorithm.
        This method assumes that the board has already been updated with the AI's move.

        Args:
            board (Board): The new board state after the AI's move.
        """
        self.board = board  # Update the game board with the new state
        self.change_turn()  # Switch the turn to the other player (human player)
