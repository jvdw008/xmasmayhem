import pygame
from enemyBullet import EnemyBullet

class Enemy:
    def __init__(self, settings, log):
        self.settings = settings
        self.enemies = []
        self.bullets = []
        self.log = log

    # enemyNumber 1 = snowman, 2 = grinch
    def addEnemy(self, x, enemyNumber):
        self.enemies.append([x, self.settings.screen_height - (48 * self.settings.res_scale), self.settings.enemyHealth, enemyNumber, self.settings.bulletTimerMax])

    def update(self, playerPos, playerState):
        self.deleteIndex = []
        for i in range(len(self.enemies)):
            self.enemies[i][0] -= self.settings.backgroundSpeed * 3

            # Out of screen? Mark for deletion
            if (self.enemies[i][0] < -200):
                self.deleteIndex.append(i)

            # While enemy X is larger than settings.enemyLeftX, move reduce ammo timer
            if (self.enemies[i][0] > self.settings.enemyLeftX and self.enemies[i][0] < self.settings.screen_width):
                if (self.enemies[i][4] > 0):
                    self.enemies[i][4] -= 1
                # Else add a bullet aimed at player, then reset bullet timer
                else:
                    if (playerState > 0):   # Check player is still alive
                        if (self.settings.log_setting == 3):
                            self.log.write(f"Enemy created bullet at: {self.enemies[i][0], self.enemies[i][1]} position")
                        self.addBullet((self.enemies[i][0], self.enemies[i][1]), playerPos, self.enemies[i][3])
                        pygame.mixer.Sound.play(self.settings.snd_enemyShoot)
                        # If snowman
                        if (self.enemies[i][3] == 0):
                            self.enemies[i][4] = self.settings.bulletTimerMax * 2
                        # Else grinch
                        else:
                            self.enemies[i][4] = self.settings.bulletTimerMax * 1.5

        if (len(self.deleteIndex) > 0):
            for j in range(len(self.deleteIndex)):
                self.deleteEnemy(j)

        # Update enemy bullets
        self.updateBullets()

    def deleteEnemy(self, index):
        if (self.settings.log_setting == 3):
            self.log.write(f"Deleting enemy {index}")
        self.enemies.pop(index)

    def getPos(self):
        onScreenEnemyList = []
        for i in range(len(self.enemies)):
            if (int(self.enemies[i][0]) > -200 and int(self.enemies[i][0]) < self.settings.screen_width):
                onScreenEnemyList.append([self.enemies[i][0], self.enemies[i][1], self.enemies[i][3]])

        return onScreenEnemyList

    def addBullet(self, fromPos, toPos, type):
        self.bullets.append([EnemyBullet(fromPos, toPos, self.settings.enemyBulletSpeed, self.settings), type])

    # Move bullets from enemy to player
    def updateBullets(self):
        self.deleteEnemyBulletsIndex = []
        for i in range(len(self.bullets)):
            result = self.bullets[i][0].update()
            if (result == False):
                self.deleteEnemyBulletsIndex.append(i)
        
        if (len(self.deleteEnemyBulletsIndex) > 0):
            for i in range(len(self.deleteEnemyBulletsIndex)):
                self.deleteEnemyBullets(i)

    def deleteEnemyBullets(self, index):
        for i in range(len(self.bullets)):
            if (index == i):
                del self.bullets[index]
                break

    def drawBullet(self, screen, img):
        for i in range(len(self.bullets)):
            if (int(self.bullets[i][1]) == 0):
                self.bullets[i][0].draw(screen, img[self.settings.SNOWBALL])
            else:
                self.bullets[i][0].draw(screen, img[self.settings.COAL])

    def checkBulletCollisions(self, playerPos):
        for i in range(len(self.bullets)):
            # Has this bullet his player?
            if (self.bullets[i][0].checkCollision(playerPos[0], playerPos[1])):
                if (self.settings.log_setting == 3):
                    self.log.write(f"Enemy bullet has hit player")
                self.deleteEnemyBullets(i)
                return True

        return False