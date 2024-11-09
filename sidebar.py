import pygame
from settings import WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, FONT, FONT_COLOR, BLACK, WHITE, HEIGHT

class Sidebar:
    def __init__(self):
        self.debug_mode = False
        self.debug_button_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH + 20, HEADER_HEIGHT + 20, 100, 30)

    def draw(self, win, black_count, white_count):
        pygame.draw.rect(win, (128, 0, 128), (WIDTH - SIDEBAR_WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT))


        pygame.draw.circle(win, BLACK, (WIDTH - SIDEBAR_WIDTH - 120, HEADER_HEIGHT // 2), 15)
        black_count_text = FONT.render(str(black_count), True, FONT_COLOR)
        win.blit(black_count_text, (WIDTH - SIDEBAR_WIDTH - 100, HEADER_HEIGHT // 2 - black_count_text.get_height() // 2))

        pygame.draw.circle(win, WHITE, (WIDTH - SIDEBAR_WIDTH - 50, HEADER_HEIGHT // 2), 15)
        white_count_text = FONT.render(str(white_count), True, FONT_COLOR)
        win.blit(white_count_text, (WIDTH - SIDEBAR_WIDTH - 30, HEADER_HEIGHT // 2 - white_count_text.get_height() // 2))


        pygame.draw.rect(win, WHITE, self.debug_button_rect)
        debug_text = FONT.render("Debug ON" if self.debug_mode else "Debug OFF", True, BLACK)
        win.blit(debug_text, (self.debug_button_rect.x + 5, self.debug_button_rect.y + 5))

    def toggle_debug(self):
        """Toggle debug mode on or off."""
        self.debug_mode = not self.debug_mode

    def handle_click(self, pos):
        """Handle clicks in the sidebar, checking for the debug button."""
        if self.debug_button_rect.collidepoint(pos):
            self.toggle_debug()
            print(f"Debug mode {'enabled' if self.debug_mode else 'disabled'}")
            return True
        return False
