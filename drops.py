# Enemy drops

class Drops:
    def __init__(self, screen, enemyPos, img, imgIndex, settings, log):
        self.screen = screen
        self.x = enemyPos[0]
        self.y = enemyPos[1]
        self.img = img
        self.imgIndex = imgIndex
        self.settings = settings
        self.log = log
        if (self.settings.log_setting == 3):
            self.log.write(f"Added player gift drop at: {self.x, self.y} position")

    def update(self):
        self.x -= 2
        self.y -= 1
        return self.imgIndex

    def getPos(self):
        return [self.x, self.y]

    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))