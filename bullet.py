import random

# Player bullet class - uses gravity
class Bullet:
    def __init__(self, screen, settings, log):
        self.screen = screen
        self.settings = settings
        self.bullets = []
        self.log = log

    def addBullet(self, pos, gravity):
        if (len(self.bullets) < 3):
            x = self.settings.bulletStartX + pos[0] + random.randint(0, 10)
            y = self.settings.bulletStartY + pos[1] + random.randint(0, 10)
            self.bullets.append([x, y, float(gravity)])
            if (self.settings.log_setting == 3):
                self.log.write(f"Added player bullet at: {x, y} position")

    def update(self, delta):
        self.deleteIndex = []
        for i in range(len(self.bullets)):
            self.bullets[i][0] += self.settings.bulletSpeed * delta
            self.bullets[i][2] += self.settings.bulletGravity * delta
            self.bullets[i][1] += self.bullets[i][2] * delta
            if (self.bullets[i][0] > self.settings.screen_width) or (self.bullets[i][1] > self.settings.screen_height):
                self.deleteIndex.append(i)

        if (len(self.deleteIndex) > 0):
            for i in range(len(self.deleteIndex)):
                self.deleteBullet(i)

    def deleteBullet(self, index):
        for i in range(len(self.bullets)):
            if (i == index):
                if (self.settings.log_setting == 3):
                    self.log.write(f"Deleting player bullet {i}")
                self.bullets.pop(index)
                break

    def draw(self, img):
        for i in range(len(self.bullets)):
            self.screen.blit(img, (self.bullets[i][0], self.bullets[i][1]))

    def checkCollision(self, x, y):
        for i in range(len(self.bullets)):
            if (self.bullets[i][0] > x and self.bullets[i][0] < x + 12 * self.settings.res_scale):
                if (self.bullets[i][1] > y and self.bullets[i][1] < self.settings.screen_height):
                    self.deleteIndex.append(i)
                    self.deleteBullet(i)
                    return True
        return False

    def getBulletCount(self):
        return len(self.bullets)