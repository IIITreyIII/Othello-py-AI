# sidebar.py

import pygame
from settings import WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, FONT, FONT_COLOR, BLACK, WHITE, HEIGHT

class Sidebar:
    def __init__(self):
        self.debug_mode = False
        self.debug_button_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH + 20, HEADER_HEIGHT + 20, 100, 30)
        self.smart_move_button_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH + 20, HEADER_HEIGHT + 70, 100, 30)
        self.search_depth = 3

    def draw(self, win, black_count, white_count):
        """Draw the sidebar including debug and smart move controls."""
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


        if self.debug_mode:

            pygame.draw.rect(win, WHITE, self.smart_move_button_rect)
            smart_move_text = FONT.render("Smart Move", True, BLACK)
            win.blit(smart_move_text, (self.smart_move_button_rect.x + 5, self.smart_move_button_rect.y + 5))


            depth_text = FONT.render(f"Depth: {self.search_depth}", True, FONT_COLOR)
            win.blit(depth_text, (self.smart_move_button_rect.x, self.smart_move_button_rect.y + 50))

    def toggle_debug(self):
        """Toggle debug mode on or off."""
        self.debug_mode = not self.debug_mode

    def handle_click(self, pos):
        """Handle clicks in the sidebar for toggling debug and activating smart move."""
        if self.debug_button_rect.collidepoint(pos):
            self.toggle_debug()
            print(f"Debug mode {'enabled' if self.debug_mode else 'disabled'}")
            return "toggle_debug"
        elif self.debug_mode and self.smart_move_button_rect.collidepoint(pos):
            print("Smart Move button pressed")
            return "smart_move"
        return None
