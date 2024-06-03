import pygame, os

class Bars:
    def __init__(self, xmas_mayhem_game, settings, log):
        self.screen = xmas_mayhem_game.screen
        self.settings = settings
        self.log = log
        self.barY = 6
        self.barX1, self.barX2,self.barX3 = 50, 130, 206
        
        barFilePath = os.path.join(os.getcwd(), "data")
        barImg = self.settings.bar_bg_file
        
        barFile = os.path.join(barFilePath, barImg)
        if (self.settings.log_setting < 3):
            self.log.write(f"loading background file {barFile}")

        try: 
            self.bar = pygame.image.load(os.path.join(os.getcwd(), "data", barFile)).convert()
            self.rect = self.bar.get_rect()
            self.x_scale = self.rect.width * self.settings.res_scale
            self.y_scale = self.rect.height * self.settings.res_scale
            self.bar = pygame.transform.scale(self.bar, (self.x_scale, self.y_scale))

        except IOError:
            if (self.settings.log_setting < 3):
                self.log.write(f"Unable to load bar image: {barFile}")
            return

    def draw(self):
        self.screen.blit(self.bar, (self.barX1 * self.settings.res_scale, self.barY * self.settings.res_scale))
        self.screen.blit(self.bar, (self.barX2 * self.settings.res_scale, self.barY * self.settings.res_scale))
        self.screen.blit(self.bar, (self.barX3 * self.settings.res_scale, self.barY * self.settings.res_scale))