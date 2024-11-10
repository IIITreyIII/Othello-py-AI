import pygame
from settings import WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, FONT, FONT_COLOR, BLACK, WHITE, HEIGHT

class Sidebar:
    def __init__(self):
        self.debug_mode = False
        self.use_alpha_beta = False  # Track alpha-beta toggle
        self.debug_button_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH + 20, HEADER_HEIGHT + 20, 100, 30)
        self.smart_move_button_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH + 20, HEADER_HEIGHT + 70, 100, 30)
        self.update_depth_button_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH + 20, HEADER_HEIGHT + 120, 100, 30)
        self.alpha_beta_button_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH + 20, HEADER_HEIGHT + 160, 100, 30)
        self.search_depth = 3
        self.depth_input_active = False  # Tracks if depth input mode is active
        self.depth_text_input_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH + 20, HEADER_HEIGHT + 200, 100, 30)

    def draw(self, win, black_count, white_count):
        """Draw the sidebar including debug, smart move, and depth controls."""
        pygame.draw.rect(win, (128, 0, 128), (WIDTH - SIDEBAR_WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT))

        # Display black and white piece counts
        pygame.draw.circle(win, BLACK, (WIDTH - SIDEBAR_WIDTH - 120, HEADER_HEIGHT // 2), 15)
        black_count_text = FONT.render(str(black_count), True, FONT_COLOR)
        win.blit(black_count_text, (WIDTH - SIDEBAR_WIDTH - 100, HEADER_HEIGHT // 2 - black_count_text.get_height() // 2))

        pygame.draw.circle(win, WHITE, (WIDTH - SIDEBAR_WIDTH - 50, HEADER_HEIGHT // 2), 15)
        white_count_text = FONT.render(str(white_count), True, FONT_COLOR)
        win.blit(white_count_text, (WIDTH - SIDEBAR_WIDTH - 30, HEADER_HEIGHT // 2 - white_count_text.get_height() // 2))

        # Draw debug mode toggle button
        pygame.draw.rect(win, WHITE, self.debug_button_rect)
        debug_text = FONT.render("Debug ON" if self.debug_mode else "Debug OFF", True, BLACK)
        win.blit(debug_text, (self.debug_button_rect.x + 5, self.debug_button_rect.y + 5))

        # Draw smart move, alpha-beta toggle, and depth controls if debug mode is on
        if self.debug_mode:
            pygame.draw.rect(win, WHITE, self.smart_move_button_rect)
            smart_move_text = FONT.render("Smart Move", True, BLACK)
            win.blit(smart_move_text, (self.smart_move_button_rect.x + 5, self.smart_move_button_rect.y + 5))

            pygame.draw.rect(win, WHITE, self.update_depth_button_rect)
            update_depth_text = FONT.render("Update Depth", True, BLACK)
            win.blit(update_depth_text, (self.update_depth_button_rect.x + 5, self.update_depth_button_rect.y + 5))

            # Alpha-beta toggle button
            pygame.draw.rect(win, WHITE, self.alpha_beta_button_rect)
            alpha_beta_text = FONT.render("Alpha-Beta ON" if self.use_alpha_beta else "Alpha-Beta OFF", True, BLACK)
            win.blit(alpha_beta_text, (self.alpha_beta_button_rect.x + 5, self.alpha_beta_button_rect.y + 5))

            # Display current depth and allow input if active
            depth_text = FONT.render(f"Depth: {self.search_depth}", True, FONT_COLOR)
            win.blit(depth_text, (self.update_depth_button_rect.x, self.update_depth_button_rect.y + 50))

            pygame.draw.rect(win, WHITE, self.depth_text_input_rect, 2)
            if self.depth_input_active:
                input_text = FONT.render(str(self.search_depth), True, BLACK)
                win.blit(input_text, (self.depth_text_input_rect.x + 5, self.depth_text_input_rect.y + 5))
            else:
                static_text = FONT.render(str(self.search_depth), True, FONT_COLOR)
                win.blit(static_text, (self.depth_text_input_rect.x + 5, self.depth_text_input_rect.y + 5))

    def toggle_debug(self):
        """Toggle debug mode on or off."""
        self.debug_mode = not self.debug_mode

    def toggle_alpha_beta(self):
        """Toggle alpha-beta pruning on or off."""
        self.use_alpha_beta = not self.use_alpha_beta

    def get_depth(self):
        return self.search_depth

    def handle_click(self, pos):
        """Handle clicks in the sidebar for toggling debug, activating smart move, and alpha-beta pruning."""
        if self.debug_button_rect.collidepoint(pos):
            self.toggle_debug()
            return "toggle_debug"
        elif self.debug_mode and self.smart_move_button_rect.collidepoint(pos):
            return "smart_move"
        elif self.debug_mode and self.update_depth_button_rect.collidepoint(pos):
            self.depth_input_active = True  # Activate depth input mode
            return "update_depth"
        elif self.debug_mode and self.alpha_beta_button_rect.collidepoint(pos):
            self.toggle_alpha_beta()
            return "toggle_alpha_beta"
        elif self.depth_text_input_rect.collidepoint(pos):
            self.depth_input_active = True
            return None
        else:
            # If clicking outside input area, deactivate input
            self.depth_input_active = False
            return None

    def handle_key_event(self, event):
        """Handle key events to capture depth input when active."""
        if self.depth_input_active and event.key in range(pygame.K_0, pygame.K_9 + 1):  # Numbers 0-9
            number = int(chr(event.key))
            self.search_depth = self.search_depth * 10 + number  # Append digit
        elif self.depth_input_active and event.key == pygame.K_BACKSPACE:
            # Remove the last digit
            self.search_depth = self.search_depth // 10
        elif self.depth_input_active and event.key == pygame.K_RETURN:
            # Confirm depth input with Enter key
            self.depth_input_active = False
