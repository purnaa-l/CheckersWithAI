from copy import deepcopy
import pygame

PURPLE = (222, 111, 161)
YELLOW = (255,204,0)

def minimax(position, depth, max_player, game):
    # Base case: if depth is 0 or game is over
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, YELLOW, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, PURPLE, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    # Move the piece on the board
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)  # Remove the captured piece if any

    return board


def get_all_moves(board, color, game):
    moves = []
    
    # Iterate over all pieces of the given color
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)  # Get the valid moves for each piece
        for move, skip in valid_moves.items():  # If valid_moves is a dictionary
            # Simulate the move on a deepcopy of the board
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)  # Add the new board state after the move
    
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)  # Uncomment to add a delay to visualize moves
