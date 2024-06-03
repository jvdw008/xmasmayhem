import pygame, os

class Background:
    def __init__(self, xmas_mayhem_game, settings, log):
        self.screen = xmas_mayhem_game.screen
        self.settings = settings
        self.log = log
        self.bgX, self.fg01X, self.fg02X = 0, 0, 0
        
        bgFilePath = os.path.join(os.getcwd(), "data")
        bg01Img = self.settings.bg01_file
        fg01Img = self.settings.fg01_file
        fg02Img = self.settings.fg02_file
        splashImg = self.settings.splash_file
        
        bgFile = os.path.join(bgFilePath, bg01Img)
        fg01File = os.path.join(bgFilePath, fg01Img)
        fg02File = os.path.join(bgFilePath, fg02Img)
        splashFile = os.path.join(bgFilePath, splashImg)
        if (self.settings.log_setting < 3):
            self.log.write(f"loading background file {bgFile}")
            self.log.write(f"loading foreground 1 file {fg01File}")
            self.log.write(f"loading foreground 2 file {fg02File}")
            self.log.write(f"loading menu screen file {splashFile}")

        try: 
            self.bg = pygame.image.load(os.path.join(os.getcwd(), "data", bgFile)).convert()
            self.rect = self.bg.get_rect()
            self.x_scale = self.rect.width * self.settings.res_scale
            self.y_scale = self.rect.height * self.settings.res_scale
            self.bg = pygame.transform.scale(self.bg, (self.x_scale, self.y_scale))

        except IOError:
            if (self.settings.log_setting < 3):
                self.log.write(f"Unable to load background image: {bgFile}")

        try: 
            self.fg01 = pygame.image.load(os.path.join(os.getcwd(), "data", fg01File)).convert()
            self.rect = self.fg01.get_rect()
            self.x_scale = self.rect.width * self.settings.res_scale
            self.y_scale = self.rect.height * self.settings.res_scale
            self.fg01 = pygame.transform.scale(self.fg01, (self.x_scale, self.y_scale))

        except IOError:
            if (self.settings.log_setting < 3):
                self.log.write(f"Unable to load foreground 1 image: {fg01File}")

        try: 
            self.fg02 = pygame.image.load(os.path.join(os.getcwd(), "data", fg02File)).convert()
            self.rect = self.fg02.get_rect()
            self.x_scale = self.rect.width * self.settings.res_scale
            self.y_scale = self.rect.height * self.settings.res_scale
            self.fg02 = pygame.transform.scale(self.fg02, (self.x_scale, self.y_scale))

        except IOError:
            if (self.settings.log_setting < 3):
                self.log.write(f"Unable to load foreground 2 image: {fg02File}")

        try: 
            self.splash = pygame.image.load(os.path.join(os.getcwd(), "data", splashFile)).convert()
            self.rect = self.splash.get_rect()
            self.x_scale = self.rect.width * self.settings.res_scale
            self.y_scale = self.rect.height * self.settings.res_scale
            self.splash = pygame.transform.scale(self.splash, (self.x_scale, self.y_scale))

        except IOError:
            if (self.settings.log_setting < 3):
                self.log.write(f"Unable to load splash screen image: {splashFile}")

    def update(self):
        if (self.settings.log_setting == 3):
            self.log.write(f"Updating background image x: {self.bgX} foreground image 1 x: {self.fg01X} foerground image 2 x: {self.fg02X}")
        self.bgX -= self.settings.backgroundSpeed
        self.fg02X -= self.settings.backgroundSpeed * 1.25
        self.fg01X -= self.settings.backgroundSpeed * 2
        if (self.bgX <= -self.settings.screen_width * 2):
            self.bgX = 0
        if (self.fg02X <= -self.settings.screen_width):
            self.fg02X = 0
        if (self.fg01X <= -self.settings.screen_width * 2):
            self.fg01X = 0

    def draw(self):
        self.screen.blit(self.bg, (self.bgX, 0))
        # Add 2nd blit to offset sky to not glitchj
        self.screen.blit(self.bg, (self.bgX + self.settings.screen_width * 2, 0))
        self.screen.blit(self.bg, (self.bgX, 0))
        self.screen.blit(self.fg02, (self.fg02X, 0))
        self.screen.blit(self.fg01, (self.fg01X, 0))
        # Added 2nd blit offset so trees don't look like they glitch
        self.screen.blit(self.fg01, (self.fg01X + self.settings.screen_width * 2, 0))

    def showSplash(self):
        self.screen.blit(self.splash, (0, 0))