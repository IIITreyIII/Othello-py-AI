import pygame
import time
from settings import WIDTH, HEIGHT, HEADER_HEIGHT, SIDEBAR_WIDTH, SQUARE_SIZE, BLACK, WHITE, GREEN, GRAY, FONT_COLOR, FONT
from helpers import count_pieces

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.grid[3][3], self.grid[4][4] = 'W', 'W'
        self.grid[3][4], self.grid[4][3] = 'B', 'B'
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        self.message = ""
        self.message_start_time = None
        self.message_duration = 0

    def display_message(self, message, duration=2):
        self.message = message
        self.message_duration = duration
        self.message_start_time = time.time()

    def draw(self, win, current_color):
        # Draw the header
        pygame.draw.rect(win, GRAY, (0, 0, WIDTH, HEADER_HEIGHT))
        
        # Draw turn text on the left side
        turn_text = "Player 1's Turn" if current_color == 'B' else "Player 2's Turn"
        text_surface = FONT.render(turn_text, True, FONT_COLOR)
        win.blit(text_surface, (10, HEADER_HEIGHT // 2 - text_surface.get_height() // 2))

        # Draw player color indicator next to the turn text
        piece_color = BLACK if current_color == 'B' else WHITE
        pygame.draw.circle(win, piece_color, (165, HEADER_HEIGHT // 2), 15)

        # Count pieces on the board and draw on the right side of header
        black_count, white_count = count_pieces(self.grid)
        pygame.draw.circle(win, BLACK, (WIDTH - SIDEBAR_WIDTH - 100, HEADER_HEIGHT // 2), 15)
        black_count_text = FONT.render(str(black_count), True, FONT_COLOR)
        win.blit(black_count_text, (WIDTH - SIDEBAR_WIDTH - 80, HEADER_HEIGHT // 2 - black_count_text.get_height() // 2))

        pygame.draw.circle(win, WHITE, (WIDTH - SIDEBAR_WIDTH - 50, HEADER_HEIGHT // 2), 15)
        white_count_text = FONT.render(str(white_count), True, FONT_COLOR)
        win.blit(white_count_text, (WIDTH - SIDEBAR_WIDTH - 30, HEADER_HEIGHT // 2 - white_count_text.get_height() // 2))

        # Display message in the center of the header if within duration
        if self.message and (time.time() - self.message_start_time < self.message_duration):
            message_surface = FONT.render(self.message, True, FONT_COLOR)
            win.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEADER_HEIGHT // 2 - message_surface.get_height() // 2))
        else:
            self.message = ""  # Clear message if time has expired

        # Draw the game board area
        win.fill(GREEN, (0, HEADER_HEIGHT, WIDTH - SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT))
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE + HEADER_HEIGHT, SQUARE_SIZE, SQUARE_SIZE), 1)
                if self.grid[row][col] == 'B':
                    pygame.draw.circle(win, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + HEADER_HEIGHT), SQUARE_SIZE // 2 - 5)
                elif self.grid[row][col] == 'W':
                    pygame.draw.circle(win, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 + HEADER_HEIGHT), SQUARE_SIZE // 2 - 5)

        # Draw the sidebar
        pygame.draw.rect(win, (128, 0, 128), (WIDTH - SIDEBAR_WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT))

    def is_valid_move(self, row, col, color):
        if self.grid[row][col] is not None:
            return False
        for dx, dy in self.directions:
            if self.check_direction(row, col, dx, dy, color):
                return True
        return False

    def check_direction(self, row, col, dx, dy, color):
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
        if not self.is_valid_move(row, col, color):
            self.display_message("Invalid Move! Skipping Turn!", 2)
            return False
        self.grid[row][col] = color
        for dx, dy in self.directions:
            if self.check_direction(row, col, dx, dy, color):
                self.flip_pieces(row, col, dx, dy, color)
        return True

    def flip_pieces(self, row, col, dx, dy, color):
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

    def handle_click(self, pos, color):
        print(f"Click position: {pos}")
        if pos[0] >= WIDTH - SIDEBAR_WIDTH or pos[1] < HEADER_HEIGHT:
            print("Click ignored: Sidebar or header area")
            return False

        row, col = (pos[1] - HEADER_HEIGHT) // SQUARE_SIZE, pos[0] // SQUARE_SIZE


        if self.make_move(row, col, color):
            self.check_winner()
            return True
        return False

    def check_winner(self):
        black_count, white_count = count_pieces(self.grid)
        if black_count > white_count:
            self.display_message("Player 1 (Black) wins!", 5)
        elif white_count > black_count:
            self.display_message("Player 2 (White) wins!", 5)
        else:
            self.display_message("It's a tie!", 5)
