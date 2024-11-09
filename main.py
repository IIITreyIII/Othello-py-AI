import pygame
import sys
from game_modes import twoPlayer
from settings import WIDTH, HEIGHT, FONT, FONT_COLOR, BLACK, WHITE

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello Main Menu")

def main_menu():
    WIN.fill((200, 200, 200))
    title_text = FONT.render("Othello Game", True, FONT_COLOR)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    button_text = FONT.render("Two Player", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(WIN, WHITE, button_rect)
    WIN.blit(button_text, (button_rect.x + 50, button_rect.y + 10))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    twoPlayer.run_game(WIN)

if __name__ == "__main__":
    main_menu()
