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
        """Set a message to be displayed in the header for a specific duration."""
        self.message = message
        self.message_duration = duration
        self.message_start_time = time.time()

    def draw(self, win, current_color):
        pygame.draw.rect(win, GRAY, (0, 0, WIDTH, HEADER_HEIGHT))  # HEADER

        # Display the message if it's still within the duration
        if self.message and (time.time() - self.message_start_time < self.message_duration):
            text_surface = FONT.render(self.message, True, FONT_COLOR)
            win.blit(text_surface, ((WIDTH - SIDEBAR_WIDTH) // 2 - text_surface.get_width() // 2, HEADER_HEIGHT // 2 - text_surface.get_height() // 2))
        else:
            # Clear the message if the duration has passed
            self.message = ""

        # Display current player's turn or game over
        if self.game_over:
            turn_text = "Game Over"
        else:
            turn_text = "Player 1's Turn" if current_color == 'B' else "Player 2's Turn"

        turn_surface = FONT.render(turn_text, True, FONT_COLOR)
        win.blit(turn_surface, (10, HEADER_HEIGHT // 2 - turn_surface.get_height() // 2))

        # Current player piece color indicator
        if not self.game_over:
            piece_color = BLACK if current_color == 'B' else WHITE
            pygame.draw.circle(win, piece_color, (165, HEADER_HEIGHT // 2), 15)

        black_count, white_count = count_pieces(self.grid)
        self.sidebar.draw(win, black_count, white_count)

        # Draw board grid and pieces
        win.fill(GREEN, (0, HEADER_HEIGHT, WIDTH - SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT))
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE + HEADER_HEIGHT, SQUARE_SIZE, SQUARE_SIZE), 1)
                
                # Draw pieces
                if self.grid[row][col] == 'B':
                    pygame.draw.circle(win, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + HEADER_HEIGHT), SQUARE_SIZE // 2 - 5)
                elif self.grid[row][col] == 'W':
                    pygame.draw.circle(win, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + HEADER_HEIGHT), SQUARE_SIZE // 2 - 5)
                
                # Draw heuristic values in empty cells if debug mode is on
                if self.sidebar.debug_mode and (row, col) in self.heuristic_display:
                    heuristic_value = self.heuristic_display[(row, col)]
                    heuristic_surface = FONT.render(str(heuristic_value), True, FONT_COLOR)
                    win.blit(heuristic_surface, (col * SQUARE_SIZE + SQUARE_SIZE // 2 - heuristic_surface.get_width() // 2,
                                                 row * SQUARE_SIZE + HEADER_HEIGHT + SQUARE_SIZE // 2 - heuristic_surface.get_height() // 2))

    def update_heuristics(self, heuristics):
        """Update the board with heuristic values to display."""
        self.heuristic_display = heuristics

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
                return False  # Ignore if sidebar button was clicked

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

def copy_board(original_board):
    """Creates a deep copy of the given board."""
    new_board = Board()  # Create a new Board instance
    new_board.grid = [row[:] for row in original_board.grid]  # Deep copy of the grid
    new_board.game_over = original_board.game_over
    new_board.message = original_board.message
    new_board.message_start_time = original_board.message_start_time
    new_board.message_duration = original_board.message_duration
    return new_board
