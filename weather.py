# Snow particles

import pygame, random

class Weather:
    def __init__(self, settings, screen, log):
        self.settings = settings
        self.log = log
        self.screen = screen
        self.flakes = []
        self.flakeAmount = 25 * self.settings.res_scale

        for i in range(self.flakeAmount):
            # x, y, y speed, x speed, size
            self.flakes.append([random.randint(0, self.settings.screen_width * 2), random.randint(-50, self.settings.screen_height), random.randint(1, 3), random.randint(2, 5), random.randint(1, 2 * self.settings.res_scale)])

    # Reset flake position
    def resetFlakePosition(self, flakeId):
        self.flakes[flakeId][0] = random.randint(0, self.settings.screen_width * 2)     # x pos
        self.flakes[flakeId][1] = random.randint(-50, 0)   # y pos
        self.flakes[flakeId][2] = random.randint(1, 3)     # Y speed
        # Set up random global wind speed change
        randomGlobalWindSpeedParam = random.randint(1, 125 * self.settings.res_scale)
        if (randomGlobalWindSpeedParam > 480):
            self.flakes[flakeId][3] = 5 # X speed
        elif (randomGlobalWindSpeedParam > 300 and randomGlobalWindSpeedParam <= 480):
            self.flakes[flakeId][3] = 4
        elif (randomGlobalWindSpeedParam > 200 and randomGlobalWindSpeedParam <= 300):
            self.flakes[flakeId][3] = 3
        else:
            self.flakes[flakeId][3] = 2

        if (self.settings.log_setting == 3):
            self.log.write(f"flake {flakeId}: x: {self.flakes[flakeId][0]} y: {self.flakes[flakeId][1]}")

    def update(self, delta):
        for i in range(len(self.flakes)):
            if (self.flakes[i][0] < 0 or self.flakes[i][1] > self.settings.screen_height):
                self.resetFlakePosition(i)
                next
            self.flakes[i][0] -= self.flakes[i][3] * delta
            self.flakes[i][1] += self.flakes[i][2] * delta
            # if (self.settings.log_setting == 3):
            #     self.log.write(f"flake {i}: x: {self.flakes[i][0]} y: {self.flakes[i][1]}")

    def draw(self):
        for i in range(len(self.flakes)):
            pygame.draw.circle(self.screen, [255, 255, 255], [self.flakes[i][0], self.flakes[i][1]], self.flakes[i][4])
