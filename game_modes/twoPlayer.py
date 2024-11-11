# Trey Ball
# CSC 475 Assignment 3
# 11-11-2024
# This is the two player game mode. It allows two players to play against each other, taking turns each move.
# The game ends when there are no more valid moves for either player. The player with the most pieces on the board wins.
# When things get hard, no need to fear, Debug mode is here! Turning on Debug mode will calculate the best move for the current player.
# Debug provides a 'Smart Move' button play the best move for the current player.
# At the end of each game, the player is given the option to start a new game or return to the main menu. 

import pygame
from board import Board
from settings import HEADER_HEIGHT, WIDTH, SIDEBAR_WIDTH
import sys
from game_modes.AI import AIMode

def run_game(win):
    board = Board()
    ai = AIMode(depth=3)
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
                        return
                    elif action == "new_game":
                        return run_game(win)
                elif not board.game_over and pos[0] < WIDTH - SIDEBAR_WIDTH and pos[1] > HEADER_HEIGHT:
                    board.handle_click(pos, current_color)
                    current_color = 'W' if current_color == 'B' else 'B'

            elif event.type == pygame.KEYDOWN:
                board.sidebar.handle_keypress(event)

        board.draw(win, current_color)
        pygame.display.flip()
        clock.tick(30)
