
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

    def display_message(self, message, duration=2):
        self.message = message
        self.message_duration = duration
        self.message_start_time = time.time()

    def draw(self, win, current_color):
        pygame.draw.rect(win, GRAY, (0, 0, WIDTH, HEADER_HEIGHT))   # HEADER 
        
        if self.game_over:
            turn_text = "Game Over"
        else:
            turn_text = "Player 1's Turn" if current_color == 'B' else "Player 2's Turn"
        
        text_surface = FONT.render(turn_text, True, FONT_COLOR)
        win.blit(text_surface, (10, HEADER_HEIGHT // 2 - text_surface.get_height() // 2))

        if not self.game_over:
            piece_color = BLACK if current_color == 'B' else WHITE
            pygame.draw.circle(win, piece_color, (165, HEADER_HEIGHT // 2), 15)

        # Count pieces
        black_count, white_count = count_pieces(self.grid)
        
        # Draw the sidebar with piece counts and debug toggle
        self.sidebar.draw(win, black_count, white_count)

        # Draw the board and pieces
        win.fill(GREEN, (0, HEADER_HEIGHT, WIDTH - SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT))
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE + HEADER_HEIGHT, SQUARE_SIZE, SQUARE_SIZE), 1)
                if self.grid[row][col] == 'B':
                    pygame.draw.circle(win, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + HEADER_HEIGHT), SQUARE_SIZE // 2 - 5)
                elif self.grid[row][col] == 'W':
                    pygame.draw.circle(win, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + HEADER_HEIGHT), SQUARE_SIZE // 2 - 5)

    def is_valid_move(self, row, col, color):
        """Check if placing a piece at (row, col) is valid for the given color."""
        if self.grid[row][col] is not None:
            return False
        for dx, dy in self.directions:
            if self.check_direction(row, col, dx, dy, color):
                return True
        return False

    def check_direction(self, row, col, dx, dy, color):
        """Check in a specific direction if a move would capture opponent's pieces."""
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
            self.display_message("Invalid Move! Skipping Turn!", 2)
            return False

        self.grid[row][col] = color
        for dx, dy in self.directions:
            if self.check_direction(row, col, dx, dy, color):
                self.flip_pieces(row, col, dx, dy, color)

        self.check_winner()
        return True

    def flip_pieces(self, row, col, dx, dy, color):
        """Flip opponent's pieces in a specific direction after a valid move."""
        opponent = 'W' if color == 'B' else 'B'
        r, c = row + dx, col + dy
        while 0 <= r < 8 and 0 <= c < 8 and self.grid[r][c] == opponent:
            self.grid[r][c] = color
            r += dx
            c += dy

    def has_valid_moves(self, color):
        """Check if there are any valid moves left for the given color."""
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, color):
                    return True
        return False

    def handle_click(self, pos, color):
        """Handle clicks on the board or in the sidebar."""
        if pos[0] >= WIDTH - SIDEBAR_WIDTH:

            if self.sidebar.handle_click(pos):
                return False

        if pos[1] < HEADER_HEIGHT or self.game_over:
            return False

        row, col = (pos[1] - HEADER_HEIGHT) // SQUARE_SIZE, pos[0] // SQUARE_SIZE
        if self.make_move(row, col, color):
            return True
        return False

    def check_winner(self):
        """Determine if the game is over and declare the winner."""
        if not self.has_valid_moves('B') and not self.has_valid_moves('W'):
            black_count, white_count = count_pieces(self.grid)
            if black_count > white_count:
                self.display_message("Player 1 (Black) wins!", 5)
            elif white_count > black_count:
                self.display_message("Player 2 (White) wins!", 5)
            else:
                self.display_message("It's a tie!", 5)
            self.game_over = True
