import pygame
from settings import WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, FONT, FONT_COLOR, BLACK, WHITE, HEIGHT, RED
from score_manager import read_scores, write_scores

class Sidebar:
    def __init__(self):
        self.debug_mode = False
        self.use_alpha_beta = False  # Track alpha-beta toggle
        self.search_depth = 3
        self.depth_input_active = False  # Tracks if depth input mode is active
        self.scores = read_scores()  # Read scores from file

        # Define button sizes and positions with enhanced spacing and alignment
        self.button_width = SIDEBAR_WIDTH - 40
        self.button_height = 40
        self.margin_top = 30
        self.spacing = 15  # Increased spacing for better aesthetics

        # Button positions
        x_pos = WIDTH - SIDEBAR_WIDTH + 20
        self.debug_button_rect = pygame.Rect(x_pos, HEADER_HEIGHT + self.margin_top, self.button_width, self.button_height)
        self.smart_move_button_rect = pygame.Rect(x_pos, self.debug_button_rect.bottom + self.spacing, self.button_width, self.button_height)
        self.update_depth_button_rect = pygame.Rect(x_pos, self.smart_move_button_rect.bottom + self.spacing, self.button_width, self.button_height)
        self.alpha_beta_button_rect = pygame.Rect(x_pos, self.update_depth_button_rect.bottom + self.spacing, self.button_width, self.button_height)
        self.depth_text_input_rect = pygame.Rect(x_pos, self.alpha_beta_button_rect.bottom + self.spacing + 10, self.button_width, self.button_height)
        self.new_game_button_rect = pygame.Rect(x_pos, HEIGHT - self.margin_top - self.button_height * 3 - self.spacing * 2, self.button_width, self.button_height)
        self.return_button_rect = pygame.Rect(x_pos, HEIGHT - self.margin_top - self.button_height * 2 - self.spacing, self.button_width, self.button_height)
        self.reset_scores_button_rect = pygame.Rect(x_pos, HEIGHT - self.margin_top - self.button_height, self.button_width, self.button_height)

    def draw(self, win, black_count, white_count, game_over):
        """Draw the sidebar including debug, smart move, and depth controls."""
        pygame.draw.rect(win, (50, 50, 50), (WIDTH - SIDEBAR_WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT))  # Dark gray background

        # Display black and white piece counts with enhanced alignment
        pygame.draw.circle(win, BLACK, (WIDTH - SIDEBAR_WIDTH - 120, HEADER_HEIGHT // 2), 15)
        black_count_text = FONT.render(str(black_count), True, FONT_COLOR)
        win.blit(black_count_text, (WIDTH - SIDEBAR_WIDTH - 100, HEADER_HEIGHT // 2 - black_count_text.get_height() // 2))

        pygame.draw.circle(win, WHITE, (WIDTH - SIDEBAR_WIDTH - 50, HEADER_HEIGHT // 2), 15)
        white_count_text = FONT.render(str(white_count), True, FONT_COLOR)
        win.blit(white_count_text, (WIDTH - SIDEBAR_WIDTH - 30, HEADER_HEIGHT // 2 - white_count_text.get_height() // 2))

        # Draw debug mode toggle button
        pygame.draw.rect(win, (200, 200, 200), self.debug_button_rect, border_radius=8)
        debug_text = FONT.render("Debug ON" if self.debug_mode else "Debug OFF", True, BLACK)
        win.blit(debug_text, (self.debug_button_rect.x + 15, self.debug_button_rect.y + 8))

        # Draw smart move, alpha-beta toggle, and depth controls if debug mode is on
        if self.debug_mode:
            pygame.draw.rect(win, (200, 200, 200), self.smart_move_button_rect, border_radius=8)
            smart_move_text = FONT.render("Smart Move", True, BLACK)
            win.blit(smart_move_text, (self.smart_move_button_rect.x + 15, self.smart_move_button_rect.y + 8))

            pygame.draw.rect(win, (200, 200, 200), self.update_depth_button_rect, border_radius=8)
            update_depth_text = FONT.render("Update Depth", True, BLACK)
            win.blit(update_depth_text, (self.update_depth_button_rect.x + 15, self.update_depth_button_rect.y + 8))

            # Alpha-beta toggle button with rounded corners
            pygame.draw.rect(win, (200, 200, 200), self.alpha_beta_button_rect, border_radius=8)
            alpha_beta_text = FONT.render("Alpha-Beta ON" if self.use_alpha_beta else "Alpha-Beta OFF", True, BLACK)
            win.blit(alpha_beta_text, (self.alpha_beta_button_rect.x + 8, self.alpha_beta_button_rect.y + 8))

            # Display current depth with input box
            depth_label_text = FONT.render("Depth:", True, WHITE)  # White label for contrast
            win.blit(depth_label_text, (self.depth_text_input_rect.x, self.depth_text_input_rect.y - 30))
            pygame.draw.rect(win, (255, 255, 255), self.depth_text_input_rect, border_radius=8, width=2)
            depth_display_text = FONT.render(str(self.search_depth), True, RED if self.depth_input_active else WHITE)
            win.blit(depth_display_text, (self.depth_text_input_rect.x + 10, self.depth_text_input_rect.y + 8))

        # Draw scoreboard title
        scoreboard_title_y_pos = self.return_button_rect.y - 200  # Adjusted position to move the title higher
        scoreboard_title_text = FONT.render("Total Games Won", True, WHITE)
        win.blit(scoreboard_title_text, (self.return_button_rect.x + 10, scoreboard_title_y_pos))

        # Draw scoreboard for P1 and P2
        score_y_pos = self.return_button_rect.y - 160  # Adjusted position to move the score higher
        pygame.draw.rect(win, (50, 50, 50), (self.return_button_rect.x, score_y_pos, self.button_width, 40))  # Scoreboard background

        # Player 1 (Black) score
        p1_label = FONT.render(f"P1: {self.scores['P1']}", True, WHITE)
        win.blit(p1_label, (self.return_button_rect.x + 10, score_y_pos + 10))

        # Player 2 (White) score
        p2_label = FONT.render(f"P2: {self.scores['P2']}", True, WHITE)
        win.blit(p2_label, (self.return_button_rect.x + 100, score_y_pos + 10))

        # Draw new game button if the game is over
        if game_over:
            pygame.draw.rect(win, (200, 200, 200), self.new_game_button_rect, border_radius=8)
            new_game_text = FONT.render("New Game", True, BLACK)
            win.blit(new_game_text, (self.new_game_button_rect.x + 15, self.new_game_button_rect.y + 8))

        # Draw return to main menu button
        pygame.draw.rect(win, (200, 200, 200), self.return_button_rect, border_radius=8)
        return_text = FONT.render("Main Menu", True, BLACK)
        win.blit(return_text, (self.return_button_rect.x + 15, self.return_button_rect.y + 8))

        # Draw reset scores button
        pygame.draw.rect(win, (200, 200, 200), self.reset_scores_button_rect, border_radius=8)
        reset_scores_text = FONT.render("Reset Scores", True, BLACK)
        win.blit(reset_scores_text, (self.reset_scores_button_rect.x + 15, self.reset_scores_button_rect.y + 8))

    def toggle_debug(self):
        """Toggle debug mode on or off."""
        self.debug_mode = not self.debug_mode

    def toggle_alpha_beta(self):
        """Toggle alpha-beta pruning on or off."""
        self.use_alpha_beta = not self.use_alpha_beta

    def get_depth(self):
        return self.search_depth

    def reset_scores(self):
        """Reset scores to 0 and save to file."""
        self.scores = {'P1': 0, 'P2': 0}
        write_scores(self.scores)

    def update_scores(self, winner):
        """Update scores based on the winner and save to file."""
        if winner == 'B':
            self.scores['P1'] += 1
        elif winner == 'W':
            self.scores['P2'] += 1
        write_scores(self.scores)

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
        elif self.return_button_rect.collidepoint(pos):
            return "return_to_menu"
        elif self.new_game_button_rect.collidepoint(pos):
            return "new_game"
        elif self.reset_scores_button_rect.collidepoint(pos):
            self.reset_scores()
            return "reset_scores"
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
