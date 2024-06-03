# Sleigh "power" :)

import pygame, random

class MagicDust:
    def __init__(self, settings, screen, playerPos, playerHeight, playerWidth):
        self.screen = screen
        self.settings = settings
        self.dustArray = []
        self.density = 12 * self.settings.res_scale
        self.playerHeight = playerHeight
        self.playerWidth = playerWidth

        for i in range(self.density):
            speed = random.randint(2, 4) * self.settings.res_scale
            size = random.randint(1, 2)
            xPos = random.randint(playerPos[0], int(playerPos[0] + (self.playerWidth * 0.8)))
            self.dustArray.append([xPos, playerPos[1] + self.playerHeight + random.randint(-5 * self.settings.res_scale, 20 * self.settings.res_scale), speed, size])

    def update(self, playerPos):
        for i in range(len(self.dustArray)):
            self.dustArray[i][0] -= self.dustArray[i][2]

            # Reset particle if out of view
            if (self.dustArray[i][0] <= -10):
                speed = random.randint(5, 10)
                size = random.randint(1, 4)
                xPos = random.randint(playerPos[0], playerPos[0] + (int(self.playerWidth * 0.8)))
                self.dustArray[i][0] = xPos
                self.dustArray[i][1] = playerPos[1] + self.playerHeight + random.randint(-5 * self.settings.res_scale, 20 * self.settings.res_scale)
                self.dustArray[i][2] = speed
                self.dustArray[i][3] = size

    def draw(self):
        for i in range(len(self.dustArray)):
            pygame.draw.circle(self.screen, self.settings.yellow, [self.dustArray[i][0], self.dustArray[i][1]], self.dustArray[i][3])