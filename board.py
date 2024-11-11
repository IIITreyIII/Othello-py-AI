# Trey Ball
# Assignment 3
# 11-11-2024
# Board.py is responsible for managing the game board and pieces. It contains a Board class 
# which initializes the game board, places the initial pieces, and manages the game state. 
# The Board class also handles drawing the game board and pieces on the screen, checking for valid moves, making moves, flipping pieces, checking for a winner, and displaying messages.
# This was made so core game funcationalities could be shared accross different game modes. Two Player / player v comp

import pygame
import time
from settings import WIDTH, HEIGHT, HEADER_HEIGHT, SIDEBAR_WIDTH, SQUARE_SIZE, BLACK, WHITE, GREEN, GRAY, FONT_COLOR, FONT
from helpers import count_pieces
from sidebar import Sidebar

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.grid[3][3], self.grid[4][4] = 'W', 'W'
        self.grid[3][4], self.grid[4][3] = 'B', 'B'
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        self.message = ""
        self.message_start_time = None
        self.message_duration = 0
        self.game_over = False
        self.sidebar = Sidebar()
        self.heuristic_display = {}

    def display_message(self, message, duration=2):
        self.message = message
        self.message_duration = duration
        self.message_start_time = time.time()

    def draw(self, win, current_color):
        pygame.draw.rect(win, GRAY, (0, 0, WIDTH, HEADER_HEIGHT))  # HEADER
        if self.message and (time.time() - self.message_start_time < self.message_duration):
            text_surface = FONT.render(self.message, True, FONT_COLOR)
            win.blit(text_surface, ((WIDTH - SIDEBAR_WIDTH) // 2 - text_surface.get_width() // 2, HEADER_HEIGHT // 2 - text_surface.get_height() // 2))
        else:
            self.message = ""

        if self.game_over:
            turn_text = "Game Over"
        else:
            turn_text = "Player 1's Turn" if current_color == 'B' else "Player 2's Turn"

        turn_surface = FONT.render(turn_text, True, FONT_COLOR)
        win.blit(turn_surface, (10, HEADER_HEIGHT // 2 - turn_surface.get_height() // 2))

        
        if not self.game_over:
            piece_color = BLACK if current_color == 'B' else WHITE
            pygame.draw.circle(win, piece_color, (165, HEADER_HEIGHT // 2), 15)

        black_count, white_count = count_pieces(self.grid)
        self.sidebar.draw(win, black_count, white_count, self.game_over) # draws (pygame draw) sidebar


        win.fill(GREEN, (0, HEADER_HEIGHT, WIDTH - SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT)) # Board background
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE + HEADER_HEIGHT, SQUARE_SIZE, SQUARE_SIZE), 1)
                
                if self.grid[row][col] == 'B':
                    pygame.draw.circle(win, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + HEADER_HEIGHT), SQUARE_SIZE // 2 - 5)
                elif self.grid[row][col] == 'W':
                    pygame.draw.circle(win, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + HEADER_HEIGHT), SQUARE_SIZE // 2 - 5)
                

                if self.sidebar.debug_mode and (row, col) in self.heuristic_display: # display the heuristic values in the grid squares
                    heuristic_value = self.heuristic_display[(row, col)]
                    heuristic_surface = FONT.render(str(heuristic_value), True, FONT_COLOR)
                    win.blit(heuristic_surface, (col * SQUARE_SIZE + SQUARE_SIZE // 2 - heuristic_surface.get_width() // 2,
                                                 row * SQUARE_SIZE + HEADER_HEIGHT + SQUARE_SIZE // 2 - heuristic_surface.get_height() // 2))


        if self.game_over:          # when game over - shows a new game button to restart the game
            pygame.draw.rect(win, (200, 200, 200), self.sidebar.new_game_button_rect, border_radius=8)
            new_game_text = FONT.render("New Game", True, BLACK)
            win.blit(new_game_text, (self.sidebar.new_game_button_rect.x + 15, self.sidebar.new_game_button_rect.y + 8))

        pygame.draw.rect(win, (200, 200, 200), self.sidebar.return_button_rect, border_radius=8)
        return_text = FONT.render("Main Menu", True, BLACK)
        win.blit(return_text, (self.sidebar.return_button_rect.x + 15, self.sidebar.return_button_rect.y + 8))



    def update_heuristics(self, heuristics):
        self.heuristic_display = heuristics


    def is_valid_move(self, row, col, color):
        if self.grid[row][col] is not None:
            return False
        for dx, dy in self.directions:
            if self.check_direction(row, col, dx, dy, color):
                return True
        return False
    
    def check_direction(self, row, col, dx, dy, color):     # check if the direction is a valid move
        opponent = 'W' if color == 'B' else 'B'
        r, c = row + dx, col + dy
        found_opponent = False
        while 0 <= r < 8 and 0 <= c < 8 and self.grid[r][c] == opponent:
            found_opponent = True
            r += dx
            c += dy
        if found_opponent and 0 <= r < 8 and 0 <= c < 8 and self.grid[r][c] == color:
            return True
        return False

    def make_move(self, row, col, color):
        if self.game_over or not self.is_valid_move(row, col, color):
            self.display_message("Invalid Move... Turn Skipped!", 2)
            return False

        self.grid[row][col] = color
        for dx, dy in self.directions:
            if self.check_direction(row, col, dx, dy, color):
                self.flip_pieces(row, col, dx, dy, color)

        self.check_winner()
        return True

    def flip_pieces(self, row, col, dx, dy, color):         # flip the pieces in the direction
        opponent = 'W' if color == 'B' else 'B'
        r, c = row + dx, col + dy
        while 0 <= r < 8 and 0 <= c < 8 and self.grid[r][c] == opponent:
            self.grid[r][c] = color
            r += dx
            c += dy

    def has_valid_moves(self, color):
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, color):
                    return True
        return False

    def handle_click(self, pos, color):                 # stops sidebar clicks from messing with game board
        if pos[0] >= WIDTH - SIDEBAR_WIDTH:
            if self.sidebar.handle_click(pos):
                return False

        if pos[1] < HEADER_HEIGHT or self.game_over:
            return False

        row, col = (pos[1] - HEADER_HEIGHT) // SQUARE_SIZE, pos[0] // SQUARE_SIZE
        if self.make_move(row, col, color):
            return True
        return False

    def check_winner(self):                            # check if players have valid moves left, not == game over
        if not self.has_valid_moves('B') and not self.has_valid_moves('W'):
            black_count, white_count = count_pieces(self.grid)
            if black_count > white_count:
                self.display_message("Player 1 (Black) wins!", 5)
                self.sidebar.update_scores('B')
            elif white_count > black_count:
                self.display_message("Player 2 (White) wins!", 5)
                self.sidebar.update_scores('W')
            else:
                self.display_message("It's a tie!", 5)
            self.game_over = True

def copy_board(original_board):                        # copy the board to simulate possible moves
    new_board = Board()
    new_board.grid = [row[:] for row in original_board.grid]
    new_board.game_over = original_board.game_over
    new_board.message = original_board.message
    new_board.message_start_time = original_board.message_start_time
    new_board.message_duration = original_board.message_duration
    return new_board
