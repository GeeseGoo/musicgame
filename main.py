# Charles Huang 1/12/2023
# Ms. Townshend
# ICS4U0
# Muse dash style rhythm game with fish
import pygame
from lib import *
from dancetillyourdead import *
import itertools


# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Set up scrolling background
background = load_images("assets/background/2_game_background/layers/")
background = [image.convert_alpha() for image in background]
width = background[0].get_width()

# Spatula animations
spatula_idle = load_images("assets/spatula/")
spatula_idle = [pygame.transform.scale(image.convert_alpha(), (500, 540)) for image in spatula_idle]
spatula_idle = itertools.cycle(spatula_idle)

spatula = Spatula(100, 450)

# Beat map setup
beatmarker_img = pygame.transform.scale(load_images("assets/beats/")[0].convert_alpha(), (240, 220))
beatmarker_upper = Beatmarker(beatmarker_img.get_rect(x=500, y=150))
beatmarker_lower = Beatmarker(beatmarker_img.get_rect(x=500, y=550), -1)

# Load fishiesieshiesh
fish_orange = pygame.transform.scale(load_images("assets/beats/")[1].convert_alpha(), (200, 200))
fish_blue = pygame.transform.scale(load_images("assets/beats/")[2].convert_alpha(), (200, 200))

# init variables
background_obj = Background(background, [5, 4, 5, 6, 7, 9])  # Speeds of each layer
beats = []
score = 0
bpm = 154 * 4
beat_time = round(60000 / bpm)
beat_map = BeatMap(song, fish_orange, fish_blue)

pygame.time.set_timer(pygame.USEREVENT, beat_time)  # Calls an event every x milliseconds

# Game loop
running = True
while running:
    beat_clock = None
    beat_hit = None
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:   # Check for window close
            running = False
        if event.type == pygame.USEREVENT:  # Check for beat
            beat_clock = True
        if event.type == pygame.KEYDOWN:    # Check for key press
            if event.key == pygame.K_d:
                for i in beat_map.beats_onscreen_upper:
                    if i:
                        score += i.check(beatmarker_upper)
            if event.key == pygame.K_k:
                for i in beat_map.beats_onscreen_lower:
                    if i:
                        score += i.check(beatmarker_lower)

    background_obj.draw(screen)
    spatula.idle(screen, spatula_idle)
    beatmarker_upper.draw(screen, beatmarker_img)
    beatmarker_lower.draw(screen, beatmarker_img)
    draw_score(screen, score, pygame.font.Font("assets/fonts/Frutiger_bold.ttf", 100), (255, 255, 255))
    beat_map.next_beat(screen, beat_clock)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()


