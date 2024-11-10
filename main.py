import pygame
import sys
from game_modes import twoPlayer, playerVsComputer
from settings import WIDTH, HEIGHT, FONT, FONT_COLOR, BLACK, WHITE
from score_manager import write_scores
from sidebar import Sidebar

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello Main Menu")

def main_menu():
    sidebar = Sidebar()
    while True:
        WIN.fill((200, 200, 200))
        title_text = FONT.render("Othello Game", True, FONT_COLOR)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        # Two Player button
        button_text = FONT.render("Player vs Player", True, BLACK)
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
        pygame.draw.rect(WIN, WHITE, button_rect)
        WIN.blit(button_text, (button_rect.x + 50, button_rect.y + 10))
        
        # Player vs Computer button
        ai_button_text = FONT.render("Player vs CPU", True, BLACK)
        ai_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
        pygame.draw.rect(WIN, WHITE, ai_button_rect)
        WIN.blit(ai_button_text, (ai_button_rect.x + 10, ai_button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    twoPlayer.run_game(WIN)
                    break  # Exit the event loop and redraw the main menu
                elif ai_button_rect.collidepoint(event.pos):
                    playerVsComputer.run_game(WIN)
                    break  # Exit the event loop and redraw the main menu
                elif sidebar.reset_scores_button_rect.collidepoint(event.pos):
                    sidebar.reset_scores()

if __name__ == "__main__":
    main_menu()
