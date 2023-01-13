import pygame
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60


# Load in images
def load_images(path):
    images = []
    # Loop through all files in the folder specified (relative)
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            images.append(pygame.image.load(path + filename).convert_alpha())
    return images


class BackgroundImages:
    def __init__(self, x, y, images, speeds):
        self.width = images[0].get_width()
        self.images = images
        self.speeds = speeds
        self.x = x
        self.y = y

    def draw(self, screen):
        for count, i in enumerate(self.images):
            self.x -= self.speeds[count]
            if self.x < -self.width:
                #difference = self.width + self.x
                self.x = self.width * 2
            screen.blit(i, (self.x, self.y))


# Implement parallax effect
class Background:
    def __init__(self, images, speeds):
        self.width = images[0].get_width()
        self.images = [BackgroundImages(i * self.width, 0, images,  speeds) for i in range(3)]

    def draw(self, screen):
        for count, i in enumerate(self.images):
            i.draw(screen)
