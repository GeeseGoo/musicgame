# Charles Huang 1/12/2023
# Ms. Townshend
# ICS4U0
# Muse dash style rhythm game with fish
scroll = 0
import pygame
from lib import *


# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Set up scrolling background
background = load_images("assets/background/2_game_background/layers/")
background = [image.convert_alpha() for image in background]
width = background[0].get_width()

amoungs = Background(background, [2 for i in range(6)])

# Game loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    amoungs.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

