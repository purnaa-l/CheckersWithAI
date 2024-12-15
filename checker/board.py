import pygame
from .constants import WHITE, ROWS, PINK, SQUARE_SIZE, COLS, YELLOW, PURPLE
from .piece import Piece

class Board:
    """
    The Board class represents the checkers game board and contains methods
    to manage the state of the board, move pieces, calculate valid moves, and more.
    """
    def __init__(self):
        """
        Initializes the board by creating a 2D list of pieces and sets up the
        number of pieces left for both players. Calls create_board to set up the board.
        """
        self.board = []  # 2D list to store the pieces on the board
        self.red_left = self.white_left = 12  # Each player starts with 12 pieces
        self.red_kings = self.white_kings = 0  # Tracks the number of kings for each player
        self.create_board()  # Initializes the board with pieces

    def evaluate(self):
        """
        Evaluates the current state of the board for AI. It calculates a score
        based on the number of pieces left and the number of kings.

        Returns:
            float: The evaluation score of the board.
        """
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        """
        Returns a list of all pieces of the given color.

        Args:
            color (str): The color of the pieces to fetch (YELLOW or PURPLE).

        Returns:
            list: A list of pieces of the given color.
        """
        pieces = []
        for row in self.board:  # Iterate through each row of the board
            for piece in row:  # Iterate through each column in the row
                if piece != 0 and piece.color == color:  # Check if the piece matches the color
                    pieces.append(piece)  # Add the piece to the list
        return pieces  # Return the list of pieces

    def draw_squares(self, win):
        """
        Draws the alternating squares on the board using Pygame.

        Args:
            win (pygame.Surface): The window surface to draw the squares.
        """
        win.fill(PINK)  # Fill the background with the pink color
        for row in range(ROWS):  # Loop through the rows
            for col in range(row % 2, COLS, 2):  # Loop through columns with alternating colors
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        """
        Moves a piece to the new position on the board and handles promotion to a king.

        Args:
            piece (Piece): The piece to move.
            row (int): The row to move the piece to.
            col (int): The column to move the piece to.
        """
        # Swap the piece on the board with the destination square
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)  # Update the piece's position

        # If the piece reaches the last row, it is promoted to a king
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == YELLOW:
                self.white_kings += 1  # Increase the count of white kings
            else:
                self.red_kings += 1  # Increase the count of red kings

    def get_piece(self, row, col):
        """
        Returns the piece at the specified row and column.

        Args:
            row (int): The row of the piece.
            col (int): The column of the piece.

        Returns:
            Piece or int: The piece at the specified location or 0 if empty.
        """
        return self.board[row][col]

    def create_board(self):
        """
        Initializes the board with alternating pieces for the two players. Pieces are placed
        on the first three and last three rows for each player, and empty squares are set for the middle rows.

        Returns:
            None
        """
        for row in range(ROWS):  # Loop through the rows
            self.board.append([])  # Start a new row
            for col in range(COLS):  # Loop through the columns
                if col % 2 == ((row + 1) % 2):  # Alternate the squares
                    if row < 3:  # First three rows (yellow pieces)
                        self.board[row].append(Piece(row, col, YELLOW))
                    elif row > 4:  # Last three rows (purple pieces)
                        self.board[row].append(Piece(row, col, PURPLE))
                    else:
                        self.board[row].append(0)  # Middle rows (empty squares)
                else:
                    self.board[row].append(0)  # Add empty squares for the odd columns

    def draw(self, win):
        """
        Draws the board and all the pieces on the game window.

        Args:
            win (pygame.Surface): The window surface to draw the board and pieces on.
        """
        self.draw_squares(win)  # Draw the squares on the board
        for row in range(ROWS):  # Loop through the rows
            for col in range(COLS):  # Loop through the columns
                piece = self.board[row][col]  # Get the piece at the current position
                if piece != 0:  # If there is a piece, draw it
                    piece.draw(win)

    def remove(self, pieces):
        """
        Removes the captured pieces from the board and updates the count of remaining pieces.

        Args:
            pieces (list): A list of pieces to remove.
        """
        for piece in pieces:  # Loop through the captured pieces
            self.board[piece.row][piece.col] = 0  # Set the captured piece's position to empty
            if piece != 0:  # If the piece exists
                if piece.color == PURPLE:
                    self.red_left -= 1  # Decrease the count of red pieces
                else:
                    self.white_left -= 1  # Decrease the count of yellow pieces

    def winner(self):
        """
        Checks if there is a winner based on the number of pieces left.

        Returns:
            str or None: The winner's color (YELLOW or PURPLE), or None if no winner yet.
        """
        if self.red_left <= 0:
            return YELLOW  # Yellow wins if there are no red pieces left
        elif self.white_left <= 0:
            return PURPLE  # Purple wins if there are no yellow pieces left
        return None  # Return None if no winner yet

    def get_valid_moves(self, piece):
        """
        Returns a dictionary of valid moves for the specified piece. The keys are positions,
        and the values are lists of skipped pieces (if any).

        Args:
            piece (Piece): The piece for which valid moves are to be calculated.

        Returns:
            dict: A dictionary of valid moves.
        """
        moves = {}  # Dictionary to store valid moves
        left = piece.col - 1  # Left column offset
        right = piece.col + 1  # Right column offset
        row = piece.row  # Current row of the piece

        # Handle moves for purple or king pieces (moving upwards)
        if piece.color == PURPLE or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))  # Traverse left
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))  # Traverse right

        # Handle moves for yellow or king pieces (moving downwards)
        if piece.color == YELLOW or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))  # Traverse left
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))  # Traverse right

        return moves  # Return the dictionary of valid moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """
        Helper function to traverse left and calculate valid moves, including captures.

        Args:
            start (int): The starting row for traversal.
            stop (int): The stopping row for traversal.
            step (int): The step for row iteration (either -1 or 1).
            color (str): The color of the piece being moved.
            left (int): The left column offset.
            skipped (list): A list of pieces that were captured.

        Returns:
            dict: A dictionary of valid moves from the current position.
        """
        moves = {}
        last = []  # Tracks the last piece encountered (for captures)
        for r in range(start, stop, step):  # Iterate over the rows
            if left < 0:  # If left goes out of bounds, break
                break
            
            current = self.board[r][left]  # Get the piece at the current position
            if current == 0:  # If it's an empty square
                if skipped and not last:  # If there's a capture but no last piece
                    break
                elif skipped:  # If there's a captured piece, add it to the moves
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last  # Add the current path of moves
                
                if last:  # If a capture was made, look further ahead
                    if step == -1:  # If moving up
                        row = max(r - 3, 0)
                    else:  # If moving down
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))  # Traverse further left
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))  # Traverse further right
                break
            elif current.color == color:  # If the piece is the same color, stop
                break
            else:
                last = [current]  # Mark this as a captured piece

            left -= 1  # Move left by 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """
        Helper function to traverse right and calculate valid moves, including captures.

        Args:
            start (int): The starting row for traversal.
            stop (int): The stopping row for traversal.
            step (int): The step for row iteration (either -1 or 1).
            color (str): The color of the piece being moved.
            right (int): The right column offset.
            skipped (list): A list of pieces that were captured.

        Returns:
            dict: A dictionary of valid moves from the current position.
        """
        moves = {}
        last = []  # Tracks the last piece encountered (for captures)
        for r in range(start, stop, step):  # Iterate over the rows
            if right >= COLS:  # If right goes out of bounds, break
                break
            
            current = self.board[r][right]  # Get the piece at the current position
            if current == 0:  # If it's an empty square
                if skipped and not last:  # If there's a capture but no last piece
                    break
                elif skipped:  # If there's a captured piece, add it to the moves
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last  # Add the current path of moves
                
                if last:  # If a capture was made, look further ahead
                    if step == -1:  # If moving up
                        row = max(r - 3, 0)
                    else:  # If moving down
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))  # Traverse further left
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))  # Traverse further right
                break
            elif current.color == color:  # If the piece is the same color, stop
                break
            else:
                last = [current]  # Mark this as a captured piece

            right += 1  # Move right by 1
        
        return moves
