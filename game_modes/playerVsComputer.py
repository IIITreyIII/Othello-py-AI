# game_modes/playerVsComputer.py

import pygame
import time
from board import Board
from settings import HEADER_HEIGHT, WIDTH, SIDEBAR_WIDTH
import sys
from game_modes.AI import AIMode

def run_game(win):
    board = Board()
    ai = AIMode(depth=5)  # Set a higher depth for a challenging AI
    current_color = 'B'
    clock = pygame.time.Clock()
    ai_delay = 1.0  # 1-second delay for AI move
    last_move_time = None  # Track time of the last move

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] >= WIDTH - SIDEBAR_WIDTH:
                    action = board.sidebar.handle_click(pos)
                    if action == "toggle_debug":
                        ai.set_debug_mode(board.sidebar.debug_mode, board, current_color)
                    elif action == "update_depth":
                        new_depth = board.sidebar.get_depth()
                        ai.set_depth(new_depth, board, current_color)
                    elif action == "smart_move" and board.sidebar.debug_mode:
                        if ai.make_best_move(board, current_color):
                            current_color = 'W' if current_color == 'B' else 'B'
                    elif action == "toggle_alpha_beta":
                        ai.use_alpha_beta = board.sidebar.use_alpha_beta
                    elif action == "return_to_menu":
                        return  # Exit the game loop and return to the main menu
                    elif action == "new_game":
                        return run_game(win)  # Restart the game
                elif not board.game_over and pos[0] < WIDTH - SIDEBAR_WIDTH and pos[1] > HEADER_HEIGHT:
                    # Check if the move was valid
                    move_successful = board.handle_click(pos, current_color)
                    if move_successful:
                        # Valid move by player
                        current_color = 'W'  # Switch to computer's turn
                        last_move_time = time.time()  # Record the time of the player’s move
                        board.display_message("Computer's Turn", duration=ai_delay)
                    else:
                        # Invalid move, switch to computer's turn but keep the delay
                        current_color = 'W'
                        last_move_time = time.time()  # Start the delay timer here as well
                        board.display_message("Invalid Move! Computer's Turn", duration=ai_delay)

            elif event.type == pygame.KEYDOWN:
                board.sidebar.handle_key_event(event)
        
        # Check if it's the computer's turn and the delay has passed
        if current_color == 'W' and not board.game_over:
            if last_move_time and (time.time() - last_move_time >= ai_delay):
                ai.calculate_best_move(board, 'W')  # Calculate the best move for the AI
                ai.make_best_move(board, 'W')  # Make the best move for the AI
                current_color = 'B'  # Switch back to the player

        # Draw the board
        board.draw(win, current_color)
        pygame.display.flip()
        clock.tick(30)
