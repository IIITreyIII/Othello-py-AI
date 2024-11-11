# Trey Ball
# CSC 475 Assignment 3
# 11-11-2024
# Sidebar.py manages the sidebar and its UI on the right side of the gameboard. The Sidebar class
# initializes the buttons, displays scores across multiple games, and handles the debug mode options.
# Debug mode allows the player to enable smart moves (moves the computer makes for the player), update the search depth, and toggle alpha-beta pruning.
# Note: This code is hard to organize due to pygames event handling and button position, honestly this made me appreciate CSS and HTML so much more.


import pygame
from settings import WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, FONT, FONT_COLOR, BLACK, WHITE, HEIGHT, RED
from score_manager import read_scores, write_scores

class Sidebar:
    def __init__(self):
        self.debug_mode = False
        self.use_alpha_beta = False
        self.search_depth = 3
        self.depth_input_active = False 
        self.scores = read_scores()
        self.button_width = SIDEBAR_WIDTH - 40
        self.button_height = 40
        self.margin_top = 30
        self.spacing = 15


        x_pos = WIDTH - SIDEBAR_WIDTH + 20
        self.debug_button_rect = pygame.Rect(x_pos, HEADER_HEIGHT + self.margin_top, self.button_width, self.button_height)                                         # Debug mode button
        self.smart_move_button_rect = pygame.Rect(x_pos, self.debug_button_rect.bottom + self.spacing, self.button_width, self.button_height)                       # Smart move button (cpu move for player)       
        self.update_depth_button_rect = pygame.Rect(x_pos, self.smart_move_button_rect.bottom + self.spacing, self.button_width, self.button_height)                # Update depth to new val button
        self.alpha_beta_button_rect = pygame.Rect(x_pos, self.update_depth_button_rect.bottom + self.spacing, self.button_width, self.button_height)                # alpha-beta toggle button
        self.depth_text_input_rect = pygame.Rect(x_pos, self.alpha_beta_button_rect.bottom + self.spacing + 10, self.button_width, self.button_height)              # Depth input box
        self.new_game_button_rect = pygame.Rect(x_pos, HEIGHT - self.margin_top - self.button_height * 3 - self.spacing * 2, self.button_width, self.button_height) # New game button
        self.return_button_rect = pygame.Rect(x_pos, HEIGHT - self.margin_top - self.button_height * 2 - self.spacing, self.button_width, self.button_height)       # Main menu button
        self.reset_scores_button_rect = pygame.Rect(x_pos, HEIGHT - self.margin_top - self.button_height, self.button_width, self.button_height)                    # Reset scores button

    def draw(self, win, black_count, white_count, game_over):                                                                            # Draws the sidebar and its elements
        pygame.draw.rect(win, (50, 50, 50), (WIDTH - SIDEBAR_WIDTH, HEADER_HEIGHT, SIDEBAR_WIDTH, HEIGHT - HEADER_HEIGHT))               # equations are used to position elements in pygame (this took hours to position buttons :<)
        pygame.draw.circle(win, BLACK, (WIDTH - SIDEBAR_WIDTH - 120, HEADER_HEIGHT // 2), 15)
        black_count_text = FONT.render(str(black_count), True, FONT_COLOR)
        win.blit(black_count_text, (WIDTH - SIDEBAR_WIDTH - 100, HEADER_HEIGHT // 2 - black_count_text.get_height() // 2))

        pygame.draw.circle(win, WHITE, (WIDTH - SIDEBAR_WIDTH - 50, HEADER_HEIGHT // 2), 15)
        white_count_text = FONT.render(str(white_count), True, FONT_COLOR)
        win.blit(white_count_text, (WIDTH - SIDEBAR_WIDTH - 30, HEADER_HEIGHT // 2 - white_count_text.get_height() // 2))

        pygame.draw.rect(win, (200, 200, 200), self.debug_button_rect, border_radius=8)
        debug_text = FONT.render("Debug ON" if self.debug_mode else "Debug OFF", True, BLACK)
        win.blit(debug_text, (self.debug_button_rect.x + 15, self.debug_button_rect.y + 8))

        if self.debug_mode:
            pygame.draw.rect(win, (200, 200, 200), self.smart_move_button_rect, border_radius=8)
            smart_move_text = FONT.render("Smart Move", True, BLACK)
            win.blit(smart_move_text, (self.smart_move_button_rect.x + 15, self.smart_move_button_rect.y + 8))

            pygame.draw.rect(win, (200, 200, 200), self.update_depth_button_rect, border_radius=8)
            update_depth_text = FONT.render("Update Depth", True, BLACK)
            win.blit(update_depth_text, (self.update_depth_button_rect.x + 15, self.update_depth_button_rect.y + 8))

            pygame.draw.rect(win, (200, 200, 200), self.alpha_beta_button_rect, border_radius=8)
            alpha_beta_text = FONT.render("Alpha-Beta ON" if self.use_alpha_beta else "Alpha-Beta OFF", True, BLACK)
            win.blit(alpha_beta_text, (self.alpha_beta_button_rect.x + 8, self.alpha_beta_button_rect.y + 8))


            depth_label_text = FONT.render("Depth:", True, WHITE)
            win.blit(depth_label_text, (self.depth_text_input_rect.x, self.depth_text_input_rect.y - 30))
            pygame.draw.rect(win, (255, 255, 255), self.depth_text_input_rect, border_radius=8, width=2)
            depth_display_text = FONT.render(str(self.search_depth), True, RED if self.depth_input_active else WHITE)
            win.blit(depth_display_text, (self.depth_text_input_rect.x + 10, self.depth_text_input_rect.y + 8))

        
        scoreboard_title_y_pos = self.return_button_rect.y - 200
        scoreboard_title_text = FONT.render("Scoreboard", True, WHITE)
        win.blit(scoreboard_title_text, (self.return_button_rect.x + 10, scoreboard_title_y_pos))
        
        score_y_pos = self.return_button_rect.y - 160
        pygame.draw.rect(win, (50, 50, 50), (self.return_button_rect.x, score_y_pos, self.button_width, 40))

        p1_label = FONT.render(f"P1: {self.scores['P1']}", True, WHITE)
        win.blit(p1_label, (self.return_button_rect.x + 10, score_y_pos + 10))
        p2_label = FONT.render(f"P2: {self.scores['P2']}", True, WHITE)
        win.blit(p2_label, (self.return_button_rect.x + 100, score_y_pos + 10))


        if game_over:
            pygame.draw.rect(win, (200, 200, 200), self.new_game_button_rect, border_radius=8)
            new_game_text = FONT.render("New Game", True, BLACK)
            win.blit(new_game_text, (self.new_game_button_rect.x + 15, self.new_game_button_rect.y + 8))


        pygame.draw.rect(win, (200, 200, 200), self.return_button_rect, border_radius=8)
        return_text = FONT.render("Main Menu", True, BLACK)
        win.blit(return_text, (self.return_button_rect.x + 15, self.return_button_rect.y + 8))

        pygame.draw.rect(win, (200, 200, 200), self.reset_scores_button_rect, border_radius=8)
        reset_scores_text = FONT.render("Reset Scores", True, BLACK)
        win.blit(reset_scores_text, (self.reset_scores_button_rect.x + 15, self.reset_scores_button_rect.y + 8))


    def toggle_debug(self):
        self.debug_mode = not self.debug_mode

    def toggle_alpha_beta(self):
        self.use_alpha_beta = not self.use_alpha_beta

    def get_depth(self):
        return self.search_depth

    def reset_scores(self):                                    # Resets scores to 0, save to json
        self.scores = {'P1': 0, 'P2': 0}
        write_scores(self.scores)

    def update_scores(self, winner):                         # updates scores for winner
        if winner == 'B':
            self.scores['P1'] += 1
        elif winner == 'W':
            self.scores['P2'] += 1
        write_scores(self.scores)

    def handle_click(self, pos):
        if self.debug_button_rect.collidepoint(pos):
            self.toggle_debug()
            return "toggle_debug"
        elif self.debug_mode and self.smart_move_button_rect.collidepoint(pos):
            return "smart_move"
        elif self.debug_mode and self.update_depth_button_rect.collidepoint(pos):
            self.depth_input_active = True
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
            self.depth_input_active = False
            return None

    def handle_keypress(self, event):
        if self.depth_input_active and event.key in range(pygame.K_0, pygame.K_9 + 1):
            number = int(chr(event.key))
            self.search_depth = self.search_depth * 10 + number
        elif self.depth_input_active and event.key == pygame.K_BACKSPACE:
            self.search_depth = self.search_depth // 10
        elif self.depth_input_active and event.key == pygame.K_RETURN:
            self.depth_input_active = False
