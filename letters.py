# Create and draw the individual letters using this class
import pygame

class Letter:
    def __init__(self, xmas_mayhem_game):
        self.image = None
        self.name = ""
        self.screen = xmas_mayhem_game.screen
        self.x = 0.0
        self.y = 0.0
        self.alreadyScaled = False

    def draw(self, rect = (0, 0), scale = 2):
        if (not self.alreadyScaled):
            self.rect = self.image.get_rect()
            x_scale = self.rect.width * scale
            y_scale = self.rect.height * scale
            self.image = pygame.transform.scale(self.image, (x_scale, y_scale))

            self.alreadyScaled = True

        self.screen.blit(self.image, rect)

    def getName(self):
        return self.name