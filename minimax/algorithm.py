# Importing necessary libraries
from copy import deepcopy  # To create independent copies of complex objects like the board
import pygame  # For graphical display and user interface

# Defining the colors used in the game (RGB format)
PURPLE = (222, 111, 161)  # Player 1's color
YELLOW = (255, 204, 0)  # Player 2's (AI) color

# Minimax algorithm implementation
def minimax(position, depth, max_player, game):
    """
    Recursive implementation of the minimax algorithm with alpha-beta pruning.

    Args:
        position: The current state of the game board.
        depth: The maximum depth to explore the game tree.
        max_player: A boolean indicating whether it's the maximizing player's turn.
        game: The current game instance.

    Returns:
        A tuple (evaluation, best_move):
        - evaluation: The heuristic value of the board position.
        - best_move: The best board state for the current player.
    """
    # Base case: check if depth is 0 or if the game is over
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position  # Return the board evaluation and the current position

    # Maximizing player's logic (AI player)
    if max_player:
        maxEval = float('-inf')  # Initialize maximum evaluation
        best_move = None  # Placeholder for the best move
        for move in get_all_moves(position, YELLOW, game):  # Get all possible moves for AI
            # Recursively call minimax for the next depth with the minimizing player's turn
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)  # Update maxEval if a better evaluation is found
            if maxEval == evaluation:
                best_move = move  # Update best move if the current move is the best so far
        
        return maxEval, best_move  # Return the maximum evaluation and the corresponding move
    else:  # Minimizing player's logic (Human player)
        minEval = float('inf')  # Initialize minimum evaluation
        best_move = None  # Placeholder for the best move
        for move in get_all_moves(position, PURPLE, game):  # Get all possible moves for Human
            # Recursively call minimax for the next depth with the maximizing player's turn
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)  # Update minEval if a better evaluation is found
            if minEval == evaluation:
                best_move = move  # Update best move if the current move is the best so far
        
        return minEval, best_move  # Return the minimum evaluation and the corresponding move

# Simulates a move by updating the board state
def simulate_move(piece, move, board, game, skip):
    """
    Simulates a move by applying it to a board and optionally removing captured pieces.

    Args:
        piece: The piece being moved.
        move: The target position (row, col) for the move.
        board: The current state of the game board.
        game: The game instance (for any additional game-specific actions).
        skip: The piece to be captured, if any.

    Returns:
        The updated board after the move.
    """
    # Move the piece to the target position
    board.move(piece, move[0], move[1])
    if skip:  # If there is a piece to capture
        board.remove(skip)  # Remove the captured piece from the board

    return board

# Generates all possible moves for a given player
def get_all_moves(board, color, game):
    """
    Gets all possible moves for all pieces of a given color.

    Args:
        board: The current state of the game board.
        color: The color of the pieces to generate moves for.
        game: The game instance.

    Returns:
        A list of new board states, one for each possible move.
    """
    moves = []  # Initialize a list to store all possible moves
    
    # Iterate over all pieces of the given color
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)  # Get all valid moves for the piece
        for move, skip in valid_moves.items():  # Iterate through valid moves (move: target, skip: captured piece)
            # Create a deep copy of the board to simulate the move
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)  # Locate the corresponding piece on the copied board
            # Simulate the move on the temporary board
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)  # Add the resulting board state to the moves list
    
    return moves  # Return the list of all possible moves

# Draws the valid moves on the game board for visualization
def draw_moves(game, board, piece):
    """
    Highlights the valid moves for a given piece on the board.

    Args:
        game: The game instance (for window and drawing context).
        board: The current state of the game board.
        piece: The piece for which to highlight valid moves.

    Returns:
        None
    """
    valid_moves = board.get_valid_moves(piece)  # Get the valid moves for the given piece
    board.draw(game.win)  # Redraw the game board
    # Highlight the selected piece with a green circle
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    # Draw circles on all valid move positions
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()  # Update the display to show the changes
    # Uncomment the line below to add a delay for visualizing moves
    # pygame.time.delay(100)
