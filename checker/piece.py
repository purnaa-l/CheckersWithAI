# Import necessary constants and pygame for drawing
from .constants import PURPLE, YELLOW, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    """
    Represents a single game piece in the checkers game.
    Handles piece attributes like position, color, and king status,
    as well as drawing and movement on the board.
    """
    PADDING = 15  # Padding around the piece for visual separation
    OUTLINE = 5  # Outline thickness for the piece's border

    def __init__(self, row, col, color):
        """
        Initializes a Piece instance.

        Args:
            row (int): The initial row of the piece on the board.
            col (int): The initial column of the piece on the board.
            color (tuple): The RGB color of the piece.
        """
        self.row = row  # Row position of the piece on the board
        self.col = col  # Column position of the piece on the board
        self.color = color  # Color of the piece (PURPLE or YELLOW)
        self.king = False  # Flag to indicate if the piece is a king
        self.x = 0  # x-coordinate for drawing the piece (calculated later)
        self.y = 0  # y-coordinate for drawing the piece (calculated later)
        self.calc_pos()  # Calculate initial screen position based on row/col

    def calc_pos(self):
        """
        Calculates the pixel position of the piece's center based on its row and column.
        This is used for drawing the piece at the correct location.
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2  # x-coordinate of the center
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2  # y-coordinate of the center

    def make_king(self):
        """
        Promotes the piece to a king.
        A king can move both forward and backward on the board.
        """
        self.king = True

    def draw(self, win):
        """
        Draws the piece on the game window.

        Args:
            win: The Pygame window surface where the piece will be drawn.
        """
        # Radius of the piece (slightly smaller than a square for padding)
        radius = SQUARE_SIZE // 2 - self.PADDING

        # Draw the outer border of the piece (GREY outline)
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        # Draw the inner circle representing the piece (color-filled)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        
        # If the piece is a king, draw the crown symbol at its center
        if self.king:
            # Center the crown image on the piece
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        """
        Moves the piece to a new position on the board.

        Args:
            row (int): The new row to move the piece to.
            col (int): The new column to move the piece to.
        """
        self.row = row  # Update the row
        self.col = col  # Update the column
        self.calc_pos()  # Recalculate the screen position for drawing

    def __repr__(self):
        """
        Returns a string representation of the piece, mainly for debugging.

        Returns:
            str: The string representation of the piece's color.
        """
        return str(self.color)  # Convert color (tuple) to string for clarity
