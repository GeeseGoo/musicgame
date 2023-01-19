import pygame
from pygame import mixer
import os
import math

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
speed = 20
offset = 1420 / ((speed * 60) / 1000)

perfect_score = 10
good_score = 5

mixer.init()


# Load in images
def load_images(path):
    images = []
    # Loop through all files in the folder specified (relative)
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            images.append(pygame.image.load(path + filename).convert_alpha())
    return images

# Display score on screen
def draw_score(screen, score, font, colour):
    score_text = font.render(str(score), True, colour)
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))


# Class to store data for each image
class BackgroundImages:
    def __init__(self, x, y, images, speed):
        self.width = images.get_width()
        self.images = images
        self.speed = speed
        self.x = x
        self.y = y

    def draw(self, screen, speed):  # Draw the background images
        self.x -= speed
        if self.x <= -self.width:
            self.x = self.width * 2
        screen.blit(self.images, (self.x, self.y))


# Implement parallax effect
class Background:
    def __init__(self, images, speeds):
        self.width = images[0].get_width()
        self.speeds = speeds
        self.images = []
        for count, i in enumerate(images):
            self.images.append([BackgroundImages(j * SCREEN_WIDTH, 0, i, self.speeds[count]) for j in range(3)])

    def draw(self, screen):
        for count, i in enumerate(self.images):
            for j in i:
                j.draw(screen, self.speeds[count])


# Spatula animation
class Spatula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_frame = None
        self.prev_time = pygame.time.get_ticks()

    def idle(self, screen, images):
        if pygame.time.get_ticks() > self.prev_time + 10:
            self.current_frame = next(images)
            self.prev_time = pygame.time.get_ticks()
        if self.current_frame:
            screen.blit(self.current_frame, (self.x, self.y))


# Class for the marker that indicates when to hit the beat
class Beatmarker:
    def __init__(self, rect, rev=1):
        self.rect = rect
        self.rev = rev

    def draw(self, screen, circle):
        circle2 = pygame.transform.rotate(circle, pygame.time.get_ticks() / 7 * self.rev)
        rect = circle2.get_rect(center=self.rect.center)
        screen.blit(circle2, rect)


# Class to manage individual beats
class Beat:
    def __init__(self, rect, speed, yaccel, img):
        self.rect = rect
        self.speed = speed
        self.yvel = 0
        self.yaccel = yaccel
        self.hit = False
        self.img = img

    def draw(self, screen):
        img = self.img
        # Don't keep track of beats after they are off the screen
        if self.rect.right <= 0 or self.rect.bottom <= 0:
            return False

        # Change beat position
        self.rect.x -= self.speed
        if self.yvel > 0:
            self.yvel -= self.yaccel
        self.rect.y -= self.yvel

        # Spinning animation
        if self.hit:
            rect = self.rect
            img = pygame.transform.rotate(self.img, pygame.time.get_ticks())
            img.get_rect(x=rect.x, y=rect.y)

        screen.blit(img, self.rect)
        return True

    # Check if the beat has been hit
    def check(self, beatmarker):
        if abs(self.rect.center[0] - beatmarker.rect.center[0]) < 25 and self.rect.y == beatmarker.rect.y:
            self.yvel = 35
            self.hit = True
            return perfect_score
        if abs(self.rect.center[0] - beatmarker.rect.center[0]) < 65 and self.rect.y == beatmarker.rect.y:
            self.yvel = 25
            self.hit = True
            return good_score
        return 0


# Object for storing the beats
class BeatMap():
    def __init__(self, beats, image1, image2):
        self.beats_upper = [Beat(image1.get_rect(x=1920, y=150), speed, 2, image1) if i else None for i in beats[0]]
        self.beats_lower = [Beat(image2.get_rect(x=1920, y=550), speed, 2, image2) if i else None for i in beats[1]]
        self.beats_lower.reverse()
        self.beats_upper.reverse()
        self.beats_onscreen_upper = []
        self.beats_onscreen_lower = []
        self.time = pygame.time.get_ticks()


    def next_beat(self, screen, beat_clock):
        if self.time and pygame.time.get_ticks() > self.time + 1420 / 1.2 + 150:    # offset the playing of the song so that beats hit at the right time
            mixer.music.load("assets/music/Dance till You're Dead (FULL REMIX) [Bass Boosted].mp3")
            mixer.music.set_volume(0.5)
            mixer.music.play()
            self.time = None

        # Add the next beat to the screen
        if beat_clock and len(self.beats_upper) > 0 and len(self.beats_lower) > 0:
            self.beats_onscreen_upper.append(self.beats_upper.pop())
            self.beats_onscreen_lower.append(self.beats_lower.pop())

        # Display all beats
        for i in self.beats_onscreen_upper:
            if i:
                i.draw(screen)
        for i in self.beats_onscreen_lower:
            if i:
                i.draw(screen)
