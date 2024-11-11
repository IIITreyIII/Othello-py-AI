# Trey Ball
# CSC 475 Assignment 3
# 11-11-2024
# PvCPU.py is provides a main menu option for the player to play against a computer opponent.
# The difficulty of the CPU can be adjusted DEBUG menu by changing the depth, but its default is 5 (moderate).
# IT IS HIGHLY RECOMMENDED TO TURN ON ALPHA-BETA PRUNING IN THE DEBUG MENU, game performence slows very quickly every move without this.
# An intential timed delay was added to the CPU's move to make the game more enjoyable to play.

import pygame
import time
from board import Board
from settings import HEADER_HEIGHT, WIDTH, SIDEBAR_WIDTH
import sys
from game_modes.AI import AIMode

def run_game(win):
    board = Board()
    ai = AIMode(depth=5)
    current_color = 'B'
    clock = pygame.time.Clock()
    ai_delay = 1.0
    last_move_time = None

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
                    move_successful = board.handle_click(pos, current_color)
                    if move_successful:
                        current_color = 'W'
                        last_move_time = time.time()
                        board.display_message("Computer's Turn", duration=ai_delay)
                    else:
                        current_color = 'W'
                        last_move_time = time.time()
                        board.display_message("DOH!...Invalid Move. Computer's Turn", duration=ai_delay)

            elif event.type == pygame.KEYDOWN:
                board.sidebar.handle_keypress(event)
        
        
        if current_color == 'W' and not board.game_over:
            if last_move_time and (time.time() - last_move_time >= ai_delay):
                ai.calculate_best_move(board, 'W')
                ai.make_best_move(board, 'W')
                current_color = 'B'


        board.draw(win, current_color)
        pygame.display.flip()
        clock.tick(30)
