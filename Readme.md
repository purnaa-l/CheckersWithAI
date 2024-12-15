# Checkers With AI
This is a Python-based Checkers game where two players can either play against each other or play against an AI. The AI uses the Minimax algorithm to determine its moves. The game also includes features like timers for each turn, piece movement, capturing, promotion to kings, and more.

# Features
-Two-player mode: Two players can play on the same computer.

-AI Mode: One player can play against an AI that uses the Minimax algorithm to make decisions.

-Time-based turns: Each player has a set time limit per turn. If a player doesn't make a move within the time limit, the turn is forfeited.

-Game over conditions: The game ends when one player has no more pieces left or cannot make a valid move.

-Piece promotion: When a piece reaches the last row on the opponent's side, it gets promoted to a king.

-Capture mechanics: A piece can capture an opponent's piece by jumping over it.

# Requirements
Python 3.x
Pygame (for graphics and sounds)


# Game Rules
- Movement: Players can move their pieces diagonally on dark squares. Regular pieces can only move forward, while kings can move both forward and backward.

-Capturing: To capture an opponent’s piece, a player must jump over it, landing on the next available empty square.

-Promotion: If a piece reaches the opponent’s back row, it is promoted to a king. Kings can move both forward and backward.

-Timer: Each player has a set time limit to make a move. If the player doesn’t make a move in time, their turn is skipped.

-Victory Condition: The game ends when one player has no pieces left or cannot make any valid moves.

-Game Over: After the game ends, a message is displayed indicating the winner, and the player can press R to restart the game.
