# Animation class

import pygame

class Animation:
    def __init__(self, settings, screen, spriteObj, spriteParams, loop, log):
        self.screen = screen
        self.settings = settings
        self.sprite = spriteObj
        self.frameStart = spriteParams[0]
        self.frames = spriteParams[1]
        self.frameCount = 0
        self.speed = spriteParams[2]
        self.frameTime = spriteParams[2]
        self.animationPause = 0
        self.animationPauseMax = spriteParams[3]
        self.loop = loop
        self.log = log
        if (self.settings.log_setting == 3):
            self.log.write("Init animations...")

    def update(self):
        if (self.settings.log_setting == 3):
            self.log.write(f"Anim frame time: {self.frameTime}")
            self.log.write(f"Anim frame number: {self.frameCount}")
        
        if (self.animationPause == 0):
            self.frameTime -= 1                             # Animation speed timer
            if (self.frameTime <= 0):                       # If timer is 0
                self.frameTime = self.speed                 # Reset timer
                self.frameCount += 1                        # Increase animation frame by 1
                if (self.frameCount >= self.frames):         # If animation frame is at the end
                    if (self.loop):                         # Check if loop animation is enabled
                        self.frameCount = self.frameStart   # Then set it back to the start frame
                    else:
                        self.frameCount = self.frames       # Otherwise leave it at the last frame
                    self.animationPause = self.animationPauseMax
        else:
            self.animationPause -= 1

    def draw(self, pos):
        if (self.settings.log_setting == 3):
            self.log.write(f"Drawing anim frame number: {self.frameCount}")
        self.screen.blit(self.sprite[self.frameCount], (pos))

    # Used for explosion animation
    def getFrame(self):
        return self.frameCount

    def resetFrame(self):
        self.frameCount = self.frameStart