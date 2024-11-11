# Trey Ball
# Assignment 3
# 11-11-2024
# settings.py contains global variables and constants used throughout the game. This includes colors, fonts, and window dimensions.
# Somewhat cleans up pygames events and button handeling by storing constants in one place.


import pygame

WIDTH, HEIGHT = 1000, 850
HEADER_HEIGHT = 50
SIDEBAR_WIDTH = 200
SQUARE_SIZE = (WIDTH - SIDEBAR_WIDTH) // 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
GRAY = (200, 200, 200)
FONT_COLOR = (50, 50, 50)
RED = (255, 0, 0)

pygame.init()
FONT = pygame.font.SysFont("Arial", 24)
