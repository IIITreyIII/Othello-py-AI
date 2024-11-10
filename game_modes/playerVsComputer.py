# game_modes/playerVsComputer.py

import pygame
from board import Board
from settings import HEADER_HEIGHT, WIDTH, SIDEBAR_WIDTH
import sys
from game_modes.AI import AIMode

def run_game(win):
    board = Board()
    ai = AIMode(depth=5)  # Set a higher depth for a challenging AI
    current_color = 'B'
    clock = pygame.time.Clock()

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
                elif not board.game_over and pos[0] < WIDTH - SIDEBAR_WIDTH and pos[1] > HEADER_HEIGHT:
                    if board.handle_click(pos, current_color):
                        current_color = 'W' if current_color == 'B' else 'B'

            elif event.type == pygame.KEYDOWN:
                board.sidebar.handle_key_event(event)
        
        # AI makes a move if it's the computer's turn
        if current_color == 'W' and not board.game_over:
            ai.calculate_best_move(board, 'W')  # Calculate the best move for the AI
            ai.make_best_move(board, 'W')  # Make the best move for the AI
            current_color = 'B'  # Switch back to the player

        board.draw(win, current_color)
        pygame.display.flip()
        clock.tick(30)
