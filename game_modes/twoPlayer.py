import pygame
from board import Board
from settings import HEADER_HEIGHT, WIDTH, SIDEBAR_WIDTH
import sys

def run_game(win):
    board = Board()
    current_color = 'B'

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < WIDTH - SIDEBAR_WIDTH and pos[1] > HEADER_HEIGHT:
                    if board.handle_click(pos, current_color):
                        current_color = 'W' if current_color == 'B' else 'B'
        
        board.draw(win, current_color)
        pygame.display.flip()
        clock.tick(30)
