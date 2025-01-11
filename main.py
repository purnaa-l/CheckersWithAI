import pygame  # For graphics and game functionality
from checker.constants import WIDTH, HEIGHT, SQUARE_SIZE, PURPLE, YELLOW, BLACK, FONT_SIZE  # Constants used in the game
from checker.game import Game  # Game class to manage game logic
from minimax.algorithm import minimax  # Minimax algorithm for AI decisions
import gtts
import playsound as py
from os import path
import os
import pickle

def speak(msg):
    vd = gtts.gTTS(msg, lang='en-au')

    if path.exists('temp_audio.mp3'):
        os.remove('temp_audio.mp3')
    vd.save('temp_audio.mp3')
    py.playsound('temp_audio.mp3')

Frame rate per second for smooth gameplay
FPS = 60

# Creating the game window with predefined dimensions
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers With AI')  # Setting the title of the game window

def get_row_col_from_mouse(pos):
    """
    Converts the pixel position of the mouse click into board coordinates.

    Args:
        pos (tuple): Mouse position (x, y) in pixels.

    Returns:
        tuple: (row, col) indices of the board based on the mouse position.
    """
    x, y = pos
    row = y // SQUARE_SIZE  # Calculate row by dividing y-coordinate by square size
    col = x // SQUARE_SIZE  # Calculate column by dividing x-coordinate by square size
    return row, col

# Function to display the winner and total time taken
def display_winner(winner, time_taken):
    """
    Displays the winner and the total time taken at the end of the game.
    
    Args:
        winner (str): The winner of the game ("AI" or "Human").
        time_taken (int): The total time the game took in seconds.
    """
    font = pygame.font.SysFont('Times New Roman', FONT_SIZE)
    winner_text = font.render(f"Winner: {winner}", True, BLACK)
    time_text = font.render(f"Time Taken: {time_taken}s", True, BLACK)
    
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 40))
    WIN.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + 10))
    # speak(f"The winner is {winner}! Well played!")
    pygame.display.update()

   
def winner(self):
    """
    Determines the outcome of the game.

    Returns:
        str: "Human", "AI", "Draw", or None if no winner yet.
    """
    # Check if the human (Purple) has no pieces or cannot move
    human_pieces = self.get_all_pieces(PURPLE)
    if not human_pieces or not self.can_move(PURPLE):
        if not self.can_move(YELLOW):  # If AI also cannot move, it's a draw
            return "Draw"
        return "AI"  # AI wins if only Human cannot move

    # Check if the AI (Yellow) has no pieces or cannot move
    ai_pieces = self.get_all_pieces(YELLOW)
    if not ai_pieces or not self.can_move(YELLOW):
        if not self.can_move(PURPLE):  # If Human also cannot move, it's a draw
            return "Draw"
        return "Human"  # Human wins if only AI cannot move

    # Check for a draw when both sides have only one piece
    if len(human_pieces) == 1 and len(ai_pieces) == 1 and not self.can_move(PURPLE) and not self.can_move(YELLOW):
        return "Draw"
    if len(human_pieces)==1 and not self.can_move(PURPLE):
        return "Draw"

    return None  # No winner yet




# Main function to run the game loop
def main():
    """
    Main function to initialize the game loop, handle events, and manage AI moves.
    """
    pygame.font.init()  # Initialize the font system in pygame

    speak("Welcome to Checkers with AI. Do you want to listen to the instructions?")
    response = input("Do you want to listen to the instructions? (yes/no): ").strip().lower()
    
    if response == 'yes':
        instructions = (
            "The game is played between a Human and an AI. "
            "The goal is to capture all opponent's pieces or block them from making any move. "
            "Click on your pieces and then select the destination to make a move. "
            "AI plays as Yellow and you play as Purple. Please proceed to the pygame window to play your game! Good luck!"
        )
        speak(instructions)
    else:
        instructions=("Very Well. Please proceed to the pygame window to play your game. Good Luck!")
        speak(instructions)

    # Start the game
    run = True  # Boolean to control the main game loop
    clock = pygame.time.Clock()  # Clock to control frame rate
    game = Game(WIN)  # Create an instance of the Game class

    # Track the start time of the game
    start_time = pygame.time.get_ticks()

    # Main game loop
    while run:
        clock.tick(FPS)  # Limit the loop to the defined frames per second

    # AI Move: If it's the AI's turn (Yellow), compute the best move
        if game.turn == YELLOW:
            value, new_board = minimax(game.get_board(), 4, YELLOW, game)  # Depth set to 4
            game.ai_move(new_board)  # Apply the best move determined by the minimax algorithm

    # Check for a winner
        winner = game.winner()  # Get the winner (if any)
        if winner is not None:
            time_taken = (pygame.time.get_ticks() - start_time) // 1000  # Calculate time in seconds
            display_winner(winner, time_taken)  # Display winner and time
            pygame.time.delay(10000)  # Wait for 10 seconds before quitting
            run = False  # Exit the loop

    # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the close button is clicked
                run = False  # Exit the loop
        
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_s:  # Press 'S' to save the game
            #         save_game(game)
            #     elif event.key == pygame.K_l:  # Press 'L' to load the game
            #         game = load_game()

            if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse is clicked
                pos = pygame.mouse.get_pos()  # Get the position of the click
                row, col = get_row_col_from_mouse(pos)  # Convert to board coordinates
                game.select(row, col)  # Handle the selection

        game.update()  # Update the game state and redraw the screen
  # Update the game state and redraw the screen

    pygame.quit()  # Quit the game after the loop ends

# Run the main function to start the game
if __name__ == "__main__":
    main()
