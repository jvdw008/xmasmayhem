import math

# Enemy bullet class
class EnemyBullet:
    def __init__(self, fromPos, toPos, enemyBulletSpeed, settings):
        self.fromX = fromPos[0]
        self.fromY = fromPos[1]
        self.toX = toPos[0] + 40
        self.toY = toPos[1] + 20
        self.speed = enemyBulletSpeed
        self.angle = math.atan2(self.toY - self.fromY, self.toX - self.fromX)
        self.settings = settings

    # Calculate movement
    def update(self):
        # return True/False based on if bullet still on screen
        self.fromX += math.cos(self.angle) * self.speed
        self.fromY += math.sin(self.angle) * self.speed
        if (self.fromX < -20 * self.settings.res_scale):
            return False
        if (self.fromY < -20 * self.settings.res_scale):
            return False

        return True

    def draw(self, screen, img):
        screen.blit(img, (self.fromX, self.fromY))

    def checkCollision(self, x, y):
        if (self.fromX > x and self.fromX < x + 20 * self.settings.res_scale):
            if (self.fromY > y and self.fromY < y + 20 * self.settings.res_scale):
                return True
        return False

